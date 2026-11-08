#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースの電話番号・住所の誤りを、公式サイトとじゃらんで確認した値に直す (2026-11-07 点検)。
読みを推測しないよう、英語・韓国語欄の住所も日本語表記で載せる。
道順の本文はここでは直さない (別工程)。course_data.json は触らない。
冪等: 置換対象が無ければ 0 件。改行コードはそのまま保つ。
Usage:
  python scripts/fix_contact_facts_2026_11.py            # dry-run (全置換を表示)
  python scripts/fix_contact_facts_2026_11.py --apply    # REPO + PREVIEW
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv


def S(a, b):
    return (re.escape(a), b)


# (正規表現, 置換後) を上から順に適用する
AD = {
    "asoiizuka": "〒820-0609 福岡県嘉穂郡桂川町吉隈120",
    "century": "〒838-0027 福岡県朝倉市板屋1-1",
    "chikushigaoka": "〒811-1241 福岡県那珂川市後野571",
    "ito": "〒819-1147 福岡県糸島市香力474",
    "nijo": "〒819-1641 福岡県糸島市二丈吉井3362",
    "hisayama": "〒811-2501 福岡県糟屋郡久山町大字久原3549",
    "fukuokacc": "〒811-0216 福岡県福岡市東区大字上和白1318-1",
    "kyushugc": "〒805-0036 福岡県北九州市八幡東区大字小熊野1467",
    "kitakyushu": "〒820-1112 福岡県飯塚市鹿毛馬412-6",
}
PLAN = {
    "course-asoiizuka.html": [S("0948-22-3311", "0948-65-1155"), S('"streetAddress":"伊岐須1112","addressLocality":"飯塚市"', '"streetAddress":"吉隈120","addressLocality":"嘉穂郡桂川町"'), S("飯塚市 伊岐須1112", "嘉穂郡桂川町 吉隈120"), S("飯塚市", "嘉穂郡桂川町")],
    "access-asoiizuka.html": [S("0948-22-3311", "0948-65-1155"), S("〒820-0066 飯塚市伊岐須1112", "〒820-0609 嘉穂郡桂川町吉隈120"), (r"〒820-0066[\s\u3000]*福岡県飯塚市伊岐須1112", AD["asoiizuka"]), S("1112 Ikisu, Iizuka City, Fukuoka 820-0066", AD["asoiizuka"]), (r"〒820-0066[\s\u3000]*후쿠오카현 이이즈카시 이키스 1112", AD["asoiizuka"])],
    "course-century.html": [S("092-938-3031", "0946-24-1111"), S('"streetAddress": "朝倉市"', '"streetAddress": "朝倉市板屋1-1"'), S('<div class="contact-value">Asakura City, Fukuoka</div>', f'<div class="contact-value">{AD["century"]}</div>'), S('<div class="contact-value">후쿠오카현 아사쿠라시</div>', f'<div class="contact-value">{AD["century"]}</div>')],
    "access-century.html": [S("092-938-3031", "0946-24-1111"), S("〒811-2116 糟屋郡粕屋町", "〒838-0027 朝倉市板屋1-1"), (r"〒811-2116[\s\u3000]*福岡県糟屋郡粕屋町", AD["century"]), S("Kasuya-machi, Kasuya-gun, Fukuoka 811-2116", AD["century"]), (r"〒811-2116[\s\u3000]*후쿠오카현 카스야군 카스야마치", AD["century"])],
    "course-chikushigaoka.html": [S("092-952-2711", "092-952-6011"), S('"streetAddress":"五ケ山"', '"streetAddress":"後野571"'), S("那珂川市 五ケ山", "那珂川市 後野571")],
    "access-chikushigaoka.html": [S("092-952-2711", "092-952-6011"), (r"〒811-1245[\s\u3000]*福岡県那珂川市五ケ山", AD["chikushigaoka"]), (r"[^\s>][^>\n]*Gogayama, Nakagawa City, Fukuoka 811-1245", AD["chikushigaoka"]), (r"〒811-1245[\s\u3000]*후쿠오카현 나카가와시 고카야마", AD["chikushigaoka"]), S("那珂川市五ケ山", "那珂川市後野"), S("나카가와시 고카야마 방면", "那珂川市後野 방면"), S("고카야마 방면", "那珂川市後野 방면")],
    "course-ito.html": [S("092-325-0001", "092-322-5031"), S("二丈深江2243", "香力474")],
    "access-ito.html": [S("092-325-0001", "092-322-5031"), S("〒819-1651 糸島市二丈深江2243", "〒819-1147 糸島市香力474"), (r"〒819-1651[\s\u3000]*福岡県糸島市二丈深江2243", AD["ito"]), (r"〒819-1651[\s\u3000]*2243 Nijo Fukae, Itoshima City, Fukuoka", AD["ito"]), (r"〒819-1651[\s\u3000]*후쿠오카현 이토시마시 니조후카에 2243", AD["ito"])],
    "course-nijo.html": [S("092-326-2222", "092-326-5561"), S('"streetAddress":"二丈福井"', '"streetAddress":"二丈吉井3362"'), S("糸島市 二丈福井", "糸島市 二丈吉井3362")],
    "access-nijo.html": [S("092-326-2222", "092-326-5561"), (r"〒819-1635[\s\u3000]*福岡県糸島市二丈福井", AD["nijo"]), S("Nijo Fukui, Itoshima City, Fukuoka 819-1635", AD["nijo"]), (r"〒819-1635[\s\u3000]*후쿠오카현 이토시마시 니조 후쿠이", AD["nijo"]), S("糸島市二丈福井", "糸島市二丈吉井"), S("二丈福井", "二丈吉井"), S("toward Nijo Fukui", "toward Nijo-Yoshii (二丈吉井)"), S("니조 후쿠이 방면", "二丈吉井 방면")],
    "course-hisayama.html": [S("092-976-0001", "0570-0570-52"), S("大字久原2347", "大字久原3549")],
    "access-hisayama.html": [S("092-976-0001", "0570-0570-52"), S("〒811-2502 糟屋郡久山町大字久原2347", "〒811-2501 糟屋郡久山町大字久原3549"), (r"〒811-2502[\s\u3000]*福岡県糟屋郡久山町大字久原2347", AD["hisayama"]), (r"〒811-2502[\s\u3000]*2347 Ohaza Hisahara[^<\n]*", AD["hisayama"]), (r"〒811-2502[\s\u3000]*후쿠오카현 가스야군 히사야마초 오아자 히사하라 2347", AD["hisayama"])],
    "course-fukuokacc.html": [S("092-606-5600", "092-606-2931"), S('"streetAddress":"和白丘2丁目"', '"streetAddress":"大字上和白1318-1"'), S("福岡市東区 和白丘2丁目", "福岡市東区 大字上和白1318-1"), S("福岡市東区和白丘の老舗", "福岡市東区上和白の老舗")],
    "access-fukuokacc.html": [S("092-606-5600", "092-606-2931"), S("〒811-0201 福岡市東区和白丘2丁目", "〒811-0216 福岡市東区大字上和白1318-1"), (r"〒811-0201[\s\u3000]*福岡県福岡市東区和白丘2丁目", AD["fukuokacc"]), (r"[^\s>][^>\n]*Wajiroka, Higashi-ku, Fukuoka City 811-0201", AD["fukuokacc"]), (r"〒811-0201[\s\u3000]*후쿠오카현 후쿠오카시 히가시구 와지로카 2丁目", AD["fukuokacc"]), S("和白丘方面", "上和白方面"), S("와지로카 방면", "上和白 방면")],
    "course-kyushugc.html": [S("093-691-0461", "093-652-2221"), S('"streetAddress":"石坂2丁目","addressLocality":"北九州市八幡西区"', '"streetAddress":"大字小熊野1467","addressLocality":"北九州市八幡東区"'), S("北九州市八幡西区 石坂2丁目", "北九州市八幡東区 大字小熊野1467"), S("北九州市八幡西区", "北九州市八幡東区")],
    "access-kyushugc.html": [S("093-691-0461", "093-652-2221"), S("〒806-0046 北九州市八幡西区石坂2丁目", "〒805-0036 北九州市八幡東区大字小熊野1467"), (r"〒806-0046[\s\u3000]*福岡県北九州市八幡西区石坂2丁目", AD["kyushugc"]), (r"〒806-0046[\s\u3000]*2-chome Ishizaka, Yahata-nishi Ward, Kitakyushu City, Fukuoka", AD["kyushugc"]), (r"〒806-0046[\s\u3000]*후쿠오카현 기타큐슈시 야하타니시구 이시자카 2초메", AD["kyushugc"])],
    "course-kitakyushu.html": [S("093-741-3211", "0948-92-2341"), S('"streetAddress":"大字蜑住","addressLocality":"北九州市若松区"', '"streetAddress":"鹿毛馬412-6","addressLocality":"飯塚市"'), (r"北九州市若松区\s*大字蜑住", "飯塚市 鹿毛馬412-6")],
    "access-kitakyushu.html": [S("093-741-3211", "0948-92-2341"), S("〒808-0135 北九州市若松区大字蜑住", "〒820-1112 飯塚市鹿毛馬412-6"), (r"〒808-0135[\s\u3000]*福岡県北九州市若松区大字蜑住", AD["kitakyushu"]), (r"[^\s>][^>\n]*808-0135", AD["kitakyushu"]), (r"〒808-0135[\s\u3000]*후쿠오카현 기타큐슈시 와카마츠구 오아자에스미", AD["kitakyushu"])],
    "access-queenshill.html": [S("819-1107", "819-1133")],
    "area-fukuokacity.html": [S("Nakagawa City · Gokayama · Mountain", "Nakagawa City · Mountain"), S("那珂川市五ケ山", "那珂川市後野"), S("in Gokayama (Nakagawa City)", "in Nakagawa City"), S("나카가와시 고카야마", "나카가와시"), S("東区和白丘に", "東区上和白に"), S("Higashi-ku · Wajirogaoka · Heritage", "Higashi-ku · Heritage"), S("in Wajirogaoka (Higashi-ku)", "in Higashi-ku")],
    "area-itoshima.html": [S("Itoshima · Nijo-Fukae", "Itoshima"), S('<span class="course-chip">二丈深江</span>', '<span class="course-chip">香力</span>'), S("糸島市二丈深江に", "糸島市香力に"), S('<span class="course-chip">Nijo-Fukae</span>', '<span class="course-chip">Itoshima</span>'), S("in Nijo-Fukae known", "in Itoshima known"), S('<span class="course-chip">니조후카에</span>', '<span class="course-chip">이토시마시</span>'), S("이토시마시 니조후카에의", "이토시마시의"), S("Itoshima · Nijo-Fukui · Value", "Itoshima · Nijo · Value"), S("糸島市二丈福井", "糸島市二丈吉井"), S("in Nijo-Fukui overlooking", "in Nijo overlooking"), S("이토시마시 니조후쿠이의", "이토시마시 니조의")],
    "area-kitakyushu.html": [S("Kitakyushu · Yahata-nishi-ku · Heritage", "Kitakyushu · Yahata-higashi-ku · Heritage")],
    "access.html": [(r"(九州ゴルフ倶楽部 八幡コース(?:(?!</a>).){0,120}?)北九州市八幡西区", r"\g<1>北九州市八幡東区"), (r"(麻生飯塚ゴルフ倶楽部(?:(?!</a>).){0,120}?)飯塚市", r"\g<1>嘉穂郡桂川町")],
    "area-chikuho.html": [(r"(麻生飯塚ゴルフ倶楽部(?:(?!</a>).){0,200}?)飯塚市", r"\g<1>嘉穂郡桂川町")],
    "book-fukuoka-cheap.html": [(r"(麻生飯塚ゴルフ倶楽部(?:(?!</td>).){0,60}?(?:</a>)?\s*(?:<[^>]+>\s*){0,4})飯塚市", r"\g<1>嘉穂郡桂川町")],
    "book-fukuoka-onsen.html": [S("麻生飯塚ゴルフ倶楽部</", "麻生飯塚ゴルフ倶楽部</"), (r"飯塚市( ／ 27H ／ 1969年開場)", r"嘉穂郡桂川町\g<1>")],
    "seasonal.html": [S("📍 Iizuka City (higher elevation)", "📍 Keisen Town, Kaho-gun (higher elevation)")],
    "sitemap-guide.html": [(r"(麻生飯塚ゴルフ倶楽部(?:(?!</a>).){0,80}?)飯塚市", r"\g<1>嘉穂郡桂川町"), S("センチュリー三木ゴルフ倶楽部", "福岡センチュリーゴルフ倶楽部"), (r"(福岡センチュリーゴルフ倶楽部(?:(?!</a>).){0,80}?)糟屋郡", r"\g<1>朝倉市"), S("Century Miki GC", "Fukuoka Century GC"), (r"(Fukuoka Century GC(?:(?!</a>).){0,80}?)Kasuya", r"\g<1>Asakura")],
}
tot = 0
for root in ROOTS:
    show = root == ROOTS[0]
    print(root)
    for name, rules in PLAN.items():
        p = os.path.join(root, name)
        s = open(p, encoding="utf-8", newline="").read()
        new = s
        for pat, rep in rules:
            hits = list(re.finditer(pat, new, re.S))
            if not hits:
                continue
            ex = hits[0]
            after = ex.expand(rep) if "\\g<" in rep else rep
            new = re.sub(pat, (lambda m, r=rep: m.expand(r)) if "\\g<" in rep else (lambda m, r=rep: r), new, flags=re.S)
            tot += len(hits)
            if show and ex.group(0) != after:
                print(f"  {name:28} {len(hits)}x {re.sub(chr(10)+'|'+chr(13), ' ', ex.group(0))[-48:]} → {after[-44:]}")
        assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', new, re.S):
            json.loads(m.group(1))
        if APPLY and new != s:
            open(p, "w", encoding="utf-8", newline="").write(new)
print("件数", tot, "APPLIED" if APPLY else "DRY-RUN")
