#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
予約カードの料金タグで、独自の書き方 (平日昼食付 / 月曜セルフデー / ビジター平日 / メンバー) のまま古い金額が残っていたものを直す。
  じゃらんカード: 最安 ¥{平日総額}〜 / From ¥X / 최저 ¥X부터 (2026-11-20 じゃらん18H最安・税込総額)
  楽天カード: 料金は楽天で確認 (楽天の料金は取っていないので金額を出さない)
  アコーディア公式カード (メンバー価格): 会員料金は公式で確認
冪等。改行コードはそのまま。Usage: python scripts/fix_booking_tags_b_2026_11.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
WK = {"pheasant": 6490, "takaha": 7890, "fukuokakokusai": 9500, "ukiha": 7500}
TAG = re.compile(r'(<div class="booking-logo">)([^<]*)(</div>.*?<div class="booking-price-tag">)(.*?)(</div>)', re.S)
OLD = re.compile(r"平日昼食付|Weekday w/ lunch|평일 점심 포함|月曜セルフデー|Mon Self-Day|월요 셀프데이|ビジター平日|Visitor weekday|비지터 평일|空き状況をチェック|Check availability|メンバー|Member")


def lang_of(tag):
    if re.search(r"[가-힣]", tag): return "ko"
    if re.search(r"[ぁ-んァ-ン一-龥]", tag): return "ja"
    return "en"


for root in ROOTS:
    for slug, wk in WK.items():
        f = f"course-{slug}.html"
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        n = 0

        def fix(m):
            global n
            logo, tag = m.group(2), m.group(4)
            if not OLD.search(tag):
                return m.group(0)
            lg = lang_of(tag)
            if "JALAN" in logo:
                new = {"ja": f'最安 <span class="big">¥{wk:,}</span>〜', "en": f'From <span class="big">¥{wk:,}</span>',
                       "ko": f'최저 <span class="big">¥{wk:,}</span>부터'}[lg]
            elif "RAKUTEN" in logo:
                new = {"ja": '料金は <span class="big">楽天で確認</span>', "en": 'Rates <span class="big">on Rakuten</span>',
                       "ko": '요금은 <span class="big">라쿠텐에서 확인</span>'}[lg]
            elif "ACCORDIA" in logo:
                new = {"ja": '会員料金は <span class="big">公式で確認</span>', "en": 'Member rates <span class="big">on official site</span>',
                       "ko": '회원 요금은 <span class="big">공식에서 확인</span>'}[lg]
            else:
                return m.group(0)
            n += 1
            return m.group(1) + logo + m.group(3) + new + m.group(5)

        new = TAG.sub(fix, s)
        left = [t for t in re.findall(r'booking-price-tag">(.*?)</div>', new) if OLD.search(t)]
        print(f"{root[-10:]} {f}: {n}{' (変更なし)' if new == s else ''} 残り {left}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
