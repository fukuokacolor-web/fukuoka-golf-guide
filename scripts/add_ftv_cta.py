#!/usr/bin/env python
"""Add first-view (FV) CTA strip to all course-*.html pages.

Inserts microcopy + Jalan button right after each hero section, before stats-bar.
3 languages (JA/EN/KO) per file. Adds CSS once per file.

Per affiliate council strategy (Sato): convert 'first-view-only' visitors
who don't scroll. Microcopy includes price transparency (Web vs walk-in)
and trust signals (free cancel, Ponta points).
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
COURSE_PAGES = sorted(ROOT.glob('course-*.html'))

JALAN_URL = ("https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2"
             "&a8ejpredirect=https%3A%2F%2Fgolf.jalan.net%2F")

CSS_BLOCK = """    .ftv-cta-strip {
      max-width: 720px;
      margin: -20px auto 32px;
      padding: 18px 22px 22px;
      background: #fff;
      border-radius: 14px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.1);
      border: 1px solid #f0e8d8;
      text-align: center;
      position: relative; z-index: 5;
    }
    .ftv-cta-microcopy {
      font-size: 12px;
      color: #5a5a5a;
      margin-bottom: 12px;
      letter-spacing: 0.02em;
    }
    .ftv-cta-microcopy strong {
      color: #c9572d;
      font-weight: 700;
    }
    .ftv-cta-btn {
      display: inline-block;
      padding: 13px 28px;
      background: linear-gradient(135deg, #ff8a3d, #e8744c);
      color: #fff;
      font-weight: 700;
      border-radius: 999px;
      text-decoration: none;
      box-shadow: 0 6px 18px rgba(232,116,76,0.35);
      transition: all .25s;
      font-size: 14px;
    }
    .ftv-cta-btn:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 26px rgba(232,116,76,0.45);
    }
"""


def cta_block(lang: str) -> str:
    if lang == 'ja':
        microcopy = '✅ <strong>キャンセル無料</strong>（前日まで）｜ Pontaポイント1%還元 ｜ Web予約で平均¥3,000お得'
        btn = '📅 じゃらんゴルフでこのコースを予約する →'
    elif lang == 'en':
        microcopy = '✅ <strong>Free cancel</strong> (until day before) ｜ Ponta Points 1% back ｜ Save avg. ¥3,000 vs walk-in'
        btn = '📅 Book this course on Jalan Golf →'
    else:  # ko
        microcopy = '✅ <strong>무료 취소</strong>（전날까지）｜ 폰타포인트 1% 적립 ｜ Web 예약으로 평균 ¥3,000 절약'
        btn = '📅 자란골프로 이 코스 예약하기 →'

    return (
        '  <div class="ftv-cta-strip">\n'
        f'    <div class="ftv-cta-microcopy">{microcopy}</div>\n'
        f'    <a href="{JALAN_URL}" class="ftv-cta-btn" target="_blank" '
        f'rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate(\'jalan\',document.title,\'{lang}\',\'ftv-cta\')">'
        f'{btn}</a>\n'
        '  </div>'
    )


# Pattern: hero close + (optional dresscode-strip etc.) + stats-bar open
# Allows variable whitespace and an optional dresscode-strip block (kokura)
PATTERN = re.compile(
    r'(  </section>'
    r'(?:\n\n  <div class="dresscode-strip">[^<]*(?:<[^/][^>]*>[^<]*</[^>]+>[^<]*)*</div>)?'
    r')\n+(  <div class="stats-bar">)',
    re.DOTALL
)


def process_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')

    if '.ftv-cta-strip' in text:
        return f"SKIP (already has CTA): {path.name}"

    ja_start = text.find('<div id="c-ja"')
    en_start = text.find('<div id="c-en"')
    ko_start = text.find('<div id="c-ko"')

    if ja_start < 0 or en_start < 0 or ko_start < 0:
        return f"SKIP (missing language sections): {path.name}"

    # Split by language sections
    pre = text[:ja_start]
    ja_section = text[ja_start:en_start]
    en_section = text[en_start:ko_start]
    ko_section = text[ko_start:]

    # Replace pattern in each section (count=1 so only first match per section)
    def replace_lang(section: str, lang: str) -> tuple[str, bool]:
        new_section, n = PATTERN.subn(
            f'\\1\n\n{cta_block(lang)}\n\n\\2',
            section,
            count=1
        )
        return new_section, n > 0

    ja_new, ja_ok = replace_lang(ja_section, 'ja')
    en_new, en_ok = replace_lang(en_section, 'en')
    ko_new, ko_ok = replace_lang(ko_section, 'ko')

    if not (ja_ok and en_ok and ko_ok):
        missing = []
        if not ja_ok: missing.append('ja')
        if not en_ok: missing.append('en')
        if not ko_ok: missing.append('ko')
        return f"WARN (no pattern match in {','.join(missing)}): {path.name}"

    new_text = pre + ja_new + en_new + ko_new

    # Add CSS — insert before .hero-title CSS rule
    if '.hero-title {' in new_text:
        new_text = new_text.replace(
            '    .hero-title {',
            CSS_BLOCK + '    .hero-title {',
            1
        )
    else:
        return f"WARN (no .hero-title CSS anchor): {path.name}"

    path.write_text(new_text, encoding='utf-8')
    return f"UPDATED: {path.name}"


def main():
    print(f"Found {len(COURSE_PAGES)} course pages")
    counts = {'UPDATED': 0, 'SKIP': 0, 'WARN': 0}
    for path in COURSE_PAGES:
        result = process_file(path)
        print(result)
        for k in counts:
            if result.startswith(k):
                counts[k] += 1
    print()
    print(f"Summary: UPDATED={counts['UPDATED']}, SKIP={counts['SKIP']}, WARN={counts['WARN']}")


if __name__ == '__main__':
    main()
