"""
Phase 4 Task C: LP 3本 title / meta description 最適化スクリプト
作成日: 2026-05-29 (Day 28 直前準備)
実行条件: OBSERVATION_PLAYBOOK §5 で Task C 着手が決定した後
冪等: MARKER コメントで重複適用防止
dry-run: --dry-run フラグで差分プレビューのみ
両ディレクトリ: REPO + PREVIEW 両方に適用

Usage:
  python scripts/phase4_lp_title_fix.py --dry-run
  python scripts/phase4_lp_title_fix.py

注意:
  GSC の実データを確認してから title を調整すること。
  以下の PROPOSED_* 定数を Day 28 当日のデータに合わせて変更可能。
"""
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

DRY_RUN = '--dry-run' in sys.argv

REPO   = r'C:\Users\Owner\fukuoka-golf-guide'
PREVIEW = r'C:\Users\Owner\Documents\新しいPJ'
ROOTS  = [REPO, PREVIEW]

MARKER = '<!-- phase4-lp-title-v1 -->'

# ── 修正定義 ────────────────────────────────────────────────
# 各 LP の現行値と提案値。Day 28 当日に GSC データを見て調整可能。

FIXES = [
    {
        'file': 'book-fukuoka-cheap.html',
        'old_title': '福岡ゴルフ 平日¥6,000以下24コース最安比較｜福岡ゴルフ場ガイド',
        'new_title': '福岡ゴルフ格安まとめ｜平日¥3,000台〜24コース最安値比較【2026年版】',
        'old_meta': '福岡35コース中、平日¥6,000以下で予約できる24コースを最安価格順に完全比較。¥3,000台から¥6,000台名門まで、じゃらんゴルフ deep link で即予約可能。',
        'new_meta': '福岡ゴルフ格安ランキング。平日¥3,000台〜¥6,000以下の24コースを最安値順に徹底比較。じゃらんゴルフ deep link で今すぐ空き確認。料金・コース特徴・穴場コースも掲載。',
    },
    {
        'file': 'book-fukuoka-tomorrow.html',
        'old_title': '福岡ゴルフ 当日・明日予約OK 15コース即枠取得ガイド｜福岡ゴルフ場ガイド',
        'new_title': '福岡ゴルフ当日予約できるコース15選【今日・明日OK】じゃらん即枠ガイド',
        'old_meta': '福岡ゴルフ場の当日・明日予約に強い15コース。じゃらんゴルフの「今日・明日プラン」フィルターで即枠取得。大手チェーン優先・平日午後スルー狙い・雨予報前日活用の4ステップ。',
        'new_meta': '福岡ゴルフ当日予約OK！今日・明日でも枠が取りやすい15コースを厳選。じゃらんゴルフの即枠フィルターの使い方、予約成功率を上げる4ステップを解説。',
    },
    {
        'file': 'book-fukuoka-solo.html',
        'old_title': '福岡ゴルフ 1人予約マッチング率高い12コース完全ガイド｜福岡ゴルフ場ガイド',
        'new_title': '福岡ゴルフ一人予約【2026年版】マッチング率高い12コースとじゃらんの使い方',
        'old_meta': '福岡ゴルフ場の「1人予約」マッチング率が高い12コース。じゃらんゴルフのひとり予約機能の使い方、マッチング成功率、ソロゴルフのマナーまで完全解説。',
        'new_meta': '福岡ゴルフ一人予約ガイド2026年版。マッチング率が高い12コースを厳選。じゃらんゴルフのひとり予約機能の使い方、成功のコツ、ソロゴルフのマナーまで完全解説。',
    },
]


def apply_fix(root, fix):
    path = os.path.join(root, fix['file'])
    if not os.path.exists(path):
        print(f'  [NOT FOUND] {path}')
        return 'not_found'

    with open(path, encoding='utf-8') as f:
        content = f.read()

    if MARKER in content:
        print(f'  [ALREADY]   {fix["file"]} in {os.path.basename(root)}')
        return 'already'

    original = content

    # title
    old_t = f'<title>{fix["old_title"]}</title>'
    new_t = f'<title>{fix["new_title"]}</title>'
    if old_t not in content:
        print(f'  [NO MATCH]  title not found in {fix["file"]} ({os.path.basename(root)})')
        return 'no_match'
    content = content.replace(old_t, new_t, 1)

    # meta description
    old_m = f'content="{fix["old_meta"]}"'
    new_m = f'content="{fix["new_meta"]}"'
    if old_m not in content:
        print(f'  [NO MATCH]  meta description not found in {fix["file"]} ({os.path.basename(root)})')
        # title was already replaced - revert
        content = original
        return 'no_match'
    content = content.replace(old_m, new_m, 1)

    # insert marker before </head>
    content = content.replace('</head>', f'  {MARKER}\n</head>', 1)

    if DRY_RUN:
        print(f'  [DRY-RUN]   would update {fix["file"]} in {os.path.basename(root)}')
        print(f'              title: {fix["old_title"][:40]}...')
        print(f'                  → {fix["new_title"][:40]}...')
        return 'would_replace'

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  [UPDATED]   {fix["file"]} in {os.path.basename(root)}')
    return 'replaced'


def main():
    print(f'{"*** DRY-RUN ***" if DRY_RUN else "*** APPLYING Phase 4 LP title fixes ***"}')
    print()

    stats = {'replaced': 0, 'already': 0, 'no_match': 0, 'not_found': 0, 'would_replace': 0}

    for fix in FIXES:
        print(f'[{fix["file"]}]')
        for root in ROOTS:
            r = apply_fix(root, fix)
            stats[r] = stats.get(r, 0) + 1
        print()

    print('Summary:')
    for k, v in stats.items():
        if v:
            print(f'  {k}: {v}')

    if DRY_RUN:
        print('\n*** DRY-RUN *** (実行するには --dry-run を外してください)')
    else:
        print('\nDONE — git add して commit してください')
        print('  git add book-fukuoka-cheap.html book-fukuoka-tomorrow.html book-fukuoka-solo.html')
        print('  git commit -m "perf(seo): LP3本 title/meta 最適化 (Phase 4 Task C)"')


if __name__ == '__main__':
    main()
