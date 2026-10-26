#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html (JA/EN/KO) の古い料金・根拠のない割合を是正する (§7)。

根拠: cheap_guide_prices.json / scripts/.cache/jalan_floor.json (じゃらん・2026-10-24・直近14日の平日18H最安の総額)
- コスパランキング Top 5 を確認データの安い順で作り直す (旧: 浮羽¥4,060 等・所在地の誤り「フェザント=古賀市」「あかね=朝倉市・27H」)
- FAQ「一番安いゴルフ場」(JSON-LD + 表示 3言語) を確認データに
- 平日と土日祝の差: 32コースの中央値 1.54倍 (1.11〜2.38倍) に
- 根拠のない「午後スルーは通常の60-70%」「ハイシーズン+30-40%」「Web予約で平均¥3,000お得」を削除
Usage:
  python scripts/fix_index_prices_2026_10.py            # dry-run
  python scripts/fix_index_prices_2026_10.py --apply    # REPO + PREVIEW
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv
F = "index.html"

CH = json.load(open(os.path.join(REPO_ROOT, "cheap_guide_prices.json"), encoding="utf-8"))
C = {c["slug"]: c for c in CH["courses"]}
TOP = sorted(CH["courses"], key=lambda c: (c["wk_total"], c["slug"]))[:5]
yen = lambda n: f"¥{n:,}"

NAMES = {  # course ページの hero-title (JA / EN / KO)
    "satsuki-ryuoh": ("皐月GC 竜王コース", "Satsuki GC Ryuoh Course", "사쓰키 GC 류오 코스"),
    "pheasant": ("福岡フェザントCC", "Fukuoka Pheasant CC", "후쿠오카 페전트 CC"),
    "takaha": ("鷹羽ロイヤルCC", "Takaha Royal CC", "타카하 로열 CC"),
    "central": ("セントラル福岡GC", "Central Fukuoka GC", "센트럴 후쿠오카 GC"),
    "kaho": ("かほGC", "Kaho GC", "카호 GC"),
    "chisan-onga": ("チサン遠賀CC", "Chisan Onga CC", "치산 온가 CC"),
}
LOC = {"飯塚市": ("飯塚市", "Iizuka", "이이즈카시"), "田川郡": ("田川郡", "Tagawa", "다가와군"),
       "筑紫野市": ("筑紫野市", "Chikushino", "지쿠시노시"), "遠賀郡遠賀町": ("遠賀郡", "Onga", "온가군")}
CHECKED = {"ja": "2026年10月24日確認", "en": "checked Oct 24, 2026", "ko": "2026년 10월 24일 확인"}
LI = ('            <li class="ranking-item">\n              <span class="rank-num">{n}</span>\n              <div class="rank-content">\n'
      '                <div class="rank-name"><a href="course-{slug}.html">{name}</a><span class="rank-badge">{badge}</span></div>\n'
      '                <div class="rank-meta">{meta}</div>\n              </div>\n            </li>\n')


def ranking(lang):
    k = {"ja": 0, "en": 1, "ko": 2}[lang]
    out = ""
    for i, c in enumerate(TOP, 1):
        badge = {"ja": f"{yen(c['wk_total'])}〜", "en": f"From {yen(c['wk_total'])}", "ko": f"{yen(c['wk_total'])}부터"}[lang]
        loc = LOC[c["loc"]][k]
        meta = {"ja": f"{loc}・平日18ホール最安（じゃらん総額）", "en": f"{loc} · weekday 18-hole low (Jalan total)",
                "ko": f"{loc}·평일 18홀 최저가 (자란 총액)"}[lang]
        out += LI.format(n=i, slug=c["slug"], name=NAMES[c["slug"]][k], badge=badge, meta=meta)
    note = {"ja": f"※じゃらん「総額」・直近14日の平日最安（{CHECKED['ja']}）。料金は日々変わります。",
            "en": f"* Jalan total price, lowest weekday plan in the next 14 days ({CHECKED['en']}). Rates change daily.",
            "ko": f"※자란 총액·향후 14일 평일 최저가 ({CHECKED['ko']}). 요금은 매일 바뀝니다."}[lang]
    return ('<ol class="ranking-list">\n' + out + '          </ol>\n'
            f'          <div style="font-size:11px;color:var(--muted,#777);margin-top:8px;line-height:1.6;">{note}</div>')


def link(slug, lang, price=True):
    k = {"ja": 0, "en": 1, "ko": 2}[lang]
    p = yen(C[slug]["wk_total"])
    return f'<a href="course-{slug}.html">{NAMES[slug][k]}' + (f" {p}" if price else "") + "</a>"


R = TOP  # 短縮
CHEAP_JA = (f"じゃらんの総額で比べると、平日の最安は{link(R[0]['slug'],'ja',False)}（{yen(R[0]['wk_total'])}〜）、"
            f"{link(R[1]['slug'],'ja',False)}（{yen(R[1]['wk_total'])}〜）、{link(R[2]['slug'],'ja',False)}（{yen(R[2]['wk_total'])}〜）の順でした"
            f"（直近14日の18ホール・{CHECKED['ja']}）。料金は日々変わるので、詳細は<a href=\"book-fukuoka-cheap.html\">平日¥8,000以下で回れる9コース比較</a>へ。")
CHEAP_EN = (f"By Jalan total price, the cheapest weekday rounds were {link(R[0]['slug'],'en',False)} (from {yen(R[0]['wk_total'])}), "
            f"{link(R[1]['slug'],'en',False)} (from {yen(R[1]['wk_total'])}) and {link(R[2]['slug'],'en',False)} (from {yen(R[2]['wk_total'])}) "
            f"(18 holes, next 14 days, {CHECKED['en']}). Rates change daily — see the <a href=\"book-fukuoka-cheap.html\">budget comparison</a>.")
CHEAP_KO = (f"자란 총액 기준 평일 최저가는 {link(R[0]['slug'],'ko',False)}({yen(R[0]['wk_total'])}부터), "
            f"{link(R[1]['slug'],'ko',False)}({yen(R[1]['wk_total'])}부터), {link(R[2]['slug'],'ko',False)}({yen(R[2]['wk_total'])}부터) 순이었습니다"
            f"(향후 14일·18홀·{CHECKED['ko']}). 요금은 매일 바뀌므로 자세한 내용은 <a href=\"book-fukuoka-cheap.html\">저가 코스 비교</a>를 참고하세요.")
CHEAP_LD = re.sub(r"<[^>]+>", "", CHEAP_JA).replace("平日¥8,000以下で回れる9コース比較へ。", "格安ガイドへ。")

RATIO = {"ja": "の料金差は、じゃらんの総額で土日祝が平日の約1.5倍（32コースの中央値・2026年10月24日確認、コースにより1.1〜2.4倍）。",
         "en": " differ by about 1.5× by Jalan total price (median of 32 courses, checked Oct 24, 2026; 1.1–2.4× by course).",
         "ko": "의 요금 차이는 자란 총액 기준 주말이 평일의 약 1.5배 (32개 코스 중앙값·2026년 10월 24일 확인, 코스에 따라 1.1-2.4배)."}

REPS = [  # (正規表現, 置換, 期待件数)
    # --- 最安 FAQ (JSON-LD + 表示)
    (r'"text": "県内最安級は浮羽カントリークラブ[^"]*"', '"text": "' + CHEAP_LD + '"', 1),
    (r'(<div class="faq-a">)県内最安級は<a href="course-ukiha\.html">浮羽カントリークラブ</a>で、平日<strong>¥4,060〜</strong>.*?(</div>)', r"\g<1>" + CHEAP_JA + r"\g<2>", 1),
    (r'(<div class="faq-a">)<a href="course-ukiha\.html">Ukiha Country Club</a> at <strong>from ¥4,060</strong>.*?(</div>)', r"\g<1>" + CHEAP_EN + r"\g<2>", 1),
    (r'(<div class="faq-a">)현 내 최저가는 <a href="course-ukiha\.html">우키하 컨트리클럽</a>으로 평일 <strong>¥4,060부터</strong>.*?(</div>)', r"\g<1>" + CHEAP_KO + r"\g<2>", 1),
    # --- 平日と土日祝の差の段落
    (r'の料金差は平均1\.5〜2倍。出張・在宅ワーク併用で平日プレーすれば<a href="course-ukiha\.html">浮羽CC ¥4,060</a>・<a href="course-lakeside\.html">レイクサイド ¥6,000</a>級の安価ラウンドが可能。さらに<strong>午後スルー</strong>を活用すれば通常の60-70%でハーフ後そのまま18Hプレーでき、',
     RATIO["ja"] + f"出張・在宅ワーク併用で平日プレーすれば{link(R[0]['slug'],'ja')}・{link(R[1]['slug'],'ja')}（総額）から回れます。さらに<strong>午後スルー</strong>を活用すればハーフ後そのまま18Hプレーでき、", 1),
    (r' averages a 1\.5–2× gap\. Combine business trips with weekday play and you can play <a href="course-ukiha\.html">Ukiha at ¥4,060</a> or <a href="course-lakeside\.html">Lakeside at ¥6,000</a>\. Use <strong>Afternoon Through</strong> rounds \(continuing 18H without a break\) at 60–70% of normal rates — ',
     RATIO["en"] + f" Combine business trips with weekday play and you can play {link(R[0]['slug'],'en')} or {link(R[1]['slug'],'en')} (total). Use <strong>Afternoon Through</strong> rounds (continuing 18H without a break) — ", 1),
    (r'의 요금 차이는 평균 1\.5-2배\. 출장·재택 병행으로 평일 라운딩하면 <a href="course-ukiha\.html">우키하 CC ¥4,060</a>·<a href="course-lakeside\.html">레이크사이드 ¥6,000</a>급 저렴 라운딩 가능\. <strong>오후 스루</strong>를 활용하면 평소의 60-70%로 하프 후',
     RATIO["ko"] + f" 출장·재택 병행으로 평일 라운딩하면 {link(R[0]['slug'],'ko')}·{link(R[1]['slug'],'ko')}(총액)부터 가능. <strong>오후 스루</strong>를 활용하면 하프 후", 1),
    # --- 午後スルー FAQ の「60-70%」
    (r"料金は通常の60-70%程度に抑えられ、", "", 2),
    (r"Fees drop to 60–70% of standard rates and finish in half a day", "Rounds finish in half a day", 1),
    (r"요금은 통상의 60-70% 정도로 억제되며, ", "", 1),
    # --- 季節の「+30-40%」
    (r"ハイシーズンは料金が通常\+30-40%上昇します。", "", 1),
    (r"料金はハイシーズンで通常\+30-40%。", "", 2),
    (r"High-season fees run \+30–40% above base rates\. ", "", 1),
    (r"High-season fees rise \+30–40%\. ", "", 1),
    (r"성수기에는 평소 대비 \+30-40% 인상\. ", "", 1),
    (r"요금은 성수기에 통상 \+30-40%\. ", "", 1),
    # --- Web予約で平均¥3,000
    (r"Web予約で平均¥3,000お得になるケース多数。", "", 1),
    (r" ?Save ¥3,000 on average via web booking\.", "", 1),
    (r" ?웹 예약으로 평균 ¥3,000 절약 가능\.", "", 1),
    # --- ペルソナ紹介文
    (r"ショートコース・フラット・¥4,060〜。", "ショートコース・フラット中心。", 1),
    (r"Short layouts, flat fairways, fees from ¥4,060\.", "Short layouts and flat fairways.", 1),
    (r"짧은 코스·평탄·¥4,060부터\.", "짧은 코스·평탄 중심.", 1),
    (r"平日¥6,000・午後スルー・月曜セルフ¥7,880。", "平日割・午後スルーで賢く。", 1),
    (r"Weekday from ¥6,000, afternoon-thru, Monday self-play ¥7,880\.", "Weekday deals and afternoon-thru rounds.", 1),
    (r"평일 ¥6,000·오후 스루·월요일 셀프 ¥7,880\.", "평일 할인·오후 스루로 알뜰하게.", 1),
    # --- 筑豊エリア記事の抜粋 (筑豊の確認最安 = 皐月GC竜王 ¥5,400)
    (r"10コース・平日¥6,000〜のコスパ穴場。", f"10コース・平日{yen(C['satsuki-ryuoh']['wk_total'])}〜（総額・10/24確認）のコスパ穴場。", 1),
    (r"10 hidden-gem courses · Weekday ¥6,000〜\.", f"10 hidden-gem courses · Weekday from {yen(C['satsuki-ryuoh']['wk_total'])} (total, Oct 24).", 1),
    (r"10개 코스·평일 ¥6,000부터\.", f"10개 코스·평일 {yen(C['satsuki-ryuoh']['wk_total'])}부터(총액·10/24 확인).", 1),
]


def main():
    src = open(os.path.join(REPO_ROOT, F), encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    s = src.replace("\r\n", "\n")
    if "平日18ホール最安（じゃらん総額）" in s:
        print("[already]"); return
    for pat, rep, n in REPS:
        s, c = re.subn(pat, rep, s, flags=re.S)
        assert c == n, (pat[:50], c, n)
    # ランキング (3言語)
    for title, lang in (("コスパランキング Top 5", "ja"), ("Value Top 5", "en"), ("가성비 랭킹 Top 5", "ko")):
        i = s.index(f'<h3 class="ranking-title">{title}</h3>')
        a = s.index('<ol class="ranking-list">', i); b = s.index("</ol>", a) + len("</ol>")
        s = s[:a] + ranking(lang) + s[b:]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(b)
    body = re.sub(r"<script(?![^>]*ld\+json).*?</script>|<style.*?</style>", " ", s, flags=re.S)
    left = sorted(set(re.findall(r"¥4,060|浮羽CC ¥|60-70%|60–70%|\+30-40%|\+30–40%|1\.5〜2倍|1\.5–2×|1\.5-2배|平均¥3,000|古賀市・施設", body)))
    print("TOP5:", [(c["slug"], c["wk_total"]) for c in TOP], "| 残:", left)
    out = s.replace("\n", nl)
    if APPLY:
        for root in (REPO_ROOT, PREVIEW_ROOT):
            open(os.path.join(root, F), "w", encoding="utf-8", newline="").write(out)
    print("APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
