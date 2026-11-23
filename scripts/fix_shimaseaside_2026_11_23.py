#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
志摩シーサイド: 料金欄の説明に「オンラインの空きが少ない → 公式のオンライン予約か電話」を足す (JA)。料金は公式料金表と一致 (2026-11-23 再確認)。
  じゃらん gc02352: リクエスト予約のプラン1件のみ・11/23〜12/31 の空き 0 日 / 楽天 c_id 400024: 空き 2 日 (12/24 キャディ付 ¥24,100)
  公式 simascc.com/price_information/: 3〜12月セルフ 平日¥19,000・土日祝¥25,000 / 1〜2月 ¥16,000・¥21,000 (3〜4名・税込)。公式にオンライン予約あり
冪等。改行コードはそのまま。Usage: python scripts/fix_shimaseaside_2026_11_23.py [--apply]
"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
OLD = "で、2026年10月に確認。キャディ付きや2名プレーは別料金です。最新料金・空き状況は公式サイトでご確認ください。</p>"
NEW = ("で、2026年11月に再確認。キャディ付きや2名プレーは別料金です。"
       "じゃらん・楽天GORAはオンラインの空きが少ない（11月23日に見たところ、12月末まででじゃらん0日・楽天2日）ので、"
       "予約は公式サイトのオンライン予約か電話（092-327-2131）が確実です。</p>")
for root in ROOTS:
    p = os.path.join(root, "course-shimaseaside.html")
    s = open(p, encoding="utf-8", newline="").read()
    if NEW in s:
        print(root[-10:], "already"); continue
    assert s.count(OLD) == 1, "no match"
    new = s.replace(OLD, NEW)
    print(root[-10:], "changed")
    if APPLY:
        open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
