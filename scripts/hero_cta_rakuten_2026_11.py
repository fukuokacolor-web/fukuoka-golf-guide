#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
じゃらん・楽天の両方で予約できる 34 コースの JA ヒーロー予約ボタン (写真の上の「このコースを予約する」) を楽天GORAに。
  背景: じゃらん予約は0成約・実収益は楽天アフィリ (楽天市場Cookie) 主体。ページで最も目立つボタンがじゃらん行きだった。
  行き先が分かるよう文言は「🏌️ 楽天GORAで予約する →」・色は楽天の赤 (固定バーの sc-rakuten と同じ)。
  GA4 は trackAffiliate('rakuten',…,'ja','hero-cta')。じゃらんは直下の予約帯・本文・固定バーに残る。EN/KO は据え置き。
  効果: GA4 click_affiliate の hero-cta 回数 (変更前はじゃらん) と A8 楽天成果を 12月初めに比較。
対象: ftv-cta-rakuten (7beeca1) が入っているページ。冪等。改行コードはそのまま。
Usage: python scripts/hero_cta_rakuten_2026_11.py [--apply] [--only course-x.html]
"""
import glob, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
HERO = re.compile(r'<a href="([^"]+)" class="hero-cta-btn"([^>]*?)trackAffiliate\(\'jalan\',document\.title,\'ja\',\'hero-cta\'\)">📅 このコースを予約する →</a>')

res = {}
for root in ROOTS:
    files = [os.path.join(root, ONLY)] if ONLY else sorted(glob.glob(os.path.join(root, "course-*.html")))
    for p in files:
        f = os.path.basename(p)
        s = open(p, encoding="utf-8", newline="").read()
        if "ftv-cta-rakuten" not in s:
            continue
        if "trackAffiliate('rakuten',document.title,'ja','hero-cta')" in s:
            res.setdefault("already", []).append(f); continue
        rak = re.search(r'var RAKUTEN="([^"]+)"', s).group(1)
        jal = re.search(r'var JALAN="([^"]+)"', s).group(1)
        ms = list(HERO.finditer(s))
        if len(ms) != 1 or ms[0].group(1) != jal:
            res.setdefault("no_match", []).append(f); continue
        m = ms[0]
        mid = (m.group(2)
               .replace("background:linear-gradient(135deg,#ff8a3d,#e8744c)", "background:linear-gradient(135deg,#c81d1d,#8f0000)")
               .replace("box-shadow:0 6px 18px rgba(232,116,76,0.45)", "box-shadow:0 6px 18px rgba(200,29,29,0.45)"))
        assert "#c81d1d" in mid and "rgba(200,29,29" in mid, f
        rep = f'<a href="{rak}" class="hero-cta-btn"{mid}trackAffiliate(\'rakuten\',document.title,\'ja\',\'hero-cta\')">🏌️ 楽天GORAで予約する →</a>'
        new = s[:m.start()] + rep + s[m.end():]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        res.setdefault("replaced", []).append(f)
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v[:4])
print("APPLIED" if APPLY else "DRY-RUN")
