#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
area-itoshima.html のページ全体の金額表現を直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日最安 ¥4,000〜」「二丈 平日¥4,000台・糸島最安」 → じゃらん18H最安 (2026-11-01) は 二丈 ¥8,596・伊都 ¥16,378
  (芥屋・クイーンズヒル・雷山は公式のみ、志摩シーサイドはじゃらんに11月前半の販売なし)
- クイーンズヒル「午後スルー ¥5,000〜9,000」「午後スルー対応」 → 公式料金ページ (queenshill.co.jp/price/・2026-11-04 確認) に
  午後スルーの記載なし。ゲスト 平日 ¥21,800・土日祝 ¥30,200 (税込・キャディフィ4バッグ込・2026年3月1日〜)
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)・queenshill.co.jp/price/
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_itoshima_2026_11.py            # dry-run
  python scripts/fix_itoshima_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_itoshima_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "area-itoshima.html"
STAT = '<div class="stat-num">{}<span class="unit">〜</span></div><div class="stat-label">{}</div>'

# (旧, 新, 出現回数)
R = [
    # ---- stats ----
    (STAT.format("¥4,000", "平日最安"), STAT.format("¥8,596", "じゃらん平日最安（11/1）"), 1),
    (STAT.format("¥4,000", "Lowest weekday"), STAT.format("¥8,596", "Lowest weekday on Jalan (Nov 1)"), 1),
    (STAT.format("¥4,000", "평일 최저"), STAT.format("¥8,596", "자란 평일 최저(11/1)"), 1),
    # ---- クイーンズヒル チップ (公式料金はキャディフィ込) ----
    ('<span class="course-chip">午後スルー対応</span>', '<span class="course-chip">キャディ付</span>', 1),
    ('<span class="course-chip">Afternoon thru</span>', '<span class="course-chip">Caddie included</span>', 1),
    ('<span class="course-chip">오후 스루 가능</span>', '<span class="course-chip">캐디 포함</span>', 1),
    # ---- モデルプラン DAY1 ----
    ('<strong>クイーンズヒル</strong>で午後スルーラウンド（¥5,000〜9,000）。空港から最短30分。',
     '<strong>クイーンズヒル</strong>でラウンド（公式のゲスト料金は平日¥21,800・キャディ付、2026年3月〜）。空港から最短30分。', 1),
    ('Afternoon-thru round at <strong>Queen\'s Hill</strong> (¥5,000–9,000). Only 30 min from FUK.',
     'Round at <strong>Queen\'s Hill</strong> (official guest rate ¥21,800 on weekdays, caddie included, from March 2026). Only 30 min from FUK.', 1),
    ('<strong>퀸즈힐</strong>에서 오후 스루 라운드（¥5,000〜9,000）. 공항에서 최단 30분.',
     '<strong>퀸즈힐</strong>에서 라운드(공식 게스트 요금 평일 ¥21,800·캐디 포함, 2026년 3월〜). 공항에서 최단 30분.', 1),
    # ---- FAQ 到着日 ----
    ('<div class="faq-a">クイーンズヒルなら十分可能です。福岡空港から車で30分、午後スルー料金は¥5,000〜9,000とリーズナブル。午前便で到着→午後プレーの定番ルート。</div>',
     '<div class="faq-a">クイーンズヒルは福岡空港から車で約30分と近く、午前便で着いて午後にプレーする組み方ができます。公式の料金ページに午後スルーの記載は無く、ゲスト料金は平日¥21,800（税込・キャディ付、2026年3月〜）。空き枠は公式サイトのオンライン予約で確認してください。</div>', 1),
    ('<div class="faq-a">Yes, via Queen\'s Hill. At 30 min from Fukuoka Airport with afternoon-thru rates from ¥5,000–9,000, it\'s the classic arrival-day option for visiting golfers.</div>',
     '<div class="faq-a">Queen\'s Hill is about 30 min from Fukuoka Airport, so a morning flight plus an afternoon round can work. Its official price page lists no afternoon-thru plan; the weekday guest rate is ¥21,800 (tax and caddie included, from March 2026). Check open slots via the official online booking.</div>', 1),
    ('<div class="faq-a">퀸즈힐이라면 충분히 가능. 후쿠오카공항에서 차로 30분, 오후 스루 요금은 ¥5,000〜9,000으로 합리적. 오전 편 도착→오후 플레이의 정석 루트.</div>',
     '<div class="faq-a">퀸즈힐은 후쿠오카공항에서 차로 약 30분으로 가까워, 오전 편 도착→오후 플레이가 가능합니다. 공식 요금 페이지에 오후 스루 기재는 없고, 게스트 요금은 평일 ¥21,800(세금·캐디 포함, 2026년 3월〜). 빈 시간대는 공식 사이트 온라인 예약에서 확인하세요.</div>', 1),
    # ---- FAQ 最安 ----
    ('<div class="faq-a">二丈カントリークラブです。平日¥4,000台からプレー可能で、糸島エリア最安値。',
     '<div class="faq-a">二丈カントリークラブです。じゃらんの18H最安（2026年11月1日時点）は平日¥8,596〜で、糸島で料金を確認できたコース（二丈・伊都・クイーンズヒル）の中で最安。', 1),
    ('<div class="faq-a">Nijo Country Club — weekday rounds from ¥4,000, with ocean glimpses from the hilltop.',
     '<div class="faq-a">Nijo Country Club — weekday rounds from ¥8,596 (Jalan, lowest 18-hole plan, Nov 1, 2026), the lowest among the Itoshima courses whose rates we could check, with ocean glimpses from the hilltop.', 1),
    ('<div class="faq-a">니조 컨트리 클럽. 평일 ¥4,000대부터 플레이 가능, 이토시마 에리어 최저가.',
     '<div class="faq-a">니조 컨트리 클럽. 자란 18홀 최저가(2026년 11월 1일 기준) 평일 ¥8,596부터로, 이토시마에서 요금을 확인한 코스(니조·이토·퀸즈힐) 중 최저.', 1),
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
