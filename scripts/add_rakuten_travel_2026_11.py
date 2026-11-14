#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
空港から遠いコースのページに「前泊・後泊の宿を探す」(楽天トラベル・楽天アフィリエイト) を入れる (2026-11-14 テスト 3 コース)。
  リンクはサイト内の楽天GORAリンクと同じ A8 経由の楽天アフィリエイト形式 (a8mat=4B1D5J+4P34KY+2HOM+BW8O1)。
  行き先は楽天トラベルの地域ページ (2026-11-14 に存在とページ名を確認):
    kitakyusyu.html「北九州」/ buzen.html「北九州空港・苅田・行橋・豊前」/ kurume.html「久留米・甘木・原鶴温泉・筑後川温泉」
  入れる位置: 日本語ブロックの天気予報欄 (jma-weather-v1) の直後。ゴルフ場の予約ボタンではない (宿の検索)。
  【PR】広告表示が無いページ (門司) には他ページと同じものを足す。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/add_rakuten_travel_2026_11.py [--apply]
"""
import os, sys
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARK = "<!-- rakuten-travel-v1 -->"


def rakuten(url):
    inner = "http://hb.afl.rakuten.co.jp/hgc/0eb4cf04.fd65a65c.0eb4cf05.fa3f041c/a26040498058_4B1D5J_4P34KY_2HOM_7O29U?pc=" + quote(url, safe="") + "&m=" + quote(url, safe="")
    return "https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=" + quote(inner, safe="")


PLAN = {
    "course-moji.html": ("https://travel.rakuten.co.jp/yado/fukuoka/kitakyusyu.html", "北九州",
                         "福岡空港からは車で約1時間30分（公式）。朝のスタートに合わせるなら、北九州に前泊する方法もあります。"),
    "course-suonada.html": ("https://travel.rakuten.co.jp/yado/fukuoka/buzen.html", "北九州空港・苅田・行橋・豊前",
                            "福岡市内からは遠いコースです。朝のスタートに合わせるなら、近くのエリアに前泊する方法もあります。"),
    "course-ukiha.html": ("https://travel.rakuten.co.jp/yado/fukuoka/kurume.html", "久留米・甘木・原鶴温泉・筑後川温泉",
                          "前泊や、プレー後にゆっくり泊まるなら、このあたりの宿も探せます。"),
}

PR_STYLE = '<style>.ad-disclosure{background:#f4f1ea;color:#555;font-size:11.5px;line-height:1.6;padding:8px 16px;text-align:center;border-bottom:1px solid #e3ddcf;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;}.ad-disclosure strong{color:#333;}.ad-disclosure a{color:#555;text-decoration:underline;}body>.back-link,body>.lang-switcher{top:46px;}@media (max-width:900px){.ad-disclosure{font-size:11px;padding:7px 12px;}.ad-disclosure .ad-d-long{display:none;}}</style>'
PR_DIV = '<div class="ad-disclosure" role="note"><strong>【PR】</strong>本ページはアフィリエイト広告を含みます。<span class="ad-d-long">掲載している予約サイト等のリンクから予約・購入されると、当サイトに報酬が支払われる場合があります。</span><a href="editorial-policy.html">詳しく</a><span class="ad-d-long" lang="en"> / Contains affiliate ads.</span><span class="ad-d-long" lang="ko"> / 제휴 광고를 포함합니다.</span></div>'


def box(url, area, text):
    return f"""
  {MARK}
  <aside class="stay-box" aria-label="宿を探す（広告）">
    <style>.stay-box{{width:calc(100% - 32px);max-width:880px;box-sizing:border-box;margin:8px auto 40px;padding:18px 20px;border:1px solid #e3ddcf;border-left:5px solid #bf0000;border-radius:14px;background:#fff;}}.stay-box-label{{font-size:11px;color:#888;letter-spacing:.1em;}}.stay-box-title{{font-weight:700;font-size:16px;color:#1a5c38;margin:4px 0 6px;}}.stay-box p{{font-size:13.5px;line-height:1.7;color:#333;margin:0 0 12px;}}.stay-box-btn{{display:inline-block;background:#bf0000;color:#fff;font-weight:700;font-size:14px;padding:11px 20px;border-radius:999px;text-decoration:none;}}</style>
    <div class="stay-box-label">PR（広告）</div>
    <div class="stay-box-title">🏨 前泊・後泊の宿を探す</div>
    <p>{text}</p>
    <a href="{rakuten(url)}" class="stay-box-btn" rel="nofollow sponsored" target="_blank" aria-label="楽天トラベル {area}の宿（広告）">楽天トラベルで「{area}」の宿を見る →</a>
  </aside>
"""


for root in ROOTS:
    print(root)
    for f, (url, area, text) in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if MARK in s:
            print(f"  {f}: already"); continue
        nl = "\r\n" if "\r\n" in s else "\n"
        w = s.replace("\r\n", "\n")
        anchor = '  <script src="weather-jma.js" defer></script>\n'
        assert w.count(anchor) == 1, f
        new = w.replace(anchor, anchor + box(url, area, text), 1)
        added_pr = False
        if "ad-disclosure" not in new:
            assert new.count("<body>\n") == 1
            new = new.replace("<body>\n", "<body>\n" + PR_STYLE + "\n" + PR_DIV + "\n", 1)
            added_pr = True
        new = new.replace("\n", nl)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {f}: 楽天トラベル「{area}」{'・PR表示を追加' if added_pr else ''}")
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
