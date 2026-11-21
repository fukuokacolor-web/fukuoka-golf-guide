#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式料金を載せている 3 コース (芥屋・クイーンズヒル・雷山) を、2026-11-21 に確認した公式の料金表に合わせる。
  芥屋 https://www.keyagc.co.jp/fee/ : ビジター平日¥21,500〜25,000・土日祝¥30,500〜34,000 (季節7段階)・メンバー¥10,400 は一致。
      貸クラブは¥6,600 (旧表記¥5,500)。薄暮9H はビジター平日¥9,800・土日祝¥13,000 (旧表記「割安プランなら平日¥7,000台〜」は根拠なし → 外す)。
  クイーンズヒル https://queenshill.co.jp/price/ : ゲスト平日¥21,800・土日祝¥30,200 (税込・キャディフィ4バッグ込・2026年3月1日〜) は一致。
      説明文の「料金は掲載していません」が表示と矛盾 → 公式料金を載せている旨に。
  雷山 http://raizan-gc.co.jp/rate-plan/ : ビジター セルフは 9/1〜1/3 が平日¥19,900・土日祝¥25,900、1/5〜2/28 と 7〜8月が¥18,900・¥24,900。
      薄暮(9H セルフ) は 9/1〜1/3 が平日¥8,000・土日祝¥11,000、1/5〜2/28 が¥6,500・¥9,000 (旧表記¥7,500〜10,000)。
      公式の注記は「利用税・消費税込」(カート代込みとは書いていない)。韓国語の「약 18.9만원」等のウォン換算は誤り (桁違い) → 外す。
  共通: 公式でしか予約できないコースに「2 サイト 予約サイト比較」の数字があったので「公式 予約先」に (5ページ)。
冪等。改行コードはそのまま。Usage: python scripts/fix_official_prices_2026_11_21.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv

STAT = [
    ('<div class="stat-num">2<span class="unit">サイト</span></div><div class="stat-label">予約サイト比較</div>',
     '<div class="stat-num">公式<span class="unit"></span></div><div class="stat-label">予約先</div>'),
    ('<div class="stat-num">2<span class="unit">sites</span></div><div class="stat-label">Compare bookings</div>',
     '<div class="stat-num">Official<span class="unit"></span></div><div class="stat-label">How to book</div>'),
    ('<div class="stat-num">2<span class="unit">사이트</span></div><div class="stat-label">예약 사이트 비교</div>',
     '<div class="stat-num">공식<span class="unit"></span></div><div class="stat-label">예약처</div>'),
]
KEYA_FAQ_OLD = "一方で薄暮など割安プランなら平日¥7,000台〜の設定が出ることもあります（時期・プランにより変動）。乗用カートは別途¥1,250。最新の料金・空き状況はじゃらん・楽天GORA・公式でご確認ください。"
KEYA_FAQ_NEW = "薄暮（9H）はビジター平日¥9,800・土日祝¥13,000。乗用カートは別途¥1,250。予約・最新の料金は公式サイトか電話で（2026年11月公式料金表で確認）。"

PLAN = {
    "course-keya.html": STAT + [
        ("<strong>薄暮など割安プランなら平日¥7,000台〜</strong>の設定が出ることも(時期・プランにより変動)。最新料金・空き状況は公式サイトまたは予約サイトでご確認ください。",
         "薄暮（9H）はビジター平日¥9,800・土日祝¥13,000。料金は2026年11月に公式の料金表で確認したもので、予約は公式サイトか電話です。"),
        ("貸クラブ¥5,500・貸シューズ¥1,100。", "貸クラブ¥6,600・貸シューズ¥1,100。"),
        (KEYA_FAQ_OLD, KEYA_FAQ_NEW),
        ("一方で<strong>薄暮など割安プランなら平日¥7,000台〜</strong>の設定が出ることも(時期・プランにより変動)。カート別¥1,250。最新はじゃらん・楽天GORA・公式で確認を。",
         "薄暮（9H）はビジター平日¥9,800・土日祝¥13,000。カート別¥1,250。予約は公式サイトか電話で。"),
        ("Club rental ¥5,500, shoes ¥1,100.", "Club rental ¥6,600, shoes ¥1,100."),
        ("최신 요금·빈자리는 공식 사이트 또는 예약 사이트에서 확인해 주세요.", "요금은 2026년 11월 공식 요금표 기준이며, 예약은 공식 사이트나 전화로 합니다."),
        ("클럽 대여 ¥5,500, 신발 대여 ¥1,100.", "클럽 대여 ¥6,600, 신발 대여 ¥1,100."),
    ],
    "course-queenshill.html": STAT + [
        ("このコースはオンライン予約サイトでの販売が確認できないため、料金は掲載していません（2026年10月時点）。ビジター料金・予約方法は公式サイトまたは電話でご確認ください。",
         "下記は公式サイトのゲスト料金です（18ホール・税込・キャディフィ4バッグ込、2026年3月1日〜。2026年11月確認）。じゃらん・楽天GORAでは販売されていないため、予約は公式サイトか電話で。"),
        ("Rates are not listed because online booking is not available for this course (as of Oct 2026). Check visitor rates and booking on the official website or by phone.",
         "Guest rates from the official website (18 holes, incl. tax and caddie fee for 4 bags, from 1 Mar 2026; checked Nov 2026). Not sold on Jalan or Rakuten GORA — book on the official website or by phone."),
        ("이 코스는 온라인 예약 사이트에서 판매가 확인되지 않아 요금을 게재하지 않습니다 (2026년 10월 기준). 비지터 요금·예약 방법은 공식 사이트 또는 전화로 확인해 주세요.",
         "아래는 공식 사이트의 게스트 요금입니다 (18홀·세금 포함·캐디피 4백 포함, 2026년 3월 1일부터. 2026년 11월 확인). 자란·라쿠텐 GORA에서는 판매하지 않으므로 공식 사이트나 전화로 예약하세요."),
    ],
    "course-raizan.html": STAT + [
        ('<span class="yen">¥</span>18,900<span class="range"></span>', '<span class="yen">¥</span>18,900<span class="range">〜19,900</span>'),
        ('<span class="yen">¥</span>24,900<span class="range"></span>', '<span class="yen">¥</span>24,900<span class="range">〜25,900</span>'),
        ('<span class="yen">¥</span>7,500<span class="range">〜10,000</span>', '<span class="yen">¥</span>6,500<span class="range">〜11,000</span>'),
        (' <span style="color:#1a3a8f;font-size:0.78rem;">(약 18.9만원)</span>', ''),
        (' <span style="color:#1a3a8f;font-size:0.78rem;">(약 24.9만원)</span>', ''),
        (' <span style="color:#1a3a8f;font-size:0.78rem;">(약 7.5만원〜10만원)</span>', ''),
        ("下記はビジター料金の目安です。カートフィー・ゴルフ場利用税・消費税込み。最新料金・空き状況は公式サイトまたは予約サイトでご確認ください。",
         "下記は公式サイトのビジター料金です（利用税・消費税込、2026年11月確認）。時期で3段階に変わり、9月1日〜1月3日がいちばん高い設定です。予約は公式サイトか電話で。"),
        ("カートフィー・ゴルフ場利用税込みのビジター料金目安。プレー時期・予約サイトにより変動します。", "9/1〜1/3は¥19,900、1/5〜2/28と7〜8月は¥18,900（公式）。"),
        ("カートフィー・ゴルフ場利用税込みのビジター料金目安。土日祝・人気時間帯は早めの予約を。", "9/1〜1/3は¥25,900、1/5〜2/28と7〜8月は¥24,900（公式）。"),
        ("カートフィー・ゴルフ場利用税込みのビジター料金目安。最新の空き状況は予約サイトでご確認ください。", "9/1〜1/3は平日¥8,000・土日祝¥11,000、1/5〜2/28は¥6,500・¥9,000（公式）。"),
        ("上記はカートフィー・ゴルフ場利用税・消費税込みのビジター料金の目安です。2名プレー割増・キャディ付プラン・季節料金など詳細は公式サイトまたは予約サイトでご確認ください。",
         "上記は公式のビジター料金（利用税・消費税込）です。キャディ付は平日¥21,900〜24,900・土日祝¥30,900〜31,900。2名・3名プレーは割増があります。詳細は公式サイトで。"),
        ("Visitor rate incl. cart fee and taxes. Varies by season and booking site.", "¥19,900 from 1 Sep to 3 Jan; ¥18,900 from 5 Jan to 28 Feb and in Jul–Aug (official)."),
        ("Visitor rate incl. cart fee and taxes. Weekends and peak times book out early.", "¥25,900 from 1 Sep to 3 Jan; ¥24,900 from 5 Jan to 28 Feb and in Jul–Aug (official)."),
        ("Visitor rate incl. cart fee and taxes. Check current availability on the booking site.", "1 Sep–3 Jan: weekday ¥8,000 / weekend ¥11,000; 5 Jan–28 Feb: ¥6,500 / ¥9,000 (official)."),
        ("Rates above include cart fee, golf tax, and consumption tax (visitor estimate). 2-player surcharges, caddie plans, and seasonal rates may apply — see the official site or booking platform for details.",
         "Official visitor rates incl. golf tax and consumption tax (checked Nov 2026). With a caddie: weekday ¥21,900–24,900, weekend ¥30,900–31,900. Surcharges apply for 2- and 3-player groups. Book on the official website or by phone."),
        ("아래는 비지터 요금 기준입니다. 카트피·골프장 이용세·소비세 포함. 최신 요금·빈자리는 공식 사이트 또는 예약 사이트에서 확인해 주세요.",
         "아래는 공식 사이트의 비지터 요금입니다 (이용세·소비세 포함, 2026년 11월 확인). 시기에 따라 3단계로 바뀌며 9월 1일〜1월 3일이 가장 높습니다. 예약은 공식 사이트나 전화로."),
        ("카트피·골프장 이용세 포함 비지터 요금 기준. 시즌·예약 사이트에 따라 변동됩니다.", "9/1〜1/3은 ¥19,900, 1/5〜2/28과 7〜8월은 ¥18,900 (공식)."),
        ("카트피·골프장 이용세 포함 비지터 요금 기준. 주말·인기 시간대는 조기 예약 권장.", "9/1〜1/3은 ¥25,900, 1/5〜2/28과 7〜8월은 ¥24,900 (공식)."),
        ("카트피·골프장 이용세 포함 비지터 요금 기준. 최신 빈자리는 예약 사이트에서 확인하세요.", "9/1〜1/3은 평일 ¥8,000·주말 ¥11,000, 1/5〜2/28은 ¥6,500·¥9,000 (공식)."),
        ("위 요금은 카트피·골프장 이용세·소비세 포함 비지터 요금 기준입니다. 2인 플레이 할증·캐디 포함 플랜·시즌 요금 등 상세는 공식 사이트 또는 예약 사이트에서 확인해 주세요.",
         "위 요금은 공식 비지터 요금(이용세·소비세 포함)입니다. 캐디 포함은 평일 ¥21,900〜24,900·주말 ¥30,900〜31,900. 2인·3인 플레이는 할증이 있습니다. 상세는 공식 사이트에서."),
    ],
    "course-classic.html": STAT,
    "course-koga.html": STAT,
}

for root in ROOTS:
    for f, rules in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, miss = s, []
        for a, b in rules:
            if a and a in new:
                new = new.replace(a, b)
            elif b and b not in new and not a.startswith('<div class="stat-num">2'):
                miss.append(a[:30])
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"{root[-10:]} {f}: {'変更あり' if new != s else '変更なし'} 未一致 {miss}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
