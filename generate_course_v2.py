#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
course_data.json からテンプレートに流し込んで
全 28 コース分の course-*-v2.html を生成。
"""
import sys, io, re, json, html as html_module
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = Path(r'C:/Users/Owner/fukuoka-golf-guide')
DATA = BASE / 'course_data.json'

# 共通のアフィリエイトURL
JALAN_URL = "https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf.jalan.net%2F"
RAKUTEN_URL = "https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+7O29U&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttp%253A%252F%252Fgora.golf.rakuten.co.jp%252F%26m%3Dhttp%253A%252F%252Fwww.rakuten.co.jp%252F"

def clean_name(n):
    if not n: return ''
    # 先頭の絵文字を除去
    return re.sub(r'^[⛳🌙🌊🌄🌲🏌️‍♂️]+\s*', '', n).strip()

def parse_fee_amount(s):
    """『約9,500〜21,500円』『¥9,500–¥21,500』『약 9,500〜21,500엔 (약..)』等から
       min_amount / range_suffix / extra_tag を取り出す"""
    if not s:
        return '', '', ''
    # 韓国の換算タグを分離
    krw_tag = ''
    m = re.search(r'(<span[^>]*>[^<]*만원[^<]*</span>)', s)
    if m:
        krw_tag = m.group(1)
        s = s.replace(krw_tag, '').strip()
    # 「約」プレフィックス除去・「円」「엔」除去
    s = re.sub(r'^約\s*', '', s)
    s = re.sub(r'^약\s*', '', s)
    s = re.sub(r'円$', '', s.strip())
    s = re.sub(r'엔$', '', s.strip()).strip()
    s = s.strip()
    # ¥や金額パターン抽出
    # e.g. "9,500〜21,500" "9,500–21,500" "¥9,500–¥21,500" "5,000"
    s_no_yen = s.replace('¥', '').replace('￥', '').strip()
    parts = re.split(r'\s*[〜～\-–]\s*', s_no_yen, maxsplit=1)
    amt = parts[0].strip() if parts else ''
    rng = '〜' + parts[1].strip() if len(parts) == 2 else ''
    return amt, rng, krw_tag

def fee_card_label_to_plan(label):
    """ラベルから 'weekday' | 'weekend' | 'afternoon' | 'other' を判定"""
    l = label.lower()
    # 1. 午後スルー判定（「午後スルー（平日）」が平日判定より先に）
    if '午後' in label or 'afternoon' in l or '오후' in label:
        return 'afternoon'
    # 2. 平日判定（「土日祝」の「日」より先に「平日」を判定）
    if '平日' in label or 'weekday' in l or '평일' in label:
        return 'weekday'
    # 3. 週末判定（「平日」の「日」を避けるため 日 単独は使わない）
    if '土' in label or '祝' in label or 'weekend' in l or 'holiday' in l or '토' in label or '공휴' in label:
        return 'weekend'
    return 'other'

def build_price_cards(fees_ja, fees_en, fees_ko, jalan_url, rakuten_url, ko_only_jalan=True):
    """JA/EN/KOそれぞれの3カード配列を組み立てる"""
    def cards_for(lang, fees):
        out = []
        # 3種類に分類
        categorized = {'weekday': None, 'weekend': None, 'afternoon': None}
        for label, val in fees:
            plan = fee_card_label_to_plan(label)
            if plan in categorized and categorized[plan] is None:
                categorized[plan] = (label, val)
        order = ['weekday', 'weekend', 'afternoon']
        return [categorized[p] for p in order]

    return {
        'ja': cards_for('ja', fees_ja or []),
        'en': cards_for('en', fees_en or []),
        'ko': cards_for('ko', fees_ko or []),
    }

PLAN_LABELS = {
    'weekday':   {'ja': '平日',          'en': 'Monday–Friday',    'ko': '평일',           'tag': 'WEEKDAY',           'note_ja':'月〜金（祝日除く）。', 'note_en':'Often includes lunch and facility fees.', 'note_ko':'월〜금 (공휴일 제외).'},
    'weekend':   {'ja': '土日祝',        'en': 'Sat · Sun · Holidays','ko': '토·일·공휴일',   'tag': 'WEEKEND / HOLIDAY', 'note_ja':'土・日・祝日。人気時間帯は早めの予約を。', 'note_en':'Peak times book out early — reserve ahead.', 'note_ko':'인기 시간대는 일찍 예약하세요.'},
    'afternoon': {'ja': '午後スルー',    'en': 'Weekday Afternoon','ko': '오후 스루',       'tag': 'AFTERNOON THROUGH', 'note_ja':'午後スタート・休憩なしで18ホール。コスパ最強プラン。', 'note_en':'18 holes straight through. Best value plan.', 'note_ko':'오후 출발·휴식 없이 18홀 연속. 가성비 최고 플랜.'},
}

def price_card_html(plan, label_str, amount_str, lang, jalan_url, rakuten_url, featured=False, ko_only_jalan=True, extra_tag=''):
    info = PLAN_LABELS[plan]
    amt, rng, _ = parse_fee_amount(amount_str)
    featured_cls = ' featured' if featured else ''
    name = info[lang]
    tag = info['tag']
    note = info[f'note_{lang}']
    # KO extra tag (KRW conversion)
    _, _, krw = parse_fee_amount(amount_str)
    extra = f' <span style="color:var(--ocean);font-size:12px;">{krw}</span>' if krw else ''

    # Booking buttons per language
    if lang == 'ja':
        btn_jalan = f'<a href="{jalan_url}" class="btn-book btn-jalan" target="_blank" rel="nofollow sponsored noopener">📅 じゃらんゴルフで予約 →</a>'
        btn_rak = f'<a href="{rakuten_url}" class="btn-book btn-rakuten" target="_blank" rel="nofollow sponsored noopener">🏌️ 楽天GORAで予約 →</a>'
        buttons = btn_jalan + '\n          ' + btn_rak
    elif lang == 'en':
        btn_jalan = f'<a href="{jalan_url}" class="btn-book btn-jalan" target="_blank" rel="nofollow sponsored noopener">📅 Book on Jalan Golf →</a>'
        btn_rak = f'<a href="{rakuten_url}" class="btn-book btn-rakuten" target="_blank" rel="nofollow sponsored noopener">🏌️ Book on Rakuten GORA →</a>'
        buttons = btn_jalan + '\n          ' + btn_rak
    else:  # ko - jalan only
        btn_jalan = f'<a href="{jalan_url}" class="btn-book btn-jalan" target="_blank" rel="nofollow sponsored noopener">📅 자란골프에서 예약 →</a>'
        buttons = btn_jalan

    return f'''<div class="price-card{featured_cls}">
        <div class="price-card-head">
          <div class="price-card-label">{tag}</div>
          <div class="price-card-name">{name}</div>
        </div>
        <div class="price-card-body">
          <div class="price-amount"><span class="yen">¥</span>{amt}<span class="range">{rng}</span></div>
          <div class="price-note">{note}{extra}</div>
        </div>
        <div class="price-card-cta">
          {buttons}
        </div>
      </div>'''

def related_html(related, lang):
    """関連コース → v2デザインのカード"""
    if not related:
        return ''
    cards = []
    for r in related[:3]:
        label = r.get('label', '').split('/')
        if lang == 'ja':
            name = label[0].strip() if label else r.get('href', '').replace('course-','').replace('.html','')
        elif lang == 'en':
            name = label[1].strip() if len(label) > 1 else label[0].strip() if label else ''
        else:  # ko
            name = label[2].strip() if len(label) > 2 else (label[0].strip() if label else '')
        if not name:
            name = r['href'].replace('course-','').replace('.html','').title()
        cards.append(f'<a href="{r["href"]}" class="related-card"><span class="related-card-name">{name}</span><span class="related-card-arrow">→</span></a>')
    return '\n        '.join(cards)

def hero_badges_ja(airport_min, holes, min_fee):
    return f'''<span class="hero-badge">✈️ 空港から{airport_min}分</span>
        <span class="hero-badge">⛳ {holes}</span>
        <span class="hero-badge">💴 ¥{min_fee}〜</span>'''

def generate_course(c):
    slug = c['slug']
    name_ja = clean_name(c.get('name_ja', ''))
    name_en = clean_name(c.get('name_en', slug.title()))
    name_ko = clean_name(c.get('name_ko', ''))
    hero_img = c.get('hero_img', 'images/itoshima-sea.webp')
    airport_min = c.get('airport_min', '?')
    holes = c.get('holes', '18ホール').replace('ホール', 'H').replace(' (PAR72)', '').replace('（2グリーン）','')
    holes_num = re.search(r'(\d+)', holes)
    holes_num_val = holes_num.group(1) if holes_num else '18'
    airport_val_ja = c.get('airport_val_ja', f'車で約{airport_min}分')
    airport_val_en = c.get('airport_val_en', f'~{airport_min} min by car')
    airport_val_ko = c.get('airport_val_ko', f'차로 약 {airport_min}분')
    ic_ja = c.get('ic_ja', '')
    ic_en = c.get('ic_en', ic_ja)
    ic_ko = c.get('ic_ko', ic_ja)
    phone = c.get('phone', '')
    street = c.get('street', '')
    locality = c.get('locality', '')
    website = c.get('website', '')
    website_display = ''
    if website:
        m = re.search(r'https?://(?:www\.)?([^/]+)', website)
        website_display = m.group(1) if m else website

    # Meta descriptions
    desc_ja = c.get('desc_ja', f'{name_ja}の詳細情報。コースデータ・アクセス・料金を掲載。福岡空港から約{airport_min}分。')

    # Fee cards
    price_sets = build_price_cards(c.get('fees_ja', []), c.get('fees_en', []), c.get('fees_ko', []), JALAN_URL, RAKUTEN_URL)

    # Find min fee from weekday or afternoon (for hero badge)
    min_fee_str = ''
    for plan in ['afternoon', 'weekday', 'weekend']:
        card = price_sets['ja'][['weekday','weekend','afternoon'].index(plan)]
        if card:
            amt, _, _ = parse_fee_amount(card[1])
            if amt:
                min_fee_str = amt
                break
    if not min_fee_str:
        min_fee_str = '5,000'

    # Build price card HTML (3 cards per lang, featured = afternoon if present)
    def build_cards_html(lang):
        order = ['weekday', 'weekend', 'afternoon']
        cards = price_sets[lang]
        html_parts = []
        for i, plan in enumerate(order):
            card = cards[i]
            if card:
                label, val = card
                featured = (plan == 'afternoon')
                html_parts.append(price_card_html(plan, label, val, lang, JALAN_URL, RAKUTEN_URL, featured=featured))
            # fallback if missing: skip
        return '\n\n      '.join(html_parts) if html_parts else '<p style="color:var(--muted);">料金情報は公式サイトをご確認ください。</p>'

    price_cards_ja = build_cards_html('ja')
    price_cards_en = build_cards_html('en')
    price_cards_ko = build_cards_html('ko')

    # Related courses
    rel_ja = related_html(c.get('related', []), 'ja')
    rel_en = related_html(c.get('related', []), 'en')
    rel_ko = related_html(c.get('related', []), 'ko')
    if not rel_ja:
        rel_ja = '<a href="recommend.html" class="related-card"><span class="related-card-name">目的別おすすめ特集</span><span class="related-card-arrow">→</span></a>'
        rel_en = '<a href="recommend.html" class="related-card"><span class="related-card-name">Best Courses by Purpose</span><span class="related-card-arrow">→</span></a>'
        rel_ko = '<a href="recommend.html" class="related-card"><span class="related-card-name">추천 골프장 특집</span><span class="related-card-arrow">→</span></a>'

    # Access page exists?
    access_href = f'access-{slug}.html'

    # Official site button (only if we have a real website)
    official_btn_ja = f'<a href="{website}" class="btn-official" target="_blank" rel="noopener">🔗 公式サイトで最新情報を見る ↗</a>' if website else ''
    official_btn_en = f'<a href="{website}" class="btn-official" target="_blank" rel="noopener">🔗 Visit Official Website ↗</a>' if website else ''
    official_btn_ko = f'<a href="{website}" class="btn-official" target="_blank" rel="noopener">🔗 공식 사이트에서 최신 정보 보기 ↗</a>' if website else ''

    # Contact website row
    contact_web_ja = f'<div class="contact-item"><div class="contact-icon">🌐</div><div><div class="contact-label">Website</div><div class="contact-value">{website_display}</div></div></div>' if website else ''
    contact_web_en = contact_web_ja
    contact_web_ko = f'<div class="contact-item"><div class="contact-icon">🌐</div><div><div class="contact-label">웹사이트</div><div class="contact-value">{website_display}</div></div></div>' if website else ''

    # Address strings
    addr_ja = f'{locality} {street}'.strip() or locality or '福岡県'
    addr_en = locality or 'Fukuoka Prefecture'
    addr_ko = locality or '후쿠오카현'

    # Sub copy for header
    sub_en = f'{name_en} ｜ {holes.replace("H"," Holes")}'
    sub_ko = f'{name_en} ｜ {holes.replace("H","홀")}'

    # KO airport sub
    airport_sub_ko = c.get('airport_sub_ko', '인천·부산 → 후쿠오카 직항 약 1시간 30분 ｜ 렌터카로 편하게 이동')

    # Hero badges (shared across langs but labels differ)
    badges_ja = f'''<span class="hero-badge">✈️ 空港から{airport_min}分</span>
        <span class="hero-badge">⛳ {holes}</span>
        <span class="hero-badge">💴 ¥{min_fee_str}〜</span>'''
    badges_en = f'''<span class="hero-badge">✈️ {airport_min} min from airport</span>
        <span class="hero-badge">⛳ {holes.replace("H"," holes")}</span>
        <span class="hero-badge">💴 From ¥{min_fee_str}</span>'''
    badges_ko = f'''<span class="hero-badge">✈️ 공항에서 {airport_min}분</span>
        <span class="hero-badge">⛳ {holes.replace("H","홀")}</span>
        <span class="hero-badge">💴 ¥{min_fee_str}부터</span>'''

    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://www.google-analytics.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=Noto+Sans+KR:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;1,400&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{desc_ja}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <title>{name_ja}｜料金・アクセス | 福岡ゴルフ場ガイド</title>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "GolfCourse",
    "name": "{name_ja}",
    "address": {{"@type":"PostalAddress","streetAddress":"{street}","addressLocality":"{locality}","addressRegion":"福岡県","addressCountry":"JP"}},
    "telephone": "{phone}",
    "description": "{desc_ja}"
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type":"ListItem","position":1,"name":"トップ","item":"https://fukuoka-golf-guide.com/"}},
      {{"@type":"ListItem","position":2,"name":"{name_ja}","item":"https://fukuoka-golf-guide.com/course-{slug}.html"}}
    ]
  }}
  </script>

  <meta property="og:type" content="website">
  <meta property="og:url" content="https://fukuoka-golf-guide.com/course-{slug}.html">
  <meta property="og:site_name" content="福岡ゴルフ場ガイド">
  <meta property="og:title" content="{name_ja}｜料金・アクセス | 福岡ゴルフ場ガイド">
  <meta property="og:description" content="{desc_ja}">
  <meta property="og:image" content="https://fukuoka-golf-guide.com/{hero_img}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://fukuoka-golf-guide.com/course-{slug}.html">

  <script async src="https://www.googletagmanager.com/gtag/js?id=G-PENH0Z4VT7"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-PENH0Z4VT7');
  </script>
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
          service: service, page: page, lang: lang,
          link_text: (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0,80),
          link_url: h.slice(0, 200)
        }});
      }}
    }}, true);
  }})();
  </script>

  <style>
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    :root {{
      --forest:#1F4D3A; --forest-dark:#163829; --orange:#E8744C; --orange-dark:#D15A34;
      --sand:#F3EADA; --paper:#FAF8F3; --charcoal:#2A2A2A; --muted:#6B7280;
      --line:#E5DDC8; --ocean:#3A7CA5; --fairway:#7FA65A;
      --serif:'Noto Serif JP','Playfair Display',Georgia,serif;
      --sans:'Noto Sans JP','Noto Sans KR','Inter',-apple-system,sans-serif;
      --num:'Inter','Noto Sans JP',sans-serif;
    }}
    html {{ scroll-behavior:smooth; }}
    body {{ font-family:var(--sans); background:var(--paper); color:var(--charcoal); line-height:1.7; -webkit-font-smoothing:antialiased; padding-bottom:76px; }}
    a {{ color:inherit; text-decoration:none; }}
    img {{ max-width:100%; display:block; }}
    .lang-switcher {{ position:fixed; top:16px; right:16px; z-index:100; display:flex; background:rgba(255,255,255,0.96); border-radius:999px; padding:4px; gap:2px; box-shadow:0 4px 14px rgba(0,0,0,0.15); backdrop-filter:blur(10px); }}
    .lang-switcher button {{ border:none; background:none; padding:8px 14px; font-size:12px; font-weight:700; cursor:pointer; border-radius:999px; color:var(--muted); font-family:var(--sans); letter-spacing:0.05em; transition:all 0.2s; }}
    .lang-switcher button.on {{ background:var(--forest); color:#fff; }}
    .back-link {{ position:fixed; top:16px; left:16px; z-index:100; background:rgba(255,255,255,0.96); border-radius:999px; padding:8px 14px; font-size:12px; font-weight:700; color:var(--forest); box-shadow:0 4px 14px rgba(0,0,0,0.15); backdrop-filter:blur(10px); }}
    .hero {{ position:relative; height:88vh; min-height:560px; max-height:780px; overflow:hidden; color:#fff; }}
    .hero-img {{ position:absolute; inset:0; background-image:linear-gradient(180deg,rgba(0,0,0,0.25) 0%,rgba(0,0,0,0.15) 40%,rgba(0,0,0,0.75) 100%),url('{hero_img}'); background-size:cover; background-position:center; }}
    .hero-inner {{ position:absolute; inset:0; display:flex; flex-direction:column; justify-content:flex-end; padding:0 24px 48px; max-width:1100px; margin:0 auto; left:0; right:0; }}
    .hero-eyebrow {{ font-family:'Playfair Display',serif; font-style:italic; font-size:16px; opacity:0.9; margin-bottom:10px; letter-spacing:0.03em; }}
    .hero-title {{ font-family:var(--serif); font-weight:700; font-size:clamp(28px,5.5vw,52px); line-height:1.15; margin-bottom:14px; letter-spacing:-0.01em; }}
    .hero-sub {{ font-size:14px; opacity:0.85; font-weight:300; letter-spacing:0.05em; margin-bottom:24px; }}
    .hero-badges {{ display:flex; flex-wrap:wrap; gap:8px; }}
    .hero-badge {{ background:rgba(255,255,255,0.15); backdrop-filter:blur(8px); border:1px solid rgba(255,255,255,0.25); color:#fff; padding:7px 14px; border-radius:999px; font-size:12px; font-weight:500; }}
    .stats-bar {{ background:var(--forest); color:#fff; padding:24px 20px; }}
    .stats-inner {{ max-width:1100px; margin:0 auto; display:grid; grid-template-columns:repeat(4,1fr); gap:4px; text-align:center; }}
    .stat-item {{ padding:8px 4px; border-right:1px solid rgba(255,255,255,0.15); }}
    .stat-item:last-child {{ border-right:none; }}
    .stat-num {{ font-family:var(--num); font-weight:700; font-size:clamp(20px,3.6vw,30px); line-height:1.1; color:#fff; margin-bottom:4px; }}
    .stat-num .unit {{ font-size:0.55em; font-weight:500; opacity:0.75; margin-left:2px; }}
    .stat-label {{ font-size:11px; letter-spacing:0.08em; opacity:0.75; text-transform:uppercase; font-family:'Inter',sans-serif; }}
    .content {{ display:none; }}
    .content.on {{ display:block; }}
    .section {{ max-width:1100px; margin:0 auto; padding:72px 24px; }}
    .section-sand {{ background:var(--sand); }}
    .section-forest {{ background:var(--forest); color:#fff; }}
    .sec-eyebrow {{ font-family:'Playfair Display',serif; font-style:italic; font-size:14px; color:var(--orange); margin-bottom:10px; letter-spacing:0.03em; }}
    .section-forest .sec-eyebrow {{ color:#F3D5C5; }}
    .sec-title {{ font-family:var(--serif); font-weight:700; font-size:clamp(26px,4vw,36px); line-height:1.25; color:var(--forest); margin-bottom:14px; letter-spacing:-0.01em; }}
    .section-forest .sec-title {{ color:#fff; }}
    .sec-desc {{ font-size:15px; color:var(--muted); max-width:620px; line-height:1.8; margin-bottom:36px; }}
    .section-forest .sec-desc {{ color:rgba(255,255,255,0.78); }}
    .pricing-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
    .price-card {{ background:#fff; border-radius:20px; overflow:hidden; box-shadow:0 4px 20px rgba(31,77,58,0.06); border:1px solid var(--line); display:flex; flex-direction:column; transition:transform 0.25s,box-shadow 0.25s; }}
    .price-card:hover {{ transform:translateY(-4px); box-shadow:0 12px 32px rgba(31,77,58,0.12); }}
    .price-card.featured {{ border:2px solid var(--orange); position:relative; }}
    .price-card.featured::before {{ content:'BEST VALUE'; position:absolute; top:14px; right:14px; background:var(--orange); color:#fff; font-size:10px; font-weight:700; letter-spacing:0.1em; padding:4px 10px; border-radius:999px; font-family:'Inter',sans-serif; }}
    .price-card-head {{ padding:24px 24px 8px; }}
    .price-card-label {{ font-family:'Inter',sans-serif; font-size:11px; letter-spacing:0.12em; color:var(--muted); text-transform:uppercase; margin-bottom:8px; }}
    .price-card-name {{ font-family:var(--serif); font-weight:700; font-size:20px; color:var(--forest); margin-bottom:4px; }}
    .price-card-body {{ padding:8px 24px 24px; flex:1; }}
    .price-amount {{ font-family:var(--num); font-weight:700; font-size:32px; color:var(--charcoal); line-height:1.1; display:flex; align-items:baseline; gap:4px; margin:12px 0 6px; }}
    .price-amount .yen {{ font-size:20px; color:var(--muted); font-weight:500; }}
    .price-amount .range {{ font-size:14px; color:var(--muted); font-weight:400; }}
    .price-note {{ font-size:12px; color:var(--muted); line-height:1.5; }}
    .price-card-cta {{ display:flex; flex-direction:column; gap:8px; padding:0 20px 20px; }}
    .btn-book {{ display:flex; align-items:center; justify-content:center; padding:13px 16px; border-radius:12px; font-weight:700; font-size:14px; transition:transform 0.2s,box-shadow 0.2s; gap:8px; }}
    .btn-book:hover {{ transform:translateY(-2px); }}
    .btn-jalan {{ background:linear-gradient(135deg,var(--orange),var(--orange-dark)); color:#fff; box-shadow:0 4px 14px rgba(232,116,76,0.35); }}
    .btn-rakuten {{ background:#fff; color:#C81D1D; border:1.5px solid #C81D1D; }}
    .btn-rakuten:hover {{ background:#C81D1D; color:#fff; }}
    .character-grid {{ display:grid; grid-template-columns:1.1fr 1fr; gap:48px; align-items:center; }}
    .character-img {{ aspect-ratio:4/5; border-radius:24px; overflow:hidden; background-size:cover; background-position:center; box-shadow:0 20px 50px rgba(31,77,58,0.18); }}
    .character-body p {{ font-size:16px; line-height:1.9; color:var(--charcoal); margin-bottom:18px; }}
    .check-list {{ list-style:none; margin-top:24px; }}
    .check-list li {{ display:flex; gap:12px; padding:14px 0; border-bottom:1px solid var(--line); font-size:14px; line-height:1.6; }}
    .check-list li:last-child {{ border-bottom:none; }}
    .check-list .check-icon {{ flex-shrink:0; width:28px; height:28px; border-radius:50%; background:var(--fairway); color:#fff; display:flex; align-items:center; justify-content:center; font-size:14px; font-weight:700; }}
    .check-list strong {{ color:var(--forest); display:block; margin-bottom:2px; }}
    .access-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-bottom:32px; }}
    .access-card {{ background:#fff; border-radius:16px; padding:24px; border:1px solid var(--line); text-align:center; }}
    .access-icon {{ font-size:28px; margin-bottom:10px; }}
    .access-label {{ font-size:12px; color:var(--muted); margin-bottom:6px; letter-spacing:0.08em; text-transform:uppercase; font-family:'Inter',sans-serif; }}
    .access-value {{ font-family:var(--serif); font-weight:700; font-size:18px; color:var(--forest); }}
    .access-tip {{ background:var(--sand); border-radius:12px; padding:16px 20px; font-size:14px; line-height:1.7; color:var(--charcoal); display:flex; gap:10px; }}
    .access-tip-icon {{ color:var(--orange); flex-shrink:0; }}
    .play-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }}
    .play-card {{ background:#fff; border-radius:16px; padding:28px; border:1px solid var(--line); }}
    .play-card-icon {{ font-size:32px; margin-bottom:14px; }}
    .play-card-title {{ font-family:var(--serif); font-weight:700; font-size:18px; color:var(--forest); margin-bottom:8px; }}
    .play-card-desc {{ font-size:14px; line-height:1.7; color:var(--muted); }}
    .booking-hub {{ padding:72px 24px; }}
    .booking-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:20px; max-width:1000px; margin:0 auto; }}
    .booking-card {{ background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.15); border-radius:24px; padding:36px 32px; backdrop-filter:blur(8px); transition:transform 0.3s,background 0.3s; display:block; }}
    .booking-card:hover {{ transform:translateY(-6px); background:rgba(255,255,255,0.12); }}
    .booking-logo {{ font-size:12px; letter-spacing:0.15em; color:var(--orange); font-family:'Inter',sans-serif; font-weight:700; margin-bottom:12px; }}
    .booking-service-name {{ font-family:var(--serif); font-weight:700; font-size:26px; color:#fff; margin-bottom:10px; }}
    .booking-desc {{ color:rgba(255,255,255,0.75); font-size:14px; line-height:1.7; margin-bottom:24px; }}
    .booking-price-tag {{ font-family:var(--num); color:var(--orange); font-size:15px; font-weight:700; margin-bottom:18px; }}
    .booking-price-tag .big {{ font-size:28px; margin:0 2px; }}
    .booking-arrow {{ display:inline-flex; align-items:center; gap:8px; color:#fff; font-weight:700; font-size:14px; padding-top:16px; border-top:1px solid rgba(255,255,255,0.15); width:100%; }}
    .booking-arrow .arrow-ico {{ transition:transform 0.3s; }}
    .booking-card:hover .arrow-ico {{ transform:translateX(6px); }}
    .contact-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-bottom:28px; }}
    .contact-item {{ background:#fff; border-radius:14px; padding:18px 20px; border:1px solid var(--line); display:flex; gap:14px; align-items:flex-start; }}
    .contact-icon {{ font-size:22px; flex-shrink:0; }}
    .contact-label {{ font-size:11px; color:var(--muted); letter-spacing:0.1em; text-transform:uppercase; font-family:'Inter',sans-serif; margin-bottom:4px; }}
    .contact-value {{ font-size:14px; font-weight:500; color:var(--forest); word-break:break-all; }}
    .btn-official {{ display:inline-flex; align-items:center; gap:8px; background:var(--forest); color:#fff; padding:14px 26px; border-radius:999px; font-weight:700; font-size:14px; transition:background 0.2s; }}
    .btn-official:hover {{ background:var(--forest-dark); }}
    .related {{ background:var(--sand); padding:56px 24px; }}
    .related-inner {{ max-width:1100px; margin:0 auto; }}
    .related-cards {{ display:grid; grid-template-columns:repeat(3,1fr); gap:16px; }}
    .related-card {{ background:#fff; border-radius:14px; padding:20px 22px; border:1px solid var(--line); display:flex; align-items:center; justify-content:space-between; transition:transform 0.2s,border-color 0.2s; }}
    .related-card:hover {{ transform:translateX(4px); border-color:var(--forest); }}
    .related-card-name {{ font-family:var(--serif); font-weight:700; font-size:15px; color:var(--forest); }}
    .related-card-arrow {{ color:var(--orange); font-size:18px; }}
    .airport-banner {{ background:linear-gradient(135deg,var(--ocean),#2E6A8F); color:#fff; padding:20px 24px; border-radius:16px; margin-bottom:32px; display:flex; gap:16px; align-items:center; }}
    .airport-banner-icon {{ font-size:32px; }}
    .airport-banner-title {{ font-weight:700; font-size:16px; margin-bottom:4px; }}
    .airport-banner-sub {{ font-size:12px; opacity:0.85; }}
    footer {{ background:var(--forest-dark); color:rgba(255,255,255,0.7); padding:40px 24px; text-align:center; font-size:13px; }}
    footer a {{ color:#fff; font-weight:600; }}
    #sticky-cta {{ position:fixed; bottom:0; left:0; right:0; z-index:200; background:rgba(255,255,255,0.98); border-top:1px solid var(--line); box-shadow:0 -4px 20px rgba(0,0,0,0.12); padding:10px 12px; display:flex; gap:8px; justify-content:center; backdrop-filter:blur(10px); }}
    #sticky-cta .sc-btn {{ flex:1; max-width:240px; text-align:center; padding:13px 10px; border-radius:12px; font-weight:700; font-size:14px; color:#fff; line-height:1.2; box-shadow:0 3px 10px rgba(0,0,0,0.18); display:flex; align-items:center; justify-content:center; gap:6px; }}
    #sticky-cta .sc-jalan {{ background:linear-gradient(135deg,var(--orange),var(--orange-dark)); }}
    #sticky-cta .sc-rakuten {{ background:linear-gradient(135deg,#c81d1d,#8f0000); }}
    @media (min-width:900px) {{ #sticky-cta {{ max-width:640px; left:50%; transform:translateX(-50%); right:auto; border-radius:16px 16px 0 0; }} }}
    #btt {{ position:fixed; bottom:90px; right:16px; z-index:150; width:44px; height:44px; border-radius:50%; border:none; background:var(--forest); color:#fff; font-size:14px; font-weight:700; cursor:pointer; box-shadow:0 4px 14px rgba(0,0,0,0.25); opacity:0; pointer-events:none; transition:opacity 0.25s,transform 0.25s; }}
    #btt.show {{ opacity:1; pointer-events:auto; }}
    #btt:hover {{ background:var(--forest-dark); }}
    @media (max-width:900px) {{
      .pricing-grid {{ grid-template-columns:1fr; }}
      .character-grid {{ grid-template-columns:1fr; gap:24px; }}
      .character-img {{ aspect-ratio:16/10; }}
      .access-grid {{ grid-template-columns:1fr; }}
      .play-grid {{ grid-template-columns:1fr; }}
      .booking-grid {{ grid-template-columns:1fr; }}
      .contact-grid {{ grid-template-columns:1fr; }}
      .related-cards {{ grid-template-columns:1fr; }}
      .stats-inner {{ grid-template-columns:repeat(2,1fr); gap:16px 4px; }}
      .stat-item:nth-child(2) {{ border-right:none; }}
      .section {{ padding:56px 20px; }}
    }}
  </style>
</head>
<body>

<a href="index.html" class="back-link">← Top</a>

<div class="lang-switcher" role="tablist">
  <button class="on" onclick="sw('ja')">JA</button>
  <button onclick="sw('en')">EN</button>
  <button onclick="sw('ko')">KO</button>
</div>

<!-- ═══════════════ 日本語 ═══════════════ -->
<div id="c-ja" class="content on">

  <section class="hero">
    <div class="hero-img"></div>
    <div class="hero-inner">
      <div class="hero-eyebrow">— {locality or "Fukuoka"}</div>
      <h1 class="hero-title">{name_ja}</h1>
      <div class="hero-sub">{name_en} ｜ {holes}</div>
      <div class="hero-badges">
        {badges_ja}
      </div>
    </div>
  </section>

  <div class="stats-bar">
    <div class="stats-inner">
      <div class="stat-item"><div class="stat-num">{holes_num_val}<span class="unit">H</span></div><div class="stat-label">Holes</div></div>
      <div class="stat-item"><div class="stat-num">{airport_min}<span class="unit">min</span></div><div class="stat-label">From Airport</div></div>
      <div class="stat-item"><div class="stat-num">¥{min_fee_str}<span class="unit">〜</span></div><div class="stat-label">Lowest Fee</div></div>
      <div class="stat-item"><div class="stat-num">JP<span class="unit">/EN/KO</span></div><div class="stat-label">3 Languages</div></div>
    </div>
  </div>

  <section class="section">
    <div class="sec-eyebrow">— Green Fees</div>
    <h2 class="sec-title">料金を、一目で比べる。</h2>
    <p class="sec-desc">平日・土日祝・午後スルーを横並びで比較。価格は目安。最新のベストレートは予約サイトでご確認ください。</p>
    <div class="pricing-grid">
      {price_cards_ja}
    </div>
  </section>

  <section class="section section-sand">
    <div class="character-grid">
      <div class="character-img" style="background-image:url('{hero_img}');"></div>
      <div class="character-body">
        <div class="sec-eyebrow">— The Course</div>
        <h2 class="sec-title">{name_ja}<br>の魅力。</h2>
        <p>{locality or "福岡"}に広がる{c.get("course_type_ja","コース")}。整備の行き届いたフェアウェイと、戦略性のあるレイアウトで、初心者から上級者まで幅広く楽しめます。福岡空港から{airport_val_ja}、日帰りでも十分アクセス可能です。</p>
        <ul class="check-list">
          <li><span class="check-icon">✓</span><div><strong>年間通して良好なコースコンディション</strong>整備されたフェアウェイとグリーンで、気持ちよくプレーできます。</div></li>
          <li><span class="check-icon">✓</span><div><strong>福岡空港から{airport_min}分</strong>レンタカーや送迎でスムーズに到着できます。</div></li>
          <li><span class="check-icon">✓</span><div><strong>午後スルーなどプレースタイルも選べる</strong>時間や予算に合わせて柔軟に楽しめるのが魅力です。</div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— Getting Here</div>
    <h2 class="sec-title">アクセス</h2>
    <p class="sec-desc">車でのご来場を推奨。福岡都市高速・九州自動車道経由。</p>
    <div class="access-grid">
      <div class="access-card"><div class="access-icon">✈️</div><div class="access-label">From Fukuoka Airport</div><div class="access-value">{airport_val_ja}</div></div>
      <div class="access-card"><div class="access-icon">🚄</div><div class="access-label">From Hakata Station</div><div class="access-value">車で約{airport_min}分</div></div>
      <div class="access-card"><div class="access-icon">🛣️</div><div class="access-label">Nearest IC</div><div class="access-value">{ic_ja or "最寄IC"}</div></div>
    </div>
    <div class="access-tip"><span class="access-tip-icon">💡</span><div>Google Maps・Naver Mapsで「{name_ja}」と検索すると案内されます。<br><a href="{access_href}" style="color:var(--forest);font-weight:700;text-decoration:underline;">詳しいアクセスガイドを見る →</a></div></div>
  </section>

  <section class="section section-sand">
    <div class="sec-eyebrow">— Play Styles</div>
    <h2 class="sec-title">プレースタイル</h2>
    <div class="play-grid">
      <div class="play-card">
        <div class="play-card-icon">☀️</div>
        <div class="play-card-title">通常ラウンド</div>
        <div class="play-card-desc">午前スタート・18ホール。前半9ホール後にクラブハウスで休憩を挟む、日本ゴルフの王道スタイル。</div>
      </div>
      <div class="play-card">
        <div class="play-card-icon">🌤️</div>
        <div class="play-card-title">午後スルー</div>
        <div class="play-card-desc">午後スタート・休憩なしで18ホール続けてプレー。半日でラウンドできて料金もお得。</div>
      </div>
    </div>
  </section>

  <section class="section-forest booking-hub">
    <div style="max-width:1100px;margin:0 auto 32px;text-align:center;">
      <div class="sec-eyebrow">— Book Your Tee Time</div>
      <h2 class="sec-title">今すぐ、ベストレートを確認。</h2>
      <p class="sec-desc" style="margin:0 auto 0;">日本最大級のゴルフ予約サイトで、最新の空き状況と価格をチェック。両サイトを比較すると、プランによって差が出ることも。</p>
    </div>
    <div class="booking-grid">
      <a href="{JALAN_URL}" class="booking-card" target="_blank" rel="nofollow sponsored noopener">
        <div class="booking-logo">01 ／ JALAN GOLF</div>
        <div class="booking-service-name">じゃらんゴルフ</div>
        <div class="booking-desc">リクルートが運営する国内最大級のゴルフ予約サイト。Pontaポイントも貯まる・使える。</div>
        <div class="booking-price-tag">最安 <span class="big">¥{min_fee_str}</span>〜</div>
        <div class="booking-arrow">ベストレートで予約する <span class="arrow-ico">→</span></div>
      </a>
      <a href="{RAKUTEN_URL}" class="booking-card" target="_blank" rel="nofollow sponsored noopener">
        <div class="booking-logo">02 ／ RAKUTEN GORA</div>
        <div class="booking-service-name">楽天GORA</div>
        <div class="booking-desc">楽天ポイントが貯まる・使えるゴルフ予約サイト。SPUでポイント倍率アップの日も。</div>
        <div class="booking-price-tag">最安 <span class="big">¥{min_fee_str}</span>〜</div>
        <div class="booking-arrow">ベストレートで予約する <span class="arrow-ico">→</span></div>
      </a>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— Contact</div>
    <h2 class="sec-title">連絡先・公式情報</h2>
    <div class="contact-grid">
      <div class="contact-item"><div class="contact-icon">📍</div><div><div class="contact-label">Address</div><div class="contact-value">{addr_ja}</div></div></div>
      <div class="contact-item"><div class="contact-icon">📞</div><div><div class="contact-label">Phone</div><div class="contact-value">{phone}</div></div></div>
      {contact_web_ja}
    </div>
    {official_btn_ja}
  </section>

  <section class="related">
    <div class="related-inner">
      <div class="sec-eyebrow">— Related Courses</div>
      <h2 class="sec-title" style="margin-bottom:28px;">近くのコースも見る</h2>
      <div class="related-cards">
        {rel_ja}
      </div>
    </div>
  </section>

</div><!-- /ja -->

<!-- ═══════════════ English ═══════════════ -->
<div id="c-en" class="content">

  <section class="hero">
    <div class="hero-img"></div>
    <div class="hero-inner">
      <div class="hero-eyebrow">— {locality or "Fukuoka"}</div>
      <h1 class="hero-title">{name_en}</h1>
      <div class="hero-sub">{name_ja} ｜ {holes.replace("H"," Holes")}</div>
      <div class="hero-badges">
        {badges_en}
      </div>
    </div>
  </section>

  <div class="stats-bar">
    <div class="stats-inner">
      <div class="stat-item"><div class="stat-num">{holes_num_val}<span class="unit">H</span></div><div class="stat-label">Holes</div></div>
      <div class="stat-item"><div class="stat-num">{airport_min}<span class="unit">min</span></div><div class="stat-label">From Airport</div></div>
      <div class="stat-item"><div class="stat-num">¥{min_fee_str}<span class="unit">〜</span></div><div class="stat-label">Lowest Fee</div></div>
      <div class="stat-item"><div class="stat-num">JP<span class="unit">/EN/KO</span></div><div class="stat-label">3 Languages</div></div>
    </div>
  </div>

  <section class="section">
    <div class="sec-eyebrow">— Green Fees</div>
    <h2 class="sec-title">Compare at a glance.</h2>
    <p class="sec-desc">Weekday, weekend, and afternoon-through rates side by side. Prices are indicative — check the booking sites for the latest best rate.</p>
    <div class="pricing-grid">
      {price_cards_en}
    </div>
  </section>

  <section class="section section-sand">
    <div class="character-grid">
      <div class="character-img" style="background-image:url('{hero_img}');"></div>
      <div class="character-body">
        <div class="sec-eyebrow">— The Course</div>
        <h2 class="sec-title">Why golfers love<br>this course.</h2>
        <p>A well-balanced layout in {locality or "Fukuoka"}, with nicely maintained fairways and a course design suited to all skill levels. About {airport_min} minutes from Fukuoka Airport by car — a perfect day-trip destination.</p>
        <ul class="check-list">
          <li><span class="check-icon">✓</span><div><strong>Year-round great conditions</strong>Consistently maintained fairways and greens, enjoyable for every skill level.</div></li>
          <li><span class="check-icon">✓</span><div><strong>{airport_min} min from Fukuoka Airport</strong>Easy by rental car or courtesy bus.</div></li>
          <li><span class="check-icon">✓</span><div><strong>Flexible play styles</strong>Choose morning rounds with a half-turn break, or afternoon-through for half-day value.</div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— Getting Here</div>
    <h2 class="sec-title">Access</h2>
    <p class="sec-desc">Car is recommended. Via Fukuoka Urban Expressway / Kyushu Expressway.</p>
    <div class="access-grid">
      <div class="access-card"><div class="access-icon">✈️</div><div class="access-label">From Fukuoka Airport</div><div class="access-value">{airport_val_en}</div></div>
      <div class="access-card"><div class="access-icon">🚄</div><div class="access-label">From Hakata Station</div><div class="access-value">~{airport_min} min by car</div></div>
      <div class="access-card"><div class="access-icon">🛣️</div><div class="access-label">Nearest IC</div><div class="access-value">{ic_en or "Nearest IC"}</div></div>
    </div>
    <div class="access-tip"><span class="access-tip-icon">💡</span><div>Search "{name_ja}" in Google Maps or Naver Maps.<br><a href="{access_href}" style="color:var(--forest);font-weight:700;text-decoration:underline;">Full access guide →</a></div></div>
  </section>

  <section class="section section-sand">
    <div class="sec-eyebrow">— Play Styles</div>
    <h2 class="sec-title">Two ways to play.</h2>
    <div class="play-grid">
      <div class="play-card">
        <div class="play-card-icon">☀️</div>
        <div class="play-card-title">Standard Round</div>
        <div class="play-card-desc">Morning start, 18 holes with a lunch break after the front 9 — the classic Japanese format.</div>
      </div>
      <div class="play-card">
        <div class="play-card-icon">🌤️</div>
        <div class="play-card-title">Afternoon Through</div>
        <div class="play-card-desc">Afternoon start, 18 holes played straight through — half-day golf at the best price.</div>
      </div>
    </div>
  </section>

  <section class="section-forest booking-hub">
    <div style="max-width:1100px;margin:0 auto 32px;text-align:center;">
      <div class="sec-eyebrow">— Book Your Tee Time</div>
      <h2 class="sec-title">Check the best rate now.</h2>
      <p class="sec-desc" style="margin:0 auto 0;">Japan's two biggest tee-time booking platforms. Comparing both often reveals meaningful differences.</p>
    </div>
    <div class="booking-grid">
      <a href="{JALAN_URL}" class="booking-card" target="_blank" rel="nofollow sponsored noopener">
        <div class="booking-logo">01 ／ JALAN GOLF</div>
        <div class="booking-service-name">Jalan Golf</div>
        <div class="booking-desc">Japan's largest tee-time booking site. Earn and use Ponta points.</div>
        <div class="booking-price-tag">From <span class="big">¥{min_fee_str}</span></div>
        <div class="booking-arrow">Book at best rate <span class="arrow-ico">→</span></div>
      </a>
      <a href="{RAKUTEN_URL}" class="booking-card" target="_blank" rel="nofollow sponsored noopener">
        <div class="booking-logo">02 ／ RAKUTEN GORA</div>
        <div class="booking-service-name">Rakuten GORA</div>
        <div class="booking-desc">Earn and use Rakuten points. SPU campaigns can multiply returns.</div>
        <div class="booking-price-tag">From <span class="big">¥{min_fee_str}</span></div>
        <div class="booking-arrow">Book at best rate <span class="arrow-ico">→</span></div>
      </a>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— Contact</div>
    <h2 class="sec-title">Contact & Official</h2>
    <div class="contact-grid">
      <div class="contact-item"><div class="contact-icon">📍</div><div><div class="contact-label">Address</div><div class="contact-value">{addr_en}</div></div></div>
      <div class="contact-item"><div class="contact-icon">📞</div><div><div class="contact-label">Phone</div><div class="contact-value">{phone}</div></div></div>
      {contact_web_en}
    </div>
    {official_btn_en}
  </section>

  <section class="related">
    <div class="related-inner">
      <div class="sec-eyebrow">— Related Courses</div>
      <h2 class="sec-title" style="margin-bottom:28px;">Nearby Courses</h2>
      <div class="related-cards">
        {rel_en}
      </div>
    </div>
  </section>

</div><!-- /en -->

<!-- ═══════════════ 한국어 ═══════════════ -->
<div id="c-ko" class="content">

  <section class="hero">
    <div class="hero-img"></div>
    <div class="hero-inner">
      <div class="hero-eyebrow">— {locality or "Fukuoka"}</div>
      <h1 class="hero-title">{name_ko}</h1>
      <div class="hero-sub">{name_en} ｜ {holes.replace("H","홀")}</div>
      <div class="hero-badges">
        {badges_ko}
      </div>
    </div>
  </section>

  <div class="stats-bar">
    <div class="stats-inner">
      <div class="stat-item"><div class="stat-num">{holes_num_val}<span class="unit">H</span></div><div class="stat-label">홀 수</div></div>
      <div class="stat-item"><div class="stat-num">{airport_min}<span class="unit">분</span></div><div class="stat-label">공항에서</div></div>
      <div class="stat-item"><div class="stat-num">¥{min_fee_str}<span class="unit">〜</span></div><div class="stat-label">최저 그린피</div></div>
      <div class="stat-item"><div class="stat-num">JP<span class="unit">/EN/KO</span></div><div class="stat-label">3개 언어</div></div>
    </div>
  </div>

  <section class="section">
    <div class="airport-banner">
      <div class="airport-banner-icon">✈️</div>
      <div>
        <div class="airport-banner-title">후쿠오카공항에서 차로 약 {airport_min}분</div>
        <div class="airport-banner-sub">{airport_sub_ko}</div>
      </div>
    </div>

    <div class="sec-eyebrow">— 그린피</div>
    <h2 class="sec-title">한눈에 비교하는 요금.</h2>
    <p class="sec-desc">평일·주말·오후 스루 3가지 플랜을 나란히 비교. 최신 요금은 예약 사이트에서 확인해 주세요.</p>
    <div class="pricing-grid">
      {price_cards_ko}
    </div>
  </section>

  <section class="section section-sand">
    <div class="character-grid">
      <div class="character-img" style="background-image:url('{hero_img}');"></div>
      <div class="character-body">
        <div class="sec-eyebrow">— 코스 소개</div>
        <h2 class="sec-title">이 코스의<br>매력.</h2>
        <p>{locality or "후쿠오카"}에 위치한 균형 잡힌 코스. 잘 정비된 페어웨이와 전략적인 레이아웃으로 초보자부터 상급자까지 모두 즐길 수 있습니다. 후쿠오카공항에서 {airport_val_ko}로 당일치기 여행에도 최적입니다.</p>
        <ul class="check-list">
          <li><span class="check-icon">✓</span><div><strong>연중 쾌적한 코스 컨디션</strong>정비된 페어웨이와 그린으로 편안하게 플레이할 수 있습니다.</div></li>
          <li><span class="check-icon">✓</span><div><strong>후쿠오카공항에서 {airport_min}분</strong>렌터카나 셔틀로 간편하게 도착합니다.</div></li>
          <li><span class="check-icon">✓</span><div><strong>유연한 플레이 스타일</strong>오전 라운드·오후 스루 등 시간과 예산에 맞춰 선택할 수 있습니다.</div></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— 오시는 길</div>
    <h2 class="sec-title">액세스</h2>
    <p class="sec-desc">자동차 추천. 후쿠오카 도시 고속도로·규슈 고속도로 경유.</p>
    <div class="access-grid">
      <div class="access-card"><div class="access-icon">✈️</div><div class="access-label">후쿠오카공항에서</div><div class="access-value">{airport_val_ko}</div></div>
      <div class="access-card"><div class="access-icon">🚄</div><div class="access-label">하카타역에서</div><div class="access-value">차로 약 {airport_min}분</div></div>
      <div class="access-card"><div class="access-icon">🛣️</div><div class="access-label">최근 IC</div><div class="access-value">{ic_ko or "최근 IC"}</div></div>
    </div>
    <div class="access-tip"><span class="access-tip-icon">💡</span><div>Google Maps 또는 Naver Maps에서 「{name_ja}」로 검색하세요.<br><a href="{access_href}" style="color:var(--forest);font-weight:700;text-decoration:underline;">자세한 오시는 길 가이드 →</a></div></div>
  </section>

  <section class="section section-sand">
    <div class="sec-eyebrow">— 플레이 스타일</div>
    <h2 class="sec-title">두 가지 플레이 방식.</h2>
    <div class="play-grid">
      <div class="play-card">
        <div class="play-card-icon">☀️</div>
        <div class="play-card-title">일반 라운드</div>
        <div class="play-card-desc">오전 출발, 18홀. 전반 9홀 후 클럽하우스에서 점심 휴식. 일본 골프의 정통 스타일.</div>
      </div>
      <div class="play-card">
        <div class="play-card-icon">🌤️</div>
        <div class="play-card-title">오후 스루</div>
        <div class="play-card-desc">오후 출발, 휴식 없이 18홀 연속 플레이. 반나절에 끝나고 요금도 가성비 최고.</div>
      </div>
    </div>
  </section>

  <section class="section-forest booking-hub">
    <div style="max-width:1100px;margin:0 auto 32px;text-align:center;">
      <div class="sec-eyebrow">— 티타임 예약</div>
      <h2 class="sec-title">지금 베스트 레이트 확인.</h2>
      <p class="sec-desc" style="margin:0 auto 0;">일본 최대 골프 예약 사이트에서 최신 빈자리와 가격을 확인하세요.</p>
    </div>
    <div class="booking-grid" style="grid-template-columns:1fr;max-width:600px;">
      <a href="{JALAN_URL}" class="booking-card" target="_blank" rel="nofollow sponsored noopener">
        <div class="booking-logo">JALAN GOLF ／ 자란골프</div>
        <div class="booking-service-name">자란골프에서 예약</div>
        <div class="booking-desc">일본 최대 규모의 골프 예약 사이트. 그린피·플레이 스타일·식사 포함 여부를 한눈에 비교할 수 있습니다.</div>
        <div class="booking-price-tag">최저 <span class="big">¥{min_fee_str}</span>부터</div>
        <div class="booking-arrow">베스트 레이트로 예약하기 <span class="arrow-ico">→</span></div>
      </a>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— 연락처</div>
    <h2 class="sec-title">연락처·공식 정보</h2>
    <div class="contact-grid">
      <div class="contact-item"><div class="contact-icon">📍</div><div><div class="contact-label">주소</div><div class="contact-value">{addr_ko}</div></div></div>
      <div class="contact-item"><div class="contact-icon">📞</div><div><div class="contact-label">전화</div><div class="contact-value">{phone}</div></div></div>
      {contact_web_ko}
    </div>
    {official_btn_ko}
  </section>

  <section class="related">
    <div class="related-inner">
      <div class="sec-eyebrow">— 관련 코스</div>
      <h2 class="sec-title" style="margin-bottom:28px;">근처 코스 보기</h2>
      <div class="related-cards">
        {rel_ko}
      </div>
    </div>
  </section>

</div><!-- /ko -->

<footer>
  ⛳ 福岡ゴルフ場ガイド ｜ Fukuoka Golf Guide ｜ 후쿠오카 골프 가이드<br>
  <small><a href="index.html">トップへ戻る / Back to Top / 목록으로</a></small>
</footer>

<button id="btt" onclick="window.scrollTo({{top:0,behavior:'smooth'}})" aria-label="トップに戻る">▲</button>
<div id="sticky-cta" aria-label="予約CTA"></div>

<script>
  function sw(l){{
    ['ja','en','ko'].forEach(x=>document.getElementById('c-'+x).classList.toggle('on', x===l));
    document.querySelectorAll('.lang-switcher button').forEach((b,i)=>b.classList.toggle('on', ['ja','en','ko'][i]===l));
    renderStickyCTA();
    window.scrollTo({{top:0, behavior:'smooth'}});
  }}
  (function(){{
    var btn = document.getElementById('btt');
    window.addEventListener('scroll', function(){{ btn.classList.toggle('show', window.scrollY > 400); }}, {{passive:true}});
  }})();
  var JALAN="{JALAN_URL}";
  var RAKUTEN="{RAKUTEN_URL}";
  var sttpl = {{
    ja:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 じゃらん</a>'+
       '<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ 楽天GORA</a>',
    en:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank">📅 Jalan</a>'+
       '<a href="'+RAKUTEN+'" class="sc-btn sc-rakuten" rel="nofollow sponsored" target="_blank">🏌️ Rakuten GORA</a>',
    ko:'<a href="'+JALAN+'" class="sc-btn sc-jalan" rel="nofollow sponsored" target="_blank" style="max-width:360px;">📅 자란골프에서 예약하기</a>'
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
</script>

</body>
</html>
'''
    return html

def main():
    all_data = json.loads(DATA.read_text(encoding='utf-8'))
    print(f'=== 生成対象: {len(all_data)}コース ===')
    generated = 0
    # Skip course-century since we already built v2 manually
    for c in all_data:
        slug = c['slug']
        if slug == 'century':
            print(f'  SKIP  course-{slug}  (already manual v2)')
            continue
        out = BASE / f'course-{slug}-v2.html'
        try:
            html = generate_course(c)
            out.write_text(html, encoding='utf-8')
            print(f'  OK    course-{slug}-v2.html')
            generated += 1
        except Exception as e:
            print(f'  FAIL  {slug}: {e}')
            import traceback; traceback.print_exc()
    print(f'\n=== 完了: {generated}件生成 ===')

if __name__ == '__main__':
    main()
