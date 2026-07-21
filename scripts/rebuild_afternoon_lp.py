#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
午後スルーLP (book-fukuoka-afternoon.html) を じゃらん検証値ベースへ再構築 (案2)。

§7対応: 従来の「午後スルー¥3,000台〜」は じゃらん・楽天GORA いずれでも裏取り不能
        (コースページ側では既に「設定日限定」へ中立化済)。
方針  : トピック(午後スルー)は維持しつつ、掲載価格を**検証済の平日最安**へ載せ替え、
        表示の意味を「平日最安(2026年7月じゃらん調べ)」と正直に明記する。
        → 価格フックと「安い順」の並びを、検証済データで維持できる。

処理:
  1. 9枚の course-card を price_audit の weekday 昇順で並べ替え (不明は末尾)
  2. rank バッジ/「最安」タグ/featured クラスを並べ替え後に振り直し
  3. price-label「午後スルー」→「平日最安」、価格を検証値へ (不明は「要確認」)
  4. title/H1/meta/JSON-LD/sticky/hero の「¥3,000台〜」表現を是正

--dry-run 対応・両ROOT書き込み。
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
DRY = "--dry-run" in sys.argv
PAGE = "book-fukuoka-afternoon.html"

CARD_RE = re.compile(r'( *<!-- (\d+) ([a-z\-]+) -->\n)(.*?</div>\n *</div>\n)', re.S)


def main():
    audit = json.load(open(os.path.join(REPO_ROOT, "price_audit_2026-07.json"), encoding="utf-8"))["courses"]
    html = open(os.path.join(REPO_ROOT, PAGE), encoding="utf-8").read()

    cards = []
    for m in CARD_RE.finditer(html):
        slug = m.group(3)
        wd = audit.get("course-" + slug, {}).get("weekday")
        cards.append({"slug": slug, "block": m.group(0), "weekday": wd})
    if len(cards) != 9:
        print(f"!! card 検出数 {len(cards)} (期待9) — 中止")
        return

    span_start = html.index(cards[0]["block"])
    span_end = html.index(cards[-1]["block"]) + len(cards[-1]["block"])

    # 昇順ソート (不明=None は末尾)
    ordered = sorted(cards, key=lambda c: (c["weekday"] is None, c["weekday"] or 0))

    rebuilt = []
    for i, c in enumerate(ordered, 1):
        b = c["block"]
        b = re.sub(r'<!-- \d+ ([a-z\-]+) -->', lambda mm: f'<!-- {i} {mm.group(1)} -->', b)
        # featured / 最安タグ は 1位のみ
        b = b.replace('<div class="course-card featured">', '<div class="course-card">')
        b = re.sub(r'\s*<span class="course-cheapest-tag">最安</span>', '', b)
        if i == 1:
            b = b.replace('<div class="course-card">', '<div class="course-card featured">', 1)
            b = b.replace('</span>\n            <span class="course-meta">',
                          '</span>\n            <span class="course-cheapest-tag">最安</span>\n            <span class="course-meta">', 1)
            if 'course-cheapest-tag' not in b:
                b = re.sub(r'(<span class="course-name">[^<]*</span>)',
                           r'\1\n            <span class="course-cheapest-tag">最安</span>', b, count=1)
        b = re.sub(r'<span class="course-rank-badge">\d+</span>',
                   f'<span class="course-rank-badge">{i}</span>', b)
        # 価格行
        b = b.replace('<span class="price-label">午後スルー</span>',
                      '<span class="price-label">平日最安</span>')
        if c["weekday"]:
            new_price = f'<span class="price-main">¥{c["weekday"]:,}<span class="unit">〜</span></span>'
            disc = '<span class="price-disc">2026年7月 じゃらん調べ・変動あり</span>'
        else:
            new_price = '<span class="price-main" style="font-size:20px;">要確認<span class="unit"></span></span>'
            disc = '<span class="price-disc">最新料金は予約サイトでご確認ください</span>'
        b = re.sub(r'<span class="price-main">.*?</span></span>', new_price, b, flags=re.S)
        b = re.sub(r'<span class="price-disc">[^<]*</span>', disc, b)
        rebuilt.append(b)

    html = html[:span_start] + "".join(rebuilt) + html[span_end:]

    # ---- ページ全体の ¥3,000台〜 表現を是正 ----
    cheapest = ordered[0]
    c_name = {"mission": "ミッションバレーゴルフクラブ", "central": "セントラル福岡ゴルフ倶楽部",
              "moonlake": "ムーンレイクゴルフクラブ鞍手コース", "kurume": "久留米カントリークラブ",
              "ariake": "有明カントリークラブ", "lakeside": "福岡レイクサイドカントリークラブ",
              "wakamiya": "トライアルゴルフ&リゾート WAKAMIYA COURSE", "ogori": "小郡カントリークラブ",
              "saitozaki": "西戸崎シーサイドカントリークラブ"}[cheapest["slug"]]
    c_price = f'¥{cheapest["weekday"]:,}'

    repl = [
        ("福岡ゴルフ場「午後スルー」¥3,000台〜 9コース比較【半日で18H・コスパ最強】2026年版",
         f"福岡ゴルフ場「午後スルー」対応 9コース比較｜平日{c_price}〜【半日で18H】2026年版"),
        ("福岡のゴルフ場「午後スルー」プランを料金が安い順に9コース比較。¥3,000台〜・休憩なしで18ホールを半日で。ミッションバレー・西戸崎・久留米など、じゃらんゴルフ・楽天GORAの予約リンク付き。2026年版。",
         f"福岡で「午後スルー」プランが設定されることのあるゴルフ場9コースを、平日最安が安い順に比較（{c_name}の平日{c_price}〜など・2026年7月じゃらん調べ）。休憩なしで18ホールを半日で。じゃらんゴルフ・楽天GORAの予約リンク付き。"),
        ("福岡ゴルフ場「午後スルー」¥3,000台〜 9コース比較 — 半日で18ホール・コスパ最強【2026年版】",
         f"福岡ゴルフ場「午後スルー」対応 9コース比較 — 平日{c_price}〜・半日で18ホール【2026年版】"),
        ("福岡ゴルフ場「午後スルー」¥3,000台〜 9コース比較【半日で18H】",
         f"福岡ゴルフ場「午後スルー」対応 9コース比較｜平日{c_price}〜"),
        ('福岡ゴルフ場「午後スルー」<br>¥3,000台〜・半日で18ホール。',
         '福岡ゴルフ場「午後スルー」<br>半日で18ホール、賢く回る。'),
        ('<span class="hero-badge">💴 ¥3,000台〜</span>',
         f'<span class="hero-badge">💴 平日{c_price}〜</span>'),
        ('🌇 午後スルー最安 ミッションバレー ¥3,000台〜',
         f'🌇 平日最安 {c_name.split("ゴルフ")[0].split("カントリー")[0]} {c_price}〜'),
        ("本ページ掲載のなかではミッションバレーゴルフクラブ（鞍手郡小竹町・午後スルー¥3,000台〜）と西戸崎シーサイドカントリークラブ（福岡市東区・¥3,500台〜）が特に安い料金設定です。料金は時期・曜日・予約サイトにより変動するため、じゃらんゴルフ・楽天GORAで最新の空き状況をご確認ください。",
         f"本ページ掲載のなかでは{c_name}（平日{c_price}〜）が最も安い料金設定です（2026年7月時点のじゃらんゴルフ調べ・平日最安）。午後スルーなどの短時間プランは設定日限定で、料金は時期・曜日・予約サイトにより変動します。最新の空き状況と午後スルーの設定はじゃらんゴルフ・楽天GORAでご確認ください。"),
        ("各コースの午後スルー料金（目安・税込）を安い順に掲載。料金は時期・曜日・予約サイトにより変動します。最新の料金と空き状況は、各コースのじゃらんゴルフ／楽天GORAリンクからご確認ください。",
         "午後スルーなど短時間プランが設定されることのあるコースを、<strong>平日最安（2026年7月時点のじゃらんゴルフ調べ・税込）</strong>が安い順に掲載しています。午後スルーの設定日・料金は時期により変動するため、最新の空き状況は各コースのじゃらんゴルフ／楽天GORAリンクからご確認ください。"),
    ]
    hit = 0
    for old, new in repl:
        if old in html:
            html = html.replace(old, new)
            hit += 1

    print(f"並べ替え: {[ (c['slug'], c['weekday']) for c in ordered ]}")
    print(f"文言置換: {hit}/{len(repl)} 件ヒット")
    print(f"最安: {c_name} {c_price}")
    if DRY:
        print("\n※ DRY-RUN。書き込みなし。")
        return
    for root in ROOTS:
        p = os.path.join(root, PAGE)
        if os.path.exists(p):
            open(p, "w", encoding="utf-8").write(html)
    print("書き込み完了 (両ROOT)")


if __name__ == "__main__":
    main()
