#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北九州カントリー倶楽部の所在地・規模の誤り (若松区・18H) を、飯塚市鹿毛馬の27ホール (PGM) に直す (2026-11-08)。
根拠: じゃらんゴルフ gc02348 (住所・27ホール・松竹梅・八幡ICから20km以内・新飯塚駅)、会員権サイト plus-web (27H)、PGM のコースページ。
空港からの所要時間は資料が無いため数字を載せず、八幡ICからの距離にする。
あわせて area-kitakyushu の瀬板の森カードの「北九州市営」と、area-chikuho の麻生飯塚カードの「飯塚市」を直す。
エリアの移動 (北九州→筑豊) は掲載コースの集計値に影響するため、ここではしない。
冪等。改行コードはそのまま保つ。
Usage: python scripts/fix_kitakyushu_cc_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
AD = "〒820-1112 福岡県飯塚市鹿毛馬412-6"
DESC_JA = "北九州カントリー倶楽部（飯塚市）の詳細情報。PGM運営の27ホール（松・竹・梅）。九州自動車道の八幡ICから約20km。コースデータ・アクセス・料金を掲載。"
P_JA = "飯塚市鹿毛馬に広がる、松・竹・梅の3コース・27ホール。PGMが運営しています。名前は「北九州」ですが、所在地は筑豊の飯塚市です。梅コース2番は池に浮かぶようなグリーンが名物で、距離感とクラブ選びが攻略の鍵になります（じゃらんのコース紹介より）。"
P_EN = "A 27-hole course with three nines (Matsu, Take and Ume) in Kakema, Iizuka City, operated by PGM. Despite the name, it is in Iizuka in the Chikuho area, not in Kitakyushu City. Ume No. 2, with a green set like an island in a pond, is the signature hole (per Jalan Golf's course description)."
P_KO = "이이즈카시 가케마에 자리한 마쓰·다케·우메 3코스 27홀. PGM이 운영합니다. 이름은 「기타큐슈」지만 소재지는 지쿠호 지역의 이이즈카시입니다. 연못 위에 떠 있는 듯한 그린의 우메 코스 2번 홀이 명물입니다(자란골프 코스 소개 기준)."
LI_JA = "<strong>八幡ICから約20km</strong>九州自動車道の八幡ICから国道200号バイパス経由。福岡市内からは八木山バイパス経由です（じゃらん）。"
LI_EN = "<strong>About 20 km from Yahata IC</strong>From Yahata IC on the Kyushu Expressway via the Route 200 bypass; from Fukuoka City via the Yagiyama Bypass (Jalan Golf)."
LI_KO = "<strong>야하타 IC에서 약 20km</strong>규슈 자동차도 야하타 IC에서 국도 200호 바이패스 경유. 후쿠오카 시내에서는 야기야마 바이패스 경유(자란)."

PLAN = {
 "course-kitakyushu.html": [
   ("北九州カントリークラブ（北九州市若松区）の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約70分。", DESC_JA),
   ('<div class="hero-eyebrow">— 北九州市若松区</div>', '<div class="hero-eyebrow">— 飯塚市</div>'),
   ("Kitakyushu Country Club ｜ 18H<", "Kitakyushu Country Club ｜ 27H<"),
   ("北九州カントリー倶楽部 ｜ 18 Holes", "北九州カントリー倶楽部 ｜ 27 Holes"),
   ("Kitakyushu Country Club ｜ 18홀", "Kitakyushu Country Club ｜ 27홀"),
   ("✈️ 空港から70分", "🛣️ 八幡ICから約20km"), ("✈️ 70 min from airport", "🛣️ ~20 km from Yahata IC"), ("✈️ 공항에서 70분", "🛣️ 야하타 IC에서 약 20km"),
   ("⛳ 18H<", "⛳ 27H<"), ("⛳ 18 holes", "⛳ 27 holes"), ("⛳ 18홀", "⛳ 27홀"),
   ('<div class="stat-num">18<span class="unit">H</span>', '<div class="stat-num">27<span class="unit">H</span>'),
   ('<div class="stat-num">70<span class="unit">min</span></div><div class="stat-label">From Airport</div>', '<div class="stat-num">20<span class="unit">km</span></div><div class="stat-label">From Yahata IC</div>'),
   ('<div class="stat-num">70<span class="unit">분</span></div><div class="stat-label">공항에서</div>', '<div class="stat-num">20<span class="unit">km</span></div><div class="stat-label">야하타 IC에서</div>'),
   ('<div class="airport-banner-title">후쿠오카공항에서 차로 약 70분</div>', '<div class="airport-banner-title">야하타 IC에서 약 20km</div>'),
   ("北九州市若松区に広がるコース。整備の行き届いたフェアウェイと、戦略性のあるレイアウトで、初心者から上級者まで幅広く楽しめます。福岡空港から車で約70分、日帰りでも十分アクセス可能です。", P_JA),
   ("A well-balanced layout in 北九州市若松区, with nicely maintained fairways and a course design suited to all skill levels. About 70 minutes from Fukuoka Airport by car — a perfect day-trip destination.", P_EN),
   ("北九州市若松区에 위치한 균형 잡힌 코스. 잘 정비된 페어웨이와 전략적인 레이아웃으로 초보자부터 상급자까지 모두 즐길 수 있습니다. 후쿠오카공항에서 차로 약 70분로 당일치기 여행에도 최적입니다.", P_KO),
   ("<strong>福岡空港から70分</strong>レンタカーや送迎でスムーズに到着できます。", LI_JA),
   ("<strong>70 min from Fukuoka Airport</strong>Easy by rental car or courtesy bus.", LI_EN),
   ("<strong>후쿠오카공항에서 70분</strong>렌터카나 셔틀로 간편하게 도착합니다.", LI_KO),
   ("車でのご来場を推奨。福岡都市高速・九州自動車道経由。", "車でのご来場を推奨。九州自動車道の八幡ICから約20km、福岡市内からは八木山バイパス経由（じゃらん）。"),
   ("Car is recommended. Via Fukuoka Urban Expressway / Kyushu Expressway.", "Car is recommended. About 20 km from Yahata IC on the Kyushu Expressway; from Fukuoka City via the Yagiyama Bypass (Jalan Golf)."),
   ("자동차 추천. 후쿠오카 도시 고속도로·규슈 고속도로 경유.", "자동차 추천. 규슈 자동차도 야하타 IC에서 약 20km, 후쿠오카 시내에서는 야기야마 바이패스 경유(자란)."),
   ('From Fukuoka Airport</div><div class="access-value">車で約70分', 'From Yahata IC</div><div class="access-value">約20km'),
   ('From Hakata Station</div><div class="access-value">車で約70分', 'From Fukuoka City</div><div class="access-value">八木山バイパス経由'),
   ('Nearest IC</div><div class="access-value">最寄IC', 'Nearest IC</div><div class="access-value">八幡IC'),
   ('From Fukuoka Airport</div><div class="access-value">~70 min by car', 'From Yahata IC</div><div class="access-value">~20 km'),
   ('From Hakata Station</div><div class="access-value">~70 min by car', 'From Fukuoka City</div><div class="access-value">Via Yagiyama Bypass'),
   ('Nearest IC</div><div class="access-value">Nearest IC', 'Nearest IC</div><div class="access-value">Yahata IC'),
   ('후쿠오카공항에서</div><div class="access-value">차로 약 70분', '야하타 IC에서</div><div class="access-value">약 20km'),
   ('하카타역에서</div><div class="access-value">차로 약 70분', '후쿠오카 시내에서</div><div class="access-value">야기야마 바이패스 경유'),
   ('최근 IC</div><div class="access-value">최근 IC', '최근 IC</div><div class="access-value">야하타 IC'),
   ('<div class="contact-value">北九州市若松区</div>', f'<div class="contact-value">{AD}</div>'),
   ('<a href="course-moji.html" class="related-card"><span class="related-card-name">門司GC</span>', '<a href="course-asoiizuka.html" class="related-card"><span class="related-card-name">麻生飯塚GC</span>'),
   ('<a href="course-sevenmillion.html" class="related-card"><span class="related-card-name">セブンミリオンGC</span>', '<a href="course-lakeside.html" class="related-card"><span class="related-card-name">福岡レイクサイドCC</span>'),
   ('<a href="course-moji.html" class="related-card"><span class="related-card-name">Moji GC</span>', '<a href="course-asoiizuka.html" class="related-card"><span class="related-card-name">Aso Iizuka GC</span>'),
   ('<a href="course-sevenmillion.html" class="related-card"><span class="related-card-name">Seven Million GC</span>', '<a href="course-lakeside.html" class="related-card"><span class="related-card-name">Fukuoka Lakeside CC</span>'),
   ('<a href="course-moji.html" class="related-card"><span class="related-card-name">모지 GC</span>', '<a href="course-asoiizuka.html" class="related-card"><span class="related-card-name">아소 이이즈카 GC</span>'),
   ('<a href="course-sevenmillion.html" class="related-card"><span class="related-card-name">세븐밀리언 GC</span>', '<a href="course-lakeside.html" class="related-card"><span class="related-card-name">후쿠오카 레이크사이드 CC</span>'),
 ],
 "access-kitakyushu.html": [
   ("~70 min from Fukuoka Airport by car.", "About 20 km from Yahata IC on the Kyushu Expressway."),
   ("상세 지도를 한국어로 안내합니다. 후쿠오카공항에서 차로 약 70분.", "상세 지도를 한국어로 안내합니다. 규슈 자동차도 야하타 IC에서 약 20km."),
   (f"{AD}　후쿠오카현 기타큐슈시 와카마츠구 오아자에스미", AD),
   ("「北九州カントリー倶楽部 若松区」", "「北九州カントリー倶楽部 飯塚市」"),
   ('"北九州カントリー倶楽部 若松区"', '"北九州カントリー倶楽部 飯塚市"'),
 ],
 "area-kitakyushu.html": [
   ('<div class="course-area">Kitakyushu · Wakamatsu-ku</div>\n          <div class="course-name">北九州カントリー倶楽部</div>', '<div class="course-area">Iizuka City · PGM</div>\n          <div class="course-name">北九州カントリー倶楽部</div>'),
   ('<span class="course-chip">18H</span>\n            <span class="course-chip">若松区</span>\n            <span class="course-chip">響灘エリア</span>', '<span class="course-chip">27H</span>\n            <span class="course-chip">飯塚市</span>\n            <span class="course-chip">松・竹・梅</span>'),
   ("若松区・響灘近くに位置する自然豊かなコース。北九州都市高速・若松IC/響灘ICからアクセス良好で、地元ゴルファーに長く愛される一面も。", "名前は「北九州」ですが、所在地は筑豊の飯塚市鹿毛馬。PGM運営の27ホール（松・竹・梅）で、九州自動車道の八幡ICから約20kmです（じゃらん）。"),
   ('<span class="course-chip">18H</span>\n            <span class="course-chip">Wakamatsu Ward</span>\n            <span class="course-chip">Hibikinada coast</span>', '<span class="course-chip">27H</span>\n            <span class="course-chip">Iizuka City</span>\n            <span class="course-chip">Three nines</span>'),
   ("Set in Wakamatsu-ku near the Hibikinada coast. Easy access from either Wakamatsu IC or Hibikino IC — a long-time favorite of locals.", "Despite the name, it is in Iizuka City (Chikuho area), not Kitakyushu. A 27-hole PGM course about 20 km from Yahata IC on the Kyushu Expressway (Jalan Golf)."),
   ('<div class="course-area">Kitakyushu · Wakamatsu-ku</div>\n          <div class="course-name">기타큐슈 컨트리 클럽</div>', '<div class="course-area">Iizuka City · PGM</div>\n          <div class="course-name">기타큐슈 컨트리 클럽</div>'),
   ('<span class="course-chip">18홀</span>\n            <span class="course-chip">와카마츠구</span>\n            <span class="course-chip">히비키나다 해안</span>', '<span class="course-chip">27홀</span>\n            <span class="course-chip">이이즈카시</span>\n            <span class="course-chip">3코스</span>'),
   ("와카마츠구・히비키나다 근처의 자연 친화적인 코스. 기타큐슈 도시 고속도로 와카마츠 IC/히비키노 IC에서 접근성이 좋고 지역 골퍼에게 오래 사랑받는 코스.", "이름은 「기타큐슈」지만 소재지는 지쿠호 지역의 이이즈카시. PGM이 운영하는 27홀로, 규슈 자동차도 야하타 IC에서 약 20km입니다(자란)."),
   ('<span class="course-chip">北九州市営</span>', '<span class="course-chip">PGM運営</span>'),
   ("北九州市営のパブリックコース。", "PGM運営のパブリックコース。"),
   ('<span class="course-chip">Municipal</span>', '<span class="course-chip">PGM</span>'),
   ("A municipal public course run by Kitakyushu City.", "A public course operated by PGM."),
   ('<span class="course-chip">기타큐슈 시영</span>', '<span class="course-chip">PGM 운영</span>'),
   ("기타큐슈 시영 퍼블릭 코스.", "PGM이 운영하는 퍼블릭 코스."),
 ],
 "book-fukuoka-tomorrow.html": [('<a href="course-kitakyushu.html">北九州CC</a></div><div class="cmp-area">北九州市若松区</div>', '<a href="course-kitakyushu.html">北九州CC</a></div><div class="cmp-area">飯塚市</div>')],
 "book-fukuoka-cheap.html": [('<a href="course-kitakyushu.html">北九州カントリー倶楽部</a></div><div class="cmp-area">北九州市若松区</div>', '<a href="course-kitakyushu.html">北九州カントリー倶楽部</a></div><div class="cmp-area">飯塚市</div>')],
 "sitemap-guide.html": [
   ('北九州カントリー倶楽部<span>北九州市 / 18H</span>', '北九州カントリー倶楽部<span>飯塚市 / 27H</span>'),
   ('Kitakyushu CC<span>Kitakyushu / 18 holes</span>', 'Kitakyushu CC<span>Iizuka / 27 holes</span>'),
   ('기타큐슈 CC<span>기타큐슈시 / 18홀</span>', '기타큐슈 CC<span>이이즈카시 / 27홀</span>'),
 ],
 "access.html": [
   ('北九州カントリー倶楽部<small>北九州市若松区</small>', '北九州カントリー倶楽部<small>飯塚市</small>'),
   ('Kitakyushu Country Club<small>Kitakyushu (Wakamatsu)</small>', 'Kitakyushu Country Club<small>Iizuka City</small>'),
   ('기타큐슈 컨트리 클럽<small>기타큐슈시 와카마쓰구</small>', '기타큐슈 컨트리 클럽<small>이이즈카시</small>'),
 ],
 "area-chikuho.html": [
   ("飯塚市の歴史ある林間名門コース。", "嘉穂郡桂川町の歴史ある林間名門コース。"),
   ("A historic forest course in Iizuka tied", "A historic forest course in Keisen Town (Kaho District) tied"),
   ('<span class="course-chip earth">Iizuka</span>', '<span class="course-chip earth">Keisen Town</span>'),
   ('<span class="course-chip earth">이이즈카시</span>', '<span class="course-chip earth">가호군 게이센마치</span>'),
   ("이이즈카시의 역사 있는 숲 명문 코스.", "가호군 게이센마치의 역사 있는 숲 명문 코스."),
   ('<div class="course-area">Iizuka City · Historic Forest</div>', '<div class="course-area">Keisen Town · Historic Forest</div>'),
 ],
}
for root in ROOTS:
    print(root)
    for name, pairs in PLAN.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        new = s
        miss = []
        for a, b in pairs:
            a2, b2 = a.replace("\n", nl), b.replace("\n", nl)
            if a2 not in new and b2 not in new:
                miss.append(a[:50])
            new = new.replace(a2, b2)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {name}: {'変更あり' if new != s else 'already'} 未一致={miss}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
