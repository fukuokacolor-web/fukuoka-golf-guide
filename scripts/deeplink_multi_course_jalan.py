# -*- coding: utf-8 -*-
"""
deeplink_multi_course_jalan.py
Phase 2: multi-course ファイル (recommend/seasonal/hub-*/fees/airport-access/area-*) の
じゃらんゴルフ アフィリエイトリンクを各コース個別ページに deep link 化する

戦略: 「直前に出現した course-XXX.html リンク」を使って文脈推定し、
該当行のじゃらんトップURL を deep link URL に書き換える。
"""

import sys, io, json, re, urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
DATA_FILE = PREVIEW_ROOT / "jalan_golf_mapping.json"

A8_CODE = "4B1D5J+5JG8FM+36SI+BW8O2"
JALAN_TOP_ENC = "https%3A%2F%2Fgolf.jalan.net%2F"

# 対象ファイル (multi-course)
TARGET_FILES = [
    "recommend.html", "seasonal.html",
    "hub-beginner.html", "hub-budget.html", "hub-business.html", "hub-traveler.html",
    "fees.html", "airport-access-top5.html", "beginner-cards.html",
    "area-chikugo.html", "area-chikuho.html", "area-fukuokacity.html",
    "area-itoshima.html", "area-kitakyushu.html",
    "index.html",
]


def build_encoded_url(jalan_id: str) -> str:
    raw = f"https://golf-jalan.net/gc{jalan_id}/"
    return urllib.parse.quote(raw, safe='')


def process_file(filepath: Path, course_map: dict, dry_run: bool = False) -> dict:
    """1ファイル処理: 直前のcourse-XXX.htmlリンクから所属コース推定して書き換え"""
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    text = filepath.read_text(encoding='utf-8')
    original = text

    lines = text.split('\n')
    current_course = None
    course_link_pat = re.compile(r'href="(course-[a-z0-9]+)\.html')

    n_replaced = 0
    n_excluded_removed = 0
    n_unknown = 0
    n_no_action_excluded = 0  # akane等: 既にCTAなし

    out_lines = []
    for ln in lines:
        m = course_link_pat.search(ln)
        if m:
            current_course = m.group(1)

        if A8_CODE in ln and JALAN_TOP_ENC in ln and current_course:
            cdata = course_map.get(current_course)
            if cdata is None:
                n_unknown += 1
                out_lines.append(ln)
                continue

            if cdata.get("deeplink"):
                enc = build_encoded_url(cdata["jalan_id"])
                ln = ln.replace(f"a8ejpredirect={JALAN_TOP_ENC}", f"a8ejpredirect={enc}")
                n_replaced += 1
            else:
                # 除外コース: じゃらんを含む <a>タグ全体 or div ブロック を削除
                stripped = re.sub(
                    r'<a [^>]*?px\.a8\.net[^>]*?5JG8FM[^>]*?>.*?</a>\s*',
                    '',
                    ln,
                    flags=re.DOTALL
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

    print(f"[deeplink_multi_jalan] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    print(f"[deeplink_multi_jalan] target files = {len(TARGET_FILES)} x 2 dirs")
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
