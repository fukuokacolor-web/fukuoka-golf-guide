#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福岡センチュリーGCの道順・所要時間・ホール数を公式 (fcgc.biz/access/・/course/) に合わせる (2026-11-08)。
  - 道順: 粕屋方面・JR篠栗線 → 大分自動車道 甘木IC/朝倉ICから約10分、甘木鉄道 甘木駅・西鉄甘木駅から約10分
  - 所要時間: 空港55分・博多50〜55分 → 公式「JR博多駅・福岡空港より約40分」
  - ホール数: 27ホール・3つの9ホール → 公式「日本初の20ホールスタイル」、筑紫野・朝倉の2コース
冪等。改行コードはそのまま保つ。
Usage: python scripts/fix_century_access_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
JA_P = "朝倉市の丘陵に広がる倶楽部。公式は「日本初の20ホールスタイル」をうたい、筑紫野コースと朝倉コースという異なる2タイプのコースで構成されています。"
EN_P = "A club set in the hills of Asakura City. The club describes itself as Japan's first 20-hole-style layout, with two contrasting courses: Chikushino and Asakura."
KO_P = "아사쿠라시 구릉지에 자리한 클럽. 공식 사이트는 「일본 최초의 20홀 스타일」로 소개하며, 지쿠시노 코스와 아사쿠라 코스라는 두 가지 타입의 코스로 구성됩니다."
PLAN = {
    "course-century.html": [
        ("27ホールの大型コース、", "20ホールスタイルの2コース、"),
        ("福岡空港から約55分。", "福岡空港から約40分。"),
        ("— 27 holes of championship layout ~55 min from Fukuoka Airport.", "— a 20-hole-style club with two courses, ~40 min from Fukuoka Airport."),
        ("— 27홀 대형 코스, 후쿠오카공항에서 차로 약 55분.", "— 20홀 스타일 2개 코스, 후쿠오카공항에서 차로 약 40분."),
        ("— 27ホール。", "— 20ホールスタイルの2コース。"),
        ("27ホールの大型コース。", "20ホールスタイルの2コース。"),
        ("✈️ 空港から55分", "✈️ 空港から40分"), ("✈️ 55 min from airport", "✈️ 40 min from airport"), ("✈️ 공항에서 55분", "✈️ 공항에서 40분"),
        ("⛳ 27ホール", "⛳ 20ホールスタイル"), ("⛳ 27 holes", "⛳ 20-hole style"), ("⛳ 27홀", "⛳ 20홀 스타일"),
        ("27<span class=\"unit\">H</span>", "20<span class=\"unit\">H</span>"),
        ("55<span class=\"unit\">min</span>", "40<span class=\"unit\">min</span>"), ("55<span class=\"unit\">분</span>", "40<span class=\"unit\">분</span>"),
        ("Fukuoka Century Golf Club ｜ 27홀 대형 코스", "Fukuoka Century Golf Club ｜ 20홀 스타일 2개 코스"),
        ("27ホール、<br>3つの表情。", "20ホール、<br>2つのコース。"),
        ("27 holes,<br>three characters.", "20 holes,<br>two courses."),
        ("27홀,<br>세 가지 표정.", "20홀,<br>두 개의 코스."),
        ("福岡市近郊の丘陵地帯に広がる大型倶楽部。3つの9ホール構成で、同じコースでも組み合わせ次第で表情が変わります。整備の行き届いたフェアウェイと、戦略性のあるレイアウトが、リピーターから長く愛される理由です。", JA_P),
        ("A large championship club set in the wooded hills just outside Fukuoka City. Three distinct nines can be combined into different 18-hole rounds, giving the course a different personality each visit.", EN_P),
        ("후쿠오카시 근교 구릉 지대에 자리잡은 대형 클럽. 3개의 9홀 코스를 조합해 매번 다른 라운드를 즐길 수 있습니다. 잘 정비된 페어웨이와 전략적인 레이아웃이 많은 골퍼에게 사랑받는 이유입니다.", KO_P),
        ("福岡空港から車で約55分。レンタカーや送迎でスムーズに到着できます。", "福岡空港・博多駅から車で約40分（公式）。大分自動車道の甘木IC・朝倉ICから約10分です。"),
        ("About 55 minutes by car. Rental cars or courtesy buses recommended.", "About 40 minutes by car from Fukuoka Airport or Hakata Station (per the club), about 10 minutes from Amagi IC or Asakura IC on the Oita Expressway."),
        ("후쿠오카공항에서 차로 약 55분. 렌터카나 셔틀로 편하게 도착할 수 있습니다.", "후쿠오카공항·하카타역에서 차로 약 40분(공식). 오이타 자동차도 아마기 IC·아사쿠라 IC에서 약 10분입니다."),
        ("福岡都市高速・九州自動車道経由で約55分。", "九州自動車道・大分自動車道経由で約40分。"),
        ("About 55 min via Fukuoka Urban Expressway / Kyushu Expressway.", "About 40 min via the Kyushu and Oita Expressways."),
        ("후쿠오카 도시 고속도로·규슈 고속도로 경유 약 55분.", "규슈 자동차도·오이타 자동차도 경유 약 40분."),
        ('<div class="access-value">車で約55分</div>', '<div class="access-value">車で約40分</div>'),
        ('<div class="access-value">車で約50分</div>', '<div class="access-value">車で約40分</div>'),
        ('<div class="access-value">朝倉IC</div>', '<div class="access-value">甘木IC・朝倉IC</div>'),
        ("~55 min by car", "~40 min by car"), ("~50 min by car", "~40 min by car"),
        ('<div class="access-value">Asakura IC</div>', '<div class="access-value">Amagi IC / Asakura IC</div>'),
        ("후쿠오카공항에서 차로 약 55분", "후쿠오카공항에서 차로 약 40분"),
        ('<div class="access-value">차로 약 55분</div>', '<div class="access-value">차로 약 40분</div>'),
        ('<div class="access-value">차로 약 50분</div>', '<div class="access-value">차로 약 40분</div>'),
        ('<div class="access-value">아사쿠라 IC</div>', '<div class="access-value">아마기 IC·아사쿠라 IC</div>'),
    ],
    "access-century.html": [
        ("~55 min from Fukuoka Airport by car.", "~40 min from Fukuoka Airport by car."),
        ("福岡空港から車で約55分。最新の", "福岡空港・博多駅から車で約40分（公式）。最新の"),
        ("<li>福岡空港から福岡都市高速または九州自動車道へ</li>", "<li>福岡空港から九州自動車道へ入り、鳥栖JCTで大分自動車道へ</li>"),
        ("<li>糟屋・粕屋方面のICで降りる</li>", "<li>甘木IC または 朝倉ICで降りる</li>"),
        ("<li>ICから一般道を経由してクラブハウス着</li>", "<li>ICから一般道で約10分</li>"),
        ("<li>合計：福岡空港から車で約55分</li>", "<li>合計：福岡空港から車で約40分（公式）</li>"),
        ('<span class="title">都市高速・九州自動車道利用</span>', '<span class="title">九州自動車道・大分自動車道利用</span>'),
        ("<li>博多・天神から福岡都市高速または九州自動車道へ</li>", "<li>博多・天神から福岡都市高速を経由して九州自動車道へ</li>"),
        ("<li>糟屋・粕屋方面へ進む</li>", "<li>鳥栖JCTで大分自動車道へ進み、甘木IC または 朝倉ICで降りる</li>"),
        ("<li>博多駅からは車で約50〜55分</li>", "<li>博多駅からは車で約40分（公式）</li>"),
        ("JR篠栗線「長者原駅」または「須恵中央駅」が最寄り駅です。駅からはタクシーをご利用ください。", "甘木鉄道「甘木駅」または西鉄甘木線「西鉄甘木駅」から車で約10分です（公式）。駅からはタクシーをご利用ください。"),
        ("Approx. 55 min from Fukuoka Airport by car.", "Approx. 40 min from Fukuoka Airport or Hakata Station by car (per the club)."),
        ("<li>Take the Fukuoka Urban Expressway or Kyushu Expressway from the airport</li>", "<li>From the airport, take the Kyushu Expressway and switch to the Oita Expressway at Tosu JCT</li>"),
        ("<li>Exit at the nearest IC toward Kasuya / Kasuya-machi</li>", "<li>Exit at Amagi IC or Asakura IC</li>"),
        ("<li>Follow local roads to the clubhouse</li>", "<li>About 10 min on local roads to the clubhouse</li>"),
        ("<li>Total: approx. 55 min from Fukuoka Airport</li>", "<li>Total: approx. 40 min from Fukuoka Airport (per the club)</li>"),
        ('<span class="title">Via Urban Expressway / Kyushu Expressway</span>', '<span class="title">Via Kyushu Expressway / Oita Expressway</span>'),
        ("<li>Take the Fukuoka Urban Expressway or Kyushu Expressway from Hakata / Tenjin</li>", "<li>From Hakata / Tenjin, take the Fukuoka Urban Expressway to the Kyushu Expressway</li>"),
        ("<li>Head toward Kasuya / Kasuya-machi area</li>", "<li>Switch to the Oita Expressway at Tosu JCT and exit at Amagi IC or Asakura IC</li>"),
        ("<li>Approx. 50–55 min from Hakata Station</li>", "<li>Approx. 40 min from Hakata Station (per the club)</li>"),
        ('Nearest stations: JR Sasaguri Line "Choshahara" or "Suekita-chuo." Take a taxi from the station.', 'About 10 min by car from Amagi Station (Amagi Railway) or Nishitetsu Amagi Station (Nishitetsu Amagi Line), per the club. Take a taxi from the station.'),
        ("후쿠오카공항에서 차로 약 55분.", "후쿠오카공항·하카타역에서 차로 약 40분(공식)."),
        ("후쿠오카 공항에서 차로 약 55분.", "후쿠오카공항·하카타역에서 차로 약 40분(공식)."),
        ("<li>후쿠오카 도시 고속도로 또는 규슈 자동차도로 진입</li>", "<li>공항에서 규슈 자동차도로 진입 후 도스 JCT에서 오이타 자동차도로</li>"),
        ("<li>카스야·카스야마치 방면 IC에서 하차</li>", "<li>아마기 IC 또는 아사쿠라 IC에서 하차</li>"),
        ("<li>일반 도로를 경유하여 클럽하우스 도착</li>", "<li>일반 도로로 약 10분</li>"),
        ("<li>합계: 후쿠오카 공항에서 차로 약 55분</li>", "<li>합계: 후쿠오카공항에서 차로 약 40분(공식)</li>"),
        ('<span class="title">도시 고속도로·규슈 자동차도로 이용</span>', '<span class="title">규슈 자동차도·오이타 자동차도 이용</span>'),
        ("<li>하카타·텐진에서 후쿠오카 도시 고속도로 또는 규슈 자동차도로 진입</li>", "<li>하카타·텐진에서 후쿠오카 도시고속도로를 거쳐 규슈 자동차도로 진입</li>"),
        ("<li>카스야·카스야마치 방면으로 진행</li>", "<li>도스 JCT에서 오이타 자동차도로 진행, 아마기 IC 또는 아사쿠라 IC에서 하차</li>"),
        ("<li>하카타역에서 약 50〜55분</li>", "<li>하카타역에서 약 40분(공식)</li>"),
        ("JR 사사구리선 「조샤하라역」 또는 「스에키타추오역」에서 택시 이용.", "아마기 철도 「아마기역」 또는 니시테츠 아마기선 「니시테츠 아마기역」에서 차로 약 10분(공식). 역에서 택시를 이용하세요."),
    ],
    "course-quiz.html": [('"n": "福岡センチュリーゴルフ倶楽部", "a": "chikugo", "h": "27ホール"', '"n": "福岡センチュリーゴルフ倶楽部", "a": "chikugo", "h": "20ホール"')],
}
for root in ROOTS:
    print(root)
    for name, pairs in PLAN.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        new = s
        miss = []
        for a, b in pairs:
            n = new.count(a)
            if n == 0 and b not in new:
                miss.append(a[:40])
            new = new.replace(a, b)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        left = [w for w in ("55分", "55 min", "55분", "27ホール", "27 holes", "27홀", "粕屋", "Kasuya", "카스야", "長者原", "Sasaguri", "사사구리") if w in re.sub(r"<style\b.*?</style>", "", new, flags=re.S)]
        print(f"  {name}: {'replaced' if new != s else 'already'} 未一致={miss} 残り={left}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
