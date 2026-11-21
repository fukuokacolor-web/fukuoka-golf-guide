#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
じゃらん・楽天の両方で予約できるコースの JA ファーストビュー予約帯 (ftv-cta-strip) に楽天GORAボタンを足す。
  背景: 実収益は楽天アフィリ (楽天市場Cookie) 主体・じゃらん予約は0成約。ページ最上部の予約帯がじゃらんだけだった。
  対象: JA の ftv 帯にじゃらんボタンがあり、ページに var RAKUTEN= があるコース。EN/KO は触らない (新規施策は JA 単独の方針)。
  リンクはページ内の var RAKUTEN (A8 経由の楽天アフィリ) をそのまま使う。GA4 は trackAffiliate('rakuten',...,'ja','ftv-cta')。
  JA じゃらんボタンの文言を「じゃらんゴルフで予約 →」に短縮 (2ボタンの長さを揃える)。
  マイクロコピーの「Pontaポイント1%還元」→「Ponta・楽天ポイントが貯まる」(2サイト並びに合わせる)。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/add_ftv_rakuten_btn_2026_11.py [--apply] [--only course-x.html]
"""
import glob, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "ftv-cta-rakuten"
JA_OLD_LABEL = "📅 じゃらんゴルフでこのコースを予約する →"  # 2ボタン並びで長さを揃える
JA_NEW_LABEL = "📅 じゃらんゴルフで予約 →"
JA_TRACK = "trackAffiliate('jalan',document.title,'ja','ftv-cta')\">"
CSS_ANCHOR = re.compile(r"(    \.ftv-cta-btn:hover \{[^}]*\}(\r?\n))")
CSS_ADD = ("    .ftv-cta-btn.ftv-cta-rakuten { background:linear-gradient(135deg,#c81d1d,#8f0000); box-shadow:0 6px 18px rgba(200,29,29,0.3); margin:8px 0 0 6px; }{nl}"
           "    .ftv-cta-btn.ftv-cta-rakuten:hover {{ box-shadow:0 10px 26px rgba(200,29,29,0.4); }}{nl}")

res = {}
for root in ROOTS:
    files = [os.path.join(root, ONLY)] if ONLY else sorted(glob.glob(os.path.join(root, "course-*.html")))
    for p in files:
        f = os.path.basename(p)
        s = open(p, encoding="utf-8", newline="").read()
        if MARKER in s:
            new = s.replace(JA_TRACK + JA_OLD_LABEL, JA_TRACK + JA_NEW_LABEL, 1)
            res.setdefault("already" if new == s else "label", []).append(f)
            if APPLY and new != s:
                open(p, "w", encoding="utf-8", newline="").write(new)
            continue
        m = re.search(r'var RAKUTEN="([^"]+)"', s)
        i = s.find(JA_TRACK)
        if not m or i < 0:
            res.setdefault("skip", []).append(f); continue
        end = s.index("</a>", i) + 4
        rak = m.group(1)
        btn = (f'\n    <a href="{rak}" class="ftv-cta-btn {MARKER}" target="_blank" rel="nofollow sponsored noopener" '
               f"onclick=\"if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','ftv-cta')\">🏌️ 楽天GORAで予約 →</a>")
        nl = "\r\n" if "\r\n" in s else "\n"
        new = s[:end] + btn.replace("\n", nl) + s[end:]
        new = new.replace(JA_TRACK + JA_OLD_LABEL, JA_TRACK + JA_NEW_LABEL, 1)
        new = new.replace("｜ Pontaポイント1%還元 ｜", "｜ Ponta・楽天ポイントが貯まる ｜", 1)
        cm = CSS_ANCHOR.search(new)
        assert cm, f
        css = CSS_ADD.replace("{nl}", nl).replace("{{", "{").replace("}}", "}")
        new = new[:cm.end()] + css + new[cm.end():]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        res.setdefault("added", []).append(f)
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v if k != "added" else v[:3])
print("APPLIED" if APPLY else "DRY-RUN")
