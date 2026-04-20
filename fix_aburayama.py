#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
油山ゴルフクラブ（現：ララヒルズ油山）の情報訂正：
 - 誤: 18ホール丘陵/山岳コース
 - 正: 10ホール ショートコース（2グリーン制・最長345yd）
 - 電話: 092-871-2515
 - 住所: 福岡市城南区大字東油山169-1
"""
import os, io, sys, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/Owner/fukuoka-golf-guide'

# === course-aburayama.html 修正 ===
path = os.path.join(BASE, 'course-aburayama.html')
with open(path, encoding='utf-8') as f:
    html = f.read()

# --- head meta/title/jsonld ---
replacements = [
    # JA meta
    ('content="油山ゴルフクラブ（福岡市城南区）の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約25〜30分。"',
     'content="油山ゴルフクラブ（現ララヒルズ油山・福岡市城南区）は10ホールのショートコース。2グリーン制・最長345ヤード。初心者・短時間ラウンド向け。福岡空港から約25〜30分。"'),
    # EN meta
    ('content="油山ゴルフクラブ golf course in Fukuoka Prefecture. Hilly mountain layout. Green fees, access map and tee time booking for foreign visitors. ~25〜30 min from Fukuoka Airport by car."',
     'content="Aburayama Golf Club (now Lala Hills Aburayama) is a 10-hole short course in Fukuoka City. Two-green layout, longest hole 345 yards. Ideal for beginners and quick rounds. ~25–30 min from Fukuoka Airport."'),
    # KO meta
    ('content="油山ゴルフクラブ 골프장 (후쿠오카현). 구릉·산악 코스. 그린피·오시는 길·예약 정보를 한국어로 안내합니다. 후쿠오카공항에서 차로 약 25〜30분."',
     'content="아부라야마 골프클럽 (현 라라힐즈 아부라야마·후쿠오카시 조난구)는 10홀 쇼트코스입니다. 2그린제·최장 345야드. 초보자·단시간 라운드 추천. 후쿠오카공항에서 차로 약 25〜30분."'),
    # Title
    ('<title>油山ゴルフクラブ（福岡市）料金・アクセス | 福岡ゴルフ場ガイド</title>',
     '<title>油山ゴルフクラブ（ララヒルズ油山・10Hショート）料金・アクセス | 福岡ゴルフ場ガイド</title>'),
    # OG
    ('<meta property="og:title"       content="油山ゴルフクラブ（福岡市）料金・アクセス | 福岡ゴルフ場ガイド">',
     '<meta property="og:title"       content="油山ゴルフクラブ（ララヒルズ油山・10Hショート）料金・アクセス | 福岡ゴルフ場ガイド">'),
    ('<meta property="og:description" content="油山ゴルフクラブ（福岡市城南区）の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約25〜30分。">',
     '<meta property="og:description" content="10ホールのショートコース。2グリーン制・最長345ヤード。初心者・短時間ラウンド向け。福岡空港から約25〜30分。">'),
    # JSON-LD description in course card
    ('"description": "油山ゴルフクラブ（福岡市城南区）の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約25〜30分。"',
     '"description": "油山ゴルフクラブ（現ララヒルズ油山）は10ホールのショートコース。2グリーン制・最長345ヤード。初心者や短時間ラウンドに最適。"'),
]
for old, new in replacements:
    if old in html:
        html = html.replace(old, new, 1)
        print(f'  OK: replaced head block ({old[:40]}...)')
    else:
        print(f'  MISS: {old[:40]}')

# JSON-LD name — 追加 alternateName
html = html.replace(
    '"name": "油山ゴルフクラブ",\n  "address"',
    '"name": "油山ゴルフクラブ",\n  "alternateName": ["ララヒルズ油山", "Lala Hills Aburayama", "라라힐즈 아부라야마"],\n  "telephone": "092-871-2515",\n  "numberOfHoles": 10,\n  "address"',
    1
)
# address update
html = html.replace(
    '"streetAddress": "油山山麓"',
    '"streetAddress": "大字東油山169-1"'
)

# --- JA section: warning banner + fact-grid + info-bar + 見どころ + contact + play-options ---

# ショートコース警告バナー: JA ja section先頭 (<div id="c-ja" class="content on">の直後)
WARN_JA = '''
  <div style="background:#fff3cd; border:2px solid #e6a817; border-radius:10px; padding:12px 14px; margin-bottom:14px; font-size:0.85rem; line-height:1.65; color:#5a3e00;">
    <strong style="color:#9a5100; font-size:0.95rem;">⚠️ このコースは10ホールのショートコースです</strong><br>
    2グリーン制・最長345ヤード。初心者・練習・短時間プレー向けで、<strong>本格的な18ホールラウンドをご希望の方は他のコースをおすすめ</strong>します。
    <a href="recommend.html" style="color:#7a3500; font-weight:800; text-decoration:underline;">目的別おすすめコース →</a>
  </div>
'''
html = html.replace(
    '<div id="c-ja" class="content on">\n\n  <div class="sec-head">📋 基本情報</div>',
    '<div id="c-ja" class="content on">\n' + WARN_JA + '\n  <div class="sec-head">📋 基本情報</div>',
    1
)

# JA fact-grid
html = html.replace(
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">ホール数</span><span class="f-val">18ホール</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">カート</span><span class="f-val">乗用カート</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">コースタイプ</span><span class="f-val">丘陵・山岳コース</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">ロケーション</span><span class="f-val">油山山麓・城南区</span></div>
        <div class="fact-item"><span class="f-icon">🌤️</span><span class="f-label">午後スルー</span><span class="f-val">要確認</span></div>
        <div class="fact-item"><span class="f-icon">👤</span><span class="f-label">1人予約</span><span class="f-val">要確認</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>福岡市城南区の油山山麓に広がる丘陵・山岳コース。市街地から近く、起伏に富んだダイナミックなコースレイアウトが楽しめます。フェアウェイから油山の自然を堪能できます。</div>''',
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">ホール数</span><span class="f-val">10ホール（2グリーン）</span></div>
        <div class="fact-item"><span class="f-icon">📏</span><span class="f-label">最長ホール</span><span class="f-val">345ヤード</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">カート</span><span class="f-val">手引き／2026/9〜乗用</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">コース種別</span><span class="f-val">山岳ショートコース</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">ロケーション</span><span class="f-val">福岡市城南区 東油山</span></div>
        <div class="fact-item"><span class="f-icon">🏙️</span><span class="f-label">眺望</span><span class="f-val">福岡市街を一望</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>福岡市街地から近く、山の斜面に広がる<strong>10ホールのショートコース</strong>。2グリーン制で気軽に短時間ラウンドが楽しめます。PayPayドームや福岡タワーが見える眺望が特徴で、初心者の練習や観光のついでに最適です。</div>'''
)

# JA 見どころ
html = html.replace(
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">山の斜面を活かした起伏豊かなコース設計が特徴です。高低差を利用したダイナミックなショットが攻略のカギとなり、豊かな自然と眺望を楽しみながら挑戦的なラウンドを満喫できます。</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>山岳コースならではのダイナミズム</strong> — 高低差のあるホールが続き、上級者にも満足のいる攻略性があります。</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>アクセス良好</strong> — 福岡空港から車で約25〜30分のドライブで到着。レンタカーや送迎バスを利用するとスムーズです。</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>ハーフターン休憩あり</strong> — 前半9ホール後にレストランで食事休憩。日本ゴルフ文化を体験できる伝統的なスタイルで楽しめます。</div></li>
      </ul>''',
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">谷越えのショートホールや最長345ヤードの打ち下ろしミドルホールなど、<strong>10ホールに凝縮された戦略性</strong>が魅力。2グリーン制なのでほぼ20通りのレイアウトを楽しめます。</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🌆</span><div><strong>福岡市街の絶景</strong> — PayPayドーム・福岡タワーを見下ろす開放感ある眺望。観光気分でプレーできます。</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">⏱️</span><div><strong>短時間でプレー可能</strong> — 10ホールなので約1.5〜2時間で1ラウンド。福岡観光と組み合わせやすい。</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🔰</span><div><strong>初心者・練習に最適</strong> — プレッシャー少なめでスイング確認に◎。本格ラウンド前の足慣らしにも。</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">💴</span><div><strong>リーズナブル</strong> — 平日3,000円台〜と、気軽に立ち寄れる料金設定。</div></li>
      </ul>'''
)

# JA contact
html = html.replace(
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>住所</strong><br>福岡市城南区（油山山麓）</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>電話</strong><br>公式サイトにてご確認ください</div></div>''',
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>住所</strong><br>〒814-0155 福岡市城南区大字東油山169-1</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>電話</strong><br><a href="tel:0928712515" style="color:var(--accent);font-weight:700;">092-871-2515</a></div></div>'''
)

# JA play-options
html = html.replace(
    '''<div class="play-option">
    <div class="play-option-head"><span>☀️</span>通常ラウンド（18ホール・ハーフ休憩あり）</div>
    <div class="play-option-body">午前スタート。前半9ホール後にレストランで休憩を挟み、後半9ホールをプレー。</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌤️</span>午後スルー（18ホール・休憩なし）</div>
    <div class="play-option-body">昼過ぎスタート。休憩なしで18ホールを続けてプレー。観光との組み合わせにも便利。</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>ハーフラウンド（9ホール）</div>
    <div class="play-option-body">9ホールのみのショートプレー。時間が限られている方や初めての方にもおすすめ。</div>
  </div>''',
    '''<div class="play-option">
    <div class="play-option-head"><span>⛳</span>1ラウンド（10ホール）</div>
    <div class="play-option-body">約1.5〜2時間で完結。観光合間のプレーや初心者の練習に最適。</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🔁</span>2ラウンド（20ホール・2グリーン制）</div>
    <div class="play-option-body">AグリーンとBグリーンで2周すれば実質20ホール。ハーフ休憩を挟んで通常コースに近い感覚。</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>早朝・薄暮プレー</div>
    <div class="play-option-body">時間に応じて気軽にスタート可能。料金も抑えめでコスパ◎。</div>
  </div>'''
)

# --- EN section ---

WARN_EN = '''
  <div style="background:#fff3cd; border:2px solid #e6a817; border-radius:10px; padding:12px 14px; margin-bottom:14px; font-size:0.85rem; line-height:1.65; color:#5a3e00;">
    <strong style="color:#9a5100; font-size:0.95rem;">⚠️ This is a 10-hole SHORT course</strong><br>
    Two-green layout, longest hole 345 yards. Best for beginners, practice or quick rounds — <strong>if you want a full 18-hole round, please choose another course</strong>.
    <a href="recommend.html" style="color:#7a3500; font-weight:800; text-decoration:underline;">Best Courses by Purpose →</a>
  </div>
'''
html = html.replace(
    '<div id="c-en" class="content">\n\n  <div class="sec-head">📋 Course Overview</div>',
    '<div id="c-en" class="content">\n' + WARN_EN + '\n  <div class="sec-head">📋 Course Overview</div>',
    1
)

html = html.replace(
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">Holes</span><span class="f-val">18 holes</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">Cart</span><span class="f-val">Riding cart</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">Course Type</span><span class="f-val">Hillside / Mountain</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">Location</span><span class="f-val">Mt. Aburayama, Jonan-ku</span></div>
        <div class="fact-item"><span class="f-icon">🌤️</span><span class="f-label">Afternoon Through</span><span class="f-val">Confirm on-site</span></div>
        <div class="fact-item"><span class="f-icon">👤</span><span class="f-label">Solo Booking</span><span class="f-val">Confirm on-site</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>Nestled at the foot of Mt. Aburayama in Jonan-ku, Fukuoka City, this hillside course offers dynamic elevation changes and lush scenery just a short drive from the city center.</div>''',
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">Holes</span><span class="f-val">10 holes (2 greens)</span></div>
        <div class="fact-item"><span class="f-icon">📏</span><span class="f-label">Longest hole</span><span class="f-val">345 yd</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">Cart</span><span class="f-val">Push cart / Riding (from Sep 2026)</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">Type</span><span class="f-val">Mountain short course</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">Location</span><span class="f-val">Higashi-Aburayama, Jonan-ku</span></div>
        <div class="fact-item"><span class="f-icon">🏙️</span><span class="f-label">View</span><span class="f-val">Fukuoka cityscape</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>A <strong>10-hole short course</strong> on the slopes above Fukuoka City. The two-green layout lets you play up to 20 different hole setups. Sweeping views of PayPay Dome and Fukuoka Tower — perfect for a quick round, practice, or to combine with sightseeing.</div>'''
)

html = html.replace(
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">A course that makes bold use of mountain slopes for dramatic elevation changes. Reading the hilly lies is key — stunning natural scenery makes the challenge all the more rewarding.</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>Mountain-influenced challenge</strong> — Dramatic elevation changes make this a rewarding test for all skill levels.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>Easy access</strong> — Approximately ~25〜30 min from Fukuoka Airport by car. Rental cars or courtesy buses are recommended.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>Half-turn restaurant break included</strong> — Enjoy a ~40-min lunch break after the front 9. A great way to experience traditional Japanese golf culture.</div></li>
      </ul>''',
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">Ten holes packed with variety — carry-over par-3s and a downhill 345-yard par-4. The two-green setup effectively gives you 20 hole layouts to enjoy.</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🌆</span><div><strong>Fukuoka cityscape view</strong> — PayPay Dome and Fukuoka Tower visible from the tee. Feels as much sightseeing as golf.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">⏱️</span><div><strong>Quick rounds</strong> — 10 holes done in 1.5–2 hours. Easy to pair with a half-day of Fukuoka sightseeing.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🔰</span><div><strong>Beginner-friendly</strong> — Low-pressure setting for swing practice or a warm-up before a real course.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">💴</span><div><strong>Budget-friendly</strong> — Weekday rounds from ¥3,000-range. Walk-in friendly rates.</div></li>
      </ul>'''
)

html = html.replace(
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>Address</strong><br>Jonan-ku, Fukuoka City (Mt. Aburayama area)</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>Phone</strong><br>Please check the official website</div></div>''',
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>Address</strong><br>169-1 Higashi-Aburayama, Jonan-ku, Fukuoka City 814-0155</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>Phone</strong><br><a href="tel:+81928712515" style="color:var(--accent);font-weight:700;">+81-92-871-2515</a></div></div>'''
)

html = html.replace(
    '''<div class="play-option">
    <div class="play-option-head"><span>☀️</span>Standard Round (18 holes with half-turn break)</div>
    <div class="play-option-body">Morning start. Take a break at the restaurant after the front 9, then complete the back 9.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌤️</span>Afternoon Through (18 holes, no break)</div>
    <div class="play-option-body">Afternoon start. Play all 18 holes straight through — great for combining with sightseeing.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>Half Round (9 holes)</div>
    <div class="play-option-body">Play only 9 holes — perfect if time is short or it's your first golf experience in Japan.</div>
  </div>''',
    '''<div class="play-option">
    <div class="play-option-head"><span>⛳</span>One Round (10 holes)</div>
    <div class="play-option-body">About 1.5–2 hours. Perfect for beginners or squeezing golf into a sightseeing day.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🔁</span>Two Rounds (20 holes via A/B greens)</div>
    <div class="play-option-body">Play the second lap on the other green — effectively 20 holes, close to a regulation round.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>Early / Twilight Play</div>
    <div class="play-option-body">Flexible start times with off-peak pricing.</div>
  </div>'''
)

# --- KO section ---

WARN_KO = '''
  <div style="background:#fff3cd; border:2px solid #e6a817; border-radius:10px; padding:12px 14px; margin-bottom:14px; font-size:0.85rem; line-height:1.65; color:#5a3e00;">
    <strong style="color:#9a5100; font-size:0.95rem;">⚠️ 10홀 쇼트코스입니다</strong><br>
    2그린제·최장 345야드. 초보자·연습·단시간 라운드 전용. <strong>본격 18홀 라운드를 원하시면 다른 코스를 추천</strong>드립니다.
    <a href="recommend.html" style="color:#7a3500; font-weight:800; text-decoration:underline;">목적별 추천 코스 →</a>
  </div>
'''
html = html.replace(
    '<div id="c-ko" class="content">\n\n  <div class="airport-badge">',
    '<div id="c-ko" class="content">\n' + WARN_KO + '\n  <div class="airport-badge">',
    1
)

html = html.replace(
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">홀 수</span><span class="f-val">18홀</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">카트</span><span class="f-val">승용 카트</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">코스 유형</span><span class="f-val">구릉·산악 코스</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">위치</span><span class="f-val">아부라야마 산기슭·조난구</span></div>
        <div class="fact-item"><span class="f-icon">🌤️</span><span class="f-label">오후 스루</span><span class="f-val">공식 사이트 확인</span></div>
        <div class="fact-item"><span class="f-icon">👤</span><span class="f-label">1인 예약</span><span class="f-val">공식 사이트 확인</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>후쿠오카시 조난구 아부라야마 산기슭에 위치한 구릉·산악 코스입니다. 시내에서 가깝고 기복이 풍부한 다이나믹한 레이아웃이 특징입니다.</div>''',
    '''<div class="fact-grid">
        <div class="fact-item"><span class="f-icon">⛳</span><span class="f-label">홀 수</span><span class="f-val">10홀 (2그린)</span></div>
        <div class="fact-item"><span class="f-icon">📏</span><span class="f-label">최장 홀</span><span class="f-val">345야드</span></div>
        <div class="fact-item"><span class="f-icon">🚙</span><span class="f-label">카트</span><span class="f-val">손카트／2026.9~승용</span></div>
        <div class="fact-item"><span class="f-icon">🌲</span><span class="f-label">종류</span><span class="f-val">산악 쇼트코스</span></div>
        <div class="fact-item"><span class="f-icon">🏞️</span><span class="f-label">위치</span><span class="f-val">후쿠오카시 히가시아부라야마</span></div>
        <div class="fact-item"><span class="f-icon">🏙️</span><span class="f-label">조망</span><span class="f-val">후쿠오카 시가지 전망</span></div>
      </div>
      <div class="info-bar"><span>ℹ️</span>후쿠오카 시내에서 가까운 산기슭의 <strong>10홀 쇼트코스</strong>입니다. 2그린제라 최대 20개 홀 레이아웃으로 즐길 수 있습니다. PayPay돔·후쿠오카타워가 보이는 조망이 특징이며, 초보자 연습이나 관광 틈새 라운드에 최적입니다.</div>'''
)

html = html.replace(
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">산의 경사를 살린 기복 풍부한 코스 설계가 특징입니다. 고저차를 이용한 다이내믹한 샷이 공략의 핵심이며, 풍부한 자연과 절경을 즐기면서 도전적인 라운드를 만끽할 수 있습니다.</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>산악 코스만의 다이나미즘</strong> — 고저차가 있는 홀이 이어져 상급자도 만족할 수 있는 공략성이 있습니다.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>편리한 접근성</strong> — 후쿠오카공항에서 차로 약 25〜30분 거리. 렌터카나 셔틀버스 이용을 추천합니다.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">✅</span><div><strong>하프 턴 휴식 있음</strong> — 전반 9홀 후 레스토랑에서 식사·휴식. 일본 골프 문화를 체험할 수 있는 전통적인 스타일로 즐길 수 있습니다.</div></li>
      </ul>''',
    '''<p style="font-size:0.84rem;line-height:1.8;margin-bottom:14px;">짧지만 변화무쌍한 10홀. 계곡 넘는 쇼트홀과 최장 345야드 다운힐 미들홀 등 볼거리 가득. 2그린제로 사실상 20가지 레이아웃을 경험할 수 있습니다.</p>
      <ul style="list-style:none;display:flex;flex-direction:column;gap:10px;">
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🌆</span><div><strong>후쿠오카 시가지 조망</strong> — PayPay돔, 후쿠오카타워가 한눈에. 라운드 자체가 관광 체험.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">⏱️</span><div><strong>단시간 라운드</strong> — 10홀 약 1.5-2시간. 관광과 조합하기 편리.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">🔰</span><div><strong>초보자·연습용 추천</strong> — 부담 적게 스윙 연습. 본격 코스 전 몸풀기에도.</div></li>
        <li style="display:flex;gap:10px;font-size:0.84rem;line-height:1.6;"><span style="flex-shrink:0;">💴</span><div><strong>합리적 요금</strong> — 평일 3,000엔대~. 부담 없이 방문 가능.</div></li>
      </ul>'''
)

html = html.replace(
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>주소</strong><br>후쿠오카시 조난구 (아부라야마 산기슭)</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>전화</strong><br>공식 사이트에서 확인해 주세요</div></div>''',
    '''<div class="contact-row"><span class="c-icon">📍</span><div><strong>주소</strong><br>〒814-0155 후쿠오카시 조난구 히가시아부라야마 169-1</div></div>
      <div class="contact-row"><span class="c-icon">📞</span><div><strong>전화</strong><br><a href="tel:+81928712515" style="color:var(--accent);font-weight:700;">+81-92-871-2515</a></div></div>'''
)

html = html.replace(
    '''<div class="play-option">
    <div class="play-option-head"><span>☀️</span>일반 라운드 (18홀·하프 휴식 있음)</div>
    <div class="play-option-body">오전 출발. 전반 9홀 후 레스토랑에서 휴식, 이후 후반 9홀 플레이.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌤️</span>오후 스루 (18홀·휴식 없음)</div>
    <div class="play-option-body">오후 출발. 18홀 연속 플레이. 관광과 병행하기에 최적입니다.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>하프 라운드 (9홀)</div>
    <div class="play-option-body">9홀만 플레이. 시간이 제한적이거나 처음 골프를 즐기는 분께 추천합니다.</div>
  </div>''',
    '''<div class="play-option">
    <div class="play-option-head"><span>⛳</span>1라운드 (10홀)</div>
    <div class="play-option-body">약 1.5-2시간 소요. 관광 중 여유 시간에·초보자 연습용 적합.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🔁</span>2라운드 (20홀·2그린제)</div>
    <div class="play-option-body">A그린·B그린으로 2바퀴 돌면 실질 20홀. 일반 코스 느낌.</div>
  </div>
  <div class="play-option">
    <div class="play-option-head"><span>🌅</span>조조·박명 플레이</div>
    <div class="play-option-body">시간대에 따라 할인 요금. 저렴하게 즐길 수 있습니다.</div>
  </div>'''
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('course-aburayama.html ✓ updated')

# === access-aburayama.html: 名称は維持（検索SEO）、ただし説明補強 ===
# 特に修正不要（アクセス情報は変わらず）

# === index.html: course-card for aburayama ===
idx = os.path.join(BASE, 'index.html')
with open(idx, encoding='utf-8') as f:
    ih = f.read()
# JA card meta
ih = ih.replace(
    '📍 福岡市城南区　｜　18ホール　｜　丘陵コース　｜　午後スルーあり',
    '📍 福岡市城南区　｜　⚠️ 10ホール ショートコース　｜　2グリーン制'
)
# EN card meta (if any "18 holes" with aburayama context) - check & adjust
# KO card meta
with open(idx, 'w', encoding='utf-8') as f:
    f.write(ih)
print('index.html ✓ updated')

print('\nDONE.')
