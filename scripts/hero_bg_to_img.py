# -*- coding: utf-8 -*-
"""SERPサムネイル対策: hero の CSS背景画像を実<img>化 (A型=.hero-img{...url...}+<div class="hero-img">)。
グラデ overlay は残し z-index でデザイン維持 (hub-business `74cf0c5` と同型)。
冪等(hero-photo 済ならskip)・両ROOT・--dry-run。C型(index)/D型(別hero)は対象外。"""
import re, os, sys, glob

REPO = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO, PREVIEW]
DRY = "--dry-run" in sys.argv
ONLY = [a for a in sys.argv[1:] if not a.startswith("--")]  # 任意: 対象ファイルを限定

CSS_RE = re.compile(r"(\.hero-img\s*\{)(.*?)(\})", re.S)
URL_RE = re.compile(r"url\((['\"]?)([^)'\"]+)\1\)")
DIV_RE = "<div class=\"hero-img\"></div>"
H1_RE = re.compile(r'<h1 class="hero-title">(.*?)</h1>', re.S)

PHOTO_CSS = (".hero-photo{position:absolute;inset:0;z-index:0;width:100%;height:100%;"
             "object-fit:cover;object-position:center;}\n"
             "    .hero-inner{z-index:2;}\n    ")


def alt_of(html):
    m = H1_RE.search(html)
    if not m:
        return "福岡のゴルフ場"
    t = re.sub(r"<[^>]+>", "", m.group(1))
    t = re.sub(r"\s+", "", t).strip()
    return (t or "福岡のゴルフ場") + "のコース風景"


def transform(html):
    if "hero-photo" in html or "<img" in html:
        return None, "skip(既に<img>あり)"
    if DIV_RE not in html:
        return None, "skip(hero-img div無し)"
    cm = CSS_RE.search(html)
    if not cm:
        return None, "skip(.hero-img CSS無し)"
    um = URL_RE.search(cm.group(2))
    if not um:
        return None, "skip(hero url無し)"
    path = um.group(2)
    alt = alt_of(html)

    # 1) .hero-img CSS: ", url(...)" を除去し z-index:1・前に .hero-photo/.hero-inner を注入
    def css_repl(m):
        props = re.sub(r",\s*url\([^)]*\)", "", m.group(2)).rstrip()
        return PHOTO_CSS + m.group(1) + props + " z-index:1; " + m.group(3)
    html = CSS_RE.sub(css_repl, html, count=1)

    # 2) body: <div class="hero-img"> の前に実<img>を挿入 (全言語ブロック)
    img = ('<img class="hero-photo" src="' + path + '" alt="' + alt +
           '" fetchpriority="high">\n    ')
    html = html.replace(DIV_RE, img + DIV_RE)
    return html, f"OK img={path} alt={alt}"


def main():
    files = sorted(glob.glob(os.path.join(REPO, "*.html")))
    if ONLY:
        files = [os.path.join(REPO, f) for f in ONLY]
    n_ok = 0; n_skip = 0
    print(f"モード: {'DRY-RUN' if DRY else '本番'}  対象走査 {len(files)} ファイル\n")
    for src in files:
        name = os.path.basename(src)
        html = open(src, encoding="utf-8").read()
        new, msg = transform(html)
        if new is None:
            n_skip += 1
            continue
        n_ok += 1
        print(f"  [変換] {name:32} {msg}")
        if not DRY:
            for root in ROOTS:
                p = os.path.join(root, name)
                if os.path.exists(p):
                    open(p, "w", encoding="utf-8").write(new)
    print(f"\n=== SUMMARY === 変換 {n_ok} / skip {n_skip}")
    if DRY:
        print("※ DRY-RUN。本番は --dry-run を外す。")


if __name__ == "__main__":
    main()
