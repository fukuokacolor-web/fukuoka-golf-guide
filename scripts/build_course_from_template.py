#!/usr/bin/env python3
"""build_course_from_template.py — 既存テンプレから新規コース HTML を生成

Phase B (Tier 1 追加) 専用・1 回限りの bulk replace スクリプト。
将来は generate_course_v2.py に統合予定 (~/blog-template/ Phase 3.3)。

Usage:
    python scripts/build_course_from_template.py <new_slug> <template_slug>

Example:
    python scripts/build_course_from_template.py shimaseaside keya
    python scripts/build_course_from_template.py classic chikushigaoka

両ディレクトリ (REPO_ROOT + PREVIEW_ROOT) に出力。
"""

import json
import sys
from pathlib import Path

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

new_slug = sys.argv[1]
template_slug = sys.argv[2]
file_prefix = "access" if "--access" in sys.argv else "course"

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")

# course_data.json から両 slug のデータ取得
data = json.loads((REPO_ROOT / "course_data.json").read_text(encoding="utf-8"))
template_html = (REPO_ROOT / f"{file_prefix}-{template_slug}.html").read_text(encoding="utf-8")

try:
    new = next(c for c in data if c["slug"] == new_slug)
    old = next(c for c in data if c["slug"] == template_slug)
except StopIteration:
    print(f"ERROR: slug not found in course_data.json")
    sys.exit(1)

# 置換ペア (長い文字列を先・短い文字列を後)
replacements = [
    # ファイル名参照
    (f"course-{template_slug}.html", f"course-{new_slug}.html"),
    (f"access-{template_slug}.html", f"access-{new_slug}.html"),
    # 名称 (3 言語)
    (old["title_full"], new["title_full"]),
    (old["name_ja"], new["name_ja"]),
    (old["name_en"], new["name_en"]),
    (old["name_ko"], new["name_ko"]),
    # 住所
    (old["phone"], new["phone"]),
    (old["street"], new["street"]),
    # 説明
    (old["desc_ja"], new["desc_ja"]),
    # 画像
    (old["hero_img"], new["hero_img"]),
    # ホール数 (大きな括りで置換)
    (old["holes"], new["holes"]),
    # ロケーション
    (old.get("location_ja", ""), new.get("location_ja", "")),
]

# アクセス (オプショナルフィールド・存在チェック)
for key in ["airport_val_ja", "airport_val_en", "airport_val_ko"]:
    if old.get(key) and new.get(key):
        replacements.append((old[key], new[key]))

# website (任意フィールド)
if "website" in old and "website" in new:
    replacements.append((old["website"], new["website"]))

# course_type_en (任意フィールド)
if old.get("course_type_en") and new.get("course_type_en"):
    replacements.append((old["course_type_en"], new["course_type_en"]))

# 料金 (3 言語 × N セット)
for lang in ["ja", "en", "ko"]:
    old_fees = old.get(f"fees_{lang}", [])
    new_fees = new.get(f"fees_{lang}", [])
    for i in range(min(len(old_fees), len(new_fees))):
        old_label, old_value = old_fees[i]
        new_label, new_value = new_fees[i]
        if old_label != new_label:
            replacements.append((old_label, new_label))
        if old_value != new_value:
            replacements.append((old_value, new_value))

# 関連コース (related)
old_related = old.get("related", [])
new_related = new.get("related", [])
for i in range(min(len(old_related), len(new_related))):
    old_href = old_related[i]["href"]
    new_href = new_related[i]["href"]
    old_label = old_related[i]["label"]
    new_label = new_related[i]["label"]
    if old_href != new_href:
        replacements.append((old_href, new_href))
    if old_label != new_label:
        replacements.append((old_label, new_label))

# 置換適用
result = template_html
applied = 0
for old_str, new_str in replacements:
    if old_str and new_str and old_str != new_str:
        count = result.count(old_str)
        if count > 0:
            result = result.replace(old_str, new_str)
            applied += count
            # print(f"  + {count}× replaced: {old_str[:40]}... → {new_str[:40]}...")

# 両ディレクトリ出力
out_filename = f"{file_prefix}-{new_slug}.html"
(REPO_ROOT / out_filename).write_text(result, encoding="utf-8")
(PREVIEW_ROOT / out_filename).write_text(result, encoding="utf-8")

print(f"OK Generated {out_filename} (both REPO_ROOT + PREVIEW_ROOT)")
print(f"  Template: course-{template_slug}.html")
print(f"  Total replacements applied: {applied}")
print(f"  Output size: {len(result):,} chars / {result.count(chr(10)):,} lines")
print()
print(f"Manual review checklist:")
print(f"  [ ] JSON-LD priceRange should be updated (template had old course's value)")
print(f"  [ ] Course-specific text (e.g. '日本のペブルビーチ', '名門') may need addition")
print(f"  [ ] 3-language sections (#JA / #EN / #KO) should all show new content")
