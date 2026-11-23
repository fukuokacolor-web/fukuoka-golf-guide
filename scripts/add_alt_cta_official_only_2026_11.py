#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
公式サイトでしか予約できない7コース (日本語) に「楽天GORAで予約できる近くのコース」枠を入れる。
  背景 (2026-11-23 分析 ANALYSIS_2026-11-23.md): 10/19〜26 に公式のみにした7コースは予約ボタンのクリックが0に。
  福岡CC・玄海・若松の同じ形の枠 (近くの予約できるコース) は実際に収益が出ている。
  そのコース自体には予約ボタンを付けない (CLAUDE.md §9.4)。案内するのは別のコース。
  候補は 2026-11-23 に gora_floor.py で楽天GORAの空き (直近14日に7〜14日) を確認したもの。
  位置: 日本語の料金セクション (— Green Fees) の直前。EN/KO は触らない (新規はJAのみの方針)。
冪等 (MARKER・内容が変わったら差し替え)。改行コードはそのまま。
Usage: python scripts/add_alt_cta_official_only_2026_11.py [--apply] [--only course-x.html]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "alt-cta-official-v1"

ALT = {  # slug: (表示名, 所在地, 楽天 c_id)
    "nijo": ("二丈カントリークラブ", "糸島市", "400037"),
    "ito": ("伊都ゴルフ倶楽部", "糸島市", "400006"),
    "sevenmillion": ("セブンミリオンカントリークラブ", "福岡市早良区", "400027"),
    "newui": ("NEWユーアイゴルフクラブ", "宗像市", "400052"),
    "hisayama": ("久山カントリー倶楽部", "久山町", "400038"),
    "wakamiya": ("WAKAMIYA COURSE", "宮若市", "400051"),
    "moonlake": ("ムーンレイクゴルフクラブ鞍手", "鞍手町", "400013"),
    "nishinihon": ("西日本カントリークラブ", "直方市", "400036"),
    "seitanomori": ("瀬板の森北九州ゴルフコース", "北九州市八幡西区", "400026"),
    "kitakyushu": ("北九州カントリー倶楽部", "北九州市", "400010"),
    "chisan-onga": ("チサンカントリークラブ遠賀", "遠賀町", "400035"),
    "suonada": ("周防灘カントリークラブ", "築上町", "400025"),
}
NOTICE_STD = "{name}は、じゃらん・楽天GORAではオンライン予約を受け付けていません（予約は公式サイトか電話で）。"
TARGETS = {  # slug: (コース名, エリア見出し, 説明, 案内するコース)
    "queenshill": ("ザ・クイーンズヒルゴルフクラブ", "糸島・福岡市西部", NOTICE_STD, ["nijo", "ito", "sevenmillion"]),
    "keya": ("芥屋ゴルフ倶楽部", "糸島", NOTICE_STD, ["ito", "nijo", "sevenmillion"]),
    "raizan": ("福岡雷山ゴルフ倶楽部", "糸島", NOTICE_STD, ["nijo", "ito", "sevenmillion"]),
    "koga": ("古賀ゴルフ・クラブ", "古賀・宗像・粕屋", NOTICE_STD, ["newui", "hisayama", "wakamiya"]),
    "classic": ("ザ・クラシックゴルフ倶楽部", "宮若・直方", NOTICE_STD, ["wakamiya", "moonlake", "nishinihon"]),
    "kokura": ("小倉カンツリー倶楽部", "北九州",
               "小倉カンツリー倶楽部のビジター予約は、会員の紹介を受けてからの電話予約です（公式サイトより）。", ["seitanomori", "kitakyushu", "chisan-onga"]),
    "moji": ("門司ゴルフ倶楽部", "北九州・京築", NOTICE_STD, ["kitakyushu", "seitanomori", "suonada"]),
}


def rakuten_url(cid):
    u = f"https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F{cid}"
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
            "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + u + "%26m%3D" + u)


def block(slug, nl):
    name, area, notice, alts = TARGETS[slug]
    L = [f'  <!-- {MARKER} -->',
         '  <div style="max-width:1100px;margin:0 auto;padding:28px 24px 0;">',
         '    <div style="background:#f4f1ea;border:1px solid #e3ddcf;border-left:5px solid #1a5c38;border-radius:14px;padding:22px 24px;">',
         f'      <div style="font-weight:700;font-size:16px;color:#1a5c38;margin-bottom:6px;">⛳ {area}で、楽天GORAから予約できるコース</div>',
         f'      <div style="font-size:13px;color:#5a5a5a;line-height:1.8;margin-bottom:14px;">{notice.format(name=name)}'
         'ネットで予約したい日は、近くのこちらのコースも候補に。下のボタンは各コースの楽天GORAの予約ページに移動します。</div>',
         '      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:10px;">']
    for a in alts:
        an, loc, cid = ALT[a]
        L += ['        <div style="background:#fff;border:1px solid #e3ddcf;border-radius:10px;padding:12px 14px;">',
              f'          <div style="font-weight:700;color:#1a5c38;font-size:13.5px;margin-bottom:8px;">{an} <span style="font-weight:400;color:#777;">／{loc}</span></div>',
              '          <div style="display:flex;gap:6px;">',
              f'            <a href="{rakuten_url(cid)}" target="_blank" rel="nofollow sponsored noopener" style="flex:1;text-align:center;background:linear-gradient(135deg,#BF0000,#8B0000);color:#fff;font-weight:700;font-size:12.5px;padding:9px 10px;border-radius:8px;text-decoration:none;">楽天GORAで予約 →</a>',
              f'            <a href="course-{a}.html" onclick="if(window.gtag)gtag(\'event\',\'internal_nav_click\',{{page:\'course-{slug}\',lang:\'ja\',nav_section:\'alternative_cta\',target_page:\'course-{a}\'}})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:12px;padding:9px 12px;border-radius:8px;text-decoration:none;border:1px solid #e3ddcf;">詳細</a>',
              '          </div>',
              '        </div>']
    L += ['      </div>',
          '      <div style="font-size:11.5px;color:#888;margin-top:10px;">楽天GORAで予約を受け付けていることを2026年11月23日に確認。空き状況・料金は日によって変わります。</div>',
          '    </div>',
          '  </div>',
          f'  <!-- /{MARKER} -->']
    return nl.join(L) + nl


BLOCK_RE = re.compile(r'[ \t]*<!-- ' + MARKER + r' -->.*?<!-- /' + MARKER + r' -->\r?\n', re.S)
res = {}
for root in ROOTS:
    for slug in TARGETS:
        f = f"course-{slug}.html"
        if ONLY and f != ONLY:
            continue
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        new = BLOCK_RE.sub("", s)
        i = new.find('id="c-ja"')
        j = new.find("— Green Fees", i)
        k = new.find('id="c-en"', i)
        assert i > 0 and 0 < j < k, (f, i, j, k)
        sec = new.rfind("<section", i, j)
        assert sec > 0, f
        ls = new.rfind("\n", 0, sec) + 1
        new = new[:ls] + block(slug, nl) + new[ls:]
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        key = "already" if new == s else ("updated" if MARKER in s else "added")
        res.setdefault(key, []).append(f)
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
for k, v in res.items():
    print(k, len(v), v)
print("APPLIED" if APPLY else "DRY-RUN")
