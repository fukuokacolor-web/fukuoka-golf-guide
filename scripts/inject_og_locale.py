# -*- coding: utf-8 -*-
"""
inject_og_locale.py
全 HTML に <meta property="og:locale" content="ja_JP"> を追加 (OGP 言語明示)。
- og:type の直後に挿入 (慣例的位置)
- 冪等: 'og:locale' が既に存在すれば skip
- 両ディレクトリ (REPO + PREVIEW) を処理

使い方:
    python scripts/inject_og_locale.py --dry-run        # 確認
    python scripts/inject_og_locale.py                   # 適用
"""

import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
LOCALE = "ja_JP"

# og:type タグを検出 (インデント保持のため lookbehind なしで前後 context を取得)
PATTERN = re.compile(
    r'(?P<indent>[ \t]*)(?P<tag><meta\s+property="og:type"\s+content="[^"]*"\s*/?>)',
    re.IGNORECASE,
)


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {'file': filepath.name, 'status': 'not_found'}
    content = filepath.read_text(encoding='utf-8')
    if 'og:locale' in content:
        return {'file': filepath.name, 'status': 'already'}
    m = PATTERN.search(content)
    if not m:
        return {'file': filepath.name, 'status': 'no_og_type'}

    indent = m.group('indent')
    insert_text = f'{m.group("tag")}\n{indent}<meta property="og:locale" content="{LOCALE}">'
    new_content = content[:m.start()] + indent + insert_text + content[m.end():]

    if new_content == content:
        return {'file': filepath.name, 'status': 'noop'}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {'file': filepath.name, 'status': 'inserted', 'indent_chars': len(indent)}


def main():
    dry_run = '--dry-run' in sys.argv
    print(f"[inject_og_locale] mode = {'DRY-RUN' if dry_run else 'LIVE'}\n")

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
            print(f"  inserted: {r['file']:<46} {r['root']:<14} indent={r.get('indent_chars')}")
        elif s == 'no_og_type':
            print(f"  skip: {r['file']:<46} {r['root']:<14} (no og:type)")

    print()
    print(f"[summary] total={len(results)}")
    for s, n in sorted(by_status.items()):
        print(f"          {s}: {n}")
    if dry_run:
        print('\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***')


if __name__ == '__main__':
    main()
