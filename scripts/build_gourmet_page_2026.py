#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
「福岡のゴルフ場ランチ」ページ gourmet-fukuoka-golf.html を作る (日本語のみ)。
  専門家会議 (2026-11-28) の結論:
    - 載せるメニュー名・価格は、ゴルフ場の公式サイトで確認できたものだけ (2026-11-28 確認)。「名物」「絶品」「必食」「ランキング」とは書かない
      (芥屋の「芥屋ゴルフ倶楽部名物」は公式の表記として「」付きで引用)。
    - SNS は Instagram / Threads の公式埋め込みのみ (画像のダウンロード・転載はしない)。投稿の文章・ユーザー名は載せず、件数と趣旨だけ。
    - ネット予約できるコースは楽天GORA → じゃらんの順でボタン。玄海・芥屋は公式サイトのみ (CLAUDE.md §9.4)。
    - 浮羽は公式のランチメニューが画像の表紙・飲み物だけで料理を確認できないので「SNSに料理の写真があるコース」として別枠。
    - 夜須高原・クイーンズヒルは SNS で挙がった料理が公式メニューに無かったので載せない (注記のみ)。
  公式の確認先:
    志摩   https://simascc.com/restaurant/  (SHIMA SPECIALTIES「玄界灘産 天然鯛茶漬け」・グランドメニュー「海鮮皿うどん」。価格の記載なし)
    小郡   https://ogoricc.com/restaurant/  (和牛とろろ丼 2,480円 税込)
    WAKAMIYA https://trial-golf-resort-wakamiya-course.com/restaurants/ (手作りジューシーハンバーグ定食 1,650円 税込)
    玄海   https://genkai-gc.com/restaurant (玄界灘・真鯛 鯛茶漬け膳 ¥2,200・若鶏の半身揚げ ¥2,000 数量限定/プレー前に予約・特製海鮮ちゃんぽん ¥1,750。税込の表記なし)
    芥屋   https://www.keyagc.co.jp/restaurant/ (「芥屋ゴルフ倶楽部名物」鯛茶漬 2,720円 税込・海鮮丼 2,300円 税込)
    浮羽   https://ukiha-cc.com/restaurant/ (ランチ画像は表紙と飲み物・おつまみのみ)
Usage: python scripts/build_gourmet_page_2026.py [--apply]
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
R0 = ROOTS[0]
OUT = "gourmet-fukuoka-golf.html"
CHECKED = "2026年11月28日"
TAKEDOWN = ('掲載の取り下げは<a href="https://www.threads.com/@fukuoka_golf_guide1" target="_blank" rel="noopener">運営者のThreads</a>へご連絡ください'
            '（<a href="privacy.html">プライバシーポリシー</a>）。')


def jalan_url(jid):
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


# menu: (料理名, 価格の表示, 補足)。価格が公式に無いものは None
COURSES = [
    dict(slug="shimaseaside", name="志摩シーサイドカンツリークラブ", area="糸島市", cid="400024", jid="02352",
         src="https://simascc.com/restaurant/", src_label="公式サイト（レストラン）",
         menu=[("玄界灘産 天然鯛茶漬け", None, "公式で「SHIMA SPECIALTIES」として紹介"),
               ("海鮮皿うどん", None, "グランドメニュー")],
         price_note="公式サイトに価格の記載はありません。",
         sns="Instagramで、このコースの位置情報がついた投稿のうち、説明文で食事をほめていたものが3件、皿うどんの写真が1件ありました（編集部が2026年11月28日に確認）。",
         embeds=[("https://www.instagram.com/p/DemQhDuE6y_/", "皿うどんの写真（2026年10月の投稿）")],
         note="公式のレストランページは、海を望むクラブレストランとして紹介しています。"),
    dict(slug="ogori", name="小郡カンツリー倶楽部", area="小郡市", cid="400008", jid="02321",
         src="https://ogoricc.com/restaurant/", src_label="公式サイト（レストラン）",
         menu=[("和牛とろろ丼", "2,480円（税込）", "味噌汁・小鉢・漬物付")],
         price_note="",
         sns="Threadsに「ランチは和牛とろろ丼」と書いた投稿がありました（2026年4月。写真はコースの看板とフェアウェイ）。",
         embeds=[("https://www.threads.com/@hideyoshisato/post/DXtRHR8E51Y", "ランチに和牛とろろ丼を食べたという投稿（2026年4月）")],
         note=""),
    dict(slug="wakamiya", name="トライアルゴルフ&リゾート WAKAMIYA COURSE", area="宮若市", cid="400051", jid="02341",
         src="https://trial-golf-resort-wakamiya-course.com/restaurants/", src_label="公式サイト（レストラン）",
         menu=[("手作りジューシーハンバーグ定食（80g×3個）", "1,650円（税込）", "ご飯・味噌汁・サラダバイキング・お漬物付")],
         price_note="ハンバーグ定食は、エビフライや唐揚げとの組み合わせなど数種類あります。",
         sns="", embeds=[], note=""),
    dict(slug="genkai", name="玄海ゴルフクラブ", area="宗像市", cid=None, jid=None,
         src="https://genkai-gc.com/restaurant", src_label="公式サイト（レストラン）",
         menu=[("玄界灘・真鯛 鯛茶漬け膳", "¥2,200", ""),
               ("若鶏の半身揚げ", "¥2,000", "数量限定・プレー前に予約"),
               ("特製海鮮ちゃんぽん", "¥1,750", "")],
         price_note="公式サイトに税込かどうかの記載はありません。",
         sns="", embeds=[],
         note="予約はメンバー本人からの完全予約制です（公式）。ゲストは公式サイトのゲスト申込書で申し込みます。じゃらん・楽天GORAでは予約できません。"),
    dict(slug="keya", name="芥屋ゴルフ倶楽部", area="糸島市", cid=None, jid=None,
         src="https://www.keyagc.co.jp/restaurant/", src_label="公式サイト（レストラン）",
         menu=[("鯛茶漬", "2,720円（税込）", "公式の表記は「芥屋ゴルフ倶楽部名物」。玄海産の天然鯛使用・小鉢・デザート付"),
               ("海鮮丼", "2,300円（税込）", "小鉢・汁物付")],
         price_note="鯛茶漬は持ち帰り用もあると公式に書かれています。",
         sns="", embeds=[],
         note="じゃらん・楽天GORAでは予約できません。予約は公式サイトか電話です。"),
]
UKIHA = dict(slug="ukiha", name="浮羽カントリークラブ", area="うきは市", cid="400007", jid="02353",
             src="https://ukiha-cc.com/restaurant/",
             embeds=[("https://www.instagram.com/p/DgE1K3aTS3V/", "「ビーフバター」と書かれたパスタの写真（2026年11月の投稿）")])


def embed_card(url, note):
    if "instagram.com" in url:
        at = f'class="instagram-media" data-instgrm-permalink="{url}" data-instgrm-version="14"'
        lbl = "この投稿をInstagramで見る"
    else:
        at = f'class="text-post-media" data-text-post-permalink="{url}" data-text-post-version="0"'
        lbl = "この投稿をThreadsで見る"
    return (f'<div class="gm-embed"><p class="gm-enote">{note}</p>'
            f'<blockquote {at} style="margin:0;max-width:100%;"><a href="{url}" target="_blank" rel="noopener">{lbl}</a></blockquote></div>')


def buttons(c, official):
    if c.get("cid"):
        return (f'<div class="gm-btns"><a href="{rakuten_url(c["cid"])}" class="gm-btn gm-rak" target="_blank" rel="nofollow sponsored noopener">楽天GORAで空きを見る</a>'
                f'<a href="{jalan_url(c["jid"])}" class="gm-btn gm-jal" target="_blank" rel="nofollow sponsored noopener">じゃらんで空きを見る</a></div>')
    return f'<div class="gm-btns"><a href="{official}" class="gm-btn gm-off" target="_blank" rel="noopener">公式サイトで予約方法を見る</a></div>'


OFFICIAL_TOP = {"genkai": "https://genkai-gc.com/", "keya": "https://www.keyagc.co.jp/"}

rows, cards = [], []
for c in COURSES:
    first = c["menu"][0]
    book = "楽天GORA・じゃらん" if c["cid"] else "公式サイトのみ"
    rows.append(f'<tr><td class="gm-n"><a href="course-{c["slug"]}.html">{c["name"]}</a><span>{c["area"]}</span></td>'
                f'<td>{"<br>".join(m[0] for m in c["menu"])}</td>'
                f'<td class="gm-p">{"<br>".join(m[1] or "記載なし" for m in c["menu"])}</td><td>{book}</td></tr>')
    menu = "".join(f'<li><strong>{n}</strong>{"　<span class=gm-yen>" + p + "</span>" if p else ""}{"<br><span class=gm-sub>" + s + "</span>" if s else ""}</li>' for n, p, s in c["menu"])
    parts = [f'<div class="gm-card" id="{c["slug"]}"><div class="gm-name">{c["name"]} <a href="course-{c["slug"]}.html" class="gm-more">コース詳細 →</a></div>',
             f'<div class="gm-meta">{c["area"]}｜予約：{book}</div>',
             f'<ul class="gm-menu">{menu}</ul>',
             f'<p class="gm-src">出典：<a href="{c["src"]}" target="_blank" rel="noopener">{c["src_label"]}</a>（{CHECKED}確認）{c["price_note"]}</p>']
    if c["note"]:
        parts.append(f'<p class="gm-note">{c["note"]}</p>')
    if c["sns"]:
        parts.append(f'<p class="gm-sns"><strong>SNSでは：</strong>{c["sns"]}</p>')
    if c["embeds"]:
        parts.append('<div class="gm-embeds">' + "".join(embed_card(u, n) for u, n in c["embeds"]) + '</div>')
    parts.append(buttons(c, OFFICIAL_TOP.get(c["slug"], c["src"])))
    parts.append('</div>')
    cards.append("".join(parts))

ukiha_html = (f'<div class="gm-card" id="ukiha"><div class="gm-name">{UKIHA["name"]} <a href="course-ukiha.html" class="gm-more">コース詳細 →</a></div>'
              f'<div class="gm-meta">{UKIHA["area"]}｜予約：楽天GORA・じゃらん</div>'
              f'<p class="gm-note">Instagramで、このコースの位置情報がついた投稿に料理の写真がありました。ほかに説明文で「お蕎麦」「昆布うどん」に触れた投稿が2件ありました（いずれも2022年）。'
              f'公式サイトの<a href="{UKIHA["src"]}" target="_blank" rel="noopener">レストランのページ</a>に載っているランチの画像は表紙と飲み物・おつまみだけで、料理のメニューは確認できませんでした（{CHECKED}確認）。'
              'メニューは変わることがあるので、当日レストランで確かめてください。</p>'
              '<div class="gm-embeds">' + "".join(embed_card(u, n) for u, n in UKIHA["embeds"]) + '</div>'
              + buttons(UKIHA, "") + '</div>')

all_emb = [u for c in COURSES for u, _ in c["embeds"]] + [u for u, _ in UKIHA["embeds"]]
srcs = [u for u, k in (("https://www.instagram.com/embed.js", "instagram.com"), ("https://www.threads.com/embed.js", "threads.")) if any(k in x for x in all_emb)]
loader = ("<script>(function(){var e=document.querySelectorAll('.gm-embeds');if(!e.length)return;var done=false;function l(){if(done)return;done=true;["
          + ",".join(f"'{u}'" for u in srcs) + "].forEach(function(u){var s=document.createElement('script');s.src=u;s.async=true;document.body.appendChild(s);});}"
          "if(!('IntersectionObserver' in window)){l();return;}var o=new IntersectionObserver(function(x){x.forEach(function(i){if(i.isIntersecting){o.disconnect();l();}});},{rootMargin:'400px'});"
          "e.forEach(function(n){o.observe(n);});})();</script>")

faq = [
    ("福岡で鯛茶漬けが食べられるゴルフ場は？",
     f"公式サイトのレストランメニューで確認できたのは、志摩シーサイドカンツリークラブ（玄界灘産 天然鯛茶漬け）、玄海ゴルフクラブ（玄界灘・真鯛 鯛茶漬け膳 ¥2,200）、芥屋ゴルフ倶楽部（鯛茶漬 2,720円・税込）の3コースです（{CHECKED}確認）。"),
    ("ゴルフ場のランチ代はいくらくらい？",
     f"このページで確認したメニューは1,650円〜2,720円でした（{CHECKED}時点の公式サイトの表示）。プランによってはランチ代が料金に含まれるものもあるので、予約画面のプラン内容を確認してください。"),
    ("玄海ゴルフクラブや芥屋ゴルフ倶楽部はネットで予約できますか？",
     "じゃらん・楽天GORAでは予約できません。玄海ゴルフクラブはメンバー本人からの完全予約制で、ゲストは公式サイトのゲスト申込書で申し込みます。芥屋ゴルフ倶楽部は公式サイトか電話で予約します。"),
    ("メニューや価格は変わりますか？",
     f"変わることがあります。このページの内容は{CHECKED}に各ゴルフ場の公式サイトで確認したものです。季節限定のメニューもあるので、最新の内容は公式サイトかレストランで確かめてください。"),
]
faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}, ensure_ascii=False, indent=1)
item_ld = json.dumps({"@context": "https://schema.org", "@type": "ItemList", "name": "公式サイトでランチメニューを確認できた福岡のゴルフ場",
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c["name"], "url": f"https://fukuoka-golf-guide.com/course-{c['slug']}.html"}
                                          for i, c in enumerate(COURSES)]}, ensure_ascii=False, indent=1)
faq_html = "".join(f'<div class="faq-item"><div class="faq-q">{q}</div><div class="faq-a">{a}</div></div>' for q, a in faq)

title = "福岡のゴルフ場ランチ｜公式メニューで確かめた5コース（鯛茶漬け・和牛とろろ丼ほか）"
desc = ("福岡のゴルフ場のランチを、各コースの公式サイトのメニューで確認して紹介。志摩シーサイドの天然鯛茶漬け、小郡CCの和牛とろろ丼（2,480円）、"
        "WAKAMIYAのハンバーグ定食（1,650円）、玄海GCの鯛茶漬け膳、芥屋GCの鯛茶漬。SNSに上がった料理の写真も公式埋め込みで。2026年11月確認。")

tpl = open(os.path.join(R0, "book-fukuoka-tomorrow.html"), encoding="utf-8").read()
shared_head = tpl[tpl.index("  <!-- Google Analytics -->"):tpl.index("</style>", tpl.index("  <style>")) + len("</style>")]
body_start = tpl.index("<body>") + len("<body>")
disclosure = tpl[body_start:tpl.index('<a href="/" class="back-link">')]
footer = tpl[tpl.index("<footer>"):]
CSS = """
  <style>
    .gm-wrap { overflow-x:auto; border:1px solid var(--line); border-radius:14px; background:#fff; }
    .gm-table { border-collapse:collapse; width:100%; min-width:620px; font-size:13.5px; }
    .gm-table th { background:var(--forest-dark); color:#fff; padding:10px 8px; font-size:12px; text-align:left; white-space:nowrap; }
    .gm-table td { border-top:1px solid var(--line); padding:10px 8px; vertical-align:top; line-height:1.7; }
    .gm-n { font-weight:700; color:var(--forest-dark); }
    .gm-n a { color:inherit; border-bottom:1px dotted; }
    .gm-n span { display:block; font-weight:400; font-size:11.5px; color:var(--muted); }
    .gm-p { font-family:var(--num); font-weight:700; color:var(--orange-dark); white-space:nowrap; }
    .gm-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(min(360px,100%),1fr)); gap:16px; }
    .gm-card { background:#fff; border:1px solid var(--line); border-radius:16px; padding:18px 20px; min-width:0; }
    .gm-name { font-family:var(--serif); font-weight:700; font-size:18px; color:var(--forest-dark); margin-bottom:4px; }
    .gm-more { font-family:var(--sans,inherit); font-size:12.5px; font-weight:700; color:#1a5fa0; }
    .gm-meta { font-size:12.5px; color:var(--muted); }
    .gm-menu { margin:12px 0 8px 18px; font-size:14.5px; line-height:1.8; }
    .gm-yen { font-family:var(--num); font-weight:700; color:var(--orange-dark); }
    .gm-sub { font-size:12px; color:var(--muted); }
    .gm-src { font-size:12px; color:var(--muted); line-height:1.7; }
    .gm-src a, .gm-note a { color:var(--ocean-dark); border-bottom:1px dotted var(--ocean); }
    .gm-note { font-size:13px; color:var(--charcoal); line-height:1.75; margin:8px 0; }
    .gm-sns { font-size:13px; line-height:1.75; background:var(--pale,#f4f7f2); border-radius:10px; padding:10px 12px; margin:10px 0; }
    .gm-embeds { display:grid; gap:12px; margin:12px 0; }
    .gm-embed { min-height:420px; min-width:0; }
    .gm-enote { font-size:12px; color:var(--muted); margin:0 0 8px; }
    .gm-btns { display:flex; gap:8px; flex-wrap:wrap; margin-top:12px; }
    .gm-btn { flex:1; min-width:140px; text-align:center; color:#fff; font-weight:700; font-size:13px; padding:11px 12px; border-radius:10px; }
    .gm-rak { background:linear-gradient(135deg,#c81d1d,#8f0000); }
    .gm-jal { background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }
    .gm-off { background:var(--forest-dark); }
    .gm-list { font-size:14px; line-height:1.9; max-width:820px; padding-left:20px; }
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
  <meta property="og:title" content="福岡のゴルフ場ランチ｜公式メニューで確かめた5コース">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/images/kaho-play-1.webp">
  <script type="application/ld+json">
{item_ld}
  </script>
  <script type="application/ld+json">
{faq_ld}
  </script>
  <script type="application/ld+json">
  {{"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
    {{"@type":"ListItem","position":1,"name":"福岡ゴルフ場ガイド","item":"https://fukuoka-golf-guide.com/"}},
    {{"@type":"ListItem","position":2,"name":"観光と一緒に楽しむゴルフ場","item":"https://fukuoka-golf-guide.com/hub-traveler.html"}},
    {{"@type":"ListItem","position":3,"name":"福岡のゴルフ場ランチ","item":"https://fukuoka-golf-guide.com/{OUT}"}}]}}
  </script>

{shared_head}
{CSS}
</head>
<body>{disclosure}<a href="/" class="back-link">← Top</a>

<section class="hero">
  <img class="hero-photo" src="images/kaho-play-1.webp" alt="イメージ写真（福岡県のかほゴルフクラブ・編集部撮影）" fetchpriority="high">
  <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Golf Course Lunch</div>
    <h1 class="hero-title">福岡のゴルフ場ランチ。<br>公式メニューで確かめた5コース。</h1>
    <p class="hero-sub">SNSで食事の話題が出ていたコースについて、各ゴルフ場の公式サイトのメニューを確認し、載っていた料理と価格だけをまとめました。SNSに上がった料理の写真は、公式の埋め込みで紹介しています（{CHECKED}確認）。</p>
    <div class="hero-badges">
      <span class="hero-badge">🐟 鯛茶漬けは3コース</span>
      <span class="hero-badge">🍽️ 1,650円〜2,720円</span>
      <span class="hero-badge">✅ 公式メニューで確認</span>
    </div>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Compare</div>
  <h2 class="sec-title">5コースのランチを一覧で。</h2>
  <p class="sec-desc">価格は公式サイトの表示どおりです。「記載なし」は、公式サイトに価格が載っていなかったものです。</p>
  <div class="gm-wrap"><table class="gm-table"><thead><tr><th>コース</th><th>公式に載っている料理</th><th>価格</th><th>予約</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Courses</div>
  <h2 class="sec-title">コースごとに、出典と一緒に。</h2>
  <p class="sec-desc">上の3コースはじゃらん・楽天GORAで予約できます。玄海と芥屋はネットの予約サイトでは予約できないので、公式サイトへのリンクだけにしています。</p>
  <div class="gm-grid">{"".join(cards)}</div>
  <p style="margin-top:14px;font-size:12px;line-height:1.7;color:var(--muted);">投稿はInstagram・Threadsの公式埋め込みで紹介しています。表示されない場合は、元の投稿が削除されたか非公開になった可能性があります。{TAKEDOWN}</p>
</section>

<section class="section">
  <div class="sec-eyebrow">— On SNS</div>
  <h2 class="sec-title">SNSに料理の写真があるコース。</h2>
  <p class="sec-desc">公式サイトでメニューを確認できなかったため、上の5コースとは分けて載せています。</p>
  <div class="gm-grid">{ukiha_html}</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— FAQ</div>
  <h2 class="sec-title">よくある質問。</h2>
  <div class="faq-list">{faq_html}</div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Notes</div>
  <h2 class="sec-title">このページについて。</h2>
  <ul class="gm-list">
    <li>料理名と価格は、各ゴルフ場の公式サイトのレストランのページで{CHECKED}に確認したものです。メニューや価格は変わることがあります。</li>
    <li>SNSの投稿は、Instagramの位置情報つき投稿とThreadsの検索で編集部が確認しました。投稿の文章やユーザー名は載せず、写真は公式の埋め込みだけを使っています。</li>
    <li>夜須高原カントリークラブとクイーンズヒルゴルフクラブは、SNSで話題に出ていた料理が公式サイトのメニューに見当たらなかったため、今回は載せていません。</li>
    <li>このページの「予約」ボタンはアフィリエイトリンクです。お店の評価や順位をつけたものではありません。</li>
  </ul>
</section>

<section class="section">
  <div class="sec-eyebrow">— Related Pages</div>
  <h2 class="sec-title">関連ページ。</h2>
  <div class="related-grid">
    <a href="hub-traveler.html" class="related-card"><span class="related-name">🌊 観光と一緒に楽しむゴルフ場</span><span class="related-arrow">→</span></a>
    <a href="area-itoshima.html" class="related-card"><span class="related-name">⛳ 糸島エリアのゴルフ場</span><span class="related-arrow">→</span></a>
    <a href="/" class="related-card"><span class="related-name">🏠 福岡の全コースを比べる</span><span class="related-arrow">→</span></a>
  </div>
</section>
{loader}

{footer}"""

assert html.count("G-PENH0Z4VT7") == tpl.count("G-PENH0Z4VT7")
for bad in ("絶品", "必食", "ランキング", "No.1"):
    assert bad not in html.replace("ランキング</", ""), bad
for root in ROOTS:
    p = os.path.join(root, OUT)
    old = open(p, encoding="utf-8").read() if os.path.exists(p) else None
    print(root, "new" if old is None else ("same" if old == html else "update"))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="\n").write(html)
print("embeds", len(all_emb), "APPLIED" if APPLY else "DRY-RUN")
