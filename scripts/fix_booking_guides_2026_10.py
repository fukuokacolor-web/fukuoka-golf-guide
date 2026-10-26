#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
当日・明日予約ガイド (book-fukuoka-tomorrow) と ひとり予約ガイド (book-fukuoka-solo) の根拠のない数字を是正する (§7・§8)。

- 比較表の「最安」を、じゃらんの直近14日・18H最安の総額 (scripts/.cache/jalan_floor.json・2026-10-24 取得) に置換
- tomorrow には「直近14日で予約できた日数」の列を追加 (同じデータ。じゃらんで18Hプランがあった日数)
- 「成功率8割」「マッチング率7-8割」「9割」「月3,000件」等の根拠のない割合・件数を削除
- じゃらんで予約できない西戸崎・茜は「楽天で確認」
件数 (14 / 11) は変えない (他ページの件数表記は 2026-10-24 にそろえ済み)。
Usage:
  python scripts/fix_booking_guides_2026_10.py            # dry-run
  python scripts/fix_booking_guides_2026_10.py --apply    # REPO + PREVIEW
"""
import re, os, sys, json

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
APPLY = "--apply" in sys.argv

FLOOR = json.load(open(os.path.join(REPO_ROOT, "scripts/.cache/jalan_floor.json"), encoding="utf-8"))
MAP = {c["file"].replace("course-", ""): c.get("jalan_id")
       for c in json.load(open(os.path.join(REPO_ROOT, "jalan_golf_mapping.json"), encoding="utf-8"))["courses"]}
CHECKED_MD = "10/24"
RAKUTEN_ONLY = {"saitozaki", "akane"}  # じゃらんに予約カレンダー無し (2026-10-24 確認)


def floor(slug):
    jid = MAP.get(slug)
    r = FLOOR.get(str(jid).zfill(5)) if jid else None
    return r


def price_cell(slug):
    r = floor(slug)
    if slug in RAKUTEN_ONLY or not r or not r.get("weekday"):
        return '<td class="cmp-rate" style="font-size:12px;">楽天で確認</td>'
    return f'<td class="cmp-rate">¥{r["weekday"]["total"]:,}〜</td>'


def days_cell(slug):
    r = floor(slug)
    if slug in RAKUTEN_ONLY or not r:
        return '<td class="cmp-meta">—<br><small>じゃらん予約不可</small></td>'
    return f'<td class="cmp-meta">{r["days_with_plans"]}日</td>'


def table(html, with_days, remove_star=False):
    """比較表の最安列を置換 (+ 予約可能日数列を追加 / ★列を削除)"""
    log = {"rows": 0}

    def row_sub(m):
        row = m.group(0)
        slug = re.search(r'href="course-([a-z-]+)\.html"', row).group(1)
        if remove_star:  # <td>★★★</td> の列を削除
            row = re.sub(r'<td><span class="star">★+</span></td>', "", row, count=1)
        new_cells = price_cell(slug) + (days_cell(slug) if with_days else "")
        row, n = re.subn(r'<td class="cmp-rate">[^<]*</td>', new_cells, row, count=1)
        assert n == 1, slug
        row = row.replace(">" + REMARK_OLD.get(slug, "\x00") + "<", ">" + REMARK_NEW.get(slug, "") + "<")
        log["rows"] += 1
        return row
    html = re.sub(r'<tr><td class="cmp-rank">\d+</td>.*?</tr>', row_sub, html, flags=re.S)
    return html, log


# 備考の主張 (裏付けなし) → 事実だけ
REMARK_OLD, REMARK_NEW = {}, {}
TOMORROW_REMARKS = {
    "lakeside": ("PGM・直前割多", "PGM"), "moonlake": ("PGM・午後スルー強", "PGM"),
    "saitozaki": ("空港30分・午後スルー強", "楽天GORAのみ"), "mission": ("直前割¥3,000台連発", "独立系"),
    "kurume": ("名門の格安枠", "独立系"), "ariake": ("フラット・1人予約強", "独立系"),
}
SOLO_REMARKS = {
    "ogori": ("福岡県内 1人予約No.1常連", "独立系"), "ariake": ("フラット・初級者多", "独立系"),
    "central": ("アコーディア大箱・常連多", "アコーディア"), "saitozaki": ("空港30分・午後スルー人気", "楽天GORAのみ"),
    "mission": ("山岳・中級者の練習場として人気", "独立系"), "akane": ("フラット・初心者ひとり予約多", "楽天GORAのみ"),
    "hisayama": ("名匠コース・中級者多", "独立系"), "kurume": ("名門の格安枠", "独立系"),
    "lakeside": ("PGM・直前割多", "PGM"), "moonlake": ("PGM・午後スルー強", "PGM"),
}


def stats(rows_slugs):
    vals = [floor(s) for s in rows_slugs if s not in RAKUTEN_ONLY]
    vals = [v for v in vals if v and v.get("weekday")]
    full = sum(1 for v in vals if v["days_with_plans"] == 14)
    low = min(v["weekday"]["total"] for v in vals)
    return full, low


TOMORROW = [  # (old, new, 期待件数)
    ("じゃらんゴルフの即枠フィルターの使い方、予約成功率を上げる4ステップを解説。", "じゃらんゴルフの即枠フィルターの使い方、空き枠の探し方4ステップを解説。", 1),
    ("福岡35コース中、当日・明日の予約成功率が高い14コースをまとめ。", "当日・明日の予約に使いやすい14コースを、じゃらんで直近14日に予約できた日数つきでまとめ。", 1),
    ("福岡35コース中、当日・明日の予約成功率が高い14コースまとめ。", "当日・明日の予約に使いやすい14コースを、予約できた日数つきでまとめ。", 1),
    ("当日朝のキャンセル枠が¥500-2,000割引で出ることがあります。", "直前割引のプランが出ることがあります（割引額はプランごとに異なります）。", 2),
    ("福岡は降水量が安定しないため、予報¥6,000の日が当日¥4,000で取れることもあります。", "", 2),
    ("空き枠が出やすい大手チェーン14コースを実例付きで解説。平日午後スルー狙いなら成功率は8割超。",
     "当日・明日の予約に使いやすい14コースを、じゃらんで直近14日に予約できた日数つきで紹介。", 1),
    ("このページは <strong>当日・明日の予約成功率が高い14コース</strong> を", "このページは <strong>当日・明日の予約に使いやすい14コース</strong> を", 1),
    ("<p>このフィルターを使わない人が9割。逆にこれを使うだけで、空き枠探しの時間が10分→1分に短縮できます。</p>",
     "<p>このフィルターを使うと、今日・明日に予約できるプランだけに絞り込めます。</p>", 1),
    ("の枠が <strong>¥3,500-5,000で並びます</strong>。平日午後は最も空きが多く、当日でも8割の確率で枠が取れます。",
     "の枠が上位に並びやすくなります。料金はコース・日付で大きく変わるので、下の表の最安（総額）も目安にしてください。", 1),
    ('<h2 class="sec-title">当日・明日予約成功率が高い14コース。</h2>', '<h2 class="sec-title">当日・明日の予約に使いやすい14コース。</h2>', 1),
    ("大手チェーン優先 + コース所有数の多さ + 直前割引枠の出やすさを基準に編集部が選定。料金は午後スルー含む最安(平日通常スタートまたは午後スルー)。季節・曜日で変動するため最新は予約画面でご確認ください。",
     f"編集部が選定。<strong>平日最安</strong>は、じゃらんの直近14日（{CHECKED_MD}確認）の18ホールプランの最安（総額・ハーフ/薄暮/ナイト除く）。<strong>予約できた日</strong>は、その14日のうちじゃらんに18ホールの予約可能プランがあった日数です。料金・空きは日々変わるため、最新は予約画面でご確認ください。", 1),
    ('<h2 class="sec-title">予約成功率を上げる4つのコツ。</h2>', '<h2 class="sec-title">空き枠を見つける4つのコツ。</h2>', 1),
    ("前日まで雨予報→当日朝に晴れに変わる、というケースは月3-5回発生。<strong>当日朝7-8時の予報切替直後</strong>に空き枠が増える瞬間を狙うと、通常¥6,000の枠が¥4,000で取れることも。",
     "前日まで雨予報だった日は、キャンセルで当日朝に空き枠が出ることがあります。<strong>当日朝に予約サイトをもう一度確認</strong>すると、枠が見つかる場合があります。", 1),
    ("<th>最安</th>", f"<th>平日最安<br><small>総額・{CHECKED_MD}</small></th><th>予約できた日<br><small>直近14日中</small></th>", 1),
]


def tomorrow(html):
    log = {}
    for old, new, n in TOMORROW:
        c = html.count(old)
        assert c == n, ("tomorrow", old[:30], c)
        html = html.replace(old, new)
    log["text"] = len(TOMORROW)
    REMARK_OLD.clear(); REMARK_NEW.clear()
    for s, (o, nw) in TOMORROW_REMARKS.items(): REMARK_OLD[s], REMARK_NEW[s] = o, nw
    slugs = re.findall(r'<tr><td class="cmp-rank">\d+</td><td><div class="cmp-name"><a href="course-([a-z-]+)\.html"', html)
    html, l2 = table(html, with_days=True)
    log.update(l2)
    full, low = stats(slugs)
    band_old = re.search(r'<div class="stats-band-inner">.*?\n  </div>', html, re.S).group(0)
    band_new = ('<div class="stats-band-inner">\n'
                '    <div class="stats-band-item">\n      <div class="stats-band-num">14<span class="unit">courses</span></div>\n      <div class="stats-band-label">掲載コース</div>\n    </div>\n'
                f'    <div class="stats-band-item">\n      <div class="stats-band-num">{full}<span class="unit">コース</span></div>\n      <div class="stats-band-label">14日すべて予約可</div>\n    </div>\n'
                f'    <div class="stats-band-item">\n      <div class="stats-band-num">¥{low:,}<span class="unit">〜</span></div>\n      <div class="stats-band-label">平日最安（総額）</div>\n    </div>\n'
                f'    <div class="stats-band-item">\n      <div class="stats-band-num">{CHECKED_MD}</div>\n      <div class="stats-band-label">じゃらんで確認</div>\n    </div>\n  </div>')
    html = html.replace(band_old, band_new, 1)
    log["stats"] = f"14日すべて{full}・最安¥{low:,}"
    return html, log


SOLO = [
    ("マッチング率が高い11コースを厳選。", "ひとり予約に使いやすい11コースを紹介。", 1),
    ("福岡ゴルフ一人予約【2026年版】マッチング率高い11コースとじゃらんの使い方", "福岡ゴルフ一人予約【2026年版】ひとり予約に使いやすい11コースとじゃらんの使い方", 1),
    ("福岡ゴルフ 1人予約マッチング率高い11コース完全ガイド", "福岡ゴルフ 1人予約に使いやすい11コース完全ガイド", 2),
    ("じゃらんゴルフ「ひとり予約」のマッチング率が高い11コース。", "じゃらんゴルフ「ひとり予約」に使いやすい11コース。", 1),
    ('"name": "1人予約マッチング率高い11コース"', '"name": "1人予約に使いやすい11コース"', 1),
    ("平日昼の時間帯であれば成功率は約7-8割(編集部目安)。特に福岡市近郊・筑後エリアの大手コース(セントラル福岡・小郡CC・有明CC等)は1人予約者が常に複数いるため、マッチング率が高いです。",
     "成立するかどうかは、同じ日・同じ時間帯に1人予約で申し込む人がいるかによります。成立条件や締切はプランごとに違うので、予約画面の条件を確認してください。", 2),
    ("じゃらんゴルフ「ひとり予約」のマッチング率が高い福岡11コース。", "じゃらんゴルフ「ひとり予約」に使いやすい福岡11コース。", 1),
    ('alt="福岡ゴルフ、ひとりで予約。マッチング率高い11コース。のコース風景"', 'alt="福岡ゴルフ、ひとりで予約。使いやすい11コース。のコース風景"', 1),
    ("福岡ゴルフ、ひとりで予約。<br>マッチング率高い11コース。", "福岡ゴルフ、ひとりで予約。<br>使いやすい11コース。", 1),
    ("福岡で1人予約マッチング率が高い11コースを編集部が選定。", "福岡でひとり予約に使いやすい11コースを編集部が選定。", 1),
    ('<span class="hero-badge">🤝 マッチング率7-8割(平日)</span>', '<span class="hero-badge">🤝 成立条件はプランごとに確認</span>', 1),
    ("福岡県内の主要コースでは平日昼に安定してマッチング成立しており(編集部調べ)、", "", 1),
    ("このページは <strong>福岡県内35コース中、ひとり予約マッチング率が特に高い11コース</strong> を選定。",
     "このページは <strong>ひとり予約に使いやすい11コース</strong> を編集部が選定。", 1),
    ('<h2 class="sec-title">ひとり予約マッチング率が高い11コース。</h2>', '<h2 class="sec-title">ひとり予約に使いやすい11コース。</h2>', 1),
    ("大手チェーン・大箱コース・1人予約利用者の継続性を基準に編集部が選定。★は編集部によるマッチング率の目安(★3=平日昼のマッチング率8割超・★2=同6-7割・★1=同5割前後)。料金は午後スルー含む最安。",
     f"大手チェーン・大箱コースを中心に編集部が選定（ひとり予約の成立率は公開データが無いため掲載していません）。<strong>平日最安</strong>は、じゃらんの直近14日（{CHECKED_MD}確認）の18ホールプランの最安（総額）で、ひとり予約プランの料金とは限りません。", 1),
    ("<th>マッチ率</th><th>最安</th>", f"<th>平日最安<br><small>総額・{CHECKED_MD}</small></th>", 1),
    # じゃらんの「ひとり予約」の締切・割増・開示情報は公式で確認できていない → 断定せず「プランごとに確認」へ
    ("料金は通常プレーと同額・追加料金なし。</p>", "締切や割増の有無はプランごとに違うので、予約画面で確認しましょう。</p>", 1),
    ('<span class="hero-badge">💴 追加料金なし</span>', f'<span class="hero-badge">💴 平日最安を{CHECKED_MD}に確認</span>', 1),
    ("<p>料金は通常プレー と同額、<strong>追加料金は一切なし</strong>。マッチング成立後にじゃらんから組合せメンバー(氏名・年齢・スコア帯)が通知され、当日コースで合流します。",
     "<p>一般的には、同じ日・同じ時間帯に1人で申し込んだ人どうしで組み合わせが作られ、当日コースで合流します。<strong>締切時刻・割増料金の有無・相手に伝わる情報などの条件はプランやコースごとに違う</strong>ので、予約画面の注意事項で必ず確認してください（このページの手順は一般的な流れです）。", 1),
]
SOLO_REGEX = [  # 文の一部が長く可変なもの
    (r"福岡では月3,000件以上のマッチング[^。<]*。", ""),
    (r"寝坊・道中遅延も「予約より遅れます」連絡なしは即ブラックリスト入りします。", "遅れそうなときは、必ずコースに連絡を入れましょう。"),
]
STAT_ITEM = '    <div class="stats-band-item">\n      <div class="stats-band-num">{n}</div>\n      <div class="stats-band-label">{l}</div>\n    </div>\n'


def solo(html):
    log = {}
    for old, new, n in SOLO:
        c = html.count(old)
        assert c == n, ("solo", old[:30], c)
        html = html.replace(old, new)
    REMARK_OLD.clear(); REMARK_NEW.clear()
    for s, (o, nw) in SOLO_REMARKS.items(): REMARK_OLD[s], REMARK_NEW[s] = o, nw
    slugs = re.findall(r'<tr><td class="cmp-rank">\d+</td><td><div class="cmp-name"><a href="course-([a-z-]+)\.html"', html)
    html, l2 = table(html, with_days=False, remove_star=True)
    log.update(l2)
    _, low = stats(slugs)
    n_rak = sum(1 for x in slugs if x in RAKUTEN_ONLY)
    band_old = re.search(r'<div class="stats-band-inner">.*?\n  </div>', html, re.S).group(0)
    band_new = ('<div class="stats-band-inner">\n'
                + STAT_ITEM.format(n='11<span class="unit">courses</span>', l="掲載コース")
                + STAT_ITEM.format(n=f'¥{low:,}<span class="unit">〜</span>', l="平日最安（総額）")
                + STAT_ITEM.format(n=CHECKED_MD, l="じゃらんで確認")
                + STAT_ITEM.format(n=f'{n_rak}<span class="unit">コース</span>', l="楽天GORAのみ") + '  </div>')
    html = html.replace(band_old, band_new, 1)
    for pat, rep in SOLO_REGEX:
        html, n = re.subn(pat, rep.replace("{low}", f"¥{low:,}"), html)
        log[pat[:12]] = n
    log["text"] = len(SOLO)
    return html, log


def main():
    for page, fn in (("book-fukuoka-tomorrow.html", tomorrow), ("book-fukuoka-solo.html", solo)):
        src = open(os.path.join(REPO_ROOT, page), encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in src else "\n"
        if "予約できた日" in src or "使いやすい11コース" in src:
            print(f"  [already] {page}"); continue
        new, log = fn(src.replace("\r\n", "\n"))
        new = new.replace("\n", nl)
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(b)
        body = re.sub(r"<script(?![^>]*ld\+json).*?</script>|<style.*?</style>", " ", new, flags=re.S)
        left = sorted(set(re.findall(r"[0-9]+(?:-[0-9]+)?\s*割|マッチング率|成功率|月3,000件|ブラックリスト", re.sub(r"<[^>]+>", " ", body))))
        print(f"  [change] {page:28} {log}  残る表現={left}")
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, page), "w", encoding="utf-8", newline="").write(new)
    print("APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
