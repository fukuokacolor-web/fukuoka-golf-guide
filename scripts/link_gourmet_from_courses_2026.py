#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ランチページ (gourmet-fukuoka-golf.html) へのリンクを、載せた6コースの日本語セクションに1行ずつ入れる。
  位置: 日本語セクションの SNS 評判欄の直後 (<!-- /course-voices-v1 --> の後・「— Getting Here」の前)。
  文言は公式メニューで確認した料理名だけ (2026-11-28)。浮羽は公式で確認できていないので料理名を出さない。
冪等 (MARKER)・改行コードはファイルに合わせる・両ディレクトリ。
Usage: python scripts/link_gourmet_from_courses_2026.py [--apply]
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARKER = "<!-- gourmet-link-v1 -->"
ANCHOR = "<!-- /course-voices-v1 -->"
TEXT = {
    "shimaseaside": "天然鯛茶漬け・海鮮皿うどん",
    "ogori": "和牛とろろ丼",
    "wakamiya": "ハンバーグ定食",
    "genkai": "鯛茶漬け膳",
    "keya": "鯛茶漬",
    "ukiha": None,
}

for slug, dish in TEXT.items():
    lead = f"このコースのランチ（{dish}）を、ほかのコースと並べて公式メニューで紹介しています。" if dish else "SNSに上がった、このコースの料理の写真を紹介しています。"
    for root in ROOTS:
        p = os.path.join(root, f"course-{slug}.html")
        b = open(p, "rb").read().decode("utf-8")
        nl = "\r\n" if "\r\n" in b else "\n"
        if MARKER in b:
            print(root[-6:], slug, "already"); continue
        i = b.find('<div id="c-ja"'); j = b.find('<div id="c-en"')
        k = b.find(ANCHOR, i)
        if k < 0 or (j > 0 and k > j):
            print(root[-6:], slug, "no_match"); continue
        k += len(ANCHOR)
        block = (nl + f'  {MARKER}<div style="max-width:1100px;margin:0 auto;padding:0 20px 8px;">'
                 f'<a href="gourmet-fukuoka-golf.html#{slug}" style="display:block;background:#fff;border:1px solid var(--line);border-radius:12px;padding:12px 16px;font-size:14px;line-height:1.7;color:var(--forest-dark);">'
                 f'🍽️ <strong>福岡のゴルフ場ランチ</strong> — {lead} →</a></div>')
        b = b[:k] + block + b[k:]
        print(root[-6:], slug, "insert")
        if APPLY:
            open(p, "wb").write(b.encode("utf-8"))
print("APPLIED" if APPLY else "DRY-RUN")
