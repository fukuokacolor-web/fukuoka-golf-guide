#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英語・韓国語のコースページに「海外からの方の予約条件」の注意書きを入れる (foreign_booking_rules.json の 26 コース)。
  背景 (2026-11-23): 楽天GORA・じゃらんのプラン説明と公式サイトに、会員同伴・日本語話者の同伴・入国当日不可などの条件が
  書かれているのに、EN/KO ページは何も触れていなかった。予約しても当日断られる恐れ → 事実の注記 (既存ページの誤り修正)。
  位置: EN/KO それぞれの最初の stats-bar の直前 (ファーストビューの予約帯の下)。JA は触らない。
  出典の表示: 「楽天GORA / じゃらん / 公式サイトのコースの案内による (2026年11月23日確認)」。
冪等 (MARKER・内容が変わったら差し替え)。改行コードはそのまま。
Usage: python scripts/add_foreign_notice_2026_11.py [--apply] [--only course-x.html]
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "foreign-notice-v1"
RULES = json.load(open(os.path.join(ROOTS[0], "foreign_booking_rules.json"), encoding="utf-8"))
SRC = {"en": {"rakuten": "Rakuten GORA", "jalan": "Jalan", "official": "the official website"},
       "ko": {"rakuten": "라쿠텐 GORA", "jalan": "자란", "official": "공식 사이트"}}
HEAD = {"en": "Booking note for overseas visitors", "ko": "해외 고객 예약 안내"}
FOOT = {"en": "From the course's own notice on {src} (checked 23 Nov 2026). Conditions can change — confirm with the course before you travel.",
        "ko": "{src}에 게재된 골프장 안내 기준 (2026년 11월 23일 확인). 조건은 바뀔 수 있으니 출발 전에 골프장에 확인하세요."}
GUIDE = {"en": ('book-fukuoka-golf-foreigner.html', "Conditions at other courses →"),
         "ko": ('book-fukuoka-golf-foreigner.html', "다른 골프장 조건 보기 →")}
BLOCK_RE = re.compile(r'[ \t]*<!-- ' + MARKER + r' -->.*?<!-- /' + MARKER + r' -->\r?\n', re.S)


def block(slug, lang, nl):
    r = RULES["courses"][slug]
    srcs = [SRC[lang][x] for x in r["src"].split(",")]
    src = " / ".join(srcs)
    href, label = GUIDE[lang]
    return (f'  <!-- {MARKER} -->{nl}'
            f'  <div class="foreign-notice" style="max-width:720px;margin:0 auto 28px;padding:16px 20px;background:#fff8e6;border:1px solid #f0d28a;border-left:5px solid #e0a100;border-radius:12px;font-size:14px;line-height:1.7;color:#3a3a3a;">{nl}'
            f'    <strong>⚠️ {HEAD[lang]}</strong><br>{r[lang]}{nl}'
            f'    <div style="margin-top:6px;font-size:12px;color:#6a6a6a;">{FOOT[lang].format(src=src)} <a href="{href}" style="color:#1a5fa0;">{label}</a></div>{nl}'
            f'  </div>{nl}'
            f'  <!-- /{MARKER} -->{nl}')


res = {}
for root in ROOTS:
    for slug in RULES["courses"]:
        f = f"course-{slug}.html"
        if ONLY and f != ONLY:
            continue
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        new = BLOCK_RE.sub("", s)  # 差し替えのため一度外す
        for lang in ("ko", "en"):  # 後ろから入れて位置ずれを防ぐ
            i = new.find(f'id="c-{lang}"')
            j = new.find('<div class="stats-bar">', i)
            k = new.find('id="c-', i + 10)
            assert i > 0 and j > 0 and (k < 0 or j < k), (f, lang)
            line_start = new.rfind("\n", 0, j) + 1
            new = new[:line_start] + block(slug, lang, nl) + new[line_start:]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        key = "already" if new == s else ("updated" if MARKER in s else "added")
        res.setdefault(key, []).append(f)
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v[:4])
print("APPLIED" if APPLY else "DRY-RUN")
