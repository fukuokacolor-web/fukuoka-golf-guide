#!/usr/bin/env python3
"""add_area_cards2.py — Phase B Step 1 の 2 コース (shimaseaside / classic) を
エリアハブに追加。Tier 1 Batch 1 で course/access ページは作ったがエリアハブ
course-list には未掲載だったため、ここで補完して全 50 コースを揃える。

- shimaseaside → area-itoshima (badge 6)
- classic      → area-kitakyushu (badge 15)

挿入は add_area_cards.py と同じ `      </article>\\n\\n    </div>` マーカー split。
冪等ではない (再実行で重複) — 一度だけ実行。

Usage: python scripts/add_area_cards2.py [--dry-run]
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

COURSES = {
"itoshima": [
 dict(slug="shimaseaside", jid="02352", img="images/itoshima-sea.webp", sea=True,
   tagline="Itoshima · Shima-Nogita · Seaside",
   name={"ja":"志摩シーサイドカンツリークラブ","en":"Shima Seaside Country Club","ko":"시마 시사이드 컨트리 클럽"},
   chips={"ja":[("18H",""),("玄界灘ビュー","ocean"),("日本のペブルビーチ","gold")],
          "en":[("18H",""),("Ocean view","ocean"),("'Pebble Beach of Japan'","gold")],
          "ko":[("18홀",""),("겐카이나다 뷰","ocean"),("일본의 페블비치","gold")]},
   blurb={"ja":"玄界灘を望む18ホールのシーサイドコース。1977年開場。「日本のペブルビーチ」と称される絶景が魅力で、福岡空港から約50分。",
          "en":"An 18-hole seaside course overlooking the Genkai Sea, opened in 1977. Famed for ocean views that earn it the nickname 'the Pebble Beach of Japan' — about 50 minutes from Fukuoka Airport.",
          "ko":"겐카이나다를 바라보는 18홀 시사이드 코스. 1977년 개장. '일본의 페블비치'라 불리는 절경이 매력이며, 후쿠오카공항에서 약 50분."},
   price=("16,000","25,000")),
],
"kitakyushu": [
 dict(slug="classic", jid="02340", img="images/spring-forest.webp", sea=False,
   tagline="Miyawaka · Kurahisa · Championship",
   name={"ja":"ザ・クラシックゴルフ倶楽部","en":"The Classic Golf Club","ko":"더 클래식 골프 클럽"},
   chips={"ja":[("27H",""),("名門","gold"),("2028日本女子オープン会場","hl")],
          "en":[("27H",""),("Prestige","gold"),("2028 JP Women's Open","hl")],
          "ko":[("27홀",""),("명문","gold"),("2028 일본여자오픈","hl")]},
   blurb={"ja":"27ホールの名門コース。1990年開場で、2028年日本女子オープンの開催が予定される実力派。福岡空港から約45分。",
          "en":"A prestigious 27-hole course opened in 1990, set to host the 2028 Japan Women's Open — about 45 minutes from Fukuoka Airport.",
          "ko":"27홀 명문 코스. 1990년 개장으로 2028년 일본여자오픈 개최가 예정된 실력파. 후쿠오카공항에서 약 45분."},
   price=("13,390","24,450")),
],
}

PAGES = {
"area-itoshima.html": dict(
    area="itoshima", start=6, grad2="rgba(22,56,41,.55)",
    repl=[('"numberOfItems": 5,', '"numberOfItems": 6,'),
          ("— All 5 Courses", "— All 6 Courses"),
          ("糸島エリアの5コース", "糸島エリアの6コース"),
          ("The 5 courses, at a glance", "The 6 courses, at a glance"),
          ("이토시마 에리어의 5개 코스", "이토시마 에리어의 6개 코스"),
          ("ゴルフ場5コース完全ガイド", "ゴルフ場6コース完全ガイド"),
          ("to 5 golf courses in the Itoshima", "to 6 golf courses in the Itoshima"),
          ("이토시마 에리어 골프장 5개 코스 완전 가이드", "이토시마 에리어 골프장 6개 코스 완전 가이드")],
    jsonld_anchor='      { "@type": "ListItem", "position": 5, "name": "福岡雷山ゴルフ倶楽部", "url": "https://fukuoka-golf-guide.com/course-raizan.html" }',
    jsonld_add=[(6, "志摩シーサイドカンツリークラブ", "shimaseaside")]),
"area-kitakyushu.html": dict(
    area="kitakyushu", start=15, grad2="rgba(22,56,41,.55)",
    repl=[('"numberOfItems": 14,', '"numberOfItems": 15,'),
          ("— All 14 Courses", "— All 15 Courses"),
          ("北九州・宗像エリアの14コース", "北九州・宗像エリアの15コース"),
          ("The 14 courses, at a glance", "The 15 courses, at a glance"),
          ("기타큐슈・무나카타 에리어의 14개 코스", "기타큐슈・무나카타 에리어의 15개 코스"),
          ("ゴルフ場14コース完全ガイド", "ゴルフ場15コース完全ガイド"),
          ("to 14 golf courses in the Kitakyushu", "to 15 golf courses in the Kitakyushu"),
          ("기타큐슈・무나카타 에리어 골프장 14개 코스 완전 가이드", "기타큐슈・무나카타 에리어 골프장 15개 코스 완전 가이드")],
    jsonld_anchor='      { "@type": "ListItem", "position": 14, "name": "瀬板の森北九州ゴルフコース", "url": "https://fukuoka-golf-guide.com/course-seitanomori.html" }',
    jsonld_add=[(15, "ザ・クラシックゴルフ倶楽部", "classic")]),
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
        for o, n in cfg["repl"]:
            if o not in out:
                results.append(f"  {root.name}: WARN repl miss: {o[:40]}")
            out = out.replace(o, n)
        add = ",\n".join(
            f'      {{ "@type": "ListItem", "position": {p}, "name": "{nm}", '
            f'"url": "https://fukuoka-golf-guide.com/course-{sl}.html" }}'
            for p, nm, sl in cfg["jsonld_add"])
        if cfg["jsonld_anchor"] not in out:
            results.append(f"  {root.name}: WARN jsonld anchor miss")
        out = out.replace(cfg["jsonld_anchor"], cfg["jsonld_anchor"] + ",\n" + add, 1)
        if not DRY:
            path.write_text(out, encoding="utf-8")
        results.append(f"  {root.name}: +{len(courses)} card x3 / "
                        f"{'(dry-run)' if DRY else 'written'}")
    return results


print(f"[add_area_cards2] mode = {'DRY-RUN' if DRY else 'LIVE'}\n")
for fname, cfg in PAGES.items():
    print(f"--- {fname} (+{len(COURSES[cfg['area']])} course, badge {cfg['start']}) ---")
    for line in process(fname, cfg):
        print(line)
    print()
print("DONE" if not DRY else "*** DRY-RUN ***")
