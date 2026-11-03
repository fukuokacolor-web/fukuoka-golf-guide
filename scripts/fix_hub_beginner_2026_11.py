#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hub-beginner.html のページ全体の金額表現と、確認できた事実誤りを直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「¥4,060〜」「¥4,000台〜」「平日¥4,060〜¥6,500台が中心」 → 本ハブでじゃらんに出ている平日18H最安は
  フェザント ¥4,959・かほ ¥6,323・うきは ¥6,332・セブンミリオン ¥10,600 (油山・あかねは楽天GORAのみ)
- 「レンタルクラブ込み¥7,000以下」「(関連ガイド) ¥3,500〜」 → 根拠なし
- 「本ハブ最安コース」(うきは)・「下にいくほど料金が下がり」 → 最安はフェザント。並びも料金順ではない
- 「英語/韓国語サポート」「韓国語OK・英語OK」 → 根拠なし (EN/KO 版の注記でも「予約サイトは日本の電話番号が必要・各コースへ直接」)
- フェザントの所在地「糸島」は誤り (じゃらん・コースページとも田川郡川崎町) → エリア導線も筑豊へ。うきは市は筑後エリア
- JA は 6 コース掲載なのに「5選」「5コース」 (EN/KO は 5 コースのまま正しい)
数値の出典: scripts/.cache/jalan_floor.json (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_hub_beginner_2026_11.py            # dry-run
  python scripts/fix_hub_beginner_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_hub_beginner_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "hub-beginner.html"
BADGE = '\r\n        <span class="hero-badge">'
AREA = '<a href="{href}" class="area-card"><span class="area-card-name">{name}</span>'

# (旧, 新, 出現回数)
R = [
    # ---- head ----
    ('content="ゴルフ初心者のための福岡ゴルフ場ガイド。ショートコース・フラットレイアウト・¥4,000台〜の手頃な料金、英語/韓国語サポートのある初心者歓迎コース5選。ドレスコードもやさしいクラブを厳選。"',
     'content="ゴルフ初心者のための福岡ゴルフ場ガイド。ショートコース・フラットレイアウト中心の初心者向け6コース。じゃらんの18H最安は平日¥4,959〜（2026年11月1日時点）。ドレスコードもやさしいクラブを厳選。"', 1),
    ('content="A Fukuoka golf hub for beginners. Five beginner-friendly courses with short layouts, flat fairways, prices from ¥4,000, and clubs with English/Korean support — all without the stuffiness."',
     'content="A Fukuoka golf hub for beginners. Five beginner-friendly courses with short layouts and flat fairways — weekday 18-hole plans from ¥4,959 on Jalan (as of Nov 1, 2026), all without the stuffiness."', 1),
    ('content="후쿠오카 골프 초보자를 위한 허브 가이드. 짧은 코스·평지 레이아웃·¥4,000부터의 합리적 요금, 영어/한국어 지원이 가능한 초보자 환영 코스 5선. 드레스코드도 편안한 클럽을 엄선."',
     'content="후쿠오카 골프 초보자를 위한 허브 가이드. 짧은 코스·평지 레이아웃 중심의 초보자 환영 코스 5선. 자란 18홀 최저가는 평일 ¥4,959부터(2026년 11월 1일 기준). 드레스코드도 편안한 클럽을 엄선."', 1),
    ('<title>初心者向け｜福岡ゴルフ場 5選 — ショート・フラット・¥4,000〜の入門ハブ | 福岡ゴルフ場ガイド</title>',
     '<title>初心者向け｜福岡ゴルフ場 6選 — ショート・フラット中心の入門ハブ | 福岡ゴルフ場ガイド</title>', 1),
    ('"name": "初心者向けゴルフコース 5選｜福岡"', '"name": "初心者向けゴルフコース 6選｜福岡"', 1),
    ('"description": "ゴルフ初心者でも安心の福岡ゴルフ場5選。', '"description": "ゴルフ初心者でも安心の福岡ゴルフ場6選。', 1),
    ('<meta property="og:title" content="初心者向け｜福岡ゴルフ場 5選 — ショート・フラット・¥4,000〜の入門ハブ">',
     '<meta property="og:title" content="初心者向け｜福岡ゴルフ場 6選 — ショート・フラット中心の入門ハブ">', 1),
    ('福岡の初心者向けコース5選。">', '福岡の初心者向けコース6選。">', 1),
    # ---- JA hero / band / why ----
    ('<div class="hero-sub">ショートコース・フラットレイアウト・¥4,000台〜の手頃な料金。「ゴルフ場って怖い」を払拭する、初心者にやさしい福岡の5コース。</div>',
     '<div class="hero-sub">ショートコース・フラットレイアウト中心。「ゴルフ場って怖い」を払拭する、初心者にやさしい福岡の6コース。</div>', 1),
    ('<span class="hero-badge">💴 ¥4,060〜</span>', '<span class="hero-badge">💴 平日¥4,959〜（11/1時点）</span>', 1),
    (BADGE + '🇰🇷 韓国語OK・🇬🇧 英語OK</span>', '', 1),
    ('<div class="persona-band-num">5<span class="unit">コース</span></div>', '<div class="persona-band-num">6<span class="unit">コース</span></div>', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">最安</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">平日最安（11/1）</div>', 1),
    ('<div class="why-title">料金が透明・手頃</div>', '<div class="why-title">料金を事前に確認できる</div>', 1),
    ('<div class="why-desc">平日¥4,060〜¥6,500台が中心。じゃらんゴルフのWeb予約で前日まで料金が確定し、現地での想定外請求がない安心感。レンタルクラブ込み¥7,000以下も狙えます。</div>',
     '<div class="why-desc">じゃらんの18H最安（2026年11月1日時点）は平日でフェザント¥4,959・かほ¥6,323・うきは¥6,332。予約サイトでは予約するときにプランの料金が表示されるので、当日の支払いを前もって見込めます。</div>', 1),
    ('1〜5は「都心・短い」→「フラット・林間」→「料金最安」の順で、下にいくほど料金が下がり、上にいくほどアクセスがいい構成。',
     '1〜5は「都心・短い」→「フラット・林間」→「郊外」の順で、上にいくほど福岡市中心部から近い構成。', 1),
    # ---- EN hero / band / why ----
    ('<div class="hero-sub">Short courses, flat fairways, and prices from ¥4,060. Five welcoming',
     '<div class="hero-sub">Short courses and flat fairways. Five welcoming', 1),
    ('<span class="hero-badge">💴 From ¥4,060</span>', '<span class="hero-badge">💴 Weekdays from ¥4,959 (Nov 1)</span>', 1),
    (BADGE + '🇰🇷 KO &amp; 🇬🇧 EN support</span>', '', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">Lowest fee</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">Lowest weekday (Nov 1)</div>', 1),
    ('<div class="why-title">Transparent, honest pricing</div>', '<div class="why-title">Know the price before you go</div>', 1),
    ('<div class="why-desc">Weekday fees mostly ¥4,060–¥6,500. Jalan Golf locks in the rate before you arrive — no surprise charges at the desk. Rentals included, you can finish under ¥7,000.</div>',
     '<div class="why-desc">Jalan\'s lowest weekday 18-hole plans (as of Nov 1, 2026): Pheasant ¥4,959, Ukiha ¥6,332. Booking sites show the plan price when you book, so you know roughly what you\'ll pay on the day.</div>', 1),
    ('Ordered roughly: most accessible (top) → lowest price (bottom).', 'Ordered roughly: closest to central Fukuoka (top) → further out (bottom).', 1),
    # ---- KO hero / band / why ----
    ('<div class="hero-sub">짧은 코스·평지 페어웨이·¥4,060부터의 합리적 요금. ', '<div class="hero-sub">짧은 코스·평지 페어웨이 중심. ', 1),
    ('<span class="hero-badge">💴 ¥4,060부터</span>', '<span class="hero-badge">💴 평일 ¥4,959부터(11/1 기준)</span>', 1),
    (BADGE + '🇰🇷 한국어 OK</span>', '', 1),
    ('<div class="persona-band-num">¥4,060<span class="unit">〜</span></div><div class="persona-band-label">최저가</div>',
     '<div class="persona-band-num">¥4,959<span class="unit">〜</span></div><div class="persona-band-label">평일 최저가(11/1)</div>', 1),
    ('<div class="why-desc">평일 ¥4,060〜¥6,500대 중심. 자란 골프 웹예약으로 사전에 가격이 확정되어, 현장에서 예상 외 청구가 없는 안심감. 렌탈 포함 ¥7,000 이하도 가능합니다.</div>',
     '<div class="why-desc">자란 18홀 최저가(2026년 11월 1일 기준)는 평일 페전트 ¥4,959·우키하 ¥6,332. 예약 사이트에서는 예약할 때 플랜 요금이 표시되어, 당일 지불액을 미리 가늠할 수 있습니다.</div>', 1),
    ('"도심·짧은 코스" → "평탄·임간" → "최저가" 순. 위로 갈수록 접근성, 아래로 갈수록 가격 메리트가 큽니다.',
     '"도심·짧은 코스" → "평탄·임간" → "교외" 순. 위로 갈수록 후쿠오카 시내에서 가깝습니다.', 1),
    # ---- フェザント (所在地) ----
    ('<div class="course-area">Itoshima · Flat Forest · Accordia</div>', '<div class="course-area">Tagawa District · Flat Forest · Accordia</div>', 3),
    ('<span class="course-chip">糸島</span>', '<span class="course-chip">田川郡</span>', 1),
    ('<span class="course-chip">Itoshima</span>', '<span class="course-chip">Tagawa</span>', 1),
    ('<span class="course-chip">이토시마</span>', '<span class="course-chip">다가와군</span>', 1),
    ('<div class="course-desc">糸島エリアの<strong>高低差約20mのフラット林間コース</strong>。', '<div class="course-desc">田川郡川崎町の<strong>高低差約20mのフラット林間コース</strong>。', 1),
    ('A flat forest course in Itoshima with only ~20m total elevation change. Run by the Accordia group, with strong beginner-side hospitality — clear starter instructions, bilingual rentals, easy carts.',
     'A flat forest course in Kawasaki Town, Tagawa District, with only ~20m total elevation change. Run by the Accordia group, with strong beginner-side hospitality — clear starter instructions, rentals, easy carts.', 1),
    ('<div class="course-desc">이토시마 에리어의 <strong>고저차 약 20m', '<div class="course-desc">다가와군 가와사키마치의 <strong>고저차 약 20m', 1),
    # ---- うきは ----
    ('<div class="course-area">Ukiha · Lowest Price</div>', '<div class="course-area">Ukiha · Easygoing</div>', 3),
    ('<div class="course-desc">うきは市の<strong>本ハブ最安コース</strong>。料金プレッシャーが少ないので、<strong>多少スコアが乱れても気兼ねなく楽しめる</strong>のが最大の利点。原鶴温泉とのセット利用にも◎。</div>',
     '<div class="course-desc">うきは市の18Hコース。平日料金が手頃なので、<strong>多少スコアが乱れても気兼ねなく楽しめる</strong>のが利点。原鶴温泉（朝倉市）とあわせた遠征も組めます。</div>', 1),
    ('<div class="course-desc">우키하시의 <strong>본 허브 최저가 코스</strong>. 요금 부담이 적어', '<div class="course-desc">우키하시의 18홀 코스. 평일 요금 부담이 적어', 1),
    # ---- エリア導線 (フェザント=筑豊・うきは=筑後) ----
    (AREA.format(href="area-itoshima.html", name="🌊 糸島エリア（フェザント）"), AREA.format(href="area-chikuho.html", name="🏞️ 筑豊エリア（フェザント・あかね・かほ）"), 1),
    (AREA.format(href="area-chikuho.html", name="🏞️ 筑豊・朝倉（あかね・うきは）"), AREA.format(href="area-chikugo.html", name="🌾 筑後エリア（うきは）"), 1),
    (AREA.format(href="area-itoshima.html", name="🌊 Itoshima (Pheasant)"), AREA.format(href="area-chikuho.html", name="🏞️ Chikuho (Pheasant, Akane)"), 1),
    (AREA.format(href="area-chikuho.html", name="🏞️ Chikuho &amp; Asakura (Akane, Ukiha)"), AREA.format(href="area-chikugo.html", name="🌾 Chikugo (Ukiha)"), 1),
    (AREA.format(href="area-itoshima.html", name="🌊 이토시마 (페전트)"), AREA.format(href="area-chikuho.html", name="🏞️ 치쿠호 (페전트·아카네)"), 1),
    (AREA.format(href="area-chikuho.html", name="🏞️ 치쿠호·아사쿠라 (아카네·우키하)"), AREA.format(href="area-chikugo.html", name="🌾 치쿠고 (우키하)"), 1),
    # ---- 関連ガイド CTA ----
    ('margin-right:auto;">¥3,500〜・フラット・クラブレンタル対応。', 'margin-right:auto;">フラット・クラブレンタル対応。', 1),
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
