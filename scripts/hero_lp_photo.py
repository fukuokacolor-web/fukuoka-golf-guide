# -*- coding: utf-8 -*-
"""book-LP(画像なし緑/色グラデhero)に写真ヒーローを追加 (SERPサムネ対策)。
各LPのテーマ色グラデを hex→半透明rgba 化して写真を透かす(ブランド色は維持)。
onsen `(pilot)` と同型。冪等・両ROOT・--dry-run。"""
import re, os, sys

REPO = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW = "C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO, PREVIEW]
DRY = "--dry-run" in sys.argv

# LP → 話題に合う既存写真 + alt
CFG = {
    "book-fukuoka-afternoon.html": ("images/golf-mountain.webp", "福岡の午後スルー対応ゴルフ場の風景"),
    "book-fukuoka-business.html":  ("images/IMG_1281-EDIT.webp",  "福岡の接待・名門ゴルフ場の風景"),
    "book-fukuoka-traveler.html":  ("images/keya-waves.webp",     "福岡の観光と楽しむ絶景ゴルフ場"),
    "book-fukuoka-beginner.html":  ("images/spring-forest.webp",  "福岡の初心者向けゴルフ場の風景"),
    "book-fukuoka-27holes.html":   ("images/fukuoka-overview.webp","福岡の27ホールゴルフ場の風景"),
    "book-fukuoka-access.html":    ("images/fukuoka-bay.webp",     "福岡市街から近いゴルフ場の風景"),
}

ALPHAS = [0.75, 0.62, 0.55, 0.82]  # 4stop想定(中間を薄く=写真を見せ、上下を濃く=白文字可読)
PHOTO_CSS = (".hero-photo{position:absolute;inset:0;z-index:0;width:100%;height:100%;"
             "object-fit:cover;object-position:center;}\n    ")

def hex2rgba(h, a):
    h = h.lstrip("#")
    return f"rgba({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)},{a})"

def transform(html):
    if "hero-photo" in html or "<img" in html:
        return None, "skip(既に<img>)"
    if '<div class="hero-bg"></div>' not in html:
        return None, "skip(hero-bg div無し)"
    m = re.search(r'(\.hero-bg\s*\{[^}]*background:\s*linear-gradient\()([^)]*)(\)[^}]*\})', html)
    if not m:
        return None, "skip(hero-bg gradient無し)"
    inner = m.group(2)  # "<angle>, #hex pos, #hex pos, ..."
    parts = [p.strip() for p in inner.split(",")]
    angle = parts[0]
    stops = parts[1:]
    new_stops = []
    for i, st in enumerate(stops):
        sm = re.match(r'(#[0-9A-Fa-f]{6})\s+(.*)', st)
        if not sm:
            return None, f"skip(stop解析不可: {st})"
        a = ALPHAS[i] if i < len(ALPHAS) else 0.7
        new_stops.append(f"{hex2rgba(sm.group(1), a)} {sm.group(2)}")
    new_grad = angle + ", " + ", ".join(new_stops)
    # .hero-bg 書換 + z-index:1 + 前に .hero-photo 注入
    hero_bg_new = PHOTO_CSS + m.group(1).replace(".hero-bg {", ".hero-bg { z-index:1;", 1) + new_grad + m.group(3)
    # m.group(1) は ".hero-bg { ... background: linear-gradient(" なので z-index を { 直後に
    hero_bg_new = hero_bg_new.replace("linear-gradient(", "linear-gradient(", 1)  # no-op安全
    html = html[:m.start()] + hero_bg_new + html[m.end():]
    # overlay / inner に z-index
    html = re.sub(r'(\.hero-overlay\s*\{)', r'\1 z-index:2;', html, count=1)
    html = re.sub(r'(\.hero-inner\s*\{)', r'\1 z-index:3;', html, count=1)
    return html, "OK"

def main():
    print(f"モード: {'DRY-RUN' if DRY else '本番'}\n")
    ok = 0
    for name, (photo, alt) in CFG.items():
        src = os.path.join(REPO, name)
        html = open(src, encoding="utf-8").read()
        new, msg = transform(html)
        if new is None:
            print(f"  [{name}] {msg}")
            continue
        img = f'<img class="hero-photo" src="{photo}" alt="{alt}" fetchpriority="high">\n    '
        new = new.replace('<div class="hero-bg"></div>', img + '<div class="hero-bg"></div>', 1)
        ok += 1
        print(f"  [変換] {name:28} img={photo}")
        if not DRY:
            for root in ROOTS:
                p = os.path.join(root, name)
                if os.path.exists(p):
                    open(p, "w", encoding="utf-8").write(new)
    print(f"\n=== {ok}/{len(CFG)} 変換 ===" + ("  (DRY-RUN)" if DRY else ""))

if __name__ == "__main__":
    main()
