#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hub-budget.html のページ全体の金額表現を 2026-11-01 のじゃらん実データに合わせる (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日¥6,000台中心」「最安¥4,060〜」 → 本ハブ (じゃらん掲載5コース) の平日18H最安は ¥4,959 (フェザント)〜¥7,241 (レイクサイド)。あかねは楽天のみ
- 「平日と土日の差 ¥2,500〜¥4,000」「平日狙いで¥3,000差」 → 福岡30コースの18H最安どうしの差は中央値 ¥5,228 (¥2,727〜¥9,709)。本ハブ5コースは ¥4,909〜¥8,373
- 「午後スルーで¥1,500-2,500オフ」「午後スルー対応」 → 11/2〜15 のじゃらんで本ハブの午後スルーはレイクサイドだけ (平日¥8,969〜) で通常18H最安 (¥7,241〜) より高い
- 「月曜セルフ¥7,880」 → 鷹羽のじゃらん14日分に月曜プラン・¥7,880 とも無し
- 「Web予約で平均¥3,000お得」「現地受付より¥1,000以上」「じゃらん・楽天で¥500〜¥2,000差」「1・2・8月が底値」「水曜定休が多い」「1.5倍」 → 根拠なし
- フェザントの所在地「糸島」は誤り (じゃらん・コースページとも田川郡川崎町)
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)・scripts/.cache/jalan_{gc}_202611*.html
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_hub_budget_2026_11.py            # dry-run
  python scripts/fix_hub_budget_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_hub_budget_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "hub-budget.html"

AFT = '<a href="book-fukuoka-afternoon.html">'
# (旧, 新, 出現回数)
R = [
    # ---- head ----
    ('content="コスパ重視ハブ。福岡レイクサイドCC平日¥6,000台、あかねCC・浮羽CC¥4,060〜、フェザント平日昼食付¥6,490〜、鷹羽月曜セルフ¥7,880、セントラル福岡¥6,500〜。賢く週末ゴルフ・午後スルー・季節価格・Web予約で平均¥3,000お得。"',
     'content="福岡のコスパ重視6コース。じゃらんの18H最安（2026年11月1日時点）は平日¥4,959〜¥7,241（あかねは楽天GORAのみ）。福岡30コースでは土日祝が平日より中央値で約¥5,200高く、平日に回すのがいちばんの節約です。"', 1),
    ('content="Smart weekend golf in Fukuoka. Six budget courses: Lakeside (weekday from ¥6,000), Akane (¥6,500), Ukiha (¥4,060 lowest), Pheasant lunch-included ¥6,490, Takaha Monday self-play ¥7,880, Central Fukuoka ¥6,500. Web booking saves ¥3,000 on average."',
     'content="Six budget-friendly Fukuoka courses. Jalan\'s lowest 18-hole weekday plans (as of Nov 1, 2026) run ¥4,959–¥7,241 (Akane is on Rakuten GORA only). Across 30 Fukuoka courses, weekend floors are a median ¥5,200 higher than weekdays — playing on a weekday saves the most."', 1),
    ('content="가성비 중시 허브. 후쿠오카 레이크사이드CC 평일 ¥6,000대, 아카네CC·우키하CC ¥4,060부터, 페전트 평일 점심 포함 ¥6,490, 다카하 월요일 셀프 ¥7,880, 센트럴후쿠오카 ¥6,500. 똑똑한 주말 골프·오후 스루·시즌 가격·웹 예약으로 평균 ¥3,000 절약."',
     'content="후쿠오카 가성비 6개 코스. 자란 18홀 최저가(2026년 11월 1일 기준)는 평일 ¥4,959〜¥7,241(아카네는 라쿠텐 GORA만). 후쿠오카 30개 코스에서 주말은 평일보다 중앙값 약 ¥5,200 비싸, 평일 라운드가 가장 큰 절약입니다."', 1),
    ('<title>コスパ重視｜福岡ゴルフ場 6選 — 平日¥6,000・午後スルー・Web予約節約ハブ | 福岡ゴルフ場ガイド</title>',
     '<title>コスパ重視｜福岡ゴルフ場 6選 — 平日狙い・予約サイト比較で賢く回る | 福岡ゴルフ場ガイド</title>', 1),
    ('"description": "賢く週末ゴルフ。平日¥6,000台中心、午後スルー、季節価格を活用する、福岡のコスパ重視6コース。"',
     '"description": "福岡のコスパ重視6コース。平日と土日祝の料金差（じゃらん実データ）と予約サイトの使い分けで賢く回る。"', 1),
    ('<meta property="og:title" content="コスパ重視｜福岡ゴルフ場 6選 — 平日¥6,000・午後スルー・Web予約節約ハブ">',
     '<meta property="og:title" content="コスパ重視｜福岡ゴルフ場 6選 — 平日狙い・予約サイト比較で賢く回る">', 1),
    ('<meta property="og:description" content="平日狙い・午後スルー・季節価格を駆使。Web予約で平均¥3,000お得な、福岡のコスパ最強6コース。">',
     '<meta property="og:description" content="土日祝は平日より中央値で約¥5,200高い（じゃらん18H最安・福岡30コース・2026年11月1日時点）。平日狙いで賢く回る、福岡のコスパ重視6コース。">', 1),
    ('alt="賢く回る、福岡ゴルフ。平日¥6,000・午後スルー・季節価格。のコース風景"',
     'alt="福岡のゴルフコースの風景（コスパ重視ハブ）"', 3),

    # ---- JA ----
    ('<h1 class="hero-title">賢く回る、福岡ゴルフ。<br>平日¥6,000・午後スルー・季節価格。</h1>',
     '<h1 class="hero-title">賢く回る、福岡ゴルフ。<br>狙うなら、平日。</h1>', 1),
    ('<div class="hero-sub">同じコースでも、平日 vs 土日、午前 vs 午後で平均¥3,000違う。Web予約とポイントを駆使して、月2回以上ラウンドする人のための6コース。</div>',
     '<div class="hero-sub">じゃらんの18H最安で比べると、福岡30コースの土日祝は平日より中央値で約¥5,200高い（2026年11月1日時点）。平日に回せる人のための6コース。</div>', 1),
    ('<span class="hero-badge">💴 平日¥6,000台中心</span>', '<span class="hero-badge">💴 平日18H ¥4,959〜（11/1時点）</span>', 1),
    ('<span class="hero-badge">🌤️ 午後スルー対応</span>', '<span class="hero-badge">📅 料金は確認日つき</span>', 1),
    ('<span class="hero-badge">🎯 月曜セルフ¥7,880あり</span>', '<span class="hero-badge">🔁 じゃらん・楽天を比較</span>', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">最安</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">平日最安（11/1）</div>', 1),
    ('<div class="persona-band-num">¥3,000<span class="unit">節約</span></div><div class="persona-band-label">Web予約平均</div>',
     '<div class="persona-band-num">¥5,200<span class="unit">差</span></div><div class="persona-band-label">土日祝との差（中央値）</div>', 1),
    ('<div class="persona-band-num">月<span class="unit">セルフ</span></div><div class="persona-band-label">最強プラン</div>',
     '<div class="persona-band-num">2<span class="unit">社</span></div><div class="persona-band-label">予約サイト比較</div>', 1),
    ('<div class="why-title">平日狙いで¥3,000差</div>', '<div class="why-title">平日狙いで約¥5,200差</div>', 1),
    ('<div class="why-desc">福岡周辺コースの多くは、平日と土日の差が¥2,500〜¥4,000。月1回ペースの人なら、有給を使ってでも平日に回したほうが、年間¥30,000以上の余力が生まれます。</div>',
     '<div class="why-desc">じゃらんの18H最安（2026年11月1日時点）で比べると、福岡30コースの土日祝は平日より中央値で約¥5,200高く、差は¥2,727〜¥9,709でした。月1回のラウンドを平日に回せば、年12回で約¥6万の差になります。</div>', 1),
    ('<div class="why-title">午後スルーで¥1,500-2,500オフ</div>', '<div class="why-title">午後スルーは時期とコースしだい</div>', 1),
    ('<div class="why-desc">12〜13時スタートのスループレーは、ハーフ→昼食→ハーフより¥1,500〜¥2,500安くなるコースが多数。終了は17〜18時で、夜ご飯にも間に合います。</div>',
     f'<div class="why-desc">2026年11月2〜15日のじゃらんで、本ハブ（じゃらん掲載の5コース）に午後スルーのプランがあったのは福岡レイクサイドだけ。最安で比べると、通常の18H（平日¥7,241〜）のほうが午後スルー（平日¥8,969〜）より安い結果でした。{AFT}午後スルーの実データ</a></div>', 1),
    ('<div class="why-desc">じゃらんゴルフはPontaポイント、楽天GORAは楽天ポイントが貯まり・使えます。Web予約限定の特別プランも豊富。同じコースが¥1,000〜¥2,000安くなるケースが日常的に発生します。</div>',
     '<div class="why-desc">じゃらんゴルフはPontaポイント、楽天GORAは楽天ポイントが貯まり・使えます。同じコースでも、予約サイトによって出ているプランや料金が違うことがあります。</div>', 1),
    ('<h2 class="sec-title">¥3,000節約する、4つの実践テク</h2>', '<h2 class="sec-title">安く回る、4つの実践テク</h2>', 1),
    ('"なんとなく週末"を卒業するだけで、年間ラウンド数が1.5倍になります。明日から使えるテクニックを4つ。',
     '"なんとなく週末"をやめるだけで、同じ予算で回れる回数が変わります。明日から使えるテクニックを4つ。', 1),
    ('<div class="tactic-title">月曜・火曜・木曜を狙う</div>', '<div class="tactic-title">平日を狙う</div>', 1),
    ('<div class="tactic-desc">水曜定休のコースが多いため、<strong>火曜と木曜は人気が分散</strong>します。月曜は"セルフ¥7,880"のような特別プランも出やすい曜日。週末より<strong>¥2,500〜¥4,000</strong>安くなるのが標準。</div>',
     '<div class="tactic-desc">土日祝との差は<strong>中央値で約¥5,200</strong>（じゃらん18H最安・福岡30コース・2026年11月1日時点）。本ハブの5コースでも<strong>¥4,909〜¥8,373</strong>の差がありました。</div>', 1),
    ('<div class="tactic-title">午後スルーは"通の選択"</div>', '<div class="tactic-title">午後スルーは出ている週を確認</div>', 1),
    ('<div class="tactic-desc">12時前後スタート→ハーフ昼食を取らずに18Hを通す形式。<strong>料金は午前スタートより¥1,500〜¥2,500安い</strong>。プレー時間も4時間程度に短縮されるので、家族時間とも両立しやすい。</div>',
     '<div class="tactic-desc">昼前後にスタートし、昼休憩なしで18Hを回る形式。出る時期とコースは限られ、2026年11月前半は本ハブでは福岡レイクサイドだけでした（平日¥8,969〜）。<strong>安さが目当てなら、通常プランの最安と比べてから</strong>選びましょう。</div>', 1),
    ('<div class="tactic-desc">同じコース・同じ日付でも、<strong>じゃらん・楽天GORAで¥500〜¥2,000差</strong>が出るケースが多数。両方検索が"基本動作"。Pontaか楽天、貯めているポイントの方を優先するとさらにお得。</div>',
     '<div class="tactic-desc">同じコース・同じ日でも、<strong>じゃらんと楽天GORAで出ているプランや料金が違う</strong>ことがあります（例：あかねは楽天GORAのみ）。両方を見比べるのが基本。Pontaか楽天、貯めているポイントの方を優先するのも手です。</div>', 1),
    ('<div class="tactic-title">季節ごとの価格差を狙う</div>', '<div class="tactic-title">料金は確認日つきで見る</div>', 1),
    ('<div class="tactic-desc">福岡は<strong>1月・2月・8月が底値</strong>(¥4,060〜の枠が出やすい)、3〜5月・10〜11月がピーク。寒さを我慢する1〜2月、暑さを我慢する8月のラウンドはコスパ最強。レイヤリングで快適に。</div>',
     '<div class="tactic-desc">料金は時期や日によって変わります。本ページの料金は<strong>じゃらんの2026年11月1日時点の18H最安</strong>なので、予約前に予約サイトで最新の料金を確認してください。</div>', 1),
    ('「平日最安」「特別プランあり」「アクセス良好」の3軸で並べました。どれもWeb予約で、現地受付より¥1,000以上お得な傾向。',
     '料金はじゃらんの18H最安（2026年11月1日時点）です。あかねはじゃらんに出ていないため、楽天GORAで確認してください。', 1),
    ('<span class="course-chip">糸島</span>', '<span class="course-chip">田川郡</span>', 1),
    ('フラット高低差20mで、午後スルーでも消耗しにくい設計。', 'フラット（高低差20m）で回りやすい設計。', 1),
    ('<span class="course-chip">特別プラン</span>', '<span class="course-chip">田川郡</span>', 1),
    ('<div class="course-desc"><strong>有給を月1回月曜に当てるだけで</strong>、年間ラウンド数を倍化できる人もいます。コスパ派必見の一軸。</div>',
     '<div class="course-desc"><strong>田川郡大任町</strong>の林間コース。</div>', 1),

    # ---- 共通 (3言語) ----
    ('<div class="course-area">Itoshima · Lunch Inclusive · Accordia</div>', '<div class="course-area">Tagawa District · Accordia</div>', 3),
    ('<div class="course-area">Tagawa Area · Monday Self-Play Special</div>', '<div class="course-area">Tagawa District · Forest</div>', 3),

    # ---- EN ----
    ('<div class="hero-sub">The same course can vary ¥3,000+ depending on weekday vs weekend, morning vs afternoon. Six courses, four tactics, and a savings habit that doubles your annual rounds.</div>',
     '<div class="hero-sub">Comparing Jalan\'s lowest 18-hole plans, weekend rates at 30 Fukuoka courses are a median ¥5,200 higher than weekdays (as of Nov 1, 2026). Six courses for golfers who can play on a weekday.</div>', 1),
    ('<span class="hero-badge">💴 Weekday from ¥6,000</span>', '<span class="hero-badge">💴 Weekday 18H from ¥4,959 (Nov 1)</span>', 1),
    ('<span class="hero-badge">🌤️ Afternoon-thru friendly</span>', '<span class="hero-badge">📅 Rates with check date</span>', 1),
    ('<span class="hero-badge">🎯 Monday self-play ¥7,880</span>', '<span class="hero-badge">🔁 Compare Jalan &amp; Rakuten</span>', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">Lowest fee</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">Weekday low (Nov 1)</div>', 1),
    ('<div class="persona-band-num">¥3,000<span class="unit">saved</span></div><div class="persona-band-label">Web booking avg</div>',
     '<div class="persona-band-num">¥5,200<span class="unit">gap</span></div><div class="persona-band-label">vs weekend (median)</div>', 1),
    ('<div class="persona-band-num">Mon<span class="unit">self</span></div><div class="persona-band-label">Best plan</div>',
     '<div class="persona-band-num">2<span class="unit">sites</span></div><div class="persona-band-label">Compare booking sites</div>', 1),
    ('<div class="why-title">Weekday tee times save ¥3,000</div>', '<div class="why-title">Weekdays save about ¥5,200</div>', 1),
    ('<div class="why-desc">Most Fukuoka clubs run ¥2,500–¥4,000 cheaper Monday–Friday than on weekends. If you can spend a vacation day on a Tuesday round, you free up over ¥30,000/year — easily another two rounds.</div>',
     '<div class="why-desc">On Jalan\'s lowest 18-hole plans (as of Nov 1, 2026), weekend rates at 30 Fukuoka courses were a median ¥5,200 higher than weekdays, with gaps from ¥2,727 to ¥9,709. Moving one round a month to a weekday adds up to about ¥60,000 over 12 rounds.</div>', 1),
    ('<div class="why-title">Afternoon-thru: ¥1,500–¥2,500 off</div>', '<div class="why-title">Afternoon-thru depends on season and course</div>', 1),
    ('<div class="why-desc">Tee off around noon, skip the long mid-round lunch, finish 18 by 5pm. Many clubs price afternoon-thru ¥1,500–¥2,500 below the standard morning round, and you still get home for dinner.</div>',
     f'<div class="why-desc">On Jalan for Nov 2–15, 2026, only Fukuoka Lakeside among this hub\'s five Jalan-listed courses offered afternoon-thru plans — and its regular 18-hole floor (weekday ¥7,241) was cheaper than afternoon-thru (weekday ¥8,969). {AFT}Afternoon-thru data</a></div>', 1),
    ('<div class="why-desc">Jalan Golf earns Ponta points; Rakuten GORA earns Rakuten points. Web-only deals are common, and the same course can be ¥1,000–¥2,000 cheaper than at the front desk on any given day.</div>',
     '<div class="why-desc">Jalan Golf earns Ponta points; Rakuten GORA earns Rakuten points. The same course can show different plans and rates on each site.</div>', 1),
    ('<h2 class="sec-title">Four tactics to save ¥3,000/round</h2>', '<h2 class="sec-title">Four tactics to play for less</h2>', 1),
    ('Stop defaulting to "weekend." Four small habit shifts that translate to roughly 1.5x more rounds per year.',
     'Stop defaulting to "weekend." Four habits that stretch the same budget further.', 1),
    ('<div class="tactic-title">Aim for Mon / Tue / Thu</div>', '<div class="tactic-title">Aim for weekdays</div>', 1),
    ('<div class="tactic-desc">Many clubs close on Wednesdays, so <strong>Tuesday and Thursday demand is diluted</strong>. Mondays often carry "self-play ¥7,880"-class specials. Expect <strong>¥2,500–¥4,000</strong> below weekend rates.</div>',
     '<div class="tactic-desc">The weekend gap is <strong>a median ¥5,200</strong> (Jalan lowest 18-hole plans, 30 Fukuoka courses, Nov 1, 2026). This hub\'s five Jalan-listed courses showed gaps of <strong>¥4,909–¥8,373</strong>.</div>', 1),
    ('<div class="tactic-title">Afternoon-thru is the insider play</div>', '<div class="tactic-title">Check which weeks have afternoon-thru</div>', 1),
    ('<div class="tactic-desc">Around noon start → 18 holes without the long lunch break. <strong>¥1,500–¥2,500 cheaper than morning rounds</strong>, and play wraps in roughly four hours. Family-friendly Saturdays become possible.</div>',
     '<div class="tactic-desc">Start around noon and play 18 holes without the lunch break. Availability is limited: in early November 2026 only Fukuoka Lakeside offered it in this hub (weekday from ¥8,969). <strong>If price is the goal, compare with the regular plan floor first.</strong></div>', 1),
    ('<div class="tactic-desc">For the same course on the same day, <strong>Jalan Golf and Rakuten GORA can differ ¥500–¥2,000</strong>. Checking both should be reflex. Pick the side where you bank points already.</div>',
     '<div class="tactic-desc">For the same course on the same day, <strong>Jalan Golf and Rakuten GORA can show different plans and rates</strong> (e.g. Akane is on Rakuten GORA only). Check both, and favor the site where you already bank points.</div>', 1),
    ('<div class="tactic-title">Ride the seasonal floor</div>', '<div class="tactic-title">Read rates with their check date</div>', 1),
    ('<div class="tactic-desc">In Fukuoka, <strong>January, February, and August are the price floor</strong> (¥4,060 slots appear). March–May and October–November are peak. Layer up in winter, hydrate in August — the savings are real.</div>',
     '<div class="tactic-desc">Rates change by season and by day. Rates on this page are <strong>Jalan\'s lowest 18-hole plans as of Nov 1, 2026</strong> — check the booking site for current rates before you book.</div>', 1),
    ('Sorted by lowest weekday fee, special plans, and access. All are typically ¥1,000+ cheaper booked online than at the desk.',
     'Rates are Jalan\'s lowest 18-hole plans as of Nov 1, 2026. Akane is not on Jalan — check Rakuten GORA.', 1),
    ('<span class="course-chip">Itoshima</span>', '<span class="course-chip">Tagawa</span>', 1),
    ('Flat ~20m elevation makes afternoon-thru rounds easy — a great gateway', 'Flat (~20m elevation change) and easy to play — a great gateway', 1),
    ('<span class="course-chip">Special plan</span>', '<span class="course-chip">Tagawa</span>', 1),
    ('<div class="course-desc"><strong>Spending one vacation day per month on Mondays</strong> is the single most efficient lever for doubling your annual rounds.</div>',
     '<div class="course-desc">A forest course in <strong>Oto, Tagawa District</strong>.</div>', 1),
    ('<p class="article-excerpt">Weekday, weekend, and afternoon-thru rates with direct links to Jalan and Rakuten GORA.</p>',
     '<p class="article-excerpt">Weekday and weekend rates side by side, with direct links to Jalan and Rakuten GORA.</p>', 1),

    # ---- KO ----
    ('<h1 class="hero-title">똑똑하게 도는 후쿠오카 골프.<br>평일 ¥6,000·오후 스루·시즌 가격.</h1>',
     '<h1 class="hero-title">똑똑하게 도는 후쿠오카 골프.<br>노린다면 평일.</h1>', 1),
    ('<div class="hero-sub">같은 코스라도 평일 vs 주말, 오전 vs 오후로 평균 ¥3,000 차이. 웹 예약과 포인트를 활용해 월 2회 이상 라운드하는 사람들을 위한 6개 코스.</div>',
     '<div class="hero-sub">자란 18홀 최저가로 비교하면 후쿠오카 30개 코스의 주말은 평일보다 중앙값 약 ¥5,200 비쌉니다(2026년 11월 1일 기준). 평일에 칠 수 있는 분을 위한 6개 코스.</div>', 1),
    ('<span class="hero-badge">💴 평일 ¥6,000대 중심</span>', '<span class="hero-badge">💴 평일 18홀 ¥4,959〜(11/1 기준)</span>', 1),
    ('<span class="hero-badge">🌤️ 오후 스루 가능</span>', '<span class="hero-badge">📅 요금은 확인일 표시</span>', 1),
    ('<span class="hero-badge">🎯 월요일 셀프 ¥7,880</span>', '<span class="hero-badge">🔁 자란·라쿠텐 비교</span>', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">최저가</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">평일 최저가(11/1)</div>', 1),
    ('<div class="persona-band-num">¥3,000<span class="unit">절약</span></div><div class="persona-band-label">웹 예약 평균</div>',
     '<div class="persona-band-num">¥5,200<span class="unit">차이</span></div><div class="persona-band-label">주말과의 차이(중앙값)</div>', 1),
    ('<div class="persona-band-num">월<span class="unit">셀프</span></div><div class="persona-band-label">최강 플랜</div>',
     '<div class="persona-band-num">2<span class="unit">곳</span></div><div class="persona-band-label">예약 사이트 비교</div>', 1),
    ('<div class="why-title">평일 노리면 ¥3,000 차이</div>', '<div class="why-title">평일 노리면 약 ¥5,200 차이</div>', 1),
    ('<div class="why-desc">후쿠오카 주변 코스 다수가 평일과 주말의 차이가 ¥2,500〜¥4,000. 월 1회 페이스인 사람이라면 휴가를 쓰더라도 평일에 도는 편이 연간 ¥30,000 이상의 여유가 생깁니다.</div>',
     '<div class="why-desc">자란 18홀 최저가(2026년 11월 1일 기준)로 비교하면 후쿠오카 30개 코스의 주말은 평일보다 중앙값 약 ¥5,200 비싸고, 차이는 ¥2,727〜¥9,709였습니다. 월 1회 라운드를 평일로 옮기면 12회에 약 ¥6만 차이가 납니다.</div>', 1),
    ('<div class="why-title">오후 스루로 ¥1,500-2,500 할인</div>', '<div class="why-title">오후 스루는 시기와 코스에 따라</div>', 1),
    ('<div class="why-desc">12〜13시 시작 스루 플레이는 하프→점심→하프보다 ¥1,500〜¥2,500 저렴한 코스가 많습니다. 종료는 17〜18시로 저녁 식사에도 시간 맞출 수 있어요.</div>',
     f'<div class="why-desc">2026년 11월 2〜15일 자란에서 본 허브(자란 등록 5개 코스) 중 오후 스루 플랜이 있었던 곳은 후쿠오카 레이크사이드뿐. 최저가로 비교하면 일반 18홀(평일 ¥7,241〜)이 오후 스루(평일 ¥8,969〜)보다 저렴했습니다. {AFT}오후 스루 실데이터</a></div>', 1),
    ('<div class="why-desc">자란 골프는 폰타 포인트, 라쿠텐 GORA는 라쿠텐 포인트가 적립·사용 가능. 웹 예약 한정 특별 플랜도 풍부. 같은 코스가 ¥1,000〜¥2,000 저렴해지는 케이스가 일상적으로 발생합니다.</div>',
     '<div class="why-desc">자란 골프는 폰타 포인트, 라쿠텐 GORA는 라쿠텐 포인트가 적립·사용 가능. 같은 코스라도 예약 사이트마다 나와 있는 플랜과 요금이 다를 수 있습니다.</div>', 1),
    ('<h2 class="sec-title">¥3,000 절약하는 4가지 실전 테크</h2>', '<h2 class="sec-title">저렴하게 치는 4가지 실전 테크</h2>', 1),
    ('"그냥 주말"을 졸업하는 것만으로 연간 라운드 수가 1.5배. 내일부터 쓸 수 있는 4가지.',
     '"그냥 주말"을 그만두는 것만으로 같은 예산으로 칠 수 있는 횟수가 달라집니다. 내일부터 쓸 수 있는 4가지.', 1),
    ('<div class="tactic-title">월·화·목요일을 노리기</div>', '<div class="tactic-title">평일을 노리기</div>', 1),
    ('<div class="tactic-desc">수요일 정기 휴무 코스가 많아 <strong>화요일과 목요일은 인기가 분산</strong>. 월요일은 "셀프 ¥7,880" 같은 특별 플랜도 나오기 쉬운 요일. 주말보다 <strong>¥2,500〜¥4,000</strong> 저렴한 것이 표준.</div>',
     '<div class="tactic-desc">주말과의 차이는 <strong>중앙값 약 ¥5,200</strong>(자란 18홀 최저가·후쿠오카 30개 코스·2026년 11월 1일 기준). 본 허브 5개 코스도 <strong>¥4,909〜¥8,373</strong> 차이가 있었습니다.</div>', 1),
    ('<div class="tactic-title">오후 스루는 "고수의 선택"</div>', '<div class="tactic-title">오후 스루는 나오는 주를 확인</div>', 1),
    ('<div class="tactic-desc">12시 전후 시작→하프 점심을 거르고 18H를 통과. <strong>요금은 오전 시작보다 ¥1,500〜¥2,500 저렴</strong>. 플레이 시간도 4시간 정도로 단축되어 가족 시간과도 양립.</div>',
     '<div class="tactic-desc">정오 전후에 시작해 점심 휴식 없이 18홀을 도는 방식. 나오는 시기와 코스가 한정되어, 2026년 11월 전반에는 본 허브에서 후쿠오카 레이크사이드뿐이었습니다(평일 ¥8,969〜). <strong>저렴함이 목적이라면 일반 플랜 최저가와 먼저 비교</strong>하세요.</div>', 1),
    ('<div class="tactic-desc">같은 코스·같은 날짜라도 <strong>자란·라쿠텐 GORA에서 ¥500〜¥2,000 차이</strong>가 나는 경우가 다수. 양쪽 검색이 "기본 동작". 폰타나 라쿠텐, 적립 중인 포인트 쪽을 우선하면 더 이득.</div>',
     '<div class="tactic-desc">같은 코스·같은 날이라도 <strong>자란과 라쿠텐 GORA에 나와 있는 플랜과 요금이 다를</strong> 수 있습니다(예: 아카네는 라쿠텐 GORA만). 양쪽을 비교하는 것이 기본. 폰타나 라쿠텐, 적립 중인 포인트 쪽을 우선하는 것도 방법입니다.</div>', 1),
    ('<div class="tactic-title">계절별 가격 차이 노리기</div>', '<div class="tactic-title">요금은 확인일과 함께 보기</div>', 1),
    ('<div class="tactic-desc">후쿠오카는 <strong>1월·2월·8월이 바닥</strong>(¥4,060대 슬롯이 나오기 쉬움), 3〜5월·10〜11월이 피크. 추위를 견디는 1〜2월, 더위를 견디는 8월의 라운드는 가성비 최강. 레이어링으로 쾌적하게.</div>',
     '<div class="tactic-desc">요금은 시기와 날짜에 따라 바뀝니다. 이 페이지의 요금은 <strong>자란의 2026년 11월 1일 기준 18홀 최저가</strong>이므로, 예약 전에 예약 사이트에서 최신 요금을 확인하세요.</div>', 1),
    ('"평일 최저가" "특별 플랜" "접근성" 3축으로 정렬. 모두 웹 예약 시 현장 접수보다 ¥1,000 이상 저렴한 경향.',
     '요금은 자란 18홀 최저가(2026년 11월 1일 기준)입니다. 아카네는 자란에 없으므로 라쿠텐 GORA에서 확인하세요.', 1),
    ('<span class="course-chip">이토시마</span>', '<span class="course-chip">다가와군</span>', 1),
    ('평탄(고저차 약 20m)으로 오후 스루에도 지치지 않는 설계.', '평탄(고저차 약 20m)해서 돌기 쉬운 설계.', 1),
    ('<span class="course-chip">특별 플랜</span>', '<span class="course-chip">다가와군</span>', 1),
    ('<div class="course-desc"><strong>월 1회 휴가를 월요일에 배치하는 것만으로</strong> 연간 라운드 수를 두 배로 만들 수 있는 사람도 있습니다.</div>',
     '<div class="course-desc"><strong>다가와군 오토마치</strong>의 임간 코스.</div>', 1),
    ('<p class="article-excerpt">평일·주말·오후 스루 요금을 나란히. 자란·라쿠텐 GORA로 직접 점프.</p>',
     '<p class="article-excerpt">평일·주말 요금을 나란히. 자란·라쿠텐 GORA로 직접 점프.</p>', 1),
    ('<p class="article-excerpt">平日・土日・午後スルーの料金を横並びで。じゃらん・楽天GORAへ直接ジャンプ。</p>',
     '<p class="article-excerpt">平日・土日の料金を横並びで。じゃらん・楽天GORAへ直接ジャンプ。</p>', 1),
]


def main():
    src = open(os.path.join(REPO_ROOT, NAME), encoding="utf-8", newline="").read()
    t = src
    c = {"replaced": 0, "already": 0}
    for old, new, n in R:
        k = t.count(old)
        if k == n:
            t = t.replace(old, new); c["replaced"] += 1
        elif k == 0 and t.count(new) >= n:
            c["already"] += 1
        else:
            raise SystemExit(f"NO_MATCH ({k}/{n}): {old[:70]}")
    print(c, "変更あり" if t != src else "変更なし")
    if APPLY and t != src:
        for root in ROOTS:
            open(os.path.join(root, NAME), "w", encoding="utf-8", newline="").write(t)
        print("APPLIED", ROOTS)
    elif not APPLY:
        print("DRY-RUN")


if __name__ == "__main__":
    main()
