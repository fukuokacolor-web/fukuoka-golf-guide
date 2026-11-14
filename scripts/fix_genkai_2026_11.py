#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
玄海ゴルフクラブを公式 (https://genkai-gc.com/ ・2026-11-09 にブラウザ表示で確認) に合わせて直す。
  guide   : 予約は【メンバー様ご本人様から】の【完全予約制】・キャンセルは3日前正午まで (以降1人¥2,000)
            ゲスト キャディ付き 10〜12月 ¥21,900/¥28,900・3/7/9月 ¥19,900/¥27,900・1/2/8月 ¥17,900/¥26,900
            ゲスト セルフ     10〜12月 ¥17,900/¥24,900・3/7/9月 ¥15,900/¥23,900・1/2/8月 ¥13,900/¥22,900
            メンバー キャディ付き ¥11,395・セルフ ¥8,575 / 2B割増あり
            ドレスコード: 入退場時ブレザー等 (6〜9月除く)・Tシャツ/半ズボン/ジーンズ/サンダル不可・プレー時は帽子・襟付き袖付きシャツ
  news    : ゲスト申込書をダウンロードしメールまたはFAXで提出 (2026-09-30)
            2027年1月5〜8日・1月12日〜3月6日はコース改修でクローズ (2026-11-02)
  access  : 香椎東ランプ・古賀IC・若宮IC から / 博多駅→JR東郷駅 約30分→タクシー約15分 / 福岡空港からタクシー約1時間
  旧表記の誤り: 土日祝の料金が ¥1,000 安い・「じゃらん・楽天GORAにも掲載」(予約不可)・古賀GC/芥屋GC を「予約可」
              (両方とも予約サイトでは予約不可)・若宮IC 14.5km/約25分 (公式に記載なし)
冪等。改行コードはそのまま。Usage: python scripts/fix_genkai_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
F = "course-genkai.html"
GUIDE = "https://genkai-gc.com/guide"
CLOSE_JA = "⚠️ 2027年1月5〜8日と1月12日〜3月6日は、コース改修のためクローズします（公式）。"

TITLE = "玄海ゴルフクラブの料金・予約方法・ドレスコード・アクセス｜口コミも | 福岡ゴルフ場ガイド"
DESC = "玄海ゴルフクラブ（宗像市・2029年日本オープン会場）のゲスト料金はセルフ平日¥13,900〜・キャディ付き平日¥17,900〜（税込・公式）。予約はメンバー本人からの完全予約制で、予約サイトでは予約できません。ドレスコード・アクセス・口コミ・2027年初めのクローズ期間もまとめました。"

FAQ = [
    ("玄海ゴルフクラブの料金は？", "公式の料金表（2026年11月確認・税込）では、ゲストのセルフは平日 ¥13,900〜¥17,900・土日祝 ¥22,900〜¥24,900、キャディ付きは平日 ¥17,900〜¥21,900・土日祝 ¥26,900〜¥28,900です。10〜12月が最も高く、1・2・8月が最も安い区分です。2人での利用は割増があります。"),
    ("ビジターでも予約できる？", "公式サイトでは、予約はメンバー本人からの完全予約制とされています。ゲストは公式サイトのゲスト申込書をダウンロードし、メールかFAXで提出します。じゃらんゴルフ・楽天GORAでは予約できません。GDOゴルフ場予約にはコースのページがあります。"),
    ("ドレスコードは？", "入退場時はブレザーなどの上着が必要です（6〜9月を除く）。Tシャツ・半ズボン・ブルージーンズ、サンダルでの来場はできません。プレー中は帽子かサンバイザーをかぶり、襟付きで袖のあるシャツを着てください（ハイネックは可）。ハーフパンツの場合はくるぶしが隠れるソックスが必要です（公式）。"),
    ("アクセスは？", "車なら九州自動車道の古賀ICか若宮IC、または都市高速の香椎東ランプから。電車なら JR博多駅から東郷駅まで約30分、東郷駅からタクシーで約15分です。福岡空港からタクシーで約1時間（いずれも公式）。"),
    ("休みの日やクローズ期間は？", "休場日は月曜日です。2029年日本オープンに向けたコース改修のため、2027年1月5〜8日と1月12日〜3月6日はクローズすると公式サイトで告知されています。"),
]

R = [
    # head
    ("<title>玄海ゴルフクラブ｜料金・アクセス | 福岡ゴルフ場ガイド</title>", f"<title>{TITLE}</title>"),
    ('<meta property="og:title" content="玄海ゴルフクラブ｜料金・アクセス | 福岡ゴルフ場ガイド">', f'<meta property="og:title" content="{TITLE}">'),
    ('"priceRange": "¥13,900〜¥27,900"', '"priceRange": "¥13,900〜¥28,900"'),
    # 冒頭の案内
    ("2023年10月リニューアル後、九州最高峰のトーナメントコースとして営業中。<strong>メンバー本人完全予約制が原則</strong>のため、楽天GORA・じゃらんゴルフではビジター枠が限定的です。ビジター予約は <strong>公式サイト・お電話 (0940-62-2233)・GDOゴルフ場予約</strong> のいずれかからお問い合わせください。",
     f"2023年10月リニューアル後、2029年日本オープンの会場として営業中。予約は<strong>メンバー本人からの完全予約制</strong>（公式）で、ゲストは公式サイトのゲスト申込書をメールかFAXで提出します。じゃらんゴルフ・楽天GORAでは予約できません（GDOゴルフ場予約にはコースのページがあります）。お問い合わせは 0940-62-2233。<br>{CLOSE_JA}"),
    ("Renewed October 2023 as a top-tier tournament course in Kyushu. <strong>Reservations are member-priority</strong> and visitor slots are limited on Rakuten GORA / Jalan. Visitors should book via the <strong>official site, phone (0940-62-2233), or GDO Reserve</strong>.",
     "Renewed in October 2023 and the venue for the 2029 Japan Open. Bookings are <strong>made by members themselves only</strong> (official); guests submit the club's guest application form by email or fax. Not bookable on Jalan Golf or Rakuten GORA (GDO has a course page). Phone 0940-62-2233.<br>⚠️ Closed for course work 5–8 Jan and 12 Jan–6 Mar 2027 (official)."),
    ("2023년 10월 리뉴얼 후 규슈 최고 수준의 토너먼트 코스로 영업 중. <strong>회원 우선 예약제</strong>이므로 라쿠텐 GORA·자란 골프 비지터 슬롯이 제한적. <strong>공식 사이트·전화 (0940-62-2233)·GDO 골프장 예약</strong> 중 하나로 문의해 주세요.",
     "2023년 10월 리뉴얼, 2029년 일본오픈 개최 코스로 영업 중. 예약은 <strong>회원 본인만 가능한 완전 예약제</strong> (공식)이며, 게스트는 공식 사이트의 게스트 신청서를 이메일 또는 팩스로 제출합니다. 자란골프·라쿠텐 GORA에서는 예약할 수 없습니다 (GDO에는 코스 페이지가 있음). 문의 0940-62-2233.<br>⚠️ 2027년 1월 5~8일, 1월 12일~3월 6일은 코스 개수로 휴장 (공식)."),
    # 今すぐ予約ボックス
    ("以下の楽天GORAボタンは<strong>各コース（福岡国際CC・古賀GC・芥屋GC）</strong>の予約ページに移動します。", "以下の楽天GORAボタンは<strong>各コース（福岡国際CC・NEWユーアイGC・久山CC）</strong>の予約ページに移動します。"),
    ("玄海ゴルフクラブはメンバー本人完全予約制（紹介・同伴が推奨）です。", "玄海ゴルフクラブはメンバー本人からの完全予約制です。"),
    # 料金
    ("下記は2026年4-9月のビジター料金目安。<strong>メンバー本人完全予約制</strong>のため、原則として紹介もしくはメンバー同伴が推奨されます。最新空き状況は予約サイトまたは公式へお問合せください。",
     "下記は公式の料金表（2026年11月9日確認・税込）のゲスト料金。10〜12月が最も高く、1・2・8月が最も安い区分です。予約は<strong>メンバー本人からの完全予約制</strong>です。"),
    ("平日 ¥13,900〜¥17,900／土日祝 ¥21,900〜¥23,900。季節により変動。", "平日 ¥13,900〜¥17,900／土日祝 ¥22,900〜¥24,900（季節で変わります）。"),
    ("平日 ¥17,900〜¥21,900／土日祝 ¥25,900〜¥27,900。プレー体験を高めるならキャディ付。", "平日 ¥17,900〜¥21,900／土日祝 ¥26,900〜¥28,900（季節で変わります）。"),
    ("セルフ ¥8,575／キャディ付 ¥11,395（2026年4-9月）。ビジター料金との差額参考値。", "セルフ ¥8,575／キャディ付 ¥11,395（全日・公式）。"),
    ("Below are reference rates for April-September 2026. As Genkai operates a <strong>member-only reservation system</strong>, member introduction or accompaniment is generally recommended. Confirm latest availability via booking sites or directly with the club.",
     "Below are the guest rates from the official fee table (checked 9 Nov 2026, incl. tax). Oct–Dec is the most expensive season and Jan, Feb and Aug the cheapest. Bookings are <strong>made by members themselves only</strong>."),
    ("Weekday ¥13,900〜¥17,900 / Weekend & holiday ¥21,900〜¥23,900. Seasonal variation.", "Weekday ¥13,900〜¥17,900 / weekend & holiday ¥22,900〜¥24,900 (varies by season)."),
    ("Weekday ¥17,900〜¥21,900 / Weekend & holiday ¥25,900〜¥27,900. Recommended for the full premier experience.", "Weekday ¥17,900〜¥21,900 / weekend & holiday ¥26,900〜¥28,900 (varies by season)."),
    ("Self ¥8,575 / With caddie ¥11,395 (April-September 2026). Reference for visitor pricing context.", "Self ¥8,575 / with caddie ¥11,395 (all days, official)."),
    ("아래는 2026년 4-9월 비지터 요금 기준. <strong>회원 본인 완전 예약제</strong>로 운영되어 회원 소개 또는 동반이 권장됩니다. 최신 빈자리는 예약 사이트 또는 공식 사이트에 문의해 주세요.",
     "아래는 공식 요금표 (2026년 11월 9일 확인·세금 포함)의 게스트 요금. 10~12월이 가장 비싸고 1·2·8월이 가장 저렴합니다. 예약은 <strong>회원 본인만 가능한 완전 예약제</strong>입니다."),
    ("평일 ¥13,900〜¥17,900／주말·공휴일 ¥21,900〜¥23,900. 시즌별 변동.", "평일 ¥13,900〜¥17,900／주말·공휴일 ¥22,900〜¥24,900 (시즌별 변동)."),
    ("평일 ¥17,900〜¥21,900／주말·공휴일 ¥25,900〜¥27,900. 명문의 풀 서비스 체험.", "평일 ¥17,900〜¥21,900／주말·공휴일 ¥26,900〜¥28,900 (시즌별 변동)."),
    ("셀프 ¥8,575／캐디 동반 ¥11,395 (2026년 4-9월). 비지터 요금과의 차이 참고 값.", "셀프 ¥8,575／캐디 동반 ¥11,395 (전일·공식)."),
    ('<div class="price-card-label">MEMBER / 2026年4-9月</div>', '<div class="price-card-label">MEMBER / 全日</div>'),
    ('<div class="price-card-label">MEMBER / 2026년 4-9월</div>', '<div class="price-card-label">MEMBER / 전일</div>'),
    ('<div class="price-card-label">MEMBER / Apr-Sep 2026</div>', '<div class="price-card-label">MEMBER / All days</div>'),
    # 予約条件の注意書き
    ("玄海GCは原則「メンバー本人完全予約制」。一部の予約サイト（じゃらん・楽天GORA）にも掲載されますが、実質的にはメンバー紹介またはメンバー同伴が推奨される名門コースです。",
     "玄海GCの予約はメンバー本人からの完全予約制です。ゲストは公式サイトのゲスト申込書をダウンロードし、メールかFAXで提出します。じゃらんゴルフ・楽天GORAでは予約できません。キャンセルは3日前の正午まで（以降は1人 ¥2,000）。"),
    ('Genkai GC operates a "member-only reservation system" in principle. Although some plans appear on Jalan and Rakuten GORA, member introduction or accompaniment is generally recommended for this premier course.',
     "Bookings at Genkai GC are made by members themselves only. Guests download the club's guest application form and submit it by email or fax. Not bookable on Jalan Golf or Rakuten GORA. Cancel by noon three days before (¥2,000 per person after that)."),
    ("겐카이GC는 원칙적으로 「회원 본인 완전 예약제」. 자란·라쿠텐 GORA에 일부 플랜이 게재되지만 회원 소개 또는 동반이 권장되는 명문 코스입니다.",
     "겐카이GC의 예약은 회원 본인만 가능한 완전 예약제입니다. 게스트는 공식 사이트의 게스트 신청서를 내려받아 이메일 또는 팩스로 제출합니다. 자란골프·라쿠텐 GORA에서는 예약할 수 없습니다. 취소는 3일 전 정오까지 (이후 1인 ¥2,000)."),
    # アクセス
    ('<div class="access-label">若宮IC</div><div class="access-value">14.5km / 約25分</div>', '<div class="access-label">Nearest IC</div><div class="access-value">古賀IC・若宮IC（公式）</div>'),
    ('<div class="access-label">Wakamiya IC</div><div class="access-value">14.5km / ~25 min</div>', '<div class="access-label">Nearest IC</div><div class="access-value">Koga IC / Wakamiya IC (official)</div>'),
    ('<div class="access-label">와카미야 IC</div><div class="access-value">14.5km / 약 25분</div>', '<div class="access-label">최근 IC</div><div class="access-value">고가 IC·와카미야 IC (공식)</div>'),
    # 予約セクション
    ("名門・玄海GCも一部プランで予約サイトに掲載。メンバー紹介推奨ですが、空き状況のチェックから始めましょう。", "予約はメンバー本人からの完全予約制。ゲストは公式サイトのゲスト申込書（メール・FAX）で申し込みます。"),
    ("Premier Genkai GC also appears on major booking sites for select plans. Member introduction is recommended, but start by checking availability.", "Bookings are made by members themselves only. Guests apply with the club's guest form by email or fax."),
    ("명문 겐카이GC도 일부 플랜이 예약 사이트에 게재. 회원 소개 권장이지만 빈자리 확인부터 시작하세요.", "예약은 회원 본인만 가능한 완전 예약제. 게스트는 공식 사이트의 게스트 신청서 (이메일·팩스)로 신청합니다."),
    # 近くのコース (古賀・芥屋は予約サイトで予約できない)
    ('<a href="course-koga.html" class="related-card"><span class="related-card-name">古賀GC（予約可）</span>', '<a href="course-newui.html" class="related-card"><span class="related-card-name">NEWユーアイGC（宗像・予約可）</span>'),
    ('<a href="course-keya.html" class="related-card"><span class="related-card-name">芥屋GC（予約可）</span>', '<a href="course-hisayama.html" class="related-card"><span class="related-card-name">久山CC（予約可）</span>'),
    ('<a href="course-koga.html" class="related-card"><span class="related-card-name">Koga GC (bookable)</span>', '<a href="course-newui.html" class="related-card"><span class="related-card-name">NEW UI GC (Munakata · bookable)</span>'),
    ('<a href="course-keya.html" class="related-card"><span class="related-card-name">Keya GC (bookable)</span>', '<a href="course-hisayama.html" class="related-card"><span class="related-card-name">Hisayama CC (bookable)</span>'),
    ('<a href="course-koga.html" class="related-card"><span class="related-card-name">코가 GC (예약가능)</span>', '<a href="course-newui.html" class="related-card"><span class="related-card-name">NEW UI GC (무나카타·예약가능)</span>'),
    ('<a href="course-keya.html" class="related-card"><span class="related-card-name">케야 GC (예약가능)</span>', '<a href="course-hisayama.html" class="related-card"><span class="related-card-name">히사야마 CC (예약가능)</span>'),
    # 口コミ
    ('<h2 class="sec-title">Threadsでの評判</h2>', '<h2 class="sec-title">口コミ・評判（Threadsの声）</h2>'),
]


def faq_html():
    items = "\n".join(f'''      <div style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:14px;">
        <p style="font-weight:700;color:var(--forest);margin-bottom:8px;">Q. {q}</p>
        <p style="color:var(--charcoal);line-height:1.9;margin:0;">{a}</p>
      </div>''' for q, a in FAQ)
    return f'''  <!-- genkai-faq-v1 -->
  <section class="section section-sand">
    <div class="sec-eyebrow">— FAQ</div>
    <h2 class="sec-title">よくある質問</h2>
    <div style="max-width:820px;margin-top:8px;">
{items}
    </div>
  </section>

'''


for root in ROOTS:
    p = os.path.join(root, F)
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    new = s.replace("\r\n", "\n")
    n, miss = 0, []
    for a, b in R:
        if a in new and b not in new:
            new = new.replace(a, b); n += 1
        elif b not in new:
            miss.append(a[:40])
    new = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', new, count=1)
    new = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', new, count=1)
    if "genkai-faq-v1" not in new:
        anchor = '  <section class="section">\n    <div class="sec-eyebrow">— Contact</div>\n    <h2 class="sec-title">連絡先・公式情報</h2>'
        assert new.count(anchor) == 1, new.count(anchor)
        new = new.replace(anchor, faq_html() + anchor)
        d = {"@context": "https://schema.org", "@type": "FAQPage",
             "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
        new = new.replace("</head>", '  <script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + "\n  </script>\n</head>", 1)
        n += 1
    new = new.replace("\n", nl)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
        json.loads(m.group(1))
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    left = [x for x in ("21,900〜¥23,900", "25,900〜¥27,900", "2026年4-9月", "April-September 2026", "2026년 4-9월", "古賀GC（予約可）", "Koga GC (bookable)", "코가 GC", "14.5km", "一部の予約サイト", "ビジター枠が限定的") if x in new]
    print(f"{root}: {n} 箇所{' (変更なし)' if new == s else ''} 未一致: {miss} 残り: {left}")
    if APPLY and new != s:
        open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
