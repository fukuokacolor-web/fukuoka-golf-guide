# -*- coding: utf-8 -*-
"""
generate_sitemap_ko.py
韓国人読者向けの sitemap-ko.xml を生成。
- 既存 sitemap.xml から「KO 関連コンテンツの URL」のみを抽出
- 各 URL に hreflang 注記 (xhtml:link) を付与
- Naver Search Advisor / Google Search Console 提出用

含める URL: index / recommend / fees / faq / sitemap-guide / course-* / hub-* / area-* / book-* / airport-access-top5
除外する URL: access-* / 404 / seo-meta / golf-wear / menu-multilang / rental-and-transport / rules-japan / seasonal / travel / contact / beginner-cards

両ディレクトリ (REPO + PREVIEW) に出力。

使い方:
    python scripts/generate_sitemap_ko.py
"""

import sys
import io
import re
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
SITE_BASE = "https://fukuoka-golf-guide.com"

# 含めるパターン (このいずれかに合致する URL を sitemap-ko.xml に含める)
INCLUDE_PATTERNS = [
    re.compile(r'^https://fukuoka-golf-guide\.com/$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/index\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/recommend\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/fees\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/faq\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/sitemap-guide\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/airport-access-top5\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/editorial-policy\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/course-[a-z]+\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/hub-[a-z]+\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/area-[a-z]+\.html$'),
    re.compile(r'^https://fukuoka-golf-guide\.com/book-[a-z-]+\.html$'),
]


def is_target(url: str) -> bool:
    return any(p.match(url) for p in INCLUDE_PATTERNS)


def parse_existing_sitemap(sitemap_path: Path):
    """既存 sitemap.xml から (loc, lastmod, changefreq, priority) を抽出"""
    if not sitemap_path.exists():
        print(f"[ERROR] {sitemap_path} not found")
        return []
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    urls = []
    for url_el in root.findall('sm:url', ns):
        loc = url_el.findtext('sm:loc', namespaces=ns)
        lastmod = url_el.findtext('sm:lastmod', namespaces=ns)
        changefreq = url_el.findtext('sm:changefreq', namespaces=ns)
        priority = url_el.findtext('sm:priority', namespaces=ns)
        urls.append({
            'loc': loc,
            'lastmod': lastmod,
            'changefreq': changefreq or 'weekly',
            'priority': priority or '0.7',
        })
    return urls


def build_sitemap_ko_xml(urls):
    """KO 用 sitemap XML を組み立て (xhtml:link で hreflang 注記)"""
    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append(
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">'
    )
    for u in urls:
        loc = u['loc']
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        # 3 言語の hreflang 注記 (現状は同一 URL 内タブ切替のため fragment ベース)
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ja" href="{loc}"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="en" href="{loc}#en"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="ko" href="{loc}#ko"/>')
        lines.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>')
        if u.get('lastmod'):
            lines.append(f'    <lastmod>{u["lastmod"]}</lastmod>')
        if u.get('changefreq'):
            lines.append(f'    <changefreq>{u["changefreq"]}</changefreq>')
        if u.get('priority'):
            # KO 重要 URL は priority を 0.8 に底上げ
            pri = u['priority']
            try:
                if float(pri) < 0.8:
                    pri = '0.8'
            except ValueError:
                pass
            lines.append(f'    <priority>{pri}</priority>')
        lines.append('  </url>')
    lines.append('</urlset>')
    return '\n'.join(lines) + '\n'


def main():
    src = REPO_ROOT / 'sitemap.xml'
    print(f"[generate_sitemap_ko] reading {src}")
    all_urls = parse_existing_sitemap(src)
    target_urls = [u for u in all_urls if is_target(u['loc'])]
    print(f"  total in sitemap.xml: {len(all_urls)}")
    print(f"  target (KO-relevant): {len(target_urls)}")

    xml_content = build_sitemap_ko_xml(target_urls)

    # 両ディレクトリに書き込み
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        out = root / 'sitemap-ko.xml'
        out.write_text(xml_content, encoding='utf-8')
        print(f"  written: {out}")

    print(f"\n[summary] sitemap-ko.xml generated with {len(target_urls)} URLs")


if __name__ == '__main__':
    main()
