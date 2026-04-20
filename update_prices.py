#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
福岡ゴルフガイド 料金表示更新スクリプト
JA・EN・KO各セクションの discount-row 平日・土日行を更新する
"""

import re
import glob
import os

# 調査済み料金データ
PRICE_DATA = {
    "aburayama":    {"wd_lo": 3000,  "wd_hi": 4500,  "we_lo": 3200,  "we_hi": 4500},
    "akane":        {"wd_lo": 3500,  "wd_hi": 15000, "we_lo": 3500,  "we_hi": 21000},
    "ariake":       {"wd_lo": 7000,  "wd_hi": 8500,  "we_lo": 10500, "we_hi": 11500},
    "asoiizuka":    {"wd_lo": 9000,  "wd_hi": 15000, "we_lo": 9500,  "we_hi": 21500},
    "central":      {"wd_lo": 6500,  "wd_hi": 12000, "we_lo": 8000,  "we_hi": 14000},
    "century":      {"wd_lo": 9500,  "wd_hi": 21500, "we_lo": 11500, "we_hi": 21500},
    "chikushigaoka":{"wd_lo": 13900, "wd_hi": 13900, "we_lo": 18400, "we_hi": 18400},
    "chikushino":   {"wd_lo": 9500,  "wd_hi": 17000, "we_lo": 10000, "we_hi": 18000},
    "daihakata":    {"wd_lo": 3500,  "wd_hi": 11500, "we_lo": 8000,  "we_hi": 14500},
    "dazaifu":      {"wd_lo": 11000, "wd_hi": 15500, "we_lo": 14000, "we_hi": 22500},
    "fukuokacc":    {"wd_lo": 5000,  "wd_hi": 12000, "we_lo": 8000,  "we_hi": 15500},
    "hisayama":     {"wd_lo": 3500,  "wd_hi": 12000, "we_lo": 4000,  "we_hi": 15000},
    "ito":          {"wd_lo": 9000,  "wd_hi": 22000, "we_lo": 9000,  "we_hi": 22000},
    "keya":         {"wd_lo": 21500, "wd_hi": 25000, "we_lo": 30500, "we_hi": 34000},
    "kitakyushu":   {"wd_lo": 7000,  "wd_hi": 10500, "we_lo": 11500, "we_hi": 11500},
    "koga":         {"wd_lo": 24800, "wd_hi": 30000, "we_lo": 30100, "we_hi": 36200},
    "kurume":       {"wd_lo": 6000,  "wd_hi": 8500,  "we_lo": 10000, "we_hi": 14500},
    "kyushugc":     {"wd_lo": 15500, "wd_hi": 15500, "we_lo": 15500, "we_hi": 20000},
    "lakeside":     {"wd_lo": 7000,  "wd_hi": 12000, "we_lo": 7000,  "we_hi": 16000},
    "mission":      {"wd_lo": 5000,  "wd_hi": 12000, "we_lo": 8000,  "we_hi": 15000},
    "moji":         {"wd_lo": 6000,  "wd_hi": 28000, "we_lo": 6000,  "we_hi": 33000},
    "moonlake":     {"wd_lo": 6500,  "wd_hi": 9000,  "we_lo": 6500,  "we_hi": 14500},
    "nijo":         {"wd_lo": 4000,  "wd_hi": 13000, "we_lo": 7500,  "we_hi": 16000},
    "ogori":        {"wd_lo": 13500, "wd_hi": 14500, "we_lo": 18000, "we_hi": 19000},
    "queenshill":   {"wd_lo": 21800, "wd_hi": 21800, "we_lo": 30200, "we_hi": 30200},
    "saitozaki":    {"wd_lo": 6000,  "wd_hi": 10000, "we_lo": 5500,  "we_hi": 15000},
    "sevenmillion": {"wd_lo": 9500,  "wd_hi": 15000, "we_lo": 10500, "we_hi": 15000},
    "wakamiya":     {"wd_lo": 8000,  "wd_hi": 15500, "we_lo": 12500, "we_hi": 17000},
}


def fmt_jpy(v):
    """数値を3桁カンマ区切り文字列に"""
    return f"{v:,}"


def krw_convert(yen):
    """
    円をKRWに換算（0.5万원単位で四捨五入）
    1,000円 = 1万원 ベース
    例: 3500 → 3.5万원, 5000 → 5万원, 21800 → 22万원
    """
    man = yen / 1000  # 1만원単位の数値
    # 0.5万원単位に丸め
    rounded = round(man * 2) / 2
    if rounded == int(rounded):
        # 整数
        return f"{int(rounded)}만원"
    else:
        # 小数点あり（.5）
        return f"{rounded}만원"


def make_ja_price(lo, hi):
    """JA形式の価格文字列"""
    if lo == hi:
        return f"<strong>約{fmt_jpy(lo)}円</strong>"
    else:
        return f"<strong>約{fmt_jpy(lo)}〜{fmt_jpy(hi)}円</strong>"


def make_en_price(lo, hi):
    """EN形式の価格文字列"""
    if lo == hi:
        return f"<strong>¥{fmt_jpy(lo)}</strong>"
    else:
        return f"<strong>¥{fmt_jpy(lo)}–¥{fmt_jpy(hi)}</strong>"


def make_ko_price(lo, hi):
    """KO形式の価格文字列（KRW付き）"""
    span_style = 'style="color:#1a3a8f;font-size:0.78rem;"'
    if lo == hi:
        krw = krw_convert(lo)
        return f'<strong>약 {fmt_jpy(lo)}엔 <span {span_style}>(약 {krw})</span></strong>'
    else:
        krw_lo = krw_convert(lo)
        krw_hi = krw_convert(hi)
        return f'<strong>약 {fmt_jpy(lo)}〜{fmt_jpy(hi)}엔 <span {span_style}>(약 {krw_lo}〜{krw_hi})</span></strong>'


def split_sections(html):
    """
    HTMLをJA/EN/KOセクションに分割して返す
    Returns: (before_ja, ja_block, en_block, ko_block, after_ko)
    """
    # セクション区切りコメントのパターン
    ja_start  = r'<!-- ════ 日本語 ════ -->'
    en_start  = r'<!-- ════ English ════ -->'
    ko_start  = r'<!-- ════ 한국어 ════ -->'

    ja_pos = html.find('<!-- ════ 日本語 ════ -->')
    en_pos = html.find('<!-- ════ English ════ -->')
    ko_pos = html.find('<!-- ════ 한국어 ════ -->')

    if ja_pos == -1 or en_pos == -1 or ko_pos == -1:
        return None

    before = html[:ja_pos]
    ja_block = html[ja_pos:en_pos]
    en_block = html[en_pos:ko_pos]
    ko_block = html[ko_pos:]

    return before, ja_block, en_block, ko_block


def replace_weekday_weekend_in_ja(block, wd_lo, wd_hi, we_lo, we_hi):
    """
    JAセクション内の平日・土日discount-rowの<strong>...</strong>を置換
    午後スルー行は変更しない
    """
    # 平日行（午後スルーでない行）
    # パターン: <span>📅 [何か平日テキスト]</span><strong>...</strong>
    # 午後スルー行を除外するため、行ごとに処理

    lines = block.split('\n')
    new_lines = []
    for line in lines:
        # 午後スルー行はスキップ
        if '午後スルー' in line or '오후 스루' in line or 'Afternoon Through' in line:
            new_lines.append(line)
            continue

        # JA 平日行
        if 'discount-row' in line and ('📅' in line) and '<strong>' in line:
            new_price = make_ja_price(wd_lo, wd_hi)
            line = re.sub(r'<strong>.*?</strong>', new_price, line)

        # JA 土日行
        elif 'discount-row' in line and ('🎉' in line) and '<strong>' in line:
            new_price = make_ja_price(we_lo, we_hi)
            line = re.sub(r'<strong>.*?</strong>', new_price, line)

        new_lines.append(line)
    return '\n'.join(new_lines)


def replace_weekday_weekend_in_en(block, wd_lo, wd_hi, we_lo, we_hi):
    """
    ENセクション内の平日・土日discount-rowの<strong>...</strong>を置換
    """
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if 'Afternoon Through' in line:
            new_lines.append(line)
            continue

        if 'discount-row' in line and ('📅' in line) and '<strong>' in line:
            new_price = make_en_price(wd_lo, wd_hi)
            line = re.sub(r'<strong>.*?</strong>', new_price, line)
        elif 'discount-row' in line and ('🎉' in line) and '<strong>' in line:
            new_price = make_en_price(we_lo, we_hi)
            line = re.sub(r'<strong>.*?</strong>', new_price, line)

        new_lines.append(line)
    return '\n'.join(new_lines)


def replace_weekday_weekend_in_ko(block, wd_lo, wd_hi, we_lo, we_hi):
    """
    KOセクション内の平日・土日discount-rowの<strong>...</strong>を置換
    KRW付きのspanタグも含めて書き換える
    """
    lines = block.split('\n')
    new_lines = []
    for line in lines:
        if '오후 스루' in line:
            new_lines.append(line)
            continue

        if 'discount-row' in line and ('📅' in line) and '<strong>' in line:
            new_price = make_ko_price(wd_lo, wd_hi)
            # <strong>...</strong>（内部にspanを含む場合も含めて）全部置換
            line = re.sub(r'<strong>.*?</strong>', new_price, line, flags=re.DOTALL)
        elif 'discount-row' in line and ('🎉' in line) and '<strong>' in line:
            new_price = make_ko_price(we_lo, we_hi)
            line = re.sub(r'<strong>.*?</strong>', new_price, line, flags=re.DOTALL)

        new_lines.append(line)
    return '\n'.join(new_lines)


def process_file(filepath, prices):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    result = split_sections(html)
    if result is None:
        print(f"  [SKIP] セクション区切りが見つかりません: {filepath}")
        return False

    before, ja_block, en_block, ko_block = result

    wd_lo = prices['wd_lo']
    wd_hi = prices['wd_hi']
    we_lo = prices['we_lo']
    we_hi = prices['we_hi']

    new_ja = replace_weekday_weekend_in_ja(ja_block, wd_lo, wd_hi, we_lo, we_hi)
    new_en = replace_weekday_weekend_in_en(en_block, wd_lo, wd_hi, we_lo, we_hi)
    new_ko = replace_weekday_weekend_in_ko(ko_block, wd_lo, wd_hi, we_lo, we_hi)

    new_html = before + new_ja + new_en + new_ko

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return True


def main():
    base_dir = r'C:/Users/Owner/fukuoka-golf-guide'
    files = sorted(glob.glob(os.path.join(base_dir, 'course-*.html')))

    updated = 0
    skipped = 0

    for filepath in files:
        filename = os.path.basename(filepath)
        # course-XXXX.html → XXXX
        key = filename.replace('course-', '').replace('.html', '')

        if key not in PRICE_DATA:
            print(f"  [SKIP] 料金データなし: {filename}")
            skipped += 1
            continue

        prices = PRICE_DATA[key]
        ok = process_file(filepath, prices)
        if ok:
            print(f"  [OK]   {filename}  平日:{prices['wd_lo']:,}〜{prices['wd_hi']:,}  土日:{prices['we_lo']:,}〜{prices['we_hi']:,}")
            updated += 1
        else:
            skipped += 1

    print(f"\n完了: {updated}件更新, {skipped}件スキップ")


if __name__ == '__main__':
    main()
