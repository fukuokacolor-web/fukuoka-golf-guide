#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
終了した A8 プログラム「skyticketレンタカー」(a8mat=4B1DXO+5K1O1E+DRA+356I3M・2026/05/31 終了) のリンクを
楽天トラベル レンタカー (A8 経由の楽天アフィリエイト) に置き換える。
  背景 (2026-11-25): A8 の無効クリックレポートに 11/18・11/23 のクリック → 押した人は報酬にならず、終了ページに飛ぶ。
  1) リンク URL (href・sticky バーの JS 変数) を楽天トラベル レンタカー https://travel.rakuten.co.jp/cars/ に
  2) skyticket の表示計測用画像 (0.gif?a8mat=4B1DXO...) を削除
  3) 本文の skyticket を書き換え。確認できない言い方 (最大50%OFF・空港ターミナル直結・待ち時間ゼロ) は消す
     楽天トラベル レンタカー: 「全国のレンタカー比較・予約」・トヨタ/日産/タイムズ/オリックス等・福岡空港を選べる (2026-11-25 確認)
  EN/KO も同じリンク (楽天トラベルは日本語サイトなので EN/KO の文言に「日本語サイト」と書く)。
冪等。改行コードはそのまま。G-PENH0Z4VT7 不変。
Usage: python scripts/replace_skyticket_2026_11.py [--apply]
"""
import glob, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
OLD_URL = "https://px.a8.net/svt/ejp?a8mat=4B1DXO+5K1O1E+DRA+356I3M"
U = "https%253A%252F%252Ftravel.rakuten.co.jp%252Fcars%252F"
NEW_URL = ("https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp"
           "%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3D" + U + "%26m%3D" + U)
PIXEL = re.compile(r'[ \t]*<img [^>]*0\.gif\?a8mat=4B1DXO\+5K1O1E\+DRA\+356I3M[^>]*>[ \t]*\r?\n?')

T = [  # (旧, 新)  長いものから
    # JA
    ("福岡空港・博多駅からskyticketで車を確保すれば", "福岡空港・博多駅でレンタカーを借りれば"),
    ("福岡空港直結でskyticket等で予約可能。", "レンタカーは楽天トラベルなどで事前に予約できます。"),
    ("skyticketなら主要レンタカー会社を比較予約でき、受取カウンターは空港ターミナル直結です。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticketで複数社を比較して、最安プランを押さえましょう。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticketで複数社を比較して最適プランを。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticketで複数社を比較して最安プランを。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticketで複数社を比較、最安プランをお早めに。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticket事前予約で待ち時間ゼロ。キャディバッグ積載サイズを要確認。", "事前に予約しておくと安心です。キャディバッグが積めるサイズかを確認。"),
    ("skyticket レンタカー経由で最大50%OFF。", "楽天トラベルでレンタカー各社を比べて予約できます。"),
    ("skyticket レンタカーで格安予約 →", "楽天トラベルでレンタカーを探す →"),
    ("比較して最安値を探せる", "レンタカー各社を比較・楽天ポイントが貯まる"),
    ("🚗 skyticketレンタカーで予約 →", "🚗 楽天トラベルでレンタカーを予約 →"),
    ("🚗 skyticketでレンタカーを探す →", "🚗 楽天トラベルでレンタカーを探す →"),
    ("🚗 skyticketで車を確保 →", "🚗 楽天トラベルでレンタカーを予約 →"),
    ("🚗 skyticketで車を確保", "🚗 楽天トラベルでレンタカーを予約"),
    ("<strong>skyticketレンタカー</strong>", "<strong>レンタカー</strong>"),
    # EN
    ("Pick one up at FUK or Hakata via skyticket — ", "Pick one up at FUK or Hakata — "),
    ("Book via skyticket — save up to 50% on rentals.", "Compare rental car companies on Rakuten Travel (Japanese site)."),
    ("Compare rates with skyticket.", "Compare rental car companies on Rakuten Travel (Japanese site)."),
    ("Compare rates across rental companies on skyticket.", "Compare rental car companies on Rakuten Travel (Japanese site)."),
    ("Compare rates on skyticket.", "Compare rental car companies on Rakuten Travel (Japanese site)."),
    ("Pre-booking via skyticket means zero wait. Confirm trunk size for your clubs.", "Book ahead and confirm the trunk fits your golf bags."),
    ("skyticket lets you compare all major providers, with pickup counters right at the terminal.", "You can compare rental car companies on Rakuten Travel (Japanese site)."),
    ("Book in advance via skyticket.", "Book in advance (e.g. Rakuten Travel, Japanese site)."),
    ("Book cheap rental cars on skyticket →", "Find rental cars on Rakuten Travel (Japanese) →"),
    ("🚗 Book on skyticket →", "🚗 Rakuten Travel rental cars (Japanese) →"),
    ("🚗 Find Rental Cars on skyticket →", "🚗 Rakuten Travel rental cars (Japanese) →"),
    ("🚗 Reserve on skyticket →", "🚗 Rakuten Travel rental cars (Japanese) →"),
    ("🚗 Book car on skyticket", "🚗 Rakuten Travel rental cars (Japanese)"),
    ("<strong>skyticket rental car</strong>", "<strong>rental car</strong>"),
    ('<div style="font-size:0.7rem;opacity:.8;margin-top:4px;">Compare prices and find the best deal</div>', '<div style="font-size:0.7rem;opacity:.8;margin-top:4px;">Compare rental car companies</div>'),
    # KO
    ("FUK·하카타역에서 skyticket으로 차를 확보하면", "FUK·하카타역에서 렌터카를 빌리면"),
    ("skyticket에서 주요 렌터카 회사를 비교 예약할 수 있으며, 픽업 카운터는 공항 터미널 직결입니다.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교해 예약할 수 있습니다."),
    ("skyticket에서 여러 업체를 비교해 최저가를 잡으세요.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket에서 여러 업체를 비교, 최저가 플랜을 빠르게.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket에서 여러 업체 비교 최저가 플랜.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket에서 여러 업체 비교해 최저가 플랜을.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket에서 여러 업체 비교해 최적 플랜을.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket 사전 예약으로 대기 시간 제로.", "미리 예약하고 골프백이 실리는 크기인지 확인하세요."),
    ("skyticket 렌터카로 최대 50% 할인.", "라쿠텐 트래블(일본어 사이트)에서 렌터카 회사를 비교할 수 있습니다."),
    ("skyticket 렌터카로 저렴하게 예약 →", "라쿠텐 트래블에서 렌터카 찾기 (일본어) →"),
    ("🚗 skyticket 렌터카 예약 →", "🚗 라쿠텐 트래블 렌터카 (일본어) →"),
    ("🚗 skyticket에서 렌터카 검색 →", "🚗 라쿠텐 트래블 렌터카 (일본어) →"),
    ("🚗 skyticket으로 차 확보 →", "🚗 라쿠텐 트래블 렌터카 (일본어) →"),
    ("🚗 skyticket으로 차 확보", "🚗 라쿠텐 트래블 렌터카 (일본어)"),
    ("<strong>skyticket 렌터카</strong>", "<strong>렌터카</strong>"),
    ('<div style="font-size:0.7rem;opacity:.8;margin-top:4px;">가격 비교로 최저가 찾기</div>', '<div style="font-size:0.7rem;opacity:.8;margin-top:4px;">렌터카 회사 비교</div>'),
]
CODE_OK = re.compile(r"classifyService|test\(href\)|sc-skyticket|btn-skyticket|plan-cta-sky|SKYTICKET|^\s*//|/\*|<!--|\.test\(h")

res = {}
left = set()
for root in ROOTS:
    for p in sorted(glob.glob(os.path.join(root, "*.html"))):
        f = os.path.basename(p)
        s = open(p, encoding="utf-8", newline="").read()
        if OLD_URL not in s and "0.gif?a8mat=4B1DXO" not in s and not any(o in s for o, _ in T):
            continue
        new = s.replace(OLD_URL, NEW_URL)
        new = PIXEL.sub("", new)
        for o, n in T:
            new = new.replace(o, n)
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7") and "\r\r" not in new, f
        for line in new.splitlines():
            if "skyticket" in line.lower() and not CODE_OK.search(line):
                left.add((f, line.strip()[:160]))
        res.setdefault("changed", []).append(f)
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("changed", len(res.get("changed", [])))
print("残り (コード以外の skyticket):", len(left))
for x in sorted(left)[:30]:
    print("  ", x)
print("APPLIED" if APPLY else "DRY-RUN")
