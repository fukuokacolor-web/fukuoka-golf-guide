#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
「佐賀の名門ゴルフ場はどこ？」ページ saga-meimon.html を作る (日本語のみ)。
  専門家会議 (2026-11-28) の結論: 「名門」と言い切らず、公式・2出典で確認できた「開場年・設計者・公式競技」を並べる。
  事実は SAGA_MEIMON_FACTS.md (2026-11-28 確認) に載せたものだけ。載せないもの (佐賀最古・九州初・サロンパス 等) は使わない。
  料金: scripts/.cache/jalan_floor.json・gora_floor.json (直近14日の18H最安・税込総額・両サイトの安い方)。
  コース情報: scripts/.cache/saga_rakuten_guide_2026-11-25.json (楽天GORAのコースガイド: 住所・距離・パー・IC)。
Usage: python scripts/build_saga_meimon_page_2026.py [--apply]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
R0 = ROOTS[0]
OUT = "saga-meimon.html"
C = os.path.join(R0, "scripts", ".cache")
JF = json.load(open(os.path.join(C, "jalan_floor.json"), encoding="utf-8"))
GF = json.load(open(os.path.join(C, "gora_floor.json"), encoding="utf-8"))
SLUG = {v["name"]: k for k, v in json.load(open(os.path.join(R0, "saga_courses.json"), encoding="utf-8"))["courses"].items()}
RG = json.load(open(os.path.join(C, "saga_rakuten_guide_2026-11-25.json"), encoding="utf-8"))

# 開場の古い順。facts は (項目, 内容, 出典の表示, 出典URL)
COURSES = [
    dict(name="唐津ゴルフ倶楽部", city="唐津市", jid="02365", cid="410001", open="1937年（昭和12年）", design="—", event="—",
         access="西九州自動車道 唐津千々賀山田ICから10km以内",
         facts=[("開場", "1937年（昭和12年）", "公式サイト", "https://www.resol-golf.jp/karatsu/course/")],
         note="今回確認した5コースのなかで、いちばん開場が古いコースです。"),
    dict(name="ブリヂストンカンツリー倶楽部", city="鳥栖市", jid="02366", cid="410013", open="1957年（昭和32年）", design="三好徳行", event="—",
         access="九州自動車道 鳥栖ICから10km以内",
         facts=[("開場", "1957年（昭和32年）", "公式サイト", "https://bridgestone-cc.com/about/"),
                ("創設", "ブリヂストン創業者・石橋正二郎", "公式サイト", "https://bridgestone-cc.com/about/"),
                ("設計", "三好徳行", "公式サイト", "https://bridgestone-cc.com/about/")],
         note="公式サイトによると、ブリヂストンの創業者・石橋正二郎が創設したコースです。"),
    dict(name="佐賀カントリー倶楽部", city="みやき町", jid="02376", cid="410002", open="（起工 1969年）", design="井上誠一", event="—",
         access="長崎自動車道 鳥栖ICから10km以内",
         facts=[("設計", "井上誠一", "公式サイト（当倶楽部の歴史）", "https://www.saga-cc.com/history"),
                ("起工", "1969年（昭和44年）", "公式サイト（当倶楽部の歴史）", "https://www.saga-cc.com/history")],
         note="開場年は資料によって1970年・1971年と分かれるため、ここでは公式に書かれている起工の年を載せています。"),
    dict(name="若木ゴルフ倶楽部", city="武雄市", jid="02370", cid="410016", open="1991年", design="デズモンド・ミュアヘッド", event="—",
         access="長崎自動車道 武雄北方ICから10km以内",
         facts=[("設計", "デズモンド・ミュアヘッド", "PGM公式サイト", "https://booking.pacificgolf.co.jp/guide/125.html"),
                ("開場", "1991年", "ShotNavi・楽天GORA", "https://www.shotnavi.jp/gcguide/gcinfo_693.htm")],
         note="運営するPGMの公式サイトは「ミュアヘッドが唯一西日本に生んだ作品」と紹介しています。"),
    dict(name="佐賀クラシックゴルフ倶楽部", city="多久市", jid="02369", cid="410003", open="1996年", design="中村亨治",
         event="日本シニアゴルフ選手権（2023年）ほか",
         access="長崎自動車道 多久ICから10km以内",
         facts=[("開場", "1996年", "公式サイト", "https://cm-g.co.jp/saga/history/"),
                ("設計", "中村亨治", "公式サイト", "https://cm-g.co.jp/saga/history/"),
                ("認定", "JLPGA認定コース", "日本女子プロゴルフ協会", "https://www.lpga.or.jp/about/authorized_course/"),
                ("公式競技", "2023年 日本シニアゴルフ選手権", "日本ゴルフ協会 競技規定", "https://www.jga.or.jp/jga/jsp/2023/12-0/regulation.pdf"),
                ("公式競技", "2007年 九州アマチュアゴルフ選手権 決勝・2012年 九州オープン", "公式サイト・GDO", "https://cm-g.co.jp/saga/history/tournament/")],
         note="5コースのなかで、全国規模の公式競技（日本ゴルフ協会主催）の会場になったことを確認できたのはここだけです。"),
]
CHECKED = "2026年11月28日"
P = JF[COURSES[0]["jid"]]["period"].split("/")
PERIOD = "〜".join(f"{int(x[5:7])}/{int(x[8:10])}" for x in P)


def jalan_url(jid):
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


def floor(jid, cid):
    res = {}
    for k in ("weekday", "weekend"):
        c = []
        if JF.get(jid, {}).get(k):
            c.append(JF[jid][k]["total"])
        if GF.get(cid, {}).get(k):
            c.append(GF[cid][k]["total"])
        res[k] = min(c) if c else None
    return res


def yen(v):
    return f"¥{v:,}〜" if v else "直近の空きなし"


rows, cards = [], []
for x in COURSES:
    g = RG[x["cid"]]
    f = floor(x["jid"], x["cid"])
    x["f"] = f
    rows.append(f'<tr><td class="sm-n"><a href="course-saga-{SLUG[x["name"]]}.html" style="color:inherit;border-bottom:1px dotted;">{x["name"]}</a><span>{x["city"]}</span></td><td>{x["open"]}</td><td>{x["design"]}</td><td>{x["event"]}</td><td class="sm-p">{yen(f["weekday"])}</td></tr>')
    facts = "".join(f'<li><strong>{k}</strong>：{v}（<a href="{u}" target="_blank" rel="noopener">{s}</a>）</li>' for k, v, s, u in x["facts"])
    cards.append(
        f'<div class="sm-card"><div class="sm-name">{x["name"]} <a href="course-saga-{SLUG[x["name"]]}.html" style="font-size:12.5px;font-weight:700;color:#1a5fa0;">コース詳細 →</a></div>'
        f'<div class="sm-meta">{g["addr"].replace("佐賀県 ", "佐賀県")}｜{g["holes"]}・パー{g["par"]}・{g["yard"]}｜🚗 {x["access"]}</div>'
        f'<ul class="sm-facts">{facts}</ul><p class="sm-note">{x["note"]}</p>'
        f'<div class="sm-price">平日 <strong>{yen(f["weekday"])}</strong>　土日祝 <strong>{yen(f["weekend"])}</strong></div>'
        f'<div class="sm-btns"><a href="{rakuten_url(x["cid"])}" class="sm-btn sm-rak" target="_blank" rel="nofollow sponsored noopener">楽天GORAで予約</a>'
        f'<a href="{jalan_url(x["jid"])}" class="sm-btn sm-jal" target="_blank" rel="nofollow sponsored noopener">じゃらんで予約</a></div></div>')

faq = [
    ("佐賀県で全国規模の公式競技が開かれたゴルフ場は？",
     "佐賀クラシックゴルフ倶楽部（多久市）が、2023年の日本シニアゴルフ選手権（日本ゴルフ協会主催）の会場になっています。日本ゴルフ協会の競技規定で確認できます。"),
    ("井上誠一が設計した佐賀のゴルフ場は？",
     "佐賀カントリー倶楽部（みやき町）です。クラブの公式サイトに「井上誠一の設計」と書かれています。"),
    ("佐賀でいちばん古いゴルフ場は？",
     "このページで確認した5コースのなかでは、1937年（昭和12年）開場の唐津ゴルフ倶楽部がいちばん古いコースです。佐賀県内のすべてのゴルフ場と比べた資料は見つかっていません。"),
    ("この5コースはビジターでも予約できますか？",
     f"5コースとも、じゃらん・楽天GORAでネット予約ができます（{CHECKED}確認）。プランの条件は予約画面で確認してください。"),
]
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False, indent=1)
faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q, a in faq)

title = "佐賀の名門ゴルフ場はどこ？開場年・設計者・大会で比べる5コース【予約できるコースのみ】"
desc = ("佐賀の名門ゴルフ場を、公式サイトや競技団体の記録で確認できた開場年・設計者・公式競技で比較。唐津GC（1937年開場）、"
        "ブリヂストンCC、井上誠一設計の佐賀CC、ミュアヘッド設計の若木GC、日本シニアゴルフ選手権の佐賀クラシックGC。5コースともネット予約可。")

tpl = open(os.path.join(R0, "book-fukuoka-tomorrow.html"), encoding="utf-8").read()
shared_head = tpl[tpl.index("  <!-- Google Analytics -->"):tpl.index("</style>", tpl.index("  <style>")) + len("</style>")]
body_start = tpl.index("<body>") + len("<body>")
disclosure = tpl[body_start:tpl.index('<a href="/" class="back-link">')]
footer = tpl[tpl.index("<footer>"):]
CSS = """
  <style>
    .sm-wrap { overflow-x:auto; border:1px solid var(--line); border-radius:14px; background:#fff; }
    .sm-table { border-collapse:collapse; width:100%; min-width:640px; font-size:13.5px; }
    .sm-table th { background:var(--forest-dark); color:#fff; padding:10px 8px; font-size:12px; text-align:left; white-space:nowrap; }
    .sm-table td { border-top:1px solid var(--line); padding:10px 8px; vertical-align:top; }
    .sm-n { font-weight:700; color:var(--forest-dark); }
    .sm-n span { display:block; font-weight:400; font-size:11.5px; color:var(--muted); }
    .sm-p { font-family:var(--num); font-weight:700; color:var(--orange-dark); white-space:nowrap; }
    .sm-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(320px,100%),1fr)); gap:14px; }
    .sm-card { background:#fff; border:1px solid var(--line); border-radius:16px; padding:18px 20px; }
    .sm-name { font-family:var(--serif); font-weight:700; font-size:18px; color:var(--forest-dark); margin-bottom:6px; }
    .sm-meta { font-size:12.5px; color:var(--muted); line-height:1.7; }
    .sm-facts { margin:10px 0 6px 18px; font-size:13.5px; line-height:1.8; }
    .sm-facts a { color:var(--ocean-dark); border-bottom:1px dotted var(--ocean); }
    .sm-note { font-size:13px; color:var(--charcoal); line-height:1.7; margin-bottom:8px; }
    .sm-price { font-size:14px; margin:8px 0 10px; }
    .sm-price strong { font-family:var(--num); color:var(--orange-dark); }
    .sm-btns { display:flex; gap:8px; flex-wrap:wrap; }
    .sm-btn { flex:1; min-width:130px; text-align:center; color:#fff; font-weight:700; font-size:13px; padding:10px 12px; border-radius:10px; }
    .sm-rak { background:linear-gradient(135deg,#c81d1d,#8f0000); }
    .sm-jal { background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }
    .sm-list { font-size:14px; line-height:1.9; max-width:820px; padding-left:20px; }
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
  <meta property="og:title" content="佐賀の名門ゴルフ場はどこ？開場年・設計者・大会で比べる5コース">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/images/kaho-play-1.webp">
  <script type="application/ld+json">
{faq_ld}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"福岡ゴルフ場ガイド","item":"https://fukuoka-golf-guide.com/"}},
    {{"@type":"ListItem","position":2,"name":"福岡から近い佐賀のゴルフ場","item":"https://fukuoka-golf-guide.com/saga-near-fukuoka.html"}},
    {{"@type":"ListItem","position":3,"name":"佐賀の名門ゴルフ場","item":"https://fukuoka-golf-guide.com/{OUT}"}}]}}
  </script>

{shared_head}
{CSS}
</head>
<body>{disclosure}<a href="/" class="back-link">← Top</a>

<section class="hero">
  <img class="hero-photo" src="images/kaho-play-1.webp" alt="イメージ写真（福岡県のかほゴルフクラブ・編集部撮影）" fetchpriority="high">
  <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Historic Courses in Saga</div>
    <h1 class="hero-title">佐賀の名門ゴルフ場はどこ？<br>開場年・設計者・大会で比べる。</h1>
    <p class="hero-sub">「名門」に決まった基準はありません。このページでは、公式サイトや競技団体の記録で確かめられた事実（開場年・設計者・公式競技）を並べました。5コースとも、じゃらん・楽天GORAでネット予約できます。</p>
    <div class="hero-badges">
      <span class="hero-badge">🏛️ 1937年開場〜</span>
      <span class="hero-badge">✏️ 井上誠一・ミュアヘッド設計</span>
      <span class="hero-badge">🏆 日本シニアゴルフ選手権の会場</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Compare</div>
  <h2 class="sec-title">5コースを一覧で比べる。</h2>
  <p class="sec-desc">開場の古い順。料金は{CHECKED}に確認した直近14日（{PERIOD}）の平日18ホール最安（税込総額・じゃらん／楽天GORAの安い方）です。</p>
  <div class="sm-wrap"><table class="sm-table"><thead><tr><th>コース</th><th>開場</th><th>設計</th><th>公式競技</th><th>平日</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Courses</div>
  <h2 class="sec-title">1コースずつ、根拠と一緒に。</h2>
  <p class="sec-desc">（ ）は確認した出典です。リンクから元の情報を見られます。</p>
  <div class="sm-grid">{"".join(cards)}</div>
</section>

<section class="section">
  <div class="sec-eyebrow">— FAQ</div>
  <h2 class="sec-title">よくある質問。</h2>
  <div class="faq-list">{faq_html}</div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Notes</div>
  <h2 class="sec-title">このページについて。</h2>
  <ul class="sm-list">
    <li>載せているのは、公式サイトか、2つ以上の出典で確かめられた事実だけです（{CHECKED}確認）。資料によって食い違う内容や、根拠が1つしか見つからない内容は載せていません。</li>
    <li>天山カントリークラブ・武雄嬉野カントリークラブ・佐賀ロイヤルゴルフクラブなども歴史のあるコースですが、開場年や設計者を公式で確認できなかったため、今回は入れていません。</li>
    <li>住所・距離・パー・アクセスは楽天GORAのコース情報によります。</li>
  </ul>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Related Pages</div>
  <h2 class="sec-title">関連ページ。</h2>
  <div class="related-grid">
    <a href="saga-near-fukuoka.html" class="related-card"><span class="related-name">⛳ 福岡から近い佐賀のゴルフ場</span><span class="related-arrow">→</span></a>
    <a href="hub-business.html" class="related-card"><span class="related-name">🏛️ 福岡の名門・接待ゴルフ場</span><span class="related-arrow">→</span></a>
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
for x in COURSES:
    print(x["name"], x["f"])
print("period", PERIOD, "APPLIED" if APPLY else "DRY-RUN")
