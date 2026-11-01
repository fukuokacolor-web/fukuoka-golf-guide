#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
アフィリエイトリンク (A8.net) を含む全ページの最上部に「広告を含む」表示を入れる。

根拠: 景品表示法のステルスマーケティング規制 (2023-10-01 施行) と、A8 の楽天・じゃらんの提携条件
(じゃらん: 「ページの上部に『#アフィリエイト広告』を入れるなど…記載」・違反は成果拒否の後に提携解除)。
2026-11-01 時点で a8.net リンクのある125ページと Amazon リンクの golf-wear.html (末尾注記のみ) に上部表示が無かった。

- <body> の直後に帯 (div.ad-disclosure) を挿入。言語ブロックの外なので JA/EN/KO どの表示でも出る
- 画面上端に固定の「← Top」「言語切替」(top:16px) と重ならないよう、同じ <style> で top を 46px にずらす
冪等: MARKER (class="ad-disclosure") があれば no-op。
Usage:
  python scripts/add_ad_disclosure.py                              # dry-run (対象一覧)
  python scripts/add_ad_disclosure.py --only course-kaho.html --preview   # 1件テスト: PREVIEW_ROOT だけに書く
  python scripts/add_ad_disclosure.py --apply                      # REPO + PREVIEW
"""
import os, re, sys, glob

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = 'class="ad-disclosure"'

SNIPPET = (
    '<style>'
    '.ad-disclosure{background:#f4f1ea;color:#555;font-size:11.5px;line-height:1.6;padding:8px 16px;text-align:center;'
    'border-bottom:1px solid #e3ddcf;font-family:-apple-system,BlinkMacSystemFont,"Hiragino Sans","Noto Sans JP",sans-serif;}'
    '.ad-disclosure strong{color:#333;}.ad-disclosure a{color:#555;text-decoration:underline;}'
    'body>.back-link,body>.lang-switcher{top:46px;}'
    # 900px 以下は1行に収める (説明文と英韓は省略・固定ボタンと重ならない高さに)
    '@media (max-width:900px){.ad-disclosure{font-size:11px;padding:7px 12px;}.ad-disclosure .ad-d-long{display:none;}}'
    '</style>\n'
    '<div class="ad-disclosure" role="note"><strong>【PR】</strong>本ページはアフィリエイト広告を含みます。'
    '<span class="ad-d-long">掲載している予約サイト等のリンクから予約・購入されると、当サイトに報酬が支払われる場合があります。</span>'
    '<a href="editorial-policy.html">詳しく</a>'
    '<span class="ad-d-long" lang="en"> / Contains affiliate ads.</span><span class="ad-d-long" lang="ko"> / 제휴 광고를 포함합니다.</span></div>\n'
)


def targets():
    for f in sorted(glob.glob(os.path.join(REPO_ROOT, "*.html"))):
        name = os.path.basename(f)
        if ONLY and name != ONLY:
            continue
        t = open(f, encoding="utf-8").read()
        if "a8.net" in t or "amzn.to" in t:  # golf-wear.html は Amazon アソシエイト
            yield name


def main():
    changed, already = [], []
    for name in targets():
        src = open(os.path.join(REPO_ROOT, name), encoding="utf-8", newline="").read()
        if MARKER in src:
            already.append(name); continue
        nl = "\r\n" if "\r\n" in src else "\n"
        m = re.search(r"<body[^>]*>\r?\n", src)
        assert m, name
        new = src[:m.end()] + SNIPPET.replace("\n", nl) + src[m.end():]
        changed.append(name)
        if APPLY:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(new)
    print(f"対象 {len(changed) + len(already)} / 追加 {len(changed)} / 既存 {len(already)}"
          + ("  [書き込み: " + ", ".join(r[-12:] for r in ROOTS) + "]" if APPLY else "  [DRY-RUN]"))
    if changed and not APPLY:
        print("  例:", changed[:8])


if __name__ == "__main__":
    main()
