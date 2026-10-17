#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/jalan_floor.py の結果 (scripts/.cache/jalan_floor.json) から、
fix_booking_price_tags.py 用の検証データ JSON を作る。

TARGETS の old は「いまページに出ている額」。点検のたびに前回の new へ更新すること。
Usage:
  python scripts/build_price_audit.py price_audit_2026-10.json
"""
import sys, json, pathlib

CACHE = pathlib.Path(__file__).parent / ".cache" / "jalan_floor.json"

# slug: (jalan gc id, いまページに出ている額)   ※ gc id が None = じゃらん除外 (§9.4)
TARGETS = {
    "ariake": ("02315", "¥4,000"), "central": ("02322", "¥4,000"), "lakeside": ("02346", "¥4,000"),
    "moonlake": ("02339", "¥4,000"), "nijo": ("02350", "¥4,000"), "ogori": ("02321", "¥4,000"),
    "wakamiya": ("02341", "¥4,000"), "chikushigaoka": ("02333", "¥6,000"), "chikushino": ("02324", "¥6,000"),
    "daihakata": ("02332", "¥6,000"), "hisayama": ("02334", "¥6,000"), "koga": ("02331", "¥6,000"),
    "moji": ("02307", "¥6,000"), "asoiizuka": ("02343", "¥9,000"), "ito": ("02329", "¥9,000"),
    "kyushugc": ("02310", "¥8,000"), "mission": ("02338", "¥3,000"), "sevenmillion": ("02314", "¥5,000"),
    "shimaseaside": ("02352", "¥19,000"), "kokura": ("02309", "¥15,000"),
    "kurume": ("02356", "¥6,137"), "queenshill": ("02328", "¥19,305"),   # 2026-09 是正済 → 最新値へ更新
    "aburayama": (None, "¥5,000"),
}


def yen(n):
    return f"¥{n:,}"


def note_for(wk, we, checked):
    y, m, d = checked.split("-")
    ja = f"※じゃらん料金は{y}年{int(m)}月{int(d)}日時点・直近2週間の平日18ホール最安（総額{yen(wk['total'])}）。"
    en = f"* Jalan rate is the lowest weekday 18-hole plan in the next two weeks as of {checked} (total {yen(wk['total'])})."
    ko = f"※자란 요금은 {y}년 {int(m)}월 {int(d)}일 기준 향후 2주간 평일 18홀 최저가(총액 {yen(wk['total'])})."
    if we:
        ja += f"土日祝は{yen(we['price'])}〜。"
        en += f" Weekends from {yen(we['price'])}."
        ko += f" 주말·공휴일은 {yen(we['price'])}부터."
    ja += "時期・プランにより変動するため、最新は予約サイトでご確認ください。"
    en += " Rates vary by season and plan — check the booking site for current prices."
    ko += " 시기·플랜에 따라 변동됩니다."
    return {"ja": ja, "en": en, "ko": ko}


def main():
    fl = json.loads(CACHE.read_text(encoding="utf-8"))
    out = {"_meta": {"source": "じゃらんゴルフ gc ページ・直近14日の18ホールプラン最安 (ハーフ/薄暮/ナイト除外)",
                     "rakuten": "楽天GORAは料金が動的読込で機械検証不可 → 楽天カードは金額を外す"}}
    for slug, (jid, old) in TARGETS.items():
        r = fl.get(jid) if jid else None
        wk, we = (r or {}).get("weekday"), (r or {}).get("weekend")
        spec = {"old": old, "new": yen(wk["price"]) if wk else None, "note": None,
                "evidence": "じゃらん除外(§9.4)・楽天のみ=機械検証不可" if not jid else
                            (f"じゃらんに直近{r['period']}の18H販売プラン無し" if not wk else
                             {"checked": r["checked"], "period": r["period"],
                              "weekday": [wk["price"], wk["total"], wk["ymd"], wk["name"]],
                              "weekend": [we["price"], we["total"], we["ymd"], we["name"]] if we else None})}
        if wk:
            spec["note"] = note_for(wk, we, r["checked"])
        out[slug] = spec
        print(f"{slug:14} {old:>8} → {spec['new'] or '金額を外す':>10}"
              + (f" | 土日祝 {yen(we['price'])}〜" if we else ""))
    pathlib.Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
