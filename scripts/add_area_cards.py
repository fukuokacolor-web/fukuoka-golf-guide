#!/usr/bin/env python3
"""add_area_cards.py — エリアハブ 3 ページに Tier 1 Batch 2 の course-card を追加。

area-kitakyushu (+4) / area-chikugo (+4) / area-chikuho (+4) の JA/EN/KO 3 言語
course-list セクションに course-card を挿入し、numberOfItems・sec-eyebrow・h2・
JSON-LD itemListElement を更新する。両ディレクトリ (REPO_ROOT + PREVIEW_ROOT) に出力。

挿入は `      </article>\\n\\n    </div>` マーカー (各ページ 3 箇所 = 各言語 course-list 末尾)
で split して行う。冪等ではない (再実行で重複挿入) ため一度だけ実行する。

Usage:
    python scripts/add_area_cards.py --dry-run
    python scripts/add_area_cards.py
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv

JURL = ("https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2"
        "&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{jid}%2F")
DETAIL = {"ja": "コース詳細 →", "en": "View course →", "ko": "코스 상세 →"}
JLABEL = {"ja": "じゃらん", "en": "Jalan 🇯🇵 (JP)", "ko": "자란골프 🇯🇵 (일본어)"}
PPFX = {"ja": "目安 ", "en": "From ", "ko": "참고 "}


def C(slug, jid, img, sea, tagline, name, chips, blurb, price):
    return dict(slug=slug, jid=jid, img=img, sea=sea, tagline=tagline,
                name=name, chips=chips, blurb=blurb, price=price)


# ── 12 コースのカードデータ (name/chips/blurb は ja/en/ko) ──
COURSES = {
"kitakyushu": [
 C("newui", "02336", "images/fukuoka-bay.webp", True, "Munakata · Ocean view",
   {"ja":"NEWユーアイゴルフクラブ","en":"NEW U.I. Golf Club","ko":"NEW 유아이 골프 클럽"},
   {"ja":[("18H",""),("玄界灘ビュー","ocean"),("韓国語対応","hl")],
    "en":[("18H",""),("Ocean view","ocean"),("Korean OK","hl")],
    "ko":[("18홀",""),("겐카이나다 뷰","ocean"),("한국어 지원","hl")]},
   {"ja":"玄界灘を一望する18ホールのオーシャンビューコース。2000年開場。公式韓国語ページもあり、福岡空港から約45分。",
    "en":"An 18-hole ocean-view course overlooking the Genkai Sea, opened in 2000. An official Korean-language page is available; about 45 minutes from Fukuoka Airport.",
    "ko":"겐카이나다를 한눈에 바라보는 18홀 오션뷰 코스. 2000년 개장. 공식 한국어 페이지가 있으며 후쿠오카공항에서 약 45분."},
   ("6,910","14,091")),
 C("suonada", "02363", "images/fukuoka-overview.webp", True, "Chikujo · Suonada views",
   {"ja":"周防灘カントリークラブ","en":"Suonada Country Club","ko":"스오나다 컨트리 클럽"},
   {"ja":[("18H",""),("周防灘ビュー","ocean"),("FW乗入可","")],
    "en":[("18H",""),("Suonada view","ocean"),("Cart on FW","")],
    "ko":[("18홀",""),("스오나다 뷰","ocean"),("페어웨이 카트","")]},
   {"ja":"全ホールから周防灘を望む18ホール・7,069Yのヒルトップコース。1974年開場。フェアウェイ乗り入れ可。",
    "en":"An 18-hole, 7,069-yard hilltop course with views of the Suonada Sea from every hole. Opened 1974; cart-on-fairway permitted.",
    "ko":"전 홀에서 스오나다를 바라보는 18홀·7,069Y 힐탑 코스. 1974년 개장. 페어웨이 카트 진입 가능."},
   ("7,700","15,900")),
 C("chisan-onga", "02337", "images/sakura-road.webp", False, "Onga · 27H · PGM",
   {"ja":"チサンカントリークラブ遠賀","en":"Chisan Country Club Onga","ko":"치산 컨트리 클럽 오우카"},
   {"ja":[("27H",""),("PGM",""),("3コース構成","")],
    "en":[("27H",""),("PGM",""),("3 nines","")],
    "ko":[("27홀",""),("PGM",""),("3코스","")]},
   {"ja":"筑紫・玄海・遠賀の3コースからなる27ホール。1973年開場のPGM運営コースで、玄界灘と遠賀川を望むレイアウト。",
    "en":"A 27-hole PGM course (three nines: Chikushi, Genkai, Onga), opened in 1973, with views of the Genkai Sea and the Onga River.",
    "ko":"치쿠시·겐카이·온가 3개 코스로 구성된 27홀. 1973년 개장의 PGM 운영 코스로 겐카이나다와 온가강을 바라보는 레이아웃."},
   ("5,878","11,750")),
 C("seitanomori", "02311", "images/island-view.webp", False, "Kitakyushu · Municipal",
   {"ja":"瀬板の森北九州ゴルフコース","en":"Seitanomori Kitakyushu Golf Course","ko":"세이타노모리 기타큐슈 골프 코스"},
   {"ja":[("18H",""),("北九州市営",""),("駅から車10分","hl")],
    "en":[("18H",""),("Municipal",""),("10 min from stn","hl")],
    "ko":[("18홀",""),("기타큐슈 시영",""),("역에서 10분","hl")]},
   {"ja":"北九州市営のパブリックコース。1997年開場の18ホールで、JR黒崎駅から車10分の市街地近接が魅力。",
    "en":"A municipal public course run by Kitakyushu City. This 18-hole layout opened in 1997 and sits just 10 minutes by car from JR Kurosaki Station.",
    "ko":"기타큐슈 시영 퍼블릭 코스. 1997년 개장의 18홀로, JR 쿠로사키역에서 차로 10분 거리의 시가지 근접이 매력."},
   ("7,728","14,819")),
],
"chikugo": [
 C("satsuki-tenpai", "02323", "images/spring-forest.webp", False, "Chikushino · PGM",
   {"ja":"皐月ゴルフ倶楽部 天拝コース","en":"Satsuki Golf Club Tenpai Course","ko":"사쓰키 골프 클럽 덴파이 코스"},
   {"ja":[("18H",""),("PGM",""),("筑紫野IC7分","hl")],
    "en":[("18H",""),("PGM",""),("7 min from IC","hl")],
    "ko":[("18홀",""),("PGM",""),("치쿠시노 IC 7분","hl")]},
   {"ja":"九州自動車道 筑紫野ICから車7分の18ホール。1982年開場のPGM運営コースで、平日は昼食付プランあり。",
    "en":"An 18-hole PGM course just 7 minutes from Chikushino IC on the Kyushu Expressway. Opened 1982; weekday plans include lunch.",
    "ko":"규슈자동차도 치쿠시노 IC에서 차로 7분인 18홀. 1982년 개장의 PGM 운영 코스로 평일은 점심 포함 플랜이 있습니다."},
   ("7,241","15,569")),
 C("yasukogen", "02349", "images/aso-grassland.webp", False, "Chikuzen · Highland 27H",
   {"ja":"夜須高原カントリークラブ","en":"Yasukogen Country Club","ko":"야스코겐 컨트리 클럽"},
   {"ja":[("27H",""),("標高300m高原",""),("楽天評価4.4","gold")],
    "en":[("27H",""),("Highland 300m",""),("Rakuten 4.4","gold")],
    "ko":[("27홀",""),("고원 300m",""),("라쿠텐 4.4","gold")]},
   {"ja":"標高300mの高原に広がる27ホール。1974年開場で夏でも涼しく、楽天GORA評価4.4の福岡県有数の高評価コース。",
    "en":"A 27-hole course on a 300 m plateau, opened in 1974. Cool even in summer, it holds a strong Rakuten GORA rating of 4.4.",
    "ko":"표고 300m 고원에 펼쳐진 27홀. 1974년 개장으로 여름에도 시원하며, 라쿠텐 GORA 평가 4.4의 후쿠오카현 유수의 고평가 코스."},
   ("9,510","18,100")),
 C("yamejoyo", "02355", "images/fukuoka-overview.webp", False, "Yame · Stay + Play",
   {"ja":"八女上陽ゴルフ倶楽部","en":"Yame Joyo Golf Club","ko":"야메 죠요 골프 클럽"},
   {"ja":[("18H",""),("宿泊併設","hl"),("ふるさと納税可","")],
    "en":[("18H",""),("Stay + Play","hl"),("Hometown-tax","")],
    "ko":[("18홀",""),("숙박 병설","hl"),("후루사토납세","")]},
   {"ja":"ホテル+ロッジを併設した18ホールのリゾートコース。1992年開場。耳納連山と筑後平野を望み、ふるさと納税にも対応。",
    "en":"An 18-hole resort course with an attached hotel and lodges, opened in 1992. Views of the Mino mountains and Chikugo plain; hometown-tax eligible.",
    "ko":"호텔+롯지를 병설한 18홀 리조트 코스. 1992년 개장. 미노 연산과 치쿠고 평야를 바라보며 후루사토납세에도 대응."},
   ("7,146","14,873")),
 C("sunlake", "02357", "images/itoshima-bay.webp", True, "Miyama · Water strategy",
   {"ja":"福岡サンレイクゴルフ倶楽部","en":"Fukuoka Sunlake Golf Club","ko":"후쿠오카 선레이크 골프 클럽"},
   {"ja":[("18H",""),("池戦略コース",""),("年中無休","")],
    "en":[("18H",""),("Water strategy",""),("Open year-round","")],
    "ko":[("18홀",""),("연못 전략",""),("연중무휴","")]},
   {"ja":"大小の池が戦略性を高める18ホールの「池戦略コース」。2003年開場・年中無休営業で、楽天GORA評価4.3。",
    "en":"An 18-hole 'water-strategy' course where ponds large and small shape every shot. Opened 2003, open year-round, Rakuten GORA rating 4.3.",
    "ko":"크고 작은 연못이 전략성을 높이는 18홀 「연못 전략 코스」. 2003년 개장·연중무휴 영업, 라쿠텐 GORA 평가 4.3."},
   ("10,000","17,500")),
],
"chikuho": [
 C("satsuki-ryuoh", "02318", "images/golf-mountain.webp", False, "Iizuka · Mountain · PGM",
   {"ja":"皐月ゴルフ倶楽部 竜王コース","en":"Satsuki Golf Club Ryuoh Course","ko":"사쓰키 골프 클럽 류오 코스"},
   {"ja":[("18H",""),("山岳コース",""),("平日¥3,332〜","hl")],
    "en":[("18H",""),("Mountain",""),("Weekday ¥3,332+","hl")],
    "ko":[("18홀",""),("산악 코스",""),("평일 ¥3,332〜","hl")]},
   {"ja":"竜王山中腹の18ホール山岳コース。福岡市内より約4℃涼しく、2024年よりスループレー専用。平日¥3,332〜の好コスパ。",
    "en":"An 18-hole mountain course on the slopes of Mt. Ryuoh — about 4°C cooler than central Fukuoka. Through-play only since 2024; weekday rounds from ¥3,332.",
    "ko":"류오산 중턱의 18홀 산악 코스. 후쿠오카 시내보다 약 4℃ 시원하며 2024년부터 스루플레이 전용. 평일 ¥3,332〜의 좋은 가성비."},
   ("3,332","9,332")),
 C("kaho", "02347", "images/sakura-river.webp", False, "Iizuka · Accordia",
   {"ja":"かほゴルフクラブ","en":"Kaho Golf Club","ko":"카호 골프 클럽"},
   {"ja":[("18H",""),("アコーディア",""),("2グリーン制","")],
    "en":[("18H",""),("Accordia",""),("Two greens","")],
    "ko":[("18홀",""),("아코디아",""),("2그린제","")]},
   {"ja":"丘陵OUT+林間風INの2グリーン制18ホール。1975年開場のアコーディア運営コースで、福岡空港から約60分。",
    "en":"An 18-hole, two-green course with a hillside OUT and woodland-style IN. Opened 1975, run by Accordia; about 60 minutes from Fukuoka Airport.",
    "ko":"구릉 OUT+임간풍 IN의 2그린제 18홀. 1975년 개장의 아코디아 운영 코스로 후쿠오카공항에서 약 60분."},
   ("5,869","16,778")),
 C("nishinihon", "02317", "images/golf-mountain.webp", False, "Nogata · Gary Player design",
   {"ja":"西日本カントリークラブ","en":"Nishi-Nippon Country Club","ko":"니시니혼 컨트리 클럽"},
   {"ja":[("18H",""),("G・プレーヤー設計","gold"),("50年の名門","")],
    "en":[("18H",""),("Gary Player design","gold"),("50-yr heritage","")],
    "ko":[("18홀",""),("게리 플레이어 설계","gold"),("50년 명문","")]},
   {"ja":"世界三大プロゴルファー、ゲーリー・プレーヤー設計の戦略的18ホール。1975年開場、50年の歴史を持つ福岡北部の名門。",
    "en":"A strategic 18-hole course designed by Gary Player, one of golf's 'Big Three.' Opened in 1975 — a 50-year heritage course in northern Fukuoka.",
    "ko":"세계 3대 프로골퍼 게리 플레이어가 설계한 전략적 18홀. 1975년 개장, 50년 역사를 지닌 후쿠오카 북부의 명문."},
   ("7,810","16,446")),
 C("jruchino", "02345", "images/spring-forest.webp", False, "Iizuka · JR Kyushu resort",
   {"ja":"JR内野カントリークラブ","en":"JR Uchino Country Club","ko":"JR 우치노 컨트리 클럽"},
   {"ja":[("18H",""),("JR九州運営",""),("韓国語/英語対応","hl")],
    "en":[("18H",""),("JR Kyushu",""),("KO/EN pages","hl")],
    "ko":[("18홀",""),("JR큐슈 운영",""),("한국어/영어","hl")]},
   {"ja":"JR九州リゾート開発が運営する18ホールの丘陵フラットコース。1992年開場。大浴場完備、公式韓国語/英語ページあり。",
    "en":"An 18-hole flat hillside course run by JR Kyushu Resort Development, opened in 1992. Large bath house; official Korean and English pages available.",
    "ko":"JR큐슈 리조트 개발이 운영하는 18홀 구릉 플랫 코스. 1992년 개장. 대욕장 완비, 공식 한국어/영어 페이지 있음."},
   ("9,500","16,500")),
],
}

# ── ページ別設定 ──
PAGES = {
"area-kitakyushu.html": dict(
    area="kitakyushu", start=11, grad2="rgba(22,56,41,.55)",
    repl=[('"numberOfItems": 10,', '"numberOfItems": 14,'),
          ("— All 10 Courses", "— All 14 Courses"),
          ("北九州・宗像エリアの10コース", "北九州・宗像エリアの14コース"),
          ("The 10 courses, at a glance", "The 14 courses, at a glance"),
          ("기타큐슈・무나카타 에리어의 10개 코스", "기타큐슈・무나카타 에리어의 14개 코스")],
    jsonld_anchor='      { "@type": "ListItem", "position": 10, "name": "玄海ゴルフクラブ", "url": "https://fukuoka-golf-guide.com/course-genkai.html" }',
    jsonld_add=[(11,"NEWユーアイゴルフクラブ","newui"),(12,"周防灘カントリークラブ","suonada"),
                (13,"チサンカントリークラブ遠賀","chisan-onga"),(14,"瀬板の森北九州ゴルフコース","seitanomori")]),
"area-chikugo.html": dict(
    area="chikugo", start=8, grad2="rgba(22,56,41,.55)",
    repl=[('"numberOfItems": 7,', '"numberOfItems": 11,'),
          ("— All 6 Courses", "— All 11 Courses"),
          ("筑後・久留米エリアの7コース", "筑後・久留米エリアの11コース"),
          ("The 6 courses, at a glance", "The 11 courses, at a glance"),
          ("치쿠고·구루메 에리어 6개 코스", "치쿠고·구루메 에리어 11개 코스")],
    jsonld_anchor='      { "@type": "ListItem", "position": 7, "name": "浮羽カントリークラブ", "url": "https://fukuoka-golf-guide.com/course-ukiha.html" }',
    jsonld_add=[(8,"皐月ゴルフ倶楽部 天拝コース","satsuki-tenpai"),(9,"夜須高原カントリークラブ","yasukogen"),
                (10,"八女上陽ゴルフ倶楽部","yamejoyo"),(11,"福岡サンレイクゴルフ倶楽部","sunlake")]),
"area-chikuho.html": dict(
    area="chikuho", start=7, grad2="rgba(107,84,54,.55)",
    repl=[('"numberOfItems": 5,', '"numberOfItems": 10,'),
          ("— All 4 Courses", "— All 10 Courses"),
          ("筑豊・朝倉エリアの6コース", "筑豊・朝倉エリアの10コース"),
          ("The 4 courses, at a glance", "The 10 courses, at a glance"),
          ("치쿠호·아사쿠라 에리어 6개 코스", "치쿠호·아사쿠라 에리어 10개 코스")],
    jsonld_anchor='      { "@type": "ListItem", "position": 5, "name": "福岡フェザントカントリークラブ", "url": "https://fukuoka-golf-guide.com/course-pheasant.html" }',
    jsonld_add=[(6,"セントラル福岡ゴルフ倶楽部","central"),(7,"皐月ゴルフ倶楽部 竜王コース","satsuki-ryuoh"),
                (8,"かほゴルフクラブ","kaho"),(9,"西日本カントリークラブ","nishinihon"),
                (10,"JR内野カントリークラブ","jruchino")]),
}


def build_card(c, lang, n, grad2):
    first = "58,124,165" if c["sea"] else "127,166,90"
    grad = f"linear-gradient(135deg,rgba({first},.35),{grad2})"
    chips = "\n            ".join(
        f'<span class="course-chip{(" " + cl) if cl else ""}">{t}</span>'
        for t, cl in c["chips"][lang])
    mn, mx = c["price"]
    sep = "–" if lang == "en" else "〜"
    price = f'{PPFX[lang]}<strong>¥{mn}{sep}{mx}</strong>'
    jurl = JURL.format(jid=c["jid"])
    return f'''      <article class="course-card">
        <a href="course-{c['slug']}.html" class="course-img bg" style="background-image:{grad},url('{c['img']}');">
          <div class="course-num-badge">{n}</div>
        </a>
        <div class="course-body">
          <div class="course-area">{c['tagline']}</div>
          <div class="course-name">{c['name'][lang]}</div>
          <div class="course-meta">
            {chips}
          </div>
          <div class="course-desc">{c['blurb'][lang]}</div>
          <div class="course-footer">
            <div class="course-price">{price}</div>
            <div class="course-actions">
              <a href="course-{c['slug']}.html" class="course-btn btn-detail">{DETAIL[lang]}</a>
              <a href="{jurl}" class="course-btn btn-jalan-s" target="_blank" rel="nofollow sponsored noopener">📅 {JLABEL[lang]}</a>
            </div>
          </div>
        </div>
      </article>'''


MARKER = "      </article>\n\n    </div>"


def process(fname, cfg):
    courses = COURSES[cfg["area"]]
    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        path = root / fname
        if not path.exists():
            results.append(f"  {root.name}: NOT FOUND")
            continue
        html = path.read_text(encoding="utf-8")
        parts = html.split(MARKER)
        if len(parts) != 4:
            results.append(f"  {root.name}: SKIP — marker count {len(parts)-1} != 3")
            continue
        out = parts[0]
        for i, lang in enumerate(["ja", "en", "ko"]):
            cards = "".join("\n\n" + build_card(c, lang, cfg["start"] + j, cfg["grad2"])
                            for j, c in enumerate(courses))
            out += "      </article>" + cards + "\n\n    </div>" + parts[i + 1]
        # counts / h2 / eyebrow
        for o, n in cfg["repl"]:
            out = out.replace(o, n)
        # JSON-LD itemListElement
        add = ",\n".join(
            f'      {{ "@type": "ListItem", "position": {p}, "name": "{nm}", '
            f'"url": "https://fukuoka-golf-guide.com/course-{sl}.html" }}'
            for p, nm, sl in cfg["jsonld_add"])
        out = out.replace(cfg["jsonld_anchor"], cfg["jsonld_anchor"] + ",\n" + add, 1)
        if not DRY:
            path.write_text(out, encoding="utf-8")
        results.append(f"  {root.name}: {len(courses)} cards x3 lang / "
                        f"+{out.count(chr(10)) - html.count(chr(10))} lines / "
                        f"{'(dry-run)' if DRY else 'written'}")
    return results


print(f"[add_area_cards] mode = {'DRY-RUN' if DRY else 'LIVE'}\n")
for fname, cfg in PAGES.items():
    print(f"--- {fname} (+{len(COURSES[cfg['area']])} courses, badges {cfg['start']}-) ---")
    for line in process(fname, cfg):
        print(line)
    print()
print("DONE" if not DRY else "*** DRY-RUN: re-run without --dry-run to apply ***")
