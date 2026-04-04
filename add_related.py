import re

# 関連コース定義（各コース: 近隣・同カテゴリの2〜3コース）
RELATED = {
    "aburayama":    ["fukuokacc", "hisayama", "saitozaki"],
    "akane":        ["dazaifu", "chikushino", "ogori"],
    "ariake":       ["century", "kurume"],
    "asoiizuka":    ["kyushugc", "mission", "sevenmillion"],
    "central":      ["chikushigaoka", "koga", "moonlake"],
    "century":      ["ariake", "kurume"],
    "chikushigaoka":["koga", "central", "moonlake"],
    "chikushino":   ["dazaifu", "akane", "ogori"],
    "daihakata":    ["hisayama", "fukuokacc", "saitozaki"],
    "dazaifu":      ["chikushino", "akane", "ogori"],
    "fukuokacc":    ["hisayama", "daihakata", "saitozaki"],
    "hisayama":     ["fukuokacc", "daihakata", "koga"],
    "ito":          ["keya", "nijo"],
    "keya":         ["ito", "nijo"],
    "kitakyushu":   ["moji", "sevenmillion"],
    "koga":         ["central", "chikushigaoka", "hisayama"],
    "kurume":       ["ogori", "ariake", "century"],
    "kyushugc":     ["asoiizuka", "mission", "sevenmillion"],
    "lakeside":     ["ogori", "dazaifu", "chikushino"],
    "mission":      ["sevenmillion", "kyushugc", "asoiizuka"],
    "moji":         ["kitakyushu", "sevenmillion"],
    "moonlake":     ["central", "chikushigaoka", "koga"],
    "nijo":         ["keya", "ito"],
    "ogori":        ["lakeside", "chikushino", "dazaifu"],
    "queenshill":   ["wakamiya", "central", "koga"],
    "saitozaki":    ["fukuokacc", "hisayama", "daihakata"],
    "sevenmillion": ["mission", "kyushugc", "asoiizuka"],
    "wakamiya":     ["queenshill", "central"],
}

# コース表示名
NAMES = {
    "aburayama":    ("油山市民GC",          "Aburayama GC",       "아부라야마 GC"),
    "akane":        ("あかねGC",             "Akane GC",           "아카네 GC"),
    "ariake":       ("有明GC",              "Ariake GC",          "아리아케 GC"),
    "asoiizuka":    ("阿蘇飯塚GC",          "Aso Iizuka GC",      "아소이이즈카 GC"),
    "central":      ("セントラル福岡GC",     "Central Fukuoka GC", "센트럴 후쿠오카 GC"),
    "century":      ("センチュリー大牟田GC", "Century Omuta GC",   "센추리 오무타 GC"),
    "chikushigaoka":("筑紫ヶ丘GC",          "Chikushigaoka GC",   "지쿠시가오카 GC"),
    "chikushino":   ("筑紫野GC",            "Chikushino GC",      "지쿠시노 GC"),
    "daihakata":    ("大博多CC",             "Dai-Hakata CC",      "다이하카타 CC"),
    "dazaifu":      ("太宰府CC",             "Dazaifu CC",         "다자이후 CC"),
    "fukuokacc":    ("福岡CC（和白）",       "Fukuoka CC (Wajiro)","후쿠오카 CC"),
    "hisayama":     ("久山CC",              "Hisayama CC",        "히사야마 CC"),
    "ito":          ("糸島GC",              "Itoshima GC",        "이토시마 GC"),
    "keya":         ("芥屋GC",              "Keya GC",            "케야 GC"),
    "kitakyushu":   ("北九州GC",            "Kitakyushu GC",      "기타큐슈 GC"),
    "koga":         ("古賀GC",              "Koga GC",            "고가 GC"),
    "kurume":       ("久留米CC",             "Kurume CC",          "구루메 CC"),
    "kyushugc":     ("九州GC",              "Kyushu GC",          "규슈 GC"),
    "lakeside":     ("レイクサイドGC",       "Lakeside GC",        "레이크사이드 GC"),
    "mission":      ("ミッションバレーGC",   "Mission Valley GC",  "미션밸리 GC"),
    "moji":         ("門司GC",              "Moji GC",            "모지 GC"),
    "moonlake":     ("ムーンレイクGC",       "Moon Lake GC",       "문레이크 GC"),
    "nijo":         ("二丈GC",              "Nijo GC",            "니조 GC"),
    "ogori":        ("小郡CC",              "Ogori CC",           "오고리 CC"),
    "queenshill":   ("クイーンズヒルGC",     "Queens Hill GC",     "퀸즈힐 GC"),
    "saitozaki":    ("西戸崎GC",            "Saitozaki GC",       "사이토자키 GC"),
    "sevenmillion": ("セブンミリオンGC",     "Seven Million GC",   "세븐밀리언 GC"),
    "wakamiya":     ("若宮GC",              "Wakamiya GC",        "와카미야 GC"),
}

STYLE_SECTION = """<div style="max-width:680px;margin:0 auto;padding:12px 16px 28px;">
  <div style="font-size:0.72rem;font-weight:800;text-transform:uppercase;letter-spacing:0.1em;color:#6b7280;margin-bottom:10px;">🔗 関連コース / Related Courses / 관련 코스</div>
  <div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px;">
{course_links}  </div>
  <a href="recommend.html" style="display:block;background:linear-gradient(135deg,#1a5c38,#2e8b57);color:#fff;text-align:center;padding:11px 16px;border-radius:10px;text-decoration:none;font-size:0.82rem;font-weight:700;">⭐ 目的別おすすめ特集 / Best Courses by Purpose / 추천 골프장 특집 →</a>
</div>
"""

LINK_STYLE = 'display:inline-block;background:#fff;border:1.5px solid #b8d9c5;border-radius:8px;padding:7px 14px;font-size:0.8rem;font-weight:700;text-decoration:none;color:#1a5c38;'

ok, skip = 0, 0

for slug, related in RELATED.items():
    fname = f"course-{slug}.html"
    try:
        with open(fname, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"NOT FOUND: {fname}")
        skip += 1
        continue

    if "recommend.html" in content and "関連コース" in content:
        print(f"SKIP (already done): {fname}")
        skip += 1
        continue

    # コースリンクHTML生成
    links = ""
    for r in related:
        ja, en, ko = NAMES[r]
        links += f'    <a href="course-{r}.html" style="{LINK_STYLE}">{ja} / {en} / {ko}</a>\n'

    section = STYLE_SECTION.replace("{course_links}", links)

    if "<footer>" not in content:
        print(f"WARN (no footer): {fname}")
        skip += 1
        continue

    new_content = content.replace("<footer>", section + "<footer>", 1)
    with open(fname, "w", encoding="utf-8") as f:
        f.write(new_content)
    ok += 1
    print(f"OK: {fname}")

print(f"\n完了: {ok}件 / スキップ: {skip}件")
