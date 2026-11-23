#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
hub-business.html (日本語) の上部に「福岡のゴルフ場を広く探している方へ」の案内を入れる。
  背景 (2026-11-23 GSC): 一般語「福岡 ゴルフ場」(28日で1,202表示・8.8位) がこの名門10選ページに着地している。
  名門・会員制のコースを探していない人が多いはずなので、全50コース・エリア別・安く回る・明日予約・初心者へ案内する。
  位置: 数字の帯 (persona-band) の直後。リンクのクリックは GA4 internal_nav_click (nav_section='general_search_nav') で数える。
EN/KO は触らない。冪等 (MARKER)。改行コードはそのまま。
Usage: python scripts/hub_business_general_nav_2026_11.py [--apply]
"""
import os, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARKER = "hub-business-general-nav-v1"
LINKS = [  # (href, 表示, 補足)
    ("/", "全50コースを比べる", "料金・エリア・アクセス"),
    ("book-fukuoka-cheap.html", "安く回れるコース", "平日¥8,000以下"),
    ("book-fukuoka-tomorrow.html", "今日・明日に予約できる", "当日予約OKのコース"),
    ("hub-beginner.html", "初心者向け", "ショート・フラット"),
]
AREAS = [("area-fukuokacity.html", "福岡市 8"), ("area-itoshima.html", "糸島 6"), ("area-kitakyushu.html", "北九州・宗像 15"),
         ("area-chikugo.html", "筑後・久留米 11"), ("area-chikuho.html", "筑豊 10")]


def track(target):
    t = "index" if target == "/" else target.replace(".html", "")
    return (f"if(window.gtag)gtag('event','internal_nav_click',{{page:'hub-business',lang:'ja',"
            f"nav_section:'general_search_nav',target_page:'{t}'}})")


def box(nl):
    L = [f'  <!-- {MARKER} -->',
         '  <div style="max-width:1100px;margin:0 auto;padding:22px 24px 0;">',
         '    <div style="background:#fff;border:1px solid #e3ddcf;border-radius:14px;padding:16px 18px;">',
         '      <div style="font-weight:700;font-size:14.5px;color:#1a5c38;margin-bottom:10px;">名門にこだわらず、福岡のゴルフ場を探している方へ</div>',
         '      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px;margin-bottom:10px;">']
    for href, label, sub in LINKS:
        L.append(f'        <a href="{href}" onclick="{track(href)}" style="display:block;background:#f4f1ea;border:1px solid #e3ddcf;border-radius:10px;padding:10px 12px;text-decoration:none;">'
                 f'<span style="display:block;font-weight:700;color:#1a5c38;font-size:13.5px;">{label} →</span>'
                 f'<span style="display:block;font-size:11.5px;color:#777;">{sub}</span></a>')
    L += ['      </div>',
          '      <div style="font-size:12.5px;color:#5a5a5a;line-height:2;">エリアから探す：' +
          '・'.join(f'<a href="{h}" onclick="{track(h)}" style="color:#1a5fa0;font-weight:700;">{t}コース</a>' for h, t in AREAS) +
          '</div>',
          '    </div>',
          '  </div>',
          f'  <!-- /{MARKER} -->']
    return nl.join(L) + nl


res = []
for root in ROOTS:
    p = os.path.join(root, "hub-business.html")
    s = open(p, encoding="utf-8", newline="").read()
    if MARKER in s:
        res.append("already")
        continue
    nl = "\r\n" if "\r\n" in s else "\n"
    i = s.find('id="c-ja"')
    j = s.find('id="c-en"', i)
    a = s.find('<section class="persona-band">', i)
    assert 0 < a < j
    e = s.find("</section>", a) + len("</section>")
    e = s.find("\n", e) + 1
    new = s[:e] + nl + box(nl) + s[e:]
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    assert "\r\r" not in new
    res.append("updated")
    if APPLY:
        open(p, "w", encoding="utf-8", newline="").write(new)
print(res, "APPLIED" if APPLY else "DRY-RUN")
