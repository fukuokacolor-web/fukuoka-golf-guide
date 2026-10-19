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

# slug: (jalan gc id, いまページの予約カード/sticky に出ている額)
# 2026-10-18 反映後の状態。点検のたびに、反映した new をここの old へ書き戻すこと。
# old が None = 現在は金額を出していない (確認できず外した) コース。今月じゃらんで料金が取れたら
#               「再掲候補」としてレポートするだけで、自動では戻さない (金額を足す処理は手作業で確認する)。
# 対象外: koga / moji (じゃらん・楽天とも予約不可 → 公式導線) / aburayama (楽天のみ) / kyushugc (じゃらん予約不可 → 楽天のみ)
TARGETS = {
    "ariake": ("02315", "¥6,773"), "central": ("02322", "¥5,869"), "lakeside": ("02346", "¥7,150"),
    "moonlake": ("02339", "¥7,273"), "nijo": ("02350", "¥6,778"), "ogori": ("02321", "¥14,546"),
    "wakamiya": ("02341", "¥10,455"), "chikushigaoka": ("02333", "¥13,150"), "chikushino": ("02324", "¥9,978"),
    "daihakata": ("02332", "¥7,696"), "hisayama": ("02334", "¥8,564"), "asoiizuka": ("02343", "¥9,182"),
    "ito": ("02329", "¥16,378"), "mission": ("02338", "¥9,455"), "sevenmillion": ("02314", "¥8,600"),
    "kurume": ("02356", "¥7,210"),
    "shimaseaside": ("02352", None), "kokura": ("02309", None), "queenshill": ("02328", None),
}
# course ページ以外で手書きしている料金 (スクリプト対象外・レポートで差分だけ知らせる)
MANUAL = {"kaho (hub-beginner.html のカード)": ("02347", "¥5,869")}


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
        if old is None:  # 現在は金額を出していない
            if wk:
                print(f"{slug:14} {'(金額なし)':>8} → 再掲候補 {yen(wk['price'])}（じゃらんで販売再開・手動で確認して再掲）")
            continue
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
    for label, (jid, shown) in MANUAL.items():
        wk = (fl.get(jid) or {}).get("weekday")
        print(f"[手書き] {label}: 表示 {shown} / 今月 {yen(wk['price']) if wk else '取得不可'}"
              + ("" if wk and yen(wk["price"]) == shown else "  ← 要更新"))
    pathlib.Path(sys.argv[1]).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
