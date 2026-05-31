#!/usr/bin/env python3
"""
phase4_internal_links.py
========================
Phase 4 / Day 28 GO 後に実行: hub ページと主要ページに LP への内部リンク CTA を追加する。

操作概要:
  - hub-beginner.html  → book-fukuoka-beginner.html へのリンクバナーを挿入
  - hub-traveler.html  → book-fukuoka-traveler.html + book-fukuoka-onsen.html
  - hub-business.html  → book-fukuoka-business.html
  - fees.html          → book-fukuoka-cheap.html
  - index.html         → book-fukuoka-tomorrow.html

規約:
  - MARKER: <!-- phase4-internal-links-v1 --> (冪等)
  - --dry-run フラグ必須 (観測フェーズ中の誤実行防止)
  - 両ディレクトリ処理 (ROOTS パターン)

使い方:
  python scripts/phase4_internal_links.py --dry-run   # 差分確認
  python scripts/phase4_internal_links.py             # 本番実行
"""

import sys
import os
import argparse
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

REPO_ROOT    = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
ROOTS = [REPO_ROOT, PREVIEW_ROOT]

MARKER = "<!-- phase4-internal-links-v1 -->"

# ---------------------------------------------------------------------------
# CTA HTML スニペット定義
# ---------------------------------------------------------------------------

def cta_banner(page_slug: str, href: str, emoji: str, title: str, sub: str) -> str:
    """ページの </body> 直前に挿入する CTA バナー HTML"""
    return f"""
{MARKER}
<!-- Internal Link CTA: {page_slug} → {href} -->
<div style="background:linear-gradient(135deg,#1a2640,#2c3e5a);padding:28px 24px;text-align:center;color:#fff;margin-top:40px;">
  <p style="font-size:13px;opacity:.8;margin-bottom:8px;">{emoji} 関連ガイド</p>
  <p style="font-family:'Noto Serif JP',Georgia,serif;font-size:18px;font-weight:700;margin-bottom:14px;">{title}</p>
  <p style="font-size:13px;opacity:.85;margin-bottom:18px;max-width:500px;margin-left:auto;margin-right:auto;">{sub}</p>
  <a href="{href}"
     style="display:inline-flex;align-items:center;gap:7px;background:#E8744C;color:#fff;padding:12px 24px;border-radius:999px;font-size:14px;font-weight:700;text-decoration:none;"
     onclick="if(window.gtag)gtag('event','internal_nav_click',{{page:'{page_slug}',lang:'ja',nav_section:'phase4_cta',target_page:'{href.replace('.html','')}'}})"
  >{emoji} {title} →</a>
</div>
"""

# 各ファイルの設定: (source_file, insertion_anchor, cta_html)
TASKS = [
    {
        "file": "hub-beginner.html",
        "anchor": "</body>",
        "cta": cta_banner(
            "hub-beginner",
            "book-fukuoka-beginner.html",
            "🌿",
            "初心者向けゴルフ場 4選を予約する",
            "¥3,500〜・フラット・クラブレンタル対応。じゃらんゴルフ・楽天GORAで今すぐ空き確認。"
        )
    },
    {
        "file": "hub-traveler.html",
        "anchor": "</body>",
        "cta": cta_banner(
            "hub-traveler",
            "book-fukuoka-traveler.html",
            "🌊",
            "観光ゴルフ 5選を予約する",
            "糸島・太宰府・宗像。旅行者に最適なコースをじゃらん・楽天GORAで予約。"
        )
    },
    {
        "file": "hub-business.html",
        "anchor": "</body>",
        "cta": cta_banner(
            "hub-business",
            "book-fukuoka-business.html",
            "🏆",
            "接待ゴルフ 5選を予約する",
            "小倉CC・クラシックGC・芥屋GC。名門・格式コースで大切なゲストをおもてなし。"
        )
    },
    {
        "file": "hub-budget.html",
        "anchor": "</body>",
        "cta": cta_banner(
            "hub-budget",
            "book-fukuoka-cheap.html",
            "💴",
            "平日¥6,000以下 24コース比較表を見る",
            "最安値順に並べた格安コース比較。じゃらんゴルフ deep link 付き。"
        )
    },
]

# ---------------------------------------------------------------------------
# Core logic
# ---------------------------------------------------------------------------

def process_file(root: Path, task: dict, dry_run: bool) -> str:
    filepath = root / task["file"]
    anchor   = task["anchor"]
    cta_html = task["cta"]

    if not filepath.exists():
        return f"  NOT_FOUND: {filepath}"

    content = filepath.read_text(encoding="utf-8")

    if MARKER in content:
        return f"  ALREADY:   {filepath}"

    if anchor not in content:
        return f"  NO_ANCHOR: {filepath} ('{anchor}' not found)"

    new_content = content.replace(anchor, cta_html + anchor, 1)

    if dry_run:
        # Show a small preview of what would be inserted
        lines = cta_html.strip().split("\n")
        preview = "\n    ".join(lines[:4])
        return f"  WOULD_ADD: {filepath}\n    ...{preview}..."
    else:
        filepath.write_text(new_content, encoding="utf-8")
        return f"  APPLIED:   {filepath}"


def main():
    parser = argparse.ArgumentParser(description="Phase 4 内部リンク CTA 追加スクリプト")
    parser.add_argument("--dry-run", action="store_true",
                        help="実際には変更しない (差分確認モード)")
    args = parser.parse_args()

    mode = "[DRY-RUN]" if args.dry_run else "[LIVE]"
    print(f"\n=== phase4_internal_links.py {mode} ===")
    print(f"MARKER: {MARKER}")
    print(f"Tasks:  {len(TASKS)} files × {len(ROOTS)} dirs = {len(TASKS)*len(ROOTS)} operations\n")

    stats = {"would_add": 0, "applied": 0, "already": 0, "no_anchor": 0, "not_found": 0}

    for root in ROOTS:
        print(f"--- {root} ---")
        for task in TASKS:
            result = process_file(root, task, args.dry_run)
            print(result)
            key = result.strip().split(":")[0].strip().lower().replace(" ", "_")
            if "would_add" in key: stats["would_add"] += 1
            elif "applied"  in key: stats["applied"]  += 1
            elif "already"  in key: stats["already"]  += 1
            elif "no_anchor" in key: stats["no_anchor"] += 1
            elif "not_found" in key: stats["not_found"] += 1
        print()

    print("=== Summary ===")
    if args.dry_run:
        print(f"  would_add : {stats['would_add']}")
    else:
        print(f"  applied   : {stats['applied']}")
    print(f"  already   : {stats['already']}")
    print(f"  no_anchor : {stats['no_anchor']}")
    print(f"  not_found : {stats['not_found']}")

    if args.dry_run and stats["would_add"] > 0:
        print(f"\n→ 本番実行: python scripts/phase4_internal_links.py")


if __name__ == "__main__":
    main()
