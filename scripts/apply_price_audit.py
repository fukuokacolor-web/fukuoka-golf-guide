#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
価格カード第2段: price_audit_2026-07.json の じゃらん検証値を全courseの価格カードへ適用。

- 平日カード (label に WEEKDAY・LOWEST を含まない)  → ¥{weekday}〜  (null なら中立化)
- 土日カード (label に WEEKEND/HOLIDAY)             → ¥{weekend}〜  (null なら中立化)
- featured/午後スルー (AFTERNOON / LOWEST / SPECIAL) → 常に中立化 (裏取り不能・Decoy=NO)
- 料金セクション説明に「2026年7月時点のじゃらん調べ」を明記 (3言語)

言語は c-ja / c-en / c-ko の出現位置で判定し、中立化文言をローカライズ。
冪等: price-amount に ¥ 数値が無ければスキップ。--dry-run 対応・両ROOT書き込み。
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
DRY = "--dry-run" in sys.argv

NEUTRAL_FEATURED = {"ja": "設定日限定", "en": "Limited dates", "ko": "지정일 한정"}
NEUTRAL_UNKNOWN  = {"ja": "予約サイトで確認", "en": "Check booking site", "ko": "예약 사이트에서 확인"}

SEC_DESC = {
    "平日・土日祝・午後スルーを横並びで比較。価格は目安。最新のベストレートは予約サイトでご確認ください。":
        "平日・土日祝を横並びで比較。掲載料金は<strong>2026年7月時点のじゃらんゴルフ調べ</strong>の最安値で、"
        "時期・プラン・カートや昼食の有無により変動します。最新のベストレートは予約サイトでご確認ください。",
    "Weekday, weekend, and afternoon-through rates side by side. Prices are indicative — check the booking sites for the latest best rate.":
        "Weekday and weekend rates side by side. Figures are the lowest rates found on Jalan Golf as of July 2026 "
        "and vary by season, plan, cart and meal options. Check the booking sites for the latest best rate.",
    "평일·주말·오후 스루 3가지 플랜을 나란히 비교. 최신 요금은 예약 사이트에서 확인해 주세요.":
        "평일·주말 요금을 나란히 비교. 게재 요금은 2026년 7월 시점 자란골프 기준 최저가이며, "
        "시즌·플랜에 따라 변동합니다. 최신 요금은 예약 사이트에서 확인해 주세요.",
}

# price-card ブロック: label と price-amount を持つ最小単位
CARD_RE = re.compile(
    r'(<div class="price-card-label">([^<]*)</div>.*?)'
    r'(<div class="price-amount"[^>]*>.*?</div>)',
    re.S,
)
HAS_PRICE = re.compile(r'¥</span>[0-9,]+|¥[0-9,]+')


def lang_at(html, pos):
    """pos がどの言語ブロックか (c-ja/c-en/c-ko の直近の開始位置で判定)"""
    best, lang = -1, "ja"
    for key, code in (('id="c-ja"', "ja"), ('id="c-en"', "en"), ('id="c-ko"', "ko")):
        i = html.rfind(key, 0, pos)
        if i > best:
            best, lang = i, code
    return lang


# ★スコープ厳格化: 汎用テンプレのラベルのみ完全一致で対象にする。
# VISITOR/ MEMBER/ PLAN 01/ WINTER/ SEASON 等の手作りページは個別調査済の値なので
# 部分一致で巻き込まない (誤って検証済データを潰さないため)。
GENERIC_LABELS = {
    "WEEKDAY": "weekday",
    "WEEKEND / HOLIDAY": "weekend",
    "AFTERNOON THROUGH": "featured",
    "WEEKDAY LOWEST": "featured",
}


def classify(label):
    return GENERIC_LABELS.get(label.strip())


def amount_html(value):
    return f'<div class="price-amount"><span class="yen">¥</span>{value:,}<span class="range">〜</span></div>'


def neutral_html(text):
    return f'<div class="price-amount" style="font-size:19px;">{text}</div>'


def process(html, data):
    stats = {"weekday": 0, "weekend": 0, "featured": 0, "unknown": 0, "skip": 0}

    def repl(m):
        head, label, amount_div = m.group(1), m.group(2), m.group(3)
        kind = classify(label)
        if kind is None:
            return m.group(0)
        if not HAS_PRICE.search(amount_div):
            stats["skip"] += 1          # 既に中立化済 = 冪等
            return m.group(0)
        lang = lang_at(html, m.start())
        if kind == "featured":
            stats["featured"] += 1
            return head + neutral_html(NEUTRAL_FEATURED[lang])
        val = data.get(kind)
        if val is None:
            stats["unknown"] += 1
            return head + neutral_html(NEUTRAL_UNKNOWN[lang])
        stats[kind] += 1
        return head + amount_html(val)

    html = CARD_RE.sub(repl, html)
    for old, new in SEC_DESC.items():
        html = html.replace(old, new)
    return html, stats


def main():
    audit = json.load(open(os.path.join(REPO_ROOT, "price_audit_2026-07.json"), encoding="utf-8"))
    total = {"files": 0, "weekday": 0, "weekend": 0, "featured": 0, "unknown": 0, "skip": 0}
    print(f"モード: {'DRY-RUN' if DRY else '本番'}\n")
    for name, data in sorted(audit["courses"].items()):
        src = os.path.join(REPO_ROOT, name + ".html")
        if not os.path.exists(src):
            print(f"  [not_found] {name}")
            continue
        html = open(src, encoding="utf-8").read()
        new_html, st = process(html, data)
        touched = st["weekday"] + st["weekend"] + st["featured"] + st["unknown"]
        if new_html == html:
            continue
        total["files"] += 1
        for k in ("weekday", "weekend", "featured", "unknown", "skip"):
            total[k] += st[k]
        tag = "verified" if data.get("weekday") else "UNVERIFIED→中立化"
        print(f"  [change] {name:26} 平日{st['weekday']} 土日{st['weekend']} "
              f"featured{st['featured']} 不明{st['unknown']} skip{st['skip']}  ({tag})")
        if not DRY:
            for root in ROOTS:
                p = os.path.join(root, name + ".html")
                if os.path.exists(p):
                    open(p, "w", encoding="utf-8").write(new_html)

    print(f"\n=== SUMMARY ===")
    print(f"files: {total['files']} / 平日{total['weekday']} 土日{total['weekend']} "
          f"featured中立化{total['featured']} 不明中立化{total['unknown']} skip(冪等){total['skip']}")
    if DRY:
        print("※ DRY-RUN。本番は --dry-run を外す。")


if __name__ == "__main__":
    main()
