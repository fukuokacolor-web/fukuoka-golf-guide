#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Policy C: 旧テンプレ course の hero「💴 最安¥X〜」バッジ + stat「¥X / Lowest Fee」を
新テンプレ同様の「価格を出さない」表記へ統一する (§7: 陳腐化した/実在しない安値の一掃)。

- hero price badge (💴 ¥X〜 / From ¥X / ¥X부터)  → 🌐 日本語・English・한국어 (新テンプレと同一)
- stat 「¥X〜 / Lowest Fee」                      → 2 sites / Compare (価格を除去・英ラベル統一)

冪等: 置換後は元パターンが消えるので再実行は no-op。
除外: jalan_id が null のコース (会員制/未掲載 = fukuokacc/wakamatsu/genkai/aburayama) はスキップ。
新テンプレ course は該当パターンを持たないので自動的に no-op。

Usage:
  python scripts/policyC_hero_price_to_booking.py --dry-run
  python scripts/policyC_hero_price_to_booking.py
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]

DRY = "--dry-run" in sys.argv

HERO_RE = re.compile(r'<span class="hero-badge">💴[^<]*</span>')
HERO_NEW = '<span class="hero-badge">🌐 日本語・English・한국어</span>'

# 価格stat (stat-num が ¥ で始まる) はラベル文言・行数がコースごとに異なる
# (Lowest Fee / 최저 그린피 / ビジター平日最安 / Visitor weekday lowest 等・century は複数行)。
# ∴ ¥始まりの stat-item を全般に捕捉 (\s* で複数行許容) し、ラベルの文字種で言語判定して置換。
STAT_RE = re.compile(
    r'<div class="stat-item">\s*<div class="stat-num">¥[0-9,]+<span class="unit">〜</span></div>\s*'
    r'<div class="stat-label">([^<]*)</div>\s*</div>'
)
STAT_JA = ('<div class="stat-item"><div class="stat-num">2<span class="unit">サイト</span></div>'
           '<div class="stat-label">予約サイト比較</div></div>')
STAT_EN = ('<div class="stat-item"><div class="stat-num">2<span class="unit">sites</span></div>'
           '<div class="stat-label">Compare bookings</div></div>')
STAT_KO = ('<div class="stat-item"><div class="stat-num">2<span class="unit">사이트</span></div>'
           '<div class="stat-label">예약 사이트 비교</div></div>')

def _stat_sub(m):
    label = m.group(1)
    if re.search(r'[가-힣]', label):          # Hangul → KO
        return STAT_KO
    if re.search(r'[぀-ヿ一-鿿]', label):  # かな/漢字 → JA
        return STAT_JA
    return STAT_EN                                     # ASCII → EN

def main():
    mapping = json.load(open(os.path.join(REPO_ROOT, "jalan_golf_mapping.json"), encoding="utf-8"))
    targets = [c["file"] for c in mapping["courses"] if c.get("jalan_id")]
    excluded = [c["file"] for c in mapping["courses"] if not c.get("jalan_id")]

    summary = {"changed": 0, "no_match": 0, "not_found": 0, "hero_total": 0, "stat_total": 0}
    print(f"対象 {len(targets)} コース / 除外(jalan_id null) {len(excluded)}: {', '.join(excluded)}")
    print(f"モード: {'DRY-RUN (書き込みなし)' if DRY else '本番 (両ディレクトリ書き込み)'}\n")

    for f in targets:
        # REPO をソースに判定 (両 ROOT へ同内容を書く前提)
        src = os.path.join(REPO_ROOT, f + ".html")
        if not os.path.exists(src):
            summary["not_found"] += 1
            print(f"  [not_found] {f}")
            continue
        html = open(src, encoding="utf-8").read()
        n_hero = len(HERO_RE.findall(html))
        n_stat = len(STAT_RE.findall(html))
        if n_hero == 0 and n_stat == 0:
            summary["no_match"] += 1
            continue  # 新テンプレ等 = no-op (静かにスキップ)
        new_html = STAT_RE.sub(_stat_sub, HERO_RE.sub(HERO_NEW, html))
        summary["changed"] += 1
        summary["hero_total"] += n_hero
        summary["stat_total"] += n_stat
        print(f"  [change] {f:26} hero×{n_hero} stat×{n_stat}")
        if not DRY:
            for root in ROOTS:
                path = os.path.join(root, f + ".html")
                if os.path.exists(path):
                    open(path, "w", encoding="utf-8").write(new_html)

    print(f"\n=== SUMMARY ===")
    print(f"changed:   {summary['changed']} コース (hero計 {summary['hero_total']} / stat計 {summary['stat_total']} 置換)")
    print(f"no_match:  {summary['no_match']} コース (新テンプレ等・該当なし = no-op)")
    print(f"not_found: {summary['not_found']}")
    if DRY:
        print("\n※ DRY-RUN。本番実行は --dry-run を外す。")

if __name__ == "__main__":
    main()
