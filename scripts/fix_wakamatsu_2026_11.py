#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
若松ゴルフ倶楽部のページを公式 (2026-11-09 確認) に合わせて直し、「料金・予約・口コミ・アクセス」の検索に答える形にする。
  公式: https://www.wakamatsu.or.jp/guide.php (料金表・予約) / dresscode.php / access.php
  - 料金: 会員同伴 平日¥19,100・土日祝¥25,640 / 会員紹介カード 3〜6・9〜12月 ¥21,300・¥27,840、1〜2・7〜8月 ¥19,100・¥25,640
          基本料金 ¥23,130・¥30,100 / 70歳以上 ¥19,100・¥25,640 / 65歳以上 ¥17,570・¥24,110 / カート ゲスト¥2,200・メンバー¥1,650
    (旧表記 ¥21,600・¥28,570・季節 3-5/10-12月・カート¥1,650 は誤り)
  - 予約: 毎月1日 7:30 から翌月分を電話受付 (メンバーを通じて)・予約状況は公式に掲載
  - アクセス: JR折尾駅からタクシー約10分
  - タイトル・説明文・「口コミ・評判」見出し・よくある質問 (FAQPage) を追加 (日本語)
冪等。改行コードはそのまま。Usage: python scripts/fix_wakamatsu_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
F = "course-wakamatsu.html"
OFF = "https://www.wakamatsu.or.jp/guide.php"
RES = "https://www.wakamatsu.or.jp/reservation.php"
BTN = {"ja": "🏛️ 公式の料金表 →", "en": "🏛️ Official fee table →", "ko": "🏛️ 공식 요금표 →"}


def card(label, name, amount, note, lang, featured=False, small=False):
    st = ' style="font-size:22px;"' if small else ""
    return f'''      <div class="price-card{' featured' if featured else ''}">
        <div class="price-card-head">
          <div class="price-card-label">{label}</div>
          <div class="price-card-name">{name}</div>
        </div>
        <div class="price-card-body">
          <div class="price-amount"{st}>{amount}</div>
          <div class="price-note">{note}</div>
        </div>
        <div class="price-card-cta">
          <a href="{OFF}" class="btn-book btn-jalan" target="_blank" rel="noopener">{BTN[lang]}</a>
        </div>
      </div>'''


Y = '<span class="yen">¥</span>'
GRID = {
    "ja": [card("WITH MEMBER / WEEKDAY", "会員同伴 平日", Y + "19,100", "メンバー1名につき同伴者3名まで・税込・キャディ付。会員同伴優待券なら 3〜6月・9〜12月 ¥17,460／1〜2月・7〜8月 ¥15,270。", "ja"),
           card("WITH MEMBER / WEEKEND", "会員同伴 土日祝", Y + "25,640", "税込・キャディ付。会員同伴優待券なら 3〜6月・9〜12月 ¥21,300／1〜2月・7〜8月 ¥19,100。", "ja", featured=True),
           card("GUEST CARD", "会員の紹介カード", Y + "21,300<span class=\"range\">〜</span>", "平日 ¥21,300・土日祝 ¥27,840（3〜6月・9〜12月）／平日 ¥19,100・土日祝 ¥25,640（1〜2月・7〜8月）。基本料金は平日 ¥23,130・土日祝 ¥30,100。", "ja")],
    "en": [card("WITH MEMBER / WEEKDAY", "With a member, weekday", Y + "19,100", "Up to 3 guests per member, incl. tax, with caddy. With a member's discount voucher: ¥17,460 (Mar–Jun, Sep–Dec) / ¥15,270 (Jan–Feb, Jul–Aug).", "en"),
           card("WITH MEMBER / WEEKEND", "With a member, weekend", Y + "25,640", "Incl. tax, with caddy. With a member's discount voucher: ¥21,300 (Mar–Jun, Sep–Dec) / ¥19,100 (Jan–Feb, Jul–Aug).", "en", featured=True),
           card("GUEST CARD", "Member's introduction card", Y + "21,300<span class=\"range\">+</span>", "Weekday ¥21,300 / weekend ¥27,840 (Mar–Jun, Sep–Dec); weekday ¥19,100 / weekend ¥25,640 (Jan–Feb, Jul–Aug). Standard guest rate: weekday ¥23,130 / weekend ¥30,100.", "en")],
    "ko": [card("WITH MEMBER / WEEKDAY", "회원 동반 평일", Y + "19,100", "회원 1명당 동반자 3명까지·세금 포함·캐디 동반. 회원 동반 우대권 이용 시 3~6월·9~12월 ¥17,460 / 1~2월·7~8월 ¥15,270.", "ko"),
           card("WITH MEMBER / WEEKEND", "회원 동반 주말·공휴일", Y + "25,640", "세금 포함·캐디 동반. 회원 동반 우대권 이용 시 3~6월·9~12월 ¥21,300 / 1~2월·7~8월 ¥19,100.", "ko", featured=True),
           card("GUEST CARD", "회원 소개 카드", Y + "21,300<span class=\"range\">~</span>", "평일 ¥21,300·주말 ¥27,840 (3~6월·9~12월) / 평일 ¥19,100·주말 ¥25,640 (1~2월·7~8월). 기본 요금은 평일 ¥23,130·주말 ¥30,100.", "ko")],
}
NOTE = {
    "ja": f'<strong>💡 補足（公式の料金表・2026年11月9日確認）:</strong> 全て税込・18ホール。70歳以上は平日 ¥19,100・土日祝 ¥25,640、65歳以上は ¥17,570・¥24,110（年齢の証明が必要）。原則キャディ付きの歩きのラウンドで、乗用カートは前日までに申込（ゲスト ¥2,200／メンバー ¥1,650・先着順）。予約は<strong>毎月1日 7:30から翌月分をメンバーを通じて電話で</strong>受け付け、空き状況は<a href="{RES}" target="_blank" rel="noopener" style="color:#5a3e00;text-decoration:underline;">公式の予約状況ページ</a>で見られます。',
    "en": f'<strong>💡 Notes (official fee table, checked 9 Nov 2026):</strong> All prices incl. tax, 18 holes. Age 70+: weekday ¥19,100 / weekend ¥25,640; age 65+: ¥17,570 / ¥24,110 (ID required). Rounds are normally walking with a caddy; riding carts must be requested by the day before (guest ¥2,200 / member ¥1,650, first come first served). Bookings for the following month open on the 1st at 7:30 by phone, through a member. Availability is shown on the <a href="{RES}" target="_blank" rel="noopener" style="color:#5a3e00;text-decoration:underline;">official reservation status page</a>.',
    "ko": f'<strong>💡 참고 (공식 요금표·2026년 11월 9일 확인):</strong> 모두 세금 포함·18홀. 70세 이상은 평일 ¥19,100·주말 ¥25,640, 65세 이상은 ¥17,570·¥24,110 (연령 증명 필요). 원칙적으로 캐디 동반 도보 라운드이며, 승용 카트는 전날까지 신청 (게스트 ¥2,200 / 회원 ¥1,650·선착순). 예약은 <strong>매월 1일 7:30부터 다음 달 분을 회원을 통해 전화로</strong> 접수하며, 예약 현황은 <a href="{RES}" target="_blank" rel="noopener" style="color:#5a3e00;text-decoration:underline;">공식 예약 현황 페이지</a>에서 볼 수 있습니다.',
}

FAQ = [
    ("若松ゴルフ倶楽部の料金はいくら？", "公式の料金表（2026年11月確認・税込）では、メンバー同伴で平日 ¥19,100・土日祝 ¥25,640です。メンバーの紹介カードを使う場合は、3〜6月・9〜12月が平日 ¥21,300・土日祝 ¥27,840、1〜2月・7〜8月が平日 ¥19,100・土日祝 ¥25,640です。原則キャディ付きです。"),
    ("ビジターだけで予約できる？", "できません。公式サイトによると、メンバーの同伴または紹介が必ず必要で、ゲストだけではスタート予約できません。じゃらんゴルフ・楽天GORAなどの予約サイトにも掲載がありません。予約はメンバーを通じて、毎月1日 7:30から翌月分を電話で受け付けています。"),
    ("ドレスコードは？", "男性は来場時にブレザーの着用が必要です（6〜9月は任意）。Tシャツ・ジーンズ・サンダルでの来場はできません。プレー中は襟付きのシャツ（または襟高3cm以上のハイネック）を着て、シャツの裾は出さないでください。モックネック・カーゴパンツ・ジョガーパンツも着用できません。"),
    ("アクセスは？", "車なら福岡空港から約70分、博多駅から約60分（北九州都市高速の黒崎IC経由）、小倉駅から若戸トンネル経由で約35分です。電車なら JR鹿児島本線の折尾駅からタクシーで約10分です（いずれも公式サイトの案内）。"),
    ("口コミ・評判は？", "このページの「口コミ・評判」欄に、Threadsの公開投稿を編集部が要約しています。名門としての格式を評価する声と、12番ショートの左のOBに注意という声があります。投稿はまだ少なめです。"),
]


def faq_html():
    items = "\n".join(f'''      <div style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:14px;">
        <p style="font-weight:700;color:var(--forest);margin-bottom:8px;">Q. {q}</p>
        <p style="color:var(--charcoal);line-height:1.9;margin:0;">{a}</p>
      </div>''' for q, a in FAQ)
    return f'''  <!-- wakamatsu-faq-v1 -->
  <section class="section section-sand">
    <div class="sec-eyebrow">— FAQ</div>
    <h2 class="sec-title">よくある質問</h2>
    <div style="max-width:820px;margin-top:8px;">
{items}
    </div>
  </section>

'''


def faq_ld():
    d = {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    return '  <script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + "\n  </script>\n"


TITLE = "若松ゴルフ倶楽部の料金・予約方法・ドレスコード・アクセス｜口コミも | 福岡ゴルフ場ガイド"
DESC = "若松ゴルフ倶楽部（北九州市若松区・1959年開場の名門）の料金は会員同伴で平日¥19,100・土日祝¥25,640（税込・公式）。ビジターはメンバーの同伴か紹介が必要で、予約サイトでは予約できません。ドレスコード・アクセス・口コミもまとめました。"

SIMPLE = [
    ("<title>若松ゴルフ倶楽部｜料金・アクセス | 福岡ゴルフ場ガイド</title>", f"<title>{TITLE}</title>"),
    ('<meta property="og:title" content="若松ゴルフ倶楽部｜料金・アクセス | 福岡ゴルフ場ガイド">', f'<meta property="og:title" content="{TITLE}">'),
    ('"priceRange": "¥21,600〜¥28,570"', '"priceRange": "¥19,100〜¥30,100"'),
    ("料金は平日¥21,600〜・土日祝¥28,570（メンバー同伴）。", "料金は会員同伴で平日¥19,100・土日祝¥25,640（税込・公式）。"),
    ('<div class="stat-num">¥21,600<span class="unit">〜</span></div><div class="stat-label">同伴・平日(税込)</div>', '<div class="stat-num">¥19,100<span class="unit">〜</span></div><div class="stat-label">会員同伴・平日(税込)</div>'),
    ('<div class="stat-num">¥21,600<span class="unit">〜</span></div><div class="stat-label">Accomp. weekday (incl. tax)</div>', '<div class="stat-num">¥19,100<span class="unit">〜</span></div><div class="stat-label">With member, weekday (incl. tax)</div>'),
    ('<div class="stat-num">¥21,600<span class="unit">〜</span></div><div class="stat-label">동반 평일(세금포함)</div>', '<div class="stat-num">¥19,100<span class="unit">〜</span></div><div class="stat-label">회원 동반 평일(세금포함)</div>'),
    ('同伴 平日 <span class="big">¥21,600</span> / 土日祝 ¥28,570', '会員同伴 平日 <span class="big">¥19,100</span> / 土日祝 ¥25,640'),
    ('Accomp. weekday <span class="big">¥21,600</span> / weekend ¥28,570', 'With member, weekday <span class="big">¥19,100</span> / weekend ¥25,640'),
    ('동반 평일 <span class="big">¥21,600</span> / 주말 ¥28,570', '회원 동반 평일 <span class="big">¥19,100</span> / 주말 ¥25,640'),
    ('<h2 class="sec-title">Threadsでの評判</h2>', '<h2 class="sec-title">口コミ・評判（Threadsの声）</h2>'),
    ("小倉駅からは若戸トンネル経由で約35分。", "小倉駅からは若戸トンネル経由で約35分。電車なら JR折尾駅からタクシーで約10分（公式）。"),
    ("From Kokura Station, ~35 min via the Wakato Tunnel.", "From Kokura Station, ~35 min via the Wakato Tunnel. By train, take a taxi from JR Orio Station (about 10 min, per the club)."),
    ("코쿠라역에서는 와카토 터널 경유로 약 35분.", "코쿠라역에서는 와카토 터널 경유로 약 35분. 전철은 JR 오리오역에서 택시로 약 10분 (공식)."),
]

for root in ROOTS:
    p = os.path.join(root, F)
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    new = s.replace("\r\n", "\n")
    n = 0
    for a, b in SIMPLE:
        if a in new and b not in new:
            new = new.replace(a, b); n += 1
    new, k = re.subn(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', new, count=1)
    # 料金カード 3 言語 (旧の ¥21,600 カードがある場合のみ)
    for lang, tag in (("ja", 'id="c-ja"'), ("en", 'id="c-en"'), ("ko", 'id="c-ko"')):
        i = new.find(tag)
        j = min([x for x in (new.find('id="c-en"', i + 1), new.find('id="c-ko"', i + 1), len(new)) if x > i])
        blk = new[i:j]
        m = re.search(r'(<div class="pricing-grid">\n)(.*?)(\n    </div>\n    <div style="max-width:780px;margin:24px auto 0;padding:14px 20px;background:#fff8e6;[^"]*">\n      )(.*?)(\n    </div>)', blk, re.S)
        if m and "21,600" in m.group(2):
            blk = blk[:m.start()] + m.group(1) + "\n\n".join(GRID[lang]) + m.group(3) + NOTE[lang] + m.group(5) + blk[m.end():]
            n += 1
        new = new[:i] + blk + new[j:]
    if "wakamatsu-faq-v1" not in new:
        anchor = '  <section class="section">\n    <div class="sec-eyebrow">— Contact</div>\n    <h2 class="sec-title">連絡先・公式情報</h2>'
        assert new.count(anchor) == 1
        new = new.replace(anchor, faq_html() + anchor)
        new = new.replace("</head>", faq_ld() + "</head>", 1)
        n += 1
    new = new.replace("\n", nl)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
        json.loads(m.group(1))
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    left = [x for x in ("21,600", "28,570", "16,340", "20,740", "ゲスト¥1,650", "3-5月") if x in new]
    print(f"{root}: {n} 箇所 {'(変更なし)' if new == s else ''} 残り旧表記: {left}")
    if APPLY and new != s:
        open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
