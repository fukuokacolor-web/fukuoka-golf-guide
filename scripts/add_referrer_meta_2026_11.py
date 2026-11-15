#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全ページの <head> に <meta name="referrer" content="no-referrer-when-downgrade"> を入れる (2026-11-15)。
  目的: 広告リンク (A8) をクリックしたときに、ドメインだけでなく「どのページから来たか」を A8 のコンバージョンリファラに残す。
        ブラウザ既定 (strict-origin-when-cross-origin) では他サイトへ送るリファラがドメインのみになる。
  送るのは当サイトのページ URL のみ (個人情報は含まない)。HTTP への遷移では送らない。
冪等 (同じ meta があれば何もしない)。改行コードはそのまま。
Usage: python scripts/add_referrer_meta_2026_11.py [--apply] [--only a.html b.html]
"""
import glob, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
META = '<meta name="referrer" content="no-referrer-when-downgrade">'

for root in ROOTS:
    files = ONLY or sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "*.html")))
    st = {"added": 0, "already": 0, "no_head": []}
    for f in files:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if 'name="referrer"' in s:
            st["already"] += 1; continue
        nl = "\r\n" if "\r\n" in s else "\n"
        m = re.search(r'<meta charset="[^"]*"\s*/?>', s, re.I)
        if m:
            new = s[:m.end()] + nl + META + s[m.end():]
        elif "</head>" in s:
            new = s.replace("</head>", META + nl + "</head>", 1)
        else:
            st["no_head"].append(f); continue
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        st["added"] += 1
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
    print(root, st)
print("APPLIED" if APPLY else "DRY-RUN")
