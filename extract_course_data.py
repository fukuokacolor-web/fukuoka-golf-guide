#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
既存の course-*.html から v2 生成に必要なデータを抽出して JSON に保存。
"""
import sys, io, os, re, json
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = Path(r'C:/Users/Owner/fukuoka-golf-guide')
OUT = BASE / 'course_data.json'

def extract_one(path: Path):
    html = path.read_text(encoding='utf-8')
    slug = path.stem.replace('course-', '')  # e.g. "century"
    data = {'slug': slug, 'file': path.name}

    # --- Title (JA course name) ---
    m = re.search(r'<header class="page-header">\s*<h1>[^<]*?([^⛳\s][^<]*?)</h1>', html)
    if m:
        data['name_ja'] = m.group(1).strip().lstrip('⛳ ').strip()

    # --- EN/KO name from <header><p> ---
    m = re.search(r'<header class="page-header">.*?<p>(.*?)</p>', html, re.S)
    if m:
        pp = m.group(1).replace('<br>', '|').replace('<br/>', '|').replace('<br />', '|')
        pp = re.sub(r'<[^>]+>', '', pp)
        parts = [x.strip() for x in pp.split('|') if x.strip()]
        if len(parts) >= 1: data['name_en'] = parts[0]
        if len(parts) >= 2: data['name_ko'] = parts[1]

    # --- Title tag for city/area extraction ---
    m = re.search(r'<title>([^<]+)</title>', html)
    if m:
        title = m.group(1)
        data['title_full'] = title
        am = re.search(r'（([^）]+)）', title)
        if am:
            data['area_ja'] = am.group(1)

    # --- Schema.org JSON-LD (address, phone, description) ---
    m = re.search(r'"@type":\s*"GolfCourse".*?\}\s*</script>', html, re.S)
    if m:
        block = m.group(0)
        tm = re.search(r'"telephone":\s*"([^"]+)"', block)
        if tm: data['phone'] = tm.group(1)
        sm = re.search(r'"streetAddress":\s*"([^"]+)"', block)
        if sm: data['street'] = sm.group(1)
        lm = re.search(r'"addressLocality":\s*"([^"]+)"', block)
        if lm: data['locality'] = lm.group(1)
        rm = re.search(r'"addressRegion":\s*"([^"]+)"', block)
        if rm: data['region'] = rm.group(1)

    # --- Meta description (airport time) ---
    m = re.search(r'<meta name="description" content="([^"]+)"', html)
    if m:
        desc = m.group(1)
        data['desc_ja'] = desc
        tm = re.search(r'約([0-9〜～\-]+)分', desc)
        if tm: data['airport_min'] = tm.group(1).replace('～', '〜')

    # --- Hero image (src can come before or after class) ---
    m = re.search(r'<img\s+src="([^"]+)"[^>]*class="course-hero"', html)
    if not m:
        m = re.search(r'<img[^>]*class="course-hero"[^>]*\bsrc="([^"]+)"', html)
    if m:
        data['hero_img'] = m.group(1)

    # --- Holes (from first fact-item labeled ホール数) ---
    m = re.search(r'ホール数</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['holes'] = m.group(1).strip()

    # --- Course type ---
    m = re.search(r'コース特徴</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['course_type_ja'] = m.group(1).strip()
    m = re.search(r'Course Type</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['course_type_en'] = m.group(1).strip()
    m = re.search(r'코스 특징</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['course_type_ko'] = m.group(1).strip()

    # --- Location ---
    m = re.search(r'ロケーション</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['location_ja'] = m.group(1).strip()

    # --- Official website URL (skip a8.net affiliate links) ---
    candidates = re.findall(r'<a href="(https?://[^"]*)"[^>]*class="official-btn"', html)
    for c in candidates:
        if 'a8.net' not in c and 'rakuten' not in c.lower() and 'jalan' not in c.lower():
            data['website'] = c
            break
    if 'website' not in data:
        m = re.search(r'公式サイト</strong><br>(https?://\S+?)(?:</div>|\s*<|\s*↗)', html)
        if m and 'a8.net' not in m.group(1):
            data['website'] = m.group(1).strip()

    # --- Airport time from fact-item "From Fukuoka Airport" ---
    m = re.search(r'福岡空港から</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['airport_val_ja'] = m.group(1).strip()
    m = re.search(r'From Fukuoka Airport</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['airport_val_en'] = m.group(1).strip()
    m = re.search(r'후쿠오카공항에서</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m:
        data['airport_val_ko'] = m.group(1).strip()

    # --- Nearest IC ---
    m = re.search(r'最寄りIC</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m: data['ic_ja'] = m.group(1).strip()
    m = re.search(r'Nearest IC</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m: data['ic_en'] = m.group(1).strip()
    m = re.search(r'최근 IC</span>\s*<span class="f-val">([^<]+)</span>', html)
    if m: data['ic_ko'] = m.group(1).strip()

    # --- Fees (discount-row in JA content) ---
    ja_match = re.search(r'<div id="c-ja".*?(?=<div id="c-en")', html, re.S)
    if ja_match:
        ja_block = ja_match.group(0)
        fees_ja = re.findall(r'<div class="discount-row"><span>([^<]+)</span><strong>([^<]+)</strong>', ja_block)
        data['fees_ja'] = [(k.strip(), v.strip()) for k, v in fees_ja]

    en_match = re.search(r'<div id="c-en".*?(?=<div id="c-ko")', html, re.S)
    if en_match:
        en_block = en_match.group(0)
        fees_en = re.findall(r'<div class="discount-row"><span>([^<]+)</span><strong>([^<]+)</strong>', en_block)
        data['fees_en'] = [(k.strip(), v.strip()) for k, v in fees_en]

    ko_match = re.search(r'<div id="c-ko".*?(?=</body>|<footer>|<div style="max-width)', html, re.S)
    if ko_match:
        ko_block = ko_match.group(0)
        # KO may have nested span for KRW — capture whole strong content
        fees_ko = re.findall(r'<div class="discount-row"><span>([^<]+)</span><strong>(.*?)</strong>', ko_block)
        data['fees_ko'] = [(k.strip(), re.sub(r'\s+', ' ', v).strip()) for k, v in fees_ko]

    # --- Related courses (from related section) ---
    related = re.findall(r'<a href="(course-[^"]+\.html)"[^>]*>([^<]+)</a>', html)
    # Filter out self
    related = [(h, t) for h, t in related if h != path.name]
    # First few unique
    seen = set()
    data['related'] = []
    for h, t in related:
        if h not in seen:
            seen.add(h)
            data['related'].append({'href': h, 'label': t.strip()})
        if len(data['related']) >= 3:
            break

    # --- KO airport badge subtitle ---
    m = re.search(r'airport-badge-sub">([^<]+)</div>', html)
    if m: data['airport_sub_ko'] = m.group(1).strip()

    # --- Affiliate URLs (jalan, rakuten) ---
    jm = re.search(r'(https://px\.a8\.net/svt/ejp\?a8mat=4B1D5J\+5JG8FM[^"\s]+)', html)
    if jm:
        data['jalan_url'] = jm.group(1).replace('&amp;', '&')
    rm = re.search(r'(https://rpx\.a8\.net/svt/ejp\?a8mat=4B1D5J\+4P34KY[^"\s]+)', html)
    if rm:
        data['rakuten_url'] = rm.group(1).replace('&amp;', '&')

    return data

def main():
    files = sorted([p for p in BASE.glob('course-*.html') if '-v2' not in p.name])
    print(f'=== 抽出対象: {len(files)}ファイル ===')
    all_data = []
    for f in files:
        try:
            d = extract_one(f)
            all_data.append(d)
            print(f'  OK  {f.name:30s}  {d.get("name_ja", "?"):30s}  holes={d.get("holes","?")}  {d.get("airport_min","?")}min')
        except Exception as e:
            print(f'  FAIL  {f.name}: {e}')

    OUT.write_text(json.dumps(all_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n=== 書き出し: {OUT} ({len(all_data)}件) ===')

if __name__ == '__main__':
    main()
