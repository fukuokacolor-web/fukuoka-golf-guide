#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hub-business.html (日本語) の予約導線を補う。
  背景 (2026-11-23): 流入1位 (GA4 350ビュー/4週・GSC「福岡 名門ゴルフ場」2位前後・「福岡 ゴルフ場」8.8位) なのに
  予約クリックが5回。10コース中8コースは会員制・公式のみでネット予約ができず、押せるのは
  センチュリー・太宰府の「じゃらん」ボタンだけだった。
  1) センチュリー・太宰府のカードに楽天GORAボタンを追加 (2026-11-23 に楽天で空きを確認: 14日中14日・9日)
  2) 一覧の直前に「ネットで予約できるのは2コース」の案内 (両コースのじゃらん・楽天ボタン)
EN/KO は触らない。冪等 (MARKER)。改行コードはそのまま。
Usage: python scripts/hub_business_bookable_2026_11.py [--apply]
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARKER = "hub-business-bookable-v1"
JALAN = {"century": "02319", "dazaifu": "02327"}
RAKUTEN = {"century": "400042", "dazaifu": "400031"}
NAME = {"century": "福岡センチュリーゴルフ倶楽部", "dazaifu": "太宰府ゴルフ倶楽部"}


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


def jalan_url(jid):
    return f"https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"


CSS_ANCHOR = "    .btn-jalan-s {"
CSS = ("    /* " + MARKER + " */ .btn-rakuten-s { background: linear-gradient(135deg, #c81d1d, #8f0000); color: #fff; "
       "box-shadow: 0 3px 10px rgba(200,29,29,0.3); }{nl}")


def box(nl):
    rows = []
    for k in ("century", "dazaifu"):
        rows.append(
            '        <div style="background:#fff;border:1px solid #e3ddcf;border-radius:10px;padding:12px 14px;">' + nl +
            f'          <div style="font-weight:700;color:#1a5c38;font-size:14px;margin-bottom:8px;">{NAME[k]} <a href="course-{k}.html" style="font-weight:400;font-size:12px;color:#1a5fa0;">詳細</a></div>' + nl +
            '          <div style="display:flex;gap:6px;flex-wrap:wrap;">' + nl +
            f'            <a href="{rakuten_url(RAKUTEN[k])}" target="_blank" rel="nofollow sponsored noopener" class="course-btn btn-rakuten-s" style="flex:1;justify-content:center;">楽天GORAで予約</a>' + nl +
            f'            <a href="{jalan_url(JALAN[k])}" target="_blank" rel="nofollow sponsored noopener" class="course-btn btn-jalan-s" style="flex:1;justify-content:center;">じゃらんで予約</a>' + nl +
            '          </div>' + nl +
            '        </div>')
    return (f'    <!-- {MARKER} -->{nl}'
            '    <div style="max-width:880px;margin:0 auto 28px;background:#f4f1ea;border:1px solid #e3ddcf;border-left:5px solid #1a5c38;border-radius:14px;padding:18px 20px;">' + nl +
            '      <div style="font-weight:700;font-size:15px;color:#1a5c38;margin-bottom:6px;">📅 この10コースのうち、ネットで予約できるのは2コース</div>' + nl +
            '      <div style="font-size:13px;color:#5a5a5a;line-height:1.8;margin-bottom:12px;">福岡センチュリーと太宰府は、じゃらん・楽天GORAで予約できます（2026年11月23日確認）。ほかの8コースは、公式サイト・電話での予約か、会員の紹介・同伴が必要です。</div>' + nl +
            '      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:10px;">' + nl +
            nl.join(rows) + nl +
            '      </div>' + nl +
            '    </div>' + nl +
            f'    <!-- /{MARKER} -->{nl}')


res = []
for root in ROOTS:
    p = os.path.join(root, "hub-business.html")
    s = open(p, encoding="utf-8", newline="").read()
    if MARKER in s:
        res.append((root, "already"))
        continue
    nl = "\r\n" if "\r\n" in s else "\n"
    new = s
    assert new.count(CSS_ANCHOR) == 1
    new = new.replace(CSS_ANCHOR, CSS.replace("{nl}", nl) + CSS_ANCHOR)
    i = new.find('id="c-ja"')
    j = new.find('id="c-en"', i)
    ja = new[i:j]
    for k in ("century", "dazaifu"):
        old = f'golf-jalan.net%2Fgc{JALAN[k]}%2F" class="course-btn btn-jalan-s" target="_blank" rel="nofollow sponsored noopener">📅 じゃらん</a>'
        assert ja.count(old) == 1, k
        ja = ja.replace(old, old + nl + f'              <a href="{rakuten_url(RAKUTEN[k])}" class="course-btn btn-rakuten-s" target="_blank" rel="nofollow sponsored noopener">🏌️ 楽天GORA</a>')
    anchor = '    <div class="course-list">'
    assert ja.count(anchor) == 1
    ja = ja.replace(anchor, box(nl) + anchor)
    new = new[:i] + ja + new[j:]
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    assert "\r\r" not in new
    res.append((root, "updated"))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="").write(new)
print(res, "APPLIED" if APPLY else "DRY-RUN")
