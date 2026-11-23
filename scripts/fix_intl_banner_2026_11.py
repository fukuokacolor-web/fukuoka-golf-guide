#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
全60ページの EN/KO「International visitors / 해외 이용자 안내」帯の文言を、確認できた事実に合わせる (2026-11-23)。
  旧: 「じゃらん・楽天は日本の電話番号とクレジットカードが必要 (KO: 필수)」「英語/韓国語サポートは各コースの公式サイトで」→ どちらも出典なし。
      外国人向けページの旧記述 (海外の番号でよい) とも矛盾していた。
  新: 予約サイトは日本語のみ・多くのコースが海外の方に条件 (日本語話者/会員の同伴・入国当日不可など) を付けている
      (foreign_booking_rules.json・楽天GORA/じゃらん/公式のコース案内) → 予約前に条件を確認、の案内。
冪等。改行コードはそのまま。Usage: python scripts/fix_intl_banner_2026_11.py [--apply]
"""
import glob, os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
A = 'style="color:#5a4000;font-weight:700;text-decoration:underline;"'
PAIRS = [
    ("<span><strong>International visitors:</strong> Major Japanese booking sites (Jalan, Rakuten GORA) typically require a Japanese phone number and credit card. For English support, please use each course's <strong>official website link</strong> or contact the course directly. See our <a href=\"book-fukuoka-golf-foreigner.html\" " + A + ">step-by-step booking guide for foreigners</a> (English &amp; Korean).</span>",
     "<span><strong>International visitors:</strong> Jalan Golf and Rakuten GORA are in Japanese only, and many Fukuoka courses set conditions for overseas guests — for example a Japanese speaker or a club member in your group, or no booking for the day you arrive in Japan (courses' own notices, checked Nov 2026). Check the conditions before you book: <a href=\"book-fukuoka-golf-foreigner.html\" " + A + ">conditions by course</a>.</span>"),
    ("<span><strong>해외 이용자 안내:</strong> 일본 주요 예약 사이트(자란골프, 라쿠텐 GORA)는 일본 전화번호와 신용카드가 필수입니다. 한국어 지원은 각 코스의 <strong>공식 사이트 링크</strong>를 이용하시거나 직접 연락 주세요. <a href=\"book-fukuoka-golf-foreigner.html\" " + A + ">외국인용 단계별 예약 가이드</a>를 참고하세요 (영어/한국어 1500단어).</span>",
     "<span><strong>해외 이용자 안내:</strong> 자란골프·라쿠텐 GORA는 일본어로만 운영되며, 후쿠오카의 많은 골프장이 해외 고객에게 조건을 두고 있습니다 (일본어를 할 수 있는 사람 또는 회원 동반, 입국 당일 예약 불가 등 · 각 골프장 안내, 2026년 11월 확인). 예약 전에 조건을 확인하세요: <a href=\"book-fukuoka-golf-foreigner.html\" " + A + ">골프장별 조건 보기</a>.</span>"),
]
n = 0
for root in ROOTS:
    for p in glob.glob(os.path.join(root, "*.html")):
        s = open(p, encoding="utf-8", newline="").read()
        new = s
        for a, b in PAIRS:
            new = new.replace(a, b)
        if new != s:
            n += 1
            assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
            if APPLY:
                open(p, "w", encoding="utf-8", newline="").write(new)
print("files", n, "APPLIED" if APPLY else "DRY-RUN")
