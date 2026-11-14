#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天市場 (楽天アフィリエイト) のゴルフ用品リンクを、話題が合う場所に入れる (2026-11-14)。
  行き先は楽天市場の検索結果 (特定商品は推さない・価格や在庫は書かない)。検索結果が出ることを確認済み:
    ゴルフ グローブ / ゴルフボール / ゴルフシューズ / ゴルフ レインウェア / グリーンフォーク / ゴルフ ボールマーカー
  1. golf-dresscode.html「当日の持ち物チェックリスト」の後
  2. golf-manner.html「グリーン上のマナー」の後 (グリーンフォーク・ボールマーカー)
  3. コースページ 3 件 (若松・玄海・油山) の天気予報欄の直後に「雨の予報なら」(テスト)
  1・2 は【PR】広告表示とクリック計測が無いので足す (click_affiliate・service rakuten_ichiba)。
  コースページは既存の計測 (click_affiliate) が拾う。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/add_rakuten_ichiba_2026_11.py [--apply]
"""
import os, sys
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARK = "<!-- rakuten-ichiba-v1 -->"


def rakuten(kw):
    url = "https://search.rakuten.co.jp/search/mall/" + quote(kw) + "/"
    inner = "http://hb.afl.rakuten.co.jp/hgc/0eb4cf04.fd65a65c.0eb4cf05.fa3f041c/a26040498058_4B1D5J_4P34KY_2HOM_7O29U?pc=" + quote(url, safe="") + "&m=" + quote(url, safe="")
    return "https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=" + quote(inner, safe="")


CSS = ('<style>.ichiba-box{width:calc(100% - 32px);max-width:880px;box-sizing:border-box;margin:24px auto;padding:16px 18px;border:1px solid #e3ddcf;border-left:5px solid #bf0000;border-radius:14px;background:#fff;}'
       '.ichiba-label{font-size:11px;color:#888;letter-spacing:.1em;}.ichiba-title{font-weight:700;font-size:15px;color:#1a5c38;margin:4px 0 6px;}'
       '.ichiba-box p{font-size:13px;line-height:1.7;color:#444;margin:0 0 10px;}.ichiba-links{display:flex;flex-wrap:wrap;gap:8px;}'
       '.ichiba-links a{display:inline-block;background:#bf0000;color:#fff;font-weight:700;font-size:13px;padding:9px 14px;border-radius:999px;text-decoration:none;}</style>')


def box(title, text, items, page=None):
    track = ""
    links = []
    for label, kw in items:
        if page:
            track = (f''' onclick="if(window.gtag)gtag('event','click_affiliate',{{service:'rakuten_ichiba',page:'{page}',lang:'ja',cta_position:'item_links',link_text:'{label}'}})"''')
        links.append(f'<a href="{rakuten(kw)}" rel="nofollow sponsored" target="_blank" aria-label="楽天市場 {label}（広告）"{track}>{label} →</a>')
    return f"""
  {MARK}
  <aside class="ichiba-box" aria-label="楽天市場（広告）">
    {CSS}
    <div class="ichiba-label">PR（広告）</div>
    <div class="ichiba-title">{title}</div>
    <p>{text}</p>
    <div class="ichiba-links">{''.join(links)}</div>
  </aside>
"""


NOTE = "楽天市場の検索結果を開きます。価格・在庫・サイズは各ショップでご確認ください。"
PR_STYLE = '<style>.ad-disclosure{background:#f4f1ea;color:#555;font-size:11.5px;line-height:1.6;padding:8px 16px;text-align:center;border-bottom:1px solid #e3ddcf;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;}.ad-disclosure strong{color:#333;}.ad-disclosure a{color:#555;text-decoration:underline;}body>.back-link,body>.lang-switcher{top:46px;}@media (max-width:900px){.ad-disclosure{font-size:11px;padding:7px 12px;}.ad-disclosure .ad-d-long{display:none;}}</style>'
PR_DIV = '<div class="ad-disclosure" role="note"><strong>【PR】</strong>本ページはアフィリエイト広告を含みます。<span class="ad-d-long">掲載している予約サイト等のリンクから予約・購入されると、当サイトに報酬が支払われる場合があります。</span><a href="editorial-policy.html">詳しく</a><span class="ad-d-long" lang="en"> / Contains affiliate ads.</span><span class="ad-d-long" lang="ko"> / 제휴 광고를 포함합니다.</span></div>'

RAIN = ("☔ 雨の予報なら", "ゴルフ用のレインウェアがあると、雨の日のラウンドが楽になります。" + NOTE, [("ゴルフ用レインウェア", "ゴルフ レインウェア")])

PLAN = [
    ("golf-dresscode.html", '    <h2 id="faq">7. よくある質問</h2>', "before",
     box("🛒 持ち物をそろえるなら（楽天市場）", NOTE, [("ゴルフグローブ", "ゴルフ グローブ"), ("ゴルフボール", "ゴルフボール"), ("ゴルフシューズ", "ゴルフシューズ"), ("レインウェア", "ゴルフ レインウェア")], page="golf-dresscode")),
    ("golf-manner.html", '    <h2 id="bunker">', "before",
     box("🛒 グリーンフォーク・ボールマーカー（楽天市場）", "ボールマークを直すグリーンフォークと、ボールの位置に置くマーカーは、1つずつ持っておくと安心です。" + NOTE,
         [("グリーンフォーク", "グリーンフォーク"), ("ボールマーカー", "ゴルフ ボールマーカー")], page="golf-manner")),
]
for f in ("course-wakamatsu.html", "course-genkai.html", "course-aburayama.html"):
    PLAN.append((f, '  <script src="weather-jma.js" defer></script>\n', "after", box(*RAIN)))

for root in ROOTS:
    print(root)
    for f, anchor, where, html in PLAN:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if MARK in s:
            print(f"  {f}: already"); continue
        nl = "\r\n" if "\r\n" in s else "\n"
        w = s.replace("\r\n", "\n")
        assert w.count(anchor) == 1, (f, w.count(anchor))
        new = w.replace(anchor, (html + "\n" + anchor) if where == "before" else (anchor + html), 1)
        added = False
        if "ad-disclosure" not in new:
            assert new.count("<body>\n") == 1, f
            new = new.replace("<body>\n", "<body>\n" + PR_STYLE + "\n" + PR_DIV + "\n", 1)
            added = True
        new = new.replace("\n", nl)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {f}: 追加{'・PR表示を追加' if added else ''}")
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
