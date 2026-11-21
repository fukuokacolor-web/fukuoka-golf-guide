#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天のみで予約できる あかね・油山 の最上部予約帯 (ftv-cta-strip) にボタンが無かったのを直す (バグ修正・3言語)。
  あかね: 帯はマイクロコピーだけ・下部の固定バー (sticky) も非表示 → 楽天GORAボタンを足し、固定バーを楽天で表示
          (楽天 c_id 400001 で予約可と 2026-10-24 確認済。CLAUDE.md §9-4)。
  油山  : 帯はマイクロコピーだけで、しかも文言がじゃらん用 (キャンセル無料・Ponta) → 楽天用の文言 + 楽天GORAボタン。
  ボタンの文言・GA4 は他の楽天のみコース (サンレイク等) と同じ。リンクはページ内の楽天リンク (A8→楽天アフィリ)。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/fix_ftv_rakuten_only_2026_11.py [--apply]
"""
import os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
MARKER = "ftv-rakuten-only-fix"
LABEL = {"ja": "🏌️ 楽天GORAでこのコースを予約する →",
         "en": "🏌️ Book this course on Rakuten GORA →",
         "ko": "🏌️ 라쿠텐 GORA에서 이 코스 예약 →"}
MICRO = {"ja": "✅ 楽天ポイントが貯まる・使える ｜ 季節により料金変動・最新空き状況をチェック",
         "en": "✅ Earn & use Rakuten points ｜ Rates vary by season — check live availability",
         "ko": "✅ 라쿠텐 포인트 적립·사용 가능 ｜ 시기별 요금 변동·최신 빈자리 확인"}
ABURA_OLD = {"ja": "✅ <strong>キャンセル無料</strong>（前日まで）｜ Pontaポイント1%還元 ｜ 季節により料金変動・最新空き状況をチェック",
             "en": "✅ <strong>Free cancel</strong> (until day before) ｜ Ponta Points 1% back ｜ Seasonal pricing — check current rate",
             "ko": "✅ <strong>무료 취소</strong>（전날까지）｜ 폰타포인트 1% 적립 ｜ 시즌별 요금 변동 — 최신 요금 확인"}
AKANE_HIDE = re.compile(r"  // あかねCC: Sticky CTA 非表示[^\n]*\r?\n  \(function\(\)\{\r?\n    var el = document.getElementById\('sticky-cta'\);\r?\n    if \(el\) el.style.display = 'none';\r?\n  \}\)\(\);\r?\n")
AKANE_STICKY = """  // ftv-rakuten-only-fix: あかねCC は楽天GORAで予約可 (c_id 400001・2026-10-24 確認) → 固定バーを楽天で表示
  var RAKUTEN="{rak}";
  var sttpl = {{
    ja:'<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank" style="max-width:360px;">🏌️ 楽天GORAで予約する</a>',
    en:'<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank" style="max-width:360px;">🏌️ Book on Rakuten GORA</a>',
    ko:'<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank" style="max-width:360px;">🏌️ 라쿠텐 GORA에서 예약하기</a>'
  }};
  function renderStickyCTA(){{
    var el = document.getElementById('sticky-cta');
    if (!el) return;
    var active = document.querySelector('.content.on');
    var lang = active ? active.id.replace('c-','') : 'ja';
    el.innerHTML = sttpl[lang] || sttpl.ja;
  }}
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', renderStickyCTA);
  else renderStickyCTA();
"""

for root in ROOTS:
    for f in ["course-akane.html", "course-aburayama.html"]:
        p = os.path.join(root, f)
        s = open(p, encoding="utf-8", newline="").read()
        if MARKER in s:
            print(root[-10:], f, "already"); continue
        nl = "\r\n" if "\r\n" in s else "\n"
        rak = re.search(r'href="(https://rpx\.a8\.net/[^"]+)"', s).group(1)
        assert "c_id%252F" in rak
        new, done = s, []
        for lang in ["ja", "en", "ko"]:
            old_micro = ABURA_OLD[lang] if f == "course-aburayama.html" else MICRO[lang]
            old = f'<div class="ftv-cta-strip">{nl}    <div class="ftv-cta-microcopy">{old_micro}</div>{nl}    </div>'
            btn = (f'<a href="{rak}" class="ftv-cta-btn" target="_blank" rel="nofollow sponsored noopener" '
                   f"onclick=\"if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'{lang}','ftv-cta')\">{LABEL[lang]}</a>")
            rep = (f'<div class="ftv-cta-strip"><!-- {MARKER} -->{nl}    <div class="ftv-cta-microcopy">{MICRO[lang]}</div>{nl}'
                   f'    {btn}{nl}  </div>')
            if new.count(old) == 1:
                new = new.replace(old, rep); done.append(lang)
        if f == "course-akane.html":
            m = AKANE_HIDE.search(new)
            if m:
                new = new[:m.start()] + AKANE_STICKY.format(rak=rak).replace("\n", nl) + new[m.end():]
                done.append("sticky")
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        assert "\r\r" not in new
        print(root[-10:], f, done)
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
