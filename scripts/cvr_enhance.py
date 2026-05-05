# -*- coding: utf-8 -*-
"""
cvr_enhance.py
CVR 改善: 標準 31 コースに以下 3 点を適用。

1. Hero 内 CTA — .hero-badges の直後に「📅 このコースを予約する →」ボタン挿入
2. Sticky CTA 価格込み化 — 既存 sttpl の JA/EN ラベルに hero-badge から抽出した価格を付与
3. KO Sticky 楽天ボタン追加 — 1 ボタン (Jalan のみ) → 2 ボタン (Jalan + Rakuten)

除外コース (4件・カスタムロジック保護):
  - course-fukuokacc.html / course-wakamatsu.html: 会員制 (Official Site Only)
  - course-akane.html: sticky CTA 非表示・楽天除外
  - course-genkai.html: sticky CTA 非表示・休場対応

冪等性: <!-- hero-cta --> マーカー + sttpl 内の <!-- v2-cvr --> で重複防止。
"""

import sys, io, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")

EXCLUDED = {
    'course-fukuokacc.html',
    'course-wakamatsu.html',
    'course-akane.html',
    'course-genkai.html',
}

# Hero CTA テキスト
HERO_CTA_TEXT = {
    'ja': '📅 このコースを予約する →',
    'en': '📅 Book This Course →',
    'ko': '📅 이 코스 예약하기 →',
}

# Hero CTA スタイル (hero-badges 直後・白半透明 hover で目立つ)
HERO_CTA_STYLE = (
    "display:inline-flex;align-items:center;gap:6px;margin-top:14px;"
    "padding:11px 22px;background:linear-gradient(135deg,#ff8a3d,#e8744c);"
    "color:#fff;font-weight:700;font-size:14px;border-radius:999px;"
    "text-decoration:none;box-shadow:0 6px 18px rgba(232,116,76,0.45);"
    "border:1px solid rgba(255,255,255,0.2);width:fit-content;"
)


def extract_jalan_url(content: str) -> str | None:
    """ftv-cta-strip 内の Jalan deep link を抽出"""
    m = re.search(r'class="ftv-cta-btn"[^>]*href="([^"]*golf-jalan\.net[^"]*)"', content)
    if m:
        return m.group(1)
    # フォールバック: 任意の golf-jalan.net deep link
    m = re.search(r'href="(https://px\.a8\.net[^"]*golf-jalan\.net[^"]*)"', content)
    return m.group(1) if m else None


def extract_lowest_price(content: str) -> str | None:
    """hero-badge から最安値を抽出 (例: ¥3,500〜)"""
    # JA hero-badge から探す
    m = re.search(
        r'<span class="hero-badge">💴\s*(?:From\s*)?(?:ビジター)?(¥[\d,]+)〜?',
        content
    )
    return m.group(1) if m else None


def inject_hero_cta(content: str, jalan_url: str) -> tuple[str, int]:
    """各言語の hero-badges 直後に CTA ボタンを挿入"""
    if '<!-- hero-cta -->' in content:
        return content, 0

    inserted = 0
    # 言語ごとに hero-badges の閉じ </div> を探して挿入
    # パターン: <div class="hero-badges">...</div> の直後 (ただし </div> 1個飛ばし)
    # 各 lang の hero-inner 内の hero-badges は3つあるはず

    # シンプルに: 各 lang の </div> for hero-badges の終わりを認識
    # hero-badges の形は: <div class="hero-badges">[badges]</div>
    # 単純な置換: hero-badges 内の最後の </span></div> のあとに CTA を挿入

    # 各 lang で異なる hero CTA テキストを使う必要がある
    # → 順番が JA, EN, KO になっていることに依存

    langs_in_order = ['ja', 'en', 'ko']
    pattern = re.compile(
        r'(<div class="hero-badges">.*?</div>)',
        re.DOTALL
    )
    matches = list(pattern.finditer(content))

    if len(matches) < 3:
        return content, 0

    # 後ろから挿入してオフセットを保つ
    new_content = content
    for i, lang in enumerate(reversed(langs_in_order)):
        idx = 2 - i  # 2, 1, 0 → KO, EN, JA
        m = matches[idx]
        cta_html = (
            f'\n        <!-- hero-cta -->\n'
            f'        <a href="{jalan_url}" '
            f'class="hero-cta-btn" target="_blank" rel="nofollow sponsored noopener" '
            f'style="{HERO_CTA_STYLE}" '
            f'onclick="if(window.trackAffiliate)trackAffiliate(\'jalan\',document.title,\'{lang}\',\'hero-cta\')">'
            f'{HERO_CTA_TEXT[lang]}</a>'
        )
        new_content = new_content[:m.end()] + cta_html + new_content[m.end():]
        inserted += 1

    return new_content, inserted


def upgrade_sttpl(content: str, price: str | None) -> tuple[str, bool]:
    """sttpl オブジェクトを価格込み + KO 2 ボタンに置換"""
    if '<!-- v2-cvr -->' in content:
        return content, False

    # 既存の sttpl ブロックを探す
    sttpl_pattern = re.compile(
        r'(var sttpl = \{)(.*?)(\};)',
        re.DOTALL
    )
    m = sttpl_pattern.search(content)
    if not m:
        return content, False

    body = m.group(2)
    # 標準パターンであることを確認 (Jalan + Rakuten がある)
    if 'sc-jalan' not in body or 'sc-rakuten' not in body:
        return content, False

    # 価格サフィックス (なければ空)
    price_ja = f' {price}〜' if price else ''
    price_en = f' {price}〜' if price else ''
    price_ko = f' {price}〜' if price else ''

    new_body = (
        '\n'
        '    // <!-- v2-cvr -->\n'
        '    ja:\'<a href="\'+JALAN+\'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 じゃらん' + price_ja + '</a>\'+\n'
        '       \'<a href="\'+RAKUTEN+\'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ 楽天GORA</a>\',\n'
        '    en:\'<a href="\'+JALAN+\'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 Jalan' + price_en + '</a>\'+\n'
        '       \'<a href="\'+RAKUTEN+\'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ Rakuten 🇯🇵</a>\',\n'
        '    ko:\'<a href="\'+JALAN+\'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 자란' + price_ko + ' 🇯🇵</a>\'+\n'
        '       \'<a href="\'+RAKUTEN+\'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ 라쿠텐 🇯🇵</a>\'\n'
        '  '
    )

    new_content = content[:m.start(2)] + new_body + content[m.end(2):]
    return new_content, True


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    if filepath.name in EXCLUDED:
        return {"file": filepath.name, "status": "excluded"}

    content = filepath.read_text(encoding='utf-8')
    original = content

    jalan_url = extract_jalan_url(content)
    if not jalan_url:
        return {"file": filepath.name, "status": "no_jalan_url"}

    price = extract_lowest_price(content)

    # Hero CTA 挿入
    content, hero_inserted = inject_hero_cta(content, jalan_url)

    # sttpl 強化
    content, sttpl_upgraded = upgrade_sttpl(content, price)

    if content == original:
        return {"file": filepath.name, "status": "already"}

    if not dry_run:
        filepath.write_text(content, encoding='utf-8')

    return {
        "file": filepath.name,
        "status": "ok",
        "hero": hero_inserted,
        "sttpl": "yes" if sttpl_upgraded else "no",
        "price": price or "none",
    }


def main():
    dry_run = "--dry-run" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = a.split("=", 1)[1]

    print(f"[cvr_enhance] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    if only:
        print(f"[cvr_enhance] target only = {only}")
    print()

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob("course-*.html")):
            if only and fp.name != only:
                continue
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    print(f"{'file':<35} {'root':<22} {'status':<14} {'detail'}")
    print("=" * 100)
    for r in results:
        detail = ""
        if r.get('status') == 'ok':
            detail = f"hero={r.get('hero')} sttpl={r.get('sttpl')} price={r.get('price')}"
        print(f"{r.get('file',''):<35} {r.get('root',''):<22} {r.get('status',''):<14} {detail}")

    n_ok = sum(1 for r in results if r.get('status') == 'ok')
    n_excluded = sum(1 for r in results if r.get('status') == 'excluded')
    n_already = sum(1 for r in results if r.get('status') == 'already')
    print()
    print(f"[summary] ok={n_ok}  excluded={n_excluded}  already={n_already}  total={len(results)}")
    if dry_run:
        print("\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
