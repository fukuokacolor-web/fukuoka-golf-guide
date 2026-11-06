#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
3件をまとめて直す (book-fukuoka-cheap.html 本体は rebuild_cheap_guide.py で 11/1 データに作り直し済)。

1. course-queenshill.html: 料金カード ¥15,396〜/¥19,487〜 と「午後スルー」は公式と不一致 →
   公式料金ページ (queenshill.co.jp/price/・2026-11-04 確認) のゲスト 平日¥21,800・土日祝¥30,200 (税込・キャディフィ4バッグ込・2026/3/1〜)、
   3バッグ¥1,850増・2バッグ¥6,000増・乗用カート1台¥5,000 (オプション) に。午後スルーの記載は公式に無い
2. course-saitozaki.html: 予約カード「最安¥3,500〜」 → 楽天の公開ページから料金を確認できないので、akane と同じ「楽天GORAで確認」に
3. 格安ページへのリンク文言「9コース」 → 総額¥8,000以下は 11/1 時点で 11 コース
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_queenshill_cheaplinks_2026_11.py            # dry-run
  python scripts/fix_queenshill_cheaplinks_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_queenshill_cheaplinks_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
AMOUNT = '<span class="yen">¥</span>{}<span class="range">〜</span>'
AMOUNT_NEW = '<span class="yen">¥</span>{}'
KRW = ' <span style="color:var(--ocean);font-size:12px;"><span style="color:#1a3a8f;font-size:0.78rem;">(약 {}만원)</span></span>'
LINK_JA = "平日¥8,000以下で回れる9コース比較"
LINK_JA_NEW = "平日¥8,000以下で回れる11コース比較"

# {ファイル: [(旧, 新, 出現回数)]}
FILES = {
    "course-queenshill.html": [
        (AMOUNT.format("15,396"), AMOUNT_NEW.format("21,800"), 3),
        (AMOUNT.format("19,487"), AMOUNT_NEW.format("30,200"), 3),
        ('<div class="price-note">月〜金（祝日除く）。</div>', '<div class="price-note">月〜金（祝日除く）。公式料金（税込・キャディフィ4バッグ込、2026年3月〜）。</div>', 1),
        ('<div class="price-note">土・日・祝日。人気時間帯は早めの予約を。</div>', '<div class="price-note">土・日・祝日。公式料金（税込・キャディフィ4バッグ込、2026年3月〜）。</div>', 1),
        ('<div class="price-note">Often includes lunch and facility fees.</div>', '<div class="price-note">Official rate (tax and caddie fee for 4 bags included, from March 2026).</div>', 1),
        ('<div class="price-note">Peak times book out early — reserve ahead.</div>', '<div class="price-note">Official rate (tax and caddie fee for 4 bags included, from March 2026).</div>', 1),
        ('<div class="price-note">월〜금 (공휴일 제외).' + KRW.format(22) + '</div>', '<div class="price-note">월〜금 (공휴일 제외). 공식 요금(세금·캐디피 4백 포함, 2026년 3월〜).</div>', 1),
        ('<div class="price-note">인기 시간대는 일찍 예약하세요.' + KRW.format(30) + '</div>', '<div class="price-note">토·일·공휴일. 공식 요금(세금·캐디피 4백 포함, 2026년 3월〜).</div>', 1),
        ('<strong>午後スルーなどプレースタイルも選べる</strong>時間や予算に合わせて柔軟に楽しめるのが魅力です。', '<strong>キャディ付のラウンド</strong>公式のゲスト料金はキャディフィ込みで、乗用カートはオプションです。', 1),
        ('<strong>Flexible play styles</strong>Choose morning rounds with a half-turn break, or afternoon-through for half-day value.', '<strong>Rounds with a caddie</strong>The official guest rate includes the caddie fee; a riding cart is optional.', 1),
        ('<strong>유연한 플레이 스타일</strong>오전 라운드·오후 스루 등 시간과 예산에 맞춰 선택할 수 있습니다.', '<strong>캐디 동반 라운드</strong>공식 게스트 요금에 캐디피가 포함되며, 승용 카트는 옵션입니다.', 1),
        ('<div class="play-card-title">午後スルー</div>', '<div class="play-card-title">キャディ付・カートはオプション</div>', 1),
        ('<div class="play-card-desc">午後スタート・休憩なしで18ホール続けてプレー。半日でラウンドできて料金もお得。</div>',
         '<div class="play-card-desc">公式料金は4バッグ時のもので、3バッグは¥1,850増、2バッグは¥6,000増。乗用カートは1台¥5,000のオプションで、予約時に申し込みます（公式料金ページ）。</div>', 1),
        ('<div class="play-card-title">Afternoon Through</div>', '<div class="play-card-title">Caddie included, cart optional</div>', 1),
        ('<div class="play-card-desc">Afternoon start, 18 holes played straight through — half-day golf at the best price.</div>',
         '<div class="play-card-desc">Official rates are for 4 bags: add ¥1,850 for 3 bags or ¥6,000 for 2 bags. A riding cart is an optional ¥5,000 per cart, reserved when you book (official price page).</div>', 1),
        ('<div class="play-card-title">오후 스루</div>', '<div class="play-card-title">캐디 포함·카트는 옵션</div>', 1),
        ('<div class="play-card-desc">오후 출발, 휴식 없이 18홀 연속 플레이. 반나절에 끝나고 요금도 가성비 최고.</div>',
         '<div class="play-card-desc">공식 요금은 4백 기준으로, 3백은 ¥1,850 추가, 2백은 ¥6,000 추가. 승용 카트는 1대 ¥5,000의 옵션으로 예약 시 신청합니다(공식 요금 페이지).</div>', 1),
        ('<h2 class="sec-title">Two ways to play.</h2>', '<h2 class="sec-title">How rounds work here.</h2>', 1),
        ('<h2 class="sec-title">두 가지 플레이 방식.</h2>', '<h2 class="sec-title">라운드 안내.</h2>', 1),
    ],
    "course-saitozaki.html": [
        ('<div class="booking-price-tag">最安 <span class="big">¥3,500</span>〜</div>', '<div class="booking-price-tag">料金は <span class="big">楽天GORAで確認</span></div>', 1),
        ('<div class="booking-price-tag">From <span class="big">¥3,500</span></div>', '<div class="booking-price-tag">Rates <span class="big">on Rakuten GORA</span></div>', 1),
    ],
    "book-fukuoka-solo.html": [(LINK_JA, LINK_JA_NEW, 1)],
    "book-fukuoka-tomorrow.html": [(LINK_JA, LINK_JA_NEW, 1)],
    "index.html": [(LINK_JA, LINK_JA_NEW, 2)],
    "hub-budget.html": [
        (LINK_JA, LINK_JA_NEW, 1),
        ("平日¥8,000以下 9コース比較表を見る", "平日¥8,000以下 11コース比較表を見る", 2),
    ],
    "guide-index.html": [
        ('"name": "格安まとめ（平日¥8,000以下 9コース）"', '"name": "格安まとめ（平日¥8,000以下 11コース）"', 1),
        ('<span class="guide-emoji">💴</span><span class="guide-badge">9コース</span>', '<span class="guide-emoji">💴</span><span class="guide-badge">11コース</span>', 1),
        ("平日¥8,000以下だった9コースを安い順に比較。", "平日¥8,000以下だった11コースを安い順に比較。", 1),
    ],
    "sitemap-guide.html": [
        (LINK_JA, LINK_JA_NEW, 1),
        ("💴 9 Courses ¥8,000 or less on Weekdays (JA only)", "💴 11 Courses ¥8,000 or less on Weekdays (JA only)", 1),
        ("💴 평일 ¥8,000 이하 9코스 비교 (일본어판)", "💴 평일 ¥8,000 이하 11코스 비교 (일본어판)", 1),
    ],
}


def main():
    for name, reps in FILES.items():
        src = open(os.path.join(REPO_ROOT, name), encoding="utf-8", newline="").read()
        t = src
        c = {"replaced": 0, "already": 0}
        for old, new, n in reps:
            k = t.count(old)
            if k == n:
                t = t.replace(old, new); c["replaced"] += 1
            elif k == 0 and t.count(new) >= n:
                c["already"] += 1
            else:
                raise SystemExit(f"NO_MATCH {name} ({k}/{n}): {old[:70]}")
        print(name, c, "変更あり" if t != src else "変更なし")
        if APPLY and t != src:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(t)
    print("APPLIED " + ",".join(r[-12:] for r in ROOTS) if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
