#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fees.html の料金比較表 (JS の COURSES) と料金の目安欄を、確認済みデータだけで作り直す (§7)。

旧データの問題 (2026-10-28 確認): 名前の誤り (「センチュリー三木」「有明グランド」)・所在地の誤り
(セントラル福岡/あかね=糟屋郡・ムーンレイク=飯塚市)・見出し28コースなのにデータ34件・予約できないコースに金額。

- 名前・所在地: 各 course-*.html の JSON-LD (GolfCourse) と hero-title (JA/EN/KO)
- 料金: scripts/.cache/jalan_floor.json (じゃらん・2026-10-24・直近14日の18H最安の総額)
- 予約できないコース (CLAUDE.md §9.4): 金額を出さず「公式で確認」「楽天で確認」
- 目安欄: 確認データの中央値と中央の半数の範囲
冪等: 生成結果が同じなら no-op。
Usage:
  python scripts/rebuild_fees_table_2026_10.py            # dry-run
  python scripts/rebuild_fees_table_2026_10.py --apply    # REPO + PREVIEW
"""
import re, os, sys, json, glob, statistics

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv
F = "fees.html"
CHECKED = {"ja": "2026年10月24日確認", "en": "checked Oct 24, 2026", "ko": "2026년 10월 24일 확인"}

OFFICIAL_ONLY = {"fukuokacc", "wakamatsu", "genkai", "koga", "moji", "classic", "kokura", "queenshill", "raizan", "keya"}
RAKUTEN_ONLY = {"aburayama", "kyushugc", "saitozaki", "akane", "yasukogen", "sunlake"}
AREA = {  # 所在地 (JA → EN, KO)
    "福岡市城南区": ("Fukuoka (Jonan)", "후쿠오카시 조난구"), "飯塚市": ("Iizuka", "이이즈카시"), "大牟田市": ("Omuta", "오무타시"),
    "筑紫野市": ("Chikushino", "지쿠시노시"), "朝倉市": ("Asakura", "아사쿠라시"), "那珂川市": ("Nakagawa", "나카가와시"),
    "遠賀郡遠賀町": ("Onga", "온가군"), "宮若市": ("Miyawaka", "미야와카시"), "太宰府市": ("Dazaifu", "다자이후시"),
    "福岡市東区": ("Fukuoka (Higashi)", "후쿠오카시 히가시구"), "宗像市": ("Munakata", "무나카타시"),
    "糟屋郡久山町": ("Hisayama", "히사야마정"), "糸島市": ("Itoshima", "이토시마시"), "北九州市若松区": ("Kitakyushu (Wakamatsu)", "기타큐슈시 와카마쓰구"),
    "古賀市": ("Koga", "고가시"), "北九州市": ("Kitakyushu", "기타큐슈시"), "八女郡広川町": ("Hirokawa", "히로카와정"),
    "北九州市八幡西区": ("Kitakyushu (Yahatanishi)", "기타큐슈시 야하타니시구"), "鞍手郡小竹町": ("Kotake", "고타케정"),
    "北九州市門司区": ("Kitakyushu (Moji)", "기타큐슈시 모지구"), "鞍手郡鞍手町": ("Kurate", "구라테정"), "直方市": ("Nogata", "노가타시"),
    "小郡市": ("Ogori", "오고리시"), "田川郡": ("Tagawa", "다가와군"), "福岡市早良区": ("Fukuoka (Sawara)", "후쿠오카시 사와라구"),
    "みやま市": ("Miyama", "미야마시"), "築上郡築上町": ("Chikujo", "지쿠조정"), "うきは市": ("Ukiha", "우키하시"),
    "八女市": ("Yame", "야메시"), "朝倉郡筑前町": ("Chikuzen", "지쿠젠정"),
}
AREA_FIX = {"century": "朝倉市"}  # JSON-LD に addressLocality が無い → ページの連絡先 (Asakura City) より


def courses():
    mapping = {c["file"].replace("course-", ""): c.get("jalan_id")
               for c in json.load(open(os.path.join(REPO_ROOT, "jalan_golf_mapping.json"), encoding="utf-8"))["courses"]}
    floor = json.load(open(os.path.join(REPO_ROOT, "scripts/.cache/jalan_floor.json"), encoding="utf-8"))
    out = []
    for f in sorted(glob.glob(os.path.join(REPO_ROOT, "course-*.html"))):
        slug = os.path.basename(f)[7:-5]
        if slug == "quiz":
            continue
        t = open(f, encoding="utf-8").read()
        gc = None
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
            try:
                j = json.loads(b)
            except Exception:
                continue
            if isinstance(j, dict) and j.get("@type") == "GolfCourse":
                gc = j
        titles = [re.sub(r"<[^>]+>|\s+", " ", x).strip() for x in re.findall(r'<h1 class="hero-title">(.*?)</h1>', t, re.S)]
        area = AREA_FIX.get(slug) or gc["address"]["addressLocality"]
        jid = mapping.get(slug)
        r = floor.get(str(jid).zfill(5)) if jid else None
        if slug in OFFICIAL_ONLY:
            st = "official"
        elif slug in RAKUTEN_ONLY:
            st = "rakuten"
        else:
            st = "ok" if r and r.get("weekday") else "none"
        wd = r["weekday"]["total"] if st == "ok" else None
        we = (r.get("weekend") or {}).get("total") if st == "ok" else None
        out.append({"key": slug, "ja": gc["name"], "en": titles[1], "ko": titles[2],
                    "area_ja": area, "area_en": AREA[area][0], "area_ko": AREA[area][1],
                    "wd_lo": wd, "wd_hi": wd, "we_lo": we, "we_hi": we, "st": st})
    return out


JS_OLD_L10N = re.compile(r"  var L10N = \{.*?\n  \};\n  function fmt\(lo, hi, lang\)\{.*?\n  \}\n", re.S)
JS_NEW_L10N = '''  var L10N = {
    ja: {head_name:"コース", head_wd:"平日", head_we:"土日祝", cta:"詳細 →", pre:"¥", suf:"〜",
         official:"公式で確認", rakuten:"楽天で確認", none:"予約サイトで確認"},
    en: {head_name:"Course", head_wd:"Wkd", head_we:"Wknd", cta:"Detail →", pre:"From ¥", suf:"",
         official:"Official site", rakuten:"Rakuten GORA", none:"Booking site"},
    ko: {head_name:"코스", head_wd:"평일", head_we:"주말", cta:"상세 →", pre:"¥", suf:"부터",
         official:"공식 사이트", rakuten:"라쿠텐 확인", none:"예약 사이트 확인"}
  };
  // 料金はじゃらんの総額 (2026-10-24 確認・直近14日の18H最安)。予約できない/確認できないコースは金額を出さない
  function fmt(lo, hi, lang, st){
    var p = L10N[lang];
    if (lo === null || lo === undefined) return '<span style="font-size:0.85em;opacity:.8;">' + p[st === "ok" ? "none" : st] + '</span>';
    return p.pre + lo.toLocaleString("en-US") + p.suf;
  }
'''


def main():
    src = open(os.path.join(REPO_ROOT, F), encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    s = src.replace("\r\n", "\n")
    data = courses()
    n = len(data)
    ok = [c for c in data if c["st"] == "ok"]
    wk = [c["wd_lo"] for c in ok]
    we = [c["we_lo"] for c in ok if c["we_lo"]]
    q = lambda a: statistics.quantiles(a, n=4)
    wk_med, wk_q, we_med, we_q = statistics.median(wk), q(wk), statistics.median(we), q(we)
    r100 = lambda v: int(round(v / 100.0) * 100)
    yen = lambda v: f"¥{r100(v):,}"

    # 1) データ
    s, k = re.subn(r"  var COURSES = \[.*?\];\n", "  var COURSES = " + json.dumps(data, ensure_ascii=False) + ";\n", s, count=1, flags=re.S)
    assert k == 1
    # 2) L10N / fmt / 並べ替え (金額なしは最後) / fmt 呼び出し
    first_run = "function fmt(lo, hi, lang, st)" not in s  # 2回目以降は COURSES の再生成だけ (冪等)
    if first_run:
        s, k = JS_OLD_L10N.subn(JS_NEW_L10N, s, count=1); assert k == 1, "l10n"
        old_sort = "else items.sort(function(a,b){ return a[sortKey] - b[sortKey]; });"
        assert s.count(old_sort) == 1
        s = s.replace(old_sort, "else items.sort(function(a,b){ var x = a[sortKey] == null ? 1e9 : a[sortKey], y = b[sortKey] == null ? 1e9 : b[sortKey]; return x - y; });")
        for side in ("wd", "we"):
            old = f"fmt(c.{side}_lo,c.{side}_hi,lang)"
            assert s.count(old) == 1, old
            s = s.replace(old, f"fmt(c.{side}_lo,c.{side}_hi,lang,c.st)")

    # 3) 件数と説明
    reps = [] if not first_run else [
        ("福岡近郊ゴルフ場28コースの料金・予約情報一覧。平日・週末料金、予約方法を掲載。", f"福岡のゴルフ場{n}コースの料金・予約情報一覧。じゃらんで確認した平日・土日祝の最安（総額）と予約方法を掲載。", 2),
        ("Green fees and booking guide for 28 Fukuoka golf courses.", f"Green fees and booking guide for {n} Fukuoka golf courses.", 1),
        ("후쿠오카 근교 골프장 28코스의", f"후쿠오카 골프장 {n}코스의", 1),
        ("⚖️ 28コース料金比較表（クリック詳細＆予約へ）", f"⚖️ {n}コース料金比較表（クリック詳細＆予約へ）", 1),
        ("福岡近郊28コースの平日・土日料金を一覧。予算順にソートして比較、気になるコースの「詳細 →」で詳細ページ＆予約へ。",
         f"{n}コースの平日・土日祝の最安を一覧（じゃらんの総額・直近14日の18ホール・{CHECKED['ja']}）。予約できないコースは「公式で確認」「楽天で確認」と表示しています。料金は日々変わるので、「詳細 →」から最新をご確認ください。", 1),
        ("⚖️ 28 Courses Fee Comparison (Click for Detail & Booking)", f"⚖️ {n} Courses Fee Comparison (Click for Detail & Booking)", 1),
        ("Weekday &amp; weekend green fees for 28 courses near Fukuoka. Sort by budget, then click \"Detail →\" for full info and booking.",
         f"Lowest weekday &amp; weekend rates for {n} courses (Jalan total price, 18 holes, next 14 days, {CHECKED['en']}). Courses without online booking show \"Official site\" or \"Rakuten GORA\". Rates change daily — click \"Detail →\" for the latest.", 1),
        ("⚖️ 28개 코스 요금 비교표 (클릭하여 상세·예약)", f"⚖️ {n}개 코스 요금 비교표 (클릭하여 상세·예약)", 1),
        ("후쿠오카 인근 28개 코스의 평일·주말 요금. 예산순으로 정렬하고 \"상세 →\"를 눌러 코스 상세페이지&amp;예약으로 이동하세요.",
         f"{n}개 코스의 평일·주말 최저가 (자란 총액·향후 14일·18홀·{CHECKED['ko']}). 온라인 예약이 안 되는 코스는 \"공식 사이트\" 또는 \"라쿠텐 확인\"으로 표시합니다. 요금은 매일 바뀌므로 \"상세 →\"에서 최신 정보를 확인하세요.", 1),
    ]
    # 4) 目安欄 (3言語) と FAQ
    box = {"ja": ("¥6,000〜¥12,000", "¥12,000〜¥20,000", "目安 / カート・食事別"),
           "en": ("¥6,000–¥12,000", "¥12,000–¥20,000", None), "ko": ("¥6,000〜¥12,000", "¥12,000〜¥20,000", None)}
    note = {"ja": (f"中央値 {yen(wk_med)}／半数が{yen(wk_q[0])}〜{yen(wk_q[2])}", f"中央値 {yen(we_med)}／半数が{yen(we_q[0])}〜{yen(we_q[2])}"),
            "en": (f"Median {yen(wk_med)} / half of courses {yen(wk_q[0])}–{yen(wk_q[2])}", f"Median {yen(we_med)} / half of courses {yen(we_q[0])}–{yen(we_q[2])}"),
            "ko": (f"중앙값 {yen(wk_med)} / 절반이 {yen(wk_q[0])}〜{yen(wk_q[2])}", f"중앙값 {yen(we_med)} / 절반이 {yen(we_q[0])}〜{yen(we_q[2])}")}
    if first_run:
        s, k = re.subn(r'(<div class="price">)¥6,000[〜–]¥12,000(</div>\s*<div class="note">)[^<]*(</div>)',
                       lambda m: m.group(1) + f"{yen(wk_med)}" + m.group(2) + "__WKNOTE__" + m.group(3), s)
        assert k == 3, ("wk", k)
        s, k = re.subn(r'(<div class="price">)¥12,000[〜–]¥20,000(</div>\s*<div class="note">)[^<]*(</div>)',
                       lambda m: m.group(1) + f"{yen(we_med)}" + m.group(2) + "__WENOTE__" + m.group(3), s)
        assert k == 3, ("we", k)
        for lang in ("ja", "en", "ko"):  # 出現順は JA → EN → KO
            s = s.replace("__WKNOTE__", note[lang][0], 1).replace("__WENOTE__", note[lang][1], 1)
    reps += [] if not first_run else [
        ("<span class=\"title\">グリーンフィー相場（カート・昼食別）</span>", "<span class=\"title\">平日・土日祝の最安（じゃらん総額の中央値）</span>", 1),
        ("福岡県内のゴルフ場の一般的な相場です。コースや季節・時間帯によって大きく異なります。",
         f"じゃらんで予約できる{len(ok)}コースの、直近14日の18ホール最安（総額）の中央値です（{CHECKED['ja']}）。コースや日付で大きく異なります。", 1),
        ("上記は福岡県内の一般的な相場です。各ゴルフ場の実際の料金は公式サイトでご確認ください。",
         "上記は確認時点の値です。実際の料金は予約サイトまたは公式サイトでご確認ください。", 1),
        ('"text": "平日は¥6,000〜¥12,000、土日祝は¥12,000〜¥20,000が一般的な目安です（カート・食事別）。',
         f'"text": "じゃらんの総額で比べると、平日の最安の中央値は{yen(wk_med)}（半数のコースが{yen(wk_q[0])}〜{yen(wk_q[2])}）、土日祝は{yen(we_med)}（{yen(we_q[0])}〜{yen(we_q[2])}）でした（{len(ok)}コース・{CHECKED["ja"]}）。', 1),
    ]
    for old, new, cnt in reps:
        c = s.count(old)
        assert c == cnt, (old[:40], c, cnt)
        s = s.replace(old, new)

    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(b)
    out = s.replace("\n", nl)
    print(f"courses={n} (ok={len(ok)} official={sum(c['st']=='official' for c in data)} rakuten={sum(c['st']=='rakuten' for c in data)} none={sum(c['st']=='none' for c in data)})")
    print(f"weekday median {yen(wk_med)} IQR {yen(wk_q[0])}-{yen(wk_q[2])} / weekend median {yen(we_med)} IQR {yen(we_q[0])}-{yen(we_q[2])}")
    if out == src:
        print("[already]"); return
    if APPLY:
        for root in (REPO_ROOT, PREVIEW_ROOT):
            open(os.path.join(root, F), "w", encoding="utf-8", newline="").write(out)
    print("APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
