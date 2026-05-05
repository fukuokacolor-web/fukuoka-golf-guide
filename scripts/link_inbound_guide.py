# -*- coding: utf-8 -*-
"""
link_inbound_guide.py
Phase A バナー (Japanese only / 해외 이용자 안내) の "coming soon" placeholder を
新規記事 book-fukuoka-golf-foreigner.html へのリンクに置換する。
"""

import sys, io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")

# 置換ペア (旧文字列 → 新文字列)
REPLACEMENTS = [
    # EN banner
    (
        "Detailed inbound booking guide coming soon.",
        'See our <a href="book-fukuoka-golf-foreigner.html" style="color:#5a4000;font-weight:700;text-decoration:underline;">step-by-step booking guide for foreigners</a> (English &amp; Korean).'
    ),
    # KO banner (한국어용)
    (
        "해외 이용자용 예약 가이드 곧 공개 예정.",
        '<a href="book-fukuoka-golf-foreigner.html" style="color:#5a4000;font-weight:700;text-decoration:underline;">외국인용 단계별 예약 가이드</a>를 참고하세요 (영어/한국어 1500단어).'
    ),
]


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    content = filepath.read_text(encoding='utf-8')
    original = content
    counts = []

    for old, new in REPLACEMENTS:
        n = content.count(old)
        if n > 0:
            content = content.replace(old, new)
            counts.append(f"{old[:30]}...x{n}")

    if content == original:
        return {"file": filepath.name, "status": "no_change"}

    if not dry_run:
        filepath.write_text(content, encoding='utf-8')

    return {"file": filepath.name, "status": "ok", "patterns": counts}


def main():
    dry_run = "--dry-run" in sys.argv

    print(f"[link_inbound_guide] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    print()

    # 全 .html ファイルをスキャン
    results = []
    for root in [PREVIEW_ROOT, REPO_ROOT]:
        for fp in sorted(root.glob("*.html")):
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    # 結果出力
    print(f"{'file':<40} {'root':<20} {'status':<12} {'patterns'}")
    print("=" * 110)
    n_ok = 0
    for r in results:
        if r.get('status') == 'ok':
            n_ok += 1
            print(f"{r.get('file',''):<40} {r.get('root',''):<20} {r.get('status',''):<12} {','.join(r.get('patterns', []))}")

    n_total = len(results)
    n_nochange = sum(1 for r in results if r.get('status') == 'no_change')

    print()
    print(f"[summary] ok={n_ok}  no_change={n_nochange}  total_files={n_total}")
    if dry_run:
        print("\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
