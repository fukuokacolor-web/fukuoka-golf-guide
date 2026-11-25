#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
年末年始ページ book-fukuoka-yearend.html を作る (日本語のみ)。
  データ: scripts/.cache/yearend_2026.json (yearend_scan_2026.py の結果・じゃらん/楽天GORAの空きと18H最安の税込総額)
  載せるのは「12/29〜1/3 のどこかで、じゃらんか楽天GORAに空きがあったコース」だけ。数字はすべてデータから計算する。
  ヘッダ (GA4 計測コード・広告表記・CSS) は book-fukuoka-tomorrow.html から流用。
Usage: python scripts/build_yearend_page_2026.py [--apply]
"""
import datetime, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
R0 = ROOTS[0]
OUT = "book-fukuoka-yearend.html"
CHECKED = "2026年11月25日"
DATA = json.load(open(os.path.join(R0, "scripts", ".cache", "yearend_2026.json"), encoding="utf-8"))
DATES = [datetime.date(2026, 12, 29) + datetime.timedelta(days=k) for k in range(6)]
WD = "月火水木金土日"
LABEL = {d: f"{d.month}/{d.day}({WD[d.weekday()]})" for d in DATES}
SHORT = {d: f"{d.month}/{d.day}" for d in DATES}

jal = {c["file"].replace("course-", ""): c["jalan_id"] for c in json.load(open(os.path.join(R0, "jalan_golf_mapping.json"), encoding="utf-8"))["courses"]}
rak = {c["file"].replace("course-", ""): c["c_id"] for c in json.load(open(os.path.join(R0, "rakuten_gora_mapping.json"), encoding="utf-8"))["courses"]}
cd = json.load(open(os.path.join(R0, "course_data.json"), encoding="utf-8"))  # 読むだけ
cd = cd if isinstance(cd, list) else cd.get("courses", cd)
cd = {c["slug"]: c for c in (cd if isinstance(cd, list) else cd.values())}
AREA_ORDER = ["fukuokacity", "itoshima", "kitakyushu", "chikugo", "chikuho"]
AREA_NAME = {"fukuokacity": "福岡市", "itoshima": "糸島", "kitakyushu": "北九州・宗像", "chikugo": "筑後・久留米", "chikuho": "筑豊"}
area_of = {}
for a in AREA_ORDER:
    for s in re.findall(r'href="course-([a-z-]+)\.html"', open(os.path.join(R0, f"area-{a}.html"), encoding="utf-8").read()):
        area_of.setdefault(s, a)
area_of["central"] = "chikugo"  # 筑紫野市 (course_data の area_ja)
area_of["century"] = "chikugo"  # 朝倉市 (エリアページ未掲載)
NAME_FIX = {"akane": "茜ゴルフクラブ"}  # コースページ・じゃらん・楽天の表記 (course_data は旧表記)


RAKNAME = {c["file"].replace("course-", ""): c.get("name") for c in json.load(open(os.path.join(R0, "rakuten_gora_mapping.json"), encoding="utf-8"))["courses"]}


def name(slug):
    if slug in NAME_FIX:
        return NAME_FIX[slug]
    n = cd[slug]["name_ja"] if slug in cd else re.sub(r"【[^】]*】", "", RAKNAME.get(slug) or slug)
    return re.sub(r"^\W+\s*", "", n).strip()


def jalan_url(jid, d=None):
    path = f"https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"
    if d:
        path += f"%3FplayMonth%3D{d.month - 1}%26playDate%3D{d.day}"
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect={path}"


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


# --- 集計 ---
SKIP = {"aburayama"}  # 10H ショートコース (18H の表に入れない)
rows = []
for slug, r in DATA.items():
    if slug in SKIP:
        continue
    days = {}
    for d in DATES:
        ds = d.isoformat()
        cands = []
        if ds in r["jalan"]:
            cands.append(("じゃらん", r["jalan"][ds]["total"]))
        if ds in r["rakuten"]:
            cands.append(("楽天", r["rakuten"][ds]["total"]))
        if cands:
            days[d] = dict(sites=[c[0] for c in cands], low=min(c[1] for c in cands if c[1]))
    if not days:
        continue
    low_d = min(days, key=lambda d: days[d]["low"])
    rows.append(dict(slug=slug, name=name(slug), area=area_of.get(slug, ""), days=days, n=len(days),
                     low=days[low_d]["low"], low_d=low_d,
                     jalan=bool(r["jalan"]) and jal.get(slug), rakuten=bool(r["rakuten"]) and rak.get(slug)))
rows.sort(key=lambda x: (-x["n"], x["low"]))
assert rows, "no data"
N = len(rows)
n_ganjitsu = sum(1 for x in rows if DATES[3] in x["days"])
n_all6 = sum(1 for x in rows if x["n"] == 6)
low_all = min(x["low"] for x in rows)
low_row = min(rows, key=lambda x: x["low"])
per_day = {d: sum(1 for x in rows if d in x["days"]) for d in DATES}
day_low = {d: min((x["days"][d]["low"] for x in rows if d in x["days"]), default=None) for d in DATES}


def yen(v):
    return f"¥{v:,}"


def btns(x, small=False):
    b = []
    if x["rakuten"]:
        b.append(f'<a href="{rakuten_url(x["rakuten"])}" class="ye-btn ye-rak" target="_blank" rel="nofollow sponsored noopener">楽天GORA</a>')
    if x["jalan"]:
        b.append(f'<a href="{jalan_url(x["jalan"])}" class="ye-btn ye-jal" target="_blank" rel="nofollow sponsored noopener">じゃらん</a>')
    return "".join(b)


# --- 表 ---
thead = "<tr><th>コース</th>" + "".join(f"<th>{LABEL[d]}</th>" for d in DATES) + "<th>予約</th></tr>"
tbody = []
for x in rows:
    cells = []
    for d in DATES:
        if d in x["days"]:
            v = x["days"][d]
            cells.append(f'<td class="ye-ok"><span class="ye-mark">○</span><span class="ye-p">{yen(v["low"])}〜</span><span class="ye-s">{"・".join(v["sites"])}</span></td>')
        else:
            cells.append('<td class="ye-no">－</td>')
    tbody.append(f'<tr><td class="ye-name"><a href="course-{x["slug"]}.html">{x["name"]}</a><span class="ye-area">{AREA_NAME.get(x["area"], "")}</span></td>'
                 + "".join(cells) + f'<td class="ye-act">{btns(x)}</td></tr>')

# --- 元日 ---
g = sorted([x for x in rows if DATES[3] in x["days"]], key=lambda x: x["days"][DATES[3]]["low"])
gcards = "".join(
    f'<div class="ye-card"><div class="ye-card-name"><a href="course-{x["slug"]}.html">{x["name"]}</a></div>'
    f'<div class="ye-card-meta">{AREA_NAME.get(x["area"], "")}・1/1 の18H最安 <strong>{yen(x["days"][DATES[3]]["low"])}〜</strong>（{"・".join(x["days"][DATES[3]]["sites"])}）</div>'
    f'<div class="ye-card-btns">{btns(x)}</div></div>' for x in g)

# --- エリア別 ---
area_html = []
for a in AREA_ORDER:
    xs = [x for x in rows if x["area"] == a]
    if not xs:
        continue
    lis = "".join(f'<li><a href="course-{x["slug"]}.html">{x["name"]}</a>（{x["n"]}日・最安 {yen(x["low"])}〜）</li>' for x in xs)
    area_html.append(f'<div class="ye-area-box"><div class="ye-area-title">{AREA_NAME[a]}　{len(xs)}コース</div><ul>{lis}</ul></div>')

day_line = "・".join(f"{SHORT[d]} {per_day[d]}コース" for d in DATES)
desc = (f"2026年12月29日〜2027年1月3日に、じゃらん・楽天GORAでネット予約できる福岡のゴルフ場{N}コースを日付ごとに一覧。"
        f"元日(1/1)は{n_ganjitsu}コース。18ホールの最安は{yen(low_all)}〜（{CHECKED}確認・税込総額）。")
title = f"福岡のゴルフ場 年末年始に予約できる{N}コース｜12/29〜1/3の空きと料金【2026-2027】"

faq = [
    ("元日（1月1日）に福岡で回れるゴルフ場はありますか？",
     f"{CHECKED}の時点で、1月1日にじゃらん・楽天GORAで予約できたのは{n_ganjitsu}コースです。"
     + (f"いちばん安かったのは{g[0]['name']}の{yen(g[0]['days'][DATES[3]]['low'])}〜（18ホール・税込総額）でした。" if g else "")),
    ("年末年始の料金はいくらくらいですか？",
     f"12/29〜1/3の18ホールの最安（税込総額）は、日ごとに "
     + "、".join(f"{SHORT[d]} {yen(day_low[d])}〜" for d in DATES if day_low[d]) + f" でした（{CHECKED}確認）。プランの条件（人数・昼食・時間帯）は予約画面で確認してください。"),
    ("この表に無いコースは、年末年始は休みですか？",
     "そうとは限りません。この表は、じゃらん・楽天GORAでネット予約できたコースだけです。会員制のコースや、公式サイト・電話でしか予約を受けないコースは載っていません。営業日は各コースの公式サイトで確認してください。"),
    ("空きはいつの情報ですか？",
     f"{CHECKED}に、じゃらんと楽天GORAの予約カレンダーで確認しました。年末年始が近づくと埋まったり、新しいプランが出たりするので、最新の空きは予約サイトで確認してください。"),
]
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False, indent=1)
faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q, a in faq)

# --- ヘッダ流用 ---
tpl = open(os.path.join(R0, "book-fukuoka-tomorrow.html"), encoding="utf-8").read()
ga_start = tpl.index("  <!-- Google Analytics -->")
style_end = tpl.index("</style>", tpl.index("  <style>")) + len("</style>")
shared_head = tpl[ga_start:style_end]
body_start = tpl.index("<body>") + len("<body>")
disclosure = tpl[body_start:tpl.index('<a href="/" class="back-link">')]
footer = tpl[tpl.index("<footer>"):]

EXTRA_CSS = """
  <style>
    .ye-wrap { overflow-x:auto; -webkit-overflow-scrolling:touch; border:1px solid var(--line); border-radius:14px; background:#fff; }
    .ye-table { border-collapse:collapse; min-width:860px; width:100%; font-size:13px; }
    .ye-table th { background:var(--forest-dark); color:#fff; padding:10px 8px; font-size:12px; white-space:nowrap; }
    .ye-table td { border-top:1px solid var(--line); padding:8px 6px; text-align:center; vertical-align:middle; }
    .ye-table td.ye-name { text-align:left; min-width:170px; position:sticky; left:0; background:#fff; z-index:1; }
    .ye-name a { font-weight:700; color:var(--forest-dark); border-bottom:1px dotted var(--forest); }
    .ye-area { display:block; font-size:11px; color:var(--muted); }
    .ye-ok { background:#f1f8f3; }
    .ye-mark { display:block; color:#1a7f3c; font-weight:700; }
    .ye-p { display:block; font-family:var(--num); font-weight:700; color:var(--orange-dark); white-space:nowrap; }
    .ye-s { display:block; font-size:10.5px; color:var(--muted); white-space:nowrap; }
    .ye-no { color:#bbb; }
    .ye-act { white-space:nowrap; }
    .ye-btn { display:inline-block; color:#fff; font-weight:700; font-size:12px; padding:7px 10px; border-radius:8px; margin:2px; }
    .ye-rak { background:linear-gradient(135deg,#c81d1d,#8f0000); }
    .ye-jal { background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }
    .ye-cards { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:12px; }
    .ye-card { background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px 18px; }
    .ye-card-name a { font-family:var(--serif); font-weight:700; font-size:16px; color:var(--forest-dark); }
    .ye-card-meta { font-size:13px; color:var(--muted); margin:4px 0 10px; }
    .ye-card-meta strong { color:var(--orange-dark); }
    .ye-areas { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:14px; }
    .ye-area-box { background:#fff; border:1px solid var(--line); border-radius:14px; padding:16px 18px; }
    .ye-area-title { font-weight:700; color:var(--forest-dark); margin-bottom:6px; }
    .ye-area-box ul { padding-left:18px; font-size:13.5px; line-height:1.9; }
    .ye-area-box a { color:var(--ocean-dark); font-weight:700; }
    .ye-note { font-size:13.5px; line-height:1.9; color:var(--charcoal); max-width:820px; }
    .ye-note li { margin-bottom:6px; }
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
  <meta property="og:title" content="福岡のゴルフ場 年末年始に予約できる{N}コース（12/29〜1/3）">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/images/golf-mountain.webp">
  <script type="application/ld+json">
{faq_ld}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"福岡ゴルフ場ガイド","item":"https://fukuoka-golf-guide.com/"}},
    {{"@type":"ListItem","position":2,"name":"年末年始に予約できるゴルフ場","item":"https://fukuoka-golf-guide.com/{OUT}"}}]}}
  </script>

{shared_head}
{EXTRA_CSS}
</head>
<body>{disclosure}<a href="/" class="back-link">← Top</a>

<section class="hero">
  <img class="hero-photo" src="images/golf-mountain.webp" alt="イメージ写真（特定のゴルフ場の写真ではありません）" fetchpriority="high">
  <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Year-End &amp; New Year Golf</div>
    <h1 class="hero-title">年末年始に、福岡で回れるゴルフ場。<br>12/29〜1/3 の空き{N}コース。</h1>
    <p class="hero-sub">2026年12月29日〜2027年1月3日に、じゃらん・楽天GORAでネット予約できるコースを日付ごとにまとめました。空きと料金は{CHECKED}に両サイトの予約カレンダーで確認した18ホールの最安（税込総額）です。</p>
    <div class="hero-badges">
      <span class="hero-badge">📅 6日間の空き一覧</span>
      <span class="hero-badge">🎍 元日 {n_ganjitsu}コース</span>
      <span class="hero-badge">💴 最安 {yen(low_all)}〜</span>
    </div>
  </div>
</section>

<div class="stats-band">
  <div class="stats-band-inner">
    <div class="stats-band-item"><div class="stats-band-num">{N}<span class="unit">コース</span></div><div class="stats-band-label">ネット予約できる</div></div>
    <div class="stats-band-item"><div class="stats-band-num">{n_all6}<span class="unit">コース</span></div><div class="stats-band-label">6日すべて空きあり</div></div>
    <div class="stats-band-item"><div class="stats-band-num">{n_ganjitsu}<span class="unit">コース</span></div><div class="stats-band-label">元日に空きあり</div></div>
    <div class="stats-band-item"><div class="stats-band-num">11/25</div><div class="stats-band-label">空きを確認した日</div></div>
  </div>
</div>

<section class="section">
  <div class="sec-eyebrow">— Availability</div>
  <h2 class="sec-title">日付ごとの空き（18ホール）。</h2>
  <p class="sec-desc">○ はじゃらんか楽天GORAに空きがあった日で、金額はその日の18ホール最安（税込総額）です。空きの多い順に並べています。日ごとの空き：{day_line}。表は横にスクロールできます。</p>
  <div class="ye-wrap"><table class="ye-table"><thead>{thead}</thead><tbody>{"".join(tbody)}</tbody></table></div>
  <p class="sec-desc" style="margin-top:14px;margin-bottom:0;font-size:13px;">ハーフ・薄暮・コンペ・年齢や会員の限定プランは除いています。最安だったのは {low_row["name"]}（{LABEL[low_row["low_d"]]}・{yen(low_row["low"])}〜）。</p>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— New Year's Day</div>
  <h2 class="sec-title">元日（1/1）に予約できる{n_ganjitsu}コース。</h2>
  <p class="sec-desc">1月1日に空きがあったコースを、安い順に並べました。</p>
  <div class="ye-cards">{gcards}</div>
</section>

<section class="section">
  <div class="sec-eyebrow">— By Area</div>
  <h2 class="sec-title">エリア別に見る。</h2>
  <p class="sec-desc">（ ）は 12/29〜1/3 のうち空きがあった日数と、その間の18ホール最安です。</p>
  <div class="ye-areas">{"".join(area_html)}</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Before You Book</div>
  <h2 class="sec-title">予約の前に。</h2>
  <ul class="ye-note">
    <li>空きは{CHECKED}時点です。年末年始が近づくと埋まったり、新しいプランが出たりします。</li>
    <li>この一覧に無いコースが休みとは限りません。会員制のコースや、公式サイト・電話でしか予約を受けないコースは載せていません。</li>
    <li>金額はプランの条件（人数・昼食・スタート時間）によって変わります。予約画面のプラン内容とキャンセル規定を確認してください。</li>
    <li>雪や凍結が心配な日は、前日にコースへ営業状況を確認してください。</li>
  </ul>
</section>

<section class="section">
  <div class="sec-eyebrow">— FAQ</div>
  <h2 class="sec-title">よくある質問。</h2>
  <div class="faq-list">{faq_html}</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Related Pages</div>
  <h2 class="sec-title">関連ページ。</h2>
  <div class="related-grid">
    <a href="book-fukuoka-tomorrow.html" class="related-card"><span class="related-name">⏰ 今日・明日に予約できるコース</span><span class="related-arrow">→</span></a>
    <a href="book-fukuoka-cheap.html" class="related-card"><span class="related-name">💴 安く回れるコース</span><span class="related-arrow">→</span></a>
    <a href="/" class="related-card"><span class="related-name">🏠 全50コースを比べる</span><span class="related-arrow">→</span></a>
  </div>
</section>

{footer}"""

for root in ROOTS:
    p = os.path.join(root, OUT)
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    print(root, "new" if old is None else ("same" if old == html else "update"))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="\n").write(html)
assert html.count("G-PENH0Z4VT7") == tpl.count("G-PENH0Z4VT7")
print(f"N={N} all6={n_all6} ganjitsu={n_ganjitsu} low={low_all} ({low_row['name']} {low_row['low_d']})")
print("per_day", {SHORT[d]: per_day[d] for d in DATES}, "day_low", {SHORT[d]: day_low[d] for d in DATES})
print("APPLIED" if APPLY else "DRY-RUN")
