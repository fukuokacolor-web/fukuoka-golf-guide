#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
book-fukuoka-golf-foreigner.html のページ全体の金額表現を直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日¥3,500〜」 → じゃらん18H最安 (2026-11-01) の平日最安は ¥4,605 (皐月竜王)
- 「平日¥3,500〜9,000」「東京・箱根は¥10,000〜18,000」「韓国首都圏の1/2〜1/3」「東京・大阪よりコスパ」 → 前半は実データに、比較は根拠なしで削除
  (平日プランのある32コース中 20 コースが平日¥9,000以下)
- 「平日は土日より30〜50%安い」 → 両方そろう30コースで 22〜60%・中央値39%
- 早朝スルー「6:30スタート・11:30終了」 → 根拠なし (時刻を外す)
- キャディ付 +¥3,000〜5,000・昼食付 +¥1,000・2サム保証 +¥1,000〜2,000・「セルフ昼食付が最安」 → 根拠なし
- レンタルクラブ ¥2,000〜4,000・シューズ ¥1,500〜2,000・航空会社の超過料金 ¥10,000〜20,000 → 根拠なし
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)
金額以外の要確認 (空港から20分/25分・福岡CCが最寄り・80%が飛び込み可・海外電話番号で予約可・キャンセル規定・推奨3コース) は別途。
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_foreigner_2026_11.py            # dry-run
  python scripts/fix_foreigner_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_foreigner_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "book-fukuoka-golf-foreigner.html"
BAND = '<div class="persona-band-num">¥3,500<span class="unit">+</span></div>\r\n        <div class="persona-band-label">{}</div>'
BAND_NEW = '<div class="persona-band-num">¥4,605<span class="unit">+</span></div>\r\n        <div class="persona-band-label">{}</div>'

# (旧, 新, 出現回数)
R = [
    # ---- JSON-LD FAQ ----
    ('"text": "Yes — most public courses rent clubs for ¥2,000–4,000. Reserve when you book, or call the course the day before to confirm availability."',
     '"text": "Yes — most public courses rent clubs. Fees vary by course, so check the plan details or ask the course. Reserve when you book, or call the course the day before to confirm availability."', 1),
    # ---- JA ----
    ('<p>福岡は日本国内でも有数のゴルフリゾートです。福岡空港から最短20分・35コース・平日¥3,500〜という条件は、東京・大阪より明らかにコスパが高く、韓国・台湾・香港・シンガポールから「弾丸ゴルフ旅行」に来る海外ゴルファーが年々増えています。</p>',
     '<p>福岡には当サイトで紹介している35のゴルフ場があり、じゃらんの18H最安は平日¥4,605〜（2026年11月1日時点）。韓国・台湾・香港・シンガポールからも近く、短い日程の「弾丸ゴルフ旅行」を組みやすい場所です。</p>', 1),
    # ---- EN ----
    ('<span class="hero-badge">💴 From ¥3,500 weekdays</span>', '<span class="hero-badge">💴 Weekdays from ¥4,605 (Nov 1)</span>', 1),
    (BAND.format("Weekday rates"), BAND_NEW.format("Lowest weekday (Nov 1)"), 1),
    ('<div class="why-title">Half the price of Tokyo</div>', '<div class="why-title">Weekday rounds from under ¥5,000</div>', 1),
    ('<div class="why-desc">Weekday rounds at quality courses run ¥3,500–9,000. The same level in Tokyo or Hakone is ¥10,000–18,000. Weekend rates climb but stay reasonable, especially for early-morning ("morning thru") plans.</div>',
     '<div class="why-desc">On Jalan (lowest 18-hole plans, as of Nov 1, 2026), weekday rounds start at ¥4,605, and 20 of the 32 Fukuoka courses with weekday plans were ¥9,000 or less. Weekends cost more — see below.</div>', 1),
    ('<strong>Weekdays (平日 / hira-jitsu)</strong> are 30–50% cheaper than <strong>weekends (土日 / dō-nichi)</strong>. <strong>Morning thru (早朝スルー)</strong> tees you off at 6:30 AM and you\'re done by 11:30 — perfect for a same-day flight.',
     '<strong>Weekdays (平日 / hira-jitsu)</strong> are usually much cheaper than <strong>weekends (土日 / dō-nichi)</strong> — across 30 Fukuoka courses on Jalan (Nov 1, 2026), the lowest weekday plan was 22–60% below the lowest weekend plan (median 39%). <strong>Morning thru (早朝スルー)</strong> plans tee off early and skip the lunch break — handy before a same-day flight.', 1),
    ('<strong>キャディ付 (caddie included)</strong> = local caddie. Adds ¥3,000–5,000. Rare at public courses.<br>',
     '<strong>キャディ付 (caddie included)</strong> = local caddie. Costs more than a self plan. Rare at public courses.<br>', 1),
    ('<strong>昼食付 (lunch included)</strong> = halfway-house lunch bundled. Usually +¥1,000.<br>',
     '<strong>昼食付 (lunch included)</strong> = halfway-house lunch bundled into the plan price.<br>', 1),
    ('<strong>2サム保証</strong> = guaranteed 2-player tee time (no joining strangers). Adds ¥1,000–2,000.</p>',
     '<strong>2サム保証</strong> = guaranteed 2-player tee time (no joining strangers). Compare its price with the regular plans.</p>', 1),
    ('"セルフ・昼食付" (self + lunch) is the simplest and cheapest combination.', '"セルフ・昼食付" (self + lunch) is the simplest combination.', 1),
    ('Yes — most public courses rent clubs (¥2,000–4,000) and shoes (¥1,500–2,000) on the day.',
     'Yes — most public courses rent clubs and shoes on the day. Fees vary by course, so check the plan details or ask the course.', 1),
    ('If you\'re flying in just for golf, rent. Saving the airline overweight fee (¥10,000–20,000 round-trip per bag) covers two rounds of rentals.',
     'If you\'re flying in just for golf, renting is simpler. Airline fees for a golf bag vary by carrier — compare them with the course\'s rental fee.', 1),
    # ---- KO ----
    ('<span class="hero-badge">💴 평일 ¥3,500〜</span>', '<span class="hero-badge">💴 평일 ¥4,605〜(11/1 기준)</span>', 1),
    (BAND.format("평일 요금"), BAND_NEW.format("평일 최저가(11/1)"), 1),
    ('<div class="why-title">한국보다 저렴, 도쿄의 절반</div>', '<div class="why-title">평일 ¥5,000 미만부터</div>', 1),
    ('<div class="why-desc">평일 ¥3,500~9,000은 한국 수도권의 1/2~1/3 가격. 도쿄·하코네는 ¥10,000~18,000. 「얼리/오후 스루」 플랜이라면 더 저렴하게 18홀이 가능합니다.</div>',
     '<div class="why-desc">자란 18홀 최저가(2026년 11월 1일 기준)로 평일 ¥4,605부터. 평일 플랜이 있는 후쿠오카 32개 코스 중 20개 코스가 평일 ¥9,000 이하였습니다. 주말은 더 비쌉니다(아래 참고).</div>', 1),
    ('<strong>평일(平日 / heijitsu)</strong>은 <strong>주말(土日 / dōnichi)</strong>보다 30~50% 저렴. <strong>「얼리 스루」(早朝スルー)</strong>는 6:30 티오프, 11:30 종료 — 당일 비행기로 돌아가기에 최적.',
     '<strong>평일(平日 / heijitsu)</strong>은 <strong>주말(土日 / dōnichi)</strong>보다 대체로 훨씬 저렴 — 자란의 후쿠오카 30개 코스(2026년 11월 1일 기준)에서 평일 최저가는 주말 최저가보다 22~60% 낮았습니다(중앙값 39%). <strong>「얼리 스루」(早朝スルー)</strong>는 이른 아침에 시작해 점심 휴식 없이 도는 플랜 — 당일 비행기로 돌아갈 때 편리.', 1),
    ('= 현지 캐디 동반. +¥3,000~5,000. 퍼블릭 코스에는 드뭄.<br>', '= 현지 캐디 동반. 셀프 플랜보다 비쌈. 퍼블릭 코스에는 드뭄.<br>', 1),
    ('= 중간 휴식 시 점심 포함. 보통 +¥1,000.<br>', '= 중간 휴식 시 점심이 플랜 요금에 포함.<br>', 1),
    ('= 2인 보장 (모르는 사람과 합류 안 함). +¥1,000~2,000.</p>', '= 2인 보장 (모르는 사람과 합류 안 함). 일반 플랜과 요금을 비교하세요.</p>', 1),
    ('「セルフ・昼食付」(셀프+점심)이 가장 단순하고 저렴.', '「セルフ・昼食付」(셀프+점심)이 가장 단순.', 1),
    ('네 — 대부분 퍼블릭 코스에서 클럽(¥2,000~4,000)과 신발(¥1,500~2,000) 당일 대여.',
     '네 — 대부분 퍼블릭 코스에서 클럽과 신발 당일 대여. 요금은 코스마다 다르니 플랜 상세나 코스에 확인하세요.', 1),
    ('골프 목적의 단기 여행이면 대여 추천. 항공 수하물 추가 요금(왕복 ¥10,000~20,000/백)이면 라운드 2회분 대여비.',
     '골프 목적의 단기 여행이면 대여가 간편. 골프백 항공 수하물 요금은 항공사마다 다르니 코스 렌탈 요금과 비교하세요.', 1),
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
