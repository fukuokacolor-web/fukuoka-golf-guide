#!/usr/bin/env python
"""og:url, og:image, twitter:url, twitter:image を新ドメイン基準で正規化する。
属性順序の両方 (property→content / content→property) に対応。"""
import re
from pathlib import Path
from urllib.parse import urljoin

DOMAIN = "https://fukuoka-golf-guide.com"
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# OGP 不要なテンプレート/ユーティリティHTML
# ※ 404.html は独自の OGP を持つため除外しない
EXCLUDE_FILES = {"seo-meta.html", "menu-multilang.html"}


def page_url(html_path: Path, root: Path) -> str:
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{rel}"


def normalize_image_url(value: str) -> str:
    """og:image を絶対URL に正規化"""
    if value.startswith(("http://", "https://")):
        # 旧ドメインなら新ドメインに (Phase 2 で済んでいるはずだが冪等性確保)
        return value.replace("http://fukuoka-golf-guide.com", DOMAIN) \
                    .replace("https://fukuoka-golf-guide.com", DOMAIN)
    # 相対 URL → 絶対 URL
    return urljoin(DOMAIN + "/", value.lstrip("/"))


def replace_meta_url(text: str, attr_kind: str, attr_name: str, new_value: str) -> str:
    """
    <meta {attr_kind}="{attr_name}" content="..."> または
    <meta content="..." {attr_kind}="{attr_name}"> の content を new_value で置換。
    attr_kind: 'property' (OGP) または 'name' (Twitter)
    """
    # パターンA: attr_kind が先, content が後
    pattern_a = (
        rf'(<meta[^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*\bcontent=["\'])'
        r'([^"\']*)'
        r'(["\'][^>]*/?>)'
    )
    text = re.sub(pattern_a, lambda m: f'{m.group(1)}{new_value}{m.group(3)}', text, flags=re.IGNORECASE)

    # パターンB: content が先, attr_kind が後
    pattern_b = (
        r'(<meta[^>]*\bcontent=["\'])'
        r'([^"\']*)'
        rf'(["\'][^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*/?>)'
    )
    text = re.sub(pattern_b, lambda m: f'{m.group(1)}{new_value}{m.group(3)}', text, flags=re.IGNORECASE)

    return text


def replace_meta_image(text: str, attr_kind: str, attr_name: str) -> str:
    """og:image / twitter:image の値を絶対URL に正規化"""
    pattern_a = (
        rf'(<meta[^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*\bcontent=["\'])'
        r'([^"\']+)'
        r'(["\'][^>]*/?>)'
    )
    text = re.sub(pattern_a, lambda m: f'{m.group(1)}{normalize_image_url(m.group(2))}{m.group(3)}', text, flags=re.IGNORECASE)
    pattern_b = (
        r'(<meta[^>]*\bcontent=["\'])'
        r'([^"\']+)'
        rf'(["\'][^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*/?>)'
    )
    text = re.sub(pattern_b, lambda m: f'{m.group(1)}{normalize_image_url(m.group(2))}{m.group(3)}', text, flags=re.IGNORECASE)
    return text


def update_ogp(html_path: Path, root: Path):
    text = html_path.read_text(encoding="utf-8")
    original = text
    page = page_url(html_path, root)

    # og:url, twitter:url を canonical と同じURLに
    text = replace_meta_url(text, "property", "og:url", page)
    text = replace_meta_url(text, "name", "twitter:url", page)

    # og:image, twitter:image を絶対URLに正規化
    text = replace_meta_image(text, "property", "og:image")
    text = replace_meta_image(text, "name", "twitter:image")

    if text != original:
        html_path.write_text(text, encoding="utf-8")
        print(f"UPDATED: {html_path}")
    else:
        print(f"NOCHANGE: {html_path}")


def main():
    root = Path(".").resolve()
    for html in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue
        if html.name in EXCLUDE_FILES:
            continue
        update_ogp(html, root)


if __name__ == "__main__":
    main()
