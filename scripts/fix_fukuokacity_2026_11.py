#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
area-fukuokacity.html のページ全体の金額表現と午後スルーの記述を直す (カード料金欄は fix_card_prices_2026_11.py で済)。

旧表現の根拠が無い/実データと違うもの:
- 「平日最安 ¥5,000〜」(JA)「¥3,500〜」(EN/KO) → じゃらん18H最安 (2026-11-01) は 大博多 ¥8,423・久山 ¥9,473・セブンミリオン ¥10,600・筑紫ヶ丘 ¥13,150
- 「西戸崎 平日¥3,500〜」「油山 ¥5,000前後」 → 2コースとも じゃらん予約不可。楽天の公開ページから料金を確認できない → 金額を出さず楽天GORAへ
- 「¥6,000前後なら セブンミリオン・大博多・久山・古賀」 → 実データと違う (古賀は公式のみ)
- 「手頃な料金でフルラウンド」(セブンミリオン) → じゃらん掲載4コース中2番目に高い
- 「午後スルー豊富」「西戸崎・福岡CC・久山・古賀は午後スルー対応日が多い」 → 11/1〜15 のじゃらんで 久山・大博多・セブンミリオン・筑紫ヶ丘に午後スルーなし。楽天の西戸崎ページにも記載なし。福岡CC は会員制 (メンバー同伴または紹介が必須)、古賀は公式のみ
- 「油山 2時間強」 → 根拠なし
- モデルプラン 2日目の福岡CC → カードの記述どおり会員同伴または紹介が必須と明記
数値の出典: scripts/.cache/jalan_floor.json・scripts/.cache/jalan_{gc}_202611*.html (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_fukuokacity_2026_11.py            # dry-run
  python scripts/fix_fukuokacity_2026_11.py --preview  # PREVIEW だけ
  python scripts/fix_fukuokacity_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
NAME = "area-fukuokacity.html"
STAT = '<div class="stat-num">{}<span class="unit">〜</span></div><div class="stat-label">{}</div>'

# (旧, 新, 出現回数)
R = [
    # ---- hero ----
    ('都心部・通勤圏の8コース。出張や観光の合間にも、朝イチ&午後スルーで1ラウンド。</div>', '都心部・通勤圏の8コース。出張や観光の合間にも、1ラウンド組みやすいエリアです。</div>', 1),
    ('도심·통근권의 8개 코스. 출장·관광의 틈새에도 오전 스루·오후 스루로 1라운드.</div>', '도심·통근권의 8개 코스. 출장·관광의 틈새에도 1라운드 편성하기 좋은 에리어입니다.</div>', 1),
    # ---- stats ----
    (STAT.format("¥5,000", "平日最安"), STAT.format("¥8,423", "じゃらん平日最安（11/1）"), 1),
    (STAT.format("¥3,500", "Lowest weekday"), STAT.format("¥8,423", "Lowest weekday on Jalan (Nov 1)"), 1),
    (STAT.format("¥3,500", "평일 최저"), STAT.format("¥8,423", "자란 평일 최저(11/1)"), 1),
    # ---- reason ----
    ('<div class="reason-title">朝イチ&午後スルー豊富</div>', '<div class="reason-title">出張や旅行の合間に組みやすい</div>', 1),
    ('<div class="reason-desc">都市型エリアだけあって、早朝スループレー・午後スループレーのラインアップが分厚い。出張前後の半日・旅行の合間・ワーケーションの中1日でも1ラウンド組める。</div>',
     '<div class="reason-desc">都心から近いので、出張の前後や旅行の合間にも予定に入れやすいエリアです。ただし2026年11月前半のじゃらんでは、久山・大博多・セブンミリオン・筑紫ヶ丘に午後スルーのプランはありませんでした。プランはプレー日ごとに予約サイトで確認してください。</div>', 1),
    ('<div class="reason-title">Plenty of early/afternoon thrus</div>', '<div class="reason-title">Easy to fit around a trip</div>', 1),
    ('<div class="reason-desc">This is an urban area — so early-morning and afternoon-thru tee times are easy to find. Perfect for squeezing a round between meetings, sightseeing, or a workation rest day.</div>',
     '<div class="reason-desc">These courses are close to the city, so a round fits easily around meetings or sightseeing. In the first half of November 2026, though, Jalan listed no afternoon-thru plans at Hisayama, Dai-Hakata, Seven Million or Chikushigaoka. Check the plans for your date on the booking site.</div>', 1),
    ('<div class="reason-title">이른 아침&amp;오후 스루 풍부</div>', '<div class="reason-title">출장·여행 틈새에 편성하기 좋음</div>', 1),
    ('<div class="reason-desc">도시형 에리어라 조기 스루·오후 스루 플랜이 두텁게 구비. 출장 전후 반일, 여행 틈새, 워케이션 쉬는 날에도 한 라운드 편성 가능.</div>',
     '<div class="reason-desc">도심에서 가까워 출장 전후나 여행 틈새에 일정을 넣기 좋은 에리어입니다. 다만 2026년 11월 전반 자란에서는 히사야마·다이하카타·세븐밀리언·지쿠시가오카에 오후 스루 플랜이 없었습니다. 플랜은 플레이 날짜별로 예약 사이트에서 확인하세요.</div>', 1),
    # ---- セブンミリオン カード ----
    ('高速を使わず市内で完結するアクセスが魅力。手頃な料金でフルラウンドが楽しめる。</div>', '高速を使わず市内で完結するアクセスが魅力。</div>', 1),
    ('고속도로를 쓰지 않고 시내에서 완결되는 접근성이 매력. 합리적인 요금으로 풀 라운드를 즐길 수 있음.</div>', '고속도로를 쓰지 않고 시내에서 완결되는 접근성이 매력.</div>', 1),
    # ---- モデルプラン ----
    ('空港着→午後スループレー→中洲ディナー→', '空港着→午後ラウンド→中洲ディナー→', 1),
    ('Land at FUK, play an afternoon thru, eat at', 'Land at FUK, play in the afternoon, eat at', 1),
    ('공항 도착→오후 스루 플레이→나카스 디너→', '공항 도착→오후 라운드→나카스 디너→', 1),
    ('<strong>油山ゴルフ</strong>or<strong>西戸崎シーサイド</strong>で午後スルー（空港から15-25分）。平日¥3,500〜。',
     '<strong>ララヒルズ油山</strong>or<strong>西戸崎シーサイド</strong>へ（空港から15-25分）。午後の空き枠と料金は楽天GORAで確認。', 1),
    ('Afternoon-thru at <strong>Aburayama</strong> or <strong>Saitozaki Seaside</strong> (15–25 min from FUK). From ¥3,500 weekdays.',
     'Head to <strong>Lala Hills Aburayama</strong> or <strong>Saitozaki Seaside</strong> (15–25 min from FUK). Check afternoon slots and rates on Rakuten GORA.', 1),
    ('<strong>아부라야마 골프</strong>or<strong>사이토자키 시사이드</strong>에서 오후 스루(공항에서 15-25분). 평일 ¥3,500〜.',
     '<strong>라라 힐스 아부라야마</strong>or<strong>사이토자키 시사이드</strong>로 이동(공항에서 15-25분). 오후 빈 시간대와 요금은 라쿠텐 GORA에서 확인.', 1),
    ('名門コースで18Hラウンド。1957年創設の福岡CCは特別感格別。', '名門コースで18Hラウンド。1957年創設の福岡CCは会員制で、ビジターはメンバー同伴または紹介が必須。', 1),
    ('18 holes at a heritage club. The 1957-founded Fukuoka CC has a special feel.', '18 holes at a heritage club. The 1957-founded Fukuoka CC is members-only: visitors must play with a member or have an introduction.', 1),
    ('명문 코스에서 18홀 라운드. 1957년 창설의 후쿠오카CC는 특별감 각별.', '명문 코스에서 18홀 라운드. 1957년 창설의 후쿠오카CC는 회원제로, 비지터는 멤버 동반 또는 소개가 필수.', 1),
    # ---- FAQ 半日 ----
    ('<div class="faq-a">早朝スルー or <strong>午後スルー</strong>プランの活用が定石です。油山ゴルフ（ショート）なら2時間強で完結。西戸崎・福岡CC・久山CC・古賀GCは午後スルー対応日が多く、午前中の商談→空港で着替え→ラウンド→翌朝戻る、のようなスケジュールも現実的です。</div>',
     '<div class="faq-a">いちばん手軽なのはショートコースの<strong>ララヒルズ油山</strong>です。18Hなら<strong>午後スルー</strong>が候補ですが、設定はコースと時期で変わります。2026年11月前半のじゃらんでは久山・大博多・セブンミリオン・筑紫ヶ丘に午後スルーのプランはありませんでした。西戸崎・油山は楽天GORA、古賀は公式サイトで確認してください。</div>', 1),
    ('<div class="faq-a">Yes — early-morning or <strong>afternoon-thru</strong> rounds are the trick. Aburayama (a short course) finishes in about 2 hours. Saitozaki, Fukuoka CC, Hisayama, and Koga all run afternoon-thru slots. Meeting in the morning → change at FUK → play the thru → fly back is a real itinerary.</div>',
     '<div class="faq-a">The easiest option is <strong>Lala Hills Aburayama</strong>, a short course. For 18 holes, an <strong>afternoon-thru</strong> plan is the usual choice, but availability changes by course and season. In the first half of November 2026, Jalan listed none at Hisayama, Dai-Hakata, Seven Million or Chikushigaoka. Check Rakuten GORA for Saitozaki and Aburayama, and the official site for Koga.</div>', 1),
    ('출장 겸 반나절로 플레이하고 싶어요 (오후 스루 추천)</div>', '출장 겸 반나절로 플레이하고 싶어요</div>', 1),
    ('<div class="faq-a">조기 스루 or<strong>오후 스루</strong>플랜 활용이 정석. 아부라야마 골프(쇼트)라면 2시간 조금 넘게 완결. 사이토자키·후쿠오카CC·히사야마CC·고가GC는 오후 스루 대응일이 많아 오전 미팅→공항에서 환복→라운드→다음날 귀경과 같은 스케줄도 현실적입니다.</div>',
     '<div class="faq-a">가장 간편한 곳은 쇼트 코스인 <strong>라라 힐스 아부라야마</strong>입니다. 18홀이라면 <strong>오후 스루</strong>가 후보지만, 설정은 코스와 시기에 따라 다릅니다. 2026년 11월 전반 자란에서는 히사야마·다이하카타·세븐밀리언·지쿠시가오카에 오후 스루 플랜이 없었습니다. 사이토자키·아부라야마는 라쿠텐 GORA, 고가는 공식 사이트에서 확인하세요.</div>', 1),
    # ---- FAQ コスパ ----
    ('<div class="faq-a">平日¥3,500〜の<strong>西戸崎シーサイドCC</strong>が市内最安クラス。¥5,000前後では<strong>油山ゴルフ</strong>（ショート）、¥6,000前後なら<strong>セブンミリオン・大博多・久山・古賀</strong>いずれも十分手頃。料金順なら西戸崎→油山→セブンミリオンの順で検討を。</div>',
     '<div class="faq-a">じゃらんの18H最安（2026年11月1日時点）では、平日は<strong>大博多</strong>¥8,423〜、<strong>久山</strong>¥9,473〜、<strong>セブンミリオン</strong>¥10,600〜、<strong>筑紫ヶ丘</strong>¥13,150〜の順です。西戸崎・油山はじゃらんに無いので楽天GORAで、古賀は公式サイトで料金を確認してください。</div>', 1),
    ('<div class="faq-a"><strong>Saitozaki Seaside CC</strong> from ¥3,500 is the city\'s rock-bottom leader. <strong>Aburayama</strong> around ¥5,000 (short course), then <strong>Seven Million / Dai-Hakata / Hisayama / Koga</strong> all around ¥6,000. Sorted by price: Saitozaki → Aburayama → Seven Million.</div>',
     '<div class="faq-a">On Jalan (lowest 18-hole plans, as of Nov 1, 2026), weekday rates run <strong>Dai-Hakata</strong> ¥8,423, <strong>Hisayama</strong> ¥9,473, <strong>Seven Million</strong> ¥10,600, <strong>Chikushigaoka</strong> ¥13,150. Saitozaki and Aburayama aren\'t on Jalan — check Rakuten GORA. For Koga, check the official site.</div>', 1),
    ('<div class="faq-a">평일 ¥3,500〜의<strong>사이토자키 시사이드CC</strong>가 시내 최저가 클래스. ¥5,000 전후로는<strong>아부라야마 골프</strong>(쇼트), ¥6,000 전후면<strong>세븐밀리언·다이하카타·히사야마·고가</strong>모두 충분히 합리적. 요금순이라면 사이토자키→아부라야마→세븐밀리언 순으로 검토.</div>',
     '<div class="faq-a">자란 18홀 최저가(2026년 11월 1일 기준)로 평일은 <strong>다이하카타</strong> ¥8,423〜, <strong>히사야마</strong> ¥9,473〜, <strong>세븐밀리언</strong> ¥10,600〜, <strong>지쿠시가오카</strong> ¥13,150〜 순입니다. 사이토자키·아부라야마는 자란에 없으니 라쿠텐 GORA에서, 고가는 공식 사이트에서 요금을 확인하세요.</div>', 1),
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
