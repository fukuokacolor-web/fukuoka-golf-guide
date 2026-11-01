#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
access.html を「50コースのアクセスページ一覧」に作り直す。

旧 access.html はトップの「アクセスインデックス」や FAQ の「全28コースのアクセス」から
リンクされているのに、中身は福岡レイクサイドCC 1コースだけの案内だった (2026-11-01 確認)。
- 名前・所在地: 各 course-*.html の JSON-LD / hero-title (JA/EN/KO)。所在地の英韓表記は
  rebuild_fees_table_2026_10.py の AREA を流用
- リンク先: access-{slug}.html (50件・各ページに地図とナビアプリのボタンあり)
- 地域区分は市町村からの機械的な割り当て (REGION)
冪等: 生成結果が同じなら no-op。
Usage:
  python scripts/rebuild_access_index_2026_11.py            # dry-run
  python scripts/rebuild_access_index_2026_11.py --apply    # REPO + PREVIEW
"""
import re, os, sys, json, glob, importlib.util

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv
F = "access.html"

spec = importlib.util.spec_from_file_location("fees", os.path.join(REPO_ROOT, "scripts/rebuild_fees_table_2026_10.py"))
fees = importlib.util.module_from_spec(spec)
sys.argv, _argv = ["x"], sys.argv
spec.loader.exec_module(fees)
sys.argv = _argv

REGIONS = [  # (JA, EN, KO, 市町村)
    ("福岡市・近郊", "Fukuoka City & nearby", "후쿠오카시·근교",
     {"福岡市城南区", "福岡市東区", "福岡市早良区", "糟屋郡久山町", "古賀市", "那珂川市", "太宰府市"}),
    ("糸島", "Itoshima", "이토시마", {"糸島市"}),
    ("宗像・北九州・遠賀・京築", "Munakata, Kitakyushu & east", "무나카타·기타큐슈·동부",
     {"宗像市", "北九州市", "北九州市若松区", "北九州市八幡西区", "北九州市門司区", "遠賀郡遠賀町", "築上郡築上町"}),
    ("筑豊（飯塚・田川・直方・鞍手・宮若）", "Chikuho (Iizuka, Tagawa, Nogata…)", "지쿠호 (이이즈카·다가와 등)",
     {"飯塚市", "田川郡", "直方市", "鞍手郡小竹町", "鞍手郡鞍手町", "宮若市"}),
    ("筑紫・朝倉・筑後", "Chikushi, Asakura & Chikugo", "지쿠시·아사쿠라·지쿠고",
     {"筑紫野市", "朝倉市", "朝倉郡筑前町", "小郡市", "八女郡広川町", "八女市", "うきは市", "大牟田市", "みやま市"}),
]
TEXT = {
    "ja": {"head": "📍 コース別アクセス（{n}コース）",
           "intro": "{n}コースそれぞれのアクセスページに、所在地・車でのルート・地図、Google マップや Naver Map などで開くボタンをまとめています。コース名を選んでください。最新の情報は各ゴルフ場の公式サイトでご確認ください。",
           "cta": "アクセス →"},
    "en": {"head": "📍 Directions by Course ({n} courses)",
           "intro": "Each of the {n} course pages has the address, driving route, a map and buttons to open Google Maps, Naver Map and more. Pick a course below. Always confirm the latest details on the course's official website.",
           "cta": "Directions →"},
    "ko": {"head": "📍 코스별 오시는 길 ({n}개 코스)",
           "intro": "{n}개 코스의 각 페이지에 주소·차량 루트·지도와 Google 지도, 네이버 지도 등으로 여는 버튼을 정리했습니다. 코스를 선택하세요. 최신 정보는 각 골프장 공식 사이트에서 확인해 주세요.",
           "cta": "오시는 길 →"},
}
CSS = ('  .acc-region { font-size:0.8rem; font-weight:800; color:var(--muted,#6b7280); margin:18px 2px 8px; }\n'
       '  .acc-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:8px; }\n'
       '  .acc-item { display:flex; justify-content:space-between; align-items:center; gap:8px; background:#fff; border:1px solid #e3e6df;'
       ' border-radius:10px; padding:10px 12px; text-decoration:none; color:inherit; }\n'
       '  .acc-item:hover { border-color:#2d6a4f; }\n'
       '  .acc-name { font-weight:700; font-size:0.86rem; line-height:1.35; }\n'
       '  .acc-name small { display:block; font-weight:400; font-size:0.72rem; color:var(--muted,#6b7280); margin-top:2px; }\n'
       '  .acc-cta { font-size:0.72rem; font-weight:700; color:#2d6a4f; white-space:nowrap; }\n')


def block(lang, data):
    k = {"ja": 0, "en": 1, "ko": 2}[lang]
    n = len(data)
    out = [f'  <div class="sec-head">{TEXT[lang]["head"].format(n=n)}</div>',
           f'  <p style="font-size:0.84rem;line-height:1.7;color:#444;margin:0 2px 6px;">{TEXT[lang]["intro"].format(n=n)}</p>']
    seen = set()
    for reg in REGIONS:
        items = sorted([c for c in data if c["area_ja"] in reg[3]], key=lambda c: (c["area_ja"], c[lang]))
        if not items:
            continue
        out.append(f'  <div class="acc-region">{reg[k]}</div>')
        out.append('  <div class="acc-grid">')
        for c in items:
            seen.add(c["key"])
            out.append(f'    <a class="acc-item" href="access-{c["key"]}.html"><span class="acc-name">{c[lang]}'
                       f'<small>{c["area_" + lang]}</small></span><span class="acc-cta">{TEXT[lang]["cta"]}</span></a>')
        out.append('  </div>')
    missing = [c["key"] for c in data if c["key"] not in seen]
    assert not missing, ("地域未割り当て", missing)
    return "\n".join(out) + "\n"


def main():
    src = open(os.path.join(REPO_ROOT, F), encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    s = src.replace("\r\n", "\n")
    data = fees.courses()
    n = len(data)
    for lang in ("ja", "en", "ko"):
        m = re.search(rf'(<div id="c-{lang}" class="content[^"]*">\n)(.*?)(\n</div>\n)', s, re.S)
        assert m, lang
        s = s[:m.start(2)] + "\n" + block(lang, data) + s[m.end(2):]
    if ".acc-grid" not in s:
        s = s.replace("  </style>", CSS + "  </style>", 1)
    meta = [
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="福岡のゴルフ場{n}コースのアクセス案内の一覧。各コースの所在地・車でのルート・地図のページへ。">'),
        (r'<meta name="description" lang="en" content="[^"]*">', f'<meta name="description" lang="en" content="Directions to {n} golf courses in Fukuoka. Links to each course page with address, driving route and maps.">'),
        (r'<meta name="description" lang="ko" content="[^"]*">', f'<meta name="description" lang="ko" content="후쿠오카 골프장 {n}개 코스의 오시는 길 안내 목록. 각 코스의 주소·차량 루트·지도 페이지로 이동합니다.">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="福岡のゴルフ場{n}コースのアクセス案内の一覧。各コースの所在地・車でのルート・地図のページへ。">'),
        (r"<title>アクセスガイド \| 福岡ゴルフ場ガイド</title>", f"<title>福岡ゴルフ場{n}コースのアクセス一覧 | 福岡ゴルフ場ガイド</title>"),
        (r'<meta property="og:title"( *)content="アクセスガイド \| 福岡ゴルフ場ガイド">', rf'<meta property="og:title"\1content="福岡ゴルフ場{n}コースのアクセス一覧 | 福岡ゴルフ場ガイド">'),
    ]
    for pat, rep in meta:
        s, k = re.subn(pat, rep, s, count=1)
        assert k == 1 or re.sub(r"\\\d", "", rep).split("content=")[-1][:12] in s, pat  # 2回目以降は置換済みで一致0
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        json.loads(b)
    out = s.replace("\n", nl)
    links = re.findall(r'href="access-([a-z-]+)\.html"', out)
    bad = [x for x in set(links) if not os.path.exists(os.path.join(REPO_ROOT, f"access-{x}.html"))]
    print(f"courses={n} links={len(links)} (3言語) 存在しないリンク={bad}")
    print("残るレイクサイド固有語:", out.count("新飯塚駅"), out.count("椋本611"))
    if out == src:
        print("[already]"); return
    if APPLY:
        for root in (REPO_ROOT, PREVIEW_ROOT):
            open(os.path.join(root, F), "w", encoding="utf-8", newline="").write(out)
    print("APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
