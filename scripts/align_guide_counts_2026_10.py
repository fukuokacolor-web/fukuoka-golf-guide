#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
2026-10-24: 格安ガイド (book-fukuoka-cheap) を実料金ベースに作り直したのに合わせて、各ページの件数表記をそろえる。
  - 格安: 「平日¥6,000以下 24コース」 → 「平日¥8,000以下 9コース」 (scripts/rebuild_cheap_guide.py の結果)
  - 当日・明日 (book-fukuoka-tomorrow): 古賀GC (オンライン予約不可・CLAUDE.md §9.4) の行を外して 15 → 14
  - 一人予約 (book-fukuoka-solo): 古賀GC の行を外して 12 → 11

冪等: 置換前の文字列が無く置換後の文字列がある場合は already として数える。改行コードはファイルのまま (CRLF/LF) 保持。

Usage:
  python scripts/align_guide_counts_2026_10.py --dry-run
  python scripts/align_guide_counts_2026_10.py
"""
import re, sys, pathlib

ROOTS = [pathlib.Path("C:/Users/Owner/fukuoka-golf-guide"), pathlib.Path("C:/Users/Owner/Documents/新しいPJ")]
CHEAP_JA = ("💴 平日¥6,000以下24コース完全比較", "💴 平日¥8,000以下で回れる9コース比較")
TMR_JA = ("当日・明日予約OK 15コース", "当日・明日予約OK 14コース")

# file -> [(old, new, 期待件数)]
REPL = {
    "index.html": [("平日¥6,000以下24コース完全比較</a>に全件最安価格表掲載。", "平日¥8,000以下で回れる9コース比較</a>に確認日つきの最安価格表を掲載。", 1)],
    "guide-index.html": [
        ("格安まとめ（平日¥3,000台〜24コース）", "格安まとめ（平日¥8,000以下 9コース）", 1),
        ('<span class="guide-badge">24コース</span>', '<span class="guide-badge">9コース</span>', 1),
        ("格安まとめ｜平日¥3,000台〜", "格安まとめ｜平日¥8,000以下", 1),
        ("平日¥6,000以下で予約できる24コースを最安値順に徹底比較。節約Tipsつき。", "じゃらんの実勢料金（確認日つき）で平日¥8,000以下だった9コースを安い順に比較。", 1),
        (TMR_JA[0], TMR_JA[1], 2),
        ('<span class="guide-badge">15コース</span>', '<span class="guide-badge">14コース</span>', 1),
        ("一人予約 12コース", "一人予約 11コース", 1),
        ('<span class="guide-badge">12コース</span>', '<span class="guide-badge">11コース</span>', 1),
        ("一人予約 マッチング率高い12コース", "一人予約 マッチング率高い11コース", 1),
    ],
    "hub-budget.html": [
        ("💴 平日¥6,000以下24コース完全比較(全件表)", "💴 平日¥8,000以下で回れる9コース比較(確認日つき料金表)", 1),
        ("平日¥6,000以下 24コース比較表を見る", "平日¥8,000以下 9コース比較表を見る", 2),
        ("⏰ 当日・明日予約OK 15コース即枠取得", "⏰ 当日・明日予約OK 14コース即枠取得", 1),
        ("🧍 1人予約マッチング率高い12コース", "🧍 1人予約マッチング率高い11コース", 1),
    ],
    "sitemap-guide.html": [
        ("💴 平日¥6,000以下24コース完全比較<span>最安価格順・じゃらん deep link 付・節約Tips 4種</span>",
         "💴 平日¥8,000以下で回れる9コース比較<span>じゃらん実勢料金・確認日つき・安い順</span>", 1),
        ("💴 24 Courses ¥6,000 or less (JA only)<span>Domestic-market guide for weekday budget golfers · Jalan deep links</span>",
         "💴 9 Courses ¥8,000 or less on Weekdays (JA only)<span>Verified Jalan rates with check date · domestic JA market</span>", 1),
        ("💴 평일 ¥6,000 이하 24코스 완전 비교 (일본어판)<span>국내 시장용 가격 비교·자란 딥링크</span>",
         "💴 평일 ¥8,000 이하 9코스 비교 (일본어판)<span>자란 실제 요금·확인일 표기</span>", 1),
        ("⏰ 当日・明日予約OK 15コース<span>", "⏰ 当日・明日予約OK 14コース<span>", 1),
        ("⏰ Last-Minute Booking 15 courses (JA only)", "⏰ Last-Minute Booking 14 courses (JA only)", 1),
        ("⏰ 당일·내일 예약 가능 15코스 (일본어판)", "⏰ 당일·내일 예약 가능 14코스 (일본어판)", 1),
        ("🧍 1人予約マッチング率高い12コース<span>", "🧍 1人予約マッチング率高い11コース<span>", 1),
        ("🧍 Solo Booking 12 courses (JA only)", "🧍 Solo Booking 11 courses (JA only)", 1),
        ("🧍 1인 예약 매칭률 높은 12코스 (일본어판)", "🧍 1인 예약 매칭률 높은 11코스 (일본어판)", 1),
    ],
    "book-fukuoka-beginner.html": [
        ("格安コース 24 選", "格安コース 9 選", 1),
        ("当日・明日予約 15 コース", "当日・明日予約 14 コース", 1),
        ("1 人予約マッチング 12 コース", "1 人予約マッチング 11 コース", 1),
    ],
    "book-fukuoka-traveler.html": [
        ("格安コース 24 選", "格安コース 9 選", 1),
        ("当日・明日予約 15 選", "当日・明日予約 14 選", 1),
    ],
    "book-fukuoka-tomorrow.html": [
        (CHEAP_JA[0], CHEAP_JA[1], 1),
        ("15コース", "14コース", 12),
        ("コース15選", "コース14選", 1),
        ("Top 15 for Last-Minute", "Top 14 for Last-Minute", 1),
        ('<div class="stats-band-num">15<span class="unit">courses</span>', '<div class="stats-band-num">14<span class="unit">courses</span>', 1),
        ('"dateModified": "2026-05-05"', '"dateModified": "2026-10-24"', 1),
    ],
    "book-fukuoka-solo.html": [
        (CHEAP_JA[0], CHEAP_JA[1], 1),
        (TMR_JA[0], TMR_JA[1], 1),
        ("12コース", "11コース", 13),
        ("Top 12 for Solo", "Top 11 for Solo", 1),
        ('<div class="stats-band-num">12<span class="unit">courses</span>', '<div class="stats-band-num">11<span class="unit">courses</span>', 1),
        ('"dateModified": "2026-05-05"', '"dateModified": "2026-10-24"', 1),
    ],
}
DROP_ROW = {"book-fukuoka-tomorrow.html": "course-koga.html", "book-fukuoka-solo.html": "course-koga.html"}


def drop_and_renumber(t, href):
    row = re.compile(r'[ \t]*<tr><td class="cmp-rank">\d+</td>[^\n]*?href="' + re.escape(href) + r'"[^\n]*?</tr>\r?\n')
    t, k = row.subn("", t)
    if k:  # 比較表 tbody 内の順位を 1.. で振り直す
        def renum(m):
            i = iter(range(1, 1000))
            return re.sub(r'<td class="cmp-rank">\d+</td>', lambda _: f'<td class="cmp-rank">{next(i)}</td>', m.group(0))
        t = re.sub(r"<tbody>.*?</tbody>", renum, t, flags=re.S)
    return t, k


def main():
    dry = "--dry-run" in sys.argv
    bad = False
    for root in ROOTS:
        print(f"== {root}")
        for f, reps in REPL.items():
            p = root / f
            if not p.exists():
                print(f"  {f}: not_found"); bad = True; continue
            raw = p.read_bytes()
            t = raw.decode("utf-8")
            out = []
            # 行削除を先に (「15コース」等の置換は行の中身に依存しない)
            if f in DROP_ROW:
                t, k = drop_and_renumber(t, DROP_ROW[f])
                out.append(f"drop {DROP_ROW[f]}: {'removed' if k else 'already'}")
            for old, new, n in reps:
                c = t.count(old)
                if c == n:
                    t = t.replace(old, new); out.append(f"replaced×{c}")
                elif c == 0 and new in t:
                    out.append("already")
                else:
                    out.append(f"!! no_match (found {c}, expected {n}): {old[:40]}"); bad = True
            changed = t.encode("utf-8") != raw
            crlf = raw.count(b"\r\n"); lf = raw.count(b"\n")
            print(f"  {f}: {'CHANGED' if changed else 'same'} [{'CRLF' if crlf == lf and lf else 'LF' if not crlf else f'MIXED {crlf}/{lf}'}] " + " | ".join(out))
            if changed and not dry:
                p.write_bytes(t.encode("utf-8"))
    if bad:
        print("!! 不一致あり — 内容を確認してください")
    print("(dry-run: 書き込みなし)" if dry else "done")


if __name__ == "__main__":
    main()
