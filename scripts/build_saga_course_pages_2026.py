#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佐賀の個別コースページ course-saga-{slug}.html を作る (日本語のみ・11コース)。
  データ: saga_courses.json (build_saga_course_data_2026.py)・料金は scripts/.cache/jalan_floor.json / gora_floor.json (直近14日の18H最安・税込総額)
  載せる事実は、じゃらん・楽天GORA・公式・競技団体の掲載だけ。各項目に出典を書く。電話番号は載せない。
  ヘッダ (GA4 計測コード・広告表記・CSS) は book-fukuoka-tomorrow.html から流用。
Usage: python scripts/build_saga_course_pages_2026.py [--apply] [--only slug]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
R0 = ROOTS[0]
DATA = json.load(open(os.path.join(R0, "saga_courses.json"), encoding="utf-8"))["courses"]
JF = json.load(open(os.path.join(R0, "scripts", ".cache", "jalan_floor.json"), encoding="utf-8"))
GF = json.load(open(os.path.join(R0, "scripts", ".cache", "gora_floor.json"), encoding="utf-8"))
AREA = {"tosu": ("鳥栖・みやき・神埼", "saga-near-fukuoka.html", ("area-chikugo.html", "筑後・久留米エリア（福岡県）")),
        "yamato": ("三瀬・佐賀大和", "saga-near-fukuoka.html", ("area-fukuokacity.html", "福岡市エリア")),
        "karatsu": ("唐津", "saga-meimon.html", ("area-itoshima.html", "糸島エリア（福岡県）")),
        "takeo": ("武雄", "saga-meimon.html", None),
        "taku": ("多久", "saga-meimon.html", None)}
PHOTOS = [("kaho-play-1.webp", "福岡県のかほゴルフクラブ"), ("chisan-onga-play-1.webp", "福岡県のチサンカントリークラブ遠賀"),
          ("kaho-play-2.webp", "福岡県のかほゴルフクラブ"), ("chisan-onga-play-2.webp", "福岡県のチサンカントリークラブ遠賀"),
          ("kaho-play-3.webp", "福岡県のかほゴルフクラブ"), ("chisan-onga-play-3.webp", "福岡県のチサンカントリークラブ遠賀")]
WD = "月火水木金土日"


def jalan_url(jid):
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


def floor(c):
    res = {}
    for k in ("weekday", "weekend"):
        cand = []
        if c["jalan_id"] and JF.get(c["jalan_id"], {}).get(k):
            b = JF[c["jalan_id"]][k]
            cand.append((b["total"], "じゃらん", b["ymd"]))
        if GF.get(c["rakuten_cid"], {}).get(k):
            b = GF[c["rakuten_cid"]][k]
            cand.append((b["total"], "楽天GORA", b["ymd"]))
        res[k] = min(cand) if cand else None
    days = max(JF.get(c["jalan_id"], {}).get("days_with_plans", 0) if c["jalan_id"] else 0,
               GF.get(c["rakuten_cid"], {}).get("days_with_plans", 0))
    per = (JF.get(c["jalan_id"]) or GF.get(c["rakuten_cid"]))["period"].split("/")
    checked = (JF.get(c["jalan_id"]) or GF.get(c["rakuten_cid"]))["checked"]
    return res, days, per, checked


def practice(t):
    if not t:
        return None
    if t.strip().startswith("なし"):
        return "なし"
    y = re.search(r"距離：(\d+)ヤード", t) or re.search(r"(\d+)\s*[YＹ]", t.translate(str.maketrans("０１２３４５６７８９", "0123456789")))
    n = re.search(r"打席数：(\d+)", t) or re.search(r"(\d+)\s*打席", t.translate(str.maketrans("０１２３４５６７８９", "0123456789")))
    parts = ([f"{y.group(1)}ヤード"] if y else []) + ([f"{n.group(1)}打席"] if n else [])
    return "・".join(parts) or "あり"



def acc_fmt(a):
    road, rest = a.split("・", 1)
    name, km = rest.rsplit(" ", 1)
    suffix = "IC" if road.endswith("自動車道") else "出入口"
    return f"{road} {name}{suffix}から{km}"

def md(ymd):
    return f"{int(ymd[4:6])}/{int(ymd[6:8])}"


def yen(b):
    return f"¥{b[0]:,}〜" if b else "直近の空きなし"


tpl = open(os.path.join(R0, "book-fukuoka-tomorrow.html"), encoding="utf-8").read()
shared_head = tpl[tpl.index("  <!-- Google Analytics -->"):tpl.index("</style>", tpl.index("  <style>")) + len("</style>")]
body_start = tpl.index("<body>") + len("<body>")
disclosure = tpl[body_start:tpl.index('<a href="/" class="back-link">')]
footer = tpl[tpl.index("<footer>"):]
CSS = """
  <style>
    .sc-ftv { max-width:1100px; margin:0 auto; padding:16px 20px 0; }
    .sc-ftv-box { background:#fff; border:1px solid var(--line); border-radius:14px; padding:14px 16px; }
    .sc-ftv-price { font-size:14px; margin-bottom:10px; }
    .sc-ftv-price strong { font-family:var(--num); color:var(--orange-dark); font-size:17px; }
    .sc-btns { display:flex; gap:8px; flex-wrap:wrap; }
    .sc-btn { flex:1; min-width:140px; text-align:center; color:#fff; font-weight:700; font-size:14px; padding:12px; border-radius:10px; }
    .sc-rak { background:linear-gradient(135deg,#c81d1d,#8f0000); }
    .sc-jal { background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }
    .sc-table { width:100%; border-collapse:collapse; background:#fff; border:1px solid var(--line); border-radius:14px; overflow:hidden; font-size:14px; }
    .sc-table th { width:28%; text-align:left; background:#f6f3ec; color:var(--forest-dark); padding:10px 12px; border-top:1px solid var(--line); font-weight:700; vertical-align:top; }
    .sc-table td { padding:10px 12px; border-top:1px solid var(--line); vertical-align:top; }
    .sc-src { display:block; font-size:11px; color:var(--muted); margin-top:2px; }
    .sc-facts { font-size:14px; line-height:1.9; padding-left:20px; max-width:820px; }
    .sc-facts a, .sc-sources a { color:var(--ocean-dark); border-bottom:1px dotted var(--ocean); }
    .sc-price-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr)); gap:12px; margin-bottom:14px; }
    .sc-price-card { background:#fff; border:1px solid var(--line); border-radius:14px; padding:14px 16px; }
    .sc-price-card .lbl { font-size:12px; color:var(--muted); }
    .sc-price-card .val { font-family:var(--num); font-size:22px; font-weight:700; color:var(--orange-dark); }
    .sc-price-card .sub { font-size:12px; color:var(--muted); }
    .sc-near { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(240px,100%),1fr)); gap:10px; }
    .sc-near a { display:block; background:#fff; border:1px solid var(--line); border-radius:12px; padding:12px 14px; font-weight:700; color:var(--forest-dark); }
    .sc-near a span { display:block; font-weight:400; font-size:12px; color:var(--muted); }
    .sc-sources { font-size:13px; line-height:1.9; padding-left:20px; }
    #sc-sticky { position:fixed; left:0; right:0; bottom:0; z-index:120; display:flex; gap:6px; padding:8px 10px calc(8px + env(safe-area-inset-bottom)); background:rgba(255,255,255,0.97); box-shadow:0 -4px 14px rgba(0,0,0,0.12); }
    #sc-sticky a { flex:1; text-align:center; color:#fff; font-weight:700; font-size:13.5px; padding:11px 6px; border-radius:10px; }
    body { padding-bottom:72px; }
  </style>"""


def page(slug, c, idx):
    f, days, per, checked = floor(c)
    area_name, hub, fk = AREA[c["area"]]
    photo, photo_alt = PHOTOS[idx % len(PHOTOS)]
    nine = c["holes"] == "9"
    cy, cm, cd_ = checked.split("-")
    checked_ja = f"{int(cy)}年{int(cm)}月{int(cd_)}日"
    period = "〜".join(f"{int(x[5:7])}/{int(x[8:10])}" for x in per)
    btns = f'<a href="{rakuten_url(c["rakuten_cid"])}" class="sc-btn sc-rak" target="_blank" rel="nofollow sponsored noopener">楽天GORAで予約</a>'
    if c["jalan_id"]:
        btns += f'<a href="{jalan_url(c["jalan_id"])}" class="sc-btn sc-jal" target="_blank" rel="nofollow sponsored noopener">じゃらんで予約</a>'
    sticky = btns.replace('class="sc-btn sc-rak"', 'style="background:linear-gradient(135deg,#c81d1d,#8f0000);"').replace(
        'class="sc-btn sc-jal"', 'style="background:linear-gradient(135deg,#E8744C,#D15A34);"')
    vfacts = {v["item"]: v for v in c["verified"]}

    rows = []
    def row(k, v, src):
        if v:
            rows.append(f'<tr><th>{k}</th><td>{v}<span class="sc-src">{src}</span></td></tr>')
    row("所在地", c["addr"], "楽天GORA")
    spec = f"{c['holes']}ホール・パー{c['par']}・{c['yard']}ヤード" if c["yard"] else None
    row("コース", spec, "楽天GORA")
    row("タイプ", "・".join(x for x in [c["kind"], c["slope"]] if x), "楽天GORA")
    row("グリーン", "・".join(x for x in [c["greens"], c["green"]] if x), "楽天GORA")
    if "設計" in vfacts:
        row("設計", vfacts["設計"]["value"], vfacts["設計"]["source"])
    elif c["design"]:
        row("設計", c["design"].replace("中村享治", "中村亨治"), "楽天GORA")
    if "開場" in vfacts:
        row("開場", vfacts["開場"]["value"], vfacts["開場"]["source"])
    elif c["open"]:
        row("開場", c["open"], "じゃらん")
    if c["rating"]:
        row("コースレート", f"{c['rating']['rate']}（{c['rating']['tee']}ティー・{c['rating']['yard']}ヤード）", "楽天GORA")
    row("ラウンド", (c["round_style"] or "").replace("プレ－", "プレー"), "じゃらん")
    row("練習場", practice(c["practice"]), "じゃらん")
    row("アクセス", "／".join(acc_fmt(a) for a in c["access"]), "楽天GORA（最寄りのIC・出入口からの距離）")

    facts_html = ""
    if c["verified"]:
        facts_html = ('<section class="section section-pale"><div class="sec-eyebrow">— History</div><h2 class="sec-title">公式などで確認できた経歴。</h2>'
                      '<ul class="sc-facts">' + "".join(f'<li><strong>{v["item"]}</strong>：{v["value"]}（<a href="{v["url"]}" target="_blank" rel="noopener">{v["source"]}</a>）</li>' for v in c["verified"])
                      + '</ul></section>')

    pc = []
    for k, lbl in (("weekday", "平日"), ("weekend", "土日祝")):
        b = f[k]
        sub = f"{md(b[2])}（{WD[__import__('datetime').date(int(b[2][:4]), int(b[2][4:6]), int(b[2][6:])).weekday()]}）・{b[1]}" if b else "この期間はネット予約の空きなし"
        pc.append(f'<div class="sc-price-card"><div class="lbl">{lbl}の最安（18ホール・税込総額）</div><div class="val">{yen(b)}</div><div class="sub">{sub}</div></div>')
    if nine:
        pc.append('<div class="sc-price-card"><div class="lbl">ご注意</div><div class="sub" style="font-size:13px;color:var(--charcoal);">9ホールのコースです。料金は、9ホールを2周するプランや回り放題のプランを含めた最安です。</div></div>')

    near = [x for x in DATA if x != slug and DATA[x]["area"] == c["area"]]
    near_html = "".join(f'<a href="course-saga-{x}.html">{DATA[x]["name"]}<span>{DATA[x]["city"]}・{DATA[x]["holes"]}ホール</span></a>' for x in near)
    near_html += f'<a href="{hub}">{"福岡から近い佐賀のゴルフ場" if hub == "saga-near-fukuoka.html" else "佐賀の名門ゴルフ場はどこ？"}<span>佐賀のコースをまとめて見る</span></a>'
    if fk:
        near_html += f'<a href="{fk[0]}">{fk[1]}<span>福岡県のコースも比べる</span></a>'

    few = "（空きが少なめです）" if 0 < days <= 3 else ""
    lead = (f"{c['city']}にある{c['holes']}ホールのコースです。じゃらん・楽天GORAで直近14日に空きがあったのは{days}日{few}。"
            if days else f"{c['city']}にある{c['holes']}ホールのコースです。")
    title = f"{c['name']}｜料金・予約・アクセス（佐賀県{c['city'].replace('三養基郡', '')}）"
    desc = (f"{c['name']}（佐賀県{c['city']}）の料金と予約。じゃらん・楽天GORAの直近14日の18ホール最安"
            f"（平日{yen(f['weekday'])}・土日祝{yen(f['weekend'])}、{checked_ja}確認）、コース情報、アクセスを出典つきでまとめました。")
    url = f"https://fukuoka-golf-guide.com/course-saga-{slug}.html"
    ld = {"@context": "https://schema.org", "@type": "GolfCourse", "name": c["name"], "url": url,
          "address": {"@type": "PostalAddress", "streetAddress": c["addr"].replace("佐賀県", "").replace(c["city"], "", 1) if c["addr"] else None,
                      "addressLocality": c["city"], "addressRegion": "佐賀県", "addressCountry": "JP"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "福岡ゴルフ場ガイド", "item": "https://fukuoka-golf-guide.com/"},
        {"@type": "ListItem", "position": 2, "name": "福岡から近い佐賀のゴルフ場" if hub == "saga-near-fukuoka.html" else "佐賀の名門ゴルフ場", "item": f"https://fukuoka-golf-guide.com/{hub}"},
        {"@type": "ListItem", "position": 3, "name": c["name"], "item": url}]}
    src_list = [f'<li>じゃらんゴルフ コース情報：<a href="{c["sources"]["jalan"]}" target="_blank" rel="noopener">{c["sources"]["jalan"]}</a></li>',
                f'<li>楽天GORA コースガイド：<a href="https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{c["rakuten_cid"]}" target="_blank" rel="noopener">booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{c["rakuten_cid"]}</a></li>']
    src_list += [f'<li>{v["source"]}：<a href="{v["url"]}" target="_blank" rel="noopener">{v["url"]}</a></li>' for v in c["verified"]]
    src_list = list(dict.fromkeys(src_list))

    return f"""<!DOCTYPE html>
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
  <link rel="canonical" href="{url}" />
  <link rel="alternate" hreflang="ja" href="{url}">
  <link rel="alternate" hreflang="x-default" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:url" content="{url}">
  <meta property="og:site_name" content="福岡ゴルフ場ガイド">
  <meta property="og:title" content="{c['name']}｜料金・予約・アクセス">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/images/{photo}">
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
  </script>
  <script type="application/ld+json">
{json.dumps(bc, ensure_ascii=False, indent=1)}
  </script>

{shared_head}
{CSS}
</head>
<body>{disclosure}<a href="{hub}" class="back-link">← 佐賀のコース一覧</a>

<section class="hero">
  <img class="hero-photo" src="images/{photo}" alt="イメージ写真（{photo_alt}・編集部撮影。{c['name']}の写真ではありません）" fetchpriority="high">
  <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Saga · {area_name}</div>
    <h1 class="hero-title">{c['name']}</h1>
    <p class="hero-sub">{lead}料金・コース情報・アクセスを、じゃらん・楽天GORA・公式サイトなどの掲載にもとづいてまとめました。</p>
  </div>
</section>

<div class="sc-ftv"><div class="sc-ftv-box">
  <div class="sc-ftv-price">平日 <strong>{yen(f['weekday'])}</strong>　土日祝 <strong>{yen(f['weekend'])}</strong><span style="font-size:12px;color:var(--muted);">（直近14日の18ホール最安・{checked_ja}確認）</span></div>
  <div class="sc-btns">{btns}</div>
</div></div>

<section class="section">
  <div class="sec-eyebrow">— Course Data</div>
  <h2 class="sec-title">コースの基本情報。</h2>
  <p class="sec-desc">各項目の下に、どこに書かれていた情報かを書いています。</p>
  <table class="sc-table"><tbody>{"".join(rows)}</tbody></table>
</section>

{facts_html}

<section class="section">
  <div class="sec-eyebrow">— Green Fee</div>
  <h2 class="sec-title">料金（直近14日の最安）。</h2>
  <p class="sec-desc">{checked_ja}に、じゃらん・楽天GORAの予約カレンダーで確認した{period}の18ホール最安（税込総額）です。両サイトのうち安い方を載せています。プランの条件（人数・昼食・時間帯）は予約画面で確認してください。</p>
  <div class="sc-price-grid">{"".join(pc)}</div>
  <div class="sc-btns">{btns}</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Nearby</div>
  <h2 class="sec-title">近くのコースも見る。</h2>
  <div class="sc-near">{near_html}</div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Sources</div>
  <h2 class="sec-title">出典。</h2>
  <ul class="sc-sources">{"".join(src_list)}</ul>
  <p class="sec-desc" style="margin-top:10px;">情報は{checked_ja}時点です。料金や営業日は変わることがあるので、予約前に予約サイトかコースで確認してください。電話番号は、予約サイトによって表記が異なる場合があるため載せていません。</p>
</section>

<div id="sc-sticky">{sticky}</div>

{footer}"""


res = []
for i, (slug, c) in enumerate(DATA.items()):
    if ONLY and slug != ONLY:
        continue
    html = page(slug, c, i)
    assert html.count("G-PENH0Z4VT7") == tpl.count("G-PENH0Z4VT7")
    for root in ROOTS:
        p = os.path.join(root, f"course-saga-{slug}.html")
        old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
        st = "new" if old is None else ("same" if old == html else "update")
        if APPLY and st != "same":
            open(p, "w", encoding="utf-8", newline="\n").write(html)
    res.append((slug, st))
print(res, "APPLIED" if APPLY else "DRY-RUN")
