#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
book-fukuoka-cheap.html (格安予約ガイド) を、jalan_floor.py で確認した実料金から組み直す。

- 料金の根拠: scripts/.cache/jalan_floor.json (じゃらん gc ページ・直近14日の18H最安・平日/土日祝別)
  → 掲載に使った値は cheap_guide_prices.json に確認日つきで保存 (監査用)
- 掲載対象: じゃらんで予約カレンダーがあり、平日18H料金を確認できたコースのみ
  (古賀・門司・九州GC八幡 = じゃらん予約不可 / 福岡CC和白・若松・玄海・油山 = じゃらん枠なし → 載せない・CLAUDE.md §9.4)
- 並び順・しきい値は「総額」(じゃらん表示の支払額) 基準。楽天GORAは金額を出さずリンクのみ (機械確認不可)
- 書き換えるのは <head> の title/description/JSON-LD/OGP と、hero 〜 FAQ の本文。CSS・GA4・関連ページ・footer は不変

Usage:
  python scripts/rebuild_cheap_guide.py --dry-run            # 件数・掲載コース・差分サイズを表示 (書き込みなし)
  python scripts/rebuild_cheap_guide.py --preview-only       # 1件テスト: PREVIEW_ROOT だけに書く
  python scripts/rebuild_cheap_guide.py                      # REPO_ROOT + PREVIEW_ROOT に書く
"""
import re, sys, json, html, pathlib, statistics

REPO_ROOT = pathlib.Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = pathlib.Path("C:/Users/Owner/Documents/新しいPJ")
PAGE = "book-fukuoka-cheap.html"
FLOOR = REPO_ROOT / "scripts" / ".cache" / "jalan_floor.json"
EVIDENCE = "cheap_guide_prices.json"

THRESHOLD = 8000  # 総額 (円) — 見出しの「平日¥X以下」
EXCLUDE = {"koga", "moji", "kyushugc", "fukuokacc", "wakamatsu", "genkai", "aburayama"}  # 予約不可・じゃらん枠なし
RAKUTEN_EXCLUDE = {"fukuokacc", "wakamatsu", "akane", "genkai"}
# course_data.json に無いコースの表示名・所在地 (各 course-*.html の title / addressLocality から)
EXTRA = {"pheasant": ("福岡フェザントカントリークラブ", "田川郡"), "takaha": ("鷹羽ロイヤルカントリークラブ", "田川郡"),
         "ukiha": ("浮羽カントリークラブ", "うきは市"), "fukuokakokusai": ("福岡国際カントリークラブ", "宗像市"),
         "kokura": ("小倉カンツリー倶楽部", "北九州市")}

JALAN = "https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F"
RAKUTEN = ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
           "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttps%253A%252F%252Fbooking"
           ".gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}%26m%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp"
           "%252Fguide%252Fdisp%252Fc_id%252F{cid}")
RAK_STYLE = "background:linear-gradient(135deg,#BF0000,#9B0000);color:#fff;box-shadow:0 3px 10px rgba(191,0,0,0.28);"
WD = "月火水木金土日"


def yen(n):
    return f"¥{n:,}"


def md(ymd):  # "20261026" -> "10/26(月)"
    import datetime
    d = datetime.date(int(ymd[:4]), int(ymd[4:6]), int(ymd[6:]))
    return f"{d.month}/{d.day}({WD[d.weekday()]})"


def jdate(iso):  # "2026-10-24" -> "2026年10月24日"
    y, m, d = iso.split("-")
    return f"{int(y)}年{int(m)}月{int(d)}日"


def plan_label(plan):  # じゃらんのプラン名を表示用に: 実体参照を戻し、「※備考欄必読」等の注記と末尾の * を落とす
    p = html.unescape(plan).split("※")[0].strip().rstrip("*").strip()
    return p or html.unescape(plan)


def tags(plan):
    t = []
    if "スルー" in plan:
        t.append("スルー")
    if re.search(r"昼食付|食事付|昼食・|ランチ付", plan):
        t.append("昼食付")
    elif re.search(r"昼食別|食別|食事なし|昼食なし", plan):
        t.append("昼食別")
    if "セルフ" in plan:
        t.append("セルフ")
    if re.search(r"4B限定|4サム|4名|4人", plan):
        t.append("4名1組")
    return "・".join(t)


def load():
    floor = json.loads(FLOOR.read_text(encoding="utf-8"))
    cd = {c["slug"]: c for c in json.loads((REPO_ROOT / "course_data.json").read_text(encoding="utf-8"))}  # read only
    jm = json.loads((REPO_ROOT / "jalan_golf_mapping.json").read_text(encoding="utf-8"))["courses"]
    rm = {c["file"]: c.get("c_id") for c in json.loads((REPO_ROOT / "rakuten_gora_mapping.json").read_text(encoding="utf-8"))["courses"]}
    rows, skipped = [], []
    for c in jm:
        slug, jid = c["file"].replace("course-", ""), c["jalan_id"]
        if slug in EXCLUDE or not jid:
            continue
        f = floor.get(jid)
        if not f or not f.get("weekday") or not f["weekday"].get("total"):
            skipped.append((slug, jid, "平日18H料金なし" if f else "未取得"))
            continue
        name, loc = (cd[slug]["name_ja"].replace("🌙", "").strip(), cd[slug]["locality"]) if slug in cd else EXTRA[slug]
        wk, we = f["weekday"], f.get("weekend")
        rows.append(dict(slug=slug, jid=jid, name=name, loc=loc, checked=f["checked"], period=f["period"],
                         wk_total=wk["total"], wk_price=wk["price"], wk_ymd=wk["ymd"], wk_plan=wk["name"],
                         we_total=we["total"] if we else None, we_ymd=we["ymd"] if we else None,
                         cid=None if slug in RAKUTEN_EXCLUDE else rm.get("course-" + slug)))
    rows.sort(key=lambda r: (r["wk_total"], r["wk_price"]))
    return rows, skipped


def cta(r, cls):
    a = f'<a class="{cls}" href="{JALAN.format(jid=r["jid"])}" target="_blank" rel="nofollow sponsored noopener">{"📅 じゃらんで予約 →" if cls == "tier-card-cta" else "じゃらん →"}</a>'
    if r["cid"]:
        a += (f'<a href="{RAKUTEN.format(cid=r["cid"])}" class="{cls}" style="{RAK_STYLE}" target="_blank" '
              f'rel="nofollow sponsored noopener" data-rakcid="{r["cid"]}">🅡 楽天GORA</a>')
    return a


def tr(i, r):
    we = f'{yen(r["we_total"])}<div class="cmp-area">{md(r["we_ymd"])}</div>' if r["we_total"] else "—"
    tg = tags(r["wk_plan"])
    return (f'        <tr><td class="cmp-rank">{i}</td><td><div class="cmp-name"><a href="course-{r["slug"]}.html">{html.escape(r["name"])}</a></div>'
            f'<div class="cmp-area">{html.escape(r["loc"])}</div></td>'
            f'<td class="cmp-price"><span class="yen">¥</span>{r["wk_total"]:,}<div class="cmp-area">{md(r["wk_ymd"])}{"・" + tg if tg else ""}</div></td>'
            f'<td class="cmp-meta">{we}</td><td>{cta(r, "cmp-cta")}</td></tr>')


def build(rows):
    checked = max(r["checked"] for r in rows)
    p0, p1 = rows[0]["period"].split("/")
    span = f"{int(p0[5:7])}/{int(p0[8:])}〜{int(p1[5:7])}/{int(p1[8:])}"
    hit = [r for r in rows if r["wk_total"] <= THRESHOLD]
    rest = [r for r in rows if r["wk_total"] > THRESHOLD]
    n, cheapest = len(hit), rows[0]
    med = int(statistics.median(r["wk_total"] for r in hit))
    both = [r for r in rows if r["we_total"]]
    gap = int(statistics.mean(r["we_total"] - r["wk_total"] for r in both))
    T = yen(THRESHOLD)
    D = jdate(checked)
    v = dict(n=n, T=T, D=D, span=span, total=len(rows), cheapest=cheapest, med=med, gap=gap, nboth=len(both))

    faq = [
        (f"福岡で平日いくらからゴルフができますか?",
         f"{D}にじゃらんゴルフで直近2週間（{span}）の平日18ホール最安を確認したところ、最も安かったのは{cheapest['name']}の総額{yen(cheapest['wk_total'])}（{md(cheapest['wk_ymd'])}）でした。"
         f"総額{T}以下のコースは{n}コースです。料金は日付・プランで変わるため、最新は予約画面でご確認ください。"),
        ("表の料金はどうやって調べていますか?",
         f"じゃらんゴルフの各コースの予約ページを日付ごとに開き、直近2週間で最も安い18ホールのプランを平日・土日祝に分けて記録しています（ハーフ・薄暮・ナイター、コンペ・年齢限定プラン等は除外）。"
         f"表示はじゃらんの「総額」です。確認日は{D}です。"),
        ("楽天GORAの料金は載っていないのですか?",
         "楽天GORAは料金を当サイトで機械的に確認できないため、金額は掲載していません。楽天GORAのボタンからリンク先の予約画面で料金をご確認ください。"),
        ("古賀ゴルフ・クラブや門司ゴルフ倶楽部が載っていないのはなぜですか?",
         "2026年10月の確認時点で、じゃらんゴルフ・楽天GORAのどちらでもオンライン予約できなかったため、予約できるコースの比較から外しています。"
         "福岡カンツリー倶楽部 和白コース・若松ゴルフ倶楽部・玄海ゴルフクラブなど、じゃらんに予約枠がないコースも掲載していません。各コースの公式サイトをご確認ください。"),
        ("料金はいつ更新されますか?",
         "月1回を目安にじゃらんの料金を確認し直し、表と確認日を更新しています。"),
    ]

    head = {
        "title": f"福岡ゴルフ格安ランキング｜平日{T}以下で回れる{n}コース【{int(checked[5:7])}月の実勢料金】",
        "desc": f"福岡のゴルフ場を平日の安い順に比較。{D}にじゃらんゴルフで直近2週間の平日18ホール最安を{len(rows)}コース確認し、総額{T}以下の{n}コースを掲載。最安は総額{yen(cheapest['wk_total'])}。",
        "headline": f"福岡ゴルフ 平日{T}以下で回れる{n}コース（じゃらん実勢料金・{D}確認）",
        "crumb": f"平日{T}以下で回れる{n}コース",
        "og_desc": f"じゃらんゴルフの直近2週間の平日18ホール最安を{len(rows)}コース確認。総額{T}以下の{n}コースを安い順に比較。確認日{D}。",
    }

    body = f'''<section class="hero">
  <img class="hero-photo" src="images/saitozaki-bridge.webp" alt="福岡ゴルフ、平日{T}以下で回れる{n}コースのコース風景" fetchpriority="high">
    <div class="hero-img"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Smart Booking · Domestic Guide</div>
    <h1 class="hero-title">福岡ゴルフ、平日{T}以下で<br>回れる{n}コース。</h1>
    <p class="hero-sub">{D}に、じゃらんゴルフで福岡のコースの平日18ホール最安（直近2週間）を確認。料金を確認できた{len(rows)}コースのうち、総額{T}以下の{n}コースを安い順に並べました。料金は確認した値と確認日だけを載せています。</p>
    <div class="hero-badges">
      <span class="hero-badge">⛳ {n}コース</span>
      <span class="hero-badge">💴 最安 総額{yen(cheapest['wk_total'])}</span>
      <span class="hero-badge">📅 {int(checked[5:7])}/{int(checked[8:])} 確認</span>
      <span class="hero-badge">🏌️ 平日・18ホール</span>
    </div>
  </div>
</section>

<div class="stats-band">
  <div class="stats-band-inner">
    <div class="stats-band-item">
      <div class="stats-band-num">{n}<span class="unit">courses</span></div>
      <div class="stats-band-label">平日 総額{T}以下</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{yen(cheapest['wk_total'])}</div>
      <div class="stats-band-label">平日最安（総額）</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{yen(med)}</div>
      <div class="stats-band-label">{n}コースの中央値</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{int(checked[5:7])}/{int(checked[8:])}</div>
      <div class="stats-band-label">料金確認日</div>
    </div>
  </div>
</div>

<section class="section">
  <div class="sec-eyebrow">— How We Checked</div>
  <h2 class="sec-title">料金は「じゃらんの直近2週間・平日18ホール最安」。</h2>
  <div class="prose">
    <p>ゴルフ場の料金は日付・時間帯・プランで大きく変わります。このページでは、<strong>{D}にじゃらんゴルフの予約ページを日付ごとに確認</strong>し、{span}の2週間で最も安い18ホールのプランを平日・土日祝に分けて記録しました。ハーフ・薄暮・ナイターのプランと、コンペ・年齢限定など一部の人しか使えないプランは含めていません。</p>
    <p>金額はじゃらんに表示される<strong>「総額」</strong>です。最安のプランはセルフ・昼食別・午後スルーなど条件つきのことが多いので、表の小さな文字（日付・プラン条件）とあわせて予約画面で確認してください。</p>
    <p>平日18ホールの料金を確認できた{len(rows)}コースのうち、<strong>平日の総額が{T}以下だったのは{n}コース</strong>。オンライン予約できないコース（古賀ゴルフ・クラブ、門司ゴルフ倶楽部など）は載せていません。楽天GORAは料金を当サイトで確認できないため、金額は出さずリンクだけを置いています。</p>
  </div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Full Comparison</div>
  <h2 class="sec-title">平日{T}以下の{n}コース 安い順比較表。</h2>
  <p class="sec-desc">じゃらんゴルフ・{span}の18ホール最安（総額）。{D}確認。料金は日々変わるため、最新は予約画面でご確認ください。</p>
  <div class="cmp-table-wrap">
    <table class="cmp-table">
      <thead>
        <tr><th>#</th><th>コース名</th><th>平日最安（総額）</th><th>土日祝最安（総額）</th><th>予約</th></tr>
      </thead>
      <tbody>
{chr(10).join(tr(i, r) for i, r in enumerate(hit, 1))}
      </tbody>
    </table>
  </div>
'''
    if rest:
        body += f'''  <details style="margin-top:28px;">
    <summary style="cursor:pointer;font-weight:700;color:var(--ocean-dark);">参考：平日の総額が{T}を超えたコース（{len(rest)}コース）</summary>
    <div class="cmp-table-wrap" style="margin-top:16px;">
      <table class="cmp-table">
        <thead>
          <tr><th>#</th><th>コース名</th><th>平日最安（総額）</th><th>土日祝最安（総額）</th><th>予約</th></tr>
        </thead>
        <tbody>
{chr(10).join(tr(i, r) for i, r in enumerate(rest, n + 1))}
        </tbody>
      </table>
    </div>
  </details>
'''
    body += "</section>\n\n"

    top = hit[:3]
    cards = "\n".join(f'''      <div class="tier-card">
        <div class="tier-card-area">{html.escape(r["loc"])}</div>
        <div class="tier-card-name"><a href="course-{r["slug"]}.html">{html.escape(r["name"])}</a></div>
        <div class="tier-card-price"><span class="yen">¥</span>{r["wk_total"]:,}<span class="range">総額・{md(r["wk_ymd"])}</span></div>
        <div class="tier-card-desc">最安プラン：{html.escape(plan_label(r["wk_plan"]))}{"<br>土日祝の最安は総額" + yen(r["we_total"]) + "。" if r["we_total"] else ""}</div>
        {cta(r, "tier-card-cta")}
      </div>''' for r in top)
    body += f'''<section class="section">
  <div class="sec-eyebrow">— Cheapest 3</div>
  <h2 class="sec-title">平日最安トップ3。</h2>
  <p class="sec-desc">{D}確認・じゃらんゴルフの直近2週間で、平日18ホールの総額が安かった3コース。プラン名はじゃらんの表記のままです。</p>
  <div class="tier">
    <div class="tier-grid">
{cards}
    </div>
  </div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Save More</div>
  <h2 class="sec-title">同じコースを安く回すための4つの確認ポイント。</h2>
  <div class="tip-grid">
    <div class="tip-card">
      <div class="tip-icon">📅</div>
      <div class="tip-title">1. 平日を選ぶ</div>
      <div class="tip-desc">今回、平日と土日祝の両方の料金を確認できた{len(both)}コースでは、<strong>土日祝の最安は平日の最安より平均{yen(gap)}高い</strong>結果でした。</div>
    </div>
    <div class="tip-card">
      <div class="tip-icon">🔁</div>
      <div class="tip-title">2. 日付をずらして比べる</div>
      <div class="tip-desc">同じコースでも、日によって最安プランの金額は変わります。予約画面のカレンダーで<strong>前後の日付も比べてから</strong>決めるのがおすすめです。</div>
    </div>
    <div class="tip-card">
      <div class="tip-icon">🧾</div>
      <div class="tip-title">3. 「総額」で比べる</div>
      <div class="tip-desc">じゃらんではプラン料金の下に<strong>「総額」</strong>が表示されます。コース同士を比べるときは、実際に支払う目安になる総額どうしで比べましょう。</div>
    </div>
    <div class="tip-card">
      <div class="tip-icon">🔍</div>
      <div class="tip-title">4. プラン条件を読む</div>
      <div class="tip-desc">最安プランは<strong>セルフ・昼食別・午後スルー</strong>などの条件つきが多く、浴場が使えないプランもあります。予約前にプラン名と備考を確認してください。</div>
    </div>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Frequently Asked</div>
  <h2 class="sec-title">よくある質問。</h2>
  <div class="faq-list">
{chr(10).join(f"""    <div class="faq-item">
      <div class="faq-q">{html.escape(q)}</div>
      <div class="faq-a">{html.escape(a)}</div>
    </div>""" for q, a in faq)}
  </div>
</section>

'''
    return head, body, faq, v, checked


def apply(t, head, body, faq, checked):
    rep = []

    def sub(pat, repl):  # repl: str or callable(match) — 1件だけ置換し、件数を rep に記録
        nonlocal t
        t, k = re.subn(pat, repl if callable(repl) else (lambda m: repl), t, count=1, flags=re.S)
        rep.append(k)

    js = lambda s: json.dumps(s, ensure_ascii=False)
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{head["desc"]}">')
    sub(r"<title>[^<]*</title>", f"<title>{head['title']}</title>")
    sub(r'("@type": "Article",\s*"headline": )"[^"]*"(,\s*"description": )"[^"]*"',
        lambda m: m.group(1) + js(head["headline"]) + m.group(2) + js(head["desc"]))
    sub(r'"dateModified": "[^"]*"', f'"dateModified": "{checked}"')
    sub(r'("position": 2, "name": )"[^"]*"(, "item": "https://fukuoka-golf-guide\.com/book-fukuoka-cheap\.html")',
        lambda m: m.group(1) + js(head["crumb"]) + m.group(2))
    sub(r'(<!-- Structured Data: FAQPage -->\s*<script type="application/ld\+json">\n).*?(\n  </script>)',
        lambda m: m.group(1) + "  " + json.dumps(ld, ensure_ascii=False, indent=2).replace("\n", "\n  ") + m.group(2))
    sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{head["headline"]}">')
    sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{head["og_desc"]}">')
    sub(r'<section class="hero">.*?(?=<section class="section section-pale">\s*<div class="sec-eyebrow">— Related Pages)', body)
    return t, rep


def main():
    dry = "--dry-run" in sys.argv
    roots = [PREVIEW_ROOT] if "--preview-only" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
    rows, skipped = load()
    head, body, faq, v, checked = build(rows)
    print(f"確認日 {v['D']} / 期間 {v['span']} / 予約可で平日料金ありの {v['total']} コース / 総額{v['T']}以下 {v['n']} コース / 中央値 {yen(v['med'])} / 土日祝-平日 平均差 {yen(v['gap'])} (n={v['nboth']})")
    for i, r in enumerate(rows, 1):
        print(f"{'*' if r['wk_total'] <= THRESHOLD else ' '}{i:2} {r['slug']:15} {r['name'][:18]:18} 平日 総額{r['wk_total']:>6,} (プラン{r['wk_price']:,}) {md(r['wk_ymd'])} | 土日祝 {r['we_total'] or '—'} | 楽天 {r['cid'] or '—'} | {r['wk_plan'][:30]}")
    for s in skipped:
        print("  skip", *s)
    for k, val in head.items():
        print(f"  {k}: {val}")
    for root in roots:
        p = root / PAGE
        raw = p.read_bytes()
        crlf = b"\r\n" in raw
        t = raw.decode("utf-8").replace("\r\n", "\n")
        new, rep = apply(t, head, body, faq, checked)
        print(f"{p}: subs={rep} changed={new != t} {len(t)}→{len(new)} chars {'CRLF' if crlf else 'LF'}")
        if 0 in rep:
            print("  !! パターン不一致あり — 書き込み中止")
            continue
        if not dry:
            out = new.replace("\n", "\r\n") if crlf else new
            p.write_bytes(out.encode("utf-8"))
            ev = {"_meta": {"source": "scripts/jalan_floor.py (じゃらんゴルフ gc ページ・直近14日の18ホール最安・ハーフ/薄暮/ナイト除外)",
                            "checked": checked, "threshold_total": THRESHOLD, "basis": "じゃらん表示の総額",
                            "excluded": sorted(EXCLUDE), "rakuten": "楽天GORAは料金を機械確認できないため金額は掲載しない"},
                  "courses": rows}
            (root / EVIDENCE).write_text(json.dumps(ev, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if dry:
        print("(dry-run: 書き込みなし)")


if __name__ == "__main__":
    main()
