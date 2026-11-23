#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GA4 計測 v2.1 の click_affiliate に「公式サイトへのリンク」を加える (service='official')。
  背景 (2026-11-23 分析): classifyService はアフィリエイト URL しか拾わないため、公式のみのコース
  (クイーンズヒル・芥屋・小倉 など) の予約ボタンを押しても GA4 に何も残らなかった。
  対象: 外部 URL (自サイト以外) で、次のどれか
    - onclick に trackAffiliate('official' がある (既存の公式ボタン)
    - 予約ボタンの class (hero-cta-btn / ftv-cta-btn / btn-book) か、固定バー・予約カード・料金カードの中
    - リンク文に「公式」を含む
  cta_position はそのまま (hero / ftv / sticky / booking_grid / other ...)。
冪等 (MARKER)。G-PENH0Z4VT7 には触れない。改行コードはそのまま。
Usage: python scripts/track_official_links_2026_11.py [--apply] [--only file.html]
"""
import glob, os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "track-official-v1"
OLD = "var service = classifyService(h);"
NEW = (OLD + " /* " + MARKER + " */"
       " if (!service && /^https?:\\/\\//i.test(h) && !/fukuoka-golf-guide\\.com/i.test(h) && ("
       "/trackAffiliate\\('official'/.test(a.getAttribute('onclick') || '') || "
       "/hero-cta-btn|ftv-cta-btn|btn-book/.test(a.className || '') || "
       "a.closest('#sticky-cta, .booking-card, .price-card') || "
       "/公式/.test(a.textContent || ''))) service = 'official';")

res = {}
for root in ROOTS:
    for p in sorted(glob.glob(os.path.join(root, "*.html"))):
        f = os.path.basename(p)
        if ONLY and f != ONLY:
            continue
        s = open(p, encoding="utf-8", newline="").read()
        if MARKER in s:
            res.setdefault("already", []).append(f)
            continue
        n = s.count(OLD)
        if n != 1:
            res.setdefault(f"no_match({n})", []).append(f)
            continue
        new = s.replace(OLD, NEW)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        res.setdefault("replaced", []).append(f)
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v[:6])
print("APPLIED" if APPLY else "DRY-RUN")
