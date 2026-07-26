# -*- coding: utf-8 -*-
"""会員制course(wakamatsu/genkai)の alternative_cta を fukuocc と同型に再設計。
教授:選択設計(最寄り主役・獲得フレーム) + CVR:楽天GORA直リンク併記(alternative_cta_direct計測)。
§9.4趣旨遵守: 楽天リンクは全て"予約可の別コース"で各ボタンにコース名明示。会員制自身の楽天CTAは無し。
両ROOT・--dry-run・冪等(alternative_cta_direct 済なら no-op)。"""
import re, os, sys
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
REPO = ROOTS[0]
DRY = "--dry-run" in sys.argv

def rak(slug):
    h = open(os.path.join(REPO, f"course-{slug}.html"), encoding="utf-8").read()
    return re.search(r'href="(https://rpx\.a8\.net/svt/ejp\?a8mat=4B1D5J\+4P34KY[^"]*)"', h).group(1)

CFG = {
  "course-wakamatsu": {
    "area": "北九州エリア",
    "members": "若松ゴルフ倶楽部はメンバー同伴・紹介が必要です。",
    "primary": {"slug":"kitakyushu","name":"北九州カントリー倶楽部","short":"北九州CC","tag":"◎ 同じ北九州エリア","desc":"PGM運営の人気コース／北九州市"},
    "sec": [{"slug":"kokura","short":"小倉CC","note":"ビジター枠あり"},
            {"slug":"kyushugc","short":"九州GC八幡","note":"若松の隣・八幡"}],
    "mode": "replace",
  },
  "course-genkai": {
    "area": "宗像・福岡市近郊",
    "members": "玄海ゴルフクラブはメンバー本人完全予約制（紹介・同伴が推奨）です。",
    "primary": {"slug":"fukuokakokusai","name":"福岡国際カントリークラブ","short":"福岡国際CC","tag":"◎ 宗像・近郊で予約可","desc":"36ホールの本格コース／宗像"},
    "sec": [{"slug":"koga","short":"古賀GC","note":"福岡市近郊"},
            {"slug":"keya","short":"芥屋GC","note":"糸島の名門"}],
    "mode": "insert_before",
    "anchor": '    <div class="sec-eyebrow">— Green Fees</div>',
  },
}

SEC_TPL = '''        <div style="background:#fff;border:1px solid #e3ddcf;border-radius:10px;padding:12px 14px;">
          <div style="font-weight:700;color:#1a5c38;font-size:13.5px;margin-bottom:8px;">__SHORT__ <span style="font-weight:400;color:#777;">／__NOTE__</span></div>
          <div style="display:flex;gap:6px;">
            <a href="__RAK__" target="_blank" rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','alternative_cta_direct')" style="flex:1;text-align:center;background:#BF0000;color:#fff;font-weight:700;font-size:12px;padding:9px 10px;border-radius:8px;text-decoration:none;">🏌️ __SHORT__を楽天GORAで →</a>
            <a href="course-__SLUG__.html" onclick="if(window.gtag)gtag('event','internal_nav_click',{page:'__PAGE__',lang:'ja',nav_section:'alternative_cta',target_page:'course-__SLUG__'})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:12px;padding:9px 12px;border-radius:8px;text-decoration:none;border:1px solid #e3ddcf;">詳細</a>
          </div>
        </div>'''

def block(page, cfg):
    p = cfg["primary"]
    names = "・".join([p["short"]] + [s["short"] for s in cfg["sec"]])
    secs = "\n".join(
        SEC_TPL.replace("__SHORT__", s["short"]).replace("__NOTE__", s["note"])
               .replace("__RAK__", rak(s["slug"])).replace("__SLUG__", s["slug"]).replace("__PAGE__", page)
        for s in cfg["sec"])
    tpl = '''  <!-- 予約できる近隣コース (会員制の代替誘導・alternative_cta B:楽天直リンク併記) -->
  <div style="max-width:1100px;margin:0 auto;padding:28px 24px 0;">
    <div style="background:#f4f1ea;border:1px solid #e3ddcf;border-left:5px solid #1a5c38;border-radius:14px;padding:22px 24px;">
      <div style="font-weight:700;font-size:16px;color:#1a5c38;margin-bottom:6px;">⛳ __AREA__で「今すぐ予約できる」人気コース</div>
      <div style="font-size:13px;color:#5a5a5a;line-height:1.8;margin-bottom:16px;">__MEMBERS__今すぐ予約できるなら、まずは<strong>__PSHORT__</strong>がおすすめ。以下の楽天GORAボタンは<strong>各コース（__NAMES__）</strong>の予約ページに移動します。</div>
      <div style="background:#fff;border:1px solid #e3ddcf;border-radius:12px;padding:16px 18px;margin-bottom:12px;">
        <div style="font-weight:700;color:#1a5c38;font-size:15px;margin-bottom:2px;">__PNAME__ <span style="font-size:12px;color:#e8744c;font-weight:700;">__PTAG__</span></div>
        <div style="font-size:12px;color:#777;margin-bottom:10px;">__PDESC__</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          <a href="__PRAK__" target="_blank" rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','alternative_cta_direct')" style="flex:1;min-width:200px;text-align:center;background:linear-gradient(135deg,#BF0000,#8B0000);color:#fff;font-weight:700;font-size:13px;padding:11px 16px;border-radius:9px;text-decoration:none;">🏌️ __PSHORT__を楽天GORAで予約 →</a>
          <a href="course-__PSLUG__.html" onclick="if(window.gtag)gtag('event','internal_nav_click',{page:'__PAGE__',lang:'ja',nav_section:'alternative_cta',target_page:'course-__PSLUG__'})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:13px;padding:11px 16px;border-radius:9px;text-decoration:none;border:1px solid #e3ddcf;">コース詳細 →</a>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
__SECS__
      </div>
    </div>
  </div>
'''
    return (tpl.replace("__AREA__", cfg["area"]).replace("__MEMBERS__", cfg["members"])
            .replace("__PNAME__", p["name"]).replace("__PSHORT__", p["short"])
            .replace("__PTAG__", p["tag"]).replace("__PDESC__", p["desc"])
            .replace("__PRAK__", rak(p["slug"])).replace("__PSLUG__", p["slug"])
            .replace("__NAMES__", names).replace("__PAGE__", page).replace("__SECS__", secs))

OLD_RE = re.compile(r'  <!-- 予約できる近隣コース.*?\n  </div>\n', re.S)

for page, cfg in CFG.items():
    src = open(os.path.join(REPO, page + ".html"), encoding="utf-8").read()
    if "alternative_cta_direct" in src:
        print(f"  [{page}] 済 = no-op"); continue
    nb = block(page, cfg)
    if cfg["mode"] == "replace":
        m = OLD_RE.search(src)
        if not m: print(f"  [{page}] !! 旧ブロック未検出"); continue
        new = src[:m.start()] + nb + src[m.end():]
        print(f"  [{page}] replace: 旧{len(m.group(0))}→新{len(nb)}字")
    else:
        if cfg["anchor"] not in src: print(f"  [{page}] !! anchor未検出"); continue
        new = src.replace(cfg["anchor"], nb + "\n" + cfg["anchor"], 1)
        print(f"  [{page}] insert: {len(nb)}字 を Green Fees 前に挿入")
    if not DRY:
        for root in ROOTS:
            pth = os.path.join(root, page + ".html")
            if os.path.exists(pth): open(pth, "w", encoding="utf-8").write(new)
print("DRY-RUN" if DRY else "書き込み完了")
