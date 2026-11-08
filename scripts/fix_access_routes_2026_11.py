#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
住所の誤りが見つかった 7 コースのアクセスページの道順を、公式サイト (一部じゃらんゴルフ) の案内に合わせる (2026-11-08)。
各言語ブロック (c-ja / c-en / c-ko) の card[0] の tip、card[1] (空港から)、card[2] (その他)、card[4] (電車+タクシー) を置き換える。
出典は本文に (公式) / (じゃらん) と明記する。読みが不確かな地名は英語・韓国語欄でも漢字で書く。
冪等: 同じ内容なら変更なし。改行コードはそのまま保つ。
Usage: python scripts/fix_access_routes_2026_11.py [--apply]
"""
import os, re, sys, html

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
NAV = {"ja": "ナビアプリで「{n}」と検索すると最適ルートが案内されます。", "en": 'Search "{n}" in Google Maps for the best route.', "ko": "Google Maps에서 「{n}」를 검색하면 최적 경로가 안내됩니다."}

D = {
 "asoiizuka": {"n": "麻生飯塚ゴルフ倶楽部",
  "ja": {"tip0": "博多・福岡空港から車で約45分（公式）。九州自動車道の福岡ICから約30分です。",
         "c1": ["九州自動車道の福岡ICで降りる", "国道201号のバイパスを利用し、福岡ICから約30分（公式）", "合計：福岡空港から車で約45分（公式）"],
         "t2": "国道201号・国道200号利用", "c2": ["福岡市内から国道201号で飯塚方面へ", "飯塚から国道200号で桂川町へ進み、県道豆田稲築線でコースへ（じゃらん）", "北九州方面からは八幡IC（馬場山IC）から約45分（公式）"], "i2": "道順は公式サイトとじゃらんゴルフの案内をもとにしています。",
         "st": "JR桂川駅からタクシーで約10分、JR飯塚駅からタクシーで約15分です（公式）。JR博多駅からはタクシーで約45分です（公式）。"},
  "en": {"tip0": "About 45 min by car from Hakata or Fukuoka Airport (per the club), about 30 min from Fukuoka IC on the Kyushu Expressway.",
         "c1": ["Exit the Kyushu Expressway at Fukuoka IC", "Take the Route 201 bypass — about 30 min from Fukuoka IC (per the club)", "Total: approx. 45 min from Fukuoka Airport (per the club)"],
         "t2": "Via Route 201 / Route 200", "c2": ["From Fukuoka City, take Route 201 toward Iizuka", "From Iizuka, take Route 200 to Keisen Town, then Prefectural Road 豆田稲築線 to the course (Jalan Golf)", "From the Kitakyushu side, about 45 min from Yahata IC (Babayama IC), per the club"], "i2": "Directions are based on the club's website and Jalan Golf.",
         "st": "About 10 min by taxi from JR Keisen Station, or about 15 min from JR Iizuka Station (per the club). About 45 min by taxi from JR Hakata Station (per the club)."},
  "ko": {"tip0": "하카타·후쿠오카공항에서 차로 약 45분(공식). 규슈 자동차도 후쿠오카 IC에서 약 30분입니다.",
         "c1": ["규슈 자동차도 후쿠오카 IC에서 하차", "국도 201호 바이패스 이용, 후쿠오카 IC에서 약 30분(공식)", "합계: 후쿠오카공항에서 차로 약 45분(공식)"],
         "t2": "국도 201호·국도 200호 이용", "c2": ["후쿠오카 시내에서 국도 201호로 이이즈카 방면", "이이즈카에서 국도 200호로 桂川町까지 간 뒤 현도 豆田稲築線으로 코스까지(자란)", "기타큐슈 방면에서는 야하타 IC(바바야마 IC)에서 약 45분(공식)"], "i2": "경로는 공식 사이트와 자란골프 안내를 바탕으로 했습니다.",
         "st": "JR 桂川駅에서 택시로 약 10분, JR 이이즈카역에서 택시로 약 15분(공식). JR 하카타역에서 택시로 약 45분(공식)."}},
 "chikushigaoka": {"n": "筑紫ヶ丘ゴルフクラブ",
  "ja": {"tip0": "福岡空港・JR博多駅から車で約40分（公式）。福岡都市高速の野多目ランプから約10分です。",
         "c1": ["福岡空港から福岡都市高速に乗る", "野多目ランプで降り、那珂川方面へ（じゃらん）", "「現人橋」交差点を右折し、案内板に従ってゴルフ場へ（野多目ランプから約6km・約10分、公式）", "合計：福岡空港から車で約40分（公式）"],
         "t2": "九州自動車道利用", "c2": ["九州自動車道の太宰府IC または 筑紫野ICで降りる", "各ICから約17km・約30分（公式）", "天神からは約40分、大橋からは約15分（公式）"], "i2": "最寄りの出口は福岡都市高速の野多目ランプです（公式）。",
         "st": "JR博多南駅からタクシーで約10分（約4km）です（公式）。博多駅から博多南駅まではJR博多南線が便利です。"},
  "en": {"tip0": "About 40 min by car from Fukuoka Airport or JR Hakata Station (per the club), about 10 min from Notame ramp on the Fukuoka Urban Expressway.",
         "c1": ["Take the Fukuoka Urban Expressway from the airport", "Exit at Notame ramp and head toward Nakagawa (Jalan Golf)", "Turn right at the 現人橋 intersection and follow the signs (about 6 km / 10 min from the ramp, per the club)", "Total: approx. 40 min from Fukuoka Airport (per the club)"],
         "t2": "Via Kyushu Expressway", "c2": ["Exit the Kyushu Expressway at Dazaifu IC or Chikushino IC", "About 17 km / 30 min from either IC (per the club)", "About 40 min from Tenjin, 15 min from Ohashi (per the club)"], "i2": "The nearest exit is Notame ramp on the Fukuoka Urban Expressway (per the club).",
         "st": "About 10 min (4 km) by taxi from JR Hakata-Minami Station (per the club). The JR Hakata-Minami Line runs from Hakata Station."},
  "ko": {"tip0": "후쿠오카공항·JR 하카타역에서 차로 약 40분(공식). 후쿠오카 도시고속도로 노타메 램프에서 약 10분입니다.",
         "c1": ["후쿠오카공항에서 후쿠오카 도시고속도로 진입", "노타메 램프에서 내려 나카가와 방면으로(자란)", "「現人橋」 교차로에서 우회전 후 안내판을 따라 골프장으로(램프에서 약 6km·약 10분, 공식)", "합계: 후쿠오카공항에서 차로 약 40분(공식)"],
         "t2": "규슈 자동차도 이용", "c2": ["규슈 자동차도 다자이후 IC 또는 지쿠시노 IC에서 하차", "각 IC에서 약 17km·약 30분(공식)", "텐진에서 약 40분, 오하시에서 약 15분(공식)"], "i2": "가장 가까운 출구는 후쿠오카 도시고속도로 노타메 램프입니다(공식).",
         "st": "JR 하카타미나미역에서 택시로 약 10분(약 4km, 공식). 하카타역에서 하카타미나미역까지는 JR 하카타미나미선이 편리합니다."}},
 "fukuokacc": {"n": "福岡カンツリー倶楽部 和白コース",
  "ja": {"tip0": "福岡市内からは福岡都市高速の香椎東出口または香椎出口、北九州方面からは九州自動車道の古賀ICが便利です（公式）。",
         "c1": ["福岡空港から福岡都市高速に乗る", "香椎東出口 または 香椎出口で降りる（公式）", "一般道でクラブハウスへ"],
         "t2": "九州自動車道利用（北九州方面から）", "c2": ["九州自動車道の古賀ICで降りる（公式）", "一般道でクラブハウスへ"], "i2": "所要時間は交通状況で変わります。ナビアプリでご確認ください。",
         "st": "JR鹿児島本線「福工大前駅」からタクシーで約5分です（公式）。"},
  "en": {"tip0": "From Fukuoka City, use the Kashii-Higashi or Kashii exit of the Fukuoka Urban Expressway; from the Kitakyushu side, use Koga IC on the Kyushu Expressway (per the club).",
         "c1": ["Take the Fukuoka Urban Expressway from the airport", "Exit at Kashii-Higashi or Kashii (per the club)", "Follow local roads to the clubhouse"],
         "t2": "Via Kyushu Expressway (from Kitakyushu)", "c2": ["Exit the Kyushu Expressway at Koga IC (per the club)", "Follow local roads to the clubhouse"], "i2": "Travel time depends on traffic. Check a navigation app.",
         "st": "About 5 min by taxi from Fukkodai-mae Station on the JR Kagoshima Line (per the club)."},
  "ko": {"tip0": "후쿠오카 시내에서는 후쿠오카 도시고속도로 가시이히가시 출구 또는 가시이 출구, 기타큐슈 방면에서는 규슈 자동차도 고가 IC가 편리합니다(공식).",
         "c1": ["후쿠오카공항에서 후쿠오카 도시고속도로 진입", "가시이히가시 출구 또는 가시이 출구에서 하차(공식)", "일반 도로로 클럽하우스까지"],
         "t2": "규슈 자동차도 이용(기타큐슈 방면에서)", "c2": ["규슈 자동차도 고가 IC에서 하차(공식)", "일반 도로로 클럽하우스까지"], "i2": "소요 시간은 교통 상황에 따라 달라집니다. 내비게이션 앱으로 확인하세요.",
         "st": "JR 가고시마 본선 「후코다이마에역」에서 택시로 약 5분(공식)."}},
 "hisayama": {"n": "久山カントリー倶楽部",
  "ja": {"tip0": "博多駅から約16km。福岡空港・博多駅からタクシーで約20分です（公式）。",
         "c1": ["福岡空港から福岡都市高速に乗り、粕屋ランプで降りる", "福岡東バイパス（国道201号バイパス）を八木山方面へ進み、大隈の交差点（左折専用レーン）を左折", "二日市古賀線を進み、久山役場入口（右側にローソン）を右折", "役場を右手に見て正面のロータリーを直進するとコース（公式）"],
         "t2": "福岡都市高速・一般道", "c2": ["福岡市中心部からは都市高速で貝塚ランプ→粕屋ランプへ（公式）", "一般道なら県道21号を直方（犬鳴トンネル）方面へ進み、深井の交差点を左折、次の久山役場入口を右折（公式）", "博多駅からタクシーで約20〜25分（公式）"], "i2": "最寄りの出口は福岡都市高速の粕屋ランプです（公式）。",
         "st": "JR鹿児島本線「香椎駅」からタクシーで約15分（公式）、JR福北ゆたか線「篠栗駅」からタクシーで約10分です（じゃらん）。JRバス（直方行き）の「久山」バス停から徒歩約10分です（公式）。"},
  "en": {"tip0": "About 16 km from Hakata Station; about 20 min by taxi from Fukuoka Airport or Hakata Station (per the club).",
         "c1": ["Take the Fukuoka Urban Expressway from the airport and exit at Kasuya ramp", "Take the Fukuoka East Bypass (Route 201 bypass) toward Yagiyama and turn left at the Okuma intersection (left-turn lane)", "Follow the Futsukaichi–Koga road and turn right at 久山役場入口 (Lawson on the right)", "Pass the town office on your right and go straight through the roundabout to the course (per the club)"],
         "t2": "Urban Expressway / Local Roads", "c2": ["From central Fukuoka, take the Urban Expressway from Kaizuka ramp to Kasuya ramp (per the club)", "By local roads, take Prefectural Road 21 toward Nogata (Inunaki Tunnel), turn left at Fukai, then right at 久山役場入口 (per the club)", "About 20–25 min by taxi from Hakata Station (per the club)"], "i2": "The nearest exit is Kasuya ramp on the Fukuoka Urban Expressway (per the club).",
         "st": "About 15 min by taxi from JR Kashii Station (per the club), or about 10 min from JR Sasaguri Station (Jalan Golf). About 10 min on foot from the Hisayama bus stop on the JR Bus to Nogata (per the club)."},
  "ko": {"tip0": "하카타역에서 약 16km. 후쿠오카공항·하카타역에서 택시로 약 20분(공식).",
         "c1": ["후쿠오카공항에서 후쿠오카 도시고속도로 진입, 가스야 램프에서 하차", "후쿠오카 동부 바이패스(국도 201호 바이패스)를 야기야마 방면으로 진행, 오쿠마 교차로(좌회전 전용 차선)에서 좌회전", "후쓰카이치·고가선을 따라가다 「久山役場入口」(오른쪽 로손)에서 우회전", "관공서를 오른쪽에 두고 정면 로터리를 직진하면 코스(공식)"],
         "t2": "도시고속도로·일반 도로", "c2": ["후쿠오카 중심부에서는 도시고속도로 가이즈카 램프→가스야 램프(공식)", "일반 도로는 현도 21호를 노가타(이누나키 터널) 방면으로 진행, 후카이 교차로 좌회전 후 「久山役場入口」 우회전(공식)", "하카타역에서 택시로 약 20〜25분(공식)"], "i2": "가장 가까운 출구는 후쿠오카 도시고속도로 가스야 램프입니다(공식).",
         "st": "JR 가시이역에서 택시로 약 15분(공식), JR 사사구리역에서 택시로 약 10분(자란). JR 버스(노가타행) 「久山」 정류장에서 도보 약 10분(공식)."}},
 "ito": {"n": "伊都ゴルフ倶楽部",
  "ja": {"tip0": "福岡空港から都市高速経由で約35分、天神北ランプから約20分です（公式）。",
         "c1": ["福岡空港から福岡都市高速に乗り、西九州自動車道へ", "前原料金所を直進し、東信号を左折（じゃらん）", "次の三差路を右折、八反田信号を左折して約2kmでコース（じゃらん）", "合計：福岡空港から車で約35分（公式）"],
         "t2": "西九州自動車道・一般道", "c2": ["天神北ランプから都市高速経由で約20分（公式）", "香椎東ランプから約30分、太宰府ICから（月隈JCT経由）約40分（公式）", "唐津方面からは今宿バイパス経由で、東唐津から約30分（公式）"], "i2": "国道202号バイパスを唐津方面へ進み、有田東交差点を左折するルートもあります（じゃらん）。",
         "st": "JR筑肥線「筑前前原駅」からタクシーで約10分です（公式）。"},
  "en": {"tip0": "About 35 min from Fukuoka Airport via the Urban Expressway, about 20 min from Tenjin-kita ramp (per the club).",
         "c1": ["Take the Fukuoka Urban Expressway from the airport onto the Nishi-Kyushu Expressway", "Go straight through the Maebaru toll gate and turn left at the 東 signal (Jalan Golf)", "Turn right at the next fork, then left at the 八反田 signal; the course is about 2 km ahead (Jalan Golf)", "Total: approx. 35 min from Fukuoka Airport (per the club)"],
         "t2": "Nishi-Kyushu Expressway / Local Roads", "c2": ["About 20 min from Tenjin-kita ramp via the Urban Expressway (per the club)", "About 30 min from Kashii-Higashi ramp; about 40 min from Dazaifu IC via Tsukiguma JCT (per the club)", "From Karatsu, about 30 min from Higashi-Karatsu via the Imajuku Bypass (per the club)"], "i2": "You can also take the Route 202 bypass toward Karatsu and turn left at the Arita-Higashi intersection (Jalan Golf).",
         "st": "About 10 min by taxi from Chikuzen-Maebaru Station on the JR Chikuhi Line (per the club)."},
  "ko": {"tip0": "후쿠오카공항에서 도시고속도로 경유 약 35분, 텐진키타 램프에서 약 20분(공식).",
         "c1": ["후쿠오카공항에서 후쿠오카 도시고속도로를 거쳐 니시큐슈 자동차도로", "마에바루 요금소를 직진, 「東」 신호에서 좌회전(자란)", "다음 삼거리에서 우회전, 「八反田」 신호에서 좌회전 후 약 2km에 코스(자란)", "합계: 후쿠오카공항에서 차로 약 35분(공식)"],
         "t2": "니시큐슈 자동차도·일반 도로", "c2": ["텐진키타 램프에서 도시고속도로 경유 약 20분(공식)", "가시이히가시 램프에서 약 30분, 다자이후 IC에서(쓰키구마 JCT 경유) 약 40분(공식)", "가라쓰 방면에서는 이마주쿠 바이패스 경유, 히가시카라쓰에서 약 30분(공식)"], "i2": "국도 202호 바이패스를 가라쓰 방면으로 진행해 「有田東」 교차로에서 좌회전하는 경로도 있습니다(자란).",
         "st": "JR 지쿠히선 「지쿠젠마에바루역」에서 택시로 약 10분(공식)."}},
 "nijo": {"n": "二丈カントリークラブ",
  "ja": {"tip0": "アコーディア・ゴルフ運営。前原ICから約15km・約20分です（公式）。",
         "c1": ["福岡空港から福岡都市高速に乗り、西九州自動車道へ", "前原ICを過ぎて二丈浜玉バイパスへ進む", "福吉・七山の看板に沿って降り、コースへ（前原ICから約15km・約20分、公式）"],
         "t2": "唐津・佐賀方面から", "c2": ["唐津市内から約16km・約20分（公式）", "長崎自動車道の多久ICからは国道203号を唐津方面へ約50分、国道202号に当たって右折（公式）"], "i2": "二丈浜玉バイパスの吉井ICから約2kmです（じゃらん）。",
         "st": "最寄り駅はJR筑肥線「福吉駅」ですが、駅にタクシーは待機していません。クラブの送迎もないため、車でのご来場をおすすめします（じゃらん）。"},
  "en": {"tip0": "Operated by Accordia Golf. About 15 km / 20 min from Maebaru IC (per the club).",
         "c1": ["Take the Fukuoka Urban Expressway from the airport onto the Nishi-Kyushu Expressway", "Continue past Maebaru IC onto the Nijo-Hamatama Bypass", "Exit following the 福吉・七山 signs to the course (about 15 km / 20 min from Maebaru IC, per the club)"],
         "t2": "From Karatsu / Saga", "c2": ["About 16 km / 20 min from central Karatsu (per the club)", "From Taku IC on the Nagasaki Expressway, take Route 203 toward Karatsu for about 50 min, then turn right onto Route 202 (per the club)"], "i2": "About 2 km from Yoshii IC on the Nijo-Hamatama Bypass (Jalan Golf).",
         "st": "The nearest station is Fukuyoshi on the JR Chikuhi Line, but no taxis wait there and the club has no shuttle. Coming by car is recommended (Jalan Golf)."},
  "ko": {"tip0": "아코디아 골프 운영. 마에바루 IC에서 약 15km·약 20분(공식).",
         "c1": ["후쿠오카공항에서 후쿠오카 도시고속도로를 거쳐 니시큐슈 자동차도로", "마에바루 IC를 지나 니조하마타마 바이패스로 진행", "「福吉・七山」 안내판을 따라 내려가 코스로(마에바루 IC에서 약 15km·약 20분, 공식)"],
         "t2": "가라쓰·사가 방면에서", "c2": ["가라쓰 시내에서 약 16km·약 20분(공식)", "나가사키 자동차도 다쿠 IC에서는 국도 203호를 가라쓰 방면으로 약 50분, 국도 202호에서 우회전(공식)"], "i2": "니조하마타마 바이패스 요시이 IC에서 약 2km입니다(자란).",
         "st": "가장 가까운 역은 JR 지쿠히선 「후쿠요시역」이지만 역에 택시가 대기하지 않으며 클럽 송영도 없습니다. 자동차 이용을 권장합니다(자란)."}},
 "kyushugc": {"n": "九州ゴルフ倶楽部 八幡コース",
  "ja": {"st": "公式によると小倉駅から約15分です。駅からはタクシーをご利用ください。"},
  "en": {"st": "About 15 min from Kokura Station, per the club. Take a taxi from the station."},
  "ko": {"st": "공식 사이트에 따르면 고쿠라역에서 약 15분입니다. 역에서 택시를 이용하세요."}},
}


def ul(items, ind):
    return "<ul class=\"step-list\">\n" + "".join(f"{ind}  <li>{html.escape(i, quote=False)}</li>\n" for i in items) + f"{ind}</ul>"


def edit_block(b, d, n):
    cards = [m.start() for m in re.finditer(r'<div class="card">', b)]
    assert len(cards) >= 5, len(cards)
    parts = [b[:cards[0]]] + [b[cards[i]:(cards[i + 1] if i + 1 < len(cards) else len(b))] for i in range(len(cards))]
    c = parts[1:]
    if "tip0" in d:
        c[0], k = re.subn(r'(<div class="tip-bar"><span>💡</span>).*?(</div>)', lambda m: m.group(1) + html.escape(d["tip0"], quote=False) + m.group(2), c[0], count=1)
        assert k == 1
    if "c1" in d:
        c[1], k = re.subn(r'(\n([ \t]*))<ul class="step-list">.*?</ul>', lambda m: m.group(1) + ul(d["c1"], m.group(2)), c[1], count=1, flags=re.S)
        assert k == 1
        c[1] = re.sub(r'(<div class="tip-bar"><span>💡</span>).*?(</div>)', lambda m: m.group(1) + html.escape(NAV[d["lang"]].format(n=n), quote=False) + m.group(2), c[1], count=1)
    if "c2" in d:
        c[2] = re.sub(r'(<span class="title">).*?(</span>)', lambda m: m.group(1) + html.escape(d["t2"], quote=False) + m.group(2), c[2], count=1)
        c[2], k = re.subn(r'(\n([ \t]*))<ul class="step-list">.*?</ul>', lambda m: m.group(1) + ul(d["c2"], m.group(2)), c[2], count=1, flags=re.S)
        assert k == 1
        c[2], k = re.subn(r'(<div class="info-bar"><span>ℹ️</span>).*?(</div>)', lambda m: m.group(1) + html.escape(d["i2"], quote=False) + m.group(2), c[2], count=1)
        if k == 0:
            c[2] = re.sub(r'(<div class="tip-bar"><span>💡</span>).*?(</div>)', lambda m: m.group(1) + html.escape(d["i2"], quote=False) + m.group(2), c[2], count=1)
    if "st" in d:
        c[4], k = re.subn(r'(<div class="card-body">\s*\n?[ \t]*)[^<\n][^<]*?(\s*<div class="tip-bar">)', lambda m: m.group(1) + html.escape(d["st"], quote=False) + m.group(2), c[4], count=1)
        assert k == 1, "station"
    return parts[0] + "".join(c)


for root in ROOTS:
    print(root)
    for sl, data in D.items():
        p = os.path.join(root, f"access-{sl}.html")
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        t = s.replace("\r\n", "\n")
        ids = [(m.start(), m.group(1)) for m in re.finditer(r'<div id="c-(ja|en|ko)" class="content', t)]
        assert [i[1] for i in ids] == ["ja", "en", "ko"], ids
        out, last = [], 0
        for i, (pos, lang) in enumerate(ids):
            end = ids[i + 1][0] if i + 1 < len(ids) else t.find("</body>")
            out.append(t[last:pos])
            out.append(edit_block(t[pos:end], dict(data[lang], lang=lang), data["n"]))
            last = end
        out.append(t[last:])
        new = "".join(out).replace("\n", nl)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  access-{sl}.html: {'変更あり' if new != s else 'already'} ({len(new) - len(s):+d} chars)")
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
