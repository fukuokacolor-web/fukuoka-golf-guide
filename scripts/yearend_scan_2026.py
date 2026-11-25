#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
年末年始 (2026-12-29〜2027-01-03) に、じゃらん・楽天GORAで予約できる 18H プランの日別最安を集める。読み取り専用。
  じゃらん: jalan_floor.py の fetch/parse (日付ページ・18H判定・コンペ/年齢限定の除外も同じ)。その日付の ymd を持つプランだけ数える
  楽天GORA: gora_floor.py の fetch/parse (12月のカレンダー1枚に12月+1月)。○●☆ = 空き。□ (リクエストのみ) は別に記録
  CLAUDE.md §9.4 の除外 (予約サイトで予約できないコース) は、そのサイト分を取らない。
出力: scripts/.cache/yearend_2026.json と標準出力の表。
Usage: python scripts/yearend_scan_2026.py [--only slug,slug]
"""
import datetime, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import jalan_floor as J  # noqa: E402
import gora_floor as G   # noqa: E402

ROOT = os.path.dirname(HERE)
DATES = [datetime.date(2026, 12, 29) + datetime.timedelta(days=k) for k in range(6)]
NO_JALAN = {"fukuokacc", "wakamatsu", "genkai", "aburayama", "koga", "moji", "kyushugc", "classic", "saitozaki", "akane",
            "yasukogen", "sunlake", "kokura", "queenshill", "raizan", "keya"}
NO_RAKUTEN = {"fukuokacc", "wakamatsu", "genkai", "koga", "moji", "classic", "kokura", "queenshill", "raizan", "keya"}
ONLY = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None

jal = {c["file"].replace("course-", ""): c["jalan_id"] for c in json.load(open(os.path.join(ROOT, "jalan_golf_mapping.json"), encoding="utf-8"))["courses"]}
rak = {c["file"].replace("course-", ""): c["c_id"] for c in json.load(open(os.path.join(ROOT, "rakuten_gora_mapping.json"), encoding="utf-8"))["courses"]}
slugs = sorted(set(jal) | set(rak))
OUT = os.path.join(HERE, ".cache", "yearend_2026.json")
# じゃらんの日付ページは jalan_<id>_<日付>.html で保存され取得日を含まないので、取り直すたびに消す (古い空きを使わない)
if "--keep-cache" not in sys.argv:
    for d in DATES:
        for f in __import__("glob").glob(os.path.join(HERE, ".cache", f"jalan_*_{d:%Y%m%d}.html")):
            os.remove(f)
res = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}

for slug in slugs:
    if ONLY and slug not in ONLY:
        continue
    r = {"jalan": {}, "rakuten": {}, "rakuten_request": {}}
    jid = jal.get(slug)
    if jid and slug not in NO_JALAN:
        for d in DATES:
            p = J.parse(J.fetch(jid, d))
            b = p["best"]
            if b and b["ymd"] == f"{d:%Y%m%d}":
                r["jalan"][d.isoformat()] = dict(total=b["total"], price=b["price"], name=b["name"][:60])
    cid = rak.get(slug)
    if cid and slug not in NO_RAKUTEN:
        _, plans = G.parse(G.fetch(cid, 2026, 12))
        for pid, v in plans.items():
            if v["half"]:
                continue
            for d in DATES:
                ds = d.isoformat()
                if ds in v["days"] and (ds not in r["rakuten"] or v["total"] < r["rakuten"][ds]["total"]):
                    r["rakuten"][ds] = dict(total=v["total"], name=v["name"][:60], plan_id=pid)
                if ds in v["req"] and (ds not in r["rakuten_request"] or v["total"] < r["rakuten_request"][ds]["total"]):
                    r["rakuten_request"][ds] = dict(total=v["total"], name=v["name"][:60], plan_id=pid)
    r["checked"] = datetime.date.today().isoformat()
    res[slug] = r
    cell = lambda ds: ("J" if ds in r["jalan"] else "-") + ("R" if ds in r["rakuten"] else ("r" if ds in r["rakuten_request"] else "-"))
    print(f"{slug:16}", " ".join(cell(d.isoformat()) for d in DATES), flush=True)
    json.dump(res, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("dates:", " ".join(f"{d:%m/%d}" for d in DATES), "| J=じゃらん空き R=楽天空き r=楽天リクエストのみ")
