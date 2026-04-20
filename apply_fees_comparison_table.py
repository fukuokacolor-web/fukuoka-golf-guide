#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fees.html に「28コース料金比較表」(ソート可能・3言語対応) を注入。
データ源: update_prices.py PRICE_DATA + COURSE_NAMES (当スクリプト内)
1回実行すれば idempotent (MARK_TABLE 重複検知)
"""
import os, io, sys, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = r'C:/Users/Owner/fukuoka-golf-guide'

# 28コースの3言語名（表示用・短め）
COURSE_NAMES = {
    "aburayama":     {"ja":"油山ゴルフクラブ",               "en":"Aburayama GC",            "ko":"아부라야마 GC",          "area_ja":"福岡市城南区","area_en":"Fukuoka City","area_ko":"후쿠오카시"},
    "akane":         {"ja":"あかねゴルフクラブ",             "en":"Akane GC",                "ko":"아카네 GC",              "area_ja":"糟屋郡","area_en":"Kasuya","area_ko":"카스야"},
    "ariake":        {"ja":"有明グランドゴルフクラブ",        "en":"Ariake Grand GC",         "ko":"아리아케 그랜드 GC",     "area_ja":"大牟田市","area_en":"Omuta","area_ko":"오무타"},
    "asoiizuka":     {"ja":"麻生飯塚ゴルフ倶楽部",           "en":"Aso Iizuka GC",           "ko":"아소 이이즈카 GC",       "area_ja":"飯塚市","area_en":"Iizuka","area_ko":"이이즈카"},
    "central":       {"ja":"セントラルゴルフクラブ",          "en":"Central GC",              "ko":"센트럴 GC",              "area_ja":"糟屋郡","area_en":"Kasuya","area_ko":"카스야"},
    "century":       {"ja":"センチュリー三木ゴルフ倶楽部",    "en":"Century Miki GC",         "ko":"센추리 미키 GC",         "area_ja":"糟屋郡","area_en":"Kasuya","area_ko":"카스야"},
    "chikushigaoka": {"ja":"筑紫ヶ丘ゴルフクラブ",           "en":"Chikushigaoka GC",        "ko":"치쿠시가오카 GC",        "area_ja":"那珂川市","area_en":"Nakagawa","area_ko":"나카가와"},
    "chikushino":    {"ja":"筑紫野カントリークラブ",          "en":"Chikushino CC",           "ko":"치쿠시노 CC",            "area_ja":"筑紫野市","area_en":"Chikushino","area_ko":"치쿠시노"},
    "daihakata":     {"ja":"大博多カンツリー倶楽部",          "en":"Daihakata CC",            "ko":"다이하카타 CC",          "area_ja":"那珂川市","area_en":"Nakagawa","area_ko":"나카가와"},
    "dazaifu":       {"ja":"太宰府ゴルフ倶楽部",              "en":"Dazaifu GC",              "ko":"다자이후 GC",            "area_ja":"太宰府市","area_en":"Dazaifu","area_ko":"다자이후"},
    "fukuokacc":     {"ja":"福岡カンツリー倶楽部（和白）",    "en":"Fukuoka CC (Wajiro)",     "ko":"후쿠오카 CC (와지로)",   "area_ja":"福岡市東区","area_en":"Fukuoka City","area_ko":"후쿠오카시"},
    "hisayama":      {"ja":"久山カントリー倶楽部",            "en":"Hisayama CC",             "ko":"히사야마 CC",            "area_ja":"糟屋郡","area_en":"Kasuya","area_ko":"카스야"},
    "ito":           {"ja":"伊都ゴルフクラブ",                "en":"Ito GC",                  "ko":"이토 GC",                "area_ja":"糸島市","area_en":"Itoshima","area_ko":"이토시마"},
    "keya":          {"ja":"芥屋ゴルフ倶楽部",                "en":"Keya GC",                 "ko":"케야 GC",                "area_ja":"糸島市","area_en":"Itoshima","area_ko":"이토시마"},
    "kitakyushu":    {"ja":"北九州カントリー倶楽部",          "en":"Kitakyushu CC",           "ko":"기타큐슈 CC",            "area_ja":"北九州市","area_en":"Kitakyushu","area_ko":"기타큐슈"},
    "koga":          {"ja":"古賀ゴルフクラブ",                "en":"Koga GC",                 "ko":"코가 GC",                "area_ja":"古賀市","area_en":"Koga","area_ko":"코가"},
    "kurume":        {"ja":"久留米カントリークラブ",          "en":"Kurume CC",               "ko":"쿠루메 CC",              "area_ja":"久留米市","area_en":"Kurume","area_ko":"쿠루메"},
    "kyushugc":      {"ja":"九州ゴルフ倶楽部 八幡コース",     "en":"Kyushu GC Yahata",        "ko":"큐슈 GC 야하타",         "area_ja":"北九州市","area_en":"Kitakyushu","area_ko":"기타큐슈"},
    "lakeside":      {"ja":"福岡レイクサイドCC",             "en":"Fukuoka Lakeside CC",     "ko":"후쿠오카 레이크사이드 CC","area_ja":"飯塚市","area_en":"Iizuka","area_ko":"이이즈카"},
    "mission":       {"ja":"ミッションバレーゴルフクラブ",    "en":"Mission Valley GC",       "ko":"미션밸리 GC",            "area_ja":"鞍手郡小竹町","area_en":"Kurate","area_ko":"쿠라테"},
    "moji":          {"ja":"門司ゴルフ倶楽部",                "en":"Moji GC",                 "ko":"모지 GC",                "area_ja":"北九州市","area_en":"Kitakyushu","area_ko":"기타큐슈"},
    "moonlake":      {"ja":"ムーンレイクゴルフクラブ",        "en":"Moon Lake GC",            "ko":"문레이크 GC",            "area_ja":"飯塚市","area_en":"Iizuka","area_ko":"이이즈카"},
    "nijo":          {"ja":"二丈カントリークラブ",            "en":"Nijo CC",                 "ko":"니조 CC",                "area_ja":"糸島市","area_en":"Itoshima","area_ko":"이토시마"},
    "ogori":         {"ja":"小郡カンツリー倶楽部",            "en":"Ogori CC",                "ko":"오고리 CC",              "area_ja":"小郡市","area_en":"Ogori","area_ko":"오고리"},
    "queenshill":    {"ja":"クイーンズヒルゴルフクラブ",      "en":"Queen's Hill GC",         "ko":"퀸즈힐 GC",              "area_ja":"糸島市","area_en":"Itoshima","area_ko":"이토시마"},
    "saitozaki":     {"ja":"西戸崎シーサイドCC",             "en":"Saitozaki Seaside CC",    "ko":"사이토자키 시사이드 CC", "area_ja":"福岡市東区","area_en":"Fukuoka City","area_ko":"후쿠오카시"},
    "sevenmillion":  {"ja":"セブンミリオンGC",               "en":"Seven Million GC",        "ko":"세븐밀리언 GC",          "area_ja":"福岡市早良区","area_en":"Fukuoka City","area_ko":"후쿠오카시"},
    "wakamiya":      {"ja":"若宮ゴルフクラブ",                "en":"Wakamiya GC",             "ko":"와카미야 GC",            "area_ja":"宮若市","area_en":"Miyawaka","area_ko":"미야와카"},
}

PRICE_DATA = {
    "aburayama":{"wd_lo":3000,"wd_hi":4500,"we_lo":3200,"we_hi":4500},
    "akane":{"wd_lo":3500,"wd_hi":15000,"we_lo":3500,"we_hi":21000},
    "ariake":{"wd_lo":7000,"wd_hi":8500,"we_lo":10500,"we_hi":11500},
    "asoiizuka":{"wd_lo":9000,"wd_hi":15000,"we_lo":9500,"we_hi":21500},
    "central":{"wd_lo":6500,"wd_hi":12000,"we_lo":8000,"we_hi":14000},
    "century":{"wd_lo":9500,"wd_hi":21500,"we_lo":11500,"we_hi":21500},
    "chikushigaoka":{"wd_lo":13900,"wd_hi":13900,"we_lo":18400,"we_hi":18400},
    "chikushino":{"wd_lo":9500,"wd_hi":17000,"we_lo":10000,"we_hi":18000},
    "daihakata":{"wd_lo":3500,"wd_hi":11500,"we_lo":8000,"we_hi":14500},
    "dazaifu":{"wd_lo":11000,"wd_hi":15500,"we_lo":14000,"we_hi":22500},
    "fukuokacc":{"wd_lo":5000,"wd_hi":12000,"we_lo":8000,"we_hi":15500},
    "hisayama":{"wd_lo":3500,"wd_hi":12000,"we_lo":4000,"we_hi":15000},
    "ito":{"wd_lo":9000,"wd_hi":22000,"we_lo":9000,"we_hi":22000},
    "keya":{"wd_lo":21500,"wd_hi":25000,"we_lo":30500,"we_hi":34000},
    "kitakyushu":{"wd_lo":7000,"wd_hi":10500,"we_lo":11500,"we_hi":11500},
    "koga":{"wd_lo":24800,"wd_hi":30000,"we_lo":30100,"we_hi":36200},
    "kurume":{"wd_lo":6000,"wd_hi":8500,"we_lo":10000,"we_hi":14500},
    "kyushugc":{"wd_lo":15500,"wd_hi":15500,"we_lo":15500,"we_hi":20000},
    "lakeside":{"wd_lo":7000,"wd_hi":12000,"we_lo":7000,"we_hi":16000},
    "mission":{"wd_lo":5000,"wd_hi":12000,"we_lo":8000,"we_hi":15000},
    "moji":{"wd_lo":6000,"wd_hi":28000,"we_lo":6000,"we_hi":33000},
    "moonlake":{"wd_lo":6500,"wd_hi":9000,"we_lo":6500,"we_hi":14500},
    "nijo":{"wd_lo":4000,"wd_hi":13000,"we_lo":7500,"we_hi":16000},
    "ogori":{"wd_lo":13500,"wd_hi":14500,"we_lo":18000,"we_hi":19000},
    "queenshill":{"wd_lo":21800,"wd_hi":21800,"we_lo":30200,"we_hi":30200},
    "saitozaki":{"wd_lo":6000,"wd_hi":10000,"we_lo":5500,"we_hi":15000},
    "sevenmillion":{"wd_lo":9500,"wd_hi":15000,"we_lo":10500,"we_hi":15000},
    "wakamiya":{"wd_lo":8000,"wd_hi":15500,"we_lo":12500,"we_hi":17000},
}

MARK = '<!-- COMPARISON_TABLE -->'

CSS_ADDITION = '''
    .cmp-intro { font-size:0.82rem; color:#555; margin-bottom:10px; line-height:1.6; }
    .cmp-ctrl { display:flex; gap:6px; margin:8px 0 10px; flex-wrap:wrap; }
    .cmp-btn { border:1.5px solid #b8d9c5; background:var(--green-light); color:var(--green-dark); border-radius:18px; padding:5px 12px; font-size:0.74rem; font-weight:700; cursor:pointer; transition:all .15s; }
    .cmp-btn:hover { background:#d0eedd; }
    .cmp-btn.on { background:var(--green-mid); color:#fff; border-color:var(--green-mid); }
    .cmp-table { width:100%; background:#fff; border-radius:var(--radius); box-shadow:0 3px 10px rgba(0,0,0,.08); overflow:hidden; }
    .cmp-row { display:grid; grid-template-columns:minmax(0,1.6fr) 0.9fr 0.9fr auto; gap:4px; align-items:center; padding:10px 12px; border-bottom:1px dashed #e0e8e0; font-size:0.78rem; }
    .cmp-row:last-child { border-bottom:none; }
    .cmp-row.cmp-head { background:var(--green-light); font-weight:800; font-size:0.7rem; color:var(--green-dark); text-transform:uppercase; letter-spacing:0.05em; padding:8px 12px; }
    .cmp-name { font-weight:800; color:var(--green-dark); line-height:1.3; min-width:0; }
    .cmp-name small { display:block; font-size:0.66rem; font-weight:600; color:var(--muted); margin-top:1px; }
    .cmp-price { font-weight:700; color:#333; text-align:right; font-size:0.76rem; white-space:nowrap; }
    .cmp-cta { background:linear-gradient(135deg,#c9a227,#e6b82e); color:#4a3500 !important; border-radius:8px; padding:6px 10px; font-size:0.72rem; font-weight:800; text-decoration:none; box-shadow:0 2px 4px rgba(0,0,0,0.12); white-space:nowrap; }
    .cmp-cta:active { transform:translateY(1px); }
    @media (max-width:420px) {
      .cmp-row { grid-template-columns:1.4fr 0.9fr auto; }
      .cmp-row .cmp-price.we { display:none; }
      .cmp-head .cmp-price.we { display:none; }
    }
'''

TABLE_JA = '''
  <div class="sec-head" id="cmp-ja">⚖️ 28コース料金比較表（クリック詳細＆予約へ）</div>
  <p class="cmp-intro">福岡近郊28コースの平日・土日料金を一覧。予算順にソートして比較、気になるコースの「詳細 →」で詳細ページ＆予約へ。</p>
  <div class="cmp-ctrl">
    <button class="cmp-btn on" data-sort="wd_lo" data-lang="ja" onclick="cmpSort(this,'ja','wd_lo')">💲 平日・安い順</button>
    <button class="cmp-btn"    data-sort="we_lo" data-lang="ja" onclick="cmpSort(this,'ja','we_lo')">🎉 土日・安い順</button>
    <button class="cmp-btn"    data-sort="name"  data-lang="ja" onclick="cmpSort(this,'ja','name')">🔤 名前順</button>
  </div>
  <div class="cmp-table" id="cmp-tbl-ja"></div>
'''

TABLE_EN = '''
  <div class="sec-head" id="cmp-en">⚖️ 28 Courses Fee Comparison (Click for Detail & Booking)</div>
  <p class="cmp-intro">Weekday &amp; weekend green fees for 28 courses near Fukuoka. Sort by budget, then click "Detail →" for full info and booking.</p>
  <div class="cmp-ctrl">
    <button class="cmp-btn on" data-sort="wd_lo" data-lang="en" onclick="cmpSort(this,'en','wd_lo')">💲 Weekday low→high</button>
    <button class="cmp-btn"    data-sort="we_lo" data-lang="en" onclick="cmpSort(this,'en','we_lo')">🎉 Weekend low→high</button>
    <button class="cmp-btn"    data-sort="name"  data-lang="en" onclick="cmpSort(this,'en','name')">🔤 Name A→Z</button>
  </div>
  <div class="cmp-table" id="cmp-tbl-en"></div>
'''

TABLE_KO = '''
  <div class="sec-head" id="cmp-ko">⚖️ 28개 코스 요금 비교표 (클릭하여 상세·예약)</div>
  <p class="cmp-intro">후쿠오카 인근 28개 코스의 평일·주말 요금. 예산순으로 정렬하고 "상세 →"를 눌러 코스 상세페이지&amp;예약으로 이동하세요.</p>
  <div class="cmp-ctrl">
    <button class="cmp-btn on" data-sort="wd_lo" data-lang="ko" onclick="cmpSort(this,'ko','wd_lo')">💲 평일 저렴순</button>
    <button class="cmp-btn"    data-sort="we_lo" data-lang="ko" onclick="cmpSort(this,'ko','we_lo')">🎉 주말 저렴순</button>
    <button class="cmp-btn"    data-sort="name"  data-lang="ko" onclick="cmpSort(this,'ko','name')">🔤 이름순</button>
  </div>
  <div class="cmp-table" id="cmp-tbl-ko"></div>
'''


def _build_course_data_js():
    items = []
    for key, names in COURSE_NAMES.items():
        p = PRICE_DATA[key]
        items.append({
            'key': key, 'ja': names['ja'], 'en': names['en'], 'ko': names['ko'],
            'area_ja': names['area_ja'], 'area_en': names['area_en'], 'area_ko': names['area_ko'],
            'wd_lo': p['wd_lo'], 'wd_hi': p['wd_hi'], 'we_lo': p['we_lo'], 'we_hi': p['we_hi']
        })
    import json
    return json.dumps(items, ensure_ascii=False)


def _build_render_script():
    data_js = _build_course_data_js()
    return '''
<script>
(function(){
  var COURSES = ''' + data_js + ''';
  var L10N = {
    ja: {head_name:"コース", head_wd:"平日", head_we:"土日", cta:"詳細 →", price_prefix:"約", price_suffix:"円"},
    en: {head_name:"Course", head_wd:"Wkd", head_we:"Wknd", cta:"Detail →", price_prefix:"¥", price_suffix:""},
    ko: {head_name:"코스", head_wd:"평일", head_we:"주말", cta:"상세 →", price_prefix:"약 ", price_suffix:"엔"}
  };
  function fmt(lo, hi, lang){
    var p = L10N[lang];
    var n = function(v){ return v.toLocaleString("en-US"); };
    if (lo === hi) return p.price_prefix + n(lo) + p.price_suffix;
    return p.price_prefix + n(lo) + "〜" + n(hi) + p.price_suffix;
  }
  function render(lang, sortKey){
    var el = document.getElementById("cmp-tbl-" + lang);
    if (!el) return;
    var items = COURSES.slice();
    if (sortKey === "name") items.sort(function(a,b){ return a[lang].localeCompare(b[lang]); });
    else items.sort(function(a,b){ return a[sortKey] - b[sortKey]; });
    var p = L10N[lang];
    var head = '<div class="cmp-row cmp-head">'+
      '<div>'+p.head_name+'</div>'+
      '<div class="cmp-price">'+p.head_wd+'</div>'+
      '<div class="cmp-price we">'+p.head_we+'</div>'+
      '<div></div></div>';
    var rows = items.map(function(c){
      return '<div class="cmp-row">'+
        '<div class="cmp-name">'+c[lang]+'<small>'+c["area_"+lang]+'</small></div>'+
        '<div class="cmp-price">'+fmt(c.wd_lo,c.wd_hi,lang)+'</div>'+
        '<div class="cmp-price we">'+fmt(c.we_lo,c.we_hi,lang)+'</div>'+
        '<a class="cmp-cta" href="course-'+c.key+'.html">'+p.cta+'</a>'+
        '</div>';
    }).join("");
    el.innerHTML = head + rows;
  }
  window.cmpSort = function(btn, lang, key){
    var group = btn.parentElement.querySelectorAll(".cmp-btn[data-lang='"+lang+"']");
    group.forEach(function(b){ b.classList.remove("on"); });
    btn.classList.add("on");
    render(lang, key);
  };
  function initAll(){ render("ja","wd_lo"); render("en","wd_lo"); render("ko","wd_lo"); }
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", initAll);
  else initAll();
})();
</script>
'''


def main():
    path = os.path.join(BASE, 'fees.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()
    if MARK in html:
        print('Already applied — skipping.')
        return

    # CSSを追加
    html = html.replace('.booking-btn + .booking-btn { margin-left:6px; }',
                        '.booking-btn + .booking-btn { margin-left:6px; }' + CSS_ADDITION)

    # JA: 「📱 外国人も使いやすい予約サイト」の前に挿入
    html = html.replace(
        '<div class="sec-head">📱 外国人も使いやすい予約サイト</div>',
        MARK + TABLE_JA + '\n  <div class="sec-head">📱 外国人も使いやすい予約サイト</div>',
        1
    )
    # EN
    html = html.replace(
        '<div class="sec-head">📱 Booking Sites for Foreign Visitors</div>',
        TABLE_EN + '\n  <div class="sec-head">📱 Booking Sites for Foreign Visitors</div>',
        1
    )
    # KO
    html = html.replace(
        '<div class="sec-head">📱 외국인도 사용하기 쉬운 예약 사이트</div>',
        TABLE_KO + '\n  <div class="sec-head">📱 외국인도 사용하기 쉬운 예약 사이트</div>',
        1
    )

    # Render scriptを</body>直前に挿入
    html = html.replace('</body>', _build_render_script() + '\n</body>', 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'fees.html 更新完了 ({len(COURSE_NAMES)}コース×3言語の比較表を追加)')


if __name__ == '__main__':
    main()
