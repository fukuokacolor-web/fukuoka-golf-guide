#!/usr/bin/env python
"""
全 HTML ファイルに canonical タグを挿入/更新する。
- 既存の canonical があれば新ドメインの値で上書き (1個目のみ)
- 複数 canonical を検出したら警告
- なければ </head> 直前に挿入
- ルート相対パス (/foo.html) から canonical URL を組み立てる
"""
import re
import sys
from pathlib import Path

DOMAIN = "https://fukuoka-golf-guide.com"

# 除外ディレクトリ
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# canonical 不要なテンプレート/ユーティリティHTML
# ※ 404.html は独自に canonical を持つため除外しない (現状維持)
EXCLUDE_FILES = {"seo-meta.html", "menu-multilang.html"}


def build_canonical(html_path: Path, root: Path) -> str:
    """HTML ファイルのパスから canonical URL を作る"""
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    # サブディレクトリ内 index.html (本リポジトリでは該当なしだが念のため)
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
        return f"{DOMAIN}/{rel}"
    return f"{DOMAIN}/{rel}"


def update_html(html_path: Path, root: Path) -> str:
    text = html_path.read_text(encoding="utf-8")
    canonical_url = build_canonical(html_path, root)
    new_tag = f'<link rel="canonical" href="{canonical_url}" />'

    canonical_re = re.compile(
        r'<link[^>]*\brel=["\']canonical["\'][^>]*/?>',
        re.IGNORECASE,
    )

    matches = canonical_re.findall(text)
    if len(matches) > 1:
        print(f"WARNING: {html_path} has {len(matches)} canonical tags (only first will be replaced)")

    if matches:
        new_text = canonical_re.sub(new_tag, text, count=1)
        action = "UPDATED"
    else:
        if "</head>" in text:
            new_text = text.replace("</head>", f"  {new_tag}\n</head>", 1)
            action = "INSERTED"
        else:
            return f"SKIP (no </head>): {html_path}"

    if new_text != text:
        html_path.write_text(new_text, encoding="utf-8")
    return f"{action}: {html_path} -> {canonical_url}"


def iter_html_files(root: Path):
    for path in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        yield path


def main():
    root = Path(".").resolve()
    count = {"UPDATED": 0, "INSERTED": 0, "SKIP": 0}
    for html in iter_html_files(root):
        result = update_html(html, root)
        print(result)
        for k in count:
            if result.startswith(k):
                count[k] += 1
    print()
    print(f"Summary: UPDATED={count['UPDATED']}, INSERTED={count['INSERTED']}, SKIP={count['SKIP']}")


if __name__ == "__main__":
    main()
