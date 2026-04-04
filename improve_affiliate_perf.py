import re, glob

JALAN  = "https://px.a8.net/svt/ejp?a8mat=4B1D5J+5JG8FM+36SI+BW8O2&a8ejpredirect=https%3A%2F%2Fgolf.jalan.net%2F"
RAKUTEN = "https://rpx.a8.net/svt/ejp?a8mat=4B1D5J+4P34KY+2HOM+7O29U&rakuten=y&a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F0eb4cf04.fd65a65c.0eb4cf05.fa3f041c%2Fa26040498058_4B1D5J_4P34KY_2HOM_7O29U%3Fpc%3Dhttp%253A%252F%252Fgora.golf.rakuten.co.jp%252F%26m%3Dhttp%253A%252F%252Fwww.rakuten.co.jp%252F"

BTN_STYLE = "display:inline-flex;align-items:center;gap:4px;font-size:0.75rem;font-weight:700;padding:5px 12px;border-radius:20px;text-decoration:none;"
JALAN_STYLE  = BTN_STYLE + "background:#e8f5ee;color:#1a5c38;border:1.5px solid #b8d9c5;"
RAKUTEN_STYLE = BTN_STYLE + "background:#fdecea;color:#c0392b;border:1.5px solid #f5b8b8;"

WRAP_OPEN  = '<div style="display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;">'
WRAP_CLOSE = '</div>'

def book_row(jalan_txt, rakuten_txt):
    return (
        f'{WRAP_OPEN}'
        f'<a href="{JALAN}" style="{JALAN_STYLE}" rel="nofollow" target="_blank">📅 {jalan_txt}</a>'
        f'<a href="{RAKUTEN}" style="{RAKUTEN_STYLE}" rel="nofollow" target="_blank">🏌️ {rakuten_txt}</a>'
        f'{WRAP_CLOSE}'
    )

# ── ① recommend.html: 各カードに予約ボタン追加 ──────────────────────────
with open("recommend.html", encoding="utf-8") as f:
    html = f.read()

# JA
html = re.sub(
    r'(<a href="course-[^"]+\.html" class="rec-link">詳しく見る →</a>)',
    lambda m: m.group(1) + "\n      " + book_row("じゃらんで予約", "楽天GORAで予約"),
    html
)
# EN
html = re.sub(
    r'(<a href="course-[^"]+\.html" class="rec-link">View course →</a>)',
    lambda m: m.group(1) + "\n      " + book_row("Book on Jalan", "Rakuten GORA"),
    html
)
# KO
html = re.sub(
    r'(<a href="course-[^"]+\.html" class="rec-link">자세히 보기 →</a>)',
    lambda m: m.group(1) + "\n      " + book_row("じゃらん 예약", "楽天GORA 예약"),
    html
)

with open("recommend.html", "w", encoding="utf-8") as f:
    f.write(html)
print("✅ recommend.html: 予約ボタン追加完了")

# ── ② beginner-cards.html: 予約バナー追加 ──────────────────────────────
BOOKING_BANNER_JA = """
  <div class="sec-head">📅 福岡のゴルフ場を予約する</div>
  <div class="card theme-green">
    <div class="card-head">
      <span class="big-icon">🏌️</span>
      <div class="title-wrap">
        <div>オンライン予約はこちら</div>
        <div class="en">Book Your Tee Time Online</div>
      </div>
    </div>
    <div class="card-body">
      <p style="font-size:0.82rem;line-height:1.7;margin-bottom:14px;">福岡のゴルフ場は以下の予約サイトから外国語でも簡単に予約できます。空き状況をリアルタイムで確認でき、ネット割引もあります。</p>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <a href="{jalan}" style="display:block;background:#e8f5ee;border:2px solid #b8d9c5;color:#1a5c38;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">📅 じゃらんゴルフで予約する →</a>
        <a href="{rakuten}" style="display:block;background:#fdecea;border:2px solid #f5b8b8;color:#c0392b;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">🏌️ 楽天GORAで予約する →</a>
      </div>
      <div class="info-bar" style="margin-top:12px;"><span class="icon">💡</span>初めての方は「パック料金」でグリーンフィー・カート・食事がまとめてお得になるプランをお試しください。</div>
    </div>
  </div>
""".format(jalan=JALAN, rakuten=RAKUTEN)

BOOKING_BANNER_EN = """
  <div class="sec-head">📅 Book a Golf Course in Fukuoka</div>
  <div class="card theme-green">
    <div class="card-head">
      <span class="big-icon">🏌️</span>
      <div class="title-wrap"><div>Book Your Tee Time Online</div></div>
    </div>
    <div class="card-body">
      <p style="font-size:0.82rem;line-height:1.7;margin-bottom:14px;">Fukuoka's golf courses can be easily booked online. Check real-time availability and score exclusive online discounts.</p>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <a href="{jalan}" style="display:block;background:#e8f5ee;border:2px solid #b8d9c5;color:#1a5c38;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">📅 Book on Jalan Golf →</a>
        <a href="{rakuten}" style="display:block;background:#fdecea;border:2px solid #f5b8b8;color:#c0392b;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">🏌️ Book on Rakuten GORA →</a>
      </div>
      <div class="info-bar" style="margin-top:12px;"><span class="icon">💡</span>Look for "pack" plans that bundle green fees, cart and lunch — great value for first-timers.</div>
    </div>
  </div>
""".format(jalan=JALAN, rakuten=RAKUTEN)

BOOKING_BANNER_KO = """
  <div class="sec-head">📅 후쿠오카 골프장 예약하기</div>
  <div class="card theme-green">
    <div class="card-head">
      <span class="big-icon">🏌️</span>
      <div class="title-wrap">
        <div>온라인 예약은 여기서</div>
        <div class="en">Book Your Tee Time Online</div>
      </div>
    </div>
    <div class="card-body">
      <p style="font-size:0.82rem;line-height:1.7;margin-bottom:14px;">후쿠오카의 골프장은 아래 예약 사이트에서 간편하게 예약할 수 있습니다. 실시간 빈 자리 확인 및 온라인 할인도 이용하세요.</p>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <a href="{jalan}" style="display:block;background:#e8f5ee;border:2px solid #b8d9c5;color:#1a5c38;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">📅 じゃらんゴルフ에서 예약 →</a>
        <a href="{rakuten}" style="display:block;background:#fdecea;border:2px solid #f5b8b8;color:#c0392b;text-align:center;padding:12px 16px;border-radius:10px;text-decoration:none;font-size:0.85rem;font-weight:700;" rel="nofollow" target="_blank">🏌️ 楽天GORA에서 예약 →</a>
      </div>
      <div class="info-bar" style="margin-top:12px;"><span class="icon">💡</span>그린피·카트·식사가 세트인 「패키지 플랜」을 이용하면 더욱 알뜰하게 즐길 수 있습니다.</div>
    </div>
  </div>
""".format(jalan=JALAN, rakuten=RAKUTEN)

with open("beginner-cards.html", encoding="utf-8") as f:
    bc = f.read()

bc = bc.replace("</div><!-- /ja -->", BOOKING_BANNER_JA + "</div><!-- /ja -->", 1)
bc = bc.replace("</div><!-- /en -->", BOOKING_BANNER_EN + "</div><!-- /en -->", 1)
bc = bc.replace("</div><!-- /ko -->", BOOKING_BANNER_KO + "</div><!-- /ko -->", 1)

with open("beginner-cards.html", "w", encoding="utf-8") as f:
    f.write(bc)
print("✅ beginner-cards.html: 予約バナー追加完了")

# ── ③ 全ページ: preconnect + lazy loading ──────────────────────────────
PRECONNECT = """  <link rel="preconnect" href="https://www.googletagmanager.com">
  <link rel="preconnect" href="https://www.google-analytics.com">"""

files = glob.glob("*.html")
perf_ok = 0

for fname in files:
    with open(fname, encoding="utf-8") as f:
        content = f.read()

    changed = False

    # preconnect追加（GAがある場合のみ）
    if "googletagmanager.com" in content and 'rel="preconnect"' not in content:
        content = content.replace("<head>", "<head>\n" + PRECONNECT, 1)
        changed = True

    # img loading="lazy" 追加（tracking pixelは除外）
    def add_lazy(m):
        tag = m.group(0)
        if 'loading=' in tag or '0.gif' in tag or 'width="1"' in tag:
            return tag
        return tag.replace('<img ', '<img loading="lazy" ')

    new_content = re.sub(r'<img [^>]+>', add_lazy, content)
    if new_content != content:
        content = new_content
        changed = True

    if changed:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(content)
        perf_ok += 1

print(f"✅ パフォーマンス改善: {perf_ok}件のファイルを更新")
print("\n全作業完了！")
