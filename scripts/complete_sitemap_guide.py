#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""complete_sitemap_guide.py — sitemap-guide.html を 50 コース体制に完全整合。

#4 (6 エージェント ミスチェック残項目)。sitemap-guide.html は meta 説明で
「福岡近郊 50 ゴルフ場の全ページ一覧」と謳うが、実態は以下が未整合だった:
  - access(教通編)セクション: 50 中 29 コースのみ掲載 (欠落 21 = 旧 8 + Batch2 13)
  - セクションヘッダー 6 箇所が「29コース」のまま (コース紹介は実際 50 掲載済)
  - KO meta description が「29개 골프장」(JA/EN は 50)
  - エリアガイド sublabel のコース数が旧値 (北九州7→15 / 糸島4→6 / 筑後6→11 / 筑豊6→10)

本スクリプトでこれらを 50 コース体制の実数に整合させる。access リンクのラベルは
コース紹介セクションの正式名称を流用 (検証済テキスト)。
fees.html sublabel の「29コース」は fees.html 自体の掲載数依存のため対象外。
両ディレクトリ・冪等 (再実行で 0 件)。

Usage: python scripts/complete_sitemap_guide.py [--dry-run]
"""
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path("C:/Users/Owner/fukuoka-golf-guide")
PREVIEW_ROOT = Path("C:/Users/Owner/Documents/新しいPJ")
DRY = "--dry-run" in sys.argv
TARGET = "sitemap-guide.html"

# --- 1. カウント / ヘッダー文字列置換 (冪等: 再実行で旧値なし→0件) ---
REPLACEMENTS = [
    # セクションヘッダー 6 箇所
    ("コース紹介（29コース）", "コース紹介（50コース）"),
    ("アクセスページ（29コース）", "アクセスページ（50コース）"),
    ("Course Guides (29 Courses)", "Course Guides (50 Courses)"),
    ("Access Pages (29 Courses)", "Access Pages (50 Courses)"),
    ("코스 소개 (29개 코스)", "코스 소개 (50개 코스)"),
    ("교통편 페이지 (29개 코스)", "교통편 페이지 (50개 코스)"),
    # KO meta description
    ("후쿠오카 인근 29개 골프장", "후쿠오카 인근 50개 골프장"),
    # エリアガイド sublabel JA
    ("7コース・国際空港", "15コース・国際空港"),
    ("4コース・玄界灘", "6コース・玄界灘"),
    ("6コース・温泉", "11コース・温泉"),
    ("6コース・コスパ", "10コース・コスパ"),
    # エリアガイド sublabel EN (dot-free アンカー)
    ("7 courses", "15 courses"),
    ("4 ocean-view courses", "6 ocean-view courses"),
    ("6 courses", "11 courses"),
    ("6 hidden-gem courses", "10 hidden-gem courses"),
    # エリアガイド sublabel KO
    ("7개 코스", "15개 코스"),
    ("4개 코스", "6개 코스"),
    ("6개 코스·온천", "11개 코스·온천"),
    ("6개 코스·가성비", "10개 코스·가성비"),
]

# --- 2. access リンク欠落 21 コース (コース紹介セクション順) ---
# (slug, name_ja, name_en, name_ko)
MISSING = [
    ("shimaseaside",   "志摩シーサイドカンツリークラブ", "Shima Seaside CC",                   "시마 시사이드 CC"),
    ("classic",        "ザ・クラシックゴルフ倶楽部",     "The Classic GC",                     "더 클래식 GC"),
    ("fukuokakokusai", "福岡国際カントリークラブ",       "Fukuoka Kokusai CC",                 "후쿠오카 국제 CC"),
    ("wakamatsu",      "若松ゴルフ倶楽部",               "Wakamatsu GC",                       "와카마쓰 GC"),
    ("ukiha",          "浮羽カントリークラブ",           "Ukiha CC",                           "우키하 CC"),
    ("genkai",         "玄海ゴルフクラブ",               "Genkai GC",                          "겐카이 GC"),
    ("takaha",         "鷹羽ロイヤルカントリークラブ",   "Takaha Royal CC",                    "다카하 로열 CC"),
    ("pheasant",       "福岡フェザントカントリークラブ", "Fukuoka Pheasant CC",                "후쿠오카 페즌트 CC"),
    ("raizan",         "福岡雷山ゴルフ倶楽部",           "Fukuoka Raizan Golf Club",           "후쿠오카 라이잔 골프 클럽"),
    ("newui",          "NEWユーアイゴルフクラブ",        "NEW U.I. Golf Club",                 "NEW 유아이 골프 클럽"),
    ("suonada",        "周防灘カントリークラブ",         "Suonada Country Club",               "스오나다 컨트리 클럽"),
    ("chisan-onga",    "チサンカントリークラブ遠賀",     "Chisan Country Club Onga",           "치산 컨트리 클럽 온가"),
    ("seitanomori",    "瀬板の森北九州ゴルフコース",     "Seitanomori Kitakyushu Golf Course", "세이타노모리 기타큐슈 골프 코스"),
    ("satsuki-tenpai", "皐月ゴルフ倶楽部 天拝コース",    "Satsuki Golf Club Tenpai Course",    "사쓰키 골프 클럽 덴파이 코스"),
    ("yasukogen",      "夜須高原カントリークラブ",       "Yasukogen Country Club",             "야스코겐 컨트리 클럽"),
    ("yamejoyo",       "八女上陽ゴルフ倶楽部",           "Yame Joyo Golf Club",                "야메 죠요 골프 클럽"),
    ("sunlake",        "福岡サンレイクゴルフ倶楽部",     "Fukuoka Sunlake Golf Club",          "후쿠오카 선레이크 골프 클럽"),
    ("satsuki-ryuoh",  "皐月ゴルフ倶楽部 竜王コース",    "Satsuki Golf Club Ryuoh Course",     "사쓰키 골프 클럽 류오 코스"),
    ("kaho",           "かほゴルフクラブ",               "Kaho Golf Club",                     "카호 골프 클럽"),
    ("nishinihon",     "西日本カントリークラブ",         "Nishi-Nippon Country Club",          "니시니혼 컨트리 클럽"),
    ("jruchino",       "JR内野カントリークラブ",         "JR Uchino Country Club",             "JR 우치노 컨트리 클럽"),
]

# 各言語の access セクション末尾アンカー (aburayama リンク行) と接尾辞・name index
ANCHORS = [
    ('<a href="access-aburayama.html">ララヒルズ油山 アクセス</a>',      " アクセス", 1),
    ('<a href="access-aburayama.html">Lala Hills Aburayama Access</a>',  " Access",   2),
    ('<a href="access-aburayama.html">라라 힐스 아부라야마 교통편</a>',   " 교통편",   3),
]


def build_block(suffix, idx):
    return "\n".join(
        f'      <a href="access-{row[0]}.html">{row[idx]}{suffix}</a>'
        for row in MISSING
    )


print(f"[complete_sitemap_guide] mode = {'DRY-RUN' if DRY else 'LIVE'}\n")
for root in [REPO_ROOT, PREVIEW_ROOT]:
    path = root / TARGET
    print(f"--- {root.name} ---")
    if not path.exists():
        print("  NOT FOUND\n")
        continue
    text = path.read_text(encoding="utf-8")
    orig = text
    # 1. 文字列置換
    rep_count = 0
    for old, new in REPLACEMENTS:
        c = text.count(old)
        if c == 0 and new not in text:
            print(f"  WARN no match: {old}")
        rep_count += c
        text = text.replace(old, new)
    # 2. access リンク挿入 (冪等ガード: access-raizan.html 未挿入時のみ)
    ins_count = 0
    if "access-raizan.html" not in text:
        for anchor, suffix, idx in ANCHORS:
            if anchor in text:
                text = text.replace(anchor, anchor + "\n" + build_block(suffix, idx), 1)
                ins_count += len(MISSING)
            else:
                print(f"  WARN access anchor not found: {anchor[:48]}")
    else:
        print("  access links already present (skip insertion)")
    if not DRY and text != orig:
        path.write_text(text, encoding="utf-8")
    print(f"  string replacements: {rep_count} / access links inserted: {ins_count}"
          f" / {'(dry-run)' if DRY else 'written'}\n")
print("*** DRY-RUN ***" if DRY else "DONE")
