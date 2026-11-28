#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
まとめページ (トップ・ハブ・エリア・空港) の上部に「楽天GORAで福岡のゴルフ場の空きを見る」ボタンを入れる (日本語のみ)。
  背景 (2026-11-28 点検): スマホで最初の予約リンクが hub-business 2,973px・hub-beginner 3,572px・area-fukuokacity 4,330px・
  airport-access-top5 3,467px、トップは予約リンクなし。コースページ (648〜1,383px) に比べて4〜5画面下だった。
  収益の中心は楽天のリンクから入った人の楽天市場での買い物 (A8 楽天アフィリ) なので、楽天のリンクを最初の画面の近くに置く。
  リンク先: 楽天GORA「福岡県 検索結果」 https://gora.golf.rakuten.co.jp/map_search/result/?widthday=7&area_flg=0&area[]=40
            (2026-11-28 にタイトル「福岡県 検索結果｜…【楽天GORA】」を確認)。A8 経由の楽天アフィリエイト。
  位置: ヒーローの次の帯 (数字の帯 / トップは coverage-section) の直後。
冪等 (MARKER)。改行コードはそのまま。G-PENH0Z4VT7 不変。
Usage: python scripts/add_hub_rakuten_cta_2026_11.py [--apply] [--only file.html]
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "hub-rakuten-cta-v1"
PAGES = ["hub-business.html", "index.html", "hub-beginner.html", "area-fukuokacity.html", "airport-access-top5.html"]
U = "https%253A%252F%252Fgora.golf.rakuten.co.jp%252Fmap_search%252Fresult%252F%253Fwidthday%253D7%2526area_flg%253D0%2526area%25255B%25255D%253D40"
URL = ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
       "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + U + "%26m%3D" + U)


def block(nl):
    return (f'  <!-- {MARKER} -->{nl}'
            f'  <div style="max-width:1100px;margin:0 auto;padding:18px 20px 0;">{nl}'
            f'    <a href="{URL}" target="_blank" rel="nofollow sponsored noopener" style="display:block;background:linear-gradient(135deg,#c81d1d,#8f0000);color:#fff;border-radius:14px;padding:14px 18px;text-align:center;text-decoration:none;box-shadow:0 6px 18px rgba(200,29,29,0.25);">{nl}'
            f'      <span style="display:block;font-weight:800;font-size:16px;">🏌️ 楽天GORAで福岡のゴルフ場の空きを見る →</span>{nl}'
            f'      <span style="display:block;font-size:12px;opacity:.9;margin-top:3px;">日付とエリアから、ネットで予約できるコースを探せます</span>{nl}'
            f'    </a>{nl}'
            f'  </div>{nl}'
            f'  <!-- /{MARKER} -->{nl}')


res = {}
for root in ROOTS:
    for f in PAGES:
        if ONLY and f != ONLY:
            continue
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if MARKER in s:
            res.setdefault("already", []).append(f)
            continue
        nl = "\r\n" if "\r\n" in s else "\n"
        i = s.find('id="c-ja"')
        i = i if i > 0 else 0
        h = s.find('<section class="hero"', i)
        e1 = s.find("</section>", h)                      # ヒーローの終わり
        e2 = s.find("</section>", e1 + 10)                # 次の帯の終わり
        assert h > 0 and e1 > 0 and e2 > 0, f
        ls = s.find("\n", e2) + 1
        new = s[:ls] + block(nl) + s[ls:]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7") and "\r\r" not in new
        res.setdefault("added", []).append(f)
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v)
print("APPLIED" if APPLY else "DRY-RUN")
