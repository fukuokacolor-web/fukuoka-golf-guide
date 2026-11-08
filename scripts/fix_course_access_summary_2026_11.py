#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースページの「空港から◯分」「最寄IC」を公式の所要時間に揃える (2026-11-08)。
  麻生飯塚 50→45分・最寄 福岡IC / 筑紫ヶ丘 30→40分・野多目ランプ / 久山 25→20分・粕屋ランプ
  伊都 50→35分 (博多駅欄は公式に記載がないため天神北ランプ 20分に) / 福岡CC 最寄 香椎東出口 (時間は公式記載なしで据え置き)
冪等。改行コードはそのまま保つ。
Usage: python scripts/fix_course_access_summary_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv


def mins(a, b):
    # 所要時間の表記だけを置き換える (「1시간 30분」のような飛行時間は対象外)
    return [
        (rf"(?<![\d時시간 ]){a}分", f"{b}分"), (rf"約{a}分", f"約{b}分"), (rf"(?<![\d,]){a} min", f"{b} min"),
        (rf'{a}<span class="unit">(min|분)', rf'{b}<span class="unit">\1'), (rf"약 {a}분", f"약 {b}분"),
        (rf"공항에서 {a}분", f"공항에서 {b}분"), (rf"空港{a}分", f"空港{b}分"),
    ]


def ic(ja, en, ko):
    return [
        (r'(Nearest IC</div><div class="access-value">)[^<]*(</div>)', rf"\g<1>{ja}\2", "JA"),
        (r'(Nearest IC</div><div class="access-value">)[^<]*(</div>)', rf"\g<1>{en}\2", "EN"),
        (r'(최근 IC</div><div class="access-value">)[^<]*(</div>)', rf"\g<1>{ko}\2", "KO"),
    ]


PLAN = {
    "course-asoiizuka.html": (mins(50, 45), ic("福岡IC", "Fukuoka IC", "후쿠오카 IC")),
    "course-chikushigaoka.html": (mins(30, 40), ic("野多目ランプ", "Notame ramp", "노타메 램프")),
    "course-hisayama.html": (mins(25, 20) + [("九州自動車道・福岡都市高速経由でアクセスでき", "福岡都市高速の粕屋ランプ経由でアクセスでき")], ic("粕屋ランプ", "Kasuya ramp", "가스야 램프")),
    "course-ito.html": ([(r'From Hakata Station</div><div class="access-value">車で約50分', 'From Tenjin-kita ramp</div><div class="access-value">車で約20分'),
                         (r'From Hakata Station</div><div class="access-value">~50 min by car', 'From Tenjin-kita ramp</div><div class="access-value">~20 min by car'),
                         (r'하카타역에서</div><div class="access-value">차로 약 50분', '텐진키타 램프에서</div><div class="access-value">차로 약 20분')] + mins(50, 35), []),
    "course-fukuokacc.html": ([], ic("香椎東出口", "Kashii-Higashi exit", "가시이히가시 출구")),
}
for root in ROOTS:
    print(root)
    for name, (rules, ics) in PLAN.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        new = s
        total = 0
        for pat, rep in rules:
            new, k = re.subn(pat, rep, new)
            total += k
        # 最寄IC は言語ブロックごとに置き換える
        for pat, rep, lang in ics:
            tag = {"JA": 'id="c-ja"', "EN": 'id="c-en"', "KO": 'id="c-ko"'}[lang]
            i = new.find(tag)
            j = min([x for x in (new.find('id="c-en"', i + 1), new.find('id="c-ko"', i + 1), len(new)) if x > i])
            blk, k = re.subn(pat, rep, new[i:j], count=1)
            total += k
            new = new[:i] + blk + new[j:]
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {name}: {total} 件 {'(変更なし)' if new == s else ''}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
