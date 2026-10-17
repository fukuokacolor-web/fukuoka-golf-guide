#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
予約カード (booking-price-tag) と sticky CTA の料金表示を、検証済データに合わせて是正する (§7)。

入力: 検証データ JSON (例: price_audit_2026-09.json)
  { "<slug>": { "old": "¥4,000", "new": "¥6,319" | null,
                "note": {"ja": "...", "en": "...", "ko": "..."} | null }, ... }
  - new が値      → じゃらんカード・sticky の旧額を new に置換
  - new が null   → 検証できないので金額を外す (「料金は 予約ページで確認」表記)・前回の注記も削除
  - 楽天GORAカード → 料金を機械検証できないため常に金額を外す (「料金は 楽天で確認」)
  - note          → 各言語の予約セクション説明の直後に変動注記 (p.fee-note) を挿入
  - hero バッジ / 「¥X〜 Lowest Fee」stat が残っていれば Policy C と同じ表記に統一

冪等: 処理後は旧額が消え、fee-note は同じ文面で上書きされるので、再実行は no-op。
既に fee-note があるページ (前回点検済) は、注記を新しい文面に書き換える。
Usage:
  python scripts/fix_booking_price_tags.py price_audit_2026-09.json            # dry-run
  python scripts/fix_booking_price_tags.py price_audit_2026-09.json --apply    # 両ディレクトリに書き込み
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
APPLY = "--apply" in sys.argv

CARD_RE = re.compile(r'(<a href="(?P<href>[^"]+)" class="booking-card"[^>]*>)(?P<body>.*?)(</a>)', re.S)
TAG_RE = re.compile(r'<div class="booking-price-tag">.*?</div>', re.S)
STICKY_RE = re.compile(r'(class="sc-btn sc-jalan"[^>]*>)([^<]*)(</a>)')
MARKER = 'class="fee-note"'

# 言語はカードが属する content ブロック (c-ja / c-en / c-ko) で判定する
LANG_BLOCK_RE = re.compile(r'<div id="c-(ja|en|ko)" class="content')

TAG_RAKUTEN = {"ja": '<div class="booking-price-tag">料金は <span class="big">楽天で確認</span></div>',
               "en": '<div class="booking-price-tag">Rates <span class="big">on Rakuten</span></div>',
               "ko": '<div class="booking-price-tag">요금은 <span class="big">라쿠텐에서 확인</span></div>'}
# じゃらん側に料金が出ていない (予約カレンダー無し/直近の販売プラン無し) コースもあるため中立表記にする
TAG_JALAN_UNVERIFIED = {"ja": '<div class="booking-price-tag">料金は <span class="big">予約ページで確認</span></div>',
                        "en": '<div class="booking-price-tag">Rates <span class="big">on booking page</span></div>',
                        "ko": '<div class="booking-price-tag">요금은 <span class="big">예약 페이지에서 확인</span></div>'}

DESC_RE = re.compile(r'(<p class="sec-desc" style="margin:0 auto 0;">[^<]*</p>)')
NOTE_P = '\n      <p class="fee-note" style="margin:10px auto 0;font-size:12px;opacity:.8;max-width:680px;">{t}</p>'
FEE_NOTE_RE = re.compile(r'(<p class="fee-note"[^>]*>)(.*?)(</p>)', re.S)
HUB_RE = re.compile(r'<section class="section-forest booking-hub">.*?</section>', re.S)

# Policy C と同一 (scripts/policyC_hero_price_to_booking.py)
HERO_RE = re.compile(r'<span class="hero-badge">💴[^<]*</span>')
HERO_NEW = '<span class="hero-badge">🌐 日本語・English・한국어</span>'
STAT_RE = re.compile(r'<div class="stat-item">\s*<div class="stat-num">¥[0-9,]+<span class="unit">〜</span></div>\s*'
                     r'<div class="stat-label">([^<]*)</div>\s*</div>')
STAT = {"ja": '<div class="stat-item"><div class="stat-num">2<span class="unit">サイト</span></div><div class="stat-label">予約サイト比較</div></div>',
        "en": '<div class="stat-item"><div class="stat-num">2<span class="unit">sites</span></div><div class="stat-label">Compare bookings</div></div>',
        "ko": '<div class="stat-item"><div class="stat-num">2<span class="unit">사이트</span></div><div class="stat-label">예약 사이트 비교</div></div>'}


def lang_at(html, pos):
    last = None
    for m in LANG_BLOCK_RE.finditer(html, 0, pos):
        last = m.group(1)
    return last or "ja"


def stat_lang(label):
    if re.search(r'[가-힣]', label): return "ko"
    if re.search(r'[぀-ヿ一-鿿]', label): return "ja"
    return "en"


def fix(html, spec):
    old, new, note = spec["old"], spec.get("new"), spec.get("note")
    log = {"jalan_card": 0, "rakuten_card": 0, "sticky": 0, "note": 0, "note_updated": 0, "note_removed": 0, "hero": 0, "stat": 0}

    def card_sub(m):
        href, body = m.group("href"), m.group("body")
        lang = lang_at(html, m.start())
        tag = TAG_RE.search(body)
        if not tag or old not in tag.group(0):
            return m.group(0)
        if "rakuten" in href:
            log["rakuten_card"] += 1
            body = body.replace(tag.group(0), TAG_RAKUTEN[lang])
        elif "golf-jalan" in href:
            log["jalan_card"] += 1
            body = body.replace(tag.group(0), tag.group(0).replace(old, new) if new else TAG_JALAN_UNVERIFIED[lang])
        else:
            return m.group(0)
        return m.group(1) + body + m.group(4)

    html = CARD_RE.sub(card_sub, html)

    def sticky_sub(m):
        if old not in m.group(2):
            return m.group(0)
        log["sticky"] += 1
        text = m.group(2).replace(old, new) if new else re.sub(r"\s*" + re.escape(old) + r"〜?", "", m.group(2))
        return m.group(1) + text + m.group(3)

    html = STICKY_RE.sub(sticky_sub, html)

    n = len(HERO_RE.findall(html)); log["hero"] = n
    html = HERO_RE.sub(HERO_NEW, html)
    log["stat"] = len(STAT_RE.findall(html))
    html = STAT_RE.sub(lambda m: STAT[stat_lang(m.group(1))], html)

    # 予約セクション (booking-hub) 内だけを対象にする。言語は hub の位置で判定
    def hub_sub(hub):
        lang = lang_at(html, hub.start())
        text = (note or {}).get(lang)
        body = hub.group(0)
        if not text:
            # 今回は料金を確認できない → 前回点検の注記が残っていれば古い情報なので削除
            # \r?\n: CRLF のファイルで \r だけ残すと行末が \r\r\n に壊れる (2026-10-18 queenshill で発生)
            new_body = re.sub(r'\r?\n[ \t]*<p class="fee-note"[^>]*>.*?</p>', "", body, count=1, flags=re.S)
            if new_body != body:
                log["note_removed"] += 1
            return new_body
        if MARKER in body:  # 既存の注記を最新内容に書き換え (前回点検分の更新)
            new_body = FEE_NOTE_RE.sub(lambda m: m.group(1) + text + m.group(3), body, count=1)
            if new_body != body:
                log["note_updated"] += 1
            return new_body
        log["note"] += 1
        nl = "\r\n" if "\r\n" in body else "\n"  # ファイルの改行コードに合わせる
        return DESC_RE.sub(lambda m: m.group(1) + NOTE_P.format(t=text).replace("\n", nl), body, count=1)

    html = HUB_RE.sub(hub_sub, html)
    return html, log


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    data = json.load(open(args[0], encoding="utf-8"))
    print(f"モード: {'本番 (両ディレクトリ書き込み)' if APPLY else 'DRY-RUN (書き込みなし)'}\n")
    total = {"changed": 0, "already": 0, "leftover": 0}
    for slug, spec in data.items():
        if slug.startswith("_"):
            continue
        f = f"course-{slug}.html"
        html = open(os.path.join(REPO_ROOT, f), encoding="utf-8", newline="").read()  # 改行コード (LF/CRLF 混在) を保持
        new_html, log = fix(html, spec)
        if new_html == html:
            total["already"] += 1
            print(f"  [already] {f}")
            continue
        left = new_html.count(spec["old"])
        total["changed"] += 1
        total["leftover"] += left
        flag = "  ⚠ 旧額が残存" if left else ""
        print(f"  [change] {f:28} {spec['old']}→{spec.get('new') or '(金額を外す)':10} "
              + " ".join(f"{k}×{v}" for k, v in log.items() if v) + f"  残{left}{flag}")
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, f), "w", encoding="utf-8", newline="").write(new_html)
    print(f"\n結果: {total}")


if __name__ == "__main__":
    main()
