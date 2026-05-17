#!/usr/bin/env python3
"""build_course_from_template.py v2 — テンプレ駆動の新規コース HTML 生成 + 残存チェック

v2 改善点 (Phase B Step 1 で 23 件のバグが発生した反省):
- deep link 自動置換: jalan_id / rakuten c_id を mapping から取得して置換
- 料金の数字抽出置換: fees の値から数値を抽出し HTML 内の料金数値を置換
- 残存チェック: 生成後にテンプレ元コースの固有値 (名称/地名/deep link/画像) を検出
- 要手動修正レポート: 生成直後に問題を可視化 (専門家会議を待たずに検出)

Usage:
    python scripts/build_course_from_template.py <new_slug> <template_slug> [--access]

Example:
    python scripts/build_course_from_template.py raizan keya
    python scripts/build_course_from_template.py raizan keya --access

両ディレクトリ (REPO_ROOT + PREVIEW_ROOT) に出力。
"""

import json
import re
import sys
from pathlib import Path

# Windows cp932 対策: stdout を UTF-8 に再設定
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

new_slug = sys.argv[1]
template_slug = sys.argv[2]
file_prefix = "access" if "--access" in sys.argv else "course"

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")

data = json.loads((REPO_ROOT / "course_data.json").read_text(encoding="utf-8"))
template_html = (REPO_ROOT / f"{file_prefix}-{template_slug}.html").read_text(encoding="utf-8")

# mapping ファイル (jalan_id / rakuten c_id)
jalan_map = json.loads((REPO_ROOT / "jalan_golf_mapping.json").read_text(encoding="utf-8"))
rakuten_map = json.loads((REPO_ROOT / "rakuten_gora_mapping.json").read_text(encoding="utf-8"))


def get_jalan_id(slug):
    for c in jalan_map.get("courses", []):
        if c["file"] == f"course-{slug}":
            return c.get("jalan_id")
    return None


def get_rakuten_id(slug):
    for c in rakuten_map.get("courses", []):
        if c["file"] == f"course-{slug}":
            return c.get("c_id")
    return None


try:
    new = next(c for c in data if c["slug"] == new_slug)
    old = next(c for c in data if c["slug"] == template_slug)
except StopIteration:
    print(f"ERROR: slug '{new_slug}' or '{template_slug}' not found in course_data.json")
    sys.exit(1)

old_jalan = get_jalan_id(template_slug)
new_jalan = get_jalan_id(new_slug)
old_rakuten = get_rakuten_id(template_slug)
new_rakuten = get_rakuten_id(new_slug)

# ── 置換ペア構築 ──
replacements = [
    (f"course-{template_slug}.html", f"course-{new_slug}.html"),
    (f"access-{template_slug}.html", f"access-{new_slug}.html"),
    (old["title_full"], new["title_full"]),
    (old["name_ja"], new["name_ja"]),
    (old["name_en"], new["name_en"]),
    (old["name_ko"], new["name_ko"]),
    (old["phone"], new["phone"]),
    (old["street"], new["street"]),
    (old["locality"], new["locality"]),
    (old["desc_ja"], new["desc_ja"]),
    (old["hero_img"], new["hero_img"]),
    (old["holes"], new["holes"]),
    (old.get("location_ja", ""), new.get("location_ja", "")),
]

for key in ["airport_val_ja", "airport_val_en", "airport_val_ko"]:
    if old.get(key) and new.get(key):
        replacements.append((old[key], new[key]))

if "website" in old and "website" in new:
    replacements.append((old["website"], new["website"]))

if old.get("course_type_en") and new.get("course_type_en"):
    replacements.append((old["course_type_en"], new["course_type_en"]))

# deep link (jalan_id / rakuten c_id) — Phase B Step 1 の最大のバグ対策
if old_jalan and new_jalan and old_jalan != new_jalan:
    replacements.append((f"gc{old_jalan}", f"gc{new_jalan}"))
if old_rakuten and new_rakuten and str(old_rakuten) != str(new_rakuten):
    replacements.append((str(old_rakuten), str(new_rakuten)))

# 料金 (fees) — ラベル + 値の文字列置換
for lang in ["ja", "en", "ko"]:
    old_fees = old.get(f"fees_{lang}", [])
    new_fees = new.get(f"fees_{lang}", [])
    for i in range(min(len(old_fees), len(new_fees))):
        if old_fees[i][0] != new_fees[i][0]:
            replacements.append((old_fees[i][0], new_fees[i][0]))
        if old_fees[i][1] != new_fees[i][1]:
            replacements.append((old_fees[i][1], new_fees[i][1]))

# 料金 — 数字抽出置換 (HTML の price-amount 形式 ¥X,XXX に対応)
# Phase B Step 1 では fees の「約19,000円」と HTML の「¥19,000」が不一致で料金が未置換だった
price_warnings = []


def extract_numbers(s):
    return re.findall(r"[\d,]{3,}", s)  # 3 桁以上のカンマ区切り数字


for lang in ["ja", "en", "ko"]:
    old_fees = old.get(f"fees_{lang}", [])
    new_fees = new.get(f"fees_{lang}", [])
    for i in range(min(len(old_fees), len(new_fees))):
        old_nums = extract_numbers(old_fees[i][1])
        new_nums = extract_numbers(new_fees[i][1])
        if old_nums and len(old_nums) == len(new_nums):
            for on, nn in zip(old_nums, new_nums):
                if on != nn:
                    replacements.append((on, nn))
        elif old_nums or new_nums:
            price_warnings.append(
                f"fees_{lang}[{i}]: 数字個数不一致 old={old_nums} new={new_nums} → 料金カードは手動確認が必要"
            )

# related
old_related = old.get("related", [])
new_related = new.get("related", [])
for i in range(min(len(old_related), len(new_related))):
    if old_related[i]["href"] != new_related[i]["href"]:
        replacements.append((old_related[i]["href"], new_related[i]["href"]))
    if old_related[i]["label"] != new_related[i]["label"]:
        replacements.append((old_related[i]["label"], new_related[i]["label"]))

# ── 置換適用 (長い文字列から先に) ──
result = template_html
applied = 0
for old_str, new_str in sorted(replacements, key=lambda p: -len(str(p[0]))):
    if old_str and new_str and old_str != new_str:
        count = result.count(old_str)
        if count > 0:
            result = result.replace(old_str, new_str)
            applied += count

# ── 残存チェック (生成後・Phase B Step 1 の見落とし対策) ──
residual = []
for key in ["name_ja", "name_en", "name_ko"]:
    val = old.get(key, "")
    if val and val != new.get(key, "") and val in result:
        residual.append(f"旧コース名 [{key}] '{val}' が {result.count(val)} 件残存")

old_ja_short = old.get("name_ja", "")[:2]
if old_ja_short and old_ja_short not in new.get("name_ja", "") and old_ja_short in result:
    residual.append(f"旧コース名の主要部分 '{old_ja_short}' が {result.count(old_ja_short)} 件残存 (略称の可能性)")

if old_jalan and old_jalan != new_jalan and f"gc{old_jalan}" in result:
    residual.append(f"旧 jalan deep link 'gc{old_jalan}' が残存 (収益が別コースに流れる)")
if old_rakuten and str(old_rakuten) != str(new_rakuten) and str(old_rakuten) in result:
    residual.append(f"旧 rakuten c_id '{old_rakuten}' が残存 (収益が別コースに流れる)")

old_img = old.get("hero_img", "")
if old_img and old_img != new.get("hero_img", "") and old_img in result:
    residual.append(f"旧 hero_img '{old_img}' が残存")

old_loc = old.get("locality", "")
if old_loc and old_loc != new.get("locality", "") and old_loc in result:
    residual.append(f"旧 locality '{old_loc}' が {result.count(old_loc)} 件残存")

old_st = old.get("street", "")
if old_st and old_st != new.get("street", "") and old_st in result:
    residual.append(f"旧 street '{old_st}' が残存")

# ── 出力 ──
out_filename = f"{file_prefix}-{new_slug}.html"
(REPO_ROOT / out_filename).write_text(result, encoding="utf-8")
(PREVIEW_ROOT / out_filename).write_text(result, encoding="utf-8")

print(f"OK Generated {out_filename} (REPO_ROOT + PREVIEW_ROOT)")
print(f"  Template: {file_prefix}-{template_slug}.html")
print(f"  Replacements applied: {applied}")
print(f"  Output: {len(result):,} chars / {result.count(chr(10)):,} lines")
print()

if price_warnings:
    print("WARN 料金の手動確認が必要:")
    for w in price_warnings:
        print(f"  - {w}")
    print()

if residual:
    print(f"NG 残存チェック: {len(residual)} 件の旧コース文字列が残存 — 要手動修正:")
    for r in residual:
        print(f"  - {r}")
else:
    print("OK 残存チェック合格 (旧コース名/deep link/画像/地名の残存なし)")
print()
print("注意: テンプレ HTML の hardcoded 内容 (季節別料金説明・観光地名・大会実績等) は")
print("      残存チェックで検出しきれない場合あり。preview で 3 言語の目視確認を推奨。")
