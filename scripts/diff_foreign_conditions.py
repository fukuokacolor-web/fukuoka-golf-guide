#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天GORA プラン説明の「海外の方向けの条件」の変化を、前回の取得結果と比べる (月次点検用・読み取り専用)。
  1. python scripts/scan_foreign_conditions.py <出力dir>        → <出力dir>/rakuten_foreign.json
  2. python scripts/diff_foreign_conditions.py <出力dir>/rakuten_foreign.json [前回json]
前回json の既定は scripts/.cache/rakuten_foreign_2026-11-23.json (foreign_booking_rules.json を作った時点)。
出力: 条件が増えた/消えたコースと文の抜粋。foreign_booking_rules.json に載っていないコースで新たに条件が出たら「未登録」と表示。
サイトのファイルは触らない。変化があっても自動では反映しない (公式・プラン本文を読んで手で foreign_booking_rules.json を直す)。
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
NEW = sys.argv[1]
OLD = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, ".cache", "rakuten_foreign_2026-11-23.json")
RULES = json.load(open(os.path.join(HERE, "..", "foreign_booking_rules.json"), encoding="utf-8"))["courses"]
# 条件らしい語 (「英語メニューあり」など案内だけのものと区別するため)
COND = re.compile(r"お断り|ご遠慮|同伴|必須|必要|できません|不可|限り|のみ")


def norm(s):
    # 抜粋は前後60字の窓なので、日付やプラン名の揺れで差分が出ないよう条件語の周りだけ比べる
    s = re.sub(r"\s+", "", s)
    return s


def key_sentences(hits):
    out = set()
    for h in hits:
        for sent in re.split(r"[。！!]", norm(h)):
            if re.search(r"海外|外国|日本語|渡航|訪日|インバウンド|国外|英語", sent) and COND.search(sent):
                out.add(sent[:80])
    return out


old = json.load(open(OLD, encoding="utf-8"))
new = json.load(open(NEW, encoding="utf-8"))
changed = 0
for f in sorted(set(old) | set(new)):
    slug = f.replace("course-", "").replace(".html", "")
    a = key_sentences(old.get(f, {}).get("hits", []))
    b = key_sentences(new.get(f, {}).get("hits", []))
    if f in old and f not in new:
        print(f"[取得なし] {f} (今回のスキャンに無い・楽天掲載が消えた可能性)")
        changed += 1
        continue
    if a == b:
        continue
    # 片方の文がもう片方の文の一部なら同じ扱い (抜粋窓のずれ)
    added = {x for x in b - a if not any(x in y or y in x for y in a)}
    removed = {x for x in a - b if not any(x in y or y in x for y in b)}
    if not added and not removed:
        continue
    changed += 1
    tag = "登録済" if slug in RULES else "未登録"
    print(f"[{tag}] {f}")
    for x in sorted(added):
        print(f"   + {x}")
    for x in sorted(removed):
        print(f"   - {x}")
print(f"\n比較: 前回 {len(old)} コース / 今回 {len(new)} コース / 変化あり {changed}")
print("変化なし" if changed == 0 else "→ 変化のあったコースは楽天のプラン本文・公式で確認し、foreign_booking_rules.json を手で直す")
