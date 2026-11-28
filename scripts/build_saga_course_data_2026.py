#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
佐賀の個別コースページ用のデータ saga_courses.json を作る (2026-11-28)。読み取り専用で、HTML は作らない。
  入力 (scripts/.cache/saga/ に保存した取得済みページ):
    じゃらん コース情報 golf-jalan.net/gc{id}/info/  → 開場年月日・ラウンドスタイル・練習場
    楽天GORA コースガイド booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{id} → 住所・ホール数・距離・パー・種別・グリーン・高低差・面積・設計者・コースレート・アクセス
  事実確認済み (SAGA_MEIMON_FACTS.md) の項目は "verified" に入れる。
  食い違い: 佐賀CC の開場年 (公式 Since1970 / じゃらん 1971-05-11) → open を None にする。
  電話番号は持たない (佐賀CC でじゃらんと楽天の番号が違ったため)。
Usage: python scripts/build_saga_course_data_2026.py
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
R0 = "C:/Users/Owner/fukuoka-golf-guide"
C = os.path.join(R0, "scripts", ".cache", "saga")

COURSES = [  # slug, 名前, 市町, エリア, じゃらん gc, 楽天 c_id
    ("bridgestone", "ブリヂストンカンツリー倶楽部", "鳥栖市", "tosu", "02366", "410013"),
    ("sagacc", "佐賀カントリー倶楽部", "三養基郡みやき町", "tosu", "02376", "410002"),
    ("hinokuma", "日の隈カンツリークラブ", "神埼市", "tosu", "02373", "410011"),
    ("welcome", "ウェルカムゴルフクラブ", "鳥栖市", "tosu", "21013", "520385"),
    ("sansui", "山水カントリークラブ", "三養基郡みやき町", "tosu", "02375", "6389"),
    ("kitayama", "北山カントリー倶楽部", "佐賀市三瀬村", "yamato", "02374", "410014"),
    ("yamatofudo", "大和不動カントリー倶楽部", "佐賀市大和町", "yamato", "02371", "410015"),
    ("fuji", "フジカントリークラブ", "佐賀市富士町", "yamato", None, "410012"),
    ("karatsu", "唐津ゴルフ倶楽部", "唐津市", "karatsu", "02365", "410001"),
    ("wakagi", "若木ゴルフ倶楽部", "武雄市", "takeo", "02370", "410016"),
    ("classic", "佐賀クラシックゴルフ倶楽部", "多久市", "taku", "02369", "410003"),
]
# フジ: じゃらんに予約カレンダーなし (cal=0) → じゃらんの予約導線なし。じゃらんのコース情報 (gc02372) は開場日の出典として使う
JALAN_INFO_ONLY = {"fuji": "02372"}
VERIFIED = {  # SAGA_MEIMON_FACTS.md (公式・2出典)
    "karatsu": [("開場", "1937年（昭和12年）", "公式サイト", "https://www.resol-golf.jp/karatsu/course/")],
    "bridgestone": [("開場", "1957年（昭和32年）", "公式サイト", "https://bridgestone-cc.com/about/"),
                    ("創設", "ブリヂストン創業者・石橋正二郎", "公式サイト", "https://bridgestone-cc.com/about/"),
                    ("設計", "三好徳行", "公式サイト", "https://bridgestone-cc.com/about/")],
    "sagacc": [("設計", "井上誠一", "公式サイト（当倶楽部の歴史）", "https://www.saga-cc.com/history"),
               ("起工", "1969年（昭和44年）", "公式サイト（当倶楽部の歴史）", "https://www.saga-cc.com/history")],
    "wakagi": [("設計", "デズモンド・ミュアヘッド", "PGM公式サイト", "https://booking.pacificgolf.co.jp/guide/125.html")],
    "classic": [("開場", "1996年", "公式サイト", "https://cm-g.co.jp/saga/history/"),
                ("設計", "中村亨治", "公式サイト", "https://cm-g.co.jp/saga/history/"),
                ("認定", "JLPGA認定コース", "日本女子プロゴルフ協会", "https://www.lpga.or.jp/about/authorized_course/"),
                ("公式競技", "2023年 日本シニアゴルフ選手権", "日本ゴルフ協会 競技規定", "https://www.jga.or.jp/jga/jsp/2023/12-0/regulation.pdf"),
                ("公式競技", "2007年 九州アマチュアゴルフ選手権 決勝・2012年 九州オープン", "公式サイト・GDO", "https://cm-g.co.jp/saga/history/tournament/")],
}
NO_OPEN = {"sagacc"}  # 開場年が出典で食い違う


def jalan(gid):
    t = open(os.path.join(C, f"gc{gid}_info.html"), "rb").read()
    try:
        t = t.decode("utf-8")
    except UnicodeDecodeError:
        t = t.decode("cp932", "ignore")
    pairs = re.findall(r'<div class="title">\s*(.*?)\s*</div>\s*<div class="data">\s*(.*?)\s*</div>', t, re.S)
    clean = lambda v: re.sub(r"\s+", " ", re.sub(r"<br\s*/?>", " / ", re.sub(r"<(?!br)[^>]+>", "", v))).strip()
    return {re.sub(r"<[^>]+>|\s", "", k): clean(v) for k, v in pairs}


def rakuten(cid):
    t = open(os.path.join(C, f"g{cid}.html"), "rb").read().decode("utf-8", "replace")
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", "", t, flags=re.S)))
    g = lambda p: (re.search(p, txt).group(1).strip() if re.search(p, txt) else None)
    acc = re.findall(r"((?:長崎|九州|西九州|大分)自動車道・\S+ \d+km以内|福岡都市高速道路・\S+ \d+km以内)", txt)
    rating = re.search(r"コースレーティング ヤード (\S+) (\S+) ([\d.]+) ([\d,]+)", txt)
    return dict(addr=g(r"住所\s*〒\d{3}-\d{4}\s*佐賀県\s*(\S+)"), holes=g(r"ホール数\s*(\d+)ホール"), yard=g(r"距離\s*([\d,]+)Y"),
                par=g(r"パー\s*(\d+)"), kind=g(r"種別\s*(\S+)"), greens=g(r"グリーン数\s*(\S+)"), green=g(r"グリーン数\s*\S+\s*グリーン\s*(\S+)"),
                slope=g(r"コース高低差\s*(\S+)"), area=g(r"面積\s*([\d,]+)万m"), design=(re.findall(r"コース\s+[^ ]+\s+設計者\s*(.+?)\s*(?:ドラコン推奨|ニアピン推奨|もっと見る|コースレート)", txt) or [None])[-1],
                access=sorted(set(acc)), rating=(dict(tee=rating.group(2), rate=rating.group(3), yard=rating.group(4)) if rating else None))


out = {}
for slug, name, city, area, jid, cid in COURSES:
    rk = rakuten(cid)
    jinfo = jalan(jid or JALAN_INFO_ONLY[slug])
    open_ = None if slug in NO_OPEN else (jinfo.get("開場年月日") or None)
    out[slug] = dict(name=name, city=city, area=area, jalan_id=jid, rakuten_cid=cid, addr=f"佐賀県{rk['addr']}" if rk["addr"] else None,
                     holes=rk["holes"], par=rk["par"], yard=rk["yard"], kind=rk["kind"], greens=rk["greens"], green=rk["green"],
                     slope=rk["slope"], area_m2=rk["area"], design=rk["design"], rating=rk["rating"], access=rk["access"],
                     open=open_, round_style=jinfo.get("ラウンドスタイル") or None, practice=jinfo.get("練習場") or None,
                     verified=[dict(item=a, value=b, source=c, url=d) for a, b, c, d in VERIFIED.get(slug, [])],
                     sources=dict(jalan=f"https://golf-jalan.net/gc{jid or JALAN_INFO_ONLY[slug]}/info/",
                                  rakuten=f"https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{cid}"),
                     checked="2026-11-28")
    o = out[slug]
    print(slug, o["addr"], o["holes"], o["par"], o["yard"], o["kind"], o["green"], o["design"], o["open"], o["access"], o["rating"])
json.dump({"_meta": {"created": "2026-11-28", "note": "佐賀の個別コースページ用。じゃらん・楽天GORAのコース情報と SAGA_MEIMON_FACTS.md から作成。course_data.json とは別管理。"},
           "courses": out}, open(os.path.join(R0, "saga_courses.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote saga_courses.json", len(out))
