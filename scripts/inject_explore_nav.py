# -*- coding: utf-8 -*-
"""
inject_explore_nav.py
全 course-*.html の各言語コンテンツ末尾に「Explore More」逆流ナビゲーションを注入。
- エリアハブ5本(該当エリアをハイライト)
- ペルソナハブ4本
- ガイド3本(book-foreigner / sitemap-guide / recommend)

目的: 葉ノード(コースページ)からハブへのPageRank流入とUX回遊性向上。
冪等性: <!-- explore-nav --> マーカーで重複注入を防止。
"""

import sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")

# コース → エリア マッピング (35コース)
COURSE_TO_AREA = {
    # 福岡市エリア (8)
    'aburayama': 'fukuokacity', 'chikushigaoka': 'fukuokacity',
    'daihakata': 'fukuokacity', 'fukuokacc': 'fukuokacity',
    'hisayama': 'fukuokacity', 'koga': 'fukuokacity',
    'saitozaki': 'fukuokacity', 'sevenmillion': 'fukuokacity',
    # 糸島エリア (4)
    'ito': 'itoshima', 'keya': 'itoshima',
    'nijo': 'itoshima', 'queenshill': 'itoshima',
    # 北九州エリア (10)
    'fukuokakokusai': 'kitakyushu', 'genkai': 'kitakyushu',
    'kitakyushu': 'kitakyushu', 'kokura': 'kitakyushu',
    'kyushugc': 'kitakyushu', 'mission': 'kitakyushu',
    'moji': 'kitakyushu', 'moonlake': 'kitakyushu',
    'wakamatsu': 'kitakyushu', 'wakamiya': 'kitakyushu',
    # 筑後エリア (7+1)
    'ariake': 'chikugo', 'century': 'chikugo', 'chikushino': 'chikugo',
    'dazaifu': 'chikugo', 'kurume': 'chikugo',
    'ogori': 'chikugo', 'ukiha': 'chikugo',
    # 筑豊エリア (5+1=6, central は両エリアに登場するため chikuho に分類)
    'akane': 'chikuho', 'asoiizuka': 'chikuho', 'central': 'chikuho',
    'lakeside': 'chikuho', 'pheasant': 'chikuho', 'takaha': 'chikuho',
}

AREAS = [
    ('fukuokacity', {'ja': '福岡市エリア', 'en': 'Fukuoka City', 'ko': '후쿠오카시'}),
    ('itoshima',    {'ja': '糸島エリア',   'en': 'Itoshima',     'ko': '이토시마'}),
    ('kitakyushu',  {'ja': '北九州エリア', 'en': 'Kitakyushu',   'ko': '기타큐슈'}),
    ('chikugo',     {'ja': '筑後エリア',   'en': 'Chikugo',      'ko': '치쿠고'}),
    ('chikuho',     {'ja': '筑豊エリア',   'en': 'Chikuho',      'ko': '치쿠호'}),
]

PERSONAS = [
    ('beginner', '🔰', {'ja': '初心者向け',   'en': 'For Beginners',  'ko': '초보자'}),
    ('traveler', '✈️', {'ja': '旅行者向け',   'en': 'For Travelers',  'ko': '여행자'}),
    ('business', '💼', {'ja': '接待・コンペ', 'en': 'For Business',   'ko': '비즈니스'}),
    ('budget',   '💰', {'ja': '格安重視',     'en': 'Budget Picks',   'ko': '가성비'}),
]

GUIDES = [
    ('book-fukuoka-golf-foreigner.html', '🌏', {'ja': '海外からの予約方法', 'en': 'Booking Guide for Foreigners', 'ko': '해외 예약 가이드'}),
    ('sitemap-guide.html', '🗺',  {'ja': '全コース一覧', 'en': 'All Courses Sitemap', 'ko': '전체 코스 사이트맵'}),
    ('recommend.html', '⭐',     {'ja': '編集部おすすめ', 'en': 'Editor\'s Picks', 'ko': '편집부 추천'}),
]

SECTION_TITLES = {
    'ja': {'eyebrow': '— Explore More', 'title': '他のコース・ガイドも見る', 'area': '📍 エリアから探す', 'persona': '🎯 目的別に探す', 'guide': '📚 ガイド'},
    'en': {'eyebrow': '— Explore More', 'title': 'Browse Other Courses & Guides', 'area': '📍 By Area', 'persona': '🎯 By Purpose', 'guide': '📚 Guides'},
    'ko': {'eyebrow': '— Explore More', 'title': '다른 코스・가이드 보기', 'area': '📍 지역별', 'persona': '🎯 목적별', 'guide': '📚 가이드'},
}

# Pill ボタンスタイル
PILL_BASE = "display:inline-block;padding:9px 16px;background:#fff;border:1px solid #d5d0c5;border-radius:20px;font-size:13px;color:#1f3d2b;text-decoration:none;font-weight:600;line-height:1.2;"
PILL_HIGHLIGHT = "display:inline-block;padding:9px 16px;background:#e8732a;border:1px solid #c75d1c;border-radius:20px;font-size:13px;color:#fff;text-decoration:none;font-weight:700;line-height:1.2;"
LABEL_STYLE = "font-size:11px;font-weight:700;color:#888;letter-spacing:1.5px;margin-bottom:10px;text-transform:uppercase;"
GROUP_STYLE = "margin-bottom:20px;"
PILLS_WRAP = "display:flex;flex-wrap:wrap;gap:8px;"


def build_nav_section(course_slug: str, lang: str) -> str:
    """1言語分の Explore Nav セクションを生成"""
    current_area = COURSE_TO_AREA.get(course_slug, '')
    titles = SECTION_TITLES[lang]

    # エリア pills
    area_pills = []
    for slug, names in AREAS:
        style = PILL_HIGHLIGHT if slug == current_area else PILL_BASE
        area_pills.append(f'<a href="area-{slug}.html" style="{style}">{names[lang]}</a>')

    # ペルソナ pills
    persona_pills = []
    for slug, emoji, names in PERSONAS:
        persona_pills.append(f'<a href="hub-{slug}.html" style="{PILL_BASE}">{emoji} {names[lang]}</a>')

    # ガイド pills
    guide_pills = []
    for href, emoji, names in GUIDES:
        guide_pills.append(f'<a href="{href}" style="{PILL_BASE}">{emoji} {names[lang]}</a>')

    return f'''
  <!-- explore-nav -->
  <section class="related" style="background:#efece4;padding:48px 24px;">
    <div class="related-inner" style="max-width:880px;">
      <div class="sec-eyebrow" style="text-align:center;">{titles['eyebrow']}</div>
      <h2 class="sec-title" style="text-align:center;margin-bottom:28px;">{titles['title']}</h2>
      <div style="{GROUP_STYLE}">
        <div style="{LABEL_STYLE}">{titles['area']}</div>
        <div style="{PILLS_WRAP}">{''.join(area_pills)}</div>
      </div>
      <div style="{GROUP_STYLE}">
        <div style="{LABEL_STYLE}">{titles['persona']}</div>
        <div style="{PILLS_WRAP}">{''.join(persona_pills)}</div>
      </div>
      <div>
        <div style="{LABEL_STYLE}">{titles['guide']}</div>
        <div style="{PILLS_WRAP}">{''.join(guide_pills)}</div>
      </div>
    </div>
  </section>
'''


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    content = filepath.read_text(encoding='utf-8')

    # 既に注入済みなら skip (冪等性)
    if '<!-- explore-nav -->' in content:
        return {"file": filepath.name, "status": "already"}

    # course-{slug}.html から slug を抽出
    m = re.match(r'course-([a-z]+)\.html', filepath.name)
    if not m:
        return {"file": filepath.name, "status": "skip"}
    slug = m.group(1)

    if slug not in COURSE_TO_AREA:
        return {"file": filepath.name, "status": "no_area_mapping"}

    original = content
    inserted_count = 0
    for lang in ['ja', 'en', 'ko']:
        marker = f'</div><!-- /{lang} -->'
        if marker not in content:
            continue
        nav = build_nav_section(slug, lang)
        content = content.replace(marker, nav + marker, 1)
        inserted_count += 1

    if content == original:
        return {"file": filepath.name, "status": "no_marker"}

    if not dry_run:
        filepath.write_text(content, encoding='utf-8')

    return {"file": filepath.name, "status": "ok", "inserted": inserted_count, "area": COURSE_TO_AREA[slug]}


def main():
    dry_run = "--dry-run" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = a.split("=", 1)[1]

    print(f"[inject_explore_nav] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    if only:
        print(f"[inject_explore_nav] target only = {only}")
    print()

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob("course-*.html")):
            if only and fp.name != only:
                continue
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    print(f"{'file':<40} {'root':<12} {'status':<14} {'detail'}")
    print("=" * 90)
    for r in results:
        detail = ""
        if r.get('status') == 'ok':
            detail = f"langs={r.get('inserted')} area={r.get('area')}"
        print(f"{r.get('file',''):<40} {r.get('root',''):<12} {r.get('status',''):<14} {detail}")

    n_ok = sum(1 for r in results if r.get('status') == 'ok')
    n_already = sum(1 for r in results if r.get('status') == 'already')
    print()
    print(f"[summary] ok={n_ok}  already={n_already}  total={len(results)}")
    if dry_run:
        print("\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
