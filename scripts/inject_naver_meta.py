# -*- coding: utf-8 -*-
"""
inject_naver_meta.py
全 HTML に <meta name="naver-site-verification" content="<ID>" /> を追加。
ユーザーが Naver Search Advisor (https://searchadvisor.naver.com) で取得した
認証 ID を引数で渡す。

挿入位置: <meta charset="UTF-8"> の直後
冪等: 既に naver-site-verification が存在すれば skip (--replace で上書き可)
両ディレクトリ (REPO + PREVIEW) を処理

使い方:
    # ID 受領後の確認 (推奨)
    python scripts/inject_naver_meta.py --id=abc123def456 --dry-run

    # 適用
    python scripts/inject_naver_meta.py --id=abc123def456

    # 既存 meta を新 ID で置換 (再認証時)
    python scripts/inject_naver_meta.py --id=newId --replace

    # Bing 用 (オプション・--name で meta name を変更)
    python scripts/inject_naver_meta.py --id=bingId --name=msvalidate.01
"""

import sys
import io
import re
import argparse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")

# 挿入位置候補: <meta charset="..."> の直後
CHARSET_PATTERN = re.compile(r'(?P<indent>[ \t]*)(?P<tag><meta\s+charset="[^"]+"\s*/?>)', re.IGNORECASE)


def build_existing_pattern(meta_name: str) -> 're.Pattern[str]':
    """既存の <meta name="<META_NAME>" content="..." /> 検出 regex"""
    return re.compile(
        rf'<meta\s+name="{re.escape(meta_name)}"\s+content="[^"]*"\s*/?>',
        re.IGNORECASE,
    )


def process_file(filepath: Path, verify_id: str, meta_name: str, replace: bool, dry_run: bool) -> dict:
    if not filepath.exists():
        return {'file': filepath.name, 'status': 'not_found'}

    content = filepath.read_text(encoding='utf-8')
    new_meta = f'<meta name="{meta_name}" content="{verify_id}" />'
    existing = build_existing_pattern(meta_name)

    if existing.search(content):
        if replace:
            new_content = existing.sub(new_meta, content)
            if new_content == content:
                return {'file': filepath.name, 'status': 'noop'}
            if not dry_run:
                filepath.write_text(new_content, encoding='utf-8')
            return {'file': filepath.name, 'status': 'replaced'}
        return {'file': filepath.name, 'status': 'already'}

    m = CHARSET_PATTERN.search(content)
    if not m:
        return {'file': filepath.name, 'status': 'no_charset'}

    indent = m.group('indent')
    insert_text = f'{m.group("tag")}\n{indent}{new_meta}'
    new_content = content[:m.start()] + indent + insert_text + content[m.end():]

    if new_content == content:
        return {'file': filepath.name, 'status': 'noop'}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')
    return {'file': filepath.name, 'status': 'inserted', 'indent_chars': len(indent)}


def main():
    parser = argparse.ArgumentParser(
        description='Inject Naver/Bing verification meta tag into all HTML files',
    )
    parser.add_argument(
        '--id',
        required=False,
        help='Verification ID (content value). 例: abc123def456',
    )
    parser.add_argument(
        '--name',
        default='naver-site-verification',
        help='meta name 属性 (default: naver-site-verification / Bing は msvalidate.01)',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='変更を適用せず確認のみ',
    )
    parser.add_argument(
        '--replace',
        action='store_true',
        help='既存の同 name meta を新 ID で置換 (再認証時)',
    )
    args = parser.parse_args()

    if not args.id:
        print("[ERROR] --id=<verification-id> を指定してください\n")
        print("  例: python scripts/inject_naver_meta.py --id=abc123def456 --dry-run")
        print("  ID は Naver Search Advisor (https://searchadvisor.naver.com) で取得:")
        print("    1. サイト登録 → HTML タグ認証選択")
        print("    2. 提示される <meta name=\"naver-site-verification\" content=\"...\" />")
        print("    3. content=\"...\" の値だけを --id に渡す\n")
        sys.exit(1)

    # ID 形式検証 (英数字・ハイフン・アンダースコア・等号のみ)
    if not re.fullmatch(r'[a-zA-Z0-9_=\-]+', args.id):
        print(f"[ERROR] 無効な ID 形式: {args.id}")
        print("        英数字・ハイフン・アンダースコア・等号のみ可")
        print("        半角クォートやスペースが含まれている場合は除去してください")
        sys.exit(1)

    print(f"[inject_naver_meta] mode = {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"  meta name: {args.name}")
    print(f"  ID: {args.id[:6]}...{args.id[-4:] if len(args.id) > 10 else ''}  (長さ: {len(args.id)})")
    print(f"  Replace existing: {args.replace}")
    print()

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob('*.html')):
            r = process_file(fp, args.id, args.name, args.replace, args.dry_run)
            r['root'] = root.name
            results.append(r)

    by_status = {}
    for r in results:
        s = r.get('status', '?')
        by_status[s] = by_status.get(s, 0) + 1
        if s in ('inserted', 'replaced', 'no_charset'):
            mark = {'inserted': 'OK', 'replaced': 'UPD', 'no_charset': 'SKIP'}[s]
            indent_info = f"indent={r.get('indent_chars')}" if 'indent_chars' in r else ''
            print(f"  [{mark:<4}] {r['file']:<46} {r['root']:<14} {indent_info}")

    print()
    print(f"[summary] total={len(results)}")
    for s, n in sorted(by_status.items()):
        print(f"          {s}: {n}")

    if args.dry_run:
        print('\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***')
    else:
        print('\n[next] 公開サイトに git push して Naver Search Advisor で「확인」ボタンを押す')


if __name__ == '__main__':
    main()
