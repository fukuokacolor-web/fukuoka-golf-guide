#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アクセスページの「存在しない IC・駅名」と明らかな路線誤りを訂正する (2026-11-08)。
  - 博多IC (九州道にも都市高速にも無い) → 都市高速経由で 太宰府IC / 福岡IC
  - 福岡空港IC (無い) → 都市高速経由
  - 飯塚IC (無い・レイクサイド) → 八木山バイパス 穂波西IC (じゃらん)
  - 都市高速2号線で福岡IC (2号線は太宰府線) → 福岡都市高速経由
  - 天神北ICまたは福岡IC → 西九州道 (福岡IC は無関係) → 都市高速 (天神北ランプなど)
  - 大博多 須恵駅/宇美駅 → 博多南駅 タクシー約25分 (じゃらん)・野多目の読み のだめ→のため
  - 若宮 「若宮駅」(無い) → 赤間駅 タクシー約20分 (じゃらん)
  - ムーンレイク 「赤間関駅」(JR筑豊本線) → JR鹿児島本線「赤間駅」(じゃらん)・鞍手ICから約9分 (公式)
  - セントラル 太宰府IC経由 → 筑紫野ICから約15km (公式)・駅を公式の 筑紫駅/朝倉街道駅 に
  - クラシック 九州道の方向 鳥栖方面→北九州方面
  - 福岡国際 「60〜70km」削除
所要時間の合計は根拠が無い限り触らない。冪等。改行コードはそのまま。
Usage: python scripts/fix_route_names_2026_11.py [--apply]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv

DZ_JA = "福岡都市高速を経由し、太宰府ICから九州自動車道"
DZ_EN = "Take the Fukuoka Urban Expressway to Dazaifu IC, then the Kyushu Expressway"
DZ_KO = "후쿠오카 도시고속도로를 경유해 다자이후 IC에서 규슈 자동차도로"
FK_JA = "福岡都市高速を経由し、福岡ICから九州自動車道"
FK_EN = "Take the Fukuoka Urban Expressway to Fukuoka IC, then the Kyushu Expressway"
FK_KO = "후쿠오카 도시고속도로를 경유해 후쿠오카 IC에서 규슈 자동차도로"

SOUTH = [
    ("博多ICから九州自動車道（鳥栖・熊本方面）へ", f"{DZ_JA}（鳥栖・熊本方面）へ"),
    ("博多ICから九州自動車道（鳥栖方面）へ", f"{DZ_JA}（鳥栖方面）へ"),
    ("Take the Kyushu Expressway from Hakata IC toward Tosu / Kumamoto", f"{DZ_EN} toward Tosu / Kumamoto"),
    ("Take the Kyushu Expressway from Hakata IC toward Tosu", f"{DZ_EN} toward Tosu"),
    ("하카타 IC에서 규슈 자동차도로 (도스·구마모토 방면) 진입", f"{DZ_KO} (도스·구마모토 방면) 진입"),
    ("하카타 IC에서 규슈 자동차도로 (도스 방면) 진입", f"{DZ_KO} (도스 방면) 진입"),
]
NORTH = [
    ("博多ICから九州自動車道（北九州方面）へ", f"{FK_JA}（北九州方面）へ"),
    ("Take the Kyushu Expressway from Hakata IC toward Kitakyushu", f"{FK_EN} toward Kitakyushu"),
    ("하카타 IC에서 규슈 자동차도로 (기타큐슈 방면) 진입", f"{FK_KO} (기타큐슈 방면) 진입"),
]
ROUTE2 = [
    ("福岡空港から都市高速2号線で福岡IC方面へ", "福岡空港から福岡都市高速を経由して福岡IC方面へ"),
    ("Take Urban Expressway Route 2 toward Fukuoka IC", "Take the Fukuoka Urban Expressway toward Fukuoka IC"),
    ("후쿠오카 공항에서 도시고속 2호선으로 후쿠오카 IC 방면", "후쿠오카 공항에서 후쿠오카 도시고속도로를 경유해 후쿠오카 IC 방면"),
]
NISHIKYU = [
    ("天神北ICまたは福岡ICから西九州自動車道へ", "福岡都市高速（天神北ランプなど）から西九州自動車道へ"),
    ("Take the Nishi-Kyushu Expressway from Tenjin-Kita IC or Fukuoka IC", "Take the Fukuoka Urban Expressway (e.g. from Tenjin-kita ramp) onto the Nishi-Kyushu Expressway"),
    ("텐진키타 IC 또는 후쿠오카 IC에서 니시규슈 자동차도로 진입", "후쿠오카 도시고속도로 (텐진키타 램프 등)에서 니시규슈 자동차도로 진입"),
]
AIRPORT_IC = [
    ("福岡空港ICから九州自動車道に乗る", "福岡空港から福岡都市高速を経由して九州自動車道へ"),
    ("Enter Kyushu Expressway from Fukuoka Airport IC", "Take the Fukuoka Urban Expressway to the Kyushu Expressway"),
    ("Enter the Kyushu Expressway from Fukuoka Airport IC", "Take the Fukuoka Urban Expressway to the Kyushu Expressway"),
    ("후쿠오카 공항 IC에서 규슈 고속도로 진입", "후쿠오카 도시고속도로를 경유해 규슈 고속도로 진입"),
]

PLAN = {
    "access-ariake.html": SOUTH,
    "access-chikushino.html": SOUTH,
    "access-kurume.html": SOUTH,
    "access-ogori.html": SOUTH,
    "access-classic.html": [
        ("博多ICから九州自動車道（鳥栖方面）へ", f"{FK_JA}（北九州方面）へ"),
        ("Take the Kyushu Expressway from Hakata IC toward Tosu", f"{FK_EN} toward Kitakyushu"),
        ("하카타 IC에서 규슈 자동차도로 (도스 방면) 진입", f"{FK_KO} (기타큐슈 방면) 진입"),
    ],
    "access-wakamiya.html": NORTH + [
        ("JR筑豊本線「若宮駅」が最寄り駅です。駅からタクシーをご利用ください（約15〜20分）。",
         "JR鹿児島本線「赤間駅」からタクシーで約20分です（じゃらん）。"),
        ('Nearest station: JR Chikuho Main Line "Wakamiya Station." Take a taxi from the station (approx. 15–20 min).',
         'From JR Kagoshima Main Line "Akama Station" it is about 20 min by taxi (Jalan Golf).'),
        ("가장 가까운 역은 JR 치쿠호 본선 「와카미야역」입니다. 역에서 택시 이용 (약 15〜20분).",
         "JR 가고시마 본선 「아카마역」에서 택시로 약 20분 (자란 골프)."),
    ],
    "access-koga.html": [
        ("博多IC（または千鳥橋JCT）から九州自動車道へ", f"{FK_JA}（北九州方面）へ"),
        ("Take the Kyushu Expressway from Hakata IC", f"{FK_EN} toward Kitakyushu"),
        ("하카타 IC에서 규슈 자동차도로 진입", f"{FK_KO} (기타큐슈 방면) 진입"),
    ],
    "access-dazaifu.html": [
        ("博多ICまたは太宰府ICから九州自動車道を利用", "福岡都市高速2号線（太宰府線）で九州自動車道・太宰府ICへ"),
        ("Take the Kyushu Expressway from Hakata IC or Dazaifu IC", "Take Fukuoka Urban Expressway Route 2 (Dazaifu Line) to Dazaifu IC on the Kyushu Expressway"),
        ("규슈 자동차도로 하카타 IC 또는 다자이후 IC 진입", "후쿠오카 도시고속도로 2호선 (다자이후선)으로 규슈 자동차도로 다자이후 IC 방면"),
    ],
    "access-fukuokakokusai.html": ROUTE2 + [
        ("合計：福岡空港から車で約45〜60分（60〜70km）", "合計：福岡空港から車で約45〜60分"),
        ("합계: 후쿠오카 공항에서 차로 약 45〜60분 (60〜70km)", "합계: 후쿠오카 공항에서 차로 약 45〜60분"),
    ],
    "access-genkai.html": ROUTE2,
    "access-pheasant.html": ROUTE2,
    "access-takaha.html": ROUTE2,
    "access-wakamatsu.html": ROUTE2,
    "access-keya.html": NISHIKYU,
    "access-queenshill.html": NISHIKYU,
    "access-shimaseaside.html": NISHIKYU,
    "access-kyushugc.html": AIRPORT_IC,
    "access-central.html": AIRPORT_IC + [
        ("<li>太宰府ICで降りる（約15分）</li>", "<li>筑紫野ICで降りる</li>"),
        ("<li>一般道で筑紫野市方面へ　約15〜20分</li>", "<li>国道386号を日田・甘木方面へ進み、山家道交差点を飯塚方面へ左折（筑紫野ICから約15km・公式）</li>"),
        ("<li>Exit at Dazaifu IC (approx. 15 min)</li>", "<li>Exit at Chikushino IC</li>"),
        ("<li>Continue on local roads toward Chikushino City — approx. 15–20 min</li>",
         "<li>Take Route 386 toward Hita / Amagi and turn left toward Iizuka at the Yamaemichi intersection (about 15 km from Chikushino IC, per the club)</li>"),
        ("<li>다자이후 IC에서 하차（약 15분）</li>", "<li>지쿠시노 IC에서 하차</li>"),
        ("<li>일반 도로로 지쿠시노시 방면 약 15〜20분</li>", "<li>국도 386호선을 히타·아마기 방면으로 진행, 야마에미치 교차로에서 이즈카 방면 좌회전 (지쿠시노 IC에서 약 15km·공식)</li>"),
        ("最寄り駅は西鉄天神大牟田線「筑紫駅」または「二日市駅」です。駅からゴルフ場まで直通バスはないためタクシーをご利用ください（約15〜20分）。",
         "最寄り駅は西鉄天神大牟田線「筑紫駅」（タクシー約15分）または「朝倉街道駅」（タクシー約20分）です（公式）。"),
        ('The nearest stations are Nishitetsu "Chikushi Station" or "Futsukaichi Station". There is no direct bus — take a taxi (approx. 15–20 min).',
         'The nearest stations are Nishitetsu "Chikushi Station" (about 15 min by taxi) or "Asakura-gaido Station" (about 20 min by taxi), per the club.'),
        ("가장 가까운 역은 니시테쓰 「지쿠시역」또는 「후쓰카이치역」입니다. 역에서 골프장까지 직통 버스가 없으므로 택시를 이용하세요（약 15〜20분）.",
         "가장 가까운 역은 니시테쓰 「지쿠시역」(택시 약 15분) 또는 「아사쿠라가이도역」(택시 약 20분)입니다 (공식)."),
    ],
    "access-moonlake.html": [
        ("最寄り駅はJR筑豊本線「赤間関駅」です。駅からゴルフ場まで直通バスはないためタクシーをご利用ください（約25分）。",
         "最寄り駅はJR鹿児島本線「赤間駅」です（じゃらん）。駅からゴルフ場まで直通バスはないためタクシーをご利用ください。"),
        ('The nearest station is JR Chikuho Main Line "Akamageki Station". There is no direct bus — take a taxi (approx. 25 min).',
         'The nearest station is JR Kagoshima Main Line "Akama Station" (Jalan Golf). There is no direct bus — take a taxi.'),
        ("가장 가까운 역은 JR 치쿠호 본선 「아카마가세키역」입니다. 역에서 골프장까지 직통 버스가 없으므로 택시를 이용하세요（약 25분）.",
         "가장 가까운 역은 JR 가고시마 본선 「아카마역」입니다 (자란 골프). 역에서 골프장까지 직통 버스가 없으므로 택시를 이용하세요."),
        ("<li>鞍手ICで降りる</li>", "<li>鞍手ICで降りる（ICから約9分・公式）</li>"),
        ("<li>Exit at Kurate IC</li>", "<li>Exit at Kurate IC (about 9 min from the IC, per the club)</li>"),
    ],
    "access-daihakata.html": [
        ("野多目IC（のだめIC）", "野多目IC（のためIC）"),
        ("toward Nodame", "toward Notame"),
        ("Nodame IC", "Notame IC"),
        ("노다메", "노타메"),
        ("JR鹿児島本線「須恵駅」または「宇美駅」（JR香椎線）が比較的近い駅です。駅からゴルフ場まで直通バスはないためタクシーをご利用ください。",
         "最寄り駅はJR博多南線「博多南駅」で、駅からタクシーで約25分です（じゃらん）。"),
        ('The nearest stations are JR Kagoshima Main Line "Sue Station" or JR Kashii Line "Umi Station." No direct bus service — take a taxi to the course.',
         'The nearest station is JR "Hakata-Minami Station"; the course is about 25 min by taxi from there (Jalan Golf).'),
        ("가장 가까운 역은 JR 가고시마 본선 「스에역」 또는 JR 카시이선 「우미역」입니다. 직통 버스가 없으므로 택시를 이용하세요.",
         "가장 가까운 역은 JR 「하카타미나미역」이며, 역에서 택시로 약 25분입니다 (자란 골프)."),
    ],
    "access-lakeside.html": [
        ("九州道・飯塚ICから約10分。", "八木山バイパス・穂波西ICから約5分（じゃらん）。"),
        ("九州道・飯塚ICから車で約10分。福岡空港から約40分。", "八木山バイパス・穂波西ICから約5分（じゃらん）。博多駅・福岡空港から約40分（公式）。"),
        ("<li>福岡空港から九州自動車道（鳥栖・熊本方面）へ</li>", "<li>福岡空港から国道201号線を飯塚方面へ</li>"),
        ("<li>飯塚ICで降りる（約30分）</li>", "<li>八木山バイパス（有料）に入り、2つ目の穂波西ICで降りる</li>"),
        ("<li>飯塚ICから一般道を経由して約10分でクラブハウス着</li>", "<li>穂波西ICから約5分でクラブハウス着（じゃらん）</li>"),
        ("<li>合計：福岡空港から車で約40分</li>", "<li>合計：福岡空港から車で約40分（公式）</li>"),
        ('<span class="title">九州自動車道利用</span>', '<span class="title">北九州方面から</span>'),
        ("<li>博多ICから九州自動車道（鳥栖・熊本方面）へ</li>", "<li>九州自動車道・八幡IC（または北九州都市高速・馬場山出口）から国道200号線を飯塚方面へ</li>"),
        ("<li>飯塚ICで降りる（博多から約25〜30分）</li>", "<li>太郎丸一区交差点を右折</li>"),
        ("<li>飯塚ICから約10分でクラブハウス着</li>", "<li>交差点から約5分でクラブハウス着（じゃらん）</li>"),
        ("<li>博多駅からは車で約35〜40分</li>", "<li></li>"),
        ('JR篠栗線「飯塚駅」が最寄りの主要駅です。', 'JR筑豊本線（福北ゆたか線）「飯塚駅」が最寄りの主要駅です。'),
        # EN
        ("About 10 min from Iizuka IC on the Kyushu Expressway. Approx. 40 min from Fukuoka Airport.",
         "About 5 min from Honami-nishi IC on the Yagiyama Bypass (Jalan Golf). Approx. 40 min from Hakata Station or Fukuoka Airport (per the club)."),
        ("<li>Take the Kyushu Expressway toward Tosu / Kumamoto</li>", "<li>Take Route 201 toward Iizuka</li>"),
        ("<li>Exit at Iizuka IC (approx. 30 min)</li>", "<li>Enter the Yagiyama Bypass (toll) and exit at Honami-nishi IC, the second exit</li>"),
        ("<li>Approx. 10 min from the IC to the clubhouse</li>", "<li>About 5 min from the IC to the clubhouse (Jalan Golf)</li>"),
        ('<span class="title">Via Kyushu Expressway</span>', '<span class="title">From Kitakyushu</span>'),
        ("<li>Take the Kyushu Expressway from Hakata IC toward Tosu / Kumamoto</li>", "<li>From Yahata IC on the Kyushu Expressway (or Babayama exit on the Kitakyushu Urban Expressway), take Route 200 toward Iizuka</li>"),
        ("<li>Exit at Iizuka IC (approx. 25–30 min from Hakata)</li>", "<li>Turn right at the Taromaru 1-ku intersection</li>"),
        ("<li>Approx. 35–40 min from Hakata Station</li>", "<li>About 5 min from the intersection to the clubhouse (Jalan Golf)</li>"),
        ('JR Sasaguri Line "Iizuka Station."', 'JR Chikuho Main Line "Iizuka Station."'),
        # KO
        ("규슈 자동차도로 이이즈카 IC에서 약 10분. 후쿠오카 공항에서 약 40분.",
         "야기야마 바이패스 호나미니시 IC에서 약 5분 (자란 골프). 하카타역·후쿠오카 공항에서 약 40분 (공식)."),
        ("<li>규슈 자동차도로 (도스·구마모토 방면) 진입</li>", "<li>국도 201호선을 이이즈카 방면으로</li>"),
        ("<li>이이즈카 IC에서 하차 (약 30분)</li>", "<li>야기야마 바이패스 (유료) 진입, 두 번째 호나미니시 IC에서 하차</li>"),
        ("<li>이이즈카 IC에서 일반 도로로 약 10분으로 클럽하우스 도착</li>", "<li>호나미니시 IC에서 약 5분이면 클럽하우스 도착 (자란 골프)</li>"),
        ('<span class="title">규슈 자동차도로 이용</span>', '<span class="title">기타큐슈 방면에서</span>'),
        ("<li>하카타 IC에서 규슈 자동차도로 (도스·구마모토 방면) 진입</li>", "<li>규슈 자동차도로 야하타 IC (또는 기타큐슈 도시고속 바바야마 출구)에서 국도 200호선을 이이즈카 방면으로</li>"),
        ("<li>이이즈카 IC에서 하차 (하카타에서 약 25〜30분)</li>", "<li>다로마루 1구 교차로에서 우회전</li>"),
        ("<li>이이즈카 IC에서 약 10분으로 클럽하우스 도착</li>", "<li>교차로에서 약 5분이면 클럽하우스 도착 (자란 골프)</li>"),
        ("<li>하카타역에서 약 35〜40분</li>", "<li></li>"),
        ("JR 사사구리선 「이이즈카역」", "JR 지쿠호 본선 「이이즈카역」"),
    ],
    "area-chikuho.html": [
        ("<li>麻生飯塚CC <strong>55分</strong>（飯塚IC）</li>", "<li>麻生飯塚CC <strong>55分</strong>（福岡IC）</li>"),
        ("<li>あかねCC <strong>60分</strong>（飯塚IC）</li>", "<li>あかねCC <strong>60分</strong>（筑穂IC）</li>"),
        ("<li>レイクサイドCC <strong>65分</strong>（飯塚IC）</li>", "<li>レイクサイドCC <strong>65分</strong>（穂波西IC）</li>"),
    ],
}

BAD = ["博多IC", "Hakata IC", "하카타 IC", "福岡空港IC", "Fukuoka Airport IC", "후쿠오카 공항 IC", "飯塚IC", "Iizuka IC", "이이즈카 IC",
       "2号線で福岡IC", "Route 2 toward Fukuoka IC", "2호선으로 후쿠오카", "天神北ICまたは福岡IC", "Tenjin-Kita IC or Fukuoka IC",
       "須恵駅", "宇美駅", "若宮駅", "Wakamiya Station", "와카미야역", "赤間関", "Akamageki", "のだめ", "Nodame", "노다메", "60〜70km"]

for root in ROOTS:
    print(root)
    for name, rules in PLAN.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        new, done, miss = s, 0, []
        for a, b in rules:
            if a in new:
                k = new.count(a)
                new = new.replace(a, b)
                done += k
            elif b == "<li></li>" or b in new:
                pass  # 適用済み (削除した行は再実行時に見つからなくて正常)
            else:
                miss.append(a[:50])
        new = re.sub(r"[ \t]*<li></li>\r?\n", "", new)
        # レイクサイド英語: 2 枚目のカードに重複した「IC から約5分」行を外す
        new = re.sub(r"(<li>Turn right at the Taromaru 1-ku intersection</li>\r?\n)[ \t]*<li>About 5 min from the IC to the clubhouse \(Jalan Golf\)</li>\r?\n", r"\1", new)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        crlf = s.count("\r\n") > 0
        if crlf:
            assert new.count("\n") == new.count("\r\n"), name + " EOL"
        left = [x for x in BAD if x in new]
        print(f"  {name}: {done} 件{' (変更なし)' if new == s else ''}{'  未一致: ' + str(miss) if miss else ''}{'  残り: ' + str(left) if left else ''}")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
