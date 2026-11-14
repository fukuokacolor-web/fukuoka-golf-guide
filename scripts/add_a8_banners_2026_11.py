#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A8 の画像広告 (RIZAPゴルフ・フェアウェイゴルフ) を関係の深い 5 ページに 1 か所ずつ入れる (2026-11-14)。
  A8 のコードは改変しない (リンク <a> に aria-label だけ足す。GA4 の click_affiliate で link_text として記録される)。
  紹介文は事実だけ: RIZAPゴルフ 九州は博多店・体験レッスン付きゴルフ力診断 3,300円 (公式 rizap-golf.jp/golfschool 2026-11-14 確認)
                   フェアウェイゴルフ = A8 のプログラム名「ゴルフクラブUSAから直送」(「激安」は広告主の言葉なので使わない)
  rental-and-transport.html には【PR】広告表示が無いので他ページと同じものを足す。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/add_a8_banners_2026_11.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv

RIZAP = ('<a href="https://px.a8.net/svt/ejp?a8mat=4BGK83+2RFESY+CW6+BF3LHT" rel="nofollow" aria-label="RIZAPゴルフ（広告）">\n'
         '<img border="0" width="300" height="250" alt="" src="https://www24.a8.net/svt/bgt?aid=261113187167&wid=001&eno=01&mid=s00000001671069049000&mc=1"></a>\n'
         '<img border="0" width="1" height="1" src="https://www11.a8.net/0.gif?a8mat=4BGK83+2RFESY+CW6+BF3LHT" alt="">')
FAIRWAY = ('<a href="https://px.a8.net/svt/ejp?a8mat=4BGK83+2NUT6A+28NM+6DC69" rel="nofollow" aria-label="フェアウェイゴルフ（広告）">\n'
           '<img border="0" width="250" height="250" alt="" src="https://www26.a8.net/svt/bgt?aid=261113187161&wid=001&eno=01&mid=s00000010453001070000&mc=1"></a>\n'
           '<img border="0" width="1" height="1" src="https://www17.a8.net/0.gif?a8mat=4BGK83+2NUT6A+28NM+6DC69" alt="">')

TXT_RIZAP = "コースデビューの前に、マンツーマンでスイングを見てもらいたい人へ。ライザップゴルフは九州では博多店があり、体験レッスン付きのゴルフ力診断（3,300円）から始められます（2026年11月時点・公式サイト）。"
TXT_FAIR = "自分のクラブをそろえるなら、通販も選択肢です。フェアウェイゴルフは、アメリカから直送するゴルフクラブの通販サイトです。"
TXT_FAIR_RENTAL = "旅のたびにレンタルするより、自分のクラブを持ちたくなったら。フェアウェイゴルフは、アメリカから直送するゴルフクラブの通販サイトです。"


def box(key, items):
    cells = "\n".join(f'''    <div class="a8-ad-item">
      <p class="a8-ad-text">{t}</p>
      {code}
    </div>''' for t, code in items)
    return f'''
<!-- a8-banner-v1:{key} -->
<aside class="a8-ad" aria-label="広告">
  <style>.a8-ad{{width:calc(100% - 32px);max-width:760px;box-sizing:border-box;margin:32px auto;padding:14px 16px 16px;border:1px solid #e3ddcf;border-radius:14px;background:#fffdf8;text-align:center;}}.a8-ad-label{{font-size:11px;color:#888;letter-spacing:.1em;margin-bottom:8px;}}.a8-ad-items{{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;}}.a8-ad-item{{flex:1 1 300px;max-width:340px;}}.a8-ad-text{{font-size:13.5px;line-height:1.7;color:#333;margin:0 0 10px;text-align:left;}}.a8-ad img{{max-width:100%;height:auto;}}</style>
  <div class="a8-ad-label">PR（広告）</div>
  <div class="a8-ad-items">
{cells}
  </div>
</aside>
'''


PR_STYLE = '<style>.ad-disclosure{background:#f4f1ea;color:#555;font-size:11.5px;line-height:1.6;padding:8px 16px;text-align:center;border-bottom:1px solid #e3ddcf;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;}.ad-disclosure strong{color:#333;}.ad-disclosure a{color:#555;text-decoration:underline;}@media (max-width:900px){.ad-disclosure{font-size:11px;padding:7px 12px;}.ad-disclosure .ad-d-long{display:none;}}</style>'
PR_DIV = '<div class="ad-disclosure" role="note"><strong>【PR】</strong>本ページはアフィリエイト広告を含みます。<span class="ad-d-long">掲載している予約サイト等のリンクから予約・購入されると、当サイトに報酬が支払われる場合があります。</span><a href="editorial-policy.html">詳しく</a><span class="ad-d-long" lang="en"> / Contains affiliate ads.</span><span class="ad-d-long" lang="ko"> / 제휴 광고를 포함합니다.</span></div>'

# (ファイル, 日本語ブロック内の挿入位置の目印 (この直前に入れる), 広告キー, 中身)
PLAN = [
    ("hub-beginner.html", '  <!-- RELATED AREAS -->', "rizap", [(TXT_RIZAP, RIZAP)]),
    ("book-fukuoka-beginner.html", '<!-- Related -->\n<div class="section-pale">', "rizap-fairway", [(TXT_RIZAP, RIZAP), (TXT_FAIR, FAIRWAY)]),
    ("beginner-cards.html", '  <div class="sec-head">📅 福岡のゴルフ場を予約する</div>', "rizap", [(TXT_RIZAP, RIZAP)]),
    ("rental-and-transport.html", '  <div class="cta-row">', "fairway", [(TXT_FAIR_RENTAL, FAIRWAY)]),
    ("golf-wear.html", '  <div class="disclaimer">', "fairway", [(TXT_FAIR, FAIRWAY)]),
]

for root in ROOTS:
    print(root)
    for f, anchor, key, items in PLAN:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if "a8-banner-v1" in s:
            print(f"  {f}: already"); continue
        nl = "\r\n" if "\r\n" in s else "\n"
        w = s.replace("\r\n", "\n")
        i = w.find('id="c-ja"')
        if i >= 0:
            j = min([x for x in (w.find('id="c-en"', i + 1), w.find('id="c-ko"', i + 1), len(w)) if x > i])
        else:
            i, j = 0, len(w)
        blk = w[i:j]
        k = blk.find(anchor)
        assert k >= 0, (f, "anchor")
        blk = blk[:k] + box(key, items) + "\n" + blk[k:]
        new = w[:i] + blk + w[j:]
        if "ad-disclosure" not in new:
            new = new.replace("<body>\n", "<body>\n" + PR_STYLE + "\n" + PR_DIV + "\n", 1)
            assert "ad-disclosure" in new, f
        new = new.replace("\n", nl)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        print(f"  {f}: {key} を追加{'・PR表示を追加' if 'ad-disclosure' not in s else ''}")
        if APPLY:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
