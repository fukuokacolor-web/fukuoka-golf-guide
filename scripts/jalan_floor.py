#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
じゃらんゴルフの gc ページから、直近 N 日間の「18ホールプラン最安」を平日/土日祝別に機械抽出する。
料金鮮度リライト (REWRITE_PLAYBOOK.md) の一次確認用。読み取り専用 (サイトのファイルは触らない)。

- 日付指定: https://golf-jalan.net/gc{id}/?playMonth={月-1}&playDate={日}  (playMonth は 0 始まり)
- 18H 判定: 9ホールアイコンが有効なプランと、名前にハーフプレー/薄暮/ナイト等を含むプランを除外
  (「※ハーフ休憩有」は 18H なので単独の「ハーフ」では除外しない)
- 文字コードはページにより UTF-8 / Shift_JIS が混在 → 自動判定
- 予約カレンダー自体が無いページ (情報掲載のみ) は日数=0 になる → 料金は「確認不可」として扱う

Usage:
  python scripts/jalan_floor.py 02347 02315 ...        # 結果は標準出力 + scripts/.cache/jalan_floor.json
  python scripts/jalan_floor.py 02347 --days 7
"""
import re, sys, json, time, datetime, pathlib, subprocess

CACHE = pathlib.Path(__file__).parent / ".cache"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
EXCL_NAME = re.compile(r"ハーフプレー|ハーフラウンド|ハーフのみ|午後ハーフ|早朝ハーフ|朝ハーフ|9H|９Ｈ|9ホール|薄暮|ナイター|ナイト|1\.5R|練習")
HOLIDAYS = {"2026-10-12", "2026-11-03", "2026-11-23", "2026-12-31", "2027-01-01", "2027-01-11"}  # 期間に合わせて更新
WD = "月火水木金土日"


def decode(b):
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("cp932", errors="ignore")


def fetch(jid, date):
    CACHE.mkdir(exist_ok=True)
    p = CACHE / f"jalan_{jid}_{date:%Y%m%d}.html"
    if not p.exists() or p.stat().st_size < 10000:
        url = f"https://golf-jalan.net/gc{jid}/?playMonth={date.month - 1}&playDate={date.day}"
        subprocess.run(["curl", "-sL", "-A", UA, "-o", str(p), url], check=True)
        time.sleep(1.2)  # 先方サーバへの配慮
    return decode(p.read_bytes())


def parse(t):
    name = re.search(r"<title>([^<|｜]+)", t)
    plans = []
    for r in re.findall(r'<tr data-detail-id="\d+">(.*?)</tr>', t, re.S):
        nm = re.search(r'<a class="planName"[^>]*>\s*(.*?)\s*</a>', r, re.S)
        pr = re.search(r'<div class="price[^"]*"><span>([\d,]+)</span>', r)
        if not (nm and pr):
            continue
        tot = re.search(r'class="totalPrice">\(総額([\d,]+)円', r)
        ymd = re.search(r"ymd=(\d{8})", r)
        n = re.sub(r"\s+", " ", nm.group(1))
        half = re.search(r'<svg class="green">\s*<title>9ホール', r) is not None or bool(EXCL_NAME.search(n))
        plans.append(dict(name=n, price=int(pr.group(1).replace(",", "")),
                          total=int(tot.group(1).replace(",", "")) if tot else None,
                          ymd=ymd.group(1) if ymd else None, half=half))
    full = [p for p in plans if not p["half"]]
    return dict(title=name.group(1).strip() if name else None,
                best=min(full, key=lambda p: p["price"]) if full else None)


def scan(jid, days=14):
    start = datetime.date.today() + datetime.timedelta(days=1)
    title, wk, we, seen = None, None, None, 0
    for k in range(days):
        d = start + datetime.timedelta(days=k)
        r = parse(fetch(jid, d))
        title = title or r["title"]
        b = r["best"]
        if not b or b["ymd"] != f"{d:%Y%m%d}":
            continue
        seen += 1
        b["dow"] = WD[d.weekday()]
        if d.weekday() >= 5 or d.isoformat() in HOLIDAYS:
            we = b if we is None or b["price"] < we["price"] else we
        else:
            wk = b if wk is None or b["price"] < wk["price"] else wk
    return dict(title=title, checked=datetime.date.today().isoformat(),
                period=f"{start:%Y-%m-%d}/{start + datetime.timedelta(days=days - 1):%Y-%m-%d}",
                days_with_plans=seen, weekday=wk, weekend=we)


def main():
    args = sys.argv[1:]
    days = int(args[args.index("--days") + 1]) if "--days" in args else 14
    ids = [a for i, a in enumerate(args) if a.isdigit() and not (i and args[i - 1] == "--days")]
    out = CACHE / "jalan_floor.json"
    res = json.loads(out.read_text(encoding="utf-8")) if out.exists() else {}
    f = lambda b: f"¥{b['price']:,}(総額{b['total']}) {b['ymd'][4:]}({b['dow']}) {b['name'][:34]}" if b else "なし"
    for jid in ids:
        jid = jid.zfill(5)
        res[jid] = scan(jid, days)
        r = res[jid]
        print(jid, (r["title"] or "")[:22], f"日数={r['days_with_plans']}",
              "| 平日", f(r["weekday"]), "| 土日祝", f(r["weekend"]), flush=True)
        out.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
