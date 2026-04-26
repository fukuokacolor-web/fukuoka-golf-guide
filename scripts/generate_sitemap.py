#!/usr/bin/env python
"""リポジトリ内の HTML ファイルから sitemap.xml を生成する。
- priority 0.9 の重要ページを HIGH_PRIORITY_PAGES で指定
- 既存 sitemap.xml から lastmod を継承 (新規HTMLは今日付)
"""
import datetime
import re
from pathlib import Path

DOMAIN = "https://fukuoka-golf-guide.com"
OLD_DOMAIN = "https://fukuokacolor-web.github.io/fukuoka-golf-guide"
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# sitemap 非収録: 404 ページとテンプレート/ユーティリティHTML
# ※ canonical/OGP スクリプトとは EXCLUDE_FILES が異なる (意図的)
EXCLUDE_FILES = {"404.html", "seo-meta.html", "menu-multilang.html"}

# v2 新規: 重要ページは priority 0.9 を維持
HIGH_PRIORITY_PAGES = {
    "airport-access-top5.html",
    "area-kitakyushu.html",
    "area-itoshima.html",
    "area-chikugo.html",
    "area-fukuokacity.html",
    "course-kokura.html",
}


def page_url(html_path: Path, root: Path) -> str:
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{rel}"


def load_existing_lastmods(sitemap_path: Path) -> dict:
    """既存 sitemap.xml から URL → lastmod のマップを作る。
    `<url>...</url>` ブロック単位で抽出するため、要素間に他のタグ
    (<priority>, <changefreq> など) が挟まっても正しく動作する。
    """
    if not sitemap_path.exists():
        return {}
    text = sitemap_path.read_text(encoding="utf-8")
    result = {}
    # <url>...</url> ブロックを取り出して、各ブロック内で <loc> と <lastmod> を独立に探す
    for url_block in re.findall(r'<url>(.*?)</url>', text, re.DOTALL):
        loc_match = re.search(r'<loc>([^<]+)</loc>', url_block)
        lastmod_match = re.search(r'<lastmod>([^<]+)</lastmod>', url_block)
        if loc_match and lastmod_match:
            # 旧ドメイン → 新ドメインへ正規化
            normalized = loc_match.group(1).replace(OLD_DOMAIN, DOMAIN)
            result[normalized] = lastmod_match.group(1)
    return result


def main():
    root = Path(".").resolve()
    today = datetime.date.today().isoformat()
    sitemap_path = Path("sitemap.xml")
    existing_lastmods = load_existing_lastmods(sitemap_path)

    urls = []
    for html in sorted(root.rglob("*.html")):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue
        if html.name in EXCLUDE_FILES:
            continue
        urls.append((page_url(html, root), html.name))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, fname in urls:
        # priority: top=1.0, 重要ページ=0.9, 通常=0.7
        if url == f"{DOMAIN}/":
            priority = "1.0"
        elif fname in HIGH_PRIORITY_PAGES:
            priority = "0.9"
        else:
            priority = "0.7"

        # lastmod: 既存値を継承、なければ今日付
        lastmod = existing_lastmods.get(url, today)

        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>weekly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    Path("sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated sitemap.xml with {len(urls)} URLs")
    print(f"  - High priority (0.9): {sum(1 for _, n in urls if n in HIGH_PRIORITY_PAGES)}")
    print(f"  - Top (1.0): 1")
    print(f"  - Lastmod inherited: {sum(1 for u, _ in urls if u in existing_lastmods)}")
    print(f"  - Lastmod new (today): {sum(1 for u, _ in urls if u not in existing_lastmods)}")


if __name__ == "__main__":
    main()
