#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
オンライン予約できなくなったコースの course ページの予約導線を作り替える (§7・§8: 予約できない先へ誘導しない)。

mode "official": じゃらん・楽天とも予約不可 → すべての予約ボタンを公式サイトへ (fukuokacc と同じ「公式のみ」)
mode "rakuten" : じゃらんのみ予約不可      → じゃらんボタンを外し楽天GORAへ一本化 (aburayama と同じ「楽天のみ」)

確認方法 (2026-10-19): じゃらん gc ページに予約カレンダー無し / 楽天GORA は「評価なし・ポイント不可・クーポン不可」= 予約不可
冪等: 対象のアフィリURLが残っていなければ no-op。
2026-10-24 追加: 西戸崎・茜・夜須高原・サンレイク (じゃらん予約カレンダー無し・楽天は予約可) → 楽天へ、
             ザ・クラシック (じゃらん・楽天とも不可・公式サイトに WEB 予約あり) → 公式へ。
             楽天の予約可否は予約カレンダー (search.gora.golf.rakuten.co.jp/cal/disp/c_id/{id}) で判定
             (「現在公開中の枠が無いか、売り切れたため予約できません。」なら不可)。ページに楽天リンクが無いコース (茜) は c_id から作る。
Usage:
  python scripts/convert_unbookable_cta.py                              # dry-run
  python scripts/convert_unbookable_cta.py --only saitozaki --preview   # 1件テスト: PREVIEW_ROOT だけに書く
  python scripts/convert_unbookable_cta.py --apply                      # REPO + PREVIEW に書き込み
"""
import re, os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO_ROOT, PREVIEW_ROOT]
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
if "--preview" in sys.argv:
    ROOTS = [PREVIEW_ROOT]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None

COURSES = {
    "koga": {"mode": "official", "jalan": "02331", "cid": "400018", "official": "https://kogagc.co.jp/"},
    "moji": {"mode": "official", "jalan": "02307", "cid": "400047", "official": "https://www.mojigolf.co.jp/"},
    "kyushugc": {"mode": "rakuten", "jalan": "02310", "cid": "400012"},
    # 2026-10-24 確認
    "saitozaki": {"mode": "rakuten", "jalan": "02313", "cid": "400020"},
    "akane": {"mode": "rakuten", "jalan": "02344", "cid": "400001"},
    "yasukogen": {"mode": "rakuten", "jalan": "02349", "cid": "400048"},
    "sunlake": {"mode": "rakuten", "jalan": "02357", "cid": "400053"},
    "classic": {"mode": "official", "jalan": "02340", "cid": "400022", "official": "https://cm-g.co.jp/the-classic/"},
    # 2026-10-26 確認: じゃらん gc ページに予約カレンダーのマス (<td class="jsDayPanel") が0
    #   (※ 文字列 "jsDayPanel" はカレンダーの無いページの JS にも1件含まれるので、件数ではなく td で判定する)
    #   かつ楽天GORA の予約カレンダーが「評価なし・現在公開中の枠が無いか、売り切れたため予約できません」
    "kokura": {"mode": "official", "jalan": "02309", "cid": "400019", "official": "https://kokura-cc.com/reserve/"},   # ビジターは会員の紹介が必要 (公式)
    "queenshill": {"mode": "official", "jalan": "02328", "cid": "400021", "official": "https://queenshill.co.jp/"},  # 公式にオンライン予約あり
    "raizan": {"mode": "official", "jalan": "02330", "cid": "400043", "official": "http://raizan-gc.co.jp/"},        # 公式にオンライン予約あり
    "keya": {"mode": "official", "jalan": "02351", "cid": "400015", "official": "https://www.keyagc.co.jp/"},       # 公式は予約・問合せフォーム
}
CHECKED = "2026年10月"

LANG_BLOCK_RE = re.compile(r'<div id="c-(ja|en|ko)" class="content')
A_RE = re.compile(r'<a (?P<attrs>[^>]*)>(?P<inner>.*?)</a>', re.S)


def lang_at(html, pos):
    last = "ja"
    for m in LANG_BLOCK_RE.finditer(html, 0, pos):
        last = m.group(1)
    return last


T = {  # 文言 (言語別)
    "official_btn": {"ja": "🏛️ 公式サイトで確認 →", "en": "🏛️ Official website →", "ko": "🏛️ 공식 사이트에서 확인 →"},
    "rakuten_btn": {"ja": "🏌️ 楽天GORAで予約 →", "en": "🏌️ Book on Rakuten GORA 🇯🇵 (JP site) →", "ko": "🏌️ 라쿠텐 GORA에서 예약 🇯🇵 (일본어 사이트) →"},
    "hero_official": {"ja": "🏛️ 公式サイトで予約方法を確認 →", "en": "🏛️ How to book: official website →", "ko": "🏛️ 예약 방법은 공식 사이트에서 →"},
    "ftv_official": {"ja": "🏛️ 公式サイトで予約方法を確認する →", "en": "🏛️ Check how to book on the official website →", "ko": "🏛️ 공식 사이트에서 예약 방법 확인 →"},
    "ftv_rakuten": {"ja": "🏌️ 楽天GORAでこのコースを予約する →", "en": "🏌️ Book this course on Rakuten GORA →", "ko": "🏌️ 라쿠텐 GORA에서 이 코스 예약 →"},
    "micro_official": {"ja": f"ℹ️ じゃらん・楽天GORAではオンライン予約の受付が確認できません（{CHECKED}時点）｜ 予約方法・料金は公式サイト・電話で",
                       "en": "ℹ️ Online booking via Jalan / Rakuten GORA is not available (as of Oct 2026) ｜ Check the official website or call the course",
                       "ko": "ℹ️ 자란·라쿠텐 GORA에서는 온라인 예약이 확인되지 않습니다 (2026년 10월 기준) ｜ 예약 방법·요금은 공식 사이트·전화로"},
    "micro_rakuten": {"ja": "✅ 楽天ポイントが貯まる・使える ｜ 季節により料金変動・最新空き状況をチェック",
                      "en": "✅ Earn & use Rakuten points ｜ Rates vary by season — check live availability",
                      "ko": "✅ 라쿠텐 포인트 적립·사용 가능 ｜ 시기별 요금 변동·최신 빈자리 확인"},
    "hub_title_official": {"ja": "予約は、公式サイトから。", "en": "Book via the official website.", "ko": "예약은 공식 사이트에서."},
    "hub_desc_official": {"ja": f"このコースは現在、じゃらんゴルフ・楽天GORAでのオンライン予約の受付が確認できません（{CHECKED}時点）。ビジターの予約方法・料金は公式サイトまたは電話でご確認ください。",
                          "en": "Online booking via Jalan Golf / Rakuten GORA is not currently available for this course (as of Oct 2026). Please check visitor booking and rates on the official website or by phone.",
                          "ko": "이 코스는 현재 자란골프·라쿠텐 GORA에서 온라인 예약이 확인되지 않습니다 (2026년 10월 기준). 비지터 예약 방법·요금은 공식 사이트 또는 전화로 확인해 주세요."},
    "hub_desc_rakuten": {"ja": "楽天GORAで、最新の空き状況と料金をチェック。楽天ポイントも貯まる・使えます。",
                         "en": "Check live availability and rates on Rakuten GORA (Japanese site).",
                         "ko": "라쿠텐 GORA에서 최신 빈자리와 요금을 확인하세요 (일본어 사이트)."},
    "price_amount_official": {"ja": "公式サイトで確認", "en": "See official site", "ko": "공식 사이트에서 확인"},
}

OFFICIAL_CARD = {
    "ja": ('<div class="booking-logo">OFFICIAL ／ 公式サイト</div>\n        <div class="booking-service-name">公式サイトで予約方法を確認</div>\n'
           '        <div class="booking-desc">ビジターの予約可否・料金・予約方法はゴルフ場の公式サイト（または電話）が最も確実です。</div>\n'
           '        <div class="booking-arrow">公式サイトへ <span class="arrow-ico">→</span></div>'),
    "en": ('<div class="booking-logo">OFFICIAL WEBSITE</div>\n        <div class="booking-service-name">Check how to book</div>\n'
           '        <div class="booking-desc">The course\'s official website (or a phone call) is the most reliable source for visitor booking and rates. Japanese only.</div>\n'
           '        <div class="booking-arrow">Go to official site <span class="arrow-ico">→</span></div>'),
    "ko": ('<div class="booking-logo">OFFICIAL ／ 공식 사이트</div>\n        <div class="booking-service-name">공식 사이트에서 예약 방법 확인</div>\n'
           '        <div class="booking-desc">비지터 예약 가능 여부·요금·예약 방법은 골프장 공식 사이트(또는 전화)가 가장 정확합니다. 일본어 사이트입니다.</div>\n'
           '        <div class="booking-arrow">공식 사이트로 <span class="arrow-ico">→</span></div>'),
}
RAKUTEN_CARD = {
    "ja": ('<div class="booking-logo">RAKUTEN GORA ／ 楽天GORA</div>\n        <div class="booking-service-name">楽天GORAで予約</div>\n'
           '        <div class="booking-desc">楽天ポイントが貯まる・使えるゴルフ予約サイト。最新の空き状況と料金プランを確認できます。</div>\n'
           '        <div class="booking-price-tag">料金は <span class="big">楽天GORAで確認</span></div>\n'
           '        <div class="booking-arrow">楽天GORAで予約する <span class="arrow-ico">→</span></div>'),
    "en": ('<div class="booking-logo">RAKUTEN GORA</div>\n        <div class="booking-service-name">Book on Rakuten GORA</div>\n'
           '        <div class="booking-desc">Japanese golf booking site (Japanese only). Check live availability and rate plans.</div>\n'
           '        <div class="booking-price-tag">Rates <span class="big">on Rakuten GORA</span></div>\n'
           '        <div class="booking-arrow">Book on Rakuten GORA <span class="arrow-ico">→</span></div>'),
}
RAKUTEN_CARD_KO = ('<div class="booking-logo">RAKUTEN GORA ／ 라쿠텐 GORA</div>\n        <div class="booking-service-name">라쿠텐 GORA에서 예약</div>\n'
                   '        <div class="booking-desc">라쿠텐 포인트가 쌓이는 일본 골프 예약 사이트. 그린피·플레이 스타일을 비교할 수 있습니다.</div>\n'
                   '        <div class="booking-price-tag">요금은 <span class="big">라쿠텐에서 확인</span></div>\n'
                   '        <div class="booking-arrow">라쿠텐에서 예약하기 <span class="arrow-ico">→</span></div>')


def rak_url(cid):
    inner = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + inner + "%26m%3D" + inner)


def aff_urls(html, c, build=False):
    j = re.search(r'https://px\.a8\.net/svt/ejp\?[^"\']*golf-jalan\.net%2Fgc' + c["jalan"] + r'%2F', html)
    r = re.search(r'https://rpx\.a8\.net/svt/ejp\?[^"\']*c_id%252F' + c["cid"] + r'%26[^"\']*', html)
    r = r.group(0) if r else (rak_url(c["cid"]) if build and c["mode"] == "rakuten" else None)  # 楽天リンクが無いページ (茜) は作る
    return (j.group(0) if j else None), r


def convert(html, slug, c):
    J, R = aff_urls(html, c, build=True)
    if not J and (c["mode"] == "rakuten" or not R):
        return html, {}
    log = {}
    bump = lambda k: log.__setitem__(k, log.get(k, 0) + 1)
    official = c.get("official")
    seen_container = set()  # booking-grid / price-card-cta ごとに1つだけ残す

    def a_sub(m):
        attrs, inner = m.group("attrs"), m.group("inner")
        href = re.search(r'href="([^"]*)"', attrs)
        href = href.group(1) if href else ""
        is_j, is_r = bool(J) and href == J, bool(R) and href == R
        if not (is_j or is_r):
            return m.group(0)
        if c["mode"] == "rakuten" and is_r:
            return m.group(0)
        lang = lang_at(html, m.start())
        cls = (re.search(r'class="([^"]*)"', attrs) or [None, ""])[1]

        # コンテナ (予約カード群 / 料金カードのボタン群) 単位で重複を除く
        cont = None
        for key in ("booking-grid", "price-card-cta"):
            if key in cls or (key == "booking-grid" and "booking-card" in cls) or (key == "price-card-cta" and "btn-book" in cls):
                cont = (key, html.rfind(f'class="{key}', 0, m.start()))
        if c["mode"] == "rakuten" and cont:
            # 同じコンテナに楽天ボタンが既にあればじゃらんボタンは削除、無ければ楽天に変換
            end = html.find("</div>", m.end()) if cont[0] == "price-card-cta" else html.find("</section>", m.end())
            scope = html[cont[1]:end]
            if R and R in scope:
                bump("removed_jalan")
                return ""
        if c["mode"] == "official" and cont:
            if cont in seen_container:
                bump("removed_dup")
                return ""
            seen_container.add(cont)

        if c["mode"] == "official":
            new_attrs = f'href="{official}" class="{cls}" target="_blank" rel="noopener"'
            if "ftv-cta-btn" in cls:
                new_attrs += f' onclick="if(window.trackAffiliate)trackAffiliate(\'official\',document.title,\'{lang}\',\'ftv-cta\')"'
            style = re.search(r'style="([^"]*)"', attrs)
            if "booking-card" in cls:
                bump("card")
                return f'<a {new_attrs}>\n        {OFFICIAL_CARD[lang]}\n      </a>'
            if style and "hero-cta-btn" in cls:
                new_attrs += f' style="{style.group(1)}"'
            if "btn-book" in cls:
                new_attrs = new_attrs.replace(f'class="{cls}"', 'class="btn-book btn-jalan"') + ' style="background:#1a5c38;"'
            label = (T["hero_official"] if "hero-cta-btn" in cls else T["ftv_official"] if "ftv-cta-btn" in cls else T["official_btn"])[lang]
            bump(cls.split()[0] if cls else "a")
            return f"<a {new_attrs}>{label}</a>"

        # mode rakuten: 残るのは「楽天ボタンが無い場所」のじゃらんボタン → 楽天へ
        new_attrs = attrs.replace(J, R)
        new_attrs = new_attrs.replace("btn-jalan", "btn-rakuten").replace("trackAffiliate('jalan'", "trackAffiliate('rakuten'")
        if "booking-card" in cls:
            bump("card_to_rakuten")
            card = RAKUTEN_CARD_KO if lang == "ko" else RAKUTEN_CARD[lang]
            return f"<a {new_attrs}>\n        {card}\n      </a>"
        label = (T["ftv_rakuten"] if "ftv-cta-btn" in cls else T["rakuten_btn"])[lang]
        if "hero-cta-btn" in cls:
            label = {"ja": "🏌️ 楽天GORAでこのコースを予約 →", "en": "🏌️ Book on Rakuten GORA →", "ko": "🏌️ 라쿠텐 GORA에서 예약 →"}[lang]
        bump("to_rakuten")
        return f"<a {new_attrs}>{label}</a>"

    html = A_RE.sub(a_sub, html)

    # ftv マイクロコピー (じゃらん固有の「キャンセル無料・Ponta」を外す)
    key = "micro_official" if c["mode"] == "official" else "micro_rakuten"
    def micro_sub(m):
        bump("microcopy")
        return f'<div class="ftv-cta-microcopy">{T[key][lang_at(html, m.start())]}</div>'
    html = re.sub(r'<div class="ftv-cta-microcopy">.*?</div>', micro_sub, html, flags=re.S)

    # 予約セクションの見出し・説明
    def hub_sub(m):
        lang = lang_at(html, m.start())
        body = m.group(0)
        if c["mode"] == "official":
            body = re.sub(r'<h2 class="sec-title">[^<]*</h2>', f'<h2 class="sec-title">{T["hub_title_official"][lang]}</h2>', body, count=1)
            body = re.sub(r'<p class="sec-desc" style="margin:0 auto 0;">[^<]*</p>', f'<p class="sec-desc" style="margin:0 auto 0;">{T["hub_desc_official"][lang]}</p>', body, count=1)
            body = re.sub(r'<div class="booking-grid"[^>]*>', '<div class="booking-grid" style="grid-template-columns:1fr;max-width:600px;">', body, count=1)
        else:
            body = re.sub(r'<p class="sec-desc" style="margin:0 auto 0;">[^<]*</p>', f'<p class="sec-desc" style="margin:0 auto 0;">{T["hub_desc_rakuten"][lang]}</p>', body, count=1)
            body = re.sub(r'<div class="booking-grid"[^>]*>', '<div class="booking-grid" style="grid-template-columns:1fr;max-width:600px;">', body, count=1)
        bump("hub")
        return body
    html = re.sub(r'<section class="section-forest booking-hub">.*?</section>', hub_sub, html, flags=re.S)

    # 料金カードの「予約サイトで確認」(official のみ)
    if c["mode"] == "official":
        for lang, old in (("ja", "予約サイトで確認"),):
            n = html.count(f'>{old}</div>')
            html = html.replace(f'>{old}</div>', f'>{T["price_amount_official"][lang]}</div>')
            if n: log["price_amount"] = n

    # sticky CTA (JS テンプレ)
    def sticky_sub(m):
        bump("sticky")
        if c["mode"] == "official":
            btn = lambda t: f"'<a href=\"'+OFFICIAL+'\" class=\"sc-btn sc-jalan\" rel=\"noopener\" target=\"_blank\" style=\"max-width:360px;background:#1a5c38;\">{t}</a>'"
            return ("var OFFICIAL=\"" + official + "\";\n  var sttpl = {\n    // <!-- v2-cvr --> 公式のみ (オンライン予約不可・" + CHECKED + "確認)\n"
                    f"    ja:{btn('🏛️ 公式サイトで確認')},\n    en:{btn('🏛️ Official website')},\n    ko:{btn('🏛️ 공식 사이트')}\n  }};")
        btn = lambda t: f"'<a href=\"'+RAKUTEN+'\" class=\"sc-btn sc-rakuten\" rel=\"nofollow sponsored\" target=\"_blank\" style=\"max-width:360px;\">{t}</a>'"
        return ("var RAKUTEN=\"" + R + "\";\n  var sttpl = {\n    // <!-- v2-cvr --> 楽天のみ (じゃらんは予約不可・" + CHECKED + "確認)\n"
                f"    ja:{btn('🏌️ 楽天GORAで予約する')},\n    en:{btn('🏌️ Book on Rakuten GORA')},\n    ko:{btn('🏌️ 라쿠텐 GORA 예약 🇯🇵')}\n  }};")
    # course-kokura だけ RAKUTEN と sttpl の間に var OFFICIAL="..."; がある (2026-10-26) → 任意で許容
    html = re.sub(r'var JALAN="[^"]*";\s*var RAKUTEN="[^"]*";\s*(?:var OFFICIAL="[^"]*";\s*)?var sttpl = \{.*?\n  \};', sticky_sub, html, count=1, flags=re.S)
    return html, log


PRICE_DESC = {
    "official": {"ja": f"このコースはオンライン予約サイトでの販売が確認できないため、料金は掲載していません（{CHECKED}時点）。ビジター料金・予約方法は公式サイトまたは電話でご確認ください。",
                 "en": "Rates are not listed because online booking is not available for this course (as of Oct 2026). Check visitor rates and booking on the official website or by phone.",
                 "ko": "이 코스는 온라인 예약 사이트에서 판매가 확인되지 않아 요금을 게재하지 않습니다 (2026년 10월 기준). 비지터 요금·예약 방법은 공식 사이트 또는 전화로 확인해 주세요."},
    "rakuten": {"ja": "平日・土日祝の料金は時期・プラン・カートや昼食の有無により変動します。最新の料金と空き状況は楽天GORAでご確認ください。",
                "en": "Weekday and weekend rates vary by season, plan, cart and meal options. Check Rakuten GORA for current rates and availability.",
                "ko": "평일·주말 요금은 시즌·플랜에 따라 변동합니다. 최신 요금과 빈자리는 라쿠텐 GORA에서 확인해 주세요."},
}
PRICE_AMOUNT = {"official": {"Check booking site": "See official site", "예약 사이트에서 확인": "공식 사이트에서 확인"},
                "rakuten": {"予約サイトで確認": "楽天GORAで確認", "Check booking site": "Check on Rakuten GORA", "예약 사이트에서 확인": "라쿠텐 GORA에서 확인"}}


def polish(html, c):
    """料金セクション: 説明文を予約導線に合わせる・公式のみコースは確認できない午後スルーのカードを外す。"""
    log = {}
    mode = c["mode"]

    def desc_sub(m):
        lang = lang_at(html, m.start())
        log["price_desc"] = log.get("price_desc", 0) + 1
        return m.group(1) + f'<p class="sec-desc">{PRICE_DESC[mode][lang]}</p>'
    # 料金見出し (JA/EN「— Green Fees」・KO「— 그린피」) 直後の説明文 (じゃらん調べの古い文面) だけを対象にする
    html = re.sub(r'(<div class="sec-eyebrow">— (?:Green Fees|그린피)</div>\s*<h2 class="sec-title">[^<]*</h2>\s*)<p class="sec-desc">[^\n]*?(?:じゃらん|Jalan|자란)[^\n]*?</p>',
                  desc_sub, html)
    for old, new in PRICE_AMOUNT[mode].items():
        n = html.count(f">{old}</div>")
        if n:
            html = html.replace(f">{old}</div>", f">{new}</div>")
            log["price_amount"] = log.get("price_amount", 0) + n
    if mode == "official":
        pat = re.compile(r'\n[ \t]*<div class="price-card featured">\s*<div class="price-card-head">\s*'
                         r'<div class="price-card-label">AFTERNOON THROUGH</div>.*?(?=\n    </div>\n  </section>)', re.S)
        html, n = pat.subn("", html)
        if n:
            log["afternoon_card_removed"] = n
    return html, log


# コース固有の文面修正 (LF 前提・置換後に元の改行コードへ戻す)
TEXT_FIX = {
    # 茜: 「楽天GORAには掲載がない」「じゃらんでビジター予約可」は 2026-10-24 時点で事実と逆 (じゃらん予約カレンダー無し・楽天 c_id 400001 で予約可)
    "akane": [
        ("じゃらんゴルフでビジター予約可。福岡空港から車で約55分。", "楽天GORAでビジター予約可。福岡空港から車で約55分。"),
        ("じゃらんゴルフでビジター予約可・福岡空港から約55分。", "楽天GORAでビジター予約可・福岡空港から約55分。"),
        ("はい。じゃらんゴルフからビジター予約が可能です（茜ゴルフクラブは楽天GORAには掲載がないため、オンライン予約はじゃらんゴルフをご利用ください）。",
         "はい。楽天GORAからビジター予約が可能です（2026年10月時点、じゃらんゴルフでは予約を受け付けていません）。"),
        ("はい。<strong>じゃらんゴルフ</strong>からビジター予約が可能です（茜GCは楽天GORAには掲載がないため、オンライン予約はじゃらんゴルフをご利用ください）。",
         "はい。<strong>楽天GORA</strong>からビジター予約が可能です（2026年10月時点、じゃらんゴルフでは予約を受け付けていません）。"),
        ("最新の最安値はじゃらんゴルフでご確認ください。", "最新の料金は楽天GORAでご確認ください。"),
        ("最新の最安値は<strong>じゃらんゴルフ</strong>でご確認ください。", "最新の料金は<strong>楽天GORA</strong>でご確認ください。"),
        ("// [Phase 1.5] あかねCC: 楽天GORA未掲載のため Sticky CTA 非表示", "// あかねCC: Sticky CTA 非表示 (予約導線は本文の楽天GORAボタン)"),
    ],
    # 西戸崎: 電話・住所 (§7)。公式 saitozaki.com と楽天GORA で「予約・お問い合わせ 092-603-0677 / 福岡市東区大字西戸崎316」(2026-10-24 確認)
    "saitozaki": [
        ('"streetAddress":"西戸崎17-18"', '"streetAddress":"大字西戸崎316"'),
        ('"telephone": "092-603-1555"', '"telephone": "092-603-0677"'),
        ('<div class="contact-value">福岡市東区 西戸崎17-18</div>', '<div class="contact-value">福岡市東区 大字西戸崎316</div>'),
        ('<div class="contact-value">092-603-1555</div>', '<div class="contact-value">092-603-0677</div>'),
    ],
}


def main():
    total = 0
    for slug, c in COURSES.items():
        if ONLY and slug != ONLY:
            continue
        f = f"course-{slug}.html"
        html = open(os.path.join(REPO_ROOT, f), encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in html else "\n"
        new, log = convert(html.replace("\r\n", "\n"), slug, c)
        new, log2 = polish(new, c)
        log.update(log2)
        for old, rnew in TEXT_FIX.get(slug, []):
            if old in new:
                new = new.replace(old, rnew)
                log["text_fix"] = log.get("text_fix", 0) + 1
        new = new.replace("\n", nl)
        if new == html:
            print(f"  [already] {f}")
            continue
        J, R = aff_urls(new, c)
        left = (new.count(J) if J else 0) + (new.count(R) if (R and c["mode"] == "official") else 0)
        print(f"  [change] {f:22} mode={c['mode']:8} " + " ".join(f"{k}×{v}" for k, v in log.items())
              + f"  残アフィリ={left}" + ("  ⚠" if left else ""))
        total += 1
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, f), "w", encoding="utf-8", newline="").write(new)
    print(f"\n{'APPLIED' if APPLY else 'DRY-RUN'}: {total} files" + (f" -> {ROOTS}" if APPLY else ""))


if __name__ == "__main__":
    main()
