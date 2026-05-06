# -*- coding: utf-8 -*-
"""
decoy_pricing_redesign.py
教授提案 Decoy + Default 価格カード再設計を 30 標準コースに適用。

行動経済学的介入:
- Center-stage 効果: featured カード (午後スルー) を視覚的中央に配置
- Decoy 効果: featured を周辺カードより明確に大きく強調 → 選びやすくする
- Hick's Law 軽減: 視線を1点 (中央 featured) に集中させ決定回避を防ぐ

実装方針:
- HTML 構造変更なし (CSS only) → アクセシビリティ・SEO 順序維持
- CSS `order` プロパティで視覚順序のみ変更:
  * デスクトップ (3 col): WEEKDAY → AFTERNOON featured → WEEKEND
  * モバイル (1 col): AFTERNOON featured → WEEKDAY → WEEKEND (featuredを最初に)
- featured カードに subtle scale + より大きい BEST VALUE バッジ

冪等性: /* decoy-v2 */ コメントマーカーで重複適用を防止。

除外コース: cvr_enhance.py と同じ 4 件
  - course-fukuokacc.html / course-wakamatsu.html (会員制・カスタム sticky)
  - course-akane.html / course-genkai.html (sticky 非表示)
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

# Decoy/Default CSS ブロック (既存 .price-card.featured ルールの直後に挿入)
DECOY_CSS = """
    /* decoy-v2: Center-stage + Default emphasis */
    .pricing-grid { align-items: center; }
    .pricing-grid > .price-card:nth-child(1) { order: 1; }
    .pricing-grid > .price-card:nth-child(2) { order: 3; }
    .pricing-grid > .price-card:nth-child(3) { order: 2; }
    .pricing-grid > .price-card.featured {
      border-width: 3px;
      box-shadow: 0 12px 32px rgba(232,116,76,0.20);
      z-index: 5;
      transform: translateY(-6px);
    }
    .pricing-grid > .price-card.featured:hover {
      transform: translateY(-10px);
      box-shadow: 0 18px 42px rgba(232,116,76,0.28);
    }
    .pricing-grid > .price-card.featured::before {
      content: '\\1F31F \\A0 BEST VALUE';
      font-size: 11px;
      padding: 5px 13px;
      top: -10px;
      right: 14px;
      box-shadow: 0 4px 12px rgba(232,116,76,0.35);
      letter-spacing: 0.08em;
    }
    @media (max-width: 900px) {
      .pricing-grid > .price-card.featured { transform: none; order: -1; }
      .pricing-grid > .price-card:nth-child(1) { order: 2; }
      .pricing-grid > .price-card:nth-child(2) { order: 3; }
    }
"""


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {"file": filepath.name, "status": "skip"}

    if filepath.name in EXCLUDED:
        return {"file": filepath.name, "status": "excluded"}

    content = filepath.read_text(encoding='utf-8')

    # 冪等性
    if 'decoy-v2' in content:
        return {"file": filepath.name, "status": "already"}

    # 既存 .price-card.featured::before ルールの行終端を見つけて、その直後に挿入
    # パターン: ".price-card.featured::before { ... 'Inter',sans-serif; }"
    pattern = re.compile(
        r"(\.price-card\.featured::before\s*\{[^}]+?\})",
        re.DOTALL
    )
    m = pattern.search(content)
    if not m:
        return {"file": filepath.name, "status": "no_anchor"}

    insert_pos = m.end()
    new_content = content[:insert_pos] + DECOY_CSS + content[insert_pos:]

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {"file": filepath.name, "status": "ok"}


def main():
    dry_run = "--dry-run" in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith("--only="):
            only = a.split("=", 1)[1]

    print(f"[decoy_pricing_redesign] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    if only:
        print(f"[decoy_pricing_redesign] target only = {only}")
    print()

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob("course-*.html")):
            if only and fp.name != only:
                continue
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    print(f"{'file':<35} {'root':<22} {'status'}")
    print("=" * 80)
    for r in results:
        print(f"{r.get('file',''):<35} {r.get('root',''):<22} {r.get('status','')}")

    n_ok = sum(1 for r in results if r.get('status') == 'ok')
    n_excluded = sum(1 for r in results if r.get('status') == 'excluded')
    n_already = sum(1 for r in results if r.get('status') == 'already')
    print()
    print(f"[summary] ok={n_ok}  excluded={n_excluded}  already={n_already}  total={len(results)}")
    if dry_run:
        print("\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***")


if __name__ == '__main__':
    main()
