#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_rakuten_cta.py — じゃらんCTAの直後に楽天GORA CTAを併記する mass apply。

規約:
- 冪等: 既に同じ c_id の楽天リンクが直後にあればスキップ(MARKER=c_id)。
- dry-run: --dry-run で件数プレビューのみ(デフォルトは dry-run)。--apply で本番。
- ROOTS: REPO + PREVIEW 両方処理。
- 除外(§9.4 楽天GORA除外): fukuocc/wakamatsu/akane/genkai は楽天CTAを付けない
  (rakuten_gora_mapping の c_id=None も自動除外)。
- 対象ファイルは引数で明示(スコープ厳格化・§12教訓)。
使い方: python scripts/add_rakuten_cta.py [--apply] file1.html file2.html ...
"""
import sys, re, json, os

REPO = r"C:/Users/Owner/fukuoka-golf-guide"
PREVIEW = r"C:/Users/Owner/Documents/新しいPJ"
ROOTS = [REPO, PREVIEW]

RAK_EXCLUDE = {"fukuokacc", "wakamatsu", "akane", "genkai"}

def build_map():
    """jalan_id(str) -> c_id(str) 。除外・c_id無しは含めない。"""
    jm = json.load(open(os.path.join(REPO, "jalan_golf_mapping.json"), encoding="utf-8"))
    rk = json.load(open(os.path.join(REPO, "rakuten_gora_mapping.json"), encoding="utf-8"))
    jrows = jm if isinstance(jm, list) else jm.get("courses", jm)
    # jalan file->id
    jby = {}
    for r in jrows:
        f = r.get("file", "").replace("course-", "")
        if r.get("jalan_id"):
            jby[f] = str(r["jalan_id"])
    cby = {}
    for r in rk["courses"]:
        f = r.get("file", "").replace("course-", "")
        if r.get("c_id"):
            cby[f] = str(r["c_id"])
    m = {}
    for f, jid in jby.items():
        if f in RAK_EXCLUDE:
            continue
        cid = cby.get(f)
        if cid:
            m[jid] = cid
    return m

def rak_href(cid):
    enc = ("https%253A%252F%252Fbooking.gora.golf.rakuten.co.jp"
           "%252Fguide%252Fdisp%252Fc_id%252F" + cid)
    return ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y"
            "&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F"
            "0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2F"
            "a26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + enc + "%26m%3D" + enc)

# course固有(gc{ID}付き)の じゃらん anchor を属性順・class名非依存で捕捉。
# generic homepage(golf-jalan.net/ のみ)は gc要求により対象外。ラベルにタグ無し想定([^<]*)。
JALAN_A = re.compile(
    r'<a\b(?P<tag>[^>]*golf-jalan\.net%2Fgc0*(?P<jid>\d+)%2F[^>]*)>'
    r'(?P<label>[^<]*)</a>'
)

def cls_of(tag):
    mm = re.search(r'class="([^"]*)"', tag)
    return mm.group(1) if mm else ''

def rak_anchor(tag, cid):
    cls = cls_of(tag)
    rcls = re.sub(r'btn-jalan[a-z-]*', 'btn-rakuten', cls) if 'btn-jalan' in cls else cls
    clsattr = f' class="{rcls}"' if rcls else ''
    style = ('background:linear-gradient(135deg,#BF0000,#9B0000);color:#fff;'
             'box-shadow:0 3px 10px rgba(191,0,0,0.28);')
    return (f'<a href="{rak_href(cid)}"{clsattr} style="{style}"'
            f' target="_blank" rel="nofollow sponsored noopener"'
            f' data-rakcid="{cid}">🅡 楽天GORA</a>')

def process(text, m):
    added = skipped_dup = skipped_excl = 0
    out = []
    pos = 0
    for mt in JALAN_A.finditer(text):
        out.append(text[pos:mt.end()])
        pos = mt.end()
        jid = mt.group("jid").zfill(5)
        cid = m.get(jid)
        if not cid:
            skipped_excl += 1
            continue
        # 冪等: 直後 ~1500字以内に data-rakcid="cid" があればスキップ
        # (楽天hrefは~500字と長いため窓を広めに取る)
        lookahead = text[mt.end():mt.end()+1500]
        if f'data-rakcid="{cid}"' in lookahead:
            skipped_dup += 1
            continue
        out.append(rak_anchor(mt.group("tag"), cid))
        added += 1
    out.append(text[pos:])
    return "".join(out), added, skipped_dup, skipped_excl

def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if not args:
        print("usage: add_rakuten_cta.py [--apply] file1.html ..."); return
    m = build_map()
    print(f"[map] jalan_id->c_id : {len(m)} 件 (楽天除外/c_id無しは除外)")
    print(f"[mode] {'APPLY(本番)' if apply else 'DRY-RUN'}\n")
    tot_add = tot_dup = tot_excl = 0
    for fname in args:
        src = os.path.join(REPO, fname)
        if not os.path.exists(src):
            print(f"  NOT_FOUND {fname}"); continue
        text = open(src, encoding="utf-8").read()
        new, add, dup, excl = process(text, m)
        tot_add += add; tot_dup += dup; tot_excl += excl
        print(f"  {fname:26} +{add} 追加 / {dup} 既存skip / {excl} 除外skip")
        if apply and new != text:
            for root in ROOTS:
                p = os.path.join(root, fname)
                if os.path.exists(os.path.dirname(p)):
                    open(p, "w", encoding="utf-8", newline="").write(new)
    print(f"\n[合計] 追加 {tot_add} / 既存 {tot_dup} / 除外 {tot_excl}")
    if not apply:
        print("※ dry-run。本番反映は --apply を付けて再実行。")

if __name__ == "__main__":
    main()
