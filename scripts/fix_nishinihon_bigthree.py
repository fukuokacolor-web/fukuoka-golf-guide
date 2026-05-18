#!/usr/bin/env python3
"""fix_nishinihon_bigthree.py — course-nishinihon.html の「世界三大プロゴルファー」→「世界ビッグスリー」。

西日本CC のゲーリー・プレーヤー紹介で JA が「世界三大プロゴルファー」、EN が
"Big Three" と不統一だった (fact-checker 一次 + 独立検証で確認)。
「世界三大プロゴルファー」は事実誤りではない (西日本CC公式の歴史ページが同表現を
使用) が、公式コースガイドページの「世界ビッグスリー」表記 + 当サイト EN との
統一のため JA を「世界ビッグスリー」に揃える。設計者が Gary Player である事実は
5ソースで確定済 (公式x2 / 楽天GORA / 三和 / GolfPass)。
KO「세계 3대 프로골퍼」は正しい韓国語訳のため維持・対象外。
course_data.json はマスタのため対象外 (手動 Edit 済・別途同期)。
両ディレクトリ・冪等 (再実行で 0 件)。

Usage: python scripts/fix_nishinihon_bigthree.py [--dry-run]
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv

OLD = "世界三大プロゴルファー"
NEW = "世界ビッグスリー"
TARGET = "course-nishinihon.html"

print(f"[fix_nishinihon_bigthree] mode = {'DRY-RUN' if DRY else 'LIVE'}  '{OLD}' -> '{NEW}'\n")
grand = 0
for root in [REPO_ROOT, PREVIEW_ROOT]:
    path = root / TARGET
    if not path.exists():
        print(f"  {root.name}: (not present - skip)")
        continue
    text = path.read_text(encoding="utf-8")
    n = text.count(OLD)
    if n:
        text = text.replace(OLD, NEW)
        if not DRY:
            path.write_text(text, encoding="utf-8")
    state = "(dry-run)" if DRY else ("written" if n else "no change")
    print(f"  {root.name}: {n} replacement(s) / {state}")
    grand += n
print(f"\n{'*** DRY-RUN ***' if DRY else 'DONE'} - total {grand} replacement(s)")
