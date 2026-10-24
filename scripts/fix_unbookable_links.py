#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
course ページ以外で、オンライン予約できないコースへの予約リンクを直す (convert_unbookable_cta.py の続き)。

- 古賀GC・門司GC (じゃらん・楽天とも予約不可): じゃらん+楽天のボタン対 → 公式サイトのボタン1つ
- 九州GC八幡 (じゃらんのみ予約不可): じゃらんボタン → 楽天GORAボタン
- 会員制コースの「予約できる近隣コース」(fukuokacc / genkai) の古賀GC → 予約できる別コースへ差替
- 接待ハブの「ビジターでも比較的予約が取りやすい」(古賀) を事実に合わせて修正
- 2026-10-24 追加: 西戸崎・茜・夜須高原・サンレイク (じゃらんのみ不可) → 楽天、ザ・クラシック (両方不可・公式に WEB 予約あり) → 公式
  じゃらんボタンの隣に同じコースの楽天ボタンがあれば、じゃらんボタンを消すだけ (楽天ボタンを2つにしない)
- 西戸崎のアクセスページの電話・住所を公式どおりに (§7)
冪等: 対象のアフィリURL・旧文面が無ければ no-op。
Usage:
  python scripts/fix_unbookable_links.py              # dry-run
  python scripts/fix_unbookable_links.py --preview    # PREVIEW_ROOT だけに書く (確認用)
  python scripts/fix_unbookable_links.py --apply      # REPO + PREVIEW
"""
import re, os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
if "--preview" in sys.argv:
    ROOTS = [PREVIEW_ROOT]

PAGES = ["area-fukuokacity.html", "area-kitakyushu.html", "hub-business.html", "book-fukuoka-access.html",
         "book-fukuoka-cheap.html", "book-fukuoka-solo.html", "book-fukuoka-tomorrow.html",
         "course-fukuokacc.html", "course-genkai.html",
         # 2026-10-24 追加
         "area-chikuho.html", "area-chikugo.html", "hub-beginner.html", "hub-budget.html", "recommend.html", "seasonal.html",
         "book-fukuoka-golf-foreigner.html", "book-fukuoka-27holes.html", "book-fukuoka-onsen.html", "book-fukuoka-business.html",
         "book-fukuoka-beginner.html", "book-fukuoka-afternoon.html", "access-saitozaki.html"]

OFFICIAL = {"koga": ("02331", "400018", "https://kogagc.co.jp/"), "moji": ("02307", "400047", "https://www.mojigolf.co.jp/"),
            "classic": ("02340", "400022", "https://cm-g.co.jp/the-classic/")}
# じゃらんのみ予約不可 → 楽天へ (2026-10-24 楽天の予約カレンダーで料金・空きを確認)
RAKUTEN_ONLY = {"kyushugc": ("02310", "400012"), "saitozaki": ("02313", "400020"), "akane": ("02344", "400001"),
                "yasukogen": ("02349", "400048"), "sunlake": ("02357", "400053")}
LANG_BLOCK_RE = re.compile(r'<div id="c-(ja|en|ko)" class="content')
A = r'<a [^>]*href="(?P<h{n}>[^"]*)"[^>]*>.*?</a>'


def lang_at(html, pos):
    last = "ja"
    for m in LANG_BLOCK_RE.finditer(html, 0, pos):
        last = m.group(1)
    return last


def rak_url(cid):
    inner = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + inner + "%26m%3D" + inner)


OFF_LABEL = {"ja": "🏛️ 公式サイト（ネット予約なし）", "en": "🏛️ Official site (no online booking)", "ko": "🏛️ 공식 사이트 (온라인 예약 없음)"}
# 公式サイト自体に WEB 予約があるコースは「ネット予約なし」と書かない
OFF_LABEL_WEB = {"ja": "🏛️ 公式サイトで予約", "en": "🏛️ Book on official site", "ko": "🏛️ 공식 사이트에서 예약"}
OFFICIAL_WEB = {"classic"}
RAK_LABEL = {"ja": "🅡 楽天GORAで予約", "en": "🅡 Rakuten GORA (JP)", "ko": "🅡 라쿠텐 GORA (일본어)"}
OFF_STYLE = "background:#1a5c38;color:#fff;"

# 会員制コースの代替誘導: 古賀GC → 予約可コース (2026-10-19 楽天GORA で予約可を確認: 評価・ポイント可)
ALT = {
    "course-fukuokacc.html": ("fukuokakokusai", "福岡国際CC", "宗像市", "400040"),
    "course-genkai.html": ("newui", "NEWユーアイGC", "宗像市", "400052"),
}

TEXT_FIX = {
    # 西戸崎: 公式 saitozaki.com・楽天GORA とも「092-603-0677 / 福岡市東区大字西戸崎316」(2026-10-24 確認)
    "access-saitozaki.html": [
        ("〒811-0321 福岡市東区西戸崎17-18。", "〒811-0321 福岡市東区大字西戸崎316。"),
        ("〒811-0321　福岡県福岡市東区西戸崎17-18<br>", "〒811-0321　福岡県福岡市東区大字西戸崎316<br>"),
        ("17-18 Saitozaki, Higashi Ward, Fukuoka City, Fukuoka 811-0321<br>", "316 Oaza Saitozaki, Higashi Ward, Fukuoka City, Fukuoka 811-0321<br>"),
        ("후쿠오카시 히가시구 사이토자키 17-18<br>", "후쿠오카시 히가시구 사이토자키 316<br>"),
        ("📞 092-603-1555<br>", "📞 092-603-0677<br>"),
    ],
    "hub-business.html": [
        ("クラブハウスの品格と、ビジターでも比較的予約が取りやすい貴重なバランスで、<strong>2回目・3回目の接待</strong>でも飽きさせません。",
         "クラブハウスの品格があり、<strong>2回目・3回目の接待</strong>でも飽きさせません。※ネット予約サイトでの受付は確認できないため（2026年10月時点）、ビジター予約は公式サイトでご確認ください。"),
        ("— and crucially, <strong>more flexible visitor booking</strong> than the strictly private clubs. ",
         "— note that online booking via Jalan / Rakuten GORA is not available (as of Oct 2026), so check visitor booking on the official website. "),
        ("클럽하우스의 품격과, 비지터도 비교적 예약 가능한 귀중한 균형으로, <strong>2회·3회째 접대</strong>에서도 질리지 않는 선택.",
         "클럽하우스의 품격이 있어 <strong>2회·3회째 접대</strong>에서도 질리지 않는 선택. ※온라인 예약 사이트에서는 접수가 확인되지 않으므로 (2026년 10월 기준) 비지터 예약은 공식 사이트에서 확인해 주세요."),
    ],
}


def fix(html, page):
    log = {}
    bump = lambda k, n=1: log.__setitem__(k, log.get(k, 0) + n)

    # 1) 会員制コースの代替誘導ブロック (古賀GC の小カード) を差替
    if page in ALT:
        slug, name, area, cid = ALT[page]
        pat = re.compile(r'(<div style="font-weight:700;color:#1a5c38;font-size:13\.5px;margin-bottom:8px;">)古賀GC '
                         r'<span style="font-weight:400;color:#777;">／福岡市近郊</span>(</div>\s*<div style="display:flex;gap:6px;">\s*'
                         r'<a href=")[^"]*(" target="_blank" rel="nofollow sponsored noopener" onclick="[^"]*" style="[^"]*">)🏌️ 古賀GCを楽天GORAで →(</a>\s*'
                         r'<a href=")course-koga\.html(" onclick="[^"]*?target_page:\')course-koga(\'[^"]*" style="[^"]*">[^<]*</a>)', re.S)
        def alt_sub(m):
            bump("alt_cta")
            return (m.group(1) + f'{name} <span style="font-weight:400;color:#777;">／{area}</span>' + m.group(2) + rak_url(cid)
                    + m.group(3) + f"🏌️ {name}を楽天GORAで →" + m.group(4) + f"course-{slug}.html" + m.group(5) + f"course-{slug}" + m.group(6))
        html = pat.sub(alt_sub, html)

    # 2) 古賀・門司: じゃらん/楽天のボタン (単独 or 対) → 公式ボタン1つ
    for slug, (gc, cid, url) in OFFICIAL.items():
        key = rf'(?:golf-jalan\.net%2Fgc{gc}%2F|c_id%252F{cid}%26)'
        one = rf'<a (?P<attrs>[^>]*href="[^"]*{key}[^"]*"[^>]*)>(?P<inner>.*?)</a>'
        pair = re.compile(one + rf'(?:\s*<a [^>]*href="[^"]*{key}[^"]*"[^>]*>.*?</a>)?', re.S)
        def off_sub(m):
            lang = lang_at(html, m.start())
            cls = re.search(r'class="([^"]*)"', m.group("attrs"))
            cls = cls.group(1).replace("btn-jalan-s", "btn-detail").replace("btn-jalan", "btn-detail").replace("btn-rakuten", "btn-detail") if cls else ""
            bump(f"{slug}_official")
            label = (OFF_LABEL_WEB if slug in OFFICIAL_WEB else OFF_LABEL)[lang]
            if "sticky-btn" in cls:  # sticky の行き先ボタンはコース名を残す (確認できない料金は外す)
                label = "🏛️ " + re.sub(r"（¥[^）]*）", "", re.sub(r"^\S+\s*", "", m.group("inner"))) + "（公式サイト）"
            return f'<a href="{url}" class="{cls}" target="_blank" rel="noopener" style="{OFF_STYLE}">{label}</a>'
        html = pair.sub(off_sub, html)

    # 3) じゃらんのみ予約不可: じゃらんボタン → 楽天GORA ボタン (同じページの楽天ボタンと同じ見た目)
    #    すぐ隣 (前後) に同じコースの楽天ボタンがあれば、じゃらんボタンを消すだけにする
    for slug, (gc, cid) in RAKUTEN_ONLY.items():
        jre = re.compile(rf'<a (?P<attrs>[^>]*href="https://px\.a8\.net/svt/ejp\?[^"]*golf-jalan\.net%2Fgc{gc}%2F"[^>]*)>(?P<inner>.*?)</a>(?P<ws>\s*)', re.S)
        rak_near = re.compile(rf'<a [^>]*href="[^"]*c_id%252F{cid}%26[^"]*"')
        def rk_sub(m):
            before = html[max(0, m.start() - 1500):m.start()]
            after = html[m.end():m.end() + 1500]  # 楽天URLの c_id は a タグの先頭から 600 文字ほど後ろにある
            prev_close = before.rstrip().endswith("</a>") and rak_near.match(before[before.rfind("<a "):]) if "<a " in before else False
            if rak_near.match(after) or prev_close:
                bump(f"{slug}_jalan_removed")
                return ""
            attrs = m.group("attrs")
            lang = lang_at(html, m.start())
            if "sticky-btn" in attrs:  # sticky の行き先ボタン (中身はコース名) は行き先だけ差替
                bump(f"{slug}_to_rakuten")
                return "<a " + re.sub(r'href="[^"]*"', f'href="{rak_url(cid)}"', attrs) + ">" + m.group("inner") + "</a>" + m.group("ws")
            cls = re.search(r'class="([^"]*)"', attrs)
            cls = (cls.group(1).replace("btn-jalan-s", "btn-rakuten").replace("cta-btn-jalan", "cta-btn-rakuten")
                   .replace("btn-jalan", "btn-rakuten")) if cls else ""
            bump(f"{slug}_to_rakuten")
            return (f'<a href="{rak_url(cid)}" class="{cls}" style="background:linear-gradient(135deg,#BF0000,#9B0000);color:#fff;'
                    f'box-shadow:0 3px 10px rgba(191,0,0,0.28);" target="_blank" rel="nofollow sponsored noopener" data-rakcid="{cid}">'
                    f'{"🅡 楽天GORA" if slug == "kyushugc" else RAK_LABEL[lang]}</a>' + m.group("ws"))
        html = jre.sub(rk_sub, html)
        # 同じコースの楽天ボタンが隣り合って2つ並んでいたら1つにする (2026-10-19 の九州GC八幡変換で area-kitakyushu に生じた重複の修復)
        html, n = re.subn(rf'(<a [^>]*href="[^"]*c_id%252F{cid}%26[^"]*"[^>]*>[^<]*</a>)\s*<a [^>]*href="[^"]*c_id%252F{cid}%26[^"]*"[^>]*>[^<]*</a>',
                          r"\1", html)
        if n:
            bump(f"{slug}_dup_removed", n)

    # 4) エリアページの sticky (代表1コースのじゃらんへ飛ぶ) が予約不可コースを向いていれば差替
    #    福岡市エリア: 古賀GC → 久山CC (gc02334・2026-10-18 じゃらんで直近の販売プラン確認済)
    for gc_old, gc_new in (("02331", "02334"), ("02307", None)):
        m = re.search(rf'(var JALAN="https://px\.a8\.net/svt/ejp\?[^"]*golf-jalan\.net%2Fgc){gc_old}(%2F")', html)
        if m and gc_new:
            html = html[:m.start()] + m.group(1) + gc_new + m.group(2) + html[m.end():]
            bump("sticky_retarget")

    # 5) 文面の事実修正
    for old, new in TEXT_FIX.get(page, []):
        if old in html:
            html = html.replace(old, new)
            bump("text_fix")
    return html, log


def main():
    total = 0
    for page in PAGES:
        src = open(os.path.join(REPO_ROOT, page), encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in src else "\n"
        new, log = fix(src.replace("\r\n", "\n"), page)
        new = new.replace("\n", nl)
        if new == src:
            print(f"  [already] {page}")
            continue
        left = len(re.findall(r'golf-jalan\.net%2Fgc0(?:2331|2307|2310|2313|2344|2340|2349|2357)%2F|c_id%252F4000(?:18|47|22)%26|603-1555|西戸崎17-18|17-18 Saitozaki', new))
        print(f"  [change] {page:28} " + " ".join(f"{k}×{v}" for k, v in log.items()) + f"  残={left}" + ("  ⚠" if left else ""))
        total += 1
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, page), "w", encoding="utf-8", newline="").write(new)
    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {total} files")


if __name__ == "__main__":
    main()
