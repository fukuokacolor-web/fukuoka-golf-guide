#!/usr/bin/env python
"""リポジトリ内の HTML ファイルから sitemap.xml を生成する。

- priority 0.9 (HIGH): index 直下の主要 area ハブ + course-kokura
- priority 0.8 (MEDIUM): 4 ペルソナハブ + Phase 2 取引KW LP × 3 + 多言語ガイド (2026-05-10 追加)
- priority 1.0 (TOP): index
- priority 0.7 (DEFAULT): 上記以外

lastmod 取得ロジック (2026-05-10 修正):
1. git log から各ファイルの最新コミット日を取得 (主)
2. ファイルが git 管理外なら file mtime
3. それも取れなければ today

両ディレクトリ (REPO_ROOT + PREVIEW_ROOT) を独立して処理する規約。

使い方:
    python scripts/generate_sitemap.py --dry-run        # 内容確認のみ
    python scripts/generate_sitemap.py                  # 両ディレクトリに反映
"""
import argparse
import datetime
import subprocess
import sys
from pathlib import Path

DOMAIN = "https://fukuoka-golf-guide.com"
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
EXCLUDE_FILES = {"404.html", "seo-meta.html", "menu-multilang.html"}

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
ROOTS = [REPO_ROOT, PREVIEW_ROOT]

# priority 0.9 (HIGH): エリアハブ・主要 course・Phase 2 取引KW LP × 3
# Phase 2 LP は当初手動で 0.9 に昇格 (book-fukuoka-cheap/tomorrow/solo) → 規約として明文化 (2026-05-10)
HIGH_PRIORITY_PAGES = {
    "airport-access-top5.html",
    "area-kitakyushu.html",
    "area-itoshima.html",
    "area-chikugo.html",
    "area-fukuokacity.html",
    "area-chikuho.html",
    "course-kokura.html",
    "book-fukuoka-cheap.html",
    "book-fukuoka-tomorrow.html",
    "book-fukuoka-solo.html",
}

# priority 0.8 (MEDIUM): 4 ペルソナハブ + 多言語エバーグリーンガイド (2026-05-10 追加)
MEDIUM_PRIORITY_PAGES = {
    "hub-budget.html",
    "hub-beginner.html",
    "hub-traveler.html",
    "hub-business.html",
    "book-fukuoka-golf-foreigner.html",
}

# priority 0.6 (LOW): 検索順位を狙わない補助・E-E-A-T 透明性ページ
LOW_PRIORITY_PAGES = {
    "editorial-policy.html",
}

# changefreq=monthly: ほぼ更新しない静的コンテンツ (E-E-A-T ポリシー / 多言語エバーグリーンガイド)
# 上記以外は weekly (規約)
MONTHLY_CHANGEFREQ_PAGES = {
    "editorial-policy.html",
    "book-fukuoka-golf-foreigner.html",
}


def page_url(html_path: Path, root: Path) -> str:
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{rel}"


def get_git_lastmods(repo_root: Path) -> dict:
    """git log から {filename: 'YYYY-MM-DD'} のマップを 1 回の git 呼び出しで取得。
    コミットは時系列降順で出力されるため、各ファイル初出のエントリ = 最新コミット日付。
    """
    result = {}
    try:
        out = subprocess.run(
            ["git", "log", "--format=COMMIT %cs", "--name-only"],
            capture_output=True, text=True, cwd=str(repo_root),
            check=True, encoding="utf-8",
        ).stdout
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"  ! git log failed: {e}", file=sys.stderr)
        return result

    current_date = None
    for line in out.split("\n"):
        line = line.rstrip()
        if line.startswith("COMMIT "):
            current_date = line[7:].strip()
        elif line and current_date and line not in result:
            result[line] = current_date  # 初出 = 最新
    return result


def lastmod_for(html_path: Path, root: Path, git_lastmods: dict, today: str) -> str:
    """git → mtime → today の優先順で lastmod を決定。"""
    rel = html_path.relative_to(root).as_posix()
    if rel in git_lastmods:
        return git_lastmods[rel]
    try:
        mtime = html_path.stat().st_mtime
        return datetime.date.fromtimestamp(mtime).isoformat()
    except OSError:
        return today


def priority_for(url: str, fname: str) -> str:
    if url == f"{DOMAIN}/":
        return "1.0"
    if fname in HIGH_PRIORITY_PAGES:
        return "0.9"
    if fname in MEDIUM_PRIORITY_PAGES:
        return "0.8"
    if fname in LOW_PRIORITY_PAGES:
        return "0.6"
    return "0.7"


def changefreq_for(fname: str) -> str:
    if fname in MONTHLY_CHANGEFREQ_PAGES:
        return "monthly"
    return "weekly"


def process_root(root: Path, git_lastmods: dict, today: str, dry_run: bool) -> dict:
    if not root.exists():
        return {"root": root.name, "status": "not_found"}

    urls = []
    for html in sorted(root.rglob("*.html")):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue
        if html.name in EXCLUDE_FILES:
            continue
        urls.append((page_url(html, root), html.name, html))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

    pri_counts = {"1.0": 0, "0.9": 0, "0.8": 0, "0.7": 0, "0.6": 0}
    lastmod_unique = set()
    for url, fname, html in urls:
        priority = priority_for(url, fname)
        pri_counts[priority] += 1
        lastmod = lastmod_for(html, root, git_lastmods, today)
        lastmod_unique.add(lastmod)

        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>{changefreq_for(fname)}</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")
    content = "\n".join(lines) + "\n"

    sitemap_path = root / "sitemap.xml"
    if not dry_run:
        sitemap_path.write_text(content, encoding="utf-8")

    return {
        "root": str(root),
        "status": "ok",
        "url_count": len(urls),
        "priorities": pri_counts,
        "lastmod_unique": sorted(lastmod_unique),
        "wrote": str(sitemap_path) if not dry_run else "(dry-run)",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="出力内容を確認するのみ・ファイル書き込みなし")
    args = parser.parse_args()

    today = datetime.date.today().isoformat()
    git_lastmods = get_git_lastmods(REPO_ROOT)
    print(f"[generate_sitemap] mode = {'DRY-RUN' if args.dry_run else 'LIVE'}")
    print(f"[generate_sitemap] git lastmod entries: {len(git_lastmods)}")
    print()

    for root in ROOTS:
        r = process_root(root, git_lastmods, today, args.dry_run)
        print(f"--- {r.get('root')} ---")
        if r.get("status") != "ok":
            print(f"  status: {r.get('status')}")
            continue
        print(f"  URLs: {r['url_count']}")
        print(f"  priority distribution: 1.0={r['priorities']['1.0']} / 0.9={r['priorities']['0.9']} / 0.8={r['priorities']['0.8']} / 0.7={r['priorities']['0.7']} / 0.6={r['priorities']['0.6']}")
        lm = r["lastmod_unique"]
        print(f"  lastmod range: {lm[0]} 〜 {lm[-1]}  (unique values: {len(lm)})")
        print(f"  wrote: {r['wrote']}")
        print()

    if args.dry_run:
        print("*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***")


if __name__ == "__main__":
    main()
