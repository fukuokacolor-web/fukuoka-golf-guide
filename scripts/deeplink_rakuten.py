# -*- coding: utf-8 -*-
"""
deeplink_rakuten.py
楽天GORA / じゃらんゴルフのアフィリエイトリンクを各コース個別ページに deep link 化する

対象: course-*.html の単体コースページのみ (Phase 1)
multi-course ファイル (recommend.html, seasonal.html, hub-*.html等) は Phase 2 で別処理

URL構造:
  Before: pc=http://gora.golf.rakuten.co.jp/  (トップページ)
  After:  pc=https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{ID} (コース個別)

a8mat code:
  Before: 4B1D5J+4P34KY+2HOM+7O29U  (バナー素材コード)
  After:  4B1D5J+4P34KY+2HOM+BW8O1  (フリーリンク素材コード)
"""

import sys
import io
import json
import re
import os
import urllib.parse
from pathlib import Path

# UTF-8 強制
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# パス設定
REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
DATA_FILE = PREVIEW_ROOT / "rakuten_gora_mapping.json"

# A8 テンプレート定数
A8_OLD_CODE = "4B1D5J+4P34KY+2HOM+7O29U"  # 旧バナーコード
A8_NEW_CODE = "4B1D5J+4P34KY+2HOM+BW8O1"  # フリーリンクコード
RAKUTEN_TOP_PC_ENC = "http%253A%252F%252Fgora.golf.rakuten.co.jp%252F"
RAKUTEN_TOP_M_ENC = "http%253A%252F%252Fwww.rakuten.co.jp%252F"


def build_course_url_encoded(c_id: str) -> str:
    """コース個別URLを A8 用に二重URLエンコード"""
    raw = f"https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{c_id}"
    # 1段目: URL-encode (%2F等になる)
    enc1 = urllib.parse.quote(raw, safe='')
    # 2段目: もう一回 encode (%252F等になる) - A8 が a8ejpredirect でデコードした後の楽天側で再度デコードされるため
    enc2 = urllib.parse.quote(enc1, safe='')
    return enc2


def replace_rakuten_urls(html: str, c_id: str) -> tuple[str, int]:
    """1ファイル内の全楽天URLを deep link に置換 (count返す)"""
    encoded_url = build_course_url_encoded(c_id)
    count = 0

    # Step 1: a8mat コード差し替え (7O29U → BW8O1) - 2箇所/URL
    new_html, n1 = re.subn(re.escape(A8_OLD_CODE), A8_NEW_CODE, html)

    # Step 2: pc= の URL 差し替え
    new_html, n2 = re.subn(
        re.escape(f"pc%3D{RAKUTEN_TOP_PC_ENC}"),
        f"pc%3D{encoded_url}",
        new_html
    )

    # Step 3: m= の URL 差し替え
    new_html, n3 = re.subn(
        re.escape(f"m%3D{RAKUTEN_TOP_M_ENC}"),
        f"m%3D{encoded_url}",
        new_html
    )

    return new_html, n2  # n2 = 置換した楽天URL数


def remove_rakuten_blocks(html: str) -> tuple[str, int]:
    """除外コース用: 楽天URLを含む <a> タグを物理削除"""
    # <a ...rpx.a8.net...4P34KY...>...</a> パターンをマッチして削除
    pattern = r'<a [^>]*?rpx\.a8\.net[^>]*?4P34KY[^>]*?>.*?</a>\s*'
    new_html, count = re.subn(pattern, '', html, flags=re.DOTALL)
    return new_html, count


def remove_jalan_blocks(html: str) -> tuple[str, int]:
    """じゃらんも合わせて削除 (akane/genkai 用)"""
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
        new_content, count = replace_rakuten_urls(content, course_data["c_id"])
        action = "deeplink"
    else:
        # 除外: Rakuten/Jalan CTA 削除
        new_content, n_rakuten = remove_rakuten_blocks(content)
        new_content, n_jalan = remove_jalan_blocks(new_content)
        count = n_rakuten + n_jalan
        action = f"removed (R:{n_rakuten} J:{n_jalan})"

    if new_content == original:
        return {"file": filepath.name, "status": "no_change", "action": action}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {"file": filepath.name, "status": "ok", "action": action, "count": count}


def main():
    dry_run = "--dry-run" in sys.argv

    # course_data.json 読込
    with open(DATA_FILE, encoding='utf-8') as f:
        data = json.load(f)

    print(f"[deeplink_rakuten] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"[deeplink_rakuten] courses = {len(data['courses'])}")
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
    print("=" * 80)
    print(f"{'file':<35} {'root':<15} {'status':<12} {'action':<25} {'count'}")
    print("=" * 80)
    for r in results:
        print(f"{r.get('file',''):<35} {r.get('root',''):<15} {r.get('status',''):<12} {r.get('action',''):<25} {r.get('count','')}")

    # 集計
    n_ok = sum(1 for r in results if r['status'] == 'ok')
    n_skip = sum(1 for r in results if r['status'] == 'skip_not_found')
    n_nochange = sum(1 for r in results if r['status'] == 'no_change')
    print()
    print(f"[summary] ok={n_ok}  no_change={n_nochange}  skip={n_skip}")
    if dry_run:
        print("\n*** DRY-RUN: no files were modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
