# -*- coding: utf-8 -*-
"""B群残ページに SERPサムネ用の実<img>を付与。
- hero-bg色グラデhero → 写真in-hero(hex→半透明rgba・LP同型)
- それ以外(page-header/hero section/simple) → 最初の</header>or</section>直後にリード画像挿入
冪等(<img>済skip)・両ROOT・--dry-run。"""
import re, os, sys

REPO = "C:/Users/Owner/fukuoka-golf-guide"; PREVIEW = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO, PREVIEW]; DRY = "--dry-run" in sys.argv

CFG = {  # file: (photo, alt)
    "faq.html": ("images/itoshimatorii.webp", "福岡ゴルフのよくある質問"),
    "rules-japan.html": ("images/itoshimatorii.webp", "日本・福岡のゴルフ場のマナーとルール"),
    "recommend.html": ("images/golf-mountain.webp", "福岡のおすすめゴルフ場"),
    "guide-index.html": ("images/fukuoka-overview.webp", "福岡ゴルフ場ガイド 目的別まとめ"),
    "golf-wear.html": ("images/golf-mountain.webp", "ゴルフウェア・必須アイテムガイド"),
    "book-wakamiya-ko.html": ("images/spring-forest.webp", "와카미야 골프장 예약 가이드"),
    "rental-and-transport.html": ("images/fukuoka-bay.webp", "福岡のゴルフ レンタル・送迎ガイド"),
    "report-index.html": ("images/IMG_1281-EDIT.webp", "福岡ゴルフ場 編集部レポート一覧"),
    "report-kokura.html": ("images/IMG_1281-EDIT.webp", "小倉カンツリー倶楽部 編集部レポート"),
    "report-lakeside.html": ("images/itoshima-bay.webp", "福岡レイクサイドCC 編集部レポート"),
    "report-mission.html": ("images/fukuoka-overview.webp", "ミッションバレーGC 編集部レポート"),
    "access-genkai.html": ("images/itoshima-sea.webp", "玄海ゴルフクラブへのアクセス"),
    "access-wakamatsu.html": ("images/IMG_1281-EDIT.webp", "若松ゴルフ倶楽部へのアクセス"),
    "access.html": ("images/itoshimatorii.webp", "福岡のゴルフ場へのアクセス総合ガイド"),
    "beginner-cards.html": ("images/spring-forest.webp", "初心者向け福岡ゴルフガイド"),
}

LEAD_CSS = "<style>.page-lead{margin:0;line-height:0;}.page-lead img{width:100%;max-height:340px;object-fit:cover;display:block;}</style>\n</head>"
ALPHAS = [0.75, 0.62, 0.55, 0.82]
PHOTO_CSS = (".hero-photo{position:absolute;inset:0;z-index:0;width:100%;height:100%;object-fit:cover;object-position:center;}\n    ")

def hex2rgba(h, a):
    h = h.lstrip("#"); return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"

def as_lp(html, photo, alt):
    m = re.search(r'(\.hero-bg\s*\{[^}]*background:\s*linear-gradient\()([^)]*)(\)[^}]*\})', html)
    if not m or '<div class="hero-bg"></div>' not in html:
        return None
    parts = [p.strip() for p in m.group(2).split(",")]
    angle, stops = parts[0], parts[1:]
    ns = []
    for i, st in enumerate(stops):
        sm = re.match(r'(#[0-9A-Fa-f]{6})\s+(.*)', st)
        if not sm: return None
        ns.append(f"{hex2rgba(sm.group(1), ALPHAS[i] if i < len(ALPHAS) else 0.7)} {sm.group(2)}")
    newbg = PHOTO_CSS + m.group(1).replace(".hero-bg {", ".hero-bg { z-index:1;", 1) + angle + ", " + ", ".join(ns) + m.group(3)
    html = html[:m.start()] + newbg + html[m.end():]
    html = re.sub(r'(\.hero-overlay\s*\{)', r'\1 z-index:2;', html, count=1)
    html = re.sub(r'(\.hero-inner\s*\{)', r'\1 z-index:3;', html, count=1)
    img = f'<img class="hero-photo" src="{photo}" alt="{alt}" fetchpriority="high">\n    '
    return html.replace('<div class="hero-bg"></div>', img + '<div class="hero-bg"></div>', 1)

def as_lead(html, photo, alt):
    fig = f'<figure class="page-lead"><img src="{photo}" alt="{alt}" loading="lazy"></figure>\n'
    if "</head>" in html and ".page-lead" not in html:
        html = html.replace("</head>", LEAD_CSS, 1)
    for anchor in ["</header>", "</section>"]:
        i = html.find(anchor)
        if i != -1:
            j = i + len(anchor)
            return html[:j] + "\n" + fig + html[j:]
    m = re.search(r'<body[^>]*>', html)
    if m:
        return html[:m.end()] + "\n" + fig + html[m.end():]
    return None

def main():
    print(f"モード: {'DRY-RUN' if DRY else '本番'}\n"); ok = 0
    for name, (photo, alt) in CFG.items():
        html = open(os.path.join(REPO, name), encoding="utf-8").read()
        if "<img" in html:
            print(f"  [{name}] skip(既に<img>)"); continue
        new = as_lp(html, photo, alt)
        how = "photo-in-hero"
        if new is None:
            new = as_lead(html, photo, alt); how = "lead-image"
        if new is None:
            print(f"  [{name}] skip(挿入点なし)"); continue
        ok += 1
        print(f"  [変換] {name:26} {how:14} img={photo}")
        if not DRY:
            for root in ROOTS:
                p = os.path.join(root, name)
                if os.path.exists(p): open(p, "w", encoding="utf-8").write(new)
    print(f"\n=== {ok}/{len(CFG)} ===" + ("  (DRY-RUN)" if DRY else ""))

if __name__ == "__main__":
    main()
