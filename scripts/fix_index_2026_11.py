#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index.html の料金まわりを 2026-10-24 のデータから 2026-11-01 のデータに揃える (じゃらん総額・book-fukuoka-cheap.html と同じ基準)。

- コスパランキング: 竜王 ¥5,400→¥5,600・4位以降 → 4位 チサン遠賀 ¥6,990・5位 セントラル ¥7,490 (かほ・ムーンレイク鞍手も同額)
- 土日祝は平日の約1.5倍 (1.1〜2.4倍) → 両方そろう30コースの中央値 約1.6倍 (1.3〜2.4倍)
- 「午後スルーを活用すれば…」 → 11月前半のじゃらんで平日に確認できたのは4コース (fix_thru_correction_2026_11.py 参照)
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_index_2026_11.py            # dry-run
  python scripts/fix_index_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_index_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "index.html"
ROW = ('                <div class="rank-name"><a href="course-{slug}.html">{name}</a><span class="rank-badge">{badge}</span></div>\r\n'
       '                <div class="rank-meta">{meta}</div>\r\n')
GAP = ('              </div>\r\n            </li>\r\n            <li class="ranking-item">\r\n'
       '              <span class="rank-num">5</span>\r\n              <div class="rank-content">\r\n')


def rows(central, chisan, c_old, c_new):
    """4位セントラル・5位チサン → 4位チサン・5位セントラル (順位の入れ替えを1ブロックで)"""
    return (ROW.format(slug="central", name=central[0], badge=c_old[0], meta=central[1]) + GAP +
            ROW.format(slug="chisan-onga", name=chisan[0], badge=c_old[1], meta=chisan[1]),
            ROW.format(slug="chisan-onga", name=chisan[0], badge=c_new[0], meta=chisan[1]) + GAP +
            ROW.format(slug="central", name=central[0], badge=c_new[1], meta=central[1]))


# (旧, 新, 出現回数)
R = [
    # ---- JSON-LD FAQ ----
    ('"text": "じゃらんの総額で比べると、平日の最安は皐月GC 竜王コース（¥5,400〜）、福岡フェザントCC（¥5,989〜）、鷹羽ロイヤルCC（¥6,690〜）の順でした（直近14日の18ホール・2026年10月24日確認）。',
     '"text": "じゃらんの総額で比べると、平日の最安は皐月GC 竜王コース（¥5,600〜）、福岡フェザントCC（¥5,989〜）、鷹羽ロイヤルCC（¥6,690〜）の順でした（直近14日の18ホール・2026年11月1日確認）。', 1),
    # ---- ランキング JA ----
    ('<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース</a><span class="rank-badge">¥5,400〜</span>', '<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース</a><span class="rank-badge">¥5,600〜</span>', 1),
    (*rows(("セントラル福岡GC", "筑紫野市・平日18ホール最安（じゃらん総額）"), ("チサン遠賀CC", "遠賀郡・平日18ホール最安（じゃらん総額）"), ("¥6,990〜", "¥6,990〜"), ("¥6,990〜", "¥7,490〜")), 1),
    ('※じゃらん「総額」・直近14日の平日最安（2026年10月24日確認）。料金は日々変わります。', '※じゃらん「総額」・直近14日の平日最安（2026年11月1日確認）。5位はかほ・ムーンレイク鞍手も同額。料金は日々変わります。', 1),
    # ---- ランキング EN ----
    ('<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course</a><span class="rank-badge">From ¥5,400</span>', '<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course</a><span class="rank-badge">From ¥5,600</span>', 1),
    (*rows(("Central Fukuoka GC", "Chikushino · weekday 18-hole low (Jalan total)"), ("Chisan Onga CC", "Onga · weekday 18-hole low (Jalan total)"), ("From ¥6,990", "From ¥6,990"), ("From ¥6,990", "From ¥7,490")), 1),
    ('* Jalan total price, lowest weekday plan in the next 14 days (checked Oct 24, 2026). Rates change daily.', '* Jalan total price, lowest weekday plan in the next 14 days (checked Nov 1, 2026). Kaho and Moon Lake Kurate tie for 5th. Rates change daily.', 1),
    # ---- ランキング KO ----
    ('<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스</a><span class="rank-badge">¥5,400부터</span>', '<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스</a><span class="rank-badge">¥5,600부터</span>', 1),
    (*rows(("센트럴 후쿠오카 GC", "지쿠시노시·평일 18홀 최저가 (자란 총액)"), ("치산 온가 CC", "온가군·평일 18홀 최저가 (자란 총액)"), ("¥6,990부터", "¥6,990부터"), ("¥6,990부터", "¥7,490부터")), 1),
    ('※자란 총액·향후 14일 평일 최저가 (2026년 10월 24일 확인). 요금은 매일 바뀝니다.', '※자란 총액·향후 14일 평일 최저가 (2026년 11월 1일 확인). 5위는 가호·문 레이크 쿠라테도 동액. 요금은 매일 바뀝니다.', 1),
    # ---- 筑豊カード ----
    ('10コース・平日¥5,400〜（総額・10/24確認）のコスパ穴場。', '10コース・平日¥5,600〜（総額・11/1確認）のコスパ穴場。', 1),
    ('10 hidden-gem courses · Weekday from ¥5,400 (total, Oct 24).', '10 hidden-gem courses · Weekday from ¥5,600 (total, Nov 1).', 1),
    ('10개 코스·평일 ¥5,400부터(총액·10/24 확인).', '10개 코스·평일 ¥5,600부터(총액·11/1 확인).', 1),
    # ---- 平日 vs 土日祝 ----
    ('じゃらんの総額で土日祝が平日の約1.5倍（32コースの中央値・2026年10月24日確認、コースにより1.1〜2.4倍）。', 'じゃらんの総額で土日祝が平日の約1.6倍（30コースの中央値・2026年11月1日確認、コースにより1.3〜2.4倍）。', 1),
    ('<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース ¥5,400</a>', '<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース ¥5,600</a>', 1),
    ('さらに<strong>午後スルー</strong>を活用すればハーフ後そのまま18Hプレーでき、半日で済むので弾丸ゴルフに最適。',
     '休憩なしで18Hを回る<strong>午後スルー</strong>は半日向きですが、設定のあるコースは限られます（2026年11月前半のじゃらんで平日に確認できたのは4コース）。', 1),
    ('differ by about 1.5× by Jalan total price (median of 32 courses, checked Oct 24, 2026; 1.1–2.4× by course).', 'differ by about 1.6× by Jalan total price (median of 30 courses, checked Nov 1, 2026; 1.3–2.4× by course).', 1),
    ('<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course ¥5,400</a>', '<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course ¥5,600</a>', 1),
    ('Use <strong>Afternoon Through</strong> rounds (continuing 18H without a break) — half-day play is ideal for short trips.',
     '<strong>Afternoon Through</strong> rounds (18H without a break) suit a half day, but few courses offer them (Jalan showed weekday plans at 4 courses in the first half of November 2026).', 1),
    ('자란 총액 기준 주말이 평일의 약 1.5배 (32개 코스 중앙값·2026년 10월 24일 확인, 코스에 따라 1.1-2.4배).', '자란 총액 기준 주말이 평일의 약 1.6배 (30개 코스 중앙값·2026년 11월 1일 확인, 코스에 따라 1.3-2.4배).', 1),
    ('<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스 ¥5,400</a>', '<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스 ¥5,600</a>', 1),
    ('<strong>오후 스루</strong>를 활용하면 하프 후 그대로 18H 플레이 가능, 반나절로 끝나 당일치기 골프에 최적.',
     '휴식 없이 18홀을 도는 <strong>오후 스루</strong>는 반나절에 적합하지만, 설정된 코스는 한정적입니다(2026년 11월 전반 자란에서 평일 확인 4개 코스).', 1),
    # ---- FAQ ----
    ('<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース</a>（¥5,400〜）', '<a href="course-satsuki-ryuoh.html">皐月GC 竜王コース</a>（¥5,600〜）', 1),
    ('<a href="course-takaha.html">鷹羽ロイヤルCC</a>（¥6,690〜）の順でした（直近14日の18ホール・2026年10月24日確認）。', '<a href="course-takaha.html">鷹羽ロイヤルCC</a>（¥6,690〜）の順でした（直近14日の18ホール・2026年11月1日確認）。', 1),
    ('<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course</a> (from ¥5,400)', '<a href="course-satsuki-ryuoh.html">Satsuki GC Ryuoh Course</a> (from ¥5,600)', 1),
    ('(18 holes, next 14 days, checked Oct 24, 2026)', '(18 holes, next 14 days, checked Nov 1, 2026)', 1),
    ('<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스</a>(¥5,400부터)', '<a href="course-satsuki-ryuoh.html">사쓰키 GC 류오 코스</a>(¥5,600부터)', 1),
    ('(향후 14일·18홀·2026년 10월 24일 확인)', '(향후 14일·18홀·2026년 11월 1일 확인)', 1),
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
            raise SystemExit(f"NO_MATCH ({k}/{n}): {old[:90]}")
    print(c, "変更あり" if t != src else "変更なし")
    if APPLY and t != src:
        for root in ROOTS:
            open(os.path.join(root, NAME), "w", encoding="utf-8", newline="").write(t)
        print("APPLIED", ROOTS)
    elif not APPLY:
        print("DRY-RUN")


if __name__ == "__main__":
    main()
