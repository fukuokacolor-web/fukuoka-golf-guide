#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
エリア・ハブ・外国人向けページの本文・統計・FAQ・meta に残る 2026-11-01 のじゃらん料金 (プラン料金) を、
2026-11-20 のじゃらん 18H 最安 (税込総額・scripts/.cache/jalan_floor.json) に合わせる。
カード料金は fix_card_prices_2026_11.py で更新済み。ここでは文章側を同じ値・同じ日付にそろえる。

再計算した値 (11/20・税込総額・じゃらんで予約できる33コース):
  全体の平日最安 皐月竜王 ¥5,300 / 平日 ¥9,000 以下 17/33 / 平日・土日祝の両方ある32コースで土日祝との差 中央値 ¥5,950 (¥2,100〜¥11,500)
  平日は土日祝より 19〜57% 安い (中央値 40%)
  筑豊 中央値 ¥7,990 (5エリアで最低) 竜王5,300・フェザント6,490・かほ6,990 / 筑後 浮羽7,500・セントラル7,990・皐月天拝/八女上陽8,400 / 久留米9,180
  福岡市 大博多9,400・久山9,480・セブンミリオン10,985・筑紫ヶ丘15,000 / 糸島 二丈7,490 / 北九州 遠賀6,990・北九州7,490・ムーンレイク7,490
  ハブ(コスパ) 平日 ¥6,490〜¥8,500・差 ¥3,500〜¥8,500 / ハブ(初心者) フェザント6,490・かほ6,990・浮羽7,500
冪等。改行コードはそのまま。Usage: python scripts/fix_area_hub_text_2026_11_20.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv

PLAN = {
    "area-chikugo.html": [
        ('<div class="stat-num">¥6,137<span class="unit">〜</span>', '<div class="stat-num">¥7,500<span class="unit">〜</span>'),
        ("平日18H最安¥6,323〜（じゃらん・11/1時点）", "平日18H最安¥7,990〜（じゃらん・11/20時点・税込総額）"),
        ("Weekday 18-hole plans from ¥6,323 (Jalan, Nov 1, 2026)", "Weekday 18 holes from ¥7,990 (Jalan, Nov 20, 2026, incl. tax)"),
        ("평일 18홀 최저 ¥6,323〜(자란·11/1 기준)", "평일 18홀 최저 ¥7,990〜(자란·11/20 기준·세금 포함 총액)"),
        ("広大な林間コース・平日¥6,137〜（じゃらん・11/1時点の18H最安）の手頃さ・戦略性の三拍子で、",
         "広大な林間コースと戦略性で知られ（じゃらんの平日18H最安は¥9,180〜・11/20時点・税込総額）、"),
        ("Wide tree-lined fairways, weekday rounds from ¥6,137 (Jalan, lowest 18-hole plan, Nov 1, 2026), and balanced strategy",
         "Wide tree-lined fairways and balanced strategy (weekday 18 holes from ¥9,180 on Jalan, Nov 20, 2026, incl. tax)"),
        ("광대한 숲속 코스·평일 ¥6,137부터(자란·11/1 기준 18홀 최저)의 합리가·전략성의 삼박자로",
         "광대한 숲속 코스와 전략성으로 알려진(자란 평일 18홀 최저 ¥9,180부터·11/20 기준·세금 포함 총액)"),
        ("じゃらんの18H最安（2026年11月1日時点）では、久留米カントリークラブ（平日¥6,137〜）・セントラル福岡ゴルフ倶楽部（¥6,323〜）・浮羽カントリークラブ（¥6,332〜）が筑後エリアの安い順トップ3。久留米とセントラルは林間、浮羽は丘陵のコースです。",
         "じゃらんの18H最安（2026年11月20日時点・税込総額）では、浮羽カントリークラブ（平日¥7,500〜）・セントラル福岡ゴルフ倶楽部（¥7,990〜）・皐月ゴルフ倶楽部 天拝コースと八女上陽ゴルフ倶楽部（ともに¥8,400〜）が筑後エリアの安い順です。浮羽は丘陵、セントラルは林間のコースです。"),
        ("On Jalan (lowest 18-hole plans, as of Nov 1, 2026), the three cheapest weekday options in Chikugo are Kurume CC (¥6,137), Central Fukuoka (¥6,323) and Ukiha CC (¥6,332). Kurume and Central are tree-lined; Ukiha is hilly.",
         "On Jalan (lowest 18-hole totals incl. tax, as of Nov 20, 2026), the cheapest weekday options in Chikugo are Ukiha CC (¥7,500), Central Fukuoka (¥7,990), then Satsuki Tenpai Course and Yame Joyo GC (both ¥8,400). Ukiha is hilly; Central is tree-lined."),
        ("자란 18홀 최저가(2026년 11월 1일 기준)로는 구루메 컨트리 클럽(평일 ¥6,137〜)·센트럴 후쿠오카 골프 클럽(¥6,323〜)·우키하 컨트리 클럽(¥6,332〜)이 치쿠고 에리어의 저렴한 순 톱3. 구루메와 센트럴은 숲속 코스, 우키하는 구릉 코스입니다.",
         "자란 18홀 최저가(2026년 11월 20일 기준·세금 포함 총액)로는 우키하 컨트리 클럽(평일 ¥7,500〜)·센트럴 후쿠오카 골프 클럽(¥7,990〜)·사쓰키 골프 클럽 덴파이 코스와 야메 죠요 골프 클럽(모두 ¥8,400〜) 순으로 저렴합니다. 우키하는 구릉, 센트럴은 숲속 코스입니다."),
    ],
    "area-chikuho.html": [
        ("¥4,605", "¥5,300"), ("平日4,605円〜", "平日5,300円〜"),
        ("福岡フェザント（¥4,959〜）、鷹羽ロイヤル（¥5,596〜）", "福岡フェザント（¥6,490〜）、かほ（¥6,990〜）"),
        ("Fukuoka Pheasant (¥4,959) and Takaha Royal (¥5,596)", "Fukuoka Pheasant (¥6,490) and Kaho (¥6,990)"),
        ("후쿠오카 페즌트(¥4,959〜), 다카하 로열(¥5,596〜)", "후쿠오카 페즌트(¥6,490〜), 카호(¥6,990〜)"),
        ('compare-price-weekday">¥6,323〜', 'compare-price-weekday">¥7,990〜'), ('compare-price-weekend">¥13,141〜', 'compare-price-weekend">¥13,990〜'),
        ('compare-price-weekday">¥10,273〜', 'compare-price-weekday">¥10,500〜'), ('compare-price-weekend">¥14,000〜', 'compare-price-weekend">¥22,000〜'),
        ('compare-price-weekday">¥7,241〜', 'compare-price-weekday">¥8,500〜'), ('compare-price-weekend">¥12,150〜', 'compare-price-weekend">¥12,000〜'),
        ("中央値¥6,323", "中央値¥7,990"), ("rate of ¥6,323", "rate of ¥7,990"), ("중앙값은 ¥6,323", "중앙값은 ¥7,990"),
    ],
    "area-fukuokacity.html": [
        ("¥8,423", "¥9,400"), ("¥9,473", "¥9,480"), ("¥10,600", "¥10,985"), ("¥13,150", "¥15,000"),
    ],
    "area-itoshima.html": [
        ("¥8,596", "¥7,490"),
    ],
    "area-kitakyushu.html": [
        ("¥5,869", "¥6,990"), ("¥6,355", "¥7,490"), ("¥6,778", "¥7,490"),
    ],
    "hub-beginner.html": [
        ("¥4,959", "¥6,490"),
        ("フェザント¥6,490・かほ¥6,323・うきは¥6,332", "フェザント¥6,490・かほ¥6,990・うきは¥7,500"),
        ("Pheasant ¥6,490, Ukiha ¥6,332", "Pheasant ¥6,490, Ukiha ¥7,500"),
        ("페전트 ¥6,490·우키하 ¥6,332", "페전트 ¥6,490·우키하 ¥7,500"),
    ],
    "hub-budget.html": [
        ("¥4,959〜¥7,241", "¥6,490〜¥8,500"), ("¥4,959–¥7,241", "¥6,490–¥8,500"),
        ("¥4,959", "¥6,490"),
        ("福岡30コース", "福岡32コース"), ("30 Fukuoka courses", "32 Fukuoka courses"), ("후쿠오카 30개 코스", "후쿠오카 32개 코스"),
        ('persona-band-num">¥5,200<', 'persona-band-num">¥6,000<'), ("about ¥5,200", "about ¥6,000"),
        ("約¥5,200", "約¥6,000"), ("median ¥5,200", "median ¥6,000"), ("약 ¥5,200", "약 ¥6,000"),
        ("¥2,727〜¥9,709", "¥2,100〜¥11,500"), ("¥2,727 to ¥9,709", "¥2,100 to ¥11,500"),
        ("年12回で約¥6万", "年12回で約¥7万"), ("about ¥60,000 over 12 rounds", "about ¥70,000 over 12 rounds"), ("12회에 약 ¥6만", "12회에 약 ¥7만"),
        ("¥4,909〜¥8,373", "¥3,500〜¥8,500"), ("¥4,909–¥8,373", "¥3,500–¥8,500"),
    ],
    "book-fukuoka-golf-foreigner.html": [
        ("¥4,605", "¥5,300"),
        ("and 20 of the 32 Fukuoka courses with weekday plans were ¥9,000 or less", "and 17 of the 33 Fukuoka courses with weekday plans were ¥9,000 or less"),
        ("평일 플랜이 있는 후쿠오카 32개 코스 중 20개 코스가", "평일 플랜이 있는 후쿠오카 33개 코스 중 17개 코스가"),
        ("across 30 Fukuoka courses on Jalan (Nov 1, 2026), the lowest weekday plan was 22–60% below the lowest weekend plan (median 39%)",
         "across 32 Fukuoka courses on Jalan (Nov 20, 2026, totals incl. tax), the lowest weekday rate was 19–57% below the lowest weekend rate (median 40%)"),
        ("자란의 후쿠오카 30개 코스(2026년 11월 1일 기준)에서 평일 최저가는 주말 최저가보다 22~60% 낮았습니다(중앙값 39%)",
         "자란의 후쿠오카 32개 코스(2026년 11월 20일 기준·세금 포함 총액)에서 평일 최저가는 주말 최저가보다 19~57% 낮았습니다(중앙값 40%)"),
    ],
    "course-chikushigaoka.html": [
        ("※じゃらん料金は2026年11月1日時点・直近2週間の平日18ホール最安（総額¥15,000）。", "※じゃらん料金は2026年11月20日時点・直近2週間の平日18ホール最安（税込総額）。土日祝は¥19,500〜。"),
        ("※자란 요금은 2026년 11월 1일 기준 향후 2주간 평일 18홀 최저가(총액 ¥15,000).", "※자란 요금은 2026년 11월 20일 기준 향후 2주간 평일 18홀 최저가(세금 포함 총액). 주말·공휴일은 ¥19,500부터."),
    ],
}
# 日付と基準の書き方 (上の個別置換のあとに全ページへ)
DATES = [
    ("じゃらんの2026年11月1日時点の18H最安", "じゃらんの2026年11月20日時点の18H最安（税込総額）"), ("2026年11月1日時点", "2026年11月20日時点"),
    ("11/1時点", "11/20時点"), ("（11/1）", "（11/20）"), ("(11/1 기준)", "(11/20 기준)"), ("(11/1)", "(11/20)"),
    ("Nov 1, 2026", "Nov 20, 2026"), ("(Nov 1)", "(Nov 20)"), ("2026년 11월 1일", "2026년 11월 20일"),
    ("lowest 18-hole plans", "lowest 18-hole totals"), ("lowest 18-hole plan,", "lowest 18-hole total,"),
    ("lowest weekday 18-hole plans", "lowest weekday 18-hole totals"), ("lowest 18-hole weekday plans", "lowest 18-hole weekday totals"),
    ("weekday 18-hole plans from", "weekday 18-hole totals from"),
]
LEFT = re.compile(r"11月1日|11/1(?![0-9])|Nov 1\b|11월 1일")

for root in ROOTS:
    for f, rules in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, miss = s, []
        for a, b in rules:
            if a in new:
                new = new.replace(a, b)
            elif b not in new:
                miss.append(a[:30])
        for a, b in DATES:
            new = new.replace(a, b)
        left = [new[max(0, m.start() - 30):m.end() + 10] for m in LEFT.finditer(new)]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"{root[-10:]} {f}: {'変更あり' if new != s else '変更なし'} 未一致 {miss} 残り {left}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
