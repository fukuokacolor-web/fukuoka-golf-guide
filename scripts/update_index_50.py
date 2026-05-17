#!/usr/bin/env python3
"""update_index_50.py — index.html のコース数表記を 35 → 50 に更新。

Tier 1 Batch 1+2 で 35 → 50 コースになったが index.html が 35 のまま。
総数 "35" 系・エリアカード件数・エリアガイド記事の件数を実数に修正 (JA/EN/KO)。
contextual な文字列のみ置換 (CSS の "135deg"・"#143528" 等の "35" は不可侵)。
両ディレクトリ。エリアカード件数は 4→6/6→10/10→15 と値が連鎖するため
降順 (10→15, 7→11, 6→10, 4→6) で適用。一度だけ実行 (再実行不可)。

Usage: python scripts/update_index_50.py [--dry-run]
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv

# (old, new) — すべて contextual。bare "35" は CSS を壊すため使わない。
PAIRS = [
    # ── 総コース数 35 → 50 (JA) ──
    ("35コース", "50コース"),
    ("35アクセス", "50アクセス"),
    # ── 総コース数 (EN) ──
    ("35-Course", "50-Course"),
    ("35 Courses", "50 Courses"),
    ("35 courses", "50 courses"),
    ("35 course pages", "50 course pages"),
    ("35 access pages", "50 access pages"),
    ("35 Course Pages", "50 Course Pages"),
    ("35 Access Pages", "50 Access Pages"),
    ("35 options", "50 options"),
    # ── 総コース数 (KO) ──
    ("35개 코스", "50개 코스"),
    ("35개 접근", "50개 접근"),
    # ── hero / coverage の stat 数値 ──
    ("<strong>35</strong>", "<strong>50</strong>"),
    # ── エリアカード件数 (kitakyushu 10→15 / chikugo 7→11 / chikuho 6→10 / itoshima 4→6) ──
    # 値が連鎖する (4→6, 6→10, 10→15) ため必ず降順で適用すること
    ('<div class="area-count">10 courses</div>', '<div class="area-count">15 courses</div>'),
    ('<div class="area-count">7 courses</div>', '<div class="area-count">11 courses</div>'),
    ('<div class="area-count">6 courses</div>', '<div class="area-count">10 courses</div>'),
    ('<div class="area-count">4 courses</div>', '<div class="area-count">6 courses</div>'),
    # ── エリアガイド記事 excerpt の件数 (JA) ──
    ("7コース・国際空港25分圏内", "15コース・国際空港25分圏内"),
    ("4コース・玄界灘の絶景", "6コース・玄界灘の絶景"),
    ("6コース・温泉と観光", "11コース・温泉と観光"),
    ("4コース・平日¥6,000〜のコスパ穴場", "10コース・平日¥6,000〜のコスパ穴場"),
    # ── エリアガイド記事 excerpt (EN) ──
    ("7 courses · 25 min from KKJ", "15 courses · 25 min from KKJ"),
    ("4 ocean-view courses", "6 ocean-view courses"),
    ("6 courses · Golf + onsen", "11 courses · Golf + onsen"),
    ("4 hidden-gem courses", "10 hidden-gem courses"),
    # ── エリアガイド記事 excerpt (KO) ──
    ("7개 코스·국제공항 25분권", "15개 코스·국제공항 25분권"),
    ("4개 코스·겐카이나다 절경", "6개 코스·겐카이나다 절경"),
    ("6개 코스·골프+온천", "11개 코스·골프+온천"),
    ("4개 코스·평일 ¥6,000부터", "10개 코스·평일 ¥6,000부터"),
]

print(f"[update_index_50] mode = {'DRY-RUN' if DRY else 'LIVE'}\n")
for root in [REPO_ROOT, PREVIEW_ROOT]:
    path = root / "index.html"
    if not path.exists():
        print(f"--- {root.name}: index.html NOT FOUND ---\n")
        continue
    html = path.read_text(encoding="utf-8")
    total = 0
    warns = []
    for old, new in PAIRS:
        n = html.count(old)
        if n == 0 and html.count(new) == 0:
            warns.append(f"  WARN no match (old/new both 0): {old[:42]}")
        total += n
        html = html.replace(old, new)
    if not DRY:
        path.write_text(html, encoding="utf-8")
    print(f"--- {root.name} ---")
    print(f"  replacements applied: {total}")
    for w in warns:
        print(w)
    # 残存チェック: bare 35 系のコース数表記が残っていないか
    for chk in ["35コース", "35 courses", "35 Courses", "35개 코스", "<strong>35</strong>"]:
        if chk in html:
            print(f"  NG residual: '{chk}' x{html.count(chk)}")
    print(f"  status: {'(dry-run)' if DRY else 'written'}\n")
print("DONE" if not DRY else "*** DRY-RUN: re-run without --dry-run to apply ***")
