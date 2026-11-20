#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
料金欄に出典・時点の無かったコースページ (「目安」の範囲・春季料金など) を、じゃらん 18H 最安 (2026-11-20・税込総額) に揃える。
  平日カード・土日祝カード: ¥{総額}〜 と出典の注記 (JA/EN/KO)
  その他の金額入りカード: 確認できない値なので「予約サイトで確認」に (月曜セルフデー・メンバー参考・午後セルフ等)
  金額の無い情報カード (27H構成・PGM運営・設計者 等): そのまま
  料金欄の説明文: 統一文に置き換え (古い料金を含むため)
  予約カード・固定予約ボタン・予約欄の注記: fix_course_price_cards_2026_11.py と同じ規則
データ: scripts/.cache/jalan_floor.json (checked 2026-11-20 のものだけ使う)
冪等。改行コードはそのまま。Usage: python scripts/fix_course_price_cards_b_2026_11.py [--apply] [--only course-x.html]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = "C:/Users/Owner/fukuoka-golf-guide"
ROOTS = [REPO, "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
TARGETS = ["century", "chisan-onga", "jruchino", "kaho", "newui", "nishinihon", "pheasant", "satsuki-ryuoh", "satsuki-tenpai",
           "seitanomori", "suonada", "takaha", "yamejoyo", "fukuokakokusai", "ukiha"]
FLOOR = json.load(open(f"{REPO}/scripts/.cache/jalan_floor.json", encoding="utf-8"))
MAP = {c["file"][7:]: c["jalan_id"] for c in json.load(open(f"{REPO}/jalan_golf_mapping.json", encoding="utf-8"))["courses"] if c.get("jalan_id")}

T = {
    "ja": dict(desc="平日・土日祝の料金は、<strong>2026年11月時点のじゃらんゴルフの18ホール最安（税込総額）</strong>です。時期・プラン・カートや昼食の有無により変わるので、最新は予約サイトでご確認ください。",
               wk=("WEEKDAY", "平日"), we=("WEEKEND / HOLIDAY", "土日祝"),
               note="じゃらんゴルフの18ホール最安（2026年11月20日時点・税込総額）。プランにより昼食やカートの条件が違います。",
               other="予約サイトで確認", other_note="設定日・料金は予約サイトでご確認ください。"),
    "en": dict(desc="Weekday and weekend rates are the lowest 18-hole totals (incl. tax) on Jalan Golf as of November 2026. They vary by season, plan, cart and meal options — check the booking sites for current prices.",
               wk=("WEEKDAY", "Monday–Friday"), we=("WEEKEND / HOLIDAY", "Sat · Sun · Holidays"),
               note="Lowest 18-hole total on Jalan Golf (as of 20 Nov 2026, incl. tax). Meal and cart conditions differ by plan.",
               other="Check booking site", other_note="Check dates and prices on the booking site."),
    "ko": dict(desc="평일·주말 요금은 2026년 11월 시점 자란골프 18홀 최저가(세금 포함 총액)입니다. 시기·플랜·카트나 식사 유무에 따라 변동하므로 최신 요금은 예약 사이트에서 확인해 주세요.",
               wk=("WEEKDAY", "평일"), we=("WEEKEND / HOLIDAY", "토·일·공휴일"),
               note="자란골프 18홀 최저가 (2026년 11월 20일 기준·세금 포함 총액). 플랜에 따라 식사·카트 조건이 다릅니다.",
               other="예약 사이트에서 확인", other_note="설정일·요금은 예약 사이트에서 확인해 주세요."),
}
WK = re.compile(r"平日|Weekday|WEEKDAY|Monday–Friday|Mon–Fri|평일")  # 「Monday Self Day」(鷹羽の月曜セルフデー) は平日カードではない
WE = re.compile(r"土日|Weekend|WEEKEND|Sat|주말|토·일|토일")
CARD = re.compile(r'(<div class="price-card(?: featured)?">\s*<div class="price-card-head">\s*<div class="price-card-label">)(.*?)(</div>\s*<div class="price-card-name">)(.*?)(</div>.*?<div class="price-amount"[^>]*>)(.*?)(</div>\s*<div class="price-note">)(.*?)(</div>)', re.S)


def block_range(s, lang):
    i = s.find(f'id="c-{lang}"')
    j = min([x for x in (s.find('id="c-en"', i + 1), s.find('id="c-ko"', i + 1), len(s)) if x > i])
    return i, j


def fix_block(b, lang, wk, we):
    d = T[lang]
    a = b.find('<div class="sec-eyebrow">— Green Fees</div>')
    if a < 0:
        a = b.find('<div class="sec-eyebrow">— 그린피</div>')
    if a < 0:
        return b, 0
    e = b.find("</section>", a)
    sec, n = b[a:e], 0
    sec, k = re.subn(r'(<p class="sec-desc">).*?(</p>)', lambda m: m.group(1) + d["desc"] + m.group(2), sec, count=1, flags=re.S); n += k
    used = {"wk": False, "we": False}

    def card(m):
        nonlocal n
        label, name, amt = m.group(2), re.sub(r"<[^>]+>", "", m.group(4)), m.group(6)
        kind = None
        if WE.search(name + label) and not used["we"] and we:
            kind = "we"
        elif WK.search(name + label) and not WE.search(name) and not used["wk"]:
            kind = "wk"
        if kind:
            used[kind] = True
            lab, nm = d[kind]
            val = wk if kind == "wk" else we
            n += 1
            return (m.group(1) + lab + m.group(3) + nm + m.group(5) + f'<span class="yen">¥</span>{val:,}<span class="range">〜</span>'
                    + m.group(7) + d["note"] + m.group(9))
        if "¥" in amt:  # 確認できない金額
            n += 1
            return m.group(1) + m.group(2) + m.group(3) + m.group(4) + m.group(5).replace('class="price-amount"', 'class="price-amount" style="font-size:19px;"', 1) \
                .replace('style="font-size:19px;" style=', 'style=') + d["other"] + m.group(7) + d["other_note"] + m.group(9)
        return m.group(0)

    sec = CARD.sub(card, sec)
    return b[:a] + sec + b[e:], n


for root in ROOTS:
    print(root)
    for slug in TARGETS:
        f = f"course-{slug}.html"
        if ONLY and f != ONLY:
            continue
        rec = FLOOR.get(MAP.get(slug, ""), {})
        if rec.get("checked", "") < "2026-11-20" or not rec.get("weekday"):
            print(f"  {f}: 11/20 のデータなし → 飛ばす"); continue
        wk = rec["weekday"]["total"]
        we = rec["weekend"]["total"] if rec.get("weekend") else None
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        new, n = s, 0
        for lang in ("ja", "en", "ko"):
            i, j = block_range(new, lang)
            if i < 0:
                continue
            b, k = fix_block(new[i:j], lang, wk, we)
            new = new[:i] + b + new[j:]; n += k
        new, k = re.subn(r'(booking-price-tag">最安 <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new); n += k
        new, k = re.subn(r'(booking-price-tag">From <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new); n += k
        new, k = re.subn(r'(booking-price-tag">최저 <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new); n += k
        for pat in (r"(📅 じゃらん )¥[\d,]+(〜)", r"(📅 Jalan )¥[\d,]+(〜)", r"(📅 자란 )¥[\d,]+(〜)"):
            new, k = re.subn(pat, rf"\g<1>¥{wk:,}\2", new); n += k
        if we:
            for pat, rep in [
                (r"※じゃらん料金は2026年11月(?:1|20)日時点・直近2週間の平日18ホール最安（(?:総額¥[\d,]+|税込総額)）。土日祝は¥[\d,]+〜。",
                 f"※じゃらん料金は2026年11月20日時点・直近2週間の平日18ホール最安（税込総額）。土日祝は¥{we:,}〜。"),
                (r"\* Jalan rate is the lowest weekday 18-hole (?:plan|total \(incl\. tax\)) in the next two weeks as of 2026-11-(?:01|20)(?: \(total ¥[\d,]+\))?\. Weekends from ¥[\d,]+\.",
                 f"* Jalan rate is the lowest weekday 18-hole total (incl. tax) in the next two weeks as of 2026-11-20. Weekends from ¥{we:,}."),
                (r"※자란 요금은 2026년 11월 (?:1|20)일 기준 향후 2주간 평일 18홀 최저가\((?:총액 ¥[\d,]+|세금 포함 총액)\)\. 주말·공휴일은 ¥[\d,]+부터\.",
                 f"※자란 요금은 2026년 11월 20일 기준 향후 2주간 평일 18홀 최저가(세금 포함 총액). 주말·공휴일은 ¥{we:,}부터."),
            ]:
                new, k = re.subn(pat, rep, new); n += k
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {f}: 平日 ¥{wk:,} / 土日祝 {f'¥{we:,}' if we else 'なし'}  ({n}){' (変更なし)' if new == s else ''}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
