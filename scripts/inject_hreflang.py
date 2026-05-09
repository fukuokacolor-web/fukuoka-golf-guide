# -*- coding: utf-8 -*-
"""
inject_hreflang.py
全 HTML ページの <head> 内に hreflang 4 セット (ja/en/ko/x-default) を追加。
3 言語切替方式 (.content c-ja|c-en|c-ko) のため、各 hreflang は同一 URL を指す
(fragment ベースは Google が無視するという田中・金星指摘を踏まえ、同一 URL 指定に統一)。

冪等: 既に hreflang="ja" + hreflang="ko" 両方存在すれば skip
両ディレクトリ (REPO + PREVIEW) を処理
挿入位置: <link rel="canonical" ...> の直後 (慣例的位置)

使い方:
    python scripts/inject_hreflang.py --dry-run        # 確認
    python scripts/inject_hreflang.py                   # 適用
"""

import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
SITE_BASE = "https://fukuoka-golf-guide.com"

# canonical タグを検出 (インデント保持)
CANONICAL_PATTERN = re.compile(
    r'(?P<indent>[ \t]*)(?P<tag><link\s+rel="canonical"\s+href="(?P<href>[^"]+)"\s*/?>)',
    re.IGNORECASE,
)

# 既存 hreflang 検出 (冪等性確認)
HREFLANG_KO = re.compile(r'<link\s+rel="alternate"\s+hreflang="ko"', re.IGNORECASE)
HREFLANG_JA = re.compile(r'<link\s+rel="alternate"\s+hreflang="ja"', re.IGNORECASE)
HREFLANG_X_DEFAULT = re.compile(r'<link\s+rel="alternate"\s+hreflang="x-default"', re.IGNORECASE)

# 既存の不完全な hreflang (fragment-based or partial) を削除
HREFLANG_ANY = re.compile(
    r'(?:[ \t]*)<link\s+rel="alternate"\s+hreflang="[^"]*"\s+href="[^"]*"\s*/?>\s*\n',
    re.IGNORECASE,
)


def build_hreflang_block(canonical_url: str, indent: str) -> str:
    """4 つの hreflang link を生成 (ja/en/ko/x-default・全て同一 URL)"""
    return (
        f'{indent}<link rel="alternate" hreflang="ja" href="{canonical_url}">\n'
        f'{indent}<link rel="alternate" hreflang="en" href="{canonical_url}">\n'
        f'{indent}<link rel="alternate" hreflang="ko" href="{canonical_url}">\n'
        f'{indent}<link rel="alternate" hreflang="x-default" href="{canonical_url}">'
    )


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {'file': filepath.name, 'status': 'not_found'}

    content = filepath.read_text(encoding='utf-8')

    # 既に完全な 3 言語 + x-default が存在すれば skip
    if HREFLANG_KO.search(content) and HREFLANG_JA.search(content) and HREFLANG_X_DEFAULT.search(content):
        return {'file': filepath.name, 'status': 'already'}

    # canonical タグ検出
    m = CANONICAL_PATTERN.search(content)
    if not m:
        return {'file': filepath.name, 'status': 'no_canonical'}

    canonical_url = m.group('href')
    indent = m.group('indent')

    # 既存の hreflang (fragment-based 等) を全削除
    cleaned = HREFLANG_ANY.sub('', content)

    # 再度 canonical 位置検出 (削除後)
    m2 = CANONICAL_PATTERN.search(cleaned)
    if not m2:
        return {'file': filepath.name, 'status': 'canonical_lost_after_clean'}

    # canonical の直後に新 hreflang block を挿入
    insert_pos = m2.end()
    hreflang_block = build_hreflang_block(canonical_url, indent)
    new_content = cleaned[:insert_pos] + '\n' + hreflang_block + cleaned[insert_pos:]

    if new_content == content:
        return {'file': filepath.name, 'status': 'noop'}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {
        'file': filepath.name,
        'status': 'inserted',
        'canonical': canonical_url[:60] + '...' if len(canonical_url) > 60 else canonical_url,
    }


def main():
    dry_run = '--dry-run' in sys.argv
    print(f"[inject_hreflang] mode = {'DRY-RUN' if dry_run else 'LIVE'}\n")

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob('*.html')):
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    by_status = {}
    for r in results:
        s = r.get('status', '?')
        by_status[s] = by_status.get(s, 0) + 1
        if s == 'inserted':
            print(f"  inserted: {r['file']:<48} {r['root']:<14}")
        elif s in ('no_canonical', 'canonical_lost_after_clean'):
            print(f"  SKIP: {r['file']:<48} {r['root']:<14} ({s})")

    print()
    print(f"[summary] total={len(results)}")
    for s, n in sorted(by_status.items()):
        print(f"          {s}: {n}")
    if dry_run:
        print('\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***')


if __name__ == '__main__':
    main()
