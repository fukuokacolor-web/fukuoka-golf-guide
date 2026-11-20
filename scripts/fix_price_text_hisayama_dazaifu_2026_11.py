#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
久山・太宰府の説明文 (meta / og / JSON-LD / FAQ) に残る 2026年7月の料金を、11/20 のじゃらん 18H 最安 (税込総額) に合わせる。
  久山: 平日 ¥9,480〜 / 土日祝 ¥12,980〜   太宰府: 平日 ¥13,500〜 / 土日祝 ¥19,350〜  (scripts/.cache/jalan_floor.json 2026-11-20)
  旧表記の「平日は薄暮9Hなら¥3,564〜」は18ホールではない別プランの値で、今回の基準と合わないため置き換える。
冪等。改行コードはそのまま。Usage: python scripts/fix_price_text_hisayama_dazaifu_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
NOTE = "2026年11月時点・じゃらんの18ホール最安・税込総額"

PLAN = {
    "course-hisayama.html": [
        ("平日は薄暮9Hなら¥3,564〜、土日祝18Hは¥7,655〜（2026年7月じゃらん確認・時期で変動）", f"平日¥9,480〜・土日祝¥12,980〜（{NOTE}・時期で変動）"),
        ("平日薄暮¥3,564〜、土日祝¥7,655〜（2026年7月じゃらん確認・時期で変動）", f"平日¥9,480〜・土日祝¥12,980〜（{NOTE}・時期で変動）"),
        ("平日薄暮¥3,564〜、土日祝¥7,655〜（2026年7月時点）", f"平日¥9,480〜、土日祝¥12,980〜（{NOTE}）"),
        ("平日は薄暮9Hプランなら<strong>¥3,564〜</strong>、土日祝の18Hセルフは<strong>¥7,655〜</strong>が目安です（2026年7月・じゃらんゴルフ確認）。",
         "2026年11月時点のじゃらんゴルフでは、18ホールの最安が平日<strong>¥9,480〜</strong>、土日祝<strong>¥12,980〜</strong>です（税込総額）。"),
        ("平日は薄暮9Hプランなら¥3,564〜、土日祝の18Hセルフは¥7,655〜が目安です（2026年7月・じゃらんゴルフ確認）。",
         "2026年11月時点のじゃらんゴルフでは、18ホールの最安が平日¥9,480〜、土日祝¥12,980〜です（税込総額）。"),
    ],
    "course-dazaifu.html": [
        ("平日は¥9,800台〜、土日祝は¥22,000台〜が目安（2026年7月じゃらん確認・カート付/昼食別・時期で変動）", f"平日¥13,500〜・土日祝¥19,350〜（{NOTE}・時期で変動）"),
        ("平日¥9,800台〜、土日祝¥22,000台〜（2026年7月じゃらん確認・時期で変動）", f"平日¥13,500〜・土日祝¥19,350〜（{NOTE}・時期で変動）"),
        ("平日¥9,800台〜、土日祝¥22,000台〜（2026年7月時点）", f"平日¥13,500〜、土日祝¥19,350〜（{NOTE}）"),
        ("2026年7月時点のじゃらんゴルフでは、平日はカート付・昼食別で¥9,800台〜、土日祝は¥22,000台〜が目安です。",
         "2026年11月時点のじゃらんゴルフでは、18ホールの最安が平日¥13,500〜、土日祝¥19,350〜です（税込総額）。"),
        ("2026年7月時点のじゃらんゴルフでは、平日はカート付・昼食別で<strong>¥9,800台〜</strong>、土日祝は<strong>¥22,000台〜</strong>が目安です。",
         "2026年11月時点のじゃらんゴルフでは、18ホールの最安が平日<strong>¥13,500〜</strong>、土日祝<strong>¥19,350〜</strong>です（税込総額）。"),
        ("じゃらんゴルフ カート付・昼食別の平日最安（2026年7月確認）。", "じゃらんゴルフの平日18ホール最安（2026年11月確認・税込総額）。"),
    ],
}

for root in ROOTS:
    for f, rules in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, n, miss = s, 0, []
        for a, b in rules:
            if a in new:
                new = new.replace(a, b); n += new.count(b)
            elif b not in new:
                miss.append(a[:30])
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        left = re.findall(r"2026年7月[^（）。]{0,12}(?:確認|時点)", new)
        print(f"{root[-12:]} {f}: {n} {'(変更なし)' if new == s else ''} 未一致 {miss} 残り {left}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
