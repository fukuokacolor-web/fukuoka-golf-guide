#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
切れた公式サイトURLの差し替えと、瀬板の森の運営表記の訂正 (2026-11-07 点検)。
  - 北九州CC: kitakyushu-cc.com (DNS 解決不可) → PGM のコースページ
  - 瀬板の森: seitanomorigc.com (工事中 503) → PGM のコースページ
  - 瀬板の森: 「北九州市営」→ PGM 運営のパブリックコース
    根拠: PGM 発表 digitalpr.jp/r/131629, /r/135847。電磁誘導カートは資料が割れるため書かない。
冪等: 置換対象が無ければ already。改行コードはそのまま保つ。
Usage:
  python scripts/fix_official_links_2026_11.py            # dry-run
  python scripts/fix_official_links_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
PGM_K = "https://www.pacificgolf.co.jp/kitakyusyu/"
PGM_S = "https://www.pacificgolf.co.jp/seitanomori/"
EDITS = {
    "course-kitakyushu.html": [
        ("https://www.kitakyushu-cc.com/", PGM_K),
        ('<div class="contact-value">kitakyushu-cc.com</div>', '<div class="contact-value">pacificgolf.co.jp/kitakyusyu/</div>'),
    ],
    "course-seitanomori.html": [
        ("https://www.seitanomorigc.com/", PGM_S),
        ("北九州市営のパブリックコース", "PGM運営のパブリックコース"),
        ('<div class="price-card-name">市営</div>', '<div class="price-card-name">公式</div>'),
        ("北九州市営・ノーキャディ・電磁誘導カート", "PGM運営のパブリックコース"),
        ('<div class="price-card-name">Municipal</div>', '<div class="price-card-name">Official</div>'),
        ("Kitakyushu City facility, no-caddy, electromagnetic cart", "Public course operated by PGM"),
        ('<div class="price-card-name">시영</div>', '<div class="price-card-name">공식</div>'),
        ("기타큐슈 시영 시설・캐디 없음・전자유도 카트", "PGM 운영 퍼블릭 코스"),
    ],
}

for root in ROOTS:
    print(root)
    for name, pairs in EDITS.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        new = s
        for a, b in pairs:
            n = new.count(a)
            print(f"  {name}: {n} x {a[:45]}")
            new = new.replace(a, b)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        if new != s and APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
        print(f"  {'already' if new == s else 'replaced'} {name}")
print("APPLIED" if APPLY else "DRY-RUN")
