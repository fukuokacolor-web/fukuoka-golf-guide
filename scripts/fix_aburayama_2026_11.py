#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ララヒルズ油山の料金・遊び方を楽天GORA (c_id 520392・2026-11-09 確認) の掲載に合わせる。公式サイトは見当たらない。
  楽天GORA 予約カレンダー (総額・税込): 土日祝 10H セルフ 歩き ¥5,900 / 乗用カート ¥6,400、20H セルフ 歩き ¥7,900 / 乗用カート ¥9,900
  楽天GORA ゴルフ場からのお知らせ: 2026年9月より乗用カート導入 (歩きも可)・手引きカート/ハーフバッグ レンタル ¥550
                                 平日は予約不要・受付順 / キャンセル料 3日前から1人 ¥1,000 / 休場日 12/31
  旧表記の誤り: 平日 ¥3,000〜4,500・土日祝 ¥3,200〜4,500 (根拠なし)・午後スルー ¥5,000〜8,000 / 18ホール (10Hのショートコースに合わない)
               「通常ラウンド 午前スタート・18ホール」・「2026年9月より乗用カート導入予定」(導入済み)
  平日の料金は掲載がないため「(要追加調査)」とし、電話での確認を案内する。
冪等。改行コードはそのまま。Usage: python scripts/fix_aburayama_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
F = "course-aburayama.html"
Y = '<span class="yen">¥</span>'

CARDS = {
    "ja": [("WEEKDAY", "平日", '<span style="font-size:19px;">予約不要・受付順</span>', "平日は予約なしで来場した順にプレー（楽天GORAのお知らせ）。料金は掲載がないため電話（092-871-2515）でご確認ください。"),
           ("WEEKEND / 10 HOLES", "土日祝 10ホール", Y + "5,900", "セルフ・歩き（総額・税込）。乗用カートは ¥6,400。楽天GORAの掲載プラン（2026年11月9日確認）。"),
           ("WEEKEND / 20 HOLES", "土日祝 20ホール", Y + "7,900", "10ホールを2周。セルフ・歩き（総額・税込）。乗用カートは ¥9,900。楽天GORAの掲載プラン。")],
    "en": [("WEEKDAY", "Monday–Friday", '<span style="font-size:19px;">No booking needed</span>', "On weekdays, play is first come, first served (notice on Rakuten GORA). Weekday fees are not listed — call 092-871-2515."),
           ("WEEKEND / 10 HOLES", "Weekend, 10 holes", Y + "5,900", "Self-play, walking (total incl. tax). With a riding cart ¥6,400. Plans on Rakuten GORA, checked 9 Nov 2026."),
           ("WEEKEND / 20 HOLES", "Weekend, 20 holes", Y + "7,900", "Two loops of the 10 holes. Self-play, walking (total incl. tax). With a riding cart ¥9,900.")],
    "ko": [("WEEKDAY", "평일", '<span style="font-size:19px;">예약 불필요·선착순</span>', "평일은 예약 없이 도착 순으로 플레이 (라쿠텐 GORA 공지). 평일 요금은 게재되어 있지 않으므로 전화 (092-871-2515)로 확인해 주세요."),
           ("WEEKEND / 10 HOLES", "주말·공휴일 10홀", Y + "5,900", "셀프·도보 (총액·세금 포함). 승용 카트는 ¥6,400. 라쿠텐 GORA 게재 플랜 (2026년 11월 9일 확인)."),
           ("WEEKEND / 20 HOLES", "주말·공휴일 20홀", Y + "7,900", "10홀을 2바퀴. 셀프·도보 (총액·세금 포함). 승용 카트는 ¥9,900.")],
}
DESC_SEC = {
    "ja": "楽天GORAに掲載されている土日祝のプラン（2026年11月9日確認・総額）。平日は予約不要の受付順です。",
    "en": "Weekend plans listed on Rakuten GORA (checked 9 Nov 2026, total price). On weekdays no booking is needed.",
    "ko": "라쿠텐 GORA에 게재된 주말·공휴일 플랜 (2026년 11월 9일 확인·총액). 평일은 예약 없이 선착순입니다.",
}
PLAY = {
    "ja": [("⛳", "10ホール・20ホール", "10ホール（2グリーン）を1周、または2周して20ホール。Par3中心で、最長345ヤードのミドルホールもあります。"),
           ("🛺", "歩き・乗用カート", "2026年9月から乗用カートを導入（歩きも可）。手引きカート・ハーフバッグのレンタルは各 ¥550（楽天GORAのお知らせ）。")],
    "en": [("⛳", "10 or 20 holes", "Play the 10 holes (two greens) once, or twice for 20 holes. Mostly par 3s, with a downhill par 4 of up to 345 yards."),
           ("🛺", "Walk or ride", "Riding carts were added in September 2026; walking is still allowed. Pull carts and half bags can be rented for ¥550 each (Rakuten GORA notice).")],
    "ko": [("⛳", "10홀·20홀", "10홀 (2그린)을 1바퀴, 또는 2바퀴 돌아 20홀. 파3 중심이며 최장 345야드의 미들홀도 있습니다."),
           ("🛺", "도보·승용 카트", "2026년 9월부터 승용 카트 도입 (도보도 가능). 수동 카트·하프백 대여는 각 ¥550 (라쿠텐 GORA 공지).")],
}
PLAY_TITLE = {"ja": "遊び方", "en": "How to play", "ko": "플레이 방식"}
EYE = {"ja": ("— Green Fees", "— Play Styles"), "en": ("— Green Fees", "— Play Styles"), "ko": ("— 그린피", "— 플레이 스타일")}

FAQ_OLD_HTML = "<strong>楽天GORA</strong>からオンライン予約が可能です（ララヒルズ油山はじゃらんゴルフには掲載なし）。料金は時期・プランで変動するため、最新は楽天GORAまたは公式サ"
FAQ_NEW = "楽天GORAで土日祝のプランを予約できます（じゃらんゴルフには掲載なし）。2026年11月9日時点の楽天GORAの総額は、10ホールが歩き ¥5,900・乗用カート ¥6,400、20ホールが歩き ¥7,900・乗用カート ¥9,900。平日は予約不要の受付順です。キャンセル料は3日前から1人 ¥1,000。"

TITLE = "ララヒルズ油山（旧 油山ゴルフクラブ）の料金・予約・アクセス｜10Hショートコース・福岡市城南区 | 福岡ゴルフ場ガイド"
DESC = "ララヒルズ油山（旧 油山ゴルフクラブ・福岡市城南区）は全10ホール2グリーンのショートコース。土日祝は10ホール¥5,900・20ホール¥7,900（歩き・総額・楽天GORA）、平日は予約不要の受付順。2026年9月から乗用カートあり。堤ICから約8分。"

SIMPLE = [
    ("<title>ララヒルズ油山（旧 油山ゴルフクラブ）｜10Hショートコース・福岡市城南区 | 福岡ゴルフ場ガイド</title>", f"<title>{TITLE}</title>"),
    ("2026年5月現在、通常営業中（2026年9月より乗用カート導入予定）。", "2026年9月から乗用カートを導入しています（歩きも可）。"),
    # 英語・韓国語のテンプレート文 (根拠なし) を日本語版の内容に合わせる
    ("<p>A well-balanced layout in 福岡市城南区, with nicely maintained fairways and a course design suited to all skill levels. About 25〜30 minutes from Fukuoka Airport by car — a perfect day-trip destination.</p>",
     "<p>A 10-hole short course with two greens in Higashi-Aburayama, Jonan-ku, Fukuoka City (formerly Aburayama Golf Club; clubhouse renewed in 2025). Mostly par 3s, with a downhill par 4 of up to 345 yards and a short hole over a valley. From the hillside you can see the city, PayPay Dome and Fukuoka Tower.</p>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>Year-round great conditions</strong>Consistently maintained fairways and greens, enjoyable for every skill level.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>10 holes, two greens</strong>Mostly par 3s — good for practice rounds, beginners and short on time days.</div></li>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>25〜30 min from Fukuoka Airport</strong>Easy by rental car or courtesy bus.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>About 8 min from Tsutsumi IC</strong>Close to the city on the Fukuoka Urban Expressway.</div></li>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>Flexible play styles</strong>Choose morning rounds with a half-turn break, or afternoon-through for half-day value.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>10 or 20 holes</strong>Play the loop once, or twice for 20 holes. Riding carts since September 2026; walking is fine too.</div></li>"),
    ("<p>福岡市城南区에 위치한 균형 잡힌 코스. 잘 정비된 페어웨이와 전략적인 레이아웃으로 초보자부터 상급자까지 모두 즐길 수 있습니다. 후쿠오카공항에서 차로 약 25〜30분로 당일치기 여행에도 최적입니다.</p>",
     "<p>후쿠오카시 조난구 히가시아부라야마에 있는 10홀·2그린 쇼트 코스 (구 아부라야마 골프클럽, 2025년 클럽하우스 리뉴얼). 파3 중심이며 최장 345야드의 내리막 미들홀과 계곡을 넘는 쇼트홀도 있습니다. 언덕에서 시내와 PayPay돔, 후쿠오카타워가 보입니다.</p>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>연중 쾌적한 코스 컨디션</strong>정비된 페어웨이와 그린으로 편안하게 플레이할 수 있습니다.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>10홀·2그린 쇼트 코스</strong>파3 중심으로 연습 라운드·초보자·시간이 없는 날에 적합합니다.</div></li>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>후쿠오카공항에서 25〜30분</strong>렌터카나 셔틀로 간편하게 도착합니다.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>쓰쓰미 IC에서 약 8분</strong>후쿠오카 도시고속도로에서 가까운 시내권 코스입니다.</div></li>"),
    ("<li><span class=\"check-icon\">✓</span><div><strong>유연한 플레이 스타일</strong>오전 라운드·오후 스루 등 시간과 예산에 맞춰 선택할 수 있습니다.</div></li>",
     "<li><span class=\"check-icon\">✓</span><div><strong>10홀·20홀 선택</strong>1바퀴 또는 2바퀴 (20홀). 2026년 9월부터 승용 카트 도입, 도보도 가능.</div></li>"),
]


def block(s, L):
    i = s.find(f'id="c-{L}"')
    j = min([x for x in (s.find('id="c-en"', i + 1), s.find('id="c-ko"', i + 1), len(s)) if x > i])
    return i, j


def section(blk, eye):
    k = blk.find(f'<div class="sec-eyebrow">{eye}</div>')
    assert k >= 0, eye
    return blk.rfind("<section", 0, k), blk.find("</section>", k) + len("</section>")


def fix_block(blk, L):
    a, b = section(blk, EYE[L][0])
    sec = blk[a:b]
    if "5,900" not in sec:
        sec = re.sub(r'<p class="sec-desc">.*?</p>', f'<p class="sec-desc">{DESC_SEC[L]}</p>', sec, count=1, flags=re.S)
        cards = list(re.finditer(r'(<div class="price-card-label">)[^<]*(</div>\s*<div class="price-card-name">)[^<]*(</div>.*?<div class="price-amount">).*?(</div>\s*<div class="price-note">).*?(</div>)', sec, re.S))
        assert len(cards) == 3, len(cards)
        for m, (lab, name, amt, note) in reversed(list(zip(cards, CARDS[L]))):
            rep = m.group(1) + lab + m.group(2) + name + m.group(3) + amt + m.group(4) + note + m.group(5)
            sec = sec[:m.start()] + rep + sec[m.end():]
        blk = blk[:a] + sec + blk[b:]
    a, b = section(blk, EYE[L][1])
    ps = blk[a:b]
    if "20" not in re.sub(r"<[^>]+>", "", ps):
        ps = re.sub(r'<h2 class="sec-title">.*?</h2>', f'<h2 class="sec-title">{PLAY_TITLE[L]}</h2>', ps, count=1)
        ps = re.sub(r'(<div class="play-grid">\n).*?(\n    </div>\n  </section>)',
                    lambda m: m.group(1) + "\n".join(f'''      <div class="play-card">
        <div class="play-card-icon">{i}</div>
        <div class="play-card-title">{t}</div>
        <div class="play-card-desc">{x}</div>
      </div>''' for i, t, x in PLAY[L]) + m.group(2), ps, count=1, flags=re.S)
        blk = blk[:a] + ps + blk[b:]
    if L == "ja":
        blk = blk.replace('<h2 class="sec-title">Threadsでの評判</h2>', '<h2 class="sec-title">口コミ・評判（Threadsの声）</h2>')
        blk = re.sub(re.escape(FAQ_OLD_HTML) + r"[^<]*", FAQ_NEW, blk, count=1)
    return blk


for root in ROOTS:
    p = os.path.join(root, F)
    s = open(p, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in s else "\n"
    new = s.replace("\r\n", "\n")
    for a, b in SIMPLE:
        new = new.replace(a, b)
    new = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{DESC}">', new, count=1)
    new = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESC}">', new, count=1)
    # FAQ 構造化データの料金の答え
    new = re.sub(r'("name":"予約はどこからできますか？料金は？","acceptedAnswer":\{"@type":"Answer","text":")[^"]*(")', lambda m: m.group(1) + FAQ_NEW + m.group(2), new, count=1)
    for L in ("ja", "en", "ko"):
        i, j = block(new, L)
        new = new[:i] + fix_block(new[i:j], L) + new[j:]
    new = new.replace("\n", nl)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
        json.loads(m.group(1))
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    left = [x for x in ("3,000<span", "3,200<span", "5,000<span", "午後スルー", "Afternoon Through", "오후 스루", "導入予定", "平日¥3,000", "料金は時期・プラン") if x in new]
    print(f"{root}: {'変更あり' if new != s else '(変更なし)'} 残り: {left}")
    if APPLY and new != s:
        open(p, "w", encoding="utf-8", newline="").write(new)
# 初心者向けガイドのカード (旧名称・区・料金が古い)
BEG = [
    ('<div class="course-name">油山ゴルフクラブ（ショートコース）</div>', '<div class="course-name">ララヒルズ油山（旧 油山ゴルフクラブ・ショートコース）</div>'),
    ('<span class="course-chip chip-area">福岡市南区 油山</span>', '<span class="course-chip chip-area">福岡市城南区 東油山</span>'),
    ('<span class="course-chip chip-price">¥3,000〜4,500</span>', '<span class="course-chip chip-price">土日祝 10H ¥5,900〜</span>'),
    ("楽天 GORA から予約可能。</p>", "土日祝は楽天 GORA から予約でき、平日は予約不要の受付順です（2026年11月確認）。</p>"),
]
for root in ROOTS:
    p = os.path.join(root, "book-fukuoka-beginner.html")
    s = open(p, encoding="utf-8", newline="").read()
    new = s
    for a, b in BEG:
        if a in new and b not in new:
            new = new.replace(a, b)
    print(f"{p}: {'変更あり' if new != s else '(変更なし)'} 残り: {[x for x in ('¥3,000〜4,500', '福岡市南区 油山') if x in new]}")
    if APPLY and new != s:
        open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
