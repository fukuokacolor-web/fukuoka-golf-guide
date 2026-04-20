#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Growth upgrades (2026-04-20):
 1. GA4 tag を全HTMLに（漏れ補完、index.html含む）
 2. Affiliate click GA4 event tracker (click_affiliate) を全HTMLに注入
 3. コース28ページにモバイル用 Sticky 予約CTA を注入（JA/EN/KO自動切替）
 4. 実行回数安全（idempotent）
"""
import os, re, glob, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/Owner/fukuoka-golf-guide'
GA_ID = 'G-PENH0Z4VT7'
MARK_GA = '<!-- GA4_TAG -->'
MARK_TRACKER = '<!-- AFFILIATE_TRACKER -->'
MARK_STICKY = '<!-- STICKY_CTA -->'

GA_SNIPPET = f'''{MARK_GA}
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
  </script>
'''

TRACKER_SNIPPET = f'''{MARK_TRACKER}
<script>
(function(){{
  document.addEventListener('click', function(e){{
    var a = e.target.closest('a[href]');
    if (!a) return;
    var h = a.getAttribute('href') || '';
    var service = null;
    if (/jalan/i.test(h)) service = 'jalan';
    else if (/rakuten/i.test(h) || /gora/i.test(h)) service = 'rakuten_gora';
    else if (/agoda/i.test(h)) service = 'agoda';
    else if (/skyticket/i.test(h)) service = 'skyticket';
    else if (/tabikobo|tabi|TM[0-9]|1NJRXE/i.test(h)) service = 'tabimonogatari';
    else if (/amazon|amzn/i.test(h)) service = 'amazon';
    else if (/a8\\.net/i.test(h)) service = 'a8_other';
    if (!service) return;
    var page = (location.pathname.split('/').pop() || 'index') + '';
    var active = document.querySelector('.content.on');
    var lang = active ? active.id.replace('c-','') : 'ja';
    if (typeof gtag === 'function') {{
      gtag('event', 'click_affiliate', {{
        service: service,
        page: page,
        lang: lang,
        link_text: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0,80),
        link_url: h.slice(0, 200)
      }});
    }}
  }}, true);
}})();
</script>
'''

JALAN_URL = "https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&amp;a8ejpredirect=https%3A%2F%2Fgolf.jalan.net%2F"
RAKUTEN_URL = "https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+7O29U&amp;rakuten=y&amp;a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttp%253A%252F%252Fgora.golf.rakuten.co.jp%252F%26m%3Dhttp%253A%252F%252Fwww.rakuten.co.jp%252F"

STICKY_SNIPPET = f'''{MARK_STICKY}
<style>
  #sticky-cta {{ position:fixed; bottom:0; left:0; right:0; z-index:200;
    background:rgba(255,255,255,0.98); border-top:2px solid #e0c0a0;
    box-shadow:0 -4px 14px rgba(0,0,0,0.14); padding:8px 10px 10px;
    display:flex; gap:6px; justify-content:center; align-items:center; }}
  #sticky-cta .sc-btn {{ flex:1; max-width:200px; text-align:center;
    padding:11px 8px; border-radius:10px; font-weight:800; font-size:0.86rem;
    color:#fff; text-decoration:none; line-height:1.25;
    box-shadow:0 2px 5px rgba(0,0,0,0.18); }}
  #sticky-cta .sc-btn:active {{ transform:translateY(1px); }}
  #sticky-cta .sc-jalan   {{ background:linear-gradient(135deg,#ff8c00,#e36b00); }}
  #sticky-cta .sc-rakuten {{ background:linear-gradient(135deg,#c81d1d,#8f0000); }}
  body {{ padding-bottom:76px; }}
  @media (min-width:900px) {{
    #sticky-cta {{ max-width:680px; left:50%; transform:translateX(-50%); right:auto;
      border-radius:14px 14px 0 0; }}
  }}
</style>
<div id="sticky-cta" aria-label="予約CTA"></div>
<script>
(function(){{
  var JALAN="{JALAN_URL}";
  var RAKUTEN="{RAKUTEN_URL}";
  var tpl = {{
    ja:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 じゃらん</a>'+
       '<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ 楽天GORA</a>',
    en:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 Jalan</a>'+
       '<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ Rakuten GORA</a>',
    ko:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank" style="max-width:360px;">📅 자란골프에서 예약하기</a>'
  }};
  function render(){{
    var el = document.getElementById('sticky-cta');
    if (!el) return;
    var active = document.querySelector('.content.on');
    var lang = active ? active.id.replace('c-','') : 'ja';
    el.innerHTML = tpl[lang] || tpl.ja;
  }}
  if (document.readyState === 'loading')
    document.addEventListener('DOMContentLoaded', render);
  else render();
  document.addEventListener('click', function(e){{
    if (e.target.closest('.lbtn')) setTimeout(render, 10);
  }});
}})();
</script>
'''


def ensure_ga4(html):
    """GA4タグが無ければ追加"""
    if GA_ID in html or 'gtag' in html:
        return html, False
    new = html.replace('</head>', GA_SNIPPET + '</head>', 1)
    return new, new != html


def ensure_tracker(html):
    """affiliate tracker を head 直前に追加（idempotent）"""
    if MARK_TRACKER in html:
        return html, False
    new = html.replace('</head>', TRACKER_SNIPPET + '</head>', 1)
    return new, new != html


def ensure_sticky_cta(html):
    """course-*.html限定 sticky CTA を </body> 直前に追加"""
    if MARK_STICKY in html:
        return html, False
    new = html.replace('</body>', STICKY_SNIPPET + '\n</body>', 1)
    return new, new != html


def main():
    all_html = sorted(glob.glob(os.path.join(BASE, '*.html')))
    course_files = [f for f in all_html if os.path.basename(f).startswith('course-')]

    ga_added = 0
    tracker_added = 0
    sticky_added = 0

    for f in all_html:
        with open(f, encoding='utf-8') as fp:
            html = fp.read()
        orig = html
        html, c1 = ensure_ga4(html)
        if c1: ga_added += 1
        html, c2 = ensure_tracker(html)
        if c2: tracker_added += 1
        if f in course_files:
            html, c3 = ensure_sticky_cta(html)
            if c3: sticky_added += 1
        if html != orig:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(html)

    print(f"GA4 added to        : {ga_added} files")
    print(f"Tracker added to    : {tracker_added} files")
    print(f"Sticky CTA added to : {sticky_added} course files (of {len(course_files)})")


if __name__ == '__main__':
    main()
