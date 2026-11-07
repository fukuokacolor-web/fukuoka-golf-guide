#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLAUDE.md §9.4 の除外コースに残っていた予約導線を外す (2026-11-07 点検)。
  1. book-fukuoka-access.html: 古賀・クイーンズヒル・雷山の楽天GORAボタン
  2. course-kokura.html: 構造化データの楽天 Offer (ビジターは会員紹介後に電話予約)
冪等: 対象が無ければ already と表示して何もしない。改行コードはそのまま保つ。
Usage:
  python scripts/fix_cta_exclusions_2026_11.py            # dry-run
  python scripts/fix_cta_exclusions_2026_11.py --apply    # REPO + PREVIEW
"""
import os, re, sys

ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
BTN = re.compile(
    r'[ \t]*<a href="[^"]*c_id%252F(400018|400021|400043)"[^>]*class="btn-book btn-rakuten"[^>]*>🏌️ 楽天GORA</a>\r?\n'
)
OFFERS = re.compile(r',\r?\n[ \t]*"offers": \[.*?c_id/400019.*?\r?\n[ \t]*\](?=\r?\n[ \t]*\}\r?\n[ \t]*</script>)', re.S)


def fix(root, name, pat, want):
    p = os.path.join(root, name)
    s = open(p, encoding="utf-8", newline="").read()
    new, n = pat.subn("", s)
    if n == 0:
        print(f"  already {name}")
        return
    assert n == want, (name, n, want)
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    print(f"  replaced {name}: {n} 件, {len(s) - len(new)} chars")
    if APPLY:
        open(p, "w", encoding="utf-8", newline="").write(new)


for root in ROOTS:
    print(root)
    fix(root, "book-fukuoka-access.html", BTN, 3)
    fix(root, "course-kokura.html", OFFERS, 1)
print("APPLIED" if APPLY else "DRY-RUN")
