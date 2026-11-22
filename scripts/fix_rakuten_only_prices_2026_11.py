#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天でしか予約できない 5 コースの料金欄を、楽天GORAの予約カレンダー (2026-11-22 確認) の数字にする。3言語。
  データ: scripts/gora_floor.py 400053 400012 400020 400001 400048 --days 39 (11/23〜12/31・18H・空きのあるプランの税込総額)
          + 1〜2月のカレンダー (夜須高原の冬季・あかねの1〜2月料金)
  サンレイク 400053: 平日 通常セルフ¥9,000・完全セルフDAY(昼食付・12/14・21・24)¥8,500 / 土日祝 通常¥17,500・11/23(祝)特別¥12,500
                    (旧表記 平日¥10,000 は出典なし)
  九州GC 400012   : 平日キャディ付¥19,200 のみ・すべてリクエスト予約 (□)。土日祝は楽天に出ていない
  西戸崎 400020   : 平日 カート・昼食付セルフ¥14,110・月曜営業日¥12,060。土日祝は楽天に出ていない
  あかね 400001   : 平日 12月¥16,000・1〜2月¥12,000 / 土日祝 12月¥22,000・1〜2月¥17,000
  夜須高原 400048 : 平日¥10,510 / 土日祝 通常¥18,100・12/31 年末特別¥15,020 / 1〜2月 平日¥9,980〜・土日祝¥15,900 (旧表記¥9,510 は今は無い)
  九州GC・西戸崎の「午後スルー 設定日限定・コスパ最強」カードは楽天にそのプランが無い → カードごと外す。
  楽天で販売なしの土日祝カードのボタンは公式サイトへ (九州GC・西戸崎)。
  韓国語のウォン換算 (약 ○만원) は為替依存・出典なし → 外す。
冪等。改行コードはそのまま。Usage: python scripts/fix_rakuten_only_prices_2026_11.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
WON = re.compile(r' ?<span style="color:#1a3a8f;font-size:0\.78rem;">\(약 [^)]*\)</span>')
WON_WRAP = re.compile(r' ?<span style="color:var\(--ocean\);font-size:12px;"><span style="color:#1a3a8f;font-size:0\.78rem;">\(약 [^)]*\)</span></span>')

SRC = {"ja": "楽天GORA・2026年11月22日確認（税込総額）。",
       "en": "Rakuten GORA, checked 22 Nov 2026 (total incl. tax). ",
       "ko": "라쿠텐 GORA · 2026년 11월 22일 확인 (세금 포함 총액). "}
DESC = {
    "ja": "下記は楽天GORAの予約カレンダーで2026年11月22日に確認した18ホールの料金です（税込総額・11月23日〜12月31日に空きのあったプラン）。日によって変わるので、予約時に楽天GORAでご確認ください。",
    "en": "Rates below are 18-hole totals incl. tax from the Rakuten GORA booking calendar, checked 22 Nov 2026 (plans with open slots between 23 Nov and 31 Dec). They change by date — confirm on Rakuten GORA when booking.",
    "ko": "아래는 2026년 11월 22일 라쿠텐 GORA 예약 캘린더에서 확인한 18홀 요금입니다 (세금 포함 총액·11월 23일〜12월 31일에 빈자리가 있던 플랜). 날짜에 따라 바뀌므로 예약할 때 라쿠텐 GORA에서 확인하세요.",
}
OLD_DESC_GENERIC = {
    "ja": "平日・土日祝の料金は時期・プラン・カートや昼食の有無により変動します。最新の料金と空き状況は楽天GORAでご確認ください。",
    "en": "Weekday and weekend rates vary by season, plan, cart and meal options. Check Rakuten GORA for current rates and availability.",
    "ko": "평일·주말 요금은 시즌·플랜에 따라 변동합니다. 최신 요금과 빈자리는 라쿠텐 GORA에서 확인해 주세요.",
}
OLD_DESC_PLAN = {
    "ja": "下記はビジター料金の目安です。カートフィー・ゴルフ場利用税・消費税込み。最新料金・空き状況は公式サイトまたは予約サイトでご確認ください。",
    "en": "Visitor fee guide below — rates include cart fee, golf tax, and consumption tax. Confirm current rates and availability on the official site or booking platform.",
    "ko": "아래는 비지터 요금 기준입니다. 카트피·골프장 이용세·소비세 포함. 최신 요금·빈자리는 공식 사이트 또는 예약 사이트에서 확인해 주세요.",
}
Y = lambda a, b="": f'<span class="yen">¥</span>{a}<span class="range">{b}</span>'
NONE = {"ja": '<span style="font-size:19px;">楽天では販売なし</span>', "en": '<span style="font-size:19px;">Not on Rakuten</span>',
        "ko": '<span style="font-size:19px;">라쿠텐 판매 없음</span>'}
NONE_NOTE = {"ja": "土日祝のプランは楽天GORAに出ていません（11月〜2月）。予約方法は公式サイトでご確認ください。",
             "en": "No weekend/holiday plans on Rakuten GORA (Nov–Feb). Check the official website for how to book.",
             "ko": "주말·공휴일 플랜은 라쿠텐 GORA에 없습니다 (11월〜2월). 예약 방법은 공식 사이트에서 확인하세요."}

# card label (per lang) -> (amount_html, note)
CARDS = {
    "course-sunlake.html": {
        "ビジター平日 セルフ": (Y("8,500", "〜9,000"), "通常の平日セルフは¥9,000。昼食付の完全セルフDAY（12/14・21・24など）は¥8,500。"),
        "ビジター土日祝 セルフ": (Y("17,500"), "通常の土日祝セルフ。11/23（祝）は特別料金¥12,500のプランもありました。"),
        "Visitor Weekday (Self)": (Y("8,500", "–9,000"), "Regular weekday self-play ¥9,000; ¥8,500 with lunch on 'self-only days' (e.g. 14, 21, 24 Dec)."),
        "Visitor Weekend (Self)": (Y("17,500"), "Regular weekend/holiday self-play. A ¥12,500 special plan was offered on 23 Nov (holiday)."),
        "비지터 평일 셀프": (Y("8,500", "〜9,000"), "평일 셀프는 ¥9,000. 점심 포함 '완전 셀프 데이'(12/14·21·24 등)는 ¥8,500."),
        "비지터 토·일·공휴일 셀프": (Y("17,500"), "토·일·공휴일 셀프 기본 요금. 11/23(공휴일)은 ¥12,500 특별 플랜도 있었습니다."),
    },
    "course-kyushugc.html": {
        "平日": (Y("19,200"), "平日キャディ付。楽天GORAではリクエスト予約のみ（空きはゴルフ場が確認して返答）。"),
        "土日祝": (NONE["ja"], NONE_NOTE["ja"]),
        "Monday–Friday": (Y("19,200"), "Weekday with caddie. Request-only booking on Rakuten GORA (the course confirms availability)."),
        "Sat · Sun · Holidays": (NONE["en"], NONE_NOTE["en"]),
        "평일": (Y("19,200"), "평일 캐디 포함. 라쿠텐 GORA에서는 리퀘스트 예약만 가능 (골프장이 확인 후 회신)."),
        "토·일·공휴일": (NONE["ko"], NONE_NOTE["ko"]),
    },
    "course-saitozaki.html": {
        "平日": (Y("12,060", "〜14,110"), "カート・昼食付セルフ。通常の平日は¥14,110、月曜営業日は¥12,060。"),
        "土日祝": (NONE["ja"], NONE_NOTE["ja"]),
        "Monday–Friday": (Y("12,060", "–14,110"), "Self-play with cart and lunch. ¥14,110 on regular weekdays, ¥12,060 on Monday opening days."),
        "Sat · Sun · Holidays": (NONE["en"], NONE_NOTE["en"]),
        "평일": (Y("12,060", "〜14,110"), "카트·점심 포함 셀프. 평일 ¥14,110, 월요일 영업일 ¥12,060."),
        "토·일·공휴일": (NONE["ko"], NONE_NOTE["ko"]),
    },
    "course-akane.html": {
        "平日": (Y("12,000", "〜16,000"), "セルフ。12月は¥16,000、1〜2月は¥12,000。"),
        "土日祝": (Y("17,000", "〜22,000"), "セルフ。12月は¥22,000、1〜2月は¥17,000。"),
        "Monday–Friday": (Y("12,000", "–16,000"), "Self-play. ¥16,000 in December, ¥12,000 in January–February."),
        "Sat · Sun · Holidays": (Y("17,000", "–22,000"), "Self-play. ¥22,000 in December, ¥17,000 in January–February."),
        "평일": (Y("12,000", "〜16,000"), "셀프. 12월 ¥16,000, 1〜2월 ¥12,000."),
        "토·일·공휴일": (Y("17,000", "〜22,000"), "셀프. 12월 ¥22,000, 1〜2월 ¥17,000."),
    },
    "course-yasukogen.html": {
        "平日（ビジター）": (Y("10,510"), "平日セルフデーの料金（12月）。"),
        "土日祝（ビジター）": (Y("15,020", "〜18,100"), "通常の土日祝セルフは¥18,100。12/31の年末特別営業は¥15,020。"),
        "冬季（1-2月）": (Y("9,980", "〜15,900"), "1〜2月は平日¥9,980〜、土日祝¥15,900（1/2の年始特別営業は¥15,020）。"),
        "Weekdays (Visitor)": (Y("10,510"), "Weekday 'self-play day' rate (December)."),
        "Weekends / Holidays (Visitor)": (Y("15,020", "–18,100"), "Regular weekend self-play ¥18,100; year-end special on 31 Dec ¥15,020."),
        "Winter (Jan-Feb)": (Y("9,980", "–15,900"), "Jan–Feb: weekdays from ¥9,980, weekends ¥15,900 (New Year special on 2 Jan ¥15,020)."),
        "평일 (비지터)": (Y("10,510"), "평일 셀프 데이 요금 (12월)."),
        "토·일·공휴일 (비지터)": (Y("15,020", "〜18,100"), "토·일·공휴일 셀프 기본 ¥18,100. 12/31 연말 특별 영업 ¥15,020."),
        "동계 (1-2월)": (Y("9,980", "〜15,900"), "1〜2월은 평일 ¥9,980〜, 주말 ¥15,900 (1/2 연초 특별 영업 ¥15,020)."),
    },
}
OFFICIAL = {"course-kyushugc.html": "http://kg-yahata.com/", "course-saitozaki.html": "http://www.saitozaki.com/"}
OFF_LABEL = {"ja": "🏛️ 公式サイトで確認 →", "en": "🏛️ Check the official website →", "ko": "🏛️ 공식 사이트에서 확인 →"}
DROP_CARD = {"course-kyushugc.html": ["午後スルー", "Weekday Afternoon", "오후 스루"],
             "course-saitozaki.html": ["午後スルー", "Weekday Afternoon", "오후 스루"]}
FOOT = {  # sunlake / yasukogen の補足
    "上記はカートフィー・ゴルフ場利用税・消費税込みのビジター料金の目安です。2名プレー割増・キャディ付プラン・季節料金など詳細は公式サイトまたは予約サイトでご確認ください。":
        "上記は楽天GORAの予約カレンダーで2026年11月22日に確認した税込総額です。2名・3名の割増やプランの条件は、楽天GORAの各プランの説明でご確認ください。",
    "Rates above include cart fee, golf tax, and consumption tax (visitor estimate). 2-player surcharges, caddie plans, and seasonal rates may apply — see the official site or booking platform for details.":
        "Rates above are totals incl. tax from the Rakuten GORA booking calendar, checked 22 Nov 2026. See each plan on Rakuten GORA for 2-/3-player surcharges and conditions.",
    "위 요금은 카트피·골프장 이용세·소비세 포함 비지터 요금 기준입니다. 2인 플레이 할증·캐디 포함 플랜·시즌 요금 등 상세는 공식 사이트 또는 예약 사이트에서 확인해 주세요.":
        "위 요금은 2026년 11월 22일 라쿠텐 GORA 예약 캘린더에서 확인한 세금 포함 총액입니다. 2인·3인 할증과 플랜 조건은 라쿠텐 GORA의 각 플랜 설명에서 확인하세요.",
}
CARD_RE = re.compile(r'(?P<indent>[ \t]*)<div class="price-card(?: featured)?">\r?\n(?:(?!<div class="price-card(?: featured)?">).)*?'
                     r'<div class="price-card-cta">.*?</div>\r?\n[ \t]*</div>\r?\n(?:\r?\n)?', re.S)


def lang_of(s, pos):
    m = list(re.finditer(r'id="c-(ja|en|ko)"', s[:pos]))
    return m[-1].group(1) if m else "ja"


def fix(f, s):
    log = []
    for lang in ("ja", "en", "ko"):
        for old in (OLD_DESC_GENERIC[lang], OLD_DESC_PLAN[lang]):
            if old in s:
                s = s.replace(old, DESC[lang]); log.append(f"desc-{lang}")
    for a, b in FOOT.items():
        if a in s:
            s = s.replace(a, b); log.append("foot")
    out, last = [], 0
    for m in CARD_RE.finditer(s):
        block = m.group(0)
        name = re.search(r'price-card-name">(.*?)</div>', block)
        name = name.group(1) if name else ""
        if name in DROP_CARD.get(f, []):
            out.append(s[last:m.start()]); last = m.end(); log.append(f"drop:{name}"); continue
        if name in CARDS.get(f, {}):
            amt, note = CARDS[f][name]
            lang = lang_of(s, m.start())
            new = re.sub(r'<div class="price-amount"[^>]*>.*?</div>', lambda _: f'<div class="price-amount">{amt}</div>', block, count=1, flags=re.S)
            new = re.sub(r'<div class="price-note">.*?</div>', lambda _: f'<div class="price-note">{note}{"" if lang != "ja" else ""}</div>', new, count=1, flags=re.S)
            if amt in NONE.values() and f in OFFICIAL:  # 楽天で販売なしのカードは予約ボタンを公式サイトに
                new = re.sub(r'<a href="[^"]*" class="btn-book btn-rakuten"[^>]*>[^<]*</a>',
                             lambda _: f'<a href="{OFFICIAL[f]}" class="btn-book" target="_blank" rel="noopener" '
                                       f"onclick=\"if(window.trackAffiliate)trackAffiliate('official',document.title,'{lang}','price-card')\">{OFF_LABEL[lang]}</a>",
                             new, count=1)
            if new != block:
                log.append(f"card:{name}")
            out.append(s[last:m.start()] + new); last = m.end()
    s = "".join(out) + s[last:]
    s2 = WON_WRAP.sub("", s); s2 = WON.sub("", s2)
    if s2 != s:
        log.append("won")
    return s2, log


for root in ROOTS:
    for f in CARDS:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, log = fix(f, s)
        names = [x for x in log if x.startswith("card:")]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        print(root[-10:], f, f"cards={len(names)}", [x for x in log if not x.startswith("card:")])
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
