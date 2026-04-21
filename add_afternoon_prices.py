#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
午後スルー料金行を discount-box に追加するスクリプト。
対象: central / century / kitakyushu / kyushugc / lakeside / mission / moonlake / saitozaki
（午後スルー play-option は既存、discount-box の料金行のみ未追加）
1回実行すれば idempotent（MARK_AF で重複検知）
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/Owner/fukuoka-golf-guide'
MARK = '<!-- AF_PRICE_ADDED -->'

# 午後スルー料金データ（平日推定・税込・カート込）
DATA = {
    'central':    dict(ja='約4,000〜8,000円',   en='¥4,000–¥8,000',   ko='약 4,000〜8,000엔',   krw='약 4만원〜8만원'),
    'century':    dict(ja='約5,500〜12,000円',  en='¥5,500–¥12,000',  ko='약 5,500〜12,000엔',  krw='약 5.5만원〜12만원'),
    'kitakyushu': dict(ja='約4,500〜7,500円',   en='¥4,500–¥7,500',   ko='약 4,500〜7,500엔',   krw='약 4.5만원〜7.5만원'),
    'kyushugc':   dict(ja='約8,000〜12,000円',  en='¥8,000–¥12,000',  ko='약 8,000〜12,000엔',  krw='약 8만원〜12만원'),
    'lakeside':   dict(ja='約4,000〜8,000円',   en='¥4,000–¥8,000',   ko='약 4,000〜8,000엔',   krw='약 4만원〜8만원'),
    'mission':    dict(ja='約3,000〜7,000円',   en='¥3,000–¥7,000',   ko='약 3,000〜7,000엔',   krw='약 3만원〜7만원'),
    'moonlake':   dict(ja='約4,000〜6,500円',   en='¥4,000–¥6,500',   ko='약 4,000〜6,500엔',   krw='약 4만원〜6.5만원'),
    'saitozaki':  dict(ja='約3,500〜7,000円',   en='¥3,500–¥7,000',   ko='약 3,500〜7,000엔',   krw='약 3.5만원〜7만원'),
}

# 各コースの土日祝料金行（この行の直後に午後スルー行を挿入）
WE_ROWS_JA = {
    'central':    '    <div class="discount-row"><span>🎉 土日祝</span><strong>約8,000〜14,000円</strong></div>',
    'century':    '    <div class="discount-row"><span>🎉 土日祝</span><strong>約11,500〜21,500円</strong></div>',
    'kitakyushu': '    <div class="discount-row"><span>🎉 土日祝</span><strong>約11,500円</strong></div>',
    'kyushugc':   '    <div class="discount-row"><span>🎉 土日祝</span><strong>約15,500〜20,000円</strong></div>',
    'lakeside':   '    <div class="discount-row"><span>🎉 土日祝</span><strong>約7,000〜16,000円</strong></div>',
    'mission':    '    <div class="discount-row"><span>🎉 土日祝</span><strong>約8,000〜15,000円</strong></div>',
    'moonlake':   '    <div class="discount-row"><span>🎉 土日祝</span><strong>約6,500〜14,500円</strong></div>',
    'saitozaki':  '    <div class="discount-row"><span>🎉 土日祝</span><strong>約5,500〜15,000円</strong></div>',
}
WE_ROWS_EN = {
    'central':    '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥8,000–¥14,000</strong></div>',
    'century':    '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥11,500–¥21,500</strong></div>',
    'kitakyushu': '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥11,500</strong></div>',
    'kyushugc':   '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥15,500–¥20,000</strong></div>',
    'lakeside':   '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥7,000–¥16,000</strong></div>',
    'mission':    '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥8,000–¥15,000</strong></div>',
    'moonlake':   '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥6,500–¥14,500</strong></div>',
    'saitozaki':  '    <div class="discount-row"><span>🎉 Weekends / Holidays</span><strong>¥5,500–¥15,000</strong></div>',
}
WE_ROWS_KO = {
    'central':    '약 8,000〜14,000엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 8만원〜14만원)</span></strong></div>',
    'century':    '약 11,500〜21,500엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 11.5만원〜21.5만원)</span></strong></div>',
    'kitakyushu': '약 11,500엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 11.5만원)</span></strong></div>',
    'kyushugc':   '약 15,500〜20,000엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 15.5만원〜20만원)</span></strong></div>',
    'lakeside':   '약 7,000〜16,000엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 7만원〜16만원)</span></strong></div>',
    'mission':    '약 8,000〜15,000엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 8만원〜15만원)</span></strong></div>',
    'moonlake':   '약 6,500〜14,500엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 6.5만원〜14.5만원)</span></strong></div>',
    'saitozaki':  '약 5,500〜15,000엔 <span style="color:#1a3a8f;font-size:0.78rem;">(약 5.5만원〜15만원)</span></strong></div>',
}


def af_row_ja(price):
    return f'    <div class="discount-row"><span>🌤️ 午後スルー（平日）</span><strong>{price}</strong></div>'

def af_row_en(price):
    return f'    <div class="discount-row"><span>🌤️ Afternoon Through (Weekday)</span><strong>{price}</strong></div>'

def af_row_ko(price, krw):
    return f'    <div class="discount-row"><span>🌤️ 오후 스루 (평일)</span><strong>{price} <span style="color:#1a3a8f;font-size:0.78rem;">({krw})</span></strong></div>'


def process(key):
    path = os.path.join(BASE, f'course-{key}.html')
    with open(path, encoding='utf-8') as f:
        html = f.read()

    if MARK in html:
        print(f'  {key}: 既に適用済み — スキップ')
        return

    d = DATA[key]
    ok_ja = ok_en = ok_ko = False

    # --- JA ---
    anchor = WE_ROWS_JA[key]
    if anchor in html:
        html = html.replace(anchor, anchor + '\n' + af_row_ja(d['ja']), 1)
        ok_ja = True
    else:
        print(f'  WARNING [{key}] JA anchor not found')

    # --- EN ---
    anchor = WE_ROWS_EN[key]
    if anchor in html:
        html = html.replace(anchor, anchor + '\n' + af_row_en(d['en']), 1)
        ok_en = True
    else:
        print(f'  WARNING [{key}] EN anchor not found')

    # --- KO ---
    # KO anchor は 토·일 行の末尾部分（ユニーク）
    anchor = WE_ROWS_KO[key]
    if anchor in html:
        ko_af = af_row_ko(d['ko'], d['krw'])
        html = html.replace(anchor, anchor + '\n' + ko_af, 1)
        ok_ko = True
    else:
        print(f'  WARNING [{key}] KO anchor not found')

    if ok_ja or ok_en or ok_ko:
        # idempotency mark を </head> 直前に追加
        html = html.replace('</head>', MARK + '\n</head>', 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        status = f"JA={'✓' if ok_ja else '✗'} EN={'✓' if ok_en else '✗'} KO={'✓' if ok_ko else '✗'}"
        print(f'  {key}: 午後スルー料金行追加 ({status})')


def main():
    print('=== 午後スルー料金行 追加スクリプト ===')
    for key in DATA:
        process(key)
    print('=== 完了 ===')


if __name__ == '__main__':
    main()
