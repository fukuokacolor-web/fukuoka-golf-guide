# -*- coding: utf-8 -*-
"""
deeplink_jalan.py
じゃらんゴルフのアフィリエイトリンクを各コース個別ページに deep link 化する

対象: course-*.html の単体コースページのみ (Phase 1)
multi-course ファイル (recommend.html, hub-*/area-*等) は deeplink_multi_course_jalan.py で別処理

URL構造:
  Before: a8ejpredirect=https%3A%2F%2Fgolf.jalan.net%2F  (トップページ)
  After:  a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{ID}%2F (コース個別)

a8mat code: 4B1D5J+5JG8FM+36SI+BW8O2 (フリーリンクコード・変更なし)
"""

import sys
import io
import json
import re
import urllib.parse
from pathlib import Path

# UTF-8 強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# パス設定
REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
DATA_FILE = PREVIEW_ROOT / "jalan_golf_mapping.json"

# A8 テンプレート定数
A8_CODE = "4B1D5J+5JG8FM+36SI+BW8O2"  # じゃらんゴルフ フリーリンクコード
JALAN_TOP_ENC = "https%3A%2F%2Fgolf.jalan.net%2F"


def build_course_url_encoded(jalan_id: str) -> str:
    """コース個別URLを A8 a8ejpredirect 用に URLエンコード (single-encode)"""
    raw = f"https://golf-jalan.net/gc{jalan_id}/"
    return urllib.parse.quote(raw, safe='')


def replace_jalan_urls(html: str, jalan_id: str) -> tuple[str, int]:
    """1ファイル内の全じゃらんトップURLを deep link に置換"""
    encoded_url = build_course_url_encoded(jalan_id)
    new_html, count = re.subn(
        re.escape(f"a8ejpredirect={JALAN_TOP_ENC}"),
        f"a8ejpredirect={encoded_url}",
        html
    )
    return new_html, count


def remove_jalan_blocks(html: str) -> tuple[str, int]:
    """除外コース用: じゃらんURLを含む <a> タグを物理削除"""
    pattern = r'<a [^>]*?px\.a8\.net[^>]*?5JG8FM[^>]*?>.*?</a>\s*'
    new_html, count = re.subn(pattern, '', html, flags=re.DOTALL)
    return new_html, count


def process_file(filepath: Path, course_data: dict, dry_run: bool = False) -> dict:
    """1ファイルを処理して結果を返す"""
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip_not_found"}

    content = filepath.read_text(encoding='utf-8')
    original = content

    if course_data.get("deeplink"):
        # Deep link 化
        new_content, count = replace_jalan_urls(content, course_data["jalan_id"])
        action = "deeplink"
    else:
        # 除外: じゃらん CTA 削除
        new_content, count = remove_jalan_blocks(content)
        action = f"removed ({course_data.get('exclude_reason','?')})"

    if new_content == original:
        return {"file": filepath.name, "status": "no_change", "action": action}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {"file": filepath.name, "status": "ok", "action": action, "count": count}


def main():
    dry_run = "--dry-run" in sys.argv

    with open(DATA_FILE, encoding='utf-8') as f:
        data = json.load(f)

    print(f"[deeplink_jalan] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"[deeplink_jalan] courses = {len(data['courses'])}")
    print()

    results = []
    for course in data['courses']:
        filename = f"{course['file']}.html"
        # 両方のディレクトリで処理 (preview + repo)
        for root in [PREVIEW_ROOT, REPO_ROOT]:
            fp = root / filename
            r = process_file(fp, course, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    # 結果サマリー
    print("=" * 90)
    print(f"{'file':<35} {'root':<15} {'status':<12} {'action':<20} {'count'}")
    print("=" * 90)
    for r in results:
        print(f"{r.get('file',''):<35} {r.get('root',''):<15} {r.get('status',''):<12} {r.get('action',''):<20} {r.get('count','')}")

    # 集計
    n_ok = sum(1 for r in results if r['status'] == 'ok')
    n_skip = sum(1 for r in results if r['status'] == 'skip_not_found')
    n_nochange = sum(1 for r in results if r['status'] == 'no_change')
    total_count = sum(r.get('count', 0) for r in results if isinstance(r.get('count'), int))
    print()
    print(f"[summary] ok={n_ok}  no_change={n_nochange}  skip={n_skip}  total_replacements={total_count}")
    if dry_run:
        print("\n*** DRY-RUN: no files were modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
