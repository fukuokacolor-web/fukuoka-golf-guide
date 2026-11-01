#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
エリア・ハブ等のコースカードの料金欄 (div.course-price) を 2026-11-01 のじゃらん実データに置き換える。

旧表示は「目安 ¥6,500〜14,000」等の出典・時点不明の範囲で、確認できる値と大きくずれていた
(浮羽¥4,060・皐月竜王¥3,332・西戸崎/久山¥3,500 等。西戸崎はじゃらん予約不可)。
- 料金: scripts/.cache/jalan_floor.json (直近14日の18H最安・プラン料金。コースページの予約カードと同じ基準)
- 予約サイトで予約できないコース (CLAUDE.md §9.4) は金額を出さず「公式サイトで確認」「楽天で確認」
- じゃらんに平日の販売が無い/データ無しは「予約サイトで確認」
カード内の紹介文 (course-desc) の金額は文ごとに書き方が違うので、このスクリプトでは触らない (別途)。
冪等: 生成結果が同じなら no-op。
Usage:
  python scripts/fix_card_prices_2026_11.py                       # dry-run (全ページ)
  python scripts/fix_card_prices_2026_11.py --only area-chikuho.html --preview   # 1件テスト: PREVIEW だけ
  python scripts/fix_card_prices_2026_11.py --apply               # REPO + PREVIEW
"""
import os, re, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
CHECKED = "2026-11-01"

PAGES = ["area-chikugo.html", "area-chikuho.html", "area-fukuokacity.html", "area-itoshima.html", "area-kitakyushu.html",
         "book-fukuoka-golf-foreigner.html", "hub-beginner.html", "hub-budget.html", "hub-business.html", "hub-traveler.html"]
OFFICIAL_ONLY = {"fukuokacc", "wakamatsu", "genkai", "koga", "moji", "classic", "kokura", "queenshill", "raizan", "keya"}
RAKUTEN_ONLY = {"aburayama", "kyushugc", "saitozaki", "akane", "yasukogen", "sunlake"}

NOTE = '<span style="display:block;font-size:11px;font-weight:400;opacity:.75;">{t}</span>'
TXT = {
    "ja": {"wd": "平日", "we": "土日祝", "suf": "〜", "note": "じゃらん・2026年11月1日時点の18H最安（変動あり）",
           "official": "料金は公式サイトで確認", "rakuten": "料金は楽天GORAで確認", "none": "料金は予約サイトで確認"},
    "en": {"wd": "Wkdy", "we": "Wknd", "suf": "", "note": "Jalan, lowest 18-hole plan as of Nov 1, 2026 (varies)",
           "official": "Rates on the official site", "rakuten": "Rates on Rakuten GORA", "none": "Rates on the booking site"},
    "ko": {"wd": "평일", "we": "주말", "suf": "〜", "note": "자란 · 2026년 11월 1일 기준 18홀 최저가(변동 있음)",
           "official": "요금은 공식 사이트에서 확인", "rakuten": "요금은 라쿠텐 GORA에서 확인", "none": "요금은 예약 사이트에서 확인"},
}
PRICE_RE = re.compile(r'<div class="course-price">(?:(?!</div>).)*</div>', re.S)
LANG_RE = re.compile(r'<div id="c-(ja|en|ko)" class="content')


def load():
    mapping = {c["file"].replace("course-", ""): c.get("jalan_id")
               for c in json.load(open(os.path.join(REPO_ROOT, "jalan_golf_mapping.json"), encoding="utf-8"))["courses"]}
    floor = json.load(open(os.path.join(REPO_ROOT, "scripts/.cache/jalan_floor.json"), encoding="utf-8"))
    data = {}
    for slug, jid in mapping.items():
        r = floor.get(str(jid).zfill(5)) if jid else None
        if r:
            assert r["checked"] == CHECKED, (slug, r["checked"])
        data[slug] = r
    return data


def render(slug, lang, data):
    t = TXT[lang]
    if slug in OFFICIAL_ONLY:
        return f'<div class="course-price">{t["official"]}</div>'
    if slug in RAKUTEN_ONLY:
        return f'<div class="course-price">{t["rakuten"]}</div>'
    r = data.get(slug)
    if not r or not r.get("weekday"):
        return f'<div class="course-price">{t["none"]}</div>'
    s = f'{t["wd"]} <strong>¥{r["weekday"]["price"]:,}{t["suf"]}</strong>'
    if r.get("weekend"):
        s += f' / {t["we"]} ¥{r["weekend"]["price"]:,}{t["suf"]}'
    return f'<div class="course-price">{s}{NOTE.format(t=t["note"])}</div>'


def fix(html, data, log):
    out, last = [], 0
    for m in PRICE_RE.finditer(html):
        before = html[:m.start()]
        langs = LANG_RE.findall(before)
        lang = langs[-1] if langs else "ja"
        card_start = max(before.rfind('class="course-card'), before.rfind("<article"))
        slug = re.findall(r'href="course-([a-z0-9-]+)\.html[#"]', html[card_start:m.start()])
        assert slug, ("slug", m.group(0)[:60])
        new = render(slug[-1], lang, data)
        log.append((slug[-1], lang, re.sub(r"<[^>]+>", "", m.group(0))[:40], re.sub(r"<[^>]+>", " ", new)[:60]))
        out.append(html[last:m.start()] + new)
        last = m.end()
    return "".join(out) + html[last:]


DESC_RE = re.compile(r'(<div class="course-desc">)(.*?)(</div>)', re.S)
CHIP_PRICE_RE = re.compile(r'[ \t]*<span class="course-chip[^"]*">[^<]*[¥￥][^<]*</span>\r?\n?')
YEN = re.compile(r"[¥￥]|[0-9,]+円")


def drop_price_sentences(html, log):
    """紹介文の金額入りの文と、金額入りのチップを外す (料金は料金欄に一本化)。タグが文をまたぐ場合は手作業用に記録だけ"""
    def desc_sub(m):
        body = m.group(2)
        if not YEN.search(body):
            return m.group(0)
        parts = [p for p in re.split(r"(?<=。)|(?<=[.!?;])\s+", body) if p.strip()]
        keep = [p for p in parts if not YEN.search(p)]
        drop = [p for p in parts if YEN.search(p)]
        if any(p.count("<") != p.count(">") or len(re.findall(r"<[a-z]", p)) != len(re.findall(r"</", p)) for p in drop) or not keep:
            log.append(("MANUAL", body[:80])); return m.group(0)
        sep = "" if "。" in body else " "
        new = re.sub(r"[;,、]$", lambda x: "。" if x.group(0) == "、" else ".", sep.join(k.strip() for k in keep).strip())
        log.append(("desc", "／".join(d.strip()[:50] for d in drop)))
        return m.group(1) + new + m.group(3)
    html = DESC_RE.sub(desc_sub, html)
    for c in CHIP_PRICE_RE.findall(html):
        log.append(("chip", re.sub(r"<[^>]+>|\s+", "", c)))
    return CHIP_PRICE_RE.sub("", html)


# 確認済の事実誤り (個別): セントラル福岡GCの所在地は筑紫野市大字山家 (じゃらん・コースページ JSON-LD)。
# 旧文の「朝倉郡・3万坪・原鶴温泉とセット・午後スルー対応」は根拠なし/誤り (11月はじゃらんで午前スルーのみ)
CENTRAL_DESC = {
    "ja": "筑紫野市（筑紫野ICから15km以内）の林間コース。アコーディア・ゴルフ運営。",
    "en": "A forest course in Chikushino City, within 15 km of Chikushino IC. Operated by Accordia Golf.",
    "ko": "지쿠시노시(지쿠시노 IC에서 15km 이내)의 숲 코스. 아코디아 골프 운영.",
}
CENTRAL_FIX = [("Asakura City · Forest · Featured", "Chikushino City · Forest · Featured"),
               ('<span class="course-chip earth">朝倉郡</span>', '<span class="course-chip earth">筑紫野市</span>'),
               ('<span class="course-chip earth">Asakura</span>', '<span class="course-chip earth">Chikushino</span>'),
               ('<span class="course-chip earth">아사쿠라군</span>', '<span class="course-chip earth">지쿠시노시</span>')]


def fix_central(html, log):
    def card_sub(m):
        c = m.group(0)
        if 'href="course-central.html"' not in c or not re.search(r"朝倉|Asakura|아사쿠라|Harazuru|原鶴|하라즈루", c):
            return c
        lang = (LANG_RE.findall(html[:m.start()]) or ["ja"])[-1]
        for a, b in CENTRAL_FIX:
            c = c.replace(a, b)
        c = DESC_RE.sub(lambda d: d.group(1) + CENTRAL_DESC[lang] + d.group(3), c, count=1)
        log.append(("central", lang))
        return c
    return re.sub(r'<article class="course-card[^"]*">.*?</article>', card_sub, html, flags=re.S)


def main():
    data = load()
    for name in PAGES:
        if ONLY and name != ONLY:
            continue
        src = open(os.path.join(REPO_ROOT, name), encoding="utf-8", newline="").read()
        log = []
        new = fix(src, data, log)
        dlog = []
        new = fix_central(new, dlog)
        new = drop_price_sentences(new, dlog)
        for d in dlog:
            if ONLY or d[0] == "MANUAL":
                print("    ", *d)
        if new == src:
            print(f"[already] {name}"); continue
        print(f"[change]  {name}  カード料金 {len(log)}")
        if ONLY or not APPLY:
            for l in log:
                if l[1] == "ja" or ONLY:
                    print("    ", l[0], l[1], "|", l[2], "→", l[3])
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(new)
    print("APPLIED " + ",".join(r[-12:] for r in ROOTS) if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
