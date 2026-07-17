#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§8是正: 旧テンプレ ftv-cta-microcopy の「Web予約で平均¥3,000お得」(根拠なき節約額) を
新テンプレ同様の「季節により料金変動・最新空き状況をチェック」へ置換 (3言語)。

冪等 (置換後は元文言が消える)。両ROOT書き込み。--dry-run 対応。
新テンプレは既に新文言のため no-op。
"""
import os, sys, glob

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
DRY = "--dry-run" in sys.argv

PAIRS = [
    ("Web予約で平均¥3,000お得", "季節により料金変動・最新空き状況をチェック"),
    ("Save avg. ¥3,000 vs walk-in", "Seasonal pricing — check current rate"),
    ("Web 예약으로 평균 ¥3,000 절약", "시즌별 요금 변동 — 최신 요금 확인"),
]

def main():
    files = sorted(glob.glob(os.path.join(REPO_ROOT, "course-*.html")))
    summary = {"changed": 0, "no_match": 0, "repl": 0}
    print(f"モード: {'DRY-RUN' if DRY else '本番'}\n")
    for src in files:
        name = os.path.basename(src)
        html = open(src, encoding="utf-8").read()
        n = sum(html.count(a) for a, _ in PAIRS)
        if n == 0:
            summary["no_match"] += 1
            continue
        new_html = html
        for a, b in PAIRS:
            new_html = new_html.replace(a, b)
        summary["changed"] += 1
        summary["repl"] += n
        print(f"  [change] {name:28} ×{n}")
        if not DRY:
            for root in ROOTS:
                p = os.path.join(root, name)
                if os.path.exists(p):
                    open(p, "w", encoding="utf-8").write(new_html)
    print(f"\n=== SUMMARY ===\nchanged: {summary['changed']} / repl {summary['repl']} / no_match {summary['no_match']}")
    if DRY: print("※ DRY-RUN。本番は --dry-run を外す。")

if __name__ == "__main__":
    main()
