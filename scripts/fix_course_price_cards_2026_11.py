#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースページの料金カードと予約カードの金額を、じゃらんの直近14日 (2026-11-20〜12-03) の 18H 最安に更新する (2026-11-20)。
  データ: scripts/.cache/jalan_floor.json (scripts/jalan_floor.py の出力)。表示は **税込総額** (これまでのプラン料金 ¥X は
          実際に払う額より安く見えるため総額に統一)。
  対象: 料金欄に「2026年7月時点のじゃらんゴルフ調べ」と書かれたページ (18件)。平日・土日祝カードと予約カード (最安 ¥X〜) を
        JA/EN/KO で更新し、時点の表記を 2026年11月 に。午後スルー等その他のカードは触らない。
  予約できないコース・楽天のみのコースは対象外 (CLAUDE.md §9.4)。データが無い場合はそのページを飛ばす。
冪等 (同じ値なら変更なし)。改行コードはそのまま。
Usage: python scripts/fix_course_price_cards_2026_11.py [--apply] [--only course-ariake.html]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = "C:/Users/Owner/fukuoka-golf-guide"
ROOTS = [REPO, "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

FLOOR = json.load(open(f"{REPO}/scripts/.cache/jalan_floor.json", encoding="utf-8"))
MAP = {c["file"] + ".html": c["jalan_id"] for c in json.load(open(f"{REPO}/jalan_golf_mapping.json", encoding="utf-8"))["courses"] if c.get("jalan_id")}

DESC = {
    "<strong>2026年7月時点のじゃらんゴルフ調べ</strong>の最安値で": "<strong>2026年11月時点のじゃらんゴルフの18ホール最安（税込総額）</strong>で",
    "Figures are the lowest rates found on Jalan Golf as of July 2026": "Figures are the lowest 18-hole totals (incl. tax) on Jalan Golf as of November 2026",
    "게재 요금은 2026년 7월 시점 자란골프 기준 최저가이며": "게재 요금은 2026년 11월 시점 자란골프 18홀 최저가(세금 포함 총액)이며",
}
CARD_NAMES = {"wk": ["平日", "Monday–Friday", "평일"], "we": ["土日祝", "Sat · Sun · Holidays", "토·일·공휴일"]}


def total(rec, key):
    v = rec.get(key)
    if not v:
        return None
    return v.get("total") or v.get("total_price") or None


def set_card(s, name, amount):
    """price-card-name が name のカードの price-amount を ¥amount〜 に"""
    pat = re.compile(r'(<div class="price-card-name">' + re.escape(name) + r'</div>.*?<div class="price-amount"[^>]*>)(.*?)(</div>)', re.S)
    new_amt = f'<span class="yen">¥</span>{amount:,}<span class="range">〜</span>'
    return pat.subn(lambda m: m.group(1) + new_amt + m.group(3), s, count=1)


for root in ROOTS:
    print(root)
    for f in sorted(os.listdir(root)):
        if not f.startswith("course-") or (ONLY and f != ONLY):
            continue
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if "2026年7月時点のじゃらんゴルフ調べ" not in s and "2026年11月時点のじゃらんゴルフの18ホール最安" not in s:
            continue
        rec = FLOOR.get(MAP.get(f, ""), {})
        if rec.get("checked", "") < "2026-11-20":
            print(f"  {f}: 11/20 のデータが無い → 飛ばす"); continue
        wk, we = total(rec, "weekday"), total(rec, "weekend")
        if not wk:
            print(f"  {f}: データなし → 飛ばす"); continue
        new, n = s, 0
        for a, b in DESC.items():
            if a in new:
                new = new.replace(a, b); n += 1
        for nm in CARD_NAMES["wk"]:
            new, k = set_card(new, nm, wk); n += k
        if we:
            for nm in CARD_NAMES["we"]:
                new, k = set_card(new, nm, we); n += k
        new, k1 = re.subn(r'(booking-price-tag">最安 <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new)
        new, k2 = re.subn(r'(booking-price-tag">From <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new)
        new, k3 = re.subn(r'(booking-price-tag">최저 <span class="big">)¥[\d,]+(</span>)', rf"\g<1>¥{wk:,}\2", new)
        n += k1 + k2 + k3
        # 画面下の固定予約ボタン (sticky) と予約欄の注記 (11/1 時点・総額) も同じ値に
        for pat in (r"(📅 じゃらん )¥[\d,]+(〜)", r"(📅 Jalan )¥[\d,]+(〜)", r"(📅 자란 )¥[\d,]+(〜)"):
            new, k = re.subn(pat, rf"\g<1>¥{wk:,}\2", new); n += k
        if we:
            notes = [
                (r"※じゃらん料金は2026年11月(?:1|20)日時点・直近2週間の平日18ホール最安（(?:総額¥[\d,]+|税込総額)）。土日祝は¥[\d,]+〜。",
                 f"※じゃらん料金は2026年11月20日時点・直近2週間の平日18ホール最安（税込総額）。土日祝は¥{we:,}〜。"),
                (r"\* Jalan rate is the lowest weekday 18-hole (?:plan|total \(incl\. tax\)) in the next two weeks as of 2026-11-(?:01|20)(?: \(total ¥[\d,]+\))?\. Weekends from ¥[\d,]+\.",
                 f"* Jalan rate is the lowest weekday 18-hole total (incl. tax) in the next two weeks as of 2026-11-20. Weekends from ¥{we:,}."),
                (r"※자란 요금은 2026년 11월 (?:1|20)일 기준 향후 2주간 평일 18홀 최저가\((?:총액 ¥[\d,]+|세금 포함 총액)\)\. 주말·공휴일은 ¥[\d,]+부터\.",
                 f"※자란 요금은 2026년 11월 20일 기준 향후 2주간 평일 18홀 최저가(세금 포함 총액). 주말·공휴일은 ¥{we:,}부터."),
            ]
            for pat, rep in notes:
                new, k = re.subn(pat, rep, new); n += k
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        old_wk = re.search(r'<div class="price-card-name">平日</div>.*?<div class="price-amount"[^>]*>.*?¥</span>([\d,]+)', s, re.S)
        print(f"  {f}: 平日 {old_wk.group(1) if old_wk else '?'} → {wk:,} / 土日祝 → {we and f'{we:,}'}  ({n} 箇所){' (変更なし)' if new == s else ''}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
