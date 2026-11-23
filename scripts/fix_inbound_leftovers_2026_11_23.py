#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
外国人向けページ作り直し (e090a97) の取り残し:
  - hub-traveler: 記事紹介の「3 foreigner-friendly courses / 외국인 친화적 3코스」→ 条件一覧の紹介に
  - seo-meta.html (内部用のメタ文案ページ・未リンク): レイクサイドを「外国人歓迎」「英語・韓国語対応、インバウンド歓迎」
    「外国人ゴルファーのご予約はネットで24時間受付中」→ 楽天の案内では海外の方は正会員の同伴が必要 → 削除。noindex を追加
冪等。改行コードはそのまま。Usage: python scripts/fix_inbound_leftovers_2026_11_23.py [--apply]
"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
PLAN = {
    "hub-traveler.html": [
        ("7-step guide using Jalan Golf with Google Translate, plus 12 essential Japanese terms and 3 foreigner-friendly courses.",
         "What each Fukuoka course requires of overseas guests (a Japanese speaker or member in your group, no arrival-day bookings), plus the Japanese terms you will see."),
        ("자란골프 + 파파고 7단계 가이드, 필수 일본어 12개, 외국인 친화적 3코스 추천.",
         "후쿠오카 골프장별 해외 고객 조건 (일본어 가능자·회원 동반, 입국 당일 불가 등)과 자주 보는 일본어."),
    ],
    "seo-meta.html": [
        ("福岡レイクサイドカントリークラブ｜福岡のゴルフ場 外国人歓迎 午後スルー・ナイター対応",
         "福岡レイクサイドカントリークラブ｜福岡のゴルフ場 午後スルー・ナイター対応"),
        ("「福岡レイクサイドカントリークラブ」。英語・韓国語対応、インバウンド歓迎。全18ホール", "「福岡レイクサイドカントリークラブ」。全18ホール"),
        ("博多から車1時間。外国人ゴルファーのご予約はネットで24時間受付中。", "博多から車1時間。"),
        ('  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
         '  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n  <meta name="robots" content="noindex, nofollow">'),
    ],
}
for root in ROOTS:
    for f, rules in PLAN.items():
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        nl = "\r\n" if "\r\n" in s else "\n"
        new, miss = s, []
        for a, b in rules:
            a, b = a.replace("\n", nl), b.replace("\n", nl)
            if b in new and a not in new:
                continue
            if a in new:
                new = new.replace(a, b, 1)
            else:
                miss.append(a[:30])
        assert "\r\r" not in new
        print(root[-10:], f, "変更" if new != s else "変更なし", miss)
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
