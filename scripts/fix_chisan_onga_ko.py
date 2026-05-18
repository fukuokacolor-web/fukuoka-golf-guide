#!/usr/bin/env python3
"""fix_chisan_onga_ko.py — chisan-onga の韓国語表記ミス「오우카」→「온가」を修正。

「遠賀 (おんが / Onga)」の韓国語音写が誤って「오우카 (Ouka)」になっていた。
6エージェント ミスチェック (inbound-strategist) で発覚。正しい音写は「온가」。
全箇所が 遠賀 を指すため単純置換で安全 (玄海=겐카이 / 筑紫=치쿠시 は別語・対象外)。
course_data.json はマスタのため本スクリプト対象外 (手動 Edit 済・別途同期)。
両ディレクトリ。冪等 (再実行で 0 件)。

Usage: python scripts/fix_chisan_onga_ko.py [--dry-run]
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv

OLD = "오우카"
NEW = "온가"

TARGETS = [
    "course-chisan-onga.html",
    "access-chisan-onga.html",
    "area-kitakyushu.html",
    "sitemap-guide.html",
    "scripts/add_area_cards.py",
    "data/COURSE_DATA_TIER1_DRAFT.json",
    "data/tier1_batch2_research.md",
]

print(f"[fix_chisan_onga_ko] mode = {'DRY-RUN' if DRY else 'LIVE'}  '{OLD}' -> '{NEW}'\n")
grand = 0
for rel in TARGETS:
    print(f"--- {rel} ---")
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        path = root / rel
        if not path.exists():
            print(f"  {root.name}: (not present - skip)")
            continue
        text = path.read_text(encoding="utf-8")
        n = text.count(OLD)
        if n == 0:
            print(f"  {root.name}: 0 (already clean)")
            continue
        text = text.replace(OLD, NEW)
        if not DRY:
            path.write_text(text, encoding="utf-8")
        grand += n
        print(f"  {root.name}: {n} replacement(s) / {'(dry-run)' if DRY else 'written'}")
    print()
print(f"{'*** DRY-RUN ***' if DRY else 'DONE'} - total {grand} replacement(s)")
