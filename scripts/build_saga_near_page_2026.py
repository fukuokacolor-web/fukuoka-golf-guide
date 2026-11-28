#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
「福岡から近い佐賀のゴルフ場」ページ saga-near-fukuoka.html を作る (日本語のみ)。
  対象 (2026-11-25 選定): じゃらんの佐賀県一覧 (住所) と楽天GORAのコース情報で、名前・住所・ホール数が一致したコース。
    鳥栖・みやき・神埼 (鳥栖IC・東脊振IC): ブリヂストンCC / 佐賀CC / 日の隈CC  + 9H: ウェルカムGC / 山水CC
    三瀬・佐賀大和 (佐賀大和IC): 北山CC / 大和不動CC / フジCC (じゃらんは予約カレンダーなし → 楽天のみ)
  料金: scripts/.cache/jalan_floor.json・gora_floor.json (jalan_floor.py / gora_floor.py --days 14) の18H最安 (税込総額)。
  コース情報: scripts/.cache/saga_rakuten_guide_2026-11-25.json (楽天GORAのコースガイド: 住所・ホール数・距離・パー・IC)。
  電話番号は載せない (佐賀CCでじゃらんと楽天の番号が違ったため)。
Usage: python scripts/build_saga_near_page_2026.py [--apply]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
R0 = ROOTS[0]
OUT = "saga-near-fukuoka.html"
C = os.path.join(R0, "scripts", ".cache")
JF = json.load(open(os.path.join(C, "jalan_floor.json"), encoding="utf-8"))
GF = json.load(open(os.path.join(C, "gora_floor.json"), encoding="utf-8"))
RG = json.load(open(os.path.join(C, "saga_rakuten_guide_2026-11-25.json"), encoding="utf-8"))

COURSES = [  # (key, 名前, エリア, じゃらんID or None, 楽天c_id, アクセス表記, ひとこと)
    ("bscc", "ブリヂストンカンツリー倶楽部", "tosu", "02366", "410013", "九州自動車道 鳥栖ICから10km以内", None),
    ("sagacc", "佐賀カントリー倶楽部", "tosu", "02376", "410002", "長崎自動車道 鳥栖ICから10km以内", None),
    ("hinokuma", "日の隈カンツリークラブ", "tosu", "02373", "410011", "長崎自動車道 東脊振ICから10km以内", None),
    ("kitayama", "北山カントリー倶楽部", "yamato", "02374", "410014", "長崎自動車道 佐賀大和ICから20km以内", None),
    ("yamatofudo", "大和不動カントリー倶楽部", "yamato", "02371", "410015", "長崎自動車道 佐賀大和ICから約5分", None),
    ("fuji", "フジカントリークラブ", "yamato", None, "410012", "長崎自動車道 佐賀大和ICから10km以内", "じゃらんには予約カレンダーがなく、ネット予約は楽天GORAです。"),
]
NINE = [
    ("welcome", "ウェルカムゴルフクラブ", "21013", "520385", "9ホール・パー27のショートコース（鳥栖市村田町）。じゃらん・楽天に「回り放題」のプランがあります。"),
    ("sansui", "山水カントリークラブ", "02375", "6389", "9ホールのコース（みやき町蓑原）。じゃらん・楽天に9ホールを2周する「18Hスルー」のプランがあります。"),
]
AREA = {"tosu": ("鳥栖・みやき・神埼", "長崎自動車道・九州自動車道の鳥栖IC・東脊振ICが最寄りのエリアです。"),
        "yamato": ("三瀬・佐賀大和", "佐賀市の三瀬村・富士町・大和町。長崎自動車道の佐賀大和ICが最寄りです。")}
JIDS = [c[3] for c in COURSES if c[3]] + [n[2] for n in NINE]
CHECKED = min(JF[j]["checked"] for j in JIDS)
y, m, d = CHECKED.split("-")
CHECKED_JA = f"{int(y)}年{int(m)}月{int(d)}日"
_a, _b = JF["02366"]["period"].split("/")
PERIOD = "〜".join(f"{int(x[5:7])}/{int(x[8:10])}" for x in (_a, _b))


def jalan_url(jid):
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


def floor(jid, cid):
    """平日・土日祝の最安 (税込総額) と空き日数。両サイトの安い方。"""
    res = {}
    for k in ("weekday", "weekend"):
        c = []
        if jid and JF.get(jid, {}).get(k):
            c.append((JF[jid][k]["total"], "じゃらん"))
        if GF.get(cid, {}).get(k):
            c.append((GF[cid][k]["total"], "楽天"))
        res[k] = min(c) if c else None
    days = max(JF.get(jid, {}).get("days_with_plans", 0) if jid else 0, GF.get(cid, {}).get("days_with_plans", 0))
    return res, days


def yen(v):
    return f"¥{v:,}"


def card(key, name, jid, cid, access, note):
    g = RG[cid]
    f, days = floor(jid, cid)
    wk = f"平日 <strong>{yen(f['weekday'][0])}〜</strong>" if f["weekday"] else "平日 <span class='sn-na'>直近の空きなし</span>"
    we = f"土日祝 <strong>{yen(f['weekend'][0])}〜</strong>" if f["weekend"] else "土日祝 <span class='sn-na'>直近の空きなし</span>"
    few = " <span class='sn-few'>空きが少なめ</span>" if 0 < days <= 3 else ""
    btns = f'<a href="{rakuten_url(cid)}" class="sn-btn sn-rak" target="_blank" rel="nofollow sponsored noopener">楽天GORAで予約</a>'
    if jid:
        btns += f'<a href="{jalan_url(jid)}" class="sn-btn sn-jal" target="_blank" rel="nofollow sponsored noopener">じゃらんで予約</a>'
    spec = f"{g['holes']}・パー{g['par']}・{g['yard']}" if g.get("yard") else g["holes"]
    return (f'<div class="sn-card"><div class="sn-name">{name}</div>'
            f'<div class="sn-meta">{g["addr"].replace("佐賀県 ", "佐賀県")}｜{spec}</div>'
            f'<div class="sn-meta">🚗 {access}</div>'
            + (f'<div class="sn-note">{note}</div>' if note else "")
            + f'<div class="sn-price">{wk}　{we}{few}</div>'
            f'<div class="sn-btns">{btns}</div></div>')


sections = []
for a in ("tosu", "yamato"):
    title, sub = AREA[a]
    cs = [c for c in COURSES if c[2] == a]
    sections.append(f'<section class="section{" section-pale" if a == "yamato" else ""}"><div class="sec-eyebrow">— {("Tosu &amp; Miyaki" if a == "tosu" else "Mitsuse &amp; Saga-Yamato")}</div>'
                    f'<h2 class="sec-title">{title}の{len(cs)}コース。</h2><p class="sec-desc">{sub}</p>'
                    f'<div class="sn-grid">{"".join(card(k, n, j, c, acc, note) for k, n, ar, j, c, acc, note in cs)}</div></section>')
nine_cards = "".join(card(k, n, j, c, "長崎自動車道 東脊振ICから10km以内", note) for k, n, j, c, note in NINE)

all18 = [floor(j, c)[0] for k, n, a, j, c, acc, note in COURSES]
low_wk = min(f["weekday"][0] for f in all18 if f["weekday"])
desc = (f"福岡から近い佐賀県のゴルフ場を、鳥栖・みやき・神埼エリアと三瀬・佐賀大和エリアに分けて紹介。18ホール6コース＋9ホール2コース。"
        f"じゃらん・楽天GORAの直近14日の最安（{CHECKED_JA}確認・税込総額）つき。")
title = "福岡から近い佐賀のゴルフ場｜鳥栖・みやき・神埼と三瀬・佐賀大和の8コース【料金・予約】"

tpl = open(os.path.join(R0, "book-fukuoka-tomorrow.html"), encoding="utf-8").read()
shared_head = tpl[tpl.index("  <!-- Google Analytics -->"):tpl.index("</style>", tpl.index("  <style>")) + len("</style>")]
body_start = tpl.index("<body>") + len("<body>")
disclosure = tpl[body_start:tpl.index('<a href="/" class="back-link">')]
footer = tpl[tpl.index("<footer>"):]
CSS = """
  <style>
    .sn-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr)); gap:14px; }
    .sn-card { background:#fff; border:1px solid var(--line); border-radius:16px; padding:18px 20px; }
    .sn-name { font-family:var(--serif); font-weight:700; font-size:17px; color:var(--forest-dark); margin-bottom:6px; }
    .sn-meta { font-size:12.5px; color:var(--muted); line-height:1.7; }
    .sn-note { font-size:13px; color:var(--charcoal); margin-top:6px; line-height:1.7; }
    .sn-price { font-size:14px; margin:10px 0; }
    .sn-price strong { font-family:var(--num); color:var(--orange-dark); font-size:16px; }
    .sn-na { color:var(--muted); font-size:12.5px; }
    .sn-few { display:inline-block; font-size:11px; background:#fff3d6; color:#8a5a00; border-radius:6px; padding:2px 6px; margin-left:4px; }
    .sn-btns { display:flex; gap:8px; flex-wrap:wrap; }
    .sn-btn { flex:1; min-width:130px; text-align:center; color:#fff; font-weight:700; font-size:13px; padding:10px 12px; border-radius:10px; }
    .sn-rak { background:linear-gradient(135deg,#c81d1d,#8f0000); }
    .sn-jal { background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }
    .sn-list { font-size:14px; line-height:1.9; max-width:820px; padding-left:20px; }
  </style>"""

html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://www.google-analytics.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,500;1,400&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <meta charset="UTF-8">
<meta name="referrer" content="no-referrer-when-downgrade">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <title>{title}</title>
  <link rel="canonical" href="https://fukuoka-golf-guide.com/{OUT}" />
  <link rel="alternate" hreflang="ja" href="https://fukuoka-golf-guide.com/{OUT}">
  <link rel="alternate" hreflang="x-default" href="https://fukuoka-golf-guide.com/{OUT}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:url" content="https://fukuoka-golf-guide.com/{OUT}">
  <meta property="og:site_name" content="福岡ゴルフ場ガイド">
  <meta property="og:title" content="福岡から近い佐賀のゴルフ場（鳥栖・みやき・神埼／三瀬・佐賀大和）">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/images/chisan-onga-play-1.webp">
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"福岡ゴルフ場ガイド","item":"https://fukuoka-golf-guide.com/"}},
    {{"@type":"ListItem","position":2,"name":"福岡から近い佐賀のゴルフ場","item":"https://fukuoka-golf-guide.com/{OUT}"}}]}}
  </script>

{shared_head}
{CSS}
</head>
<body>{disclosure}<a href="/" class="back-link">← Top</a>

<section class="hero">
  <img class="hero-photo" src="images/chisan-onga-play-1.webp" alt="イメージ写真（福岡県のチサンカントリークラブ遠賀・編集部撮影）" fetchpriority="high">
  <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Saga Courses near Fukuoka</div>
    <h1 class="hero-title">福岡から近い、<br>佐賀のゴルフ場。</h1>
    <p class="hero-sub">県境をこえてすぐの、鳥栖・みやき・神埼エリアと、三瀬・佐賀大和エリア。18ホール6コースと9ホール2コースを、じゃらん・楽天GORAの直近の最安つきでまとめました。</p>
    <div class="hero-badges">
      <span class="hero-badge">⛳ 18H 6コース＋9H 2コース</span>
      <span class="hero-badge">💴 18H平日 {yen(low_wk)}〜</span>
      <span class="hero-badge">📅 {CHECKED_JA}確認</span>
    </div>
  </div>
</section>

{"".join(sections[:1])}

<section class="section section-warm">
  <div class="sec-eyebrow">— 9-Hole Courses</div>
  <h2 class="sec-title">鳥栖・みやきの9ホールのコース。</h2>
  <p class="sec-desc">練習がてら回りたいときや、短い時間で回りたいときに。</p>
  <div class="sn-grid">{nine_cards}</div>
</section>

{"".join(sections[1:])}

<section class="section">
  <div class="sec-eyebrow">— Notes</div>
  <h2 class="sec-title">料金と情報について。</h2>
  <ul class="sn-list">
    <li>料金は{CHECKED_JA}に、じゃらん・楽天GORAの予約カレンダーで確認した直近14日（{PERIOD}）の18ホール最安（税込総額）です。両サイトのうち安い方を載せています。プランの条件（人数・昼食・時間帯）は予約画面で確認してください。</li>
    <li>9ホールのコースは、9ホールを2周するプランなども含めた最安です。</li>
    <li>住所・ホール数・距離・パーは楽天GORAのコース情報、アクセスは楽天GORA（北山CCはじゃらん）の掲載によります。</li>
    <li>ここに無い佐賀県のコース（唐津・多久・武雄など）は、福岡からは少し離れるため載せていません。</li>
  </ul>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Related Pages</div>
  <h2 class="sec-title">関連ページ。</h2>
  <div class="related-grid">
    <a href="saga-meimon.html" class="related-card"><span class="related-name">🏛️ 佐賀の名門ゴルフ場はどこ？</span><span class="related-arrow">→</span></a>
    <a href="area-chikugo.html" class="related-card"><span class="related-name">⛳ 筑後・久留米エリア（福岡県）</span><span class="related-arrow">→</span></a>
    <a href="area-fukuokacity.html" class="related-card"><span class="related-name">🏙️ 福岡市エリア</span><span class="related-arrow">→</span></a>
    <a href="/" class="related-card"><span class="related-name">🏠 福岡の全50コースを比べる</span><span class="related-arrow">→</span></a>
  </div>
</section>

{footer}"""

assert html.count("G-PENH0Z4VT7") == tpl.count("G-PENH0Z4VT7")
for root in ROOTS:
    p = os.path.join(root, OUT)
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    print(root, "new" if old is None else ("same" if old == html else "update"))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="\n").write(html)
for k, n, a, j, c, acc, note in COURSES:
    print(n, floor(j, c))
for k, n, j, c, note in NINE:
    print(n, floor(j, c))
print("checked", CHECKED, "period", PERIOD, "APPLIED" if APPLY else "DRY-RUN")
