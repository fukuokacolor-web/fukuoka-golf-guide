#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
area-chikuho.html のページ全体の金額表現と、セントラル福岡の所在地誤りから派生した記述を直す
(カード料金欄は fix_card_prices_2026_11.py で済)。

- 「平日¥6,000台/¥6,000〜」「レイクサイド¥6,000〜で筑豊最安」「午後スルーなら¥4,000台」「当日料金は平均+¥3,000」
  「Web予約で平均¥3,000お得」「Pontaポイント1%」「料金順で並べました」 → 根拠なし/誤り
  じゃらん18H最安 (2026-11-01): 皐月竜王¥4,605 / フェザント¥4,959 / 鷹羽¥5,596 / セントラル・嘉穂¥6,323 / レイクサイド¥7,241 /
  JR内野¥9,500 / 麻生飯塚¥10,273 / 西日本¥10,991。あかねはじゃらん無し (楽天のみ)。
  本ページ9コースの中央値¥6,323 は5エリアで最も低い (筑後¥6,960・北九州¥7,419・福岡市¥10,037・糸島¥12,487)
- セントラル福岡は筑紫野市 (朝倉郡ではない)。所在地は各コースページ JSON-LD: 飯塚市6・田川郡2・直方市1・筑紫野市1
  → 「飯塚市・朝倉市・田川郡の10コース」「朝倉ラウンド」「旅館から約30分」「3万坪」を是正
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_chikuho_2026_11.py            # dry-run
  python scripts/fix_chikuho_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_chikuho_2026_11.py --apply    # REPO + PREVIEW
"""
import os, re, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "area-chikuho.html"

META_JA = "筑豊（飯塚市・田川郡・直方市）の9コースと、筑紫野市のセントラル福岡を掲載。じゃらんの18H最安（2026年11月1日時点）は平日¥4,605〜。料金・アクセス・特徴を比較。"
FAQ1_JA = "所在地で選ぶと分かりやすいです。飯塚市に6コース（麻生飯塚・あかね・レイクサイド・かほ・皐月竜王・JR内野）、田川郡に2コース（鷹羽ロイヤル・フェザント）、直方市に西日本。セントラル福岡は筑紫野市で、筑豊の外にあります。料金で選ぶなら「コスパ最高はどこ？」を参照してください。"
FAQ3_JA = "じゃらんの18H最安（2026年11月1日時点）では、皐月ゴルフ倶楽部 竜王コースの平日¥4,605〜が本ページでいちばん安く、福岡フェザント（¥4,959〜）、鷹羽ロイヤル（¥5,596〜）が続きます。料金は日によって変わるので、予約前に予約サイトで確認してください。"

# (旧, 新, 出現回数)
R = [
    # ---- head ----
    ('<title>筑豊・田川・朝倉ゴルフ場10選｜平日6,000円〜の穴場10コース | 福岡ゴルフ場ガイド</title>',
     '<title>筑豊・田川ゴルフ場10選｜平日4,605円〜の穴場10コース【11月】 | 福岡ゴルフ場ガイド</title>', 1),
    ('"text": "セントラル福岡（朝倉郡）と茜カントリークラブ（飯塚市）の2コースが筑豊エリアの代表格。どちらも平日¥6,500〜と料金が手頃で、戦略性も初心者対応もバランス良し。初訪問なら最優先で検討するべき2コースです。"',
     f'"text": "{FAQ1_JA}"', 1),
    ('"text": "福岡レイクサイドカントリークラブが平日¥6,000〜と筑豊エリア最安。池絡みの戦略コースで、価格以上のプレー価値あり。午後スルーなら¥4,000台のプランもあるので、コスパ重視ならまずココ。"',
     f'"text": "{FAQ3_JA}"', 1),
    ('<meta property="og:description" content="飯塚市・朝倉市・田川郡の厳選10ゴルフ場。平日6,000円台から回れるコスパ穴場エリアを徹底解説。鷹羽ロイヤル・フェザント追加。">',
     '<meta property="og:description" content="筑豊（飯塚市・田川郡・直方市）の9コースと筑紫野市のセントラル福岡。平日18H ¥4,605〜（じゃらん・2026年11月1日時点）のコスパ穴場エリア。">', 1),

    # ---- JA ----
    ('福岡市から1時間の素朴な田舎エリア。平日¥6,000台のリアル価格、原鶴温泉とのセット、',
     '福岡市から1時間の素朴な田舎エリア。平日18H ¥4,605〜（じゃらん・2026年11月1日時点）、原鶴温泉とのセット、', 1),
    ('<span class="hero-badge">💰 平日¥6,000台</span>', '<span class="hero-badge">💰 平日¥4,605〜（11/1）</span>', 1),
    ('<div class="stat-num">¥6,000<span class="unit">〜</span></div><div class="stat-label">平日最安</div>',
     '<div class="stat-num">¥4,605<span class="unit">〜</span></div><div class="stat-label">平日最安（11/1）</div>', 1),
    ('<td>朝倉郡・原鶴温泉セット可能</td>', '<td>筑紫野市・アコーディア</td>', 1),
    ('<div class="compare-foot-note">💡 当日料金は平均 +¥3,000。<strong style="color:var(--earth-dark)">じゃらんゴルフのWeb予約</strong>でほぼ全コース最安。</div>',
     '<div class="compare-foot-note">💡 料金は<strong style="color:var(--earth-dark)">じゃらんの18H最安（2026年11月1日時点）</strong>。あかねはじゃらんに出ていないため楽天GORAで確認。</div>', 1),
    ('<div class="reason-desc">平日¥5,000〜6,000台のリアル価格。糸島・筑後より一段安く、午後スルーなら¥4,000台のプランも。コスパ重視なら筑豊・朝倉が福岡県内ベストです。</div>',
     '<div class="reason-desc">本ページの9コース（じゃらん掲載）の平日18H最安は中央値¥6,323で、当サイトの5エリアでいちばん低い水準（2026年11月1日時点）。最安は皐月竜王の¥4,605〜。</div>', 1),
    ('飯塚市・朝倉市・田川郡の厳選10コース。料金順で並べました。各カードの「コース詳細」から料金比較・予約リンクへ。',
     '飯塚市・田川郡・直方市の9コースと、筑紫野市のセントラル福岡。カードの料金はじゃらんの18H最安（2026年11月1日時点）です。各カードの「コース詳細」から料金比較・予約リンクへ。', 1),
    ('→原鶴温泉泊→朝倉ラウンド→秋月散策→', '→原鶴温泉泊→セントラル福岡（筑紫野市）ラウンド→秋月散策→', 1),
    ('<div class="plan-title">朝倉ラウンド + 秋月散策</div>', '<div class="plan-title">セントラル福岡ラウンド + 秋月散策</div>', 1),
    ('旅館発→<strong>セントラル福岡</strong>へ（約30分）。', '旅館発→<strong>セントラル福岡</strong>（筑紫野市）へ。', 1),
    ('セントラル福岡で18Hラウンド。3万坪の戦略性ある林間を堪能。', 'セントラル福岡で18Hラウンド。林間コースを堪能。', 1),
    ('Pontaポイント1%還元 ｜ Web予約で平均¥3,000お得', 'Pontaポイントが貯まる', 1),
    ('<div class="faq-a">セントラル福岡（朝倉郡）と茜カントリークラブ（飯塚市）の2コースが筑豊エリアの代表格。どちらも平日¥6,500〜と料金が手頃で、戦略性も初心者対応もバランス良し。初訪問なら最優先で検討するべき2コースです。</div>',
     f'<div class="faq-a">{FAQ1_JA}</div>', 1),
    ('<div class="faq-a">福岡レイクサイドカントリークラブが平日¥6,000〜と筑豊エリア最安。池絡みの戦略コースで、価格以上のプレー価値あり。午後スルーなら¥4,000台のプランもあるので、コスパ重視ならまずココ。</div>',
     f'<div class="faq-a">{FAQ3_JA}</div>', 1),
    ('福岡空港・博多駅から全コース60〜75分圏内、午前ハーフ・午後スルー・1.5ラウンドなど時間調整も柔軟。', '福岡空港・博多駅から全コース60〜75分圏内。', 2),

    # ---- EN ----
    ('Real ¥6,000-tier weekday rates, Harazuru onsen pairing,', 'Weekday 18 holes from ¥4,605 (Jalan, Nov 1, 2026), Harazuru onsen pairing,', 1),
    ('<span class="hero-badge">💰 Weekday ¥6,000〜</span>', '<span class="hero-badge">💰 Weekday ¥4,605〜 (Nov 1)</span>', 1),
    ('<div class="stat-num">¥6,000<span class="unit">〜</span></div><div class="stat-label">Lowest weekday</div>',
     '<div class="stat-num">¥4,605<span class="unit">〜</span></div><div class="stat-label">Lowest weekday (Nov 1)</div>', 1),
    ('<td>Asakura · Pairs with Harazuru Onsen</td>', '<td>Chikushino · Accordia</td>', 1),
    ('<div class="compare-foot-note">💡 Walk-in rates avg. +¥3,000 vs. <strong style="color:var(--earth-dark)">Jalan web booking</strong> (lowest across all 4 courses).</div>',
     '<div class="compare-foot-note">💡 Rates are <strong style="color:var(--earth-dark)">Jalan\'s lowest 18-hole plans as of Nov 1, 2026</strong>. Akane is not on Jalan — check Rakuten GORA.</div>', 1),
    ('<div class="reason-title">Real ¥5–6k weekday rates</div>', '<div class="reason-title">Lowest rates of our 5 areas</div>', 1),
    ('<div class="reason-desc">A clear tier below Itoshima and Chikugo. Afternoon-thru rates can dip to ¥4,000. Best value in Fukuoka Prefecture, period.</div>',
     '<div class="reason-desc">The nine Jalan-listed courses on this page have a median lowest weekday 18-hole rate of ¥6,323 — the lowest of our five areas (as of Nov 1, 2026). Cheapest: Satsuki Ryuoh from ¥4,605.</div>', 1),
    ('Curated picks from Iizuka and Asakura. Each card links to the full course page with pricing and booking.',
     'Nine courses in Iizuka, Tagawa and Nogata, plus Central Fukuoka in Chikushino. Card rates are Jalan\'s lowest 18-hole plans as of Nov 1, 2026. Each card links to the full course page with pricing and booking.', 1),
    ('→ Harazuru Onsen → Asakura round → Akizuki', '→ Harazuru Onsen → Central Fukuoka (Chikushino) round → Akizuki', 1),
    ('<div class="plan-title">Asakura round + Akizuki walk</div>', '<div class="plan-title">Central Fukuoka round + Akizuki walk</div>', 1),
    ('Depart ryokan → <strong>Central Fukuoka GC</strong> (~30 min).', 'Depart ryokan → <strong>Central Fukuoka GC</strong> (Chikushino City).', 1),
    ('18 holes at Central Fukuoka. Strategic forest layout on a 100,000-sqm property.', '18 holes at Central Fukuoka\'s forest layout.', 1),
    ('Ponta Points 1% back ｜ Save avg. ¥3,000 vs walk-in', 'Earn Ponta Points', 1),
    ('<div class="faq-a">Central Fukuoka (Asakura) and Akane CC (Iizuka). Both around ¥6,500 weekdays, balanced strategy and beginner-friendliness — clear top picks for a first visit.</div>',
     '<div class="faq-a">Choosing by location is easiest: six courses are in Iizuka (Aso Iizuka, Akane, Lakeside, Kaho, Satsuki Ryuoh, JR Uchino), two in Tagawa District (Takaha Royal, Pheasant) and Nishi-Nippon is in Nogata. Central Fukuoka is in Chikushino, outside Chikuho. For price, see "Best value?".</div>', 1),
    ('<div class="faq-a">Fukuoka Lakeside CC at ¥6,000 weekday — the lowest in Chikuho. Strategic water-hazard layout that delivers more than its price. Afternoon-thru drops to ¥4,000-tier on some plans.</div>',
     '<div class="faq-a">On Jalan\'s lowest 18-hole plans (as of Nov 1, 2026), Satsuki Golf Club Ryuoh Course is the cheapest on this page at ¥4,605 on weekdays, followed by Fukuoka Pheasant (¥4,959) and Takaha Royal (¥5,596). Rates change daily — check the booking site before you book.</div>', 1),
    (', and afternoon-thru play makes for a tidy half-day plan.', '.', 1),

    # ---- KO ----
    ('평일 ¥6,000대 리얼 가격, 하라즈루 온천 세트,', '평일 18홀 ¥4,605부터(자란·2026년 11월 1일 기준), 하라즈루 온천 세트,', 1),
    ('<span class="hero-badge">💰 평일 ¥6,000대</span>', '<span class="hero-badge">💰 평일 ¥4,605〜(11/1)</span>', 1),
    ('<div class="stat-num">¥6,000<span class="unit">〜</span></div><div class="stat-label">평일 최저</div>',
     '<div class="stat-num">¥4,605<span class="unit">〜</span></div><div class="stat-label">평일 최저(11/1)</div>', 1),
    ('<td>아사쿠라·하라즈루 온천 세트 가능</td>', '<td>지쿠시노·아코디아</td>', 1),
    ('<div class="compare-foot-note">💡 당일 요금은 평균 +¥3,000. <strong style="color:var(--earth-dark)">자란골프 Web 예약</strong>이 거의 모든 코스 최저가.</div>',
     '<div class="compare-foot-note">💡 요금은 <strong style="color:var(--earth-dark)">자란 18홀 최저가(2026년 11월 1일 기준)</strong>. 아카네는 자란에 없으므로 라쿠텐 GORA에서 확인.</div>', 1),
    ('<div class="reason-title">평일 5–6천엔대 가성비</div>', '<div class="reason-title">5개 에리어 중 가장 저렴</div>', 1),
    ('<div class="reason-desc">평일 ¥5,000〜6,000대의 리얼 가격. 이토시마·치쿠고보다 한 단계 저렴, 오후 스루는 ¥4,000대 플랜도. 가성비 중시라면 치쿠호·아사쿠라가 후쿠오카현 베스트.</div>',
     '<div class="reason-desc">이 페이지 9개 코스(자란 등록)의 평일 18홀 최저가 중앙값은 ¥6,323으로, 당 사이트 5개 에리어 중 가장 낮은 수준(2026년 11월 1일 기준). 최저는 사쓰키 류오의 ¥4,605부터.</div>', 1),
    ('이이즈카시·아사쿠라시의 엄선 10코스. 각 카드의「코스 상세」에서 요금 비교·예약 링크 확인 가능.',
     '이이즈카시·다가와군·노가타시의 9개 코스와 지쿠시노시의 센트럴 후쿠오카. 카드 요금은 자란 18홀 최저가(2026년 11월 1일 기준). 각 카드의「코스 상세」에서 요금 비교·예약 링크 확인 가능.', 1),
    ('→하라즈루 온천 숙박→아사쿠라 라운드→', '→하라즈루 온천 숙박→센트럴 후쿠오카(지쿠시노시) 라운드→', 1),
    ('<div class="plan-title">아사쿠라 라운드 + 아키즈키 산책</div>', '<div class="plan-title">센트럴 후쿠오카 라운드 + 아키즈키 산책</div>', 1),
    ('료칸 출발→<strong>센트럴 후쿠오카</strong>로(약 30분).', '료칸 출발→<strong>센트럴 후쿠오카</strong>(지쿠시노시)로.', 1),
    ('센트럴 후쿠오카에서 18H 라운드. 3만 평의 전략성 있는 숲을 만끽.', '센트럴 후쿠오카에서 18H 라운드. 숲 코스를 만끽.', 1),
    ('폰타포인트 1% 적립 ｜ Web 예약으로 평균 ¥3,000 절약', '폰타포인트 적립', 1),
    ('<div class="faq-a">센트럴 후쿠오카(아사쿠라군)와 아카네 컨트리 클럽(이이즈카시) 2개 코스가 치쿠호 에리어 대표격. 둘 다 평일 ¥6,500〜의 합리적 요금, 전략성과 초보자 대응의 밸런스가 좋음. 첫 방문이라면 최우선 검토.</div>',
     '<div class="faq-a">소재지로 고르면 알기 쉽습니다. 이이즈카시에 6개(아소 이이즈카·아카네·레이크사이드·카호·사쓰키 류오·JR 우치노), 다가와군에 2개(다카하 로열·페즌트), 노가타시에 니시니혼. 센트럴 후쿠오카는 지쿠시노시로 치쿠호 밖에 있습니다. 요금으로 고른다면 「가성비 최고는?」을 참고하세요.</div>', 1),
    ('<div class="faq-a">후쿠오카 레이크사이드 CC가 평일 ¥6,000〜으로 치쿠호 에리어 최저. 물 얽힌 전략 코스로 가격 이상의 플레이 가치. 오후 스루는 ¥4,000대 플랜도 있어 가성비 중시라면 우선 이곳.</div>',
     '<div class="faq-a">자란 18홀 최저가(2026년 11월 1일 기준)로는 사쓰키 골프 클럽 류오 코스가 평일 ¥4,605부터로 이 페이지에서 가장 저렴하고, 후쿠오카 페즌트(¥4,959〜), 다카하 로열(¥5,596〜)이 뒤를 잇습니다. 요금은 날짜에 따라 바뀌므로 예약 전에 예약 사이트에서 확인하세요.</div>', 1),
    ('FUK·하카타역에서 모든 코스 60〜75분권, 오전 하프·오후 스루·1.5라운드 등 시간 조정도 유연.', 'FUK·하카타역에서 모든 코스 60〜75분권.', 1),
]

# 正規表現 (属性値を丸ごと置換)
RX = [
    (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{META_JA}">'),
    (r'<meta name="description" lang="en" content="[^"]*">',
     '<meta name="description" lang="en" content="Guide to 10 golf courses: nine in Chikuho (Iizuka, Tagawa, Nogata) plus Central Fukuoka in Chikushino. Jalan\'s lowest weekday 18-hole plans start at ¥4,605 (as of Nov 1, 2026). Compare rates, access and features.">'),
    (r'<meta name="description" lang="ko" content="[^"]*">',
     '<meta name="description" lang="ko" content="치쿠호(이이즈카·다가와·노가타) 9개 코스와 지쿠시노시의 센트럴 후쿠오카 가이드. 자란 18홀 최저가(2026년 11월 1일 기준)는 평일 ¥4,605부터. 요금·접근성·특징 비교.">'),
    (r'("headline": "[^"]*",\s*"description": )"[^"]*"', r'\1"' + META_JA + '"'),
]

# 比較表 (3言語とも 4行: セントラル・あかね・麻生飯塚・レイクサイド)
ROWS = [("¥6,323〜", "¥13,141〜"), (None, None), ("¥10,273〜", "¥14,000〜"), ("¥7,241〜", "¥12,150〜")]
RAKUTEN = {"ja": "楽天GORAで確認", "en": "Rakuten GORA", "ko": "라쿠텐 GORA"}


def fix_table(t):
    def tbl(m):
        lang = (re.findall(r'<div id="c-(ja|en|ko)" class="content', t[:m.start()]) or ["ja"])[-1]
        rows = re.findall(r"<tr[ >].*?</tr>", m.group(0), re.S)[1:]
        assert len(rows) == 4, len(rows)
        out = m.group(0)
        for row, (wd, we) in zip(rows, ROWS):
            new = row
            wd = wd or RAKUTEN[lang]; we = we or RAKUTEN[lang]
            new = re.sub(r'(<span class="compare-price-weekday">)[^<]*(</span>)', lambda x: x.group(1) + wd + x.group(2), new)
            new = re.sub(r'(<span class="compare-price-weekend">)[^<]*(</span>)', lambda x: x.group(1) + we + x.group(2), new)
            out = out.replace(row, new)
        return out
    return re.sub(r'<table class="compare-table">.*?</table>', tbl, t, flags=re.S)


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
    for pat, rep in RX:
        t, k = re.subn(pat, lambda m: m.expand(rep) if "\\1" in rep else rep, t, count=1)
        assert k == 1, pat
    t = fix_table(t)
    print(c, "変更あり" if t != src else "変更なし")
    if APPLY and t != src:
        for root in ROOTS:
            open(os.path.join(root, NAME), "w", encoding="utf-8", newline="").write(t)
        print("APPLIED", ROOTS)
    elif not APPLY:
        print("DRY-RUN")


if __name__ == "__main__":
    main()
