import os, re

# コースと写真の対応（エリア・雰囲気で選択）
MAPPING = {
    # 糸島・海沿い系
    "course-keya":        "keya-rocks.webp",       # 芥屋大門の岩礁・海
    "course-nijo":        "itoshima-sea.webp",      # 糸島の海と空
    "course-queenshill":  "itoshima-bay.webp",      # 糸島の穏やかな湾
    "course-ito":         "itoshimatorii.webp",     # 糸島の鳥居

    # 西戸崎・博多湾岸
    "course-saitozaki":   "saitozaki-bridge.webp",  # 西戸崎の海岸と橋
    "course-fukuokacc":   "fukuoka-bay.webp",       # 福岡ベイエリア

    # 山・丘陵系（福岡市内・近郊）
    "course-aburayama":   "golf-mountain.webp",     # 背振山とゴルフ場
    "course-sevenmillion":"fukuoka-overview.webp",  # 山からの福岡市街俯瞰
    "course-chikushigaoka":"golf-mountain.webp",
    "course-daihakata":   "golf-mountain.webp",

    # 太宰府・筑紫野
    "course-dazaifu":     "sakura-road.webp",       # 桜並木
    "course-central":     "sakura-river.webp",      # 川沿いの桜
    "course-chikushino":  "spring-forest.webp",     # 新緑の森

    # 久山・粕屋・古賀
    "course-hisayama":    "sakura-road.webp",
    "course-century":     "sakura-river.webp",
    "course-koga":        "fukuoka-overview.webp",

    # 飯塚・山岳系
    "course-asoiizuka":   "aso-grassland.webp",     # 阿蘇の草原
    "course-akane":       "aso-grassland.webp",
    "course-lakeside":    "spring-forest.webp",

    # 鞍手・小竹・宮若
    "course-mission":     "fukuoka-overview.webp",
    "course-moonlake":    "itoshima-bay.webp",
    "course-wakamiya":    "spring-forest.webp",

    # 小郡・久留米
    "course-ogori":       "sakura-river.webp",
    "course-kurume":      "sakura-road.webp",

    # 北九州・門司
    "course-kitakyushu":  "island-view.webp",       # 海と島の絶景
    "course-kyushugc":    "fukuoka-bay.webp",
    "course-moji":        "keya-waves.webp",         # 荒波・海

    # 大牟田
    "course-ariake":      "itoshima-sea.webp",
}

CSS_TO_ADD = """
    .course-hero { width:100%; display:block; object-fit:cover; height:180px; border-radius:0; }
    .page-header { position:relative; overflow:hidden; }
"""

def add_photo(filepath, img_name):
    with open(filepath, encoding="utf-8") as f:
        html = f.read()

    # すでに course-hero があればスキップ
    if "course-hero" in html:
        print(f"SKIP (already has photo): {os.path.basename(filepath)}")
        return

    # CSSに追加
    html = html.replace(
        ".back-bar { background:#fff;",
        CSS_TO_ADD + "    .back-bar { background:#fff;"
    )

    # ヘッダー直後に画像を挿入
    html = html.replace(
        '</header>\n<div class="back-bar">',
        f'</header>\n<img src="images/{img_name}" class="course-hero" alt="コース周辺の景色" loading="lazy" width="900" height="600">\n<div class="back-bar">'
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"OK: {os.path.basename(filepath)} → {img_name}")

repo = "/c/Users/Owner/fukuoka-golf-guide"
for slug, img in MAPPING.items():
    path = f"{repo}/{slug}.html"
    if os.path.exists(path):
        add_photo(path, img)
    else:
        print(f"NOT FOUND: {slug}.html")

print("Done!")
