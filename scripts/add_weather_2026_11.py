#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースページ (日本語) に気象庁の天気予報欄を入れる (2026-11)。表示は weather-jma.js が行う。
  所在地の市町村 → 気象庁の一次細分区域 (福岡地方/北九州地方/筑豊地方/筑後地方) は気象庁 area.json の区分による。
  気温の地点: 福岡地方=福岡 / 北九州地方=八幡 / 筑豊地方=飯塚 / 筑後地方=久留米 (予報 JSON に含まれる地点)
  入れる位置: 日本語ブロックのアクセス欄 (— Getting Here) の直後。
冪等 (MARKER)。改行コードはそのまま。
Usage: python scripts/add_weather_2026_11.py [--apply] [--only course-wakamatsu.html ...]
"""
import glob, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1:] if "--only" in sys.argv else None
MARK = "<!-- jma-weather-v1 -->"

AREAS = {  # 気象庁 area.json (class10s → class20s) より
    "400010": ("福岡地方", "82182", "福岡", ["福岡市", "筑紫野市", "春日市", "大野城市", "宗像市", "太宰府市", "古賀市", "福津市", "糸島市", "那珂川市", "宇美町", "篠栗町", "志免町", "須恵町", "新宮町", "久山町", "粕屋町"]),
    "400020": ("北九州地方", "82056", "八幡", ["北九州市", "中間市", "芦屋町", "水巻町", "岡垣町", "遠賀町", "行橋市", "豊前市", "苅田町", "みやこ町", "吉富町", "上毛町", "築上町"]),
    "400030": ("筑豊地方", "82136", "飯塚", ["直方市", "飯塚市", "田川市", "宮若市", "嘉麻市", "小竹町", "鞍手町", "桂川町", "香春町", "添田町", "糸田町", "川崎町", "大任町", "赤村", "福智町"]),
    "400040": ("筑後地方", "82306", "久留米", ["久留米市", "小郡市", "うきは市", "朝倉市", "筑前町", "東峰村", "大刀洗町", "大牟田市", "柳川市", "八女市", "筑後市", "大川市", "みやま市", "大木町", "広川町"]),
}

CSS = """  <style>
    .jma-weather{max-width:880px;margin-top:8px;}
    .jw-days{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;}
    .jw-day{background:#fff;border:1px solid var(--line,#e5e0d5);border-radius:14px;padding:16px 18px;}
    .jw-date{font-weight:700;color:var(--forest,#1a5c38);font-size:14px;margin-bottom:6px;}
    .jw-main{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
    .jw-text{font-size:14px;line-height:1.5;}
    .jw-temp{font-size:15px;margin-bottom:6px;} .jw-hi{color:#c0392b;font-weight:700;} .jw-lo{color:#2563a8;font-weight:700;}
    .jw-temp small{color:var(--muted,#777);font-size:11px;}
    .jw-pop{font-size:12px;color:#444;display:flex;flex-wrap:wrap;gap:4px 10px;margin-bottom:6px;} .jw-pop b{color:#2563a8;}
    .jw-wind{font-size:12px;color:var(--muted,#777);line-height:1.5;}
    .jw-week-head{font-weight:700;font-size:13px;color:var(--forest,#1a5c38);margin:18px 0 8px;}
    .jw-week{display:grid;grid-template-columns:repeat(auto-fit,minmax(92px,1fr));gap:8px;}
    .jw-w{background:#fff;border:1px solid var(--line,#e5e0d5);border-radius:10px;padding:8px 6px;text-align:center;font-size:12px;}
    .jw-w .jw-date{font-size:12px;margin-bottom:2px;} .jw-wtext{font-size:11px;color:#444;min-height:2.6em;} .jw-wpop{color:#2563a8;font-weight:700;}
    .jw-src{font-size:11px;color:var(--muted,#777);margin-top:12px;line-height:1.6;}
    .jw-loading{font-size:13px;color:var(--muted,#777);}
  </style>"""


def city_of(s):
    m = re.search(r'"addressLocality"\s*:\s*"([^"]+)"', s)
    loc = m.group(1) if m else ""
    m2 = re.search(r'<div class="contact-label">Address</div><div class="contact-value">([^<]+)</div>', s)
    txt = loc + " " + (m2.group(1) if m2 else "")
    for code, (_, _, _, cities) in AREAS.items():
        for c in cities:
            if c in txt:
                return code, c
    # 郡名つきの表記 (例: 遠賀郡岡垣町) に対応
    for code, (_, _, _, cities) in AREAS.items():
        for c in cities:
            if c[:-1] in txt and c.endswith(("町", "村")):
                return code, c
    return None, txt.strip()


def course_name(s):
    m = re.search(r'<h1 class="hero-title">(.*?)</h1>', s, re.S)
    return re.sub(r"<[^>]+>", "", m.group(1)).split("旧")[0].strip() if m else ""


def block(code, name):
    an, city, cn, _ = AREAS[code]
    return f"""
  {MARK}
  <section class="section" id="weather">
    <div class="sec-eyebrow">— Weather</div>
    <h2 class="sec-title">{name}周辺の天気予報</h2>
    <p class="sec-desc">気象庁が発表する{an}の予報を、今日・明日と週間で表示します。</p>
{CSS}
    <div class="jma-weather" data-area="{code}" data-area-name="{an}" data-city="{city}" data-city-name="{cn}">
      <p class="jw-loading">予報を読み込んでいます…</p>
      <p class="jw-fallback" style="display:none;">予報を読み込めませんでした。<a href="https://www.jma.go.jp/bosai/forecast/#area_type=class10s&amp;area_code={code}" target="_blank" rel="noopener">気象庁の{an}の天気予報</a>をご覧ください。</p>
    </div>
  </section>
  <script src="weather-jma.js" defer></script>
"""


for root in ROOTS:
    print(root)
    files = ONLY or sorted(os.path.basename(p) for p in glob.glob(os.path.join(root, "course-*.html")))
    stats = {"added": 0, "already": 0, "no_area": [], "no_anchor": []}
    for f in files:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if MARK in s:
            stats["already"] += 1; continue
        code, c = city_of(s)
        if not code:
            stats["no_area"].append((f, c)); continue
        nl = "\r\n" if "\r\n" in s else "\n"
        w = s.replace("\r\n", "\n")
        i = w.find('id="c-ja"')
        j = min([x for x in (w.find('id="c-en"', i + 1), w.find('id="c-ko"', i + 1), len(w)) if x > i])
        blk = w[i:j]
        k = blk.find('<div class="sec-eyebrow">— Getting Here</div>')
        if k < 0:
            stats["no_anchor"].append(f); continue
        e = blk.find("</section>", k) + len("</section>")
        blk = blk[:e] + "\n" + block(code, course_name(w)) + blk[e:]
        new = (w[:i] + blk + w[j:]).replace("\n", nl)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {f}: {c} → {AREAS[code][0]}（気温 {AREAS[code][2]}）")
        stats["added"] += 1
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
    print("  ", stats)
print("APPLIED" if APPLY else "DRY-RUN")
