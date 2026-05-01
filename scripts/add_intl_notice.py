#!/usr/bin/env python
"""Add international booking notice to EN/KO sections of all pages.

Inserts a warning banner immediately after each <div id="c-en"...>
and <div id="c-ko"...> opening tag, alerting non-Japanese visitors
that Jalan/Rakuten require Japanese phone/card.

Per inbound council recommendation (金星誠 + David Chen):
"Trust transfer loss" risk if non-JP visitors click Jalan and hit
a JP-only payment wall. Quick mitigation: label expectations.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

NOTICE_EN = '''  <div style="max-width:880px;margin:18px auto 0;padding:14px 18px;background:#fff8e1;border:1px solid #f0c75e;border-left:4px solid #c9a227;border-radius:8px;font-size:13px;line-height:1.6;color:#5a4000;display:flex;gap:10px;align-items:flex-start;">
    <span style="font-size:18px;flex-shrink:0;">⚠️</span>
    <span><strong>International visitors:</strong> Major Japanese booking sites (Jalan, Rakuten GORA) typically require a Japanese phone number and credit card. For English support, please use each course\'s <strong>official website link</strong> or contact the course directly. Detailed inbound booking guide coming soon.</span>
  </div>

'''

NOTICE_KO = '''  <div style="max-width:880px;margin:18px auto 0;padding:14px 18px;background:#fff8e1;border:1px solid #f0c75e;border-left:4px solid #c9a227;border-radius:8px;font-size:13px;line-height:1.6;color:#5a4000;display:flex;gap:10px;align-items:flex-start;">
    <span style="font-size:18px;flex-shrink:0;">⚠️</span>
    <span><strong>해외 이용자 안내:</strong> 일본 주요 예약 사이트(자란골프, 라쿠텐 GORA)는 일본 전화번호와 신용카드가 필수입니다. 한국어 지원은 각 코스의 <strong>공식 사이트 링크</strong>를 이용하시거나 직접 연락 주세요. 해외 이용자용 예약 가이드 곧 공개 예정.</span>
  </div>

'''

# Marker used to detect already-inserted notices (avoid duplicates)
MARKER_EN = "International visitors:"
MARKER_KO = "해외 이용자 안내:"

# Pattern: capture the opening div tag for each lang section
PATTERN_EN = re.compile(r'(<div id="c-en"[^>]*>\s*\n)')
PATTERN_KO = re.compile(r'(<div id="c-ko"[^>]*>\s*\n)')


def process_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    original = text
    en_added = False
    ko_added = False

    # Skip if already has the notice
    if MARKER_EN not in text:
        m = PATTERN_EN.search(text)
        if m:
            text = text[:m.end()] + '\n' + NOTICE_EN + text[m.end():]
            en_added = True

    if MARKER_KO not in text:
        m = PATTERN_KO.search(text)
        if m:
            text = text[:m.end()] + '\n' + NOTICE_KO + text[m.end():]
            ko_added = True

    if text != original:
        path.write_text(text, encoding='utf-8')

    flags = []
    if en_added: flags.append('EN')
    if ko_added: flags.append('KO')
    if flags:
        return f"UPDATED [{','.join(flags)}]: {path.name}"
    elif MARKER_EN in original or MARKER_KO in original:
        return f"SKIP (already has notice): {path.name}"
    else:
        return f"SKIP (no c-en or c-ko section): {path.name}"


def main():
    # Target: course-*.html, hub-*.html, area-*.html, index.html
    targets = []
    targets.extend(sorted(ROOT.glob('course-*.html')))
    targets.extend(sorted(ROOT.glob('hub-*.html')))
    targets.extend(sorted(ROOT.glob('area-*.html')))
    if (ROOT / 'index.html').exists():
        targets.append(ROOT / 'index.html')

    counts = {'UPDATED': 0, 'SKIP': 0}
    for path in targets:
        result = process_file(path)
        print(result)
        if result.startswith('UPDATED'): counts['UPDATED'] += 1
        else: counts['SKIP'] += 1
    print()
    print(f"Total: {counts['UPDATED']} files updated, {counts['SKIP']} skipped")


if __name__ == '__main__':
    main()
