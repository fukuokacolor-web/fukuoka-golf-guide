# -*- coding: utf-8 -*-
"""fukuokacc の alternative_cta を再設計 (教授:選択設計 + CVR:楽天直リンク B案)。
§9.4趣旨遵守: 各楽天ボタンは"予約可の別コース名"を明示し、fukuocc自身を予約可と誤認させない。
両ROOT書き込み。--dry-run 対応。冪等(既に新ブロックなら no-op)。"""
import re, os, sys
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
DRY = "--dry-run" in sys.argv
REPO = ROOTS[0]

def rak(slug):
    h = open(os.path.join(REPO, f"course-{slug}.html"), encoding="utf-8").read()
    return re.search(r'href="(https://rpx\.a8\.net/svt/ejp\?a8mat=4B1D5J\+4P34KY[^"]*)"', h).group(1)

SAITO, HISA, KOGA = rak("saitozaki"), rak("hisayama"), rak("koga")

NEW = '''  <!-- 予約できる近隣コース (会員制福岡カンツリーの代替誘導・alternative_cta B:楽天直リンク併記) -->
  <div style="max-width:1100px;margin:0 auto;padding:28px 24px 0;">
    <div style="background:#f4f1ea;border:1px solid #e3ddcf;border-left:5px solid #1a5c38;border-radius:14px;padding:22px 24px;">
      <div style="font-weight:700;font-size:16px;color:#1a5c38;margin-bottom:6px;">⛳ 福岡市東区・近郊で「今すぐ予約できる」人気コース</div>
      <div style="font-size:13px;color:#5a5a5a;line-height:1.8;margin-bottom:16px;">福岡カンツリー倶楽部はメンバー同伴・紹介制のため一般予約はできません。同じ<strong>福岡市東区・近郊</strong>で今すぐ予約できるなら、まずは最寄りの<strong>西戸崎GC（同・東区）</strong>がおすすめ。以下の楽天GORAボタンは<strong>各コース（西戸崎・久山・古賀）</strong>の予約ページに移動します。</div>
      <div style="background:#fff;border:1px solid #e3ddcf;border-radius:12px;padding:16px 18px;margin-bottom:12px;">
        <div style="font-weight:700;color:#1a5c38;font-size:15px;margin-bottom:2px;">西戸崎シーサイドカントリークラブ <span style="font-size:12px;color:#e8744c;font-weight:700;">◎ 最寄り・同じ福岡市東区</span></div>
        <div style="font-size:12px;color:#777;margin-bottom:10px;">海沿いの人気コース／海の中道・福岡市東区</div>
        <div style="display:flex;flex-wrap:wrap;gap:8px;">
          <a href="__SAITO__" target="_blank" rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','alternative_cta_direct')" style="flex:1;min-width:200px;text-align:center;background:linear-gradient(135deg,#BF0000,#8B0000);color:#fff;font-weight:700;font-size:13px;padding:11px 16px;border-radius:9px;text-decoration:none;">🏌️ 西戸崎GCを楽天GORAで予約 →</a>
          <a href="course-saitozaki.html" onclick="if(window.gtag)gtag('event','internal_nav_click',{page:'course-fukuokacc',lang:'ja',nav_section:'alternative_cta',target_page:'course-saitozaki'})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:13px;padding:11px 16px;border-radius:9px;text-decoration:none;border:1px solid #e3ddcf;">コース詳細 →</a>
        </div>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;">
        <div style="background:#fff;border:1px solid #e3ddcf;border-radius:10px;padding:12px 14px;">
          <div style="font-weight:700;color:#1a5c38;font-size:13.5px;margin-bottom:8px;">久山CC <span style="font-weight:400;color:#777;">／空港25分</span></div>
          <div style="display:flex;gap:6px;">
            <a href="__HISA__" target="_blank" rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','alternative_cta_direct')" style="flex:1;text-align:center;background:#BF0000;color:#fff;font-weight:700;font-size:12px;padding:9px 10px;border-radius:8px;text-decoration:none;">🏌️ 久山CCを楽天GORAで →</a>
            <a href="course-hisayama.html" onclick="if(window.gtag)gtag('event','internal_nav_click',{page:'course-fukuokacc',lang:'ja',nav_section:'alternative_cta',target_page:'course-hisayama'})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:12px;padding:9px 12px;border-radius:8px;text-decoration:none;border:1px solid #e3ddcf;">詳細</a>
          </div>
        </div>
        <div style="background:#fff;border:1px solid #e3ddcf;border-radius:10px;padding:12px 14px;">
          <div style="font-weight:700;color:#1a5c38;font-size:13.5px;margin-bottom:8px;">古賀GC <span style="font-weight:400;color:#777;">／福岡市近郊</span></div>
          <div style="display:flex;gap:6px;">
            <a href="__KOGA__" target="_blank" rel="nofollow sponsored noopener" onclick="if(window.trackAffiliate)trackAffiliate('rakuten',document.title,'ja','alternative_cta_direct')" style="flex:1;text-align:center;background:#BF0000;color:#fff;font-weight:700;font-size:12px;padding:9px 10px;border-radius:8px;text-decoration:none;">🏌️ 古賀GCを楽天GORAで →</a>
            <a href="course-koga.html" onclick="if(window.gtag)gtag('event','internal_nav_click',{page:'course-fukuokacc',lang:'ja',nav_section:'alternative_cta',target_page:'course-koga'})" style="text-align:center;background:#f4f1ea;color:#1a5c38;font-weight:700;font-size:12px;padding:9px 12px;border-radius:8px;text-decoration:none;border:1px solid #e3ddcf;">詳細</a>
          </div>
        </div>
      </div>
    </div>
  </div>
'''.replace("__SAITO__", SAITO).replace("__HISA__", HISA).replace("__KOGA__", KOGA)

OLD_RE = re.compile(r'  <!-- 予約できる近隣コース.*?\n  </div>\n', re.S)

src = open(os.path.join(REPO, "course-fukuokacc.html"), encoding="utf-8").read()
if "alternative_cta_direct" in src:
    print("既に新ブロック適用済 = no-op"); sys.exit()
m = OLD_RE.search(src)
if not m:
    print("!! 旧ブロック未検出 — 中止"); sys.exit(1)
print(f"旧ブロック {len(m.group(0))}字 → 新ブロック {len(NEW)}字 に置換")
print(f"楽天リンク: 西戸崎 c_id=", re.search(r'c_id%252F(\d+)', SAITO).group(1),
      "/ 久山=", re.search(r'c_id%252F(\d+)', HISA).group(1),
      "/ 古賀=", re.search(r'c_id%252F(\d+)', KOGA).group(1))
if DRY:
    print("※ DRY-RUN"); sys.exit()
new = src[:m.start()] + NEW + src[m.end():]
for root in ROOTS:
    p = os.path.join(root, "course-fukuokacc.html")
    if os.path.exists(p):
        open(p, "w", encoding="utf-8").write(new)
print("書き込み完了 (両ROOT)")
