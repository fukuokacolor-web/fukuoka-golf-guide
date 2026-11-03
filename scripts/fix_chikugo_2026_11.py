#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
area-chikugo.html のページ全体の金額表現を直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日最安 ¥6,000〜」「平日¥6,000台〜」 → じゃらん18H最安 (2026-11-01) で本ページの平日最安は 久留米CC ¥6,137
  (以下 セントラル福岡 ¥6,323・浮羽 ¥6,332・有明 ¥6,773・八女上陽 ¥7,146・皐月天拝 ¥8,150)
- モデルプラン「セントラル福岡で午後スルー・平日¥6,500〜」・FAQ「午後スルー対応も◎」 → 11月前半のじゃらんでセントラルは午前スルーのみ
- セントラルのカード「午後スルー対応コースとしても人気」も同じ理由で外す
- FAQ「久留米・セントラルとも¥6,000台」は合っているが「どちらも初心者に優しい・午後スルー対応」は根拠なし → 安い順3コースに
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_chikugo_2026_11.py            # dry-run
  python scripts/fix_chikugo_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_chikugo_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "area-chikugo.html"
STAT = '<div class="stat-num">{}<span class="unit">〜</span></div><div class="stat-label">{}</div>'

# (旧, 新, 出現回数)
R = [
    # ---- stats ----
    (STAT.format("¥6,000", "平日最安"), STAT.format("¥6,137", "平日最安（11/1）"), 1),
    (STAT.format("¥6,000", "Lowest weekday"), STAT.format("¥6,137", "Lowest weekday (Nov 1)"), 1),
    (STAT.format("¥6,000", "평일 최저"), STAT.format("¥6,137", "평일 최저(11/1)"), 1),
    # ---- モデルプラン DAY1 ----
    ('<strong>セントラル福岡</strong>で午後スルーラウンド（空港から約50分）。平日¥6,500〜。',
     '<strong>セントラル福岡</strong>へ（空港から約50分）。午後の空き枠があれば到着日にラウンド。平日18H最安¥6,323〜（じゃらん・11/1時点）。', 1),
    ('Afternoon-thru at <strong>Central Fukuoka</strong> (~50 min from FUK). From ¥6,500 weekdays.',
     'Head to <strong>Central Fukuoka</strong> (~50 min from FUK) and play if there\'s an afternoon slot. Weekday 18-hole plans from ¥6,323 (Jalan, Nov 1, 2026).', 1),
    ('<strong>센트럴 후쿠오카</strong>에서 오후 스루 라운드(공항에서 약 50분). 평일 ¥6,500〜.',
     '<strong>센트럴 후쿠오카</strong>로 이동(공항에서 약 50분). 오후 빈 시간대가 있으면 도착일에 라운드. 평일 18홀 최저 ¥6,323〜(자란·11/1 기준).', 1),
    # ---- セントラル カード (午後スルー対応は根拠なし) ----
    ('<div class="course-desc">筑紫野市・山家地区の林間コース。午後スルー対応コースとしても人気で、福岡市内からの日帰りプレーの定番。</div>',
     '<div class="course-desc">筑紫野市・山家地区の林間コース。アコーディア・ゴルフ運営で、福岡市内からの日帰りプレーにも使えます。</div>', 1),
    ('<div class="course-desc">치쿠시노시·야마에 지구의 숲속 코스. 오후 스루 대응 코스로도 인기, 후쿠오카 시내에서의 당일 플레이 정석.</div>',
     '<div class="course-desc">치쿠시노시·야마에 지구의 숲속 코스. 아코디아 골프 운영으로, 후쿠오카 시내에서 당일 플레이도 가능합니다.</div>', 1),
    # ---- FAQ 一番人気 ----
    ('広大な林間コース・平日¥6,000台〜の手頃さ・戦略性の三拍子で、',
     '広大な林間コース・平日¥6,137〜（じゃらん・11/1時点の18H最安）の手頃さ・戦略性の三拍子で、', 1),
    ('Wide tree-lined fairways, weekday rounds from ¥6,000, and balanced strategy',
     'Wide tree-lined fairways, weekday rounds from ¥6,137 (Jalan, lowest 18-hole plan, Nov 1, 2026), and balanced strategy', 1),
    ('광대한 숲속 코스·평일 ¥6,000대부터의 합리가·전략성의 삼박자로',
     '광대한 숲속 코스·평일 ¥6,137부터(자란·11/1 기준 18홀 최저)의 합리가·전략성의 삼박자로', 1),
    # ---- FAQ コスパ ----
    ('<div class="faq-a">久留米カントリークラブとセントラル福岡ゴルフ倶楽部が平日¥6,000台からプレー可能。どちらも広くて林間コースで、初心者にも優しいレイアウト。午後スルー対応も◎。</div>',
     '<div class="faq-a">じゃらんの18H最安（2026年11月1日時点）では、久留米カントリークラブ（平日¥6,137〜）・セントラル福岡ゴルフ倶楽部（¥6,323〜）・浮羽カントリークラブ（¥6,332〜）が筑後エリアの安い順トップ3。久留米とセントラルは林間、浮羽は丘陵のコースです。</div>', 1),
    ('<div class="faq-a">Kurume CC and Central Fukuoka offer weekday rounds from ¥6,000–6,500. Both are spacious tree-lined layouts welcoming to all levels, and both run afternoon-thru plays.</div>',
     '<div class="faq-a">On Jalan (lowest 18-hole plans, as of Nov 1, 2026), the three cheapest weekday options in Chikugo are Kurume CC (¥6,137), Central Fukuoka (¥6,323) and Ukiha CC (¥6,332). Kurume and Central are tree-lined; Ukiha is hilly.</div>', 1),
    ('<div class="faq-a">구루메 컨트리 클럽과 센트럴 후쿠오카 골프 클럽이 평일 ¥6,000대부터 플레이 가능. 둘 다 넓은 숲속 코스로 초급자에게도 친절한 레이아웃. 오후 스루 대응도 좋음.</div>',
     '<div class="faq-a">자란 18홀 최저가(2026년 11월 1일 기준)로는 구루메 컨트리 클럽(평일 ¥6,137〜)·센트럴 후쿠오카 골프 클럽(¥6,323〜)·우키하 컨트리 클럽(¥6,332〜)이 치쿠고 에리어의 저렴한 순 톱3. 구루메와 센트럴은 숲속 코스, 우키하는 구릉 코스입니다.</div>', 1),
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
