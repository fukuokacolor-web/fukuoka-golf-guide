#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
area-kitakyushu.html のページ全体の金額表現を直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日最安 ¥3,500〜」 → じゃらん18H最安 (2026-11-01) の本ページ最安は チサン遠賀 ¥5,869
- FAQ「ムーンレイク鞍手・ミッションバレーが平日¥4,000〜5,000台」 → ムーンレイク ¥6,355・ミッション ¥9,455
  安い順は チサン遠賀 ¥5,869・ムーンレイク ¥6,355・北九州CC ¥6,778
- ミッションバレーの「コスパ」チップ → じゃらん掲載9コース中 高いほうから2番目 → 「バレーコース」に
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_kitakyushu_2026_11.py            # dry-run
  python scripts/fix_kitakyushu_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_kitakyushu_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "area-kitakyushu.html"
STAT = '<div class="stat-num">{}<span class="unit">〜</span></div><div class="stat-label">{}</div>'
CHIP = '<span class="course-chip">{}</span>\r\n            <span class="course-chip">{}</span>'

# (旧, 新, 出現回数)
R = [
    # ---- stats ----
    (STAT.format("¥3,500", "平日最安"), STAT.format("¥5,869", "じゃらん平日最安（11/1）"), 1),
    (STAT.format("¥3,500", "Lowest weekday"), STAT.format("¥5,869", "Lowest weekday on Jalan (Nov 1)"), 1),
    (STAT.format("¥3,500", "평일 최저"), STAT.format("¥5,869", "자란 평일 최저(11/1)"), 1),
    # ---- ミッションバレー チップ ----
    (CHIP.format("コスパ", "鞍手郡小竹町"), CHIP.format("バレーコース", "鞍手郡小竹町"), 1),
    (CHIP.format("Value", "Kotake-machi"), CHIP.format("Valley course", "Kotake-machi"), 1),
    (CHIP.format("가성비", "쿠라테군 코타케쵸"), CHIP.format("밸리 코스", "쿠라테군 코타케쵸"), 1),
    # ---- FAQ コスパ ----
    ('<div class="faq-a">ムーンレイクゴルフクラブ 鞍手コース、ミッションバレーゴルフクラブの2つが平日¥4,000〜5,000台でプレー可能。どちらも鞍手郡で隣接しているため、2日間で両方を回るプランも立てやすいです。</div>',
     '<div class="faq-a">じゃらんの18H最安（2026年11月1日時点）では、チサンカントリークラブ遠賀（平日¥5,869〜）・ムーンレイクゴルフクラブ 鞍手コース（¥6,355〜）・北九州カントリー倶楽部（¥6,778〜）が安い順トップ3です。土日祝は差が大きいので、予定が合えば平日がおすすめです。</div>', 1),
    ('<div class="faq-a">Moon Lake Kurate and Mission Valley offer weekday rounds from ¥4,000–5,000. Both are in adjacent Kurate-gun, making a two-day value trip easy to plan.</div>',
     '<div class="faq-a">On Jalan (lowest 18-hole plans, as of Nov 1, 2026), the three cheapest weekday options are Chisan CC Onga (¥5,869), Moon Lake Kurate (¥6,355) and Kitakyushu CC (¥6,778). Weekend rates are much higher, so play on a weekday if you can.</div>', 1),
    ('<div class="faq-a">문 레이크 GC 쿠라테, 미션 밸리 2곳이 평일 ¥4,000〜5,000대로 플레이 가능. 모두 쿠라테군에서 인접해 2일간 양쪽을 도는 플랜도 세우기 쉽습니다.</div>',
     '<div class="faq-a">자란 18홀 최저가(2026년 11월 1일 기준)로는 치산 CC 온가(평일 ¥5,869〜)·문 레이크 GC 쿠라테(¥6,355〜)·기타큐슈 CC(¥6,778〜)가 저렴한 순 톱3입니다. 주말은 요금 차이가 크니, 가능하면 평일을 추천합니다.</div>', 1),
]


def main():
    src = open(os.path.join(REPO_ROOT, NAME), encoding="utf-8", newline="").read()
    t = src
    c = {"replaced": 0, "already": 0}
    for old, new, n in R:
        k = t.count(old)
        if k == n:
            t = t.replace(old, new); c["replaced"] += 1
        elif k == 0 and t.count(new) >= n:
            c["already"] += 1
        else:
            raise SystemExit(f"NO_MATCH ({k}/{n}): {old[:70]}")
    print(c, "変更あり" if t != src else "変更なし")
    if APPLY and t != src:
        for root in ROOTS:
            open(os.path.join(root, NAME), "w", encoding="utf-8", newline="").write(t)
        print("APPLIED", ROOTS)
    elif not APPLY:
        print("DRY-RUN")


if __name__ == "__main__":
    main()
