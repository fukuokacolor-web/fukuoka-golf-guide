#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
門司ゴルフ倶楽部を公式 (https://www.mojigolf.co.jp/ ・2026-11-09 確認) に合わせて書き直す。
  informations/ : 会員の同伴または紹介が必要・予約専用 093-481-0712・平日/土日祝とも3ヶ月前の月初めから受付
                  ゲスト料金 (2026年4月改定・キャディ付・乗用カート込・税込): 通常 ¥27,770/¥32,650・メンバー紹介 ¥22,060/¥29,570
                  メンバー同伴 ¥21,100/¥26,600 (1・2・7・8月 ¥16,860/¥19,890)・ハーフ同伴 ¥11,660/¥13,310・薄暮(同伴要) ¥5,960
                  歩きは1人 ¥1,100 引き・1/2 バッグは割増・70歳以上は利用税 ¥700 免除・休場日 毎週月曜
  access/       : 小倉東IC 6km・新門司IC 4km・都市高速 長野出口 6km・門司IC 9km / 門司駅 タクシー25分 / 小倉駅 タクシー40分
                  北九州空港 タクシー40分 / 福岡空港 車で1時間30分 / クラブバスなし
  about/ course/ ueda/ legacy/ historytile/ : 1934年11月開場・上田治設計 (同氏が手掛けた日本最初のコース)・1953年18H
                  Par72・6,700Y・高麗2グリーン・コースレート73.1/スロープ136 (Full Back)・アリソンバンカー・砲台グリーン
                  クラブハウスはアントニン・レーモンド設計 (1960年)・2014年に国の登録有形文化財
  旧表記の誤り: 空港から75分 (→約90分)・午後スルー (公式に記載なし)・料金未掲載・最寄IC 空欄・定型の褒め言葉・近くのコース (セブンミリオンは福岡市)
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/fix_moji_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARK = "<!-- moji-official-v1 -->"
OFF = "https://www.mojigolf.co.jp/"
INFO = OFF + "informations/"
Y = '<span class="yen">¥</span>'


def card(label, name, amount, note, btn, featured=False):
    return f'''      <div class="price-card{' featured' if featured else ''}">
        <div class="price-card-head">
          <div class="price-card-label">{label}</div>
          <div class="price-card-name">{name}</div>
        </div>
        <div class="price-card-body">
          <div class="price-amount">{amount}</div>
          <div class="price-note">{note}</div>
        </div>
        <div class="price-card-cta">
          <a href="{INFO}" class="btn-book btn-jalan" target="_blank" rel="noopener" style="background:#1a5c38;">{btn}</a>
        </div>
      </div>'''


T = {
"ja": dict(
    fees_title="料金（ゲスト・公式）",
    fees_desc="会員制の倶楽部で、ゲストのプレーには<strong>メンバーの同伴または紹介</strong>が必要です。料金はキャディ付き・乗用カート込み・税込（公式・2026年4月改定）。",
    cards=[("WITH MEMBER", "メンバー同伴", Y + "21,100", "平日。土日祝は ¥26,600。1・2・7・8月は平日 ¥16,860・土日祝 ¥19,890。"),
           ("INTRODUCED", "メンバーの紹介", Y + "22,060", "平日。土日祝は ¥29,570。"),
           ("STANDARD", "通常（ゲスト）", Y + "27,770", "平日。土日祝は ¥32,650。")],
    btn="🏛️ 公式の料金表 →",
    note="<strong>💡 補足（公式・2026年11月9日確認）:</strong> 歩きでのプレーは1人 ¥1,100 引き。料金は4・3バッグの基本料金で、1・2バッグは割増です。ハーフ（メンバー同伴）は平日 ¥11,660・土日祝 ¥13,310、薄暮（会員の同伴が必要）は ¥5,960。70歳以上はゴルフ場利用税 ¥700 が免除。休場日は毎週月曜日（祝日の場合は翌日）。",
    course_p="1934年（昭和9年）11月に9ホールで開場した、北九州の老舗クラブ。設計は上田治で、公式サイトによると同氏が手掛けた日本最初のコースです。1953年に18ホールへ拡張。老松の林間に、アリソンバンカーや砲台グリーンが残ります。",
    checks=[("上田治の処女作「松ヶ江コース」", "18ホール・Par72・6,700ヤード。高麗の2グリーン。コースレート73.1・スロープ136（フルバック・公式）。"),
            ("文化財のクラブハウス", "アントニン・レーモンド設計（1960年完成）。2014年にクラブハウスとスタートハウスが国の登録有形文化財に。"),
            ("初代理事長は出光佐三", "門司港の財界人らが中心になって設立。キャディ付き・乗用カートでのラウンドが基本です。")],
    acc_desc="車が便利です。クラブバスはありません（公式）。",
    acc=[("✈️", "From Fukuoka Airport", "車で約1時間30分"), ("🚄", "From Kokura Station", "タクシーで約40分"), ("🛣️", "Nearest IC", "小倉東IC 6km・新門司IC 4km")],
    acc_tip="北九州市内からは都市高速の長野出口から6km、下関方面からは門司ICから9km。電車なら JR門司駅からタクシーで約25分（約3,500円）、北九州空港からはタクシーで約40分（いずれも公式）。",
    play_title="ラウンドの形",
    play=[("⛳", "キャディ付き・乗用カート", "料金はキャディ付き・乗用カート込み。歩きを希望する組は1人 ¥1,100 引き（公式）。"),
          ("🌇", "薄暮プレー", "会員の同伴が必要で ¥5,960。ロッカーと浴場は使えません（公式）。")],
    book_desc="会員制のため、ゲストはメンバーの同伴または紹介が必要です。予約は予約専用電話（093-481-0712）で、平日・土日祝とも3ヶ月前の月初めから受け付けています。じゃらんゴルフ・楽天GORAでは予約できません（公式）。",
    related=[("course-kokura.html", "小倉CC"), ("course-wakamatsu.html", "若松GC")],
    badges=["🏛️ 1934年開場", "⛳ 18H・Par72", "🎟️ 会員の同伴・紹介が必要"],
    stats=[("1934", "", "開場"), ("6,700", "Y", "Par 72"), ("90", "min", "From Airport"), ("¥21,100", "〜", "同伴・平日")],
    micro="ℹ️ 会員制：ゲストはメンバーの同伴または紹介が必要 ｜ 予約サイトでは予約できません（予約専用 093-481-0712）",
),
"en": dict(
    fees_title="Green fees (guests, official)",
    fees_desc="A private members' club: guests must play <strong>with a member or be introduced by one</strong>. Fees include caddy and riding cart, tax included (official, revised April 2026).",
    cards=[("WITH MEMBER", "With a member", Y + "21,100", "Weekday. Weekend ¥26,600. Jan, Feb, Jul, Aug: weekday ¥16,860 / weekend ¥19,890."),
           ("INTRODUCED", "Introduced by a member", Y + "22,060", "Weekday. Weekend ¥29,570."),
           ("STANDARD", "Standard guest rate", Y + "27,770", "Weekday. Weekend ¥32,650.")],
    btn="🏛️ Official fee table →",
    note="<strong>💡 Notes (official, checked 9 Nov 2026):</strong> Walking rounds are ¥1,100 off per person. Fees assume 3–4 players; 1–2 bags cost extra. Half round with a member: weekday ¥11,660 / weekend ¥13,310. Twilight (member must accompany): ¥5,960. Age 70+ exempt from the ¥700 golf course tax. Closed on Mondays (the next day if Monday is a holiday).",
    course_p="Opened with 9 holes in November 1934, Moji is one of Kitakyushu's oldest clubs. It was designed by Osamu Ueda — according to the club, the first course he designed in Japan — and extended to 18 holes in 1953. Alison bunkers and elevated greens remain among the old pines.",
    checks=[("Osamu Ueda's first course", "18 holes, par 72, 6,700 yards, two korai greens. Course rating 73.1 / slope 136 from the full back tees (official)."),
            ("A listed clubhouse", "Designed by Antonin Raymond (completed 1960). The clubhouse and starter house became Registered Tangible Cultural Properties in 2014."),
            ("Founded by Moji's business leaders", "Sazo Idemitsu was the first chairman. Rounds are normally played with a caddy and riding cart.")],
    acc_desc="Driving is easiest. There is no club shuttle bus (official).",
    acc=[("✈️", "From Fukuoka Airport", "~1 hr 30 min by car"), ("🚄", "From Kokura Station", "~40 min by taxi"), ("🛣️", "Nearest IC", "Kokura-higashi IC 6 km / Shin-Moji IC 4 km")],
    acc_tip="From Kitakyushu city, 6 km from the Nagano exit of the urban expressway; from Shimonoseki, 9 km from Moji IC. By train, about 25 min by taxi from JR Moji Station (about ¥3,500); about 40 min by taxi from Kitakyushu Airport (all per the club).",
    play_title="How rounds work",
    play=[("⛳", "Caddy and riding cart", "Fees include a caddy and riding cart. Groups who prefer to walk get ¥1,100 off per person (official)."),
          ("🌇", "Twilight play", "Requires a member; ¥5,960. Lockers and baths are not available (official).")],
    book_desc="Guests must play with a member or be introduced by one. Bookings are taken by phone (093-481-0712) from the start of the month three months ahead, weekdays and weekends. Not bookable on Jalan Golf or Rakuten GORA (official).",
    related=[("course-kokura.html", "Kokura CC"), ("course-wakamatsu.html", "Wakamatsu GC")],
    badges=["🏛️ Opened 1934", "⛳ 18 holes, par 72", "🎟️ Member or introduction required"],
    stats=[("1934", "", "Opened"), ("6,700", "Y", "Par 72"), ("90", "min", "From Airport"), ("¥21,100", "+", "With member, weekday")],
    micro="ℹ️ Members' club: guests need a member to accompany or introduce them ｜ Not bookable online (reservations 093-481-0712)",
),
"ko": dict(
    fees_title="요금 (게스트·공식)",
    fees_desc="회원제 클럽으로, 게스트는 <strong>회원 동반 또는 소개</strong>가 필요합니다. 요금은 캐디·승용 카트 포함·세금 포함 (공식·2026년 4월 개정).",
    cards=[("WITH MEMBER", "회원 동반", Y + "21,100", "평일. 주말·공휴일 ¥26,600. 1·2·7·8월은 평일 ¥16,860·주말 ¥19,890."),
           ("INTRODUCED", "회원 소개", Y + "22,060", "평일. 주말·공휴일 ¥29,570."),
           ("STANDARD", "일반 (게스트)", Y + "27,770", "평일. 주말·공휴일 ¥32,650.")],
    btn="🏛️ 공식 요금표 →",
    note="<strong>💡 참고 (공식·2026년 11월 9일 확인):</strong> 도보 라운드는 1인 ¥1,100 할인. 4·3백 기준 요금이며 1·2백은 할증. 하프 (회원 동반) 평일 ¥11,660·주말 ¥13,310, 박모 (회원 동반 필요) ¥5,960. 70세 이상은 골프장 이용세 ¥700 면제. 휴장일은 매주 월요일 (공휴일이면 다음 날).",
    course_p="1934년 11월 9홀로 개장한 기타큐슈의 전통 클럽. 우에다 오사무가 설계했으며, 공식 사이트에 따르면 그가 일본에서 처음 설계한 코스입니다. 1953년 18홀로 확장. 노송 숲 사이에 앨리슨 벙커와 포대 그린이 남아 있습니다.",
    checks=[("우에다 오사무의 첫 코스", "18홀·파72·6,700야드. 고라이 2그린. 코스레이트 73.1·슬로프 136 (풀백·공식)."),
            ("문화재 클럽하우스", "안토닌 레이먼드 설계 (1960년 완공). 2014년 클럽하우스와 스타트하우스가 국가 등록유형문화재로."),
            ("초대 이사장은 이데미쓰 사조", "모지항 경제인들이 중심이 되어 설립. 캐디·승용 카트 라운드가 기본입니다.")],
    acc_desc="자동차가 편리합니다. 클럽 버스는 없습니다 (공식).",
    acc=[("✈️", "후쿠오카공항에서", "차로 약 1시간 30분"), ("🚄", "고쿠라역에서", "택시로 약 40분"), ("🛣️", "최근 IC", "고쿠라히가시 IC 6km·신모지 IC 4km")],
    acc_tip="기타큐슈 시내에서는 도시고속 나가노 출구에서 6km, 시모노세키 방면에서는 모지 IC에서 9km. 전철은 JR 모지역에서 택시로 약 25분 (약 3,500엔), 기타큐슈공항에서 택시로 약 40분 (모두 공식).",
    play_title="라운드 방식",
    play=[("⛳", "캐디·승용 카트", "요금에 캐디와 승용 카트 포함. 도보를 원하는 조는 1인 ¥1,100 할인 (공식)."),
          ("🌇", "박모 플레이", "회원 동반 필요·¥5,960. 로커와 욕장은 이용할 수 없습니다 (공식).")],
    book_desc="회원제이므로 게스트는 회원 동반 또는 소개가 필요합니다. 예약은 예약 전용 전화 (093-481-0712)로 평일·주말 모두 3개월 전 월초부터 접수합니다. 자란골프·라쿠텐 GORA에서는 예약할 수 없습니다 (공식).",
    related=[("course-kokura.html", "고쿠라 CC"), ("course-wakamatsu.html", "와카마쓰 GC")],
    badges=["🏛️ 1934년 개장", "⛳ 18홀·파72", "🎟️ 회원 동반·소개 필요"],
    stats=[("1934", "", "개장"), ("6,700", "Y", "Par 72"), ("90", "분", "공항에서"), ("¥21,100", "~", "회원 동반 평일")],
    micro="ℹ️ 회원제: 게스트는 회원 동반 또는 소개 필요 ｜ 예약 사이트에서는 예약 불가 (예약 전용 093-481-0712)",
),
}

FAQ = [
    ("門司ゴルフ倶楽部の料金は？", "公式の料金表（2026年4月改定・キャディ付き・乗用カート込み・税込）では、メンバー同伴で平日 ¥21,100・土日祝 ¥26,600、メンバーの紹介で平日 ¥22,060・土日祝 ¥29,570、通常のゲスト料金は平日 ¥27,770・土日祝 ¥32,650です。1・2・7・8月のメンバー同伴は平日 ¥16,860・土日祝 ¥19,890です。"),
    ("ビジターだけで予約できる？", "公式サイトに「当倶楽部は会員の同伴または紹介が必要です」とあります。予約は予約専用電話 093-481-0712 で、平日・土日祝とも3ヶ月前の月初めから受け付けています。じゃらんゴルフ・楽天GORAでは予約できません。"),
    ("ドレスコードは？", "男性は来場時にジャケット・ブレザーなどの上着が必要です（6〜9月は手に持っての来場も可）。ジーンズ・カーゴパンツ・迷彩柄・短パン、サンダルやゴルフシューズでの来場はできません。プレー中は襟付きシャツで裾をズボンに入れ、くるぶしが隠れるソックスを履いてください（公式）。"),
    ("アクセスは？", "九州自動車道の小倉東ICから6km、または新門司ICから4kmです。公式サイトでは福岡空港から車で1時間30分、小倉駅からタクシーで約40分、JR門司駅からタクシーで約25分と案内しています。クラブバスはありません。"),
    ("どんなコース？口コミは？", "1934年開場、上田治が設計した18ホール・Par72・6,700ヤードのコースで、クラブハウスは国の登録有形文化財です。このページの「口コミ・評判」欄にThreadsの声を要約していて、レトロで美しいクラブハウスと、手強いアリソンバンカーを挙げる声があります。"),
]

TITLE = "門司ゴルフ倶楽部の料金・予約方法・ドレスコード・アクセス｜口コミも | 福岡ゴルフ場ガイド"
DESC = "門司ゴルフ倶楽部（北九州市門司区・1934年開場、上田治設計）の料金はメンバー同伴で平日¥21,100・土日祝¥26,600（キャディ付・税込・公式）。ゲストはメンバーの同伴か紹介が必要です。予約方法・ドレスコード・アクセス・口コミもまとめました。"
GC_DESC = "門司ゴルフ倶楽部（北九州市門司区）。1934年開場、上田治設計の18ホール・Par72。クラブハウスはアントニン・レーモンド設計で国の登録有形文化財。ゲストはメンバーの同伴または紹介が必要。"


def lang_block(s, tag):
    i = s.find(tag)
    j = min([x for x in (s.find('id="c-en"', i + 1), s.find('id="c-ko"', i + 1), len(s)) if x > i])
    return i, j


KO_EYE = {"Green Fees": "그린피", "The Course": "코스 소개", "Getting Here": "오시는 길", "Play Styles": "플레이 스타일",
          "Book Your Tee Time": "티타임 예약", "Contact": "연락처"}
CUR = {"lang": "ja"}


def sec(blk, eyebrow):
    """eyebrow を含む <section ...> ... </section> の範囲 (見つからなければ止める)"""
    if CUR["lang"] == "ko":
        eyebrow = KO_EYE[eyebrow]
    k = blk.find(f'<div class="sec-eyebrow">— {eyebrow}</div>')
    assert k >= 0, (CUR["lang"], eyebrow)
    a = blk.rfind("<section", 0, k)
    b = blk.find("</section>", k) + len("</section>")
    return a, b


def rewrite_block(blk, L):
    CUR["lang"] = L
    d = T[L]
    # hero badges
    blk = re.sub(r'(<div class="hero-badges">\n).*?(\n      </div>)',
                 lambda m: m.group(1) + "\n".join(f'        <span class="hero-badge">{b}</span>' for b in d["badges"]) + m.group(2), blk, count=1, flags=re.S)
    blk = re.sub(r'<div class="ftv-cta-microcopy">[^<]*</div>', f'<div class="ftv-cta-microcopy">{d["micro"]}</div>', blk, count=1)
    blk = re.sub(r'(<div class="stats-inner">\n).*?(\n    </div>)',
                 lambda m: m.group(1) + "\n".join(f'      <div class="stat-item"><div class="stat-num">{n}<span class="unit">{u}</span></div><div class="stat-label">{l}</div></div>' for n, u, l in d["stats"]) + m.group(2),
                 blk, count=1, flags=re.S)
    # fees
    a, b = sec(blk, "Green Fees")
    fees = f'''<section class="section">
    {MARK if L == "ja" else ""}
    <div class="sec-eyebrow">— Green Fees</div>
    <h2 class="sec-title">{d["fees_title"]}</h2>
    <p class="sec-desc">{d["fees_desc"]}</p>
    <div class="pricing-grid">
''' + "\n\n".join(card(x[0], x[1], x[2], x[3], d["btn"], featured=(k == 0)) for k, x in enumerate(d["cards"])) + f'''
    </div>
    <div style="max-width:780px;margin:24px auto 0;padding:14px 20px;background:#fff8e6;border-left:4px solid #c9a227;border-radius:4px;font-size:13px;color:#5a3e00;">
      {d["note"]}
    </div>
  </section>'''
    blk = blk[:a] + fees + blk[b:]
    # course
    a, b = sec(blk, "The Course")
    cs = blk[a:b]
    cs = re.sub(r"<p>.*?</p>", f"<p>{d['course_p']}</p>", cs, count=1, flags=re.S)
    cs = re.sub(r'(<ul class="check-list">\n).*?(\n        </ul>)',
                lambda m: m.group(1) + "\n".join(f'          <li><span class="check-icon">✓</span><div><strong>{h}</strong>{t}</div></li>' for h, t in d["checks"]) + m.group(2), cs, count=1, flags=re.S)
    blk = blk[:a] + cs + blk[b:]
    # access
    a, b = sec(blk, "Getting Here")
    ac = blk[a:b]
    ac = re.sub(r'<p class="sec-desc">.*?</p>', f'<p class="sec-desc">{d["acc_desc"]}</p>', ac, count=1, flags=re.S)
    ac = re.sub(r'(<div class="access-grid">\n).*?(\n    </div>)',
                lambda m: m.group(1) + "\n".join(f'      <div class="access-card"><div class="access-icon">{i}</div><div class="access-label">{l}</div><div class="access-value">{v}</div></div>' for i, l, v in d["acc"]) + m.group(2), ac, count=1, flags=re.S)
    ac = re.sub(r'(<div class="access-tip"><span class="access-tip-icon">💡</span><div>)[^<]*', lambda m: m.group(1) + d["acc_tip"], ac, count=1)
    blk = blk[:a] + ac + blk[b:]
    # play styles
    a, b = sec(blk, "Play Styles")
    ps = blk[a:b]
    ps = re.sub(r'<h2 class="sec-title">.*?</h2>', f'<h2 class="sec-title">{d["play_title"]}</h2>', ps, count=1)
    ps = re.sub(r'(<div class="play-grid">\n).*?(\n    </div>\n  </section>)',
                lambda m: m.group(1) + "\n".join(f'''      <div class="play-card">
        <div class="play-card-icon">{i}</div>
        <div class="play-card-title">{t}</div>
        <div class="play-card-desc">{x}</div>
      </div>''' for i, t, x in d["play"]) + m.group(2), ps, count=1, flags=re.S)
    blk = blk[:a] + ps + blk[b:]
    # booking desc
    a, b = sec(blk, "Book Your Tee Time")
    bk = re.sub(r'(<p class="sec-desc" style="margin:0 auto 0;">).*?(</p>)', lambda m: m.group(1) + d["book_desc"] + m.group(2), blk[a:b], count=1, flags=re.S)
    blk = blk[:a] + bk + blk[b:]
    # related
    blk = re.sub(r'(<div class="related-cards">\n).*?(\n      </div>)',
                 lambda m: m.group(1) + "\n".join(f'        <a href="{h}" class="related-card"><span class="related-card-name">{n}</span><span class="related-card-arrow">→</span></a>' for h, n in d["related"]) + m.group(2), blk, count=1, flags=re.S)
    if L == "ja":
        blk = blk.replace('<h2 class="sec-title">Threadsでの評判</h2>', '<h2 class="sec-title">口コミ・評判（Threadsの声）</h2>')
        items = "\n".join(f'''      <div style="background:#fff;border:1px solid var(--line);border-radius:14px;padding:20px 22px;margin-bottom:14px;">
        <p style="font-weight:700;color:var(--forest);margin-bottom:8px;">Q. {q}</p>
        <p style="color:var(--charcoal);line-height:1.9;margin:0;">{a_}</p>
      </div>''' for q, a_ in FAQ)
        faq = f'''<section class="section section-sand">
    <div class="sec-eyebrow">— FAQ</div>
    <h2 class="sec-title">よくある質問</h2>
    <div style="max-width:820px;margin-top:8px;">
{items}
    </div>
  </section>

  '''
        a, b = sec(blk, "Contact")
        blk = blk[:a] + faq + blk[a:]
    return blk


def fix_course(s):
    if MARK in s:
        return s
    s = s.replace("<title>門司ゴルフ倶楽部｜料金・アクセス | 福岡ゴルフ場ガイド</title>", f"<title>{TITLE}</title>")
    s = s.replace('<meta property="og:title" content="門司ゴルフ倶楽部｜料金・アクセス | 福岡ゴルフ場ガイド">', f'<meta property="og:title" content="{TITLE}">')
    old = "門司ゴルフクラブ（北九州市門司区）の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約75分。"
    s = s.replace(f'<meta name="description" content="{old}">', f'<meta name="description" content="{DESC}">')
    s = s.replace(f'<meta property="og:description" content="{old}">', f'<meta property="og:description" content="{DESC}">')
    s = s.replace(f'"description": "{old}"', f'"description": "{GC_DESC}",\n    "priceRange": "¥21,100〜¥32,650"')
    for L in ("ja", "en", "ko"):
        i, j = lang_block(s, f'id="c-{L}"')
        s = s[:i] + rewrite_block(s[i:j], L) + s[j:]
    d = {"@context": "https://schema.org", "@type": "FAQPage",
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
    s = s.replace("</head>", '  <script type="application/ld+json">\n' + json.dumps(d, ensure_ascii=False, indent=2) + "\n  </script>\n</head>", 1)
    return s


ACCESS = [
    ("福岡空港からは車で約75分。", "福岡空港からは車で約1時間30分（公式）。"),
    ("<li>小倉東ICで降りる（約60〜65分）</li>", "<li>小倉東ICで降りる</li>"),
    ("<li>小倉東ICから門司区吉志方面へ約6km・約15分走行</li>", "<li>小倉東ICから門司区吉志方面へ約6km（新門司ICからなら約4km）</li>"),
    ("<li>合計：福岡空港から車で約75分</li>", "<li>合計：福岡空港から車で約1時間30分（公式）</li>"),
    ("<li>ICから吉志方面へ約6km・約15分</li>", "<li>ICから吉志方面へ約6km（北九州都市高速の長野出口からも約6km）</li>"),
    ("<li>小倉駅からは車で約20分</li>", "<li>小倉駅からはタクシーで約40分（約4,000円）</li>"),
    ("JR日豊本線「下曾根駅」から車で約10分、「門司駅」から約20分。北九州観光やレトロ門司港と組み合わせたプランに最適です。", "JR門司駅からタクシーで約25分（約3,500円）。クラブバスはありません（公式）。"),
    ("JR日豊本線「下曾根駅」から車で約10分（タクシー推奨）、または「門司駅」から約20分。", "JR門司駅からタクシーで約25分（約3,500円）、新幹線の小倉駅からタクシーで約40分（約4,000円）です（公式）。クラブバスはありません。"),
    ("~75 min from Fukuoka Airport by car.", "~1 hr 30 min from Fukuoka Airport by car."),
    ("About 75 min from Fukuoka Airport.", "About 1 hr 30 min from Fukuoka Airport (official)."),
    ("<li>Exit at Kokurahigashi IC (approx. 60–65 min)</li>", "<li>Exit at Kokurahigashi IC</li>"),
    ("<li>Head toward Yoshishi, Moji-ku — approx. 6 km / 15 min from IC</li>", "<li>Head toward Yoshishi, Moji-ku — about 6 km from the IC (about 4 km from Shin-Moji IC)</li>"),
    ("<li>Total: approx. 75 min from Fukuoka Airport</li>", "<li>Total: about 1 hr 30 min from Fukuoka Airport (official)</li>"),
    ("<li>Head toward Yoshishi — approx. 6 km / 15 min</li>", "<li>Head toward Yoshishi — about 6 km (also about 6 km from the Nagano exit of the Kitakyushu Urban Expressway)</li>"),
    ("<li>Approx. 20 min from Kokura Station</li>", "<li>About 40 min by taxi from Kokura Station (about ¥4,000)</li>"),
    ('About 10 min by taxi from JR "Shimozōne Station," or 20 min from "Moji Station." Great for combining with a visit to retro Mojiko Port.', 'About 25 min by taxi from JR Moji Station (about ¥3,500). There is no club bus (official).'),
    ('JR Nippo Main Line "Shimozōne Station" — approx. 10 min by taxi. Or "Moji Station" — approx. 20 min by taxi.', 'About 25 min by taxi from JR Moji Station (about ¥3,500), or about 40 min by taxi from Kokura Station on the Shinkansen (about ¥4,000), per the club. There is no club bus.'),
    ("후쿠오카 공항에서 차로 약 75분.", "후쿠오카 공항에서 차로 약 1시간 30분 (공식)."),
    ("후쿠오카공항에서 차로 약 75분.\">", "후쿠오카공항에서 차로 약 1시간 30분.\">"),
    ("<li>고쿠라히가시 IC에서 하차 (약 60〜65분)</li>", "<li>고쿠라히가시 IC에서 하차</li>"),
    ("<li>모지구 요시시 방면으로 약 6km·약 15분 주행</li>", "<li>모지구 요시시 방면으로 약 6km (신모지 IC에서는 약 4km)</li>"),
    ("<li>합계: 후쿠오카 공항에서 차로 약 75분</li>", "<li>합계: 후쿠오카 공항에서 차로 약 1시간 30분 (공식)</li>"),
    ("<li>요시시 방면으로 약 6km·약 15분</li>", "<li>요시시 방면으로 약 6km (기타큐슈 도시고속 나가노 출구에서도 약 6km)</li>"),
    ("<li>고쿠라역에서 약 20분</li>", "<li>고쿠라역에서 택시로 약 40분 (약 4,000엔)</li>"),
    ("JR 「시모조네역」에서 택시로 약 10분, 「모지역」에서 약 20분. 레트로 모지코 항구 관광과 조합하기에도 최적입니다.", "JR 모지역에서 택시로 약 25분 (약 3,500엔). 클럽 버스는 없습니다 (공식)."),
    ("JR 닛포 본선 「시모조네역」에서 택시로 약 10분, 또는 「모지역」에서 약 20분.", "JR 모지역에서 택시로 약 25분 (약 3,500엔), 신칸센 고쿠라역에서 택시로 약 40분 (약 4,000엔) (공식). 클럽 버스는 없습니다."),
]
FAQPAGE = [("最長約75分（北九州・門司エリア）", "最長で約1時間30分（門司ゴルフ倶楽部・公式）")]


def apply_list(s, rules):
    n = 0
    for a, b in rules:
        if a in s:
            s = s.replace(a, b); n += 1
    return s, n


for root in ROOTS:
    print(root)
    for f, fn in (("course-moji.html", "course"), ("access-moji.html", "access"), ("faq.html", "faq")):
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        w = s.replace("\r\n", "\n")
        if fn == "course":
            new = fix_course(w); n = "rewrite" if new != w else 0
        elif fn == "access":
            new, n = apply_list(w, ACCESS)
        else:
            new, n = apply_list(w, FAQPAGE)
        new = new.replace("\n", nl)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        left = [x for x in ("75分", "75 min", "75분", "午後スルー", "Afternoon Through", "오후 스루", "下曾根", "Shimozōne", "시모조네", "セブンミリオン", "最寄IC</div>", "年間通して良好") if x in new.split('id="c-ja"')[-1] or (fn != "course" and x in new)]
        if fn == "faq":
            left = [x for x in ("最長約75分",) if x in new]
        print(f"  {f}: {n} {'(変更なし)' if new == s else ''} 残り: {left}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
