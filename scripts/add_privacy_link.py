#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全 HTML のフッターに privacy.html へのリンクを入れる。フッターのないページは </body> の前に小さなリンクを入れる。
冪等: MARKER があれば何もしない。
Usage:
  python scripts/add_privacy_link.py --dry-run
  python scripts/add_privacy_link.py --only index.html --preview
  python scripts/add_privacy_link.py --apply
"""
import glob, os, re, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
SKIP = {"seo-meta.html", "menu-multilang.html", "privacy.html"}
MARKER = "<!-- privacy-link-v1 -->"
LINK = '<a href="privacy.html">プライバシーポリシー</a>'


def main():
    c = {"footer": 0, "no_footer": 0, "already": 0, "skip": 0, "no_match": 0}
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "*.html"))):
        name = os.path.basename(path)
        if ONLY and name != ONLY:
            continue
        if name in SKIP:
            c["skip"] += 1; continue
        s = open(path, encoding="utf-8", newline="").read()
        if MARKER in s:
            c["already"] += 1; continue
        nl = "\r\n" if "\r\n" in s else "\n"
        i = s.rfind("</footer>")
        if i >= 0:
            new = s[:i] + f'  {MARKER}<div style="margin-top:6px;"><small>{LINK}</small></div>{nl}' + s[i:]
            c["footer"] += 1
        else:
            j = s.rfind("</body>")
            if j < 0:
                c["no_match"] += 1; print("no_match", name); continue
            new = s[:j] + f'{MARKER}<div style="text-align:center;padding:16px;font-size:12px;">{LINK}</div>{nl}' + s[j:]
            c["no_footer"] += 1
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(new)
    print(c, "APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
