#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
トップページの SEO 改修 (2026-11-09)
  A. サイト内リンク href="index.html" → href="/" (canonical と一致させ評価を一本化) ※ルート直下の全 HTML
  B. トップのタイトル・説明文・H1 を検索語 (福岡 ゴルフ場 おすすめ/料金/比較) に合わせる
  C. 1 URL に同居していた 3 言語を分離: index.html=日本語 / en.html / ko.html (削除ではなく移設)
     hreflang を正しい相互参照に・言語切替はリンクに・英韓ページから日本語の FAQ 構造化データを外す
冪等 (分離済みならスキップ)。改行コードはファイルのものに合わせる。GA4 タグはそのまま。
Usage: python scripts/split_home_lang_2026_11.py [--apply] [--preview-only]
"""
import glob, json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [PREVIEW] if "--preview-only" in sys.argv else [REPO, PREVIEW]
APPLY = "--apply" in sys.argv
SITE = "https://fukuoka-golf-guide.com/"

META = {
    "ja": dict(
        title="福岡のゴルフ場おすすめ50コース｜料金・エリア・アクセスで比較【2026年版】",
        desc="福岡県のゴルフ場50コースを料金・エリア・アクセスで比較。名門・コスパ・初心者向けのランキング、3ステップの選び方、よくある質問まで。地元目線の独立系ガイド。",
        og_title="福岡のゴルフ場おすすめ50コース｜料金・エリア・アクセスで比較",
        og_desc="福岡県のゴルフ場50コースを料金・エリア・アクセスで比較。ランキング・選び方・FAQつきの独立系ガイド。",
        locale="ja_JP", url=SITE),
    "en": dict(
        title="Fukuoka Golf Course Guide | Compare 50 Courses by Fee, Area & Access",
        desc="Compare all 50 golf courses in Fukuoka, Japan by green fee, area and access from Fukuoka Airport. Rankings, a 3-step course finder and tips for visiting golfers.",
        og_title="Fukuoka Golf Course Guide | Compare 50 Courses",
        og_desc="Compare all 50 golf courses in Fukuoka by green fee, area and access. Rankings and tips for visiting golfers.",
        locale="en_US", url=SITE + "en.html"),
    "ko": dict(
        title="후쿠오카 골프장 가이드 | 50개 코스 요금·지역·교통 비교",
        desc="후쿠오카 골프장 50개 코스를 요금·지역·후쿠오카 공항에서의 교통으로 비교. 랭킹, 3단계 코스 찾기, 여행 골퍼를 위한 안내.",
        og_title="후쿠오카 골프장 가이드 | 50개 코스 비교",
        og_desc="후쿠오카 골프장 50개 코스를 요금·지역·교통으로 비교하는 독립 가이드.",
        locale="ko_KR", url=SITE + "ko.html"),
}
FILE = {"ja": "index.html", "en": "en.html", "ko": "ko.html"}
H1_OLD = "<h1>福岡ゴルフ場ガイド<br>50コースを地元目線で完全網羅</h1>"
H1_NEW = "<h1>福岡のゴルフ場<br>おすすめ50コース<br>料金・エリアで比較</h1>"
SUB_OLD = "50コースの料金・アクセス・設備を、日本語・English・한국어で比較できる独立系ガイド。"
SUB_NEW = "50コースの料金・アクセス・設備を比較できる、地元目線の独立系ガイド。"
PRIVACY = {"ja": "プライバシーポリシー", "en": "Privacy Policy", "ko": "개인정보 처리방침"}


def fix_links(s):
    """A: href="index.html" → href="/" (アンカー付きも)"""
    s, n1 = re.subn(r'href="index\.html"', 'href="/"', s)
    s, n2 = re.subn(r'href="index\.html#', 'href="/#', s)
    return s, n1 + n2


def head_for(head, lang, nl):
    m = META[lang]
    head = re.sub(r'<html lang="[a-z]+">', f'<html lang="{lang}">', head, count=1)
    head = re.sub(r"<title>.*?</title>", f"<title>{m['title']}</title>", head, count=1, flags=re.S)
    head = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{m["desc"]}">', head, count=1)
    head = re.sub(r'<link rel="canonical" href="[^"]*" ?/?>', f'<link rel="canonical" href="{m["url"]}" />', head, count=1)
    alt = nl.join([f'<link rel="alternate" hreflang="{l}" href="{META[l]["url"]}">' for l in ("ja", "en", "ko")]
                  + [f'<link rel="alternate" hreflang="x-default" href="{SITE}">'])
    head = re.sub(r'(<link rel="alternate" hreflang="[^"]+" href="[^"]*">\r?\n)+', alt + nl, head, count=1)
    head = re.sub(r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{m["locale"]}">', head, count=1)
    head = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{m["og_title"]}">', head, count=1)
    head = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{m["og_desc"]}">', head, count=1)
    if '<meta property="og:url"' not in head:
        head = head.replace('<meta property="og:type" content="website">', f'<meta property="og:type" content="website">{nl}<meta property="og:url" content="{m["url"]}">', 1)
    else:
        head = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{m["url"]}">', head, count=1)
    # 言語切替をリンクにするための CSS
    head = head.replace("  .lang-switch button{", "  .lang-switch .lbtn{text-decoration:none;display:inline-block;", 1)
    head = head.replace("  .lang-switch button.on{", "  .lang-switch .lbtn.on{", 1)
    if lang != "ja":
        # 日本語の FAQ 構造化データは英韓ページに載せない
        head = re.sub(r"<!-- FAQPage JSON-LD -->\r?\n<script type=\"application/ld\+json\">.*?</script>\r?\n", "", head, count=1, flags=re.S)
    return head


def nav_for(lang, nl):
    a = [f'  <a class="lbtn{" on" if l == lang else ""}" href="{"/" if l == "ja" else FILE[l]}" hreflang="{l}" lang="{l}">{l.upper()}</a>' for l in ("ja", "en", "ko")]
    return nl.join(['<nav class="lang-switch">'] + a + ["</nav>"])


def split(src, nl):
    i_nav = src.index("<!-- Language Switch -->")
    j_nav = src.index("</nav>", i_nav) + len("</nav>")
    marks = {l: src.index(f"<!-- ============ {l.upper()} ============ -->") for l in ("ja", "en", "ko")}
    ends = {l: src.index(f"</div><!-- /{l} -->") + len(f"</div><!-- /{l} -->") for l in ("ja", "en", "ko")}
    head, post = src[:i_nav], src[ends["ko"]:]
    out = {}
    for l in ("ja", "en", "ko"):
        blk = src[marks[l]:ends[l]]
        blk = blk.replace(f'id="c-{l}" class="content"', f'id="c-{l}" class="content on"', 1).replace('class="content on on"', 'class="content on"')
        if "privacy-link-v1" not in blk:
            k = blk.rfind("</footer>")
            blk = blk[:k] + f'  <!-- privacy-link-v1 --><div style="margin-top:6px;"><small><a href="privacy.html">{PRIVACY[l]}</a></small></div>{nl}  ' + blk[k:]
        elif l == "ko":
            blk = blk.replace('<a href="privacy.html">プライバシーポリシー</a>', f'<a href="privacy.html">{PRIVACY["ko"]}</a>')
        if l == "ja":
            blk = blk.replace(H1_OLD, H1_NEW, 1).replace(SUB_OLD, SUB_NEW, 1)
        else:
            blk = blk.replace('href="/"', f'href="{FILE[l]}"').replace('href="/#', f'href="{FILE[l]}#')
        out[FILE[l]] = head_for(head, l, nl) + "<!-- Language Switch -->" + nl + nav_for(l, nl) + nl + nl + blk + post
    return out


for root in ROOTS:
    print(root)
    # A: ルート直下の全 HTML (index.html は C で処理するので後で上書き)
    changed = {}
    total = 0
    for p in sorted(glob.glob(os.path.join(root, "*.html"))):
        s = open(p, encoding="utf-8", newline="").read()
        new, n = fix_links(s)
        if n:
            changed[os.path.basename(p)] = new
            total += n
    print(f"  A: リンク置換 {total} 本 / {len(changed)} ファイル")
    # C (+B)
    ip = os.path.join(root, "index.html")
    src = changed.get("index.html") or open(ip, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in src else "\n"
    if 'id="c-en"' in src:
        out = split(src, nl)
        changed.update(out)
        for f, s in out.items():
            for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
                json.loads(m.group(1))
            assert s.count("G-PENH0Z4VT7") >= 2, f
            other = [x for x in ("c-ja", "c-en", "c-ko") if f'id="{x}"' in s]
            assert len(other) == 1, (f, other)
            if nl == "\r\n":
                assert s.count("\n") == s.count("\r\n"), f + " EOL"
            txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>|<style.*?</style>", "", s, flags=re.S)))
            t = re.search(r"<title>(.*?)</title>", s).group(1)
            print(f"  C: {f}: {len(s):,} bytes / 本文 {len(txt):,} 字 / title={t}")
    else:
        print("  C: 分離済み (スキップ)")
    for f, s in changed.items():
        p = os.path.join(root, f)
        if os.path.exists(p) and open(p, encoding="utf-8", newline="").read() == s:
            continue
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(s)
    left = sum(len(re.findall(r'href="index\.html', s)) for s in changed.values())
    print(f"  残り index.html リンク(変更ファイル内): {left}")
print("APPLIED" if APPLY else "DRY-RUN")
