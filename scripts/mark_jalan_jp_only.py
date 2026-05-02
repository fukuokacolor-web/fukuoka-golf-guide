#!/usr/bin/env python
"""Phase B: Add '(JP only)' marker to Jalan/Rakuten buttons in EN/KO sections.

Phase A added a banner at the top of each EN/KO section.
Phase B adds inline markers right at the button click point — so users
see the JP-only limitation at the exact moment of decision, not just at
section entry.

Strategy: surgical text replacement only inside EN/KO button labels.
- 'Book on Jalan Golf' -> 'Book on Jalan Golf (JP site)'
- 'Search on Jalan Golf' -> 'Search on Jalan Golf (JP site)'
- '자란골프에서 예약' -> '자란골프에서 예약 (일본어)'
- etc.

Idempotent (skip if marker already present).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

# (search, replace) pairs — applied only inside <div id="c-en"|"c-ko"> sections
EN_REPLACEMENTS = [
    ("Book on Jalan Golf →", "Book on Jalan Golf 🇯🇵 (JP site) →"),
    ("Search on Jalan Golf →", "Search on Jalan Golf 🇯🇵 (JP site) →"),
    ("Book on Rakuten GORA →", "Book on Rakuten GORA 🇯🇵 (JP site) →"),
    ("📅 Jalan", "📅 Jalan 🇯🇵 (JP)"),
    ("🏌️ Rakuten GORA", "🏌️ Rakuten GORA 🇯🇵 (JP)"),
    ("Book this course on Jalan Golf →", "Book on Jalan Golf 🇯🇵 (JP site) →"),
    ("📅 Book courses on Jalan", "📅 Jalan Golf 🇯🇵 (JP site)"),
    ("📅 Book Chikuho courses on Jalan →", "📅 Jalan Golf 🇯🇵 (JP site) →"),
    ("Check Jalan availability →", "Jalan Golf 🇯🇵 (JP site) →"),
    ("Book on Jalan →", "Jalan 🇯🇵 (JP site) →"),
    ("📅 Search Jalan", "📅 Jalan 🇯🇵 (JP)"),
]

KO_REPLACEMENTS = [
    ("자란골프로 이 코스 예약하기 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("자란골프에서 예약 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("자란골프로 코스 예약", "자란골프 🇯🇵 (일본어 사이트)"),
    ("📅 자란골프", "📅 자란골프 🇯🇵 (일본어)"),
    ("자란골프로 치쿠호 6코스 예약 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("자란골프로 치쿠호 4코스 예약 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("자란골프 빈자리 확인 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("자란골프 예약 →", "자란골프 🇯🇵 (일본어 사이트) →"),
    ("🏌️ 라쿠텐 GORA", "🏌️ 라쿠텐 GORA 🇯🇵 (일본어)"),
]

MARKER = "🇯🇵 (JP"  # idempotency check


def process_file(path: Path) -> str:
    text = path.read_text(encoding='utf-8')
    original = text

    en_start = text.find('<div id="c-en"')
    ko_start = text.find('<div id="c-ko"')
    if en_start < 0 and ko_start < 0:
        return f"SKIP (no EN/KO sections): {path.name}"

    # Determine ranges
    if en_start >= 0:
        en_end = ko_start if ko_start > en_start else len(text)
        en_section = text[en_start:en_end]
        en_new = en_section
        for old, new in EN_REPLACEMENTS:
            if MARKER in old:  # don't apply if pattern already has marker
                continue
            # Skip already-marked occurrences inside the section
            en_new = en_new.replace(old, new)
        text = text[:en_start] + en_new + text[en_end:]

    if ko_start >= 0:
        ko_start2 = text.find('<div id="c-ko"')  # re-find after EN edit
        ko_end = len(text)
        ko_section = text[ko_start2:ko_end]
        ko_new = ko_section
        for old, new in KO_REPLACEMENTS:
            if MARKER in old:
                continue
            ko_new = ko_new.replace(old, new)
        text = text[:ko_start2] + ko_new + text[ko_end:]

    if text != original:
        path.write_text(text, encoding='utf-8')
        return f"UPDATED: {path.name}"
    return f"NOCHANGE: {path.name}"


def main():
    targets = []
    targets.extend(sorted(ROOT.glob('course-*.html')))
    targets.extend(sorted(ROOT.glob('hub-*.html')))
    targets.extend(sorted(ROOT.glob('area-*.html')))

    counts = {'UPDATED': 0, 'NOCHANGE': 0, 'SKIP': 0}
    for path in targets:
        result = process_file(path)
        print(result)
        for k in counts:
            if result.startswith(k):
                counts[k] += 1
    print()
    print(f"Total: UPDATED={counts['UPDATED']}, NOCHANGE={counts['NOCHANGE']}, SKIP={counts['SKIP']}")


if __name__ == '__main__':
    main()
