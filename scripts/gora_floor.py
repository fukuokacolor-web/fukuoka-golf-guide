#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天GORA の予約カレンダーから、直近 N 日間の「18ホールプラン最安 (税込総額)」を平日/土日祝別に機械抽出する。
jalan_floor.py の楽天版。楽天でしか予約できないコース (サンレイク・九州GC・西戸崎・あかね・夜須高原) の料金確認用。
読み取り専用 (サイトのファイルは触らない)。

- カレンダー: https://search.gora.golf.rakuten.co.jp/cal/disp/c_id/{c_id}/select_year/{Y}/select_month/{M}/no_cache/1
  (1ページに当月+翌月。文字コードは EUC-JP)
- 各プラン行 <tr id="{plan_id}" fee="{税込総額}"> の日付セルの記号: ○/● = 空き有り (集計対象)・□ = リクエスト予約のみ (別枠)・△ キャンセル待ち・− 予約不可
- 楽天は空き枠が少ないので、楽天のみコースは --days を翌月末までにして使う (2026-11-22 は 39 日 = 11/23〜12/31)
- 18H 判定・除外語は jalan_floor.py と同じ (ハーフプレー/9H/薄暮/コンペ/年齢・属性限定 等。「ハーフ休憩」は18Hなので残す)
- 料金はページ表示の「総額」(= fee 属性)。じゃらんの総額と同じ基準 (税込・利用税込)

Usage:
  python scripts/gora_floor.py 400053 400012 ...     # 結果は標準出力 + scripts/.cache/gora_floor.json
  python scripts/gora_floor.py 400053 --days 7
"""
import re, sys, json, time, datetime, pathlib, subprocess

sys.stdout.reconfigure(encoding="utf-8")
CACHE = pathlib.Path(__file__).parent / ".cache"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
EXCL_NAME = re.compile(r"ハーフプレー|ハーフラウンド|ハーフのみ|午後ハーフ|早朝ハーフ|朝ハーフ|9H|９Ｈ|9ホール|９ホール|薄暮|ナイター|ナイト|1\.5R|練習"
                       r"|コンペ|[0-9０-９]+代|学生|シニア|レディース|女性|ジュニア|会員|メンバー")
HOLIDAYS = {"2026-11-03", "2026-11-23", "2026-12-31", "2027-01-01", "2027-01-02", "2027-01-03", "2027-01-11", "2027-02-11", "2027-02-23"}
WD = "月火水木金土日"


def fetch(cid, y, m):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / f"gora_{cid}_{y}{m:02d}_{datetime.date.today():%Y%m%d}.html"
    if not p.exists() or p.stat().st_size < 10000:
        url = f"https://search.gora.golf.rakuten.co.jp/cal/disp/c_id/{cid}/select_year/{y}/select_month/{m}/no_cache/1"
        subprocess.run(["curl", "-sL", "-A", UA, "-o", str(p), url], check=True)
        time.sleep(1.2)  # 先方サーバへの配慮
    return p.read_bytes().decode("euc_jp", errors="replace")


def parse(t):
    title = re.search(r"<title>([^<]+)", t)
    out = {}
    for pid, attrs, body in re.findall(r'<tr id="(\d+)"([^>]*\bfee="\d+"[^>]*)>(.*?)</tr>', t, re.S):
        fee = int(re.search(r'fee="(\d+)"', attrs).group(1))
        nm = re.search(r'class="planName[^"]*"[^>]*>(.*?)</td>', body, re.S)
        name = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", nm.group(1))).strip() if nm else ""
        cells = re.findall(r'<td id="%s-(\d{4}-\d\d-\d\d)" class="[^"]*cal">(.*?)</td>' % pid, body, re.S)
        mark = {d: re.sub(r"<[^>]+>|\s", "", c) or ("☆" if 'day="' in c else "") for d, c in cells}
        days = [d for d, m in mark.items() if m in ("○", "●", "☆")]  # 空き有り (☆ = おすすめプランの星アイコン + 予約リンク)
        req = [d for d, m in mark.items() if m == "□"]               # リクエスト予約のみ
        out[pid] = dict(name=name, total=fee, days=days, req=req, half=bool(EXCL_NAME.search(name)))
    return (title.group(1).strip() if title else None), out


def scan(cid, days=14):
    start = datetime.date.today() + datetime.timedelta(days=1)
    end = start + datetime.timedelta(days=days - 1)
    months = sorted({(d.year, d.month) for d in (start, end)})
    title, plans = None, {}
    for y, m in months:
        t, p = parse(fetch(cid, y, m))
        title = title or t
        for pid, v in p.items():
            if pid in plans:
                plans[pid]["days"] = sorted(set(plans[pid]["days"]) | set(v["days"]))
                plans[pid]["req"] = sorted(set(plans[pid]["req"]) | set(v["req"]))
            else:
                plans[pid] = v
    wk = we = rq = None
    seen = set()
    for pid, v in plans.items():
        if v["half"]:
            continue
        for ds in v["req"]:
            if start <= datetime.date.fromisoformat(ds) <= end and (rq is None or v["total"] < rq["total"]):
                rq = dict(name=v["name"], total=v["total"], ymd=ds.replace("-", ""), plan_id=pid)
        for ds in v["days"]:
            d = datetime.date.fromisoformat(ds)
            if not (start <= d <= end):
                continue
            seen.add(ds)
            b = dict(name=v["name"], total=v["total"], ymd=d.strftime("%Y%m%d"), dow=WD[d.weekday()], plan_id=pid)
            if d.weekday() >= 5 or ds in HOLIDAYS:
                we = b if we is None or b["total"] < we["total"] else we
            else:
                wk = b if wk is None or b["total"] < wk["total"] else wk
    return dict(title=title, checked=datetime.date.today().isoformat(), period=f"{start}/{end}",
                days_with_plans=len(seen), weekday=wk, weekend=we, request_only=rq)


def main():
    args = sys.argv[1:]
    days = int(args[args.index("--days") + 1]) if "--days" in args else 14
    ids = [a for i, a in enumerate(args) if a.isdigit() and not (i and args[i - 1] == "--days")]
    out = CACHE / "gora_floor.json"
    res = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    f = lambda b: f"¥{b['total']:,} {b['ymd'][4:]}({b['dow']}) {b['name'][:34]}" if b else "なし"
    for cid in ids:
        res[cid] = scan(cid, days)
        r = res[cid]
        print(cid, (r["title"] or "")[:24], f"日数={r['days_with_plans']}", "| 平日", f(r["weekday"]), "| 土日祝", f(r["weekend"]),
              "| リクエストのみ", f"¥{r['request_only']['total']:,} {r['request_only']['name'][:20]}" if r["request_only"] else "-", flush=True)
        out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
