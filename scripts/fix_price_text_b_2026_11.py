#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
料金欄以外 (meta / og / JSON-LD / FAQ / 本文 / バナー) に残る古い料金を、2026-11-20 のじゃらん 18H 最安 (税込総額) に合わせる。
  センチュリー 平日¥13,000 / 皐月竜王 平日¥5,300 / 鷹羽 平日¥7,890・土日祝¥15,900 / 福岡国際 平日¥9,500・土日祝¥15,400
  浮羽 平日¥7,500・土日祝¥13,000 / フェザント 平日¥6,490 (変わらず)・土日祝¥14,990
  確かめられない金額 (鷹羽の早朝/薄暮、フェザントのメンバー価格・平日上限¥7,990、センチュリーの午後スルー¥5,500) は外す。
冪等。改行コードはそのまま。Usage: python scripts/fix_price_text_b_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
N = "2026年11月時点・じゃらん・税込総額"

PLAN = {
    "course-century.html": [
        ("平日¥9,500〜、午後スルー¥5,500〜。", f"平日¥13,000〜（{N}）。"),
    ],
    "course-satsuki-ryuoh.html": [
        ("平日¥3,332〜の好コスパ。", f"平日¥5,300〜（{N}）。"),
    ],
    "course-takaha.html": [
        ("月曜セルフデーは¥7,880の高コスパ。", f"平日¥7,890〜（{N}）。"),
        ("月曜セルフデー¥7,880の高コスパ。", f"平日¥7,890〜（{N}）。"),
        ('"priceRange": "¥7,880〜¥19,340"', '"priceRange": "¥7,890〜¥15,900"'),
        ('<span class="hero-badge">🎯 月曜セルフ¥7,880</span>', '<span class="hero-badge">🎯 平日¥7,890〜</span>'),
        ("｜ 月曜セルフデー¥7,880・最新空き状況をチェック", "｜ 平日¥7,890〜（2026年11月時点）・最新空き状況をチェック"),
        ('<div class="deal-banner-title">月曜「鷹羽セルフデー」¥7,880 — 春季限定の最強コスパ</div>', '<div class="deal-banner-title">平日のじゃらん最安 ¥7,890〜（2026年11月時点・税込総額）</div>'),
        ("<strong>月曜セルフデー¥7,880の高コスパ</strong>春季の月曜は本格18Hが最強価格で楽しめる「鷹羽セルフデー」。",
         "<strong>平日¥7,890〜（2026年11月時点）</strong>じゃらんゴルフの平日18ホール最安（税込総額）。季節の割安プランは予約サイトで確認を。"),
        ("平日の早朝¥7,810 / 薄暮¥7,420で18ホール。時間と費用を節約しつつ本格ラウンドが楽しめます。", "平日の早朝・薄暮プランもあります。設定日と料金は予約サイトでご確認ください。"),
        ('<span class="hero-badge">🎯 Mon Self-Day ¥7,880</span>', '<span class="hero-badge">🎯 Weekdays from ¥7,890</span>'),
        ("｜ Monday Self-Day ¥7,880 — check current rates", "｜ Weekdays from ¥7,890 (Nov 2026) — check current rates"),
        ('<div class="deal-banner-title">"Takaha Self-Day" Monday — ¥7,880 best value (spring season)</div>', '<div class="deal-banner-title">Lowest weekday total on Jalan: from ¥7,890 (Nov 2026, incl. tax)</div>'),
        ('<strong>Monday Self-Day ¥7,880 unbeatable value</strong>Spring Monday "Takaha Self-Day" — a serious 18-hole round at the lowest price.',
         "<strong>Weekdays from ¥7,890 (Nov 2026)</strong>Lowest weekday 18-hole total on Jalan Golf (incl. tax). Check the booking sites for seasonal deals."),
        ("Weekday early-bird ¥7,810 / twilight ¥7,420 for full 18 holes — saving time and money while playing the full course.", "Early-morning and twilight weekday plans are also offered. Check dates and prices on the booking sites."),
        ('<span class="hero-badge">🎯 월요 셀프 ¥7,880</span>', '<span class="hero-badge">🎯 평일 ¥7,890부터</span>'),
        ("｜ 월요 셀프데이 ¥7,880・최신 빈자리 확인", "｜ 평일 ¥7,890부터 (2026년 11월)・최신 빈자리 확인"),
        ('<div class="deal-banner-title">월요 「타카하 셀프데이」 ¥7,880 — 봄 시즌 최고의 가성비</div>', '<div class="deal-banner-title">자란 평일 최저가 ¥7,890부터 (2026년 11월·세금 포함 총액)</div>'),
        ("<strong>월요 셀프데이 ¥7,880의 높은 가성비</strong>봄 시즌 월요는 본격 18홀을 최고 가성비로 즐길 수 있는 「타카하 셀프데이」.",
         "<strong>평일 ¥7,890부터 (2026년 11월)</strong>자란골프 평일 18홀 최저가 (세금 포함 총액). 시즌 할인 플랜은 예약 사이트에서 확인하세요."),
        ("평일 조조 ¥7,810 / 박명 ¥7,420으로 18홀. 시간과 비용을 절약하면서 본격 라운드를 즐길 수 있습니다.", "평일 조조·박모 플랜도 있습니다. 설정일과 요금은 예약 사이트에서 확인해 주세요."),
    ],
    "course-fukuokakokusai.html": [
        ("平日¥7,241〜・土日祝¥11,100〜（季節変動あり）。", f"平日¥9,500〜・土日祝¥15,400〜（{N}）。"),
        ("平日¥7,241〜・土日祝¥11,100〜（季節変動）。", f"平日¥9,500〜・土日祝¥15,400〜（{N}）。"),
        ('"priceRange": "¥7,241〜¥15,400"', '"priceRange": "¥9,500〜¥15,400"'),
        ("2026年6月時点でじゃらんゴルフの平日最安は¥7,241前後〜、土日祝は¥11,500前後〜。繁忙期は土日¥15,400まで上がります。",
         "2026年11月時点のじゃらんゴルフの18ホール最安は、平日¥9,500〜、土日祝¥15,400〜（税込総額）です。"),
        ("2026年6月時点でじゃらん平日最安は<strong>¥7,241前後〜</strong>、土日祝は¥11,500前後〜、繁忙期は土日¥15,400まで。",
         "2026年11月時点のじゃらん18ホール最安は平日<strong>¥9,500〜</strong>、土日祝¥15,400〜（税込総額）。"),
    ],
    "course-ukiha.html": [
        ("季節変動の幅広い料金（じゃらん¥4,500〜）でコスパ良好。", f"平日¥7,500〜・土日祝¥13,000〜（{N}）。"),
        ('"priceRange": "¥4,500〜¥11,332"', '"priceRange": "¥7,500〜¥13,000"'),
        ("じゃらん¥4,500〜のコスパ良好な18ホール。", f"平日¥7,500〜（{N}）の18ホール。"),
        ("<strong>幅広い料金レンジ</strong>じゃらんで¥4,500〜と平日早朝はコスパ良好。プランで大きく変動。",
         "<strong>平日¥7,500〜（2026年11月時点）</strong>じゃらんゴルフの平日18ホール最安（税込総額）。プランで大きく変動。"),
        ("2026年6月時点でじゃらんゴルフは¥4,500前後〜、繁忙期の土日は¥11,000前後まで。最安を狙うなら平日早朝・閑散期がおすすめです。",
         "2026年11月時点のじゃらんゴルフの18ホール最安は、平日¥7,500〜、土日祝¥13,000〜（税込総額）です。"),
        ("2026年6月時点でじゃらんは<strong>¥4,500前後〜</strong>、繁忙期の土日は¥11,000前後まで。最安狙いは平日早朝・閑散期。",
         "2026年11月時点のじゃらん18ホール最安は平日<strong>¥7,500〜</strong>、土日祝¥13,000〜（税込総額）。"),
        ("<strong>Wide price range</strong>From ¥4,500 on Jalan — weekday early mornings are exceptional value.",
         "<strong>Weekdays from ¥7,500 (Nov 2026)</strong>Lowest weekday 18-hole total on Jalan Golf (incl. tax). Prices vary widely by plan."),
        ("<strong>넓은 요금대</strong>자란에서 ¥4,500부터 — 평일 새벽은 가성비 우수. 플랜에 따라 크게 변동.",
         "<strong>평일 ¥7,500부터 (2026년 11월)</strong>자란골프 평일 18홀 최저가 (세금 포함 총액). 플랜에 따라 크게 변동."),
    ],
    "course-pheasant.html": [
        ("平日昼食付¥6,490〜・土日約¥10,400の高コスパ。", f"平日¥6,490〜・土日祝¥14,990〜（{N}）。"),
        ('"priceRange": "¥6,490〜¥10,400"', '"priceRange": "¥6,490〜¥14,990"'),
        ("¥6,490〜¥7,990(季節変動)。アコーディア系コスパの高コスパ昼食付プランで18ホール。", "平日¥6,490〜（2026年11月時点・じゃらん・税込総額）。昼食補助付きのプランがあります。"),
        ("アコーディアメンバーズプログラム経由のメンバー価格 ¥5,414〜。会員登録で特典も。", "アコーディアの会員プログラムでは会員向けの価格があります。料金は公式でご確認ください。"),
        ("平日は昼食付¥6,490〜¥7,990、土日祝は約¥10,400が目安です。早朝・薄暮の昼食なしプランなら平日¥4,900台〜も出ます(2026年6月時点)。",
         "2026年11月時点のじゃらんゴルフの18ホール最安は、平日¥6,490〜、土日祝¥14,990〜（税込総額）です。"),
        ("平日は<strong>昼食付¥6,490〜¥7,990</strong>、土日祝は約¥10,400が目安。早朝・薄暮の昼食なしプランなら平日<strong>¥4,900台〜</strong>も出ます(2026年6月時点)。",
         "2026年11月時点のじゃらん18ホール最安は、平日<strong>¥6,490〜</strong>、土日祝<strong>¥14,990〜</strong>（税込総額）。"),
        ("¥6,490〜¥7,990 (seasonal). Accordia's signature value-priced lunch-included 18-hole plan.", "Weekdays from ¥6,490 (Nov 2026, Jalan, incl. tax). Plans with a lunch allowance are available."),
        ("Member rate via Accordia Members Program from ¥5,414. Member registration unlocks additional benefits.", "Accordia's membership program offers member pricing. Check the official site for rates."),
        ("¥6,490〜¥7,990(시즌별 변동). 아코디아의 가성비 점심 포함 18홀 플랜.", "평일 ¥6,490부터 (2026년 11월·자란·세금 포함 총액). 점심 보조 포함 플랜이 있습니다."),
    ],
}

for root in ROOTS:
    for f, rules in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, n, miss = s, 0, []
        for a, b in rules:
            if a in new:
                new = new.replace(a, b); n += 1
            elif b not in new:
                miss.append(a[:28])
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"{root[-10:]} {f}: {n}{' (変更なし)' if new == s else ''} 未一致 {miss}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
