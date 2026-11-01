#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
book-fukuoka-afternoon.html (午後スルー) を 2026-11-01 のじゃらん実データで書き直す。

旧ページは「午後スルー対応 9コース・平日¥5,869〜・安い順」だったが、
- 金額は午後スルーではなく各コースの平日18H最安 (2026年7月) で、¥5,869 も「時間限定・休憩あり」プラン
- 11/2〜11/15 (14日) のじゃらん全プランを見ると、プラン名に「午後スルー」があったのは福岡レイクサイドCCだけ
  (セントラルは午前スルーのみ・ミッション/WAKAMIYA は土日祝のスルーのみ・他4コースはスルーなし)
- 固定ボタンが「セントラル福岡」表記なのにミッションバレー (gc02338 / c_id 400045) へリンク
- course-card の閉じタグ不足でカードが入れ子
を是正する。料金は scripts/.cache/jalan_{gc}_{yyyymmdd}.html (2026-11-01 取得) を jalan_floor.parse と同じ規則で
読んだ値 (プラン料金・括弧内はじゃらん表示の総額)。西戸崎はじゃらん予約不可 (CLAUDE.md §9.4) で楽天は機械確認不可。
リンク文: guide-index / sitemap-guide / book-fukuoka-27holes / book-fukuoka-access の「9コース比較」「¥3,000台〜」も直す。
冪等: 置換後の文字列があれば no-op。
Usage:
  python scripts/rewrite_afternoon_2026_11.py            # dry-run
  python scripts/rewrite_afternoon_2026_11.py --preview  # PREVIEW だけに書く (確認用)
  python scripts/rewrite_afternoon_2026_11.py --apply    # REPO + PREVIEW
"""
import os, re, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
F = "book-fukuoka-afternoon.html"
A8_JALAN = "https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{gc}%2F"
A8_RAKUTEN = ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F"
              "0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp"
              "%252Fguide%252Fdisp%252Fc_id%252F{cid}%26m%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}")

# (slug, 名前, meta, jalan gc, 楽天 c_id, 午後スルー行 (main, disc) , 平日18H最安行 (main, disc) | None, tag)
COURSES = [
    ("lakeside", "福岡レイクサイドカントリークラブ", "飯塚市 ／ 18H ／ 福岡空港から約40分・PGM", "02346", "400044",
     ("¥8,969", "平日 総額¥10,400・14日中8日あり／土日祝¥12,150〜（総額¥13,900）は2日"),
     ("¥7,241", "総額¥8,500・4サム優待の午前スルー（1日のみ）"), "午後スルーあり"),
    ("central", "セントラル福岡ゴルフ倶楽部", "筑紫野市 ／ 18H ／ 福岡空港から約35〜45分・アコーディア", "02322", "400028",
     ("なし", "午前スルーは平日¥7,232〜（総額¥8,490）・7日"),
     ("¥6,323", "総額¥7,490・時間限定・休憩あり"), "午前スルーあり"),
    ("kurume", "久留米カントリークラブ", "八女郡広川町 ／ 18H ／ 福岡空港から約55分・筑後", "02356", "400014",
     ("なし", "スルーのプランなし"), ("¥6,137", "総額¥7,500"), None),
    ("moonlake", "ムーンレイクゴルフクラブ 鞍手コース", "鞍手郡鞍手町 ／ 27H ／ 福岡空港から約60分・PGM", "02339", "400013",
     ("なし", "スルーのプランなし"), ("¥6,355", "総額¥7,490"), None),
    ("ariake", "有明カントリークラブ", "大牟田市 ／ 18H ／ 福岡空港から約70分・筑後南部", "02315", "400003",
     ("なし", "スルーのプランなし"), ("¥6,773", "総額¥8,000"), None),
    ("mission", "ミッションバレーゴルフクラブ", "鞍手郡小竹町 ／ 18H ／ 福岡空港から約50分", "02338", "400045",
     ("なし", "土日祝のスループレー（キャディ付）¥20,100〜のみ"), ("¥9,455", "総額¥10,900"), None),
    ("wakamiya", "トライアルゴルフ&amp;リゾート WAKAMIYA COURSE", "宮若市 ／ 18H ／ 福岡空港から約50分・フラットで初心者向け", "02341", "400051",
     ("なし", "土日祝の《スルー》¥16,819〜が1日のみ"), ("¥10,455", "総額¥12,000"), None),
    ("ogori", "小郡カントリークラブ", "小郡市 ／ 27H ／ 福岡空港から約50分", "02321", "400008",
     ("なし", "スルーのプランなし"), ("なし", "平日の販売なし（土日祝¥19,091〜・1日のみ）"), None),
    ("saitozaki", "西戸崎シーサイドカントリークラブ", "福岡市東区 ／ 18H ／ 福岡空港から約30〜40分・海沿い", None, "400020",
     ("楽天で確認", "じゃらんでは予約不可・楽天GORAの枠は予約ページで"), None, None),
]


def price_row(label, main, disc):
    word = not main.startswith("¥")
    style = ' style="font-size:18px;"' if word else ""
    unit = "" if word else "〜"
    return (f'          <div class="price-row">\n'
            f'            <span class="price-label">{label}</span>\n'
            f'            <span class="price-main"{style}>{main}<span class="unit">{unit}</span></span>\n'
            f'            <span class="price-disc">{disc}</span>\n'
            f'          </div>\n')


def cards():
    out = []
    for i, (slug, name, meta, gc, cid, thru, floor, tag) in enumerate(COURSES, 1):
        featured = " featured" if tag == "午後スルーあり" else ""
        tag_html = f'\n            <span class="course-cheapest-tag">{tag}</span>' if tag else ""
        rows = price_row("午後スルー", *thru) + (price_row("平日18H最安", *floor) if floor else "")
        jalan = (f'            <a href="{A8_JALAN.format(gc=gc)}" class="btn-book btn-jalan" target="_blank" rel="nofollow sponsored noopener">'
                 f'📅 じゃらんで空き・プランを見る →</a>\n') if gc else ""
        out.append(
            f'      <!-- {i} {slug} -->\n'
            f'      <div class="course-card{featured}">\n'
            f'        <div class="course-card-body">\n'
            f'          <div class="course-head">\n'
            f'            <span class="course-rank-badge">{i}</span>\n'
            f'            <span class="course-name">{name}</span>{tag_html}\n'
            f'          </div>\n'
            f'          <div class="course-meta">{meta}</div>\n'
            f'{rows}'
            f'          <div class="cta-group">\n'
            f'{jalan}'
            f'            <a href="{A8_RAKUTEN.format(cid=cid)}" class="btn-book btn-rakuten" target="_blank" rel="nofollow sponsored noopener">🏌️ 楽天GORAで予約 →</a>\n'
            f'          </div>\n'
            f'          <p style="margin:10px 0 0;font-size:12px;"><a href="course-{slug}.html" style="color:inherit;">コース詳細 →</a></p>\n'
            f'        </div>\n'
            f'      </div>\n')
    return "\n".join(out)


DESC = ("福岡の9コースで「午後スルー」が予約できるかを、2026年11月1日にじゃらんゴルフの直近2週間（11/2〜11/15）で確認。"
        "11月に午後スルーがあったのは福岡レイクサイドCC（平日¥8,969〜）だけでした。午前スルーと平日18ホール最安も掲載。")
FAQ2 = ("2026年11月1日に、本ページの9コースについてじゃらんゴルフの11月2日〜15日（14日間）のプランを確認したところ、"
        "午後スルーがあったのは福岡レイクサイドカントリークラブだけでした（平日¥8,969〜・総額¥10,400、14日中8日）。"
        "セントラル福岡ゴルフ倶楽部は午前スルー（平日¥7,232〜）でした。午後スルーの設定日はコースが決めるため、"
        "最新の空き状況はじゃらんゴルフ・楽天GORAでご確認ください。")
FAQ4 = ("じゃらんゴルフ・楽天GORAとも、コースが設定した日のスループレーのプランを掲載しています。"
        "じゃらんゴルフはPontaポイント、楽天GORAは楽天ポイントが貯まり、料金は予約サイトごとに異なる場合があります。"
        "両方の料金を比較して選ぶのがおすすめです。本ページの各コースから両サイトの料金を確認できます。")
FAQ1_OLD = "料金も午前スタートより安く設定されているコースが多いため、コスパ重視のゴルファーに人気です。"
FAQ1_NEW = "料金はコース・日によって異なり、午前スタートと同じ料金の日もあります。"

REPL = [  # (pattern, replacement) — 各1回
    # 説明 (disc) に確認内容が入るので、ラベルは折り返さず・説明は次の行に読める色で
    (r"\.price-row \{ display: flex; ", ".price-row { display: flex; flex-wrap: wrap; "),
    (r"\.price-label \{ font-size: 12px; ", ".price-label { white-space: nowrap; font-size: 12px; "),
    (r"\.price-disc \{ font-size: 11px; color: #9CA3AF; margin-left: auto; \}",
     ".price-disc { font-size: 11.5px; color: #6B7280; flex-basis: 100%; line-height: 1.5; }"),
    (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">'),
    (r"<title>[^<]*</title>", "<title>福岡の午後スルー｜11月の設定状況を9コースで確認【じゃらん調べ】 | 福岡ゴルフ場ガイド</title>"),
    (r'"headline": "[^"]*"', '"headline": "福岡の午後スルー — 11月の設定状況を9コースで確認（2026年11月1日 じゃらん調べ）"'),
    (r'("@type": "Article",\s*"headline": "[^"]*",\s*"description": )"[^"]*"', r'\1"' + DESC + '"'),
    (r'"dateModified": "[^"]*"', '"dateModified": "2026-11-01"'),
    (r'"name": "午後スルー 9コース比較"', '"name": "午後スルーの設定状況"'),
    (r'(<meta property="og:title" content=")[^"]*"', r'\1福岡の午後スルー｜11月の設定状況を9コースで確認"'),
    (r'(<meta property="og:description" content=")[^"]*"', r'\1' + DESC + '"'),
    (r'("name": "福岡で午後スルーが一番安いゴルフ場はどこですか\?",\s*"acceptedAnswer": \{\s*"@type": "Answer",\s*"text": )"[^"]*"',
     r'\1"' + FAQ2 + '"'),
    (r'("text": )"両サイトとも午後スルー[^"]*"', r'\1"' + FAQ4 + '"'),
    (r'(<div class="faq-q">福岡で午後スルーが一番安いゴルフ場はどこですか\?</div>\s*<p class="faq-a">)[^<]*', r'\g<1>' + FAQ2),
    (r'(<p class="faq-a">)両サイトとも午後スルー[^<]*', r'\g<1>' + FAQ4),
    # 固定ボタン: 表記はセントラルなのにミッションへリンクしていた → 午後スルーを確認できたレイクサイドへ
    (r'<span class="sticky-label">[^<]*</span>\s*<a href="[^"]*" class="sticky-btn primary"',
     '<span class="sticky-label">🌇 11月に午後スルーを確認 福岡レイクサイド 平日¥8,969〜</span>\n'
     f'    <a href="{A8_JALAN.format(gc="02346")}" class="sticky-btn primary"'),
    (r'(class="sticky-btn primary"[^>]*>[^<]*</a>\s*<a href=")[^"]*(" class="sticky-btn rakuten")', r'\1' + A8_RAKUTEN.format(cid="400044") + r'\2'),
    (r'<p class="hero-sub">.*?</p>',
     '<p class="hero-sub">午後スタート・休憩なしで18ホールを一気に回る「午後スルー」。<br>福岡の9コースについて、'
     '<strong>2026年11月1日にじゃらんゴルフで直近2週間（11/2〜11/15）のプランを確認</strong>しました。'
     '11月に午後スルーがあったのは福岡レイクサイドCCだけでした。日没が早い季節は設定が少ないことがあるため、各予約サイトで最新の設定をご確認ください。</p>'),
    (r'<span class="hero-badge">🌇 午後スルー 9コース</span>', '<span class="hero-badge">🔎 9コースを調査</span>'),
    (r'<span class="hero-badge">💴 平日¥5,869〜</span>', '<span class="hero-badge">🌇 11月の午後スルー 1コース</span>'),
    (r'<span class="hero-badge">📅 じゃらん・楽天GORA予約可</span>', '<span class="hero-badge">📅 2026/11/1 じゃらん調べ</span>'),
    (r'料金も午前スタートより<strong>安く設定されているコースが多い</strong>のが特徴です。', '料金はコース・日によって異なります。'),
    (r'<b>💴 安い</b><span>[^<]*</span>', '<b>💴 料金</b><span>午前と同じ料金の日も（レイクサイドの11月平日は午前・午後とも¥8,969〜）</span>'),
    (r'<div class="sec-eyebrow">— Ranked by Price</div>', '<div class="sec-eyebrow">— Checked 2026-11-01</div>'),
    (r'<h2 class="sec-title">福岡の午後スルー、安い順 9コース。</h2>', '<h2 class="sec-title">9コースの「スルー」設定状況（11月）。</h2>'),
    (r'<p class="sec-subtitle">午後スルーなど短時間プラン[^\n]*</p>',
     '<p class="sec-subtitle">2026年11月1日に、じゃらんゴルフの各コースページで<strong>11月2日〜15日（14日間）の全プラン</strong>を確認し、'
     'プラン名に「スルー」を含む18ホールのプランを数えました。金額は1人あたりのプラン料金（総額はじゃらん表示の利用税等込み）。'
     '午後スルーの設定はコースが日ごとに決めるため、最新の空き状況は各コースのじゃらんゴルフ／楽天GORAでご確認ください。並びは午後スルーあり → 午前スルーあり → 平日18H最安の順です。</p>'),
    (r'掲載料金は目安であり、午後スルーの設定有無', '掲載料金は2026年11月1日時点の確認値であり、午後スルーの設定有無'),
]
LINKS = {  # 他ページのリンク文
    "guide-index.html": [
        ('"name": "午後スルー 9コース比較"', '"name": "午後スルーの設定状況"'),
        ('<span class="guide-badge">9コース</span></div>\n          <div class="guide-name">午後スルー 9コース比較</div>',
         '<span class="guide-badge">11月調べ</span></div>\n          <div class="guide-name">午後スルーの設定状況（9コース）</div>'),
        ('<div class="guide-desc">午後スタート・休憩なしで18ホール。¥3,000台〜・半日で回れるコスパ最強プラン。</div>',
         '<div class="guide-desc">午後スタート・休憩なしで18ホール。11月にじゃらんで午後スルーを確認できたのは1コース。実データで掲載。</div>'),
    ],
    "sitemap-guide.html": [
        ('🌇 午後スルー9コース比較<span>¥3,000台〜・半日18H・安い順・ミッションバレー/西戸崎ほか</span>',
         '🌇 午後スルーの設定状況（9コース）<span>2026年11月 じゃらん調べ・半日18H・レイクサイド/セントラルほか</span>'),
        ('🌇 Afternoon Through-Play 9 courses (JA)<span>From ¥3,000s · 18H in half a day · ranked by price</span>',
         '🌇 Afternoon Through-Play: 9 courses checked (JA)<span>Jalan data, Nov 2026 · 18H in half a day</span>'),
        ('🌇 오후 스루 9코스 비교 (일본어판)<span>¥3,000대~·반나절 18홀·저렴한 순·미션밸리/사이토자키 외</span>',
         '🌇 오후 스루 설정 현황 9코스 (일본어판)<span>2026년 11월 자란 조사·반나절 18홀</span>'),
    ],
    "book-fukuoka-27holes.html": [("🌇 午後スルー9コース →", "🌇 午後スルーの設定状況 →")],
    "book-fukuoka-access.html": [("🌇 午後スルー9コース →", "🌇 午後スルーの設定状況 →")],
}


def rewrite_page(src):
    s = src.replace("\r\n", "\n")
    s = s.replace(FAQ1_OLD, FAQ1_NEW)
    for pat, rep in REPL:
        s, k = re.subn(pat, rep, s, count=1, flags=re.S)
        assert k == 1, ("no match", pat[:60])
    m = re.search(r'(    <div class="course-grid">\n\n)(.*?)(\n\n    </div>\n  </div>\n\n  <!-- Tips -->)', s, re.S)
    assert m, "course-grid"
    s = s[:m.start(2)] + cards() + s[m.end(2):]
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(b)
    c = cards()
    assert c.count("<div") == c.count("</div>"), "div 不一致"
    return s


def main():
    results = {}
    src = open(os.path.join(REPO_ROOT, F), encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    if "午後スルーの設定状況" in src or "11月の設定状況を9コースで確認" in src:
        results[F] = "already"
    else:
        results[F] = rewrite_page(src).replace("\n", nl)
    for name, pairs in LINKS.items():
        t = open(os.path.join(REPO_ROOT, name), encoding="utf-8", newline="").read()
        n2 = "\r\n" if "\r\n" in t else "\n"
        u = t.replace("\r\n", "\n")
        hit = 0
        for a, b in pairs:
            if b in u:
                continue
            assert u.count(a) == 1, (name, a[:40])
            u = u.replace(a, b); hit += 1
        results[name] = u.replace("\n", n2) if hit else "already"
    for name, out in results.items():
        if out == "already":
            print(f"  [already] {name}"); continue
        print(f"  [change]  {name}")
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(out)
    print("APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
