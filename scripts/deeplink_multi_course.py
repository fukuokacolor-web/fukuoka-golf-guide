# -*- coding: utf-8 -*-
"""
deeplink_multi_course.py
Phase 2: multi-course ファイル (recommend/seasonal/hub-*/fees/airport-access-top5/beginner-cards/area-*) の
楽天GORA/じゃらんゴルフ アフィリエイトリンクを各コース個別ページに deep link 化する

戦略: 「直前に出現した course-XXX.html リンク」を使って文脈推定し、
該当行の楽天URL中の pc=...gora.golf.rakuten.co.jp/  を deep link URL に書き換える
"""

import sys, io, json, re, urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
DATA_FILE = PREVIEW_ROOT / "rakuten_gora_mapping.json"

A8_OLD_CODE = "4B1D5J+4P34KY+2HOM+7O29U"
A8_NEW_CODE = "4B1D5J+4P34KY+2HOM+BW8O1"
RAKUTEN_TOP_PC_ENC = "http%253A%252F%252Fgora.golf.rakuten.co.jp%252F"
RAKUTEN_TOP_M_ENC = "http%253A%252F%252Fwww.rakuten.co.jp%252F"

# 対象ファイル (multi-course)
TARGET_FILES = [
    "recommend.html", "seasonal.html",
    "hub-beginner.html", "hub-budget.html", "hub-business.html", "hub-traveler.html",
    "fees.html", "airport-access-top5.html", "beginner-cards.html",
    "area-chikugo.html", "area-chikuho.html", "area-fukuokacity.html",
    "area-itoshima.html", "area-kitakyushu.html",
    "index.html",  # 念のため
]


def build_encoded_url(c_id: str) -> str:
    raw = f"https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{c_id}"
    enc1 = urllib.parse.quote(raw, safe='')
    enc2 = urllib.parse.quote(enc1, safe='')
    return enc2


def process_file(filepath: Path, course_map: dict, dry_run: bool = False) -> dict:
    """1ファイル処理: 直前のcourse-XXX.htmlリンクから所属コース推定して書き換え"""
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    text = filepath.read_text(encoding='utf-8')
    original = text

    # 各行を走査して、直近に出現した course-XXX.html を track
    lines = text.split('\n')
    current_course = None  # file basename (e.g., "course-keya")
    course_link_pat = re.compile(r'href="(course-[a-z0-9]+)\.html')

    n_replaced = 0
    n_excluded_removed = 0
    n_unknown = 0

    out_lines = []
    for ln in lines:
        # 直近 course link を更新
        m = course_link_pat.search(ln)
        if m:
            current_course = m.group(1)

        # 楽天URLが行にあれば処理
        if A8_OLD_CODE in ln and current_course:
            cdata = course_map.get(current_course)
            if cdata is None:
                n_unknown += 1
                # current_course is unknown → leave as-is
                out_lines.append(ln)
                continue

            if cdata.get("deeplink"):
                # Deep link 化
                enc = build_encoded_url(cdata["c_id"])
                ln = ln.replace(A8_OLD_CODE, A8_NEW_CODE)
                ln = ln.replace(f"pc%3D{RAKUTEN_TOP_PC_ENC}", f"pc%3D{enc}")
                ln = ln.replace(f"m%3D{RAKUTEN_TOP_M_ENC}", f"m%3D{enc}")
                n_replaced += 1
            else:
                # 除外コース: 楽天/じゃらんを含む div 全体を削除
                # 実装: <div ...>...</div> パターンで rpx.a8.net or 5JG8FM を含むものを削除
                # 1行に div 全体が収まっていれば対応可能
                stripped = re.sub(
                    r'<div [^>]*?>.*?(?:rpx\.a8\.net|5JG8FM).*?</div>',
                    '',
                    ln
                )
                if stripped != ln:
                    n_excluded_removed += 1
                    ln = stripped

        out_lines.append(ln)

    new_text = '\n'.join(out_lines)
    if new_text == original:
        return {"file": filepath.name, "status": "no_change"}

    if not dry_run:
        filepath.write_text(new_text, encoding='utf-8')

    return {
        "file": filepath.name, "status": "ok",
        "replaced": n_replaced, "excluded_removed": n_excluded_removed,
        "unknown_context": n_unknown,
    }


def main():
    dry_run = "--dry-run" in sys.argv

    with open(DATA_FILE, encoding='utf-8') as f:
        data = json.load(f)
    course_map = {c['file']: c for c in data['courses']}

    print(f"[deeplink_multi] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"[deeplink_multi] target files = {len(TARGET_FILES)} x 2 dirs")
    print()

    results = []
    for fname in TARGET_FILES:
        for root in [PREVIEW_ROOT, REPO_ROOT]:
            r = process_file(root / fname, course_map, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    print(f"{'file':<35} {'root':<20} {'status':<12} {'replaced':>10} {'excl_rm':>10} {'unknown':>10}")
    print("=" * 110)
    for r in results:
        print(f"{r.get('file',''):<35} {r.get('root',''):<20} {r.get('status',''):<12} {str(r.get('replaced','')):>10} {str(r.get('excluded_removed','')):>10} {str(r.get('unknown_context','')):>10}")

    total_replaced = sum(r.get('replaced', 0) for r in results)
    total_excluded = sum(r.get('excluded_removed', 0) for r in results)
    total_unknown = sum(r.get('unknown_context', 0) for r in results)
    print()
    print(f"[summary] total_replaced={total_replaced}  excluded_removed={total_excluded}  unknown_context={total_unknown}")
    if dry_run:
        print("\n*** DRY-RUN: no changes. ***")


if __name__ == '__main__':
    main()
