#!/usr/bin/env python3
"""build_course_v3.py — テンプレ + course_data からコース HTML を生成 (v3)

v3 改善点 (Phase B Step 1 の手修正地獄 / v2 の残存問題を解決):
- price section: 全 price-amount / price-card-name を fees から出現順で再構築
  (course_data の fees を「正」とし、テンプレの旧料金を完全に上書き)
- related: 全 related-card を course_data の related から言語別に再構築
- エリアハイライト: explore-nav のオレンジを area_primary で切替
- v2 機能 (フィールド置換・deep link・残存チェック・locality) を継承

Usage:
    python scripts/build_course_v3.py <new_slug> <template_slug> [--access]

Example:
    python scripts/build_course_v3.py suonada shimaseaside
"""

import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# エリア内蔵マッピング (Tier 1 Batch 1+2)
AREA_PRIMARY = {
    "shimaseaside": "itoshima", "classic": "kitakyushu",
    "raizan": "itoshima", "newui": "kitakyushu", "suonada": "kitakyushu",
    "satsuki-tenpai": "chikugo", "satsuki-ryuoh": "chikuho", "kaho": "chikuho",
    "chisan-onga": "kitakyushu", "seitanomori": "kitakyushu", "nishinihon": "chikuho",
    "jruchino": "chikuho", "yasukogen": "chikugo", "yamejoyo": "chikugo", "sunlake": "chikugo",
}

ORANGE = ("display:inline-block;padding:9px 16px;background:#e8732a;border:1px solid #c75d1c;"
          "border-radius:20px;font-size:13px;color:#fff;text-decoration:none;font-weight:700;line-height:1.2;")
WHITE = ("display:inline-block;padding:9px 16px;background:#fff;border:1px solid #d5d0c5;"
         "border-radius:20px;font-size:13px;color:#1f3d2b;text-decoration:none;font-weight:600;line-height:1.2;")

if len(sys.argv) < 3:
    print(__doc__)
    sys.exit(1)

new_slug = sys.argv[1]
template_slug = sys.argv[2]
file_prefix = "access" if "--access" in sys.argv else "course"

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")

data = json.loads((REPO_ROOT / "course_data.json").read_text(encoding="utf-8"))
# テンプレは templates/ を優先 (汎用化済テンプレ)、なければ REPO_ROOT の実コース
_tpl = REPO_ROOT / "templates" / f"{file_prefix}-{template_slug}.html"
if not _tpl.exists():
    _tpl = REPO_ROOT / f"{file_prefix}-{template_slug}.html"
template_html = _tpl.read_text(encoding="utf-8")
jalan_map = json.loads((REPO_ROOT / "jalan_golf_mapping.json").read_text(encoding="utf-8"))
rakuten_map = json.loads((REPO_ROOT / "rakuten_gora_mapping.json").read_text(encoding="utf-8"))


def get_id(mapping, slug, key):
    for c in mapping.get("courses", []):
        if c["file"] == f"course-{slug}":
            return c.get(key)
    return None


try:
    new = next(c for c in data if c["slug"] == new_slug)
    old = next(c for c in data if c["slug"] == template_slug)
except StopIteration:
    print(f"ERROR: slug '{new_slug}' or '{template_slug}' not found in course_data.json")
    sys.exit(1)

old_jalan = get_id(jalan_map, template_slug, "jalan_id")
new_jalan = get_id(jalan_map, new_slug, "jalan_id")
old_rakuten = get_id(rakuten_map, template_slug, "c_id")
new_rakuten = get_id(rakuten_map, new_slug, "c_id")

# ── 1. 基本フィールド置換 (v2 継承) ──
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
# airport_min — stats-bar / hero-badge の所要分。素の数字置換は危険なので
# 周辺文字列で context-anchor して安全に置換 (3 言語 hero-badge + JA/EN/KO stats-bar)
_om, _nm = str(old.get("airport_min", "")), str(new.get("airport_min", ""))
if _om and _nm and _om != _nm:
    for _ctx in [f"空港から{_om}分", f"{_om} min from airport", f"공항에서 {_om}분",
                 f'>{_om}<span class="unit">min', f'>{_om}<span class="unit">분']:
        replacements.append((_ctx, _ctx.replace(_om, _nm, 1)))
if old.get("website") and new.get("website"):
    replacements.append((old["website"], new["website"]))
if old.get("course_type_en") and new.get("course_type_en"):
    replacements.append((old["course_type_en"], new["course_type_en"]))
if old_jalan and new_jalan and old_jalan != new_jalan:
    replacements.append((f"gc{old_jalan}", f"gc{new_jalan}"))
if old_rakuten and new_rakuten and str(old_rakuten) != str(new_rakuten):
    replacements.append((str(old_rakuten), str(new_rakuten)))

result = template_html
applied = 0
for o, n in sorted(replacements, key=lambda p: -len(str(p[0]))):
    if o and n and o != n and o in result:
        applied += result.count(o)
        result = result.replace(o, n)


# ── 2. price section 再構築 (price-amount / price-card-name) ──
def amount_html(fee_value):
    # KO 料金の韓国ウォン併記 span『<span ...>(약 …)</span>』を保持
    krw = ""
    _k = re.search(r'<span[^>]*>\(약[^<]*\)</span>', fee_value)
    if _k:
        krw = " " + _k.group()
    # 3 桁以上の数字を価格として抽出。ただし直後が「年」= 年号は価格でないので除外
    nums = [m.group() for m in re.finditer(r"[\d,]{3,}", fee_value)
            if fee_value[m.end():m.end() + 1] != "年"]
    if len(nums) >= 2:
        return f'<span class="yen">¥</span>{nums[0]}<span class="range">〜{nums[1]}</span>{krw}'
    if len(nums) == 1:
        return f'<span class="yen">¥</span>{nums[0]}<span class="range"></span>{krw}'
    return f'<span style="font-size:17px;color:var(--muted);">{fee_value}</span>'


def clean_label(label):
    # 先頭の絵文字を除去
    return re.sub(r"^[^\wぁ-んァ-ヶ一-龠a-zA-Z]+\s*", "", label).strip()


if file_prefix == "course":
    all_fees = (new.get("fees_ja", []) + new.get("fees_en", []) + new.get("fees_ko", []))
    # price-amount を出現順に置換
    amounts = re.findall(r'<div class="price-amount">.*?</div>', result)
    for i, am in enumerate(amounts):
        if i < len(all_fees):
            result = result.replace(am, f'<div class="price-amount">{amount_html(all_fees[i][1])}</div>', 1)
    # price-card-name を出現順に置換
    names = re.findall(r'<div class="price-card-name">.*?</div>', result)
    for i, nm in enumerate(names):
        if i < len(all_fees):
            result = result.replace(nm, f'<div class="price-card-name">{clean_label(all_fees[i][0])}</div>', 1)

    # ── 3. related-cards 再構築 (言語別) ──
    rel = new.get("related", [])
    rel_blocks = re.findall(r'(<div class="related-cards">\s*.*?\s*</div>)', result, re.DOTALL)
    for li, block in enumerate(rel_blocks[:3]):  # JA/EN/KO の順
        cards = []
        for r in rel:
            parts = [p.strip() for p in r["label"].split("/")]
            name = parts[li] if li < len(parts) else parts[0]
            cards.append(f'<a href="{r["href"]}" class="related-card">'
                         f'<span class="related-card-name">{name}</span>'
                         f'<span class="related-card-arrow">→</span></a>')
        new_block = '<div class="related-cards">\n        ' + "\n        ".join(cards) + "\n      </div>"
        result = result.replace(block, new_block, 1)

# ── 4. エリアハイライト切替 ──
area = AREA_PRIMARY.get(new_slug)
old_area = AREA_PRIMARY.get(template_slug)
if area and old_area and area != old_area:
    # テンプレ元エリアを白に
    result = result.replace(f'<a href="area-{old_area}.html" style="{ORANGE}">',
                            f'<a href="area-{old_area}.html" style="{WHITE}">')
    # 新エリアをオレンジに
    result = result.replace(f'<a href="area-{area}.html" style="{WHITE}">',
                            f'<a href="area-{area}.html" style="{ORANGE}">')

# ── 5. 残存チェック ──
residual = []
for key in ["name_ja", "name_en", "name_ko"]:
    v = old.get(key, "")
    if v and v != new.get(key, "") and v in result:
        residual.append(f"旧コース名 [{key}] '{v}' が {result.count(v)} 件残存")
short = old.get("name_ja", "")[:2]
if short and short not in new.get("name_ja", "") and short in result:
    residual.append(f"旧コース名の主要部分 '{short}' が {result.count(short)} 件残存 (要テンプレ汎用化)")
if old_jalan and old_jalan != new_jalan and f"gc{old_jalan}" in result:
    residual.append(f"旧 jalan deep link 'gc{old_jalan}' 残存")
if old_rakuten and str(old_rakuten) != str(new_rakuten) and str(old_rakuten) in result:
    residual.append(f"旧 rakuten c_id '{old_rakuten}' 残存")
if old.get("hero_img") and old["hero_img"] != new.get("hero_img", "") and old["hero_img"] in result:
    residual.append(f"旧 hero_img 残存")
if old.get("locality") and old["locality"] != new.get("locality", "") and old["locality"] in result:
    residual.append(f"旧 locality '{old['locality']}' が {result.count(old['locality'])} 件残存")

# ── 出力 ──
out_filename = f"{file_prefix}-{new_slug}.html"
(REPO_ROOT / out_filename).write_text(result, encoding="utf-8")
(PREVIEW_ROOT / out_filename).write_text(result, encoding="utf-8")

print(f"OK Generated {out_filename} (REPO_ROOT + PREVIEW_ROOT)")
print(f"  Template: {file_prefix}-{template_slug}.html / Area: {old_area} -> {area}")
print(f"  Field replacements: {applied}")
if file_prefix == "course":
    print(f"  Price-amount rebuilt: {len(amounts)} / price-card-name: {len(names)} / related blocks: {len(rel_blocks[:3])}")
print(f"  Output: {len(result):,} chars / {result.count(chr(10)):,} lines")
print()
if residual:
    print(f"NG 残存チェック: {len(residual)} 件 — 要手動修正 or テンプレ汎用化:")
    for r in residual:
        print(f"  - {r}")
else:
    print("OK 残存チェック合格")
print()
print("注意: hero-sub / sec-desc 等のテンプレ固有説明文は残存チェック対象外。")
print("      テンプレ HTML を事前に汎用化しておくこと。preview で 3 言語目視確認推奨。")
