#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""generate_field_reports.py — 現地ラウンドレポート 3 本生成
  report-lakeside.html / report-mission.html / report-kokura.html
  オーナー一次体験に基づく E-E-A-T コンテンツ。写真なし・テキスト主体。
  観測フェーズ対応: 既存 course-*.html は無変更。

Usage: python scripts/generate_field_reports.py [--dry-run]
"""
import sys, os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

DRY = '--dry-run' in sys.argv
REPO = Path('C:/Users/Owner/fukuoka-golf-guide')
PREVIEW = Path('C:/Users/Owner/Documents/新しいPJ')

JALAN_BASE = 'https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2F'
RAKUTEN_BASE = 'https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F'
RAKUTEN_KOKURA = 'https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+BW8O1&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_BW8O1%3Fpc%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F400019%26m%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F400019'

GA4_SCRIPT = '''  <!-- Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-PENH0Z4VT7"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-PENH0Z4VT7');
  </script>
  <!-- AFFILIATE_TRACKER -->
  <script>
  /* GA4 tracking v2.1: cta_position + internal_nav_click */
  (function(){
    function classifyService(href) {
      if (/jalan/i.test(href)) return 'jalan';
      if (/rakuten/i.test(href) || /gora/i.test(href)) return 'rakuten_gora';
      if (/a8\\.net/i.test(href)) return 'a8_other';
      return null;
    }
    function classifyCtaPosition(a) {
      if (a.classList.contains('ftv-cta-btn') || a.closest('.ftv-cta-strip')) return 'ftv';
      if (a.closest('section.related-section')) return 'explore_nav';
      return 'other';
    }
    function getPage() { return (location.pathname.split('/').pop() || 'index') + ''; }
    document.addEventListener('click', function(e){
      var a = e.target.closest('a[href]');
      if (!a) return;
      var h = a.getAttribute('href') || '';
      if (typeof gtag !== 'function') return;
      var service = classifyService(h);
      var page = getPage();
      var ctaPos = classifyCtaPosition(a);
      var linkText = (a.textContent || a.getAttribute('aria-label') || '').trim().slice(0,80);
      if (service) {
        gtag('event', 'click_affiliate', {
          service: service, page: page, lang: 'ja',
          cta_position: ctaPos,
          link_text: linkText, link_url: h.slice(0, 200)
        });
      } else if (ctaPos === 'explore_nav' && /\\.html?(\\?|#|$)/.test(h)) {
        var target = (h.split('?')[0].split('#')[0].split('/').pop() || '').replace(/\\.html?$/,'');
        gtag('event', 'internal_nav_click', {
          page: page, lang: 'ja',
          nav_section: 'explore_nav',
          target_page: target,
          link_text: linkText
        });
      }
    }, true);
  })();
  </script>'''

CSS = '''  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root {
      --forest: #1F4D3A; --forest-dark: #163829;
      --ocean: #3A7CA5; --ocean-dark: #2C5E80; --ocean-pale: #E8F1F8;
      --orange: #E8744C; --orange-dark: #D15A34;
      --sand: #F3EADA; --paper: #FAF8F3;
      --charcoal: #2A2A2A; --muted: #6B7280;
      --line: #E5DDC8;
      --serif: 'Noto Serif JP', 'Playfair Display', Georgia, serif;
      --sans: 'Noto Sans JP', 'Inter', -apple-system, sans-serif;
      --num: 'Inter', 'Noto Sans JP', sans-serif;
    }
    html { scroll-behavior: smooth; }
    body { font-family: var(--sans); background: var(--paper); color: var(--charcoal); line-height: 1.7; -webkit-font-smoothing: antialiased; padding-bottom: 40px; }
    a { color: inherit; text-decoration: none; }
    img { max-width: 100%; display: block; }
    .back-link { position: fixed; top: 16px; left: 16px; z-index: 100; background: rgba(255,255,255,0.96); border-radius: 999px; padding: 8px 14px; font-size: 12px; font-weight: 700; color: var(--ocean-dark); box-shadow: 0 4px 14px rgba(0,0,0,0.15); backdrop-filter: blur(10px); }
    .back-link:hover { background: #fff; }
    .hero { position: relative; height: 60vh; min-height: 440px; max-height: 600px; overflow: hidden; color: #fff; }
    .hero-img { position: absolute; inset: 0; background-size: cover; background-position: center; }
    .hero-inner { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: flex-end; padding: 0 24px 56px; max-width: 1100px; margin: 0 auto; left: 0; right: 0; }
    .hero-eyebrow { font-family: 'Playfair Display', serif; font-style: italic; font-size: 16px; opacity: 0.92; margin-bottom: 12px; letter-spacing: 0.03em; }
    .hero-title { font-family: var(--serif); font-weight: 700; font-size: clamp(28px, 5vw, 46px); line-height: 1.18; margin-bottom: 14px; letter-spacing: -0.01em; }
    .hero-sub { font-size: 14px; opacity: 0.92; font-weight: 300; letter-spacing: 0.05em; margin-bottom: 26px; max-width: 720px; line-height: 1.7; }
    .hero-badges { display: flex; flex-wrap: wrap; gap: 8px; }
    .hero-badge { background: rgba(255,255,255,0.18); backdrop-filter: blur(8px); border: 1px solid rgba(255,255,255,0.3); color: #fff; padding: 7px 14px; border-radius: 999px; font-size: 12px; font-weight: 500; }
    .stats-band { background: linear-gradient(135deg, var(--forest), var(--forest-dark)); color: #fff; padding: 28px 20px; }
    .stats-band-inner { max-width: 1100px; margin: 0 auto; display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; text-align: center; }
    .stats-band-item { padding: 8px 4px; border-right: 1px solid rgba(255,255,255,0.28); }
    .stats-band-item:last-child { border-right: none; }
    .stats-band-num { font-family: var(--num); font-weight: 700; font-size: clamp(20px, 3.6vw, 28px); line-height: 1.1; color: #fff; margin-bottom: 4px; }
    .stats-band-num .unit { font-size: 0.6em; font-weight: 500; opacity: 0.9; margin-left: 2px; }
    .stats-band-label { font-size: 11px; letter-spacing: 0.08em; opacity: 0.9; text-transform: uppercase; font-family: 'Inter', sans-serif; }
    .section { max-width: 1100px; margin: 0 auto; padding: 56px 24px; }
    .section-pale { background: var(--ocean-pale); }
    .section-warm { background: var(--sand); }
    .sec-eyebrow { font-family: 'Playfair Display', serif; font-style: italic; font-size: 14px; color: var(--ocean-dark); margin-bottom: 10px; letter-spacing: 0.03em; }
    .sec-title { font-family: var(--serif); font-weight: 700; font-size: clamp(22px, 3.4vw, 30px); line-height: 1.28; color: var(--forest); margin-bottom: 18px; letter-spacing: -0.01em; }
    .prose { font-size: 16px; line-height: 1.92; color: var(--charcoal); max-width: 760px; }
    .prose p { margin-bottom: 18px; }
    .prose p:last-child { margin-bottom: 0; }
    .prose strong { color: var(--forest); font-weight: 700; }
    .prose a { color: var(--ocean); border-bottom: 1px solid var(--ocean); font-weight: 600; }
    .prose a:hover { background: var(--ocean-pale); }
    .pull-quote { margin: 28px 0; border-left: 4px solid var(--forest); padding: 18px 24px; background: #fff; border-radius: 0 12px 12px 0; font-family: var(--serif); font-size: 17px; line-height: 1.72; color: var(--forest); font-weight: 600; max-width: 720px; box-shadow: 0 4px 16px rgba(31,77,58,0.09); }
    .cta-row { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 22px; }
    .ftv-cta-btn { display: inline-flex; align-items: center; gap: 8px; background: linear-gradient(135deg, var(--orange), var(--orange-dark)); color: #fff; padding: 14px 22px; border-radius: 12px; font-weight: 700; font-size: 15px; box-shadow: 0 4px 14px rgba(232,116,76,0.35); transition: transform 0.2s; }
    .ftv-cta-btn:hover { transform: translateY(-2px); }
    .secondary-btn { display: inline-flex; align-items: center; gap: 8px; background: #fff; color: var(--ocean-dark); padding: 14px 22px; border-radius: 12px; font-weight: 700; font-size: 15px; border: 1.5px solid var(--ocean-dark); transition: background 0.2s; }
    .secondary-btn:hover { background: var(--ocean-pale); }
    .related-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .related-card { background: #fff; border-radius: 14px; padding: 22px 24px; border: 1px solid var(--line); display: flex; align-items: center; justify-content: space-between; transition: transform 0.2s, border-color 0.2s; }
    .related-card:hover { transform: translateX(4px); border-color: var(--forest); }
    .related-name { font-family: var(--serif); font-weight: 700; font-size: 15px; color: var(--forest); }
    .related-arrow { color: var(--orange); font-size: 18px; }
    .disclaimer { font-size: 12.5px; color: var(--muted); background: #fff; border-left: 3px solid var(--ocean); padding: 14px 18px; margin-top: 26px; border-radius: 4px; line-height: 1.65; max-width: 760px; }
    footer { background: var(--forest-dark); color: rgba(255,255,255,0.7); padding: 40px 24px; text-align: center; font-size: 13px; line-height: 1.85; }
    footer a { color: #fff; font-weight: 600; }
    #btt { position: fixed; bottom: 22px; right: 16px; z-index: 150; width: 44px; height: 44px; border-radius: 50%; border: none; background: var(--forest); color: #fff; font-size: 18px; font-weight: 700; cursor: pointer; box-shadow: 0 4px 14px rgba(0,0,0,0.25); opacity: 0; pointer-events: none; transition: opacity 0.25s; }
    #btt.show { opacity: 1; pointer-events: auto; }
    #btt:hover { background: var(--forest-dark); }
    @media (max-width: 900px) {
      .related-grid { grid-template-columns: 1fr; }
      .stats-band-inner { grid-template-columns: repeat(2, 1fr); gap: 16px 4px; }
      .stats-band-item:nth-child(2) { border-right: none; }
      .section { padding: 44px 20px; }
      .hero { height: 56vh; min-height: 380px; }
      .cta-row { flex-direction: column; }
      .ftv-cta-btn, .secondary-btn { justify-content: center; }
    }
  </style>'''

FOOTER_JS = '''<button id="btt" aria-label="ページトップへ">↑</button>
<script>
  var btt = document.getElementById('btt');
  window.addEventListener('scroll', function(){ btt.classList.toggle('show', window.scrollY > 400); });
  btt.addEventListener('click', function(){ window.scrollTo({top:0,behavior:'smooth'}); });
</script>'''

def build_html(slug, name_ja, name_en, location, airport_min, price_weekday, price_area,
               hero_gradient, badges,
               meta_desc, og_title, og_desc,
               headline, hero_title, hero_sub,
               stat1_num, stat1_unit, stat1_label,
               stat2_num, stat2_unit, stat2_label,
               stat3_num, stat3_unit, stat3_label,
               stat4_num, stat4_unit, stat4_label,
               sections_html,
               jalan_url, rakuten_url,
               related_html,
               date_pub='2026-05-22'):

    rakuten_btn = f'''      <a href="{rakuten_url}" class="secondary-btn" target="_blank" rel="nofollow sponsored noopener">🏌️ 楽天GORAで予約 →</a>''' if rakuten_url else ''

    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://www.google-analytics.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;600;700&family=Noto+Sans+JP:wght@300;400;500;700&family=Playfair+Display:ital,wght@0,500;1,400&family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{meta_desc}">
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <title>{headline} | 福岡ゴルフ場ガイド</title>

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "{headline}",
    "description": "{meta_desc}",
    "author": {{ "@type": "Organization", "name": "福岡ゴルフ場ガイド 編集部" }},
    "publisher": {{ "@type": "Organization", "name": "福岡ゴルフ場ガイド", "logo": {{ "@type": "ImageObject", "url": "https://fukuoka-golf-guide.com/favicon.svg" }} }},
    "datePublished": "{date_pub}",
    "dateModified": "{date_pub}",
    "inLanguage": "ja",
    "url": "https://fukuoka-golf-guide.com/report-{slug}.html",
    "mentions": {{ "@type": "GolfCourse", "name": "{name_ja}", "url": "https://fukuoka-golf-guide.com/course-{slug}.html" }}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{ "@type": "ListItem", "position": 1, "name": "Top", "item": "https://fukuoka-golf-guide.com/" }},
      {{ "@type": "ListItem", "position": 2, "name": "{name_ja}", "item": "https://fukuoka-golf-guide.com/course-{slug}.html" }},
      {{ "@type": "ListItem", "position": 3, "name": "編集部現地レポート", "item": "https://fukuoka-golf-guide.com/report-{slug}.html" }}
    ]
  }}
  </script>

  <meta property="og:type" content="article">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:url" content="https://fukuoka-golf-guide.com/report-{slug}.html">
  <meta property="og:site_name" content="福岡ゴルフ場ガイド">
  <meta property="og:title" content="{og_title}">
  <meta property="og:description" content="{og_desc}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="canonical" href="https://fukuoka-golf-guide.com/report-{slug}.html" />
  <link rel="alternate" hreflang="ja" href="https://fukuoka-golf-guide.com/report-{slug}.html">
  <link rel="alternate" hreflang="x-default" href="https://fukuoka-golf-guide.com/report-{slug}.html">

{GA4_SCRIPT}
{CSS}
</head>
<body>

<a href="index.html" class="back-link">← Top</a>

<section class="hero">
  <div class="hero-img" style="background-image: {hero_gradient};"></div>
  <div class="hero-inner">
    <div class="hero-eyebrow">— Editor's Field Report · {date_pub}</div>
    <h1 class="hero-title">{hero_title}</h1>
    <p class="hero-sub">{hero_sub}</p>
    <div class="hero-badges">
      {''.join(f'<span class="hero-badge">{b}</span>' for b in badges)}
    </div>
  </div>
</section>

<div class="stats-band">
  <div class="stats-band-inner">
    <div class="stats-band-item">
      <div class="stats-band-num">{stat1_num}<span class="unit">{stat1_unit}</span></div>
      <div class="stats-band-label">{stat1_label}</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{stat2_num}<span class="unit">{stat2_unit}</span></div>
      <div class="stats-band-label">{stat2_label}</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{stat3_num}<span class="unit">{stat3_unit}</span></div>
      <div class="stats-band-label">{stat3_label}</div>
    </div>
    <div class="stats-band-item">
      <div class="stats-band-num">{stat4_num}<span class="unit">{stat4_unit}</span></div>
      <div class="stats-band-label">{stat4_label}</div>
    </div>
  </div>
</div>

{sections_html}

<section class="section section-pale">
  <div class="sec-eyebrow">— 予約・基本情報</div>
  <h2 class="sec-title">予約はじゃらんゴルフ・楽天 GORA から。</h2>
  <div class="prose">
    <p>ビジター予約は <strong>じゃらんゴルフ</strong> から空き状況を確認するのが確実です。キャンセル料・最低人数などの条件は予約画面でご確認ください。</p>
  </div>
  <div class="cta-row">
    <a href="{jalan_url}" class="ftv-cta-btn" target="_blank" rel="nofollow sponsored noopener">📅 じゃらんゴルフで{name_ja}を予約 →</a>
    {rakuten_btn}
  </div>
  <div class="disclaimer" style="margin-top:28px;">
    ※ 本レポートは編集部の一回のラウンドに基づく一次体験記です。コースの感じ方には個人差があります。最新の料金・予約状況・コース状態は公式サイトおよびじゃらんゴルフ・楽天 GORA の予約画面でご確認ください。
  </div>
</section>

<section class="section related-section">
  <div class="sec-eyebrow">— 関連ページ</div>
  <h2 class="sec-title">コース詳細・他の現地レポートも。</h2>
  <div class="related-grid">
{related_html}
  </div>
</section>

<footer>
  <p><a href="index.html">福岡ゴルフ場ガイド</a> — 福岡近郊 50 コース掲載</p>
  <p style="margin-top:8px;font-size:12px;">本サイトはアフィリエイトプログラムを利用しています。リンク先での購入・予約により当サイトに報酬が生じる場合があります。</p>
</footer>

{FOOTER_JS}
</body>
</html>'''


# ============================================================
# 1. 福岡レイクサイドカントリークラブ
# ============================================================
LAKESIDE_SECTIONS = '''
<section class="section">
  <div class="sec-eyebrow">— Editor's First-hand Round Report</div>
  <h2 class="sec-title">率直な感想 — 入り口から美しく、スコアが出しやすいコース。</h2>
  <div class="prose">
    <p>編集部が <strong>2026 年 5 月に福岡レイクサイドカントリークラブ</strong> を実際にラウンドしてきました。第一印象から「<strong>入り口がキレイ</strong>」と感じるほどコース管理が行き届いており、雰囲気が良い。そしてラウンドを通じて実感したのが「<strong>スコアが出やすいレイアウト</strong>」であるということ。</p>
    <p>厳しい地形やトリッキーなホールが続くコースと違い、きちんと打てば素直に報いてくれる設計。<strong>「気持ちよくラウンドできる」コース</strong>とはこういうことかと感じました。</p>
  </div>
  <div class="pull-quote">「入り口からの雰囲気が良く、終始リラックスして回れるコース。スコアにも正直に反映される。」</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Observation 1 / コースの美しさ</div>
  <h2 class="sec-title">入り口から漂う「整えられたコース」の空気感。</h2>
  <div class="prose">
    <p>クラブハウスへのアプローチから、フェアウェイのコンディションまで、全体的に手入れが行き届いた印象。特に<strong>コース全体の清潔感と緑のコントラスト</strong>が気持ちよく、スタート前から気分が上がります。</p>
    <p>県内のコースを多く回ってきましたが、「環境が整っているだけでラウンドの満足度は上がる」と改めて感じたコースです。料金に対してコースクオリティの<strong>コストパフォーマンスが高い</strong>と感じました。</p>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Observation 2 / コースレイアウト</div>
  <h2 class="sec-title">素直なレイアウトで、打った通りの結果が出る。</h2>
  <div class="prose">
    <p>急激な高低差や、理不尽なアンジュレーションが少なく、<strong>「打ったところに球が落ちる」安心感</strong> があります。フェアウェイキープができれば、アプローチへの集中につながり、スコアにもそのまま反映される。</p>
    <p>「スコアを崩されているのはコースのせいではなく自分のミス」と素直に向き合えるのが、このコースの良いところ。<strong>自分のゴルフの実力を正直に確かめたい人</strong>にとって、非常に適したコースだと思います。</p>
    <p>初心者の方にも比較的取り組みやすく、<strong>グループで気軽に楽しめるコース</strong>として定番になっている理由がよくわかりました。</p>
  </div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Editor's Verdict</div>
  <h2 class="sec-title">「気持ちよくスコアが出るラウンド」を楽しみたい人に。</h2>
  <div class="prose">
    <p>難しいコースへの挑戦ではなく、<strong>「快適に、楽しく、スコアも出したい」というラウンド</strong>を求める人に間違いなくおすすめできます。コースの美しさと整備状態、スコアが出やすいレイアウトが三位一体となって、満足度の高いゴルフを提供してくれるコースです。</p>
    <p>コンペや友人・家族との記念ラウンドにも向いており、誰を誘っても喜ばれそう。<strong>福岡近郊で「また来たいコース」のひとつ</strong>に、迷わず加えました。</p>
    <div class="disclaimer">
      ※ 本レポートは編集部の一回のラウンドに基づく一次体験記です。最新の料金・予約状況は公式サイト・じゃらんゴルフ・楽天 GORA でご確認ください。
    </div>
  </div>
</section>'''

LAKESIDE_RELATED = '''    <a href="course-lakeside.html" class="related-card">
      <span class="related-name">福岡レイクサイドCC コース詳細</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="report-kurume.html" class="related-card">
      <span class="related-name">久留米CC 現地レポート</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="area-chikuho.html" class="related-card">
      <span class="related-name">筑豊エリア ゴルフ場一覧</span>
      <span class="related-arrow">→</span>
    </a>'''

html_lakeside = build_html(
    slug='lakeside',
    name_ja='福岡レイクサイドカントリークラブ',
    name_en='Fukuoka Lakeside CC',
    location='飯塚市',
    airport_min=40,
    price_weekday='¥7,000+',
    price_area='',
    hero_gradient='linear-gradient(180deg, rgba(42,94,128,0.22) 0%, rgba(44,94,128,0.25) 40%, rgba(22,56,80,0.88) 100%)',
    badges=['⛳ 18ホール', '📍 飯塚市', '✈️ 福岡空港 40 分', '📝 編集部実体験'],
    meta_desc='編集部が実際にラウンドした福岡レイクサイドカントリークラブ（飯塚市）の現地レポート。入り口からの美しさ、スコアが出やすいフラットなレイアウト、コスパの良さを一次体験で報告。',
    og_title='福岡レイクサイドCC 編集部現地レポート — 入り口から美しく、スコアが出やすいコース',
    og_desc='編集部が実際にラウンド。コース管理の美しさとスコアが出やすい素直なレイアウトを現地から報告。',
    headline='福岡レイクサイドCC 編集部ラウンドレポート — 入り口から美しく、スコアが出やすいコース',
    hero_title='レイクサイドCC、入り口から美しく、<br>素直にスコアが出るコース。',
    hero_sub='編集部が実際に 18 ホールを回ってきました。整えられたコース美観、スコアに正直なフラットなレイアウト — 「気持ちよくラウンドしたい」人に贈る現地レポートです。',
    stat1_num='18', stat1_unit='H', stat1_label='フラット / 丘陵',
    stat2_num='¥7,000', stat2_unit='+', stat2_label='平日最安目安',
    stat3_num='40', stat3_unit='min', stat3_label='福岡空港から',
    stat4_num='飯塚', stat4_unit='市', stat4_label='筑豊エリア',
    sections_html=LAKESIDE_SECTIONS,
    jalan_url=JALAN_BASE + 'gc02346%2F',
    rakuten_url=RAKUTEN_BASE + '400044%26m%3Dhttps%253A%252F%252Fbooking.gora.golf.rakuten.co.jp%252Fguide%252Fdisp%252Fc_id%252F400044',
    related_html=LAKESIDE_RELATED,
)

# ============================================================
# 2. ミッションバレーゴルフクラブ
# ============================================================
MISSION_SECTIONS = '''
<section class="section">
  <div class="sec-eyebrow">— Editor's First-hand Round Report</div>
  <h2 class="sec-title">率直な感想 — 想像以上に難しい。起伏とコブがスコアを奪う。</h2>
  <div class="prose">
    <p>編集部が <strong>2026 年 5 月にミッションバレーゴルフクラブ</strong> を実際にラウンドしてきました。「コブが多い」という事前情報は持っていましたが、実際に回ると<strong>その起伏の大きさは想像以上</strong>でした。</p>
    <p>フェアウェイの至るところに大きなマウンドやアンジュレーションがあり、フラットなライで打てるホールの方が少ない印象。<strong>スコアが出にくいコース</strong>ですが、だからこそ「攻略する楽しさ」がある本格派のコースです。</p>
    <p>また、プロ野球選手も訪れることがあるとの話を聞きました。それだけ本格的な練習コースとして認知されている証かもしれません。</p>
  </div>
  <div class="pull-quote">「コブが大きく、フラットなライがほとんどない。スコアより、コースとの対話を楽しむ一日。」</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Observation 1 / 起伏とコブ</div>
  <h2 class="sec-title">大きなコブが、球のライとメンタルを試す。</h2>
  <div class="prose">
    <p>ミッションバレー最大の特徴は<strong>フェアウェイの大きな起伏（コブ）</strong>です。ティーショットでフェアウェイをキープしても、着地点が傾斜になっていることが多く、<strong>傾斜ライからのセカンドショット</strong>を常に強いられます。</p>
    <p>「スタンスが取れない」「ボールが足より上 / 下にある」という状況が頻繁に発生するため、<strong>傾斜ライへの対応力</strong>がスコアを大きく左右します。コブ越えのアプローチも多く、グリーン周りでも気が抜けません。</p>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Observation 2 / スコアマネジメント</div>
  <h2 class="sec-title">「崩れた後のマネジメント」が問われるコース。</h2>
  <div class="prose">
    <p>一度コブにハマると連続してミスが出やすい構造になっています。<strong>無理に取り返そうとせず、ボギーを受け入れる冷静さ</strong> が求められます。</p>
    <p>このコースでスコアをまとめるには、「完璧なショットを求めない」「コブからの脱出を最優先」という<strong>リスクマネジメント重視の戦略</strong>が効果的です。難易度の高さを楽しめる中上級者向けのコースと言えます。</p>
    <p><strong>練習目的のラウンドにも最適</strong>で、傾斜ライや変則的なアプローチを繰り返すことで確実に技術が磨かれます。プロ選手も実戦的な練習コースとして使う理由がよくわかりました。</p>
  </div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Editor's Verdict</div>
  <h2 class="sec-title">「本気で鍛えたい」中上級者のコース選びの一択。</h2>
  <div class="prose">
    <p>スコアを求めてラウンドすると苦しいですが、<strong>「コースに打ち勝つ楽しさ」や「技術的な課題を見つける目的」</strong>で来るなら、これほど充実したコースはありません。大きなコブと起伏が生み出す多様なライが、ゴルファーの基礎力を否応なく試してきます。</p>
    <p>「簡単なコースでは物足りない」「傾斜ライの練習がしたい」「本気でハンデを縮めたい」という方に、自信を持っておすすめできます。<strong>福岡近郊で「本格的に難しいコース」を求めるなら、ミッションバレーは外せない一択</strong>です。</p>
    <div class="disclaimer">
      ※ 本レポートは編集部の一回のラウンドに基づく一次体験記です。最新の料金・予約状況は公式サイト・じゃらんゴルフでご確認ください。
    </div>
  </div>
</section>'''

MISSION_RELATED = '''    <a href="course-mission.html" class="related-card">
      <span class="related-name">ミッションバレーGC コース詳細</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="report-kurume.html" class="related-card">
      <span class="related-name">久留米CC 現地レポート</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="hub-beginner.html" class="related-card">
      <span class="related-name">初心者向け コース特集</span>
      <span class="related-arrow">→</span>
    </a>'''

html_mission = build_html(
    slug='mission',
    name_ja='ミッションバレーゴルフクラブ',
    name_en='Mission Valley GC',
    location='鞍手郡小竹町',
    airport_min=50,
    price_weekday='¥5,000+',
    price_area='',
    hero_gradient='linear-gradient(180deg, rgba(20,55,35,0.20) 0%, rgba(22,56,41,0.28) 40%, rgba(10,35,20,0.90) 100%)',
    badges=['⛳ 18ホール・起伏大', '📍 鞍手郡小竹町', '✈️ 福岡空港 50 分', '📝 編集部実体験'],
    meta_desc='編集部が実際にラウンドしたミッションバレーゴルフクラブ（鞍手郡小竹町）の現地レポート。大きなコブと起伏が特徴のスコアが出にくい本格コース。中上級者・技術向上目的のラウンドに最適。',
    og_title='ミッションバレーGC 編集部現地レポート — 大きなコブと起伏がスコアを試す本格コース',
    og_desc='編集部が実際にラウンド。大きなコブと起伏でスコアが出にくい本格派のコースを詳細レポート。',
    headline='ミッションバレーGC 編集部ラウンドレポート — 大きなコブと起伏が試す、本格難コース',
    hero_title='ミッションバレー、大きなコブと起伏が<br>スコアを試す本格コース。',
    hero_sub='編集部が実際に 18 ホールを回ってきました。フェアウェイを覆う大きなコブと急な起伏 — スコアより技術と対話を楽しむ、中上級者向けコースの現地レポートです。',
    stat1_num='18', stat1_unit='H', stat1_label='丘陵 / 起伏大',
    stat2_num='¥5,000', stat2_unit='+', stat2_label='平日最安目安',
    stat3_num='50', stat3_unit='min', stat3_label='福岡空港から',
    stat4_num='小竹', stat4_unit='町', stat4_label='筑豊・鞍手郡',
    sections_html=MISSION_SECTIONS,
    jalan_url=JALAN_BASE + 'gc02338%2F',
    rakuten_url='',  # じゃらんのみ
    related_html=MISSION_RELATED,
)

# ============================================================
# 3. 小倉カンツリー倶楽部
# ============================================================
KOKURA_SECTIONS = '''
<section class="section">
  <div class="sec-eyebrow">— Editor's First-hand Round Report</div>
  <h2 class="sec-title">率直な感想 — 名門の風格と、行き届いたコース整備が光る。</h2>
  <div class="prose">
    <p>編集部が <strong>2026 年 5 月に小倉カンツリー倶楽部</strong> を実際にラウンドしてきました。1961 年開場・上田治設計という名門の歴史を持つコースは、フェアウェイの状態からグリーンコンディションまで、<strong>「しっかり整備されている」という安心感</strong>がラウンド全体を通じて続きます。</p>
    <p>パー72・6,872 ヤードというコース規模も、タフさと楽しさのバランスが絶妙。<strong>本格的な名門コースの雰囲気を体感できる</strong>、福岡近郊では数少ない一本です。</p>
  </div>
  <div class="pull-quote">「コースの整備状態が素晴らしく、気持ちよく集中できるラウンド。名門の格式とホスピタリティを実感した。」</div>
</section>

<section class="section section-pale">
  <div class="sec-eyebrow">— Observation 1 / コース整備</div>
  <h2 class="sec-title">フェアウェイからグリーンまで、整備の質が高い。</h2>
  <div class="prose">
    <p>小倉カンツリーで最初に気づいたのは<strong>コース全体の整備水準の高さ</strong>です。フェアウェイの芝は均一に刈り込まれており、ラフとの境界もはっきりしている。グリーンは適度な速さと均一な転がりがあり、<strong>「読んだ通りのパッティングができる」</strong>コンディションでした。</p>
    <p>「コースが整っていると、ミスが言い訳しにくい」とはよく言いますが、まさにその通り。整備の質が高いコースでのラウンドは、<strong>自分のゴルフそのものと向き合える</strong> 時間になります。</p>
  </div>
</section>

<section class="section">
  <div class="sec-eyebrow">— Observation 2 / キャディサービス</div>
  <h2 class="sec-title">キャディさんのアプローチ案内が、ラウンドの質を上げる。</h2>
  <div class="prose">
    <p>小倉カンツリーでとりわけ印象的だったのが<strong>キャディさんのサポートの丁寧さ</strong>です。グリーン周りのアプローチについて、「このラインから打った方がいい」「この傾斜だとこう転がる」という具体的なアドバイスが的確で、スコアに直接貢献してくれます。</p>
    <p>ただ距離を読むだけでなく、<strong>コースの傾斜や芝目まで含めた実践的な情報</strong>を教えてくれるキャディワークは、まさに名門コースのプロフェッショナルなサービス。<strong>「キャディさんと一緒にコースを攻略する楽しさ」</strong>を久しぶりに実感しました。</p>
  </div>
</section>

<section class="section section-warm">
  <div class="sec-eyebrow">— Editor's Verdict</div>
  <h2 class="sec-title">接待・記念ラウンド・「本物の名門」を体感したい方に。</h2>
  <div class="prose">
    <p>料金は福岡近郊のコースとしては高めですが、<strong>それに見合う価値を確実に提供してくれるコース</strong>です。コース整備の質、キャディサービスのレベル、名門ならではの雰囲気 — どれも「一流を体験したい」というニーズに応えています。</p>
    <p><strong>接待ゴルフ、特別な記念ラウンド、初めて名門コースに挑戦する方</strong>に、自信を持っておすすめできます。平日 13,769 円〜という価格も、この内容であれば納得感があります。</p>
    <div class="disclaimer">
      ※ 本レポートは編集部の一回のラウンドに基づく一次体験記です。最新の料金・予約状況は公式サイト・じゃらんゴルフ・楽天 GORA でご確認ください。
    </div>
  </div>
</section>'''

KOKURA_RELATED = '''    <a href="course-kokura.html" class="related-card">
      <span class="related-name">小倉カンツリー倶楽部 コース詳細</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="report-kurume.html" class="related-card">
      <span class="related-name">久留米CC 現地レポート</span>
      <span class="related-arrow">→</span>
    </a>
    <a href="hub-business.html" class="related-card">
      <span class="related-name">接待向け コース特集</span>
      <span class="related-arrow">→</span>
    </a>'''

html_kokura = build_html(
    slug='kokura',
    name_ja='小倉カンツリー倶楽部',
    name_en='Kokura Country Club',
    location='北九州市小倉南区',
    airport_min=60,
    price_weekday='¥13,769+',
    price_area='',
    hero_gradient='linear-gradient(180deg, rgba(20,20,30,0.18) 0%, rgba(42,42,60,0.30) 40%, rgba(22,22,38,0.88) 100%)',
    badges=['⛳ 18H・Par72・6,872y', '📍 北九州市小倉南区', '🏆 1961年開場・上田治設計', '📝 編集部実体験'],
    meta_desc='編集部が実際にラウンドした小倉カンツリー倶楽部（北九州市小倉南区）の現地レポート。1961年開場・上田治設計の名門コース。コース整備の高水準とキャディサービスの質を一次体験で報告。',
    og_title='小倉カンツリー倶楽部 編集部現地レポート — 名門の整備とキャディワークが光るコース',
    og_desc='編集部が実際にラウンド。1961年開場の名門コースの整備水準とキャディサービスの質を詳細レポート。',
    headline='小倉カンツリー倶楽部 編集部ラウンドレポート — 名門の整備とキャディワークが光る格式コース',
    hero_title='小倉カンツリー、整備された名門コースと<br>プロのキャディワークが光る。',
    hero_sub='編集部が実際に 18 ホールを回ってきました。1961 年開場・上田治設計の名門コース。高水準のコース整備と的確なキャディサービス — 本物の「名門体験」を現地から報告します。',
    stat1_num='18', stat1_unit='H', stat1_label='Par72 / 6,872y',
    stat2_num='¥13,769', stat2_unit='+', stat2_label='平日目安',
    stat3_num='1961', stat3_unit='年', stat3_label='開場・上田治設計',
    stat4_num='北九州', stat4_unit='市', stat4_label='小倉南区',
    sections_html=KOKURA_SECTIONS,
    jalan_url=JALAN_BASE + 'gc02309%2F',
    rakuten_url=RAKUTEN_KOKURA,
    related_html=KOKURA_RELATED,
)

# ============================================================
# 書き出し
# ============================================================
files = [
    ('report-lakeside.html', html_lakeside),
    ('report-mission.html',  html_mission),
    ('report-kokura.html',   html_kokura),
]

for fname, html in files:
    for root in [REPO, PREVIEW]:
        out = root / fname
        if DRY:
            print(f'  [DRY-RUN] would write {out} ({len(html):,} chars)')
        else:
            out.write_text(html, encoding='utf-8')
            print(f'  wrote {out} ({len(html):,} chars)')

print('DONE' if not DRY else '*** DRY-RUN ***')
