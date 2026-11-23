#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースページのヒーロー写真の alt を事実どおりにする。
  汎用の風景写真 (sakura-road / spring-forest / golf-mountain / itoshima-* / keya-* / fukuoka-* / island-view / aso-grassland 等) なのに
  alt が「{コース名}のコース風景」になっていた → 「イメージ写真（{コース名}の写真ではありません）」。
  実写真 ({slug}-play-N / IMG_*) と、そのコースの写真と確かめられるものは対象外 (KEEP)。
冪等。改行コードはそのまま。Usage: python scripts/fix_stock_photo_alt_2026_11_23.py [--apply]
"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
STOCK = {"sakura-road", "sakura-river", "spring-forest", "golf-mountain", "itoshima-sea", "itoshima-bay", "itoshimatorii",
         "keya-rocks", "keya-waves", "fukuoka-bay", "fukuoka-overview", "island-view", "aso-grassland", "saitozaki-bridge"}
RX = re.compile(r'(<img class="hero-photo" src="images/([a-z-]+)\.webp" alt=")([^"]*)のコース風景(")')
n = 0
for root in ROOTS:
    for p in sorted(glob.glob(os.path.join(root, "course-*.html"))):
        s = open(p, encoding="utf-8", newline="").read()
        new = RX.sub(lambda m: f"{m.group(1)}イメージ写真（{m.group(3)}の写真ではありません）{m.group(4)}" if m.group(2) in STOCK else m.group(0), s)
        if new != s:
            n += 1
            if APPLY:
                open(p, "w", encoding="utf-8", newline="").write(new)
        elif RX.search(s):
            print("KEEP", os.path.basename(p), RX.search(s).group(2))
print("files", n, "APPLIED" if APPLY else "DRY-RUN")
