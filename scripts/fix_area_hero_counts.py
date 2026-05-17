#!/usr/bin/env python3
"""fix_area_hero_counts.py — エリアハブ 4 ページの hero / stats-bar のコース数を実数に修正。

course-card 追加スクリプト (add_area_cards*.py) は course-list の h2/eyebrow/JSON-LD のみ
更新し、ページ上部の hero-title・hero-badge・stats-bar の数値を取りこぼしていた。
ミスチェック (inbound-strategist) で発覚。実数: itoshima 6 / kitakyushu 15 / chikugo 11 / chikuho 10。
contextual 文字列のみ置換。両ディレクトリ。一度のみ実行。

Usage: python scripts/fix_area_hero_counts.py [--dry-run]
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv

PAGES = {
"area-itoshima.html": [  # 4 → 6
    ("ゴルフ場4コース", "ゴルフ場6コース"),
    ("厳選4コース", "厳選6コース"),
    ('>4<span class="unit">コース', '>6<span class="unit">コース'),
    ("全4コース", "全6コース"),
    ("4 Golf Courses in", "6 Golf Courses in"),
    ("4 curated courses", "6 curated courses"),
    ('>4<span class="unit">courses', '>6<span class="unit">courses'),
    ("All 4 courses", "All 6 courses"),
    ("골프장 4개 코스", "골프장 6개 코스"),
    ("엄선 4개 코스", "엄선 6개 코스"),
    ('>4<span class="unit">코스', '>6<span class="unit">코스'),
    ("전 4개 코스", "전 6개 코스"),
],
"area-kitakyushu.html": [  # 10 → 15
    ("ゴルフ場10コース", "ゴルフ場15コース"),
    ("厳選10コース", "厳選15コース"),
    ('>10<span class="unit">コース', '>15<span class="unit">コース'),
    ("10 Golf Courses in", "15 Golf Courses in"),
    ("10 curated courses", "15 curated courses"),
    ('>10<span class="unit">courses', '>15<span class="unit">courses'),
    ("골프장 10개 코스", "골프장 15개 코스"),
    ("엄선 10개 코스", "엄선 15개 코스"),
    ('>10<span class="unit">코스', '>15<span class="unit">코스'),
],
"area-chikugo.html": [  # 7/6 → 11
    ("ゴルフ場7コース", "ゴルフ場11コース"),
    ("厳選7コース", "厳選11コース"),
    ('>7<span class="unit">コース', '>11<span class="unit">コース'),
    ("6 Golf Courses in", "11 Golf Courses in"),
    ("6 curated courses", "11 curated courses"),
    ('>7<span class="unit">courses', '>11<span class="unit">courses'),
    ("골프장 6개 코스", "골프장 11개 코스"),
    ("엄선 6개 코스", "엄선 11개 코스"),
    ('>7<span class="unit">코스', '>11<span class="unit">코스'),
],
"area-chikuho.html": [  # 6/4 → 10
    ("厳選6コース", "厳選10コース"),
    ('>6<span class="unit">コース', '>10<span class="unit">コース'),
    ("4 curated courses", "10 curated courses"),
    ('>6<span class="unit">courses', '>10<span class="unit">courses'),
    ("가성비 골프 6코스", "가성비 골프 10코스"),
    ("엄선 4코스", "엄선 10코스"),
    ('>6<span class="unit">코스', '>10<span class="unit">코스'),
],
}

print(f"[fix_area_hero_counts] mode = {'DRY-RUN' if DRY else 'LIVE'}\n")
for fname, pairs in PAGES.items():
    print(f"--- {fname} ---")
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        path = root / fname
        if not path.exists():
            print(f"  {root.name}: NOT FOUND")
            continue
        html = path.read_text(encoding="utf-8")
        total = 0
        for old, new in pairs:
            n = html.count(old)
            if n == 0:
                print(f"  {root.name}: WARN no match: {old[:38]}")
            total += n
            html = html.replace(old, new)
        if not DRY:
            path.write_text(html, encoding="utf-8")
        print(f"  {root.name}: {total} replacements / {'(dry-run)' if DRY else 'written'}")
    print()
print("DONE" if not DRY else "*** DRY-RUN ***")
