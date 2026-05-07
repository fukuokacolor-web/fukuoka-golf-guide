# -*- coding: utf-8 -*-
"""
inject_ga4_tracking.py
全 HTML ファイルの click handler スクリプトを Plan B (GA4 tracking v2.1) 仕様に置換。

- 旧版: service 自動分類のみ → click_affiliate
- 新版: + cta_position 自動判定 (hero/ftv/sticky/price_featured/price_default/booking_grid/explore_nav/other)
        + internal_nav_click イベント (Phase 1A 逆流ナビ専用)

冪等性: マーカー 'GA4 tracking v2.1' で重複適用を防止。
両ディレクトリ (REPO_ROOT + PREVIEW_ROOT) を処理。
インデント保持: 元ファイルの行頭インデントを検出して新ブロックに適用。

使い方:
    python scripts/inject_ga4_tracking.py --dry-run        # 全ファイル確認
    python scripts/inject_ga4_tracking.py                   # 全ファイル適用
    python scripts/inject_ga4_tracking.py --only=hub-budget.html --dry-run
"""

import sys
import io
import re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

REPO_ROOT = Path(r"C:\Users\Owner\fukuoka-golf-guide")
PREVIEW_ROOT = Path(r"C:\Users\Owner\Documents\新しいPJ")
MARKER = 'GA4 tracking v2.1'

# 新スクリプトブロック (default no-indent。各行を _re_indent で prepend)
NEW_BLOCK = '''<!-- AFFILIATE_TRACKER -->
<script>
/* GA4 tracking v2.1 (2026-05-06): cta_position + internal_nav_click for Phase 1-3 measurement */
(function(){
  function classifyService(href) {
    if (/jalan/i.test(href)) return 'jalan';
    if (/rakuten/i.test(href) || /gora/i.test(href)) return 'rakuten_gora';
    if (/agoda/i.test(href)) return 'agoda';
    if (/skyticket/i.test(href) || /4B1DXO/.test(href)) return 'skyticket';
    if (/tabikobo|tabi|TM[0-9]|1NJRXE/i.test(href)) return 'tabimonogatari';
    if (/amazon|amzn/i.test(href)) return 'amazon';
    if (/a8\\.net/i.test(href)) return 'a8_other';
    return null;
  }
  function classifyCtaPosition(a) {
    if (a.classList.contains('hero-cta-btn') || a.closest('.hero-cta-btn')) return 'hero';
    if (a.classList.contains('ftv-cta-btn') || a.closest('.ftv-cta-strip')) return 'ftv';
    if (a.closest('#sticky-cta')) return 'sticky';
    if (a.closest('.price-card.featured')) return 'price_featured';
    if (a.closest('.price-card')) return 'price_default';
    if (a.closest('.booking-card')) return 'booking_grid';
    if (a.closest('section.related')) return 'explore_nav';
    return 'other';
  }
  function getLang() {
    var active = document.querySelector('.content.on');
    return active ? active.id.replace('c-','') : (document.documentElement.lang || 'ja');
  }
  function getPage() {
    return (location.pathname.split('/').pop() || 'index') + '';
  }
  document.addEventListener('click', function(e){
    var a = e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    if (typeof gtag !== 'function') return;
    var service = classifyService(h);
    var page = getPage();
    var lang = getLang();
    var ctaPos = classifyCtaPosition(a);
    var linkText = (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0,80);
    if (service) {
      gtag('event', 'click_affiliate', {
        service: service, page: page, lang: lang,
        cta_position: ctaPos,
        link_text: linkText, link_url: h.slice(0, 200)
      });
    } else if (ctaPos === 'explore_nav' && /\\.html?(\\?|#|$)/.test(h)) {
      var target = (h.split('?')[0].split('#')[0].split('/').pop() || '').replace(/\\.html?$/,'');
      gtag('event', 'internal_nav_click', {
        page: page, lang: lang,
        nav_section: 'explore_nav',
        target_page: target,
        link_text: linkText
      });
    }
  }, true);
})();
</script>'''

# 既存 click handler ブロック検出 regex
# - オプショナル先行コメント `<!-- AFFILIATE_TRACKER -->`
# - <script>...</script> ペアで
# - 中に addEventListener('click' と 'click_affiliate' を含む
OLD_BLOCK_PATTERN = re.compile(
    r"(?:<!--\s*AFFILIATE_TRACKER\s*-->\s*)?"
    r"<script>"
    r"(?:(?!</script>).)*?"
    r"addEventListener\(\s*'click'"
    r"(?:(?!</script>).)*?"
    r"'click_affiliate'"
    r"(?:(?!</script>).)*?"
    r"</script>",
    re.DOTALL,
)


def _detect_indent(content: str, pos: int) -> str:
    """pos 直前の行頭から (' ' or '\t') のみを抽出。"""
    line_start = content.rfind('\n', 0, pos) + 1
    indent = ''
    for c in content[line_start:pos]:
        if c in ' \t':
            indent += c
        else:
            break
    return indent


def _re_indent(block: str, indent: str) -> str:
    """ブロック各行の先頭に indent を prepend。空行は触らない。"""
    if not indent:
        return block
    return '\n'.join(
        (indent + line) if line.strip() else line
        for line in block.split('\n')
    )


def process_file(filepath: Path, dry_run: bool = False) -> dict:
    if not filepath.exists():
        return {'file': filepath.name, 'status': 'not_found'}
    content = filepath.read_text(encoding='utf-8')
    if MARKER in content:
        return {'file': filepath.name, 'status': 'already'}
    m = OLD_BLOCK_PATTERN.search(content)
    if not m:
        return {'file': filepath.name, 'status': 'no_old_handler'}

    # 元ブロックの行頭インデントを採用
    indent = _detect_indent(content, m.start())
    indented_new = _re_indent(NEW_BLOCK, indent)

    new_content = content[:m.start()] + indented_new + content[m.end():]
    if new_content == content:
        return {'file': filepath.name, 'status': 'noop'}

    if not dry_run:
        filepath.write_text(new_content, encoding='utf-8')

    return {
        'file': filepath.name,
        'status': 'replaced',
        'indent_chars': len(indent),
        'old_size': m.end() - m.start(),
        'new_size': len(indented_new),
    }


def main():
    dry_run = '--dry-run' in sys.argv
    only = None
    for a in sys.argv[1:]:
        if a.startswith('--only='):
            only = a.split('=', 1)[1]

    print(f"[inject_ga4_tracking] mode = {'DRY-RUN' if dry_run else 'LIVE'}")
    if only:
        print(f"[inject_ga4_tracking] target only = {only}")
    print()

    results = []
    for root in [REPO_ROOT, PREVIEW_ROOT]:
        for fp in sorted(root.glob('*.html')):
            if only and fp.name != only:
                continue
            r = process_file(fp, dry_run=dry_run)
            r['root'] = root.name
            results.append(r)

    # 詳細表示 (replaced のみ + only 指定時は全件)
    print(f"{'file':<46} {'root':<14} {'status':<16} {'detail'}")
    print('=' * 100)
    for r in results:
        s = r.get('status', '?')
        if s == 'replaced' or only:
            detail = ''
            if s == 'replaced':
                detail = f"indent={r.get('indent_chars')} {r.get('old_size')}->{r.get('new_size')} bytes"
            print(f"{r.get('file', ''):<46} {r.get('root', ''):<14} {s:<16} {detail}")

    # サマリ
    by_status = {}
    for r in results:
        s = r.get('status', '?')
        by_status[s] = by_status.get(s, 0) + 1
    print()
    print(f"[summary] total={len(results)}")
    for s, n in sorted(by_status.items()):
        print(f"          {s}: {n}")
    if dry_run:
        print('\n*** DRY-RUN: no files modified. Re-run without --dry-run to apply. ***')


if __name__ == '__main__':
    main()
