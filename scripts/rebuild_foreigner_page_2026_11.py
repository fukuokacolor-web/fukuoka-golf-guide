#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
book-fukuoka-golf-foreigner.html の本文を、確認できた事実だけで作り直す (2026-11-23)。
  旧本文の問題 (CLAUDE.md §7): 「日本語は話せなくても大丈夫」「80%以上が受け付ける」「受付は英語対応 (西戸崎・久山・芥屋)」
  「郵便番号は 100-0001 (皇居) を入れればよい」「海外の電話番号で大丈夫・ほとんど電話は来ない」「7日前まで無料キャンセル」
  「70%がセルフ・カートGPSに英語」などに出典がなく、コース自身の案内 (会員同伴・日本語話者の同伴・海外番号の予約は断る等) と矛盾。
  新本文: foreign_booking_rules.json (26コース・出典つき) の条件一覧が中心。条件が見つからなかったコースは「見つからなかった＝条件なしではない」。
  EN: The Reality〜FAQ / KO: 현실〜FAQ / JA: このページについて を置換。hero の説明・バッジ・meta・og・FAQ の JSON-LD も合わせる。
冪等 (MARKER)。改行コードはそのまま。Usage: python scripts/rebuild_foreigner_page_2026_11.py [--apply]
"""
import json, os, re, sys, html

sys.stdout.reconfigure(encoding="utf-8")
ROOTS = ["C:/Users/Owner/fukuoka-golf-guide", "C:/Users/Owner/Documents/新しいPJ"]
APPLY = "--apply" in sys.argv
F = "book-fukuoka-golf-foreigner.html"
MARK = "foreigner-rebuild-v1"
R = json.load(open(os.path.join(ROOTS[0], "foreign_booking_rules.json"), encoding="utf-8"))["courses"]
NAMES = json.load(open(os.path.join(ROOTS[0], "scripts/.cache/foreign_unchecked_names.json"), encoding="utf-8"))


def names_of(slug):
    s = open(os.path.join(ROOTS[0], f"course-{slug}.html"), encoding="utf-8").read()
    out = {}
    for lang in ("ja", "en", "ko"):
        i = s.find(f'id="c-{lang}"')
        m = re.search(r'class="hero-title"[^>]*>(.*?)</h1>', s[i:], re.S)
        out[lang] = re.sub(r"<[^>]+>|\s+", " ", m.group(1)).strip()
    return out


for slug in R:
    R[slug]["name"] = names_of(slug)

CATS = ["members_only", "member", "jp_speaker", "may_refuse", "no_lang"]
CAT_LABEL = {
    "ja": {"members_only": "会員制（ビジターは誰でも会員の紹介・同伴が必要）", "member": "海外の方・日本語が難しい方は会員の同伴が必要",
           "jp_speaker": "日本語で話せる人の同伴が必要", "may_refuse": "日本語が難しい方・海外の電話番号での予約は断ることがある",
           "no_lang": "受け付けるが外国語の表示・スタッフはない"},
    "en": {"members_only": "Members' clubs — every visitor needs a member", "member": "Overseas guests / non-Japanese speakers need a club member",
           "jp_speaker": "A Japanese speaker must be in your group", "may_refuse": "May decline guests who can't communicate in Japanese or use an overseas phone number",
           "no_lang": "Overseas guests accepted, but no foreign-language support"},
    "ko": {"members_only": "회원제 — 모든 비지터에게 회원이 필요", "member": "해외 고객·일본어가 어려운 고객은 회원 동반 필요",
           "jp_speaker": "일본어를 할 수 있는 사람의 동반 필요", "may_refuse": "일본어가 어렵거나 해외 전화번호로 예약하면 거절될 수 있음",
           "no_lang": "해외 고객 가능, 단 외국어 안내 없음"},
}
SRC = {"ja": {"rakuten": "楽天GORA", "jalan": "じゃらん", "official": "公式サイト"},
       "en": {"rakuten": "Rakuten GORA", "jalan": "Jalan", "official": "official site"},
       "ko": {"rakuten": "라쿠텐 GORA", "jalan": "자란", "official": "공식 사이트"}}
HEAD = {"ja": ("コース", "条件（コースの案内より）"), "en": ("Course", "Condition (from the course's notice)"), "ko": ("골프장", "조건 (골프장 안내 기준)")}
CSS = "    .vocab-row.cond { grid-template-columns: 1fr 2.2fr; }\n    @media (max-width: 640px) { .vocab-row.cond { grid-template-columns: 1fr; } .vocab-row.cond .vocab-cell { border-right: none; } }\n"


def table(lang):
    out = []
    for c in CATS:
        rows = [(k, v) for k, v in R.items() if v["cat"] == c]
        out.append(f'    <h3 style="font-family:var(--serif);font-size:18px;color:var(--ocean-dark);margin:30px 0 4px;">{CAT_LABEL[lang][c]}（{len(rows)}）</h3>'
                   if lang == "ja" else
                   f'    <h3 style="font-family:var(--serif);font-size:18px;color:var(--ocean-dark);margin:30px 0 4px;">{CAT_LABEL[lang][c]} ({len(rows)})</h3>')
        out.append('    <div class="vocab-table">')
        out.append(f'      <div class="vocab-row cond head"><div class="vocab-cell">{HEAD[lang][0]}</div><div class="vocab-cell">{HEAD[lang][1]}</div></div>')
        for k, v in rows:
            src = " / ".join(SRC[lang][x] for x in v["src"].split(","))
            out.append(f'      <div class="vocab-row cond"><div class="vocab-cell jp"><a href="course-{k}.html">{v["name"][lang]}</a></div>'
                       f'<div class="vocab-cell">{v[lang]} <span style="font-size:12px;color:var(--muted);">({src})</span></div></div>')
        out.append("    </div>")
    return "\n".join(out)


def unchecked(lang):
    sites = [n[lang] for k, n in sorted(NAMES.items(), key=lambda x: x[1]["en"]) if n["rakuten_plans"]]
    offi = [n[lang] for k, n in sorted(NAMES.items(), key=lambda x: x[1]["en"]) if not n["rakuten_plans"]]
    links = lambda xs: "、".join(xs) if lang == "ja" else ", ".join(xs)
    return sites, offi, links


def section_ja():
    sites, offi, links = unchecked("ja")
    return f'''  <section class="section"><!-- {MARK} -->
    <div class="sec-eyebrow">— このページについて</div>
    <h2 class="sec-title">海外からの方の予約条件を、コースごとにまとめました。</h2>
    <div class="prose">
      <p>じゃらんゴルフ・楽天GORAは日本語のみです。それに加えて、福岡の多くのゴルフ場が、海外からの方に条件を付けています。2026年11月23日に、楽天GORA・じゃらんの各コースの案内と公式サイトを読んだところ、当サイトの50コースのうち<strong>26コース</strong>に「会員の同伴が必要」「日本語で話せる人の同伴が必要」「入国当日は予約不可」といった条件が書かれていました。</p>
      <p>条件を満たさずに予約すると、当日キャンセルや断られることがあります。海外のゴルフ仲間を誘うときや、海外から来る方に紹介するときの確認用にどうぞ。英語版・韓国語版は右上の EN / KO から。</p>
    </div>
{table("ja")}
    <div class="prose" style="margin-top:28px;">
      <p><strong>条件が見つからなかったコース：</strong>{links(sites)}。各コースの最初の数プランしか見ていないので、「条件なし」という意味ではありません。予約前にコースに確認してください。</p>
      <p><strong>予約サイトで扱っていないコース（公式のみ）：</strong>{links(offi)}。今回は調べていません。</p>
    </div>
  </section>
'''


def section_en():
    sites, offi, links = unchecked("en")
    return f'''  <section class="section"><!-- {MARK} -->
    <div class="sec-eyebrow">— Read This First</div>
    <h2 class="sec-title">Many Fukuoka courses set conditions<br>for overseas guests.</h2>
    <div class="prose">
      <p>Japan's two big tee-time sites, Jalan Golf and Rakuten GORA, are in Japanese only. That is not the only hurdle. On 23 November 2026 we read the notices each course posts on Rakuten GORA and Jalan, plus some official websites. <strong>26 of the 50 courses on this site</strong> state a condition for overseas guests — most often that someone in your group must speak Japanese or be a member of the club, or that you can't book for the day you arrive in Japan.</p>
      <p>If you book without meeting a condition, the course may cancel the booking or turn you away on the day. Several courses also say they may decline bookings registered with an overseas phone number or address. <strong>Always enter your real details</strong> — do not use a made-up Japanese address or phone number.</p>
    </div>
  </section>

  <section class="section section-pale">
    <div class="sec-eyebrow">— Conditions by Course</div>
    <h2 class="sec-title">What each course says</h2>
    <p class="sec-desc">Summarised from each course's own notice on the site shown in brackets (checked 23 Nov 2026). Conditions can change — confirm with the course before you travel.</p>
{table("en")}
    <div class="prose" style="margin-top:28px;">
      <p><strong>No condition found:</strong> {links(sites)}. We only read the first few plans of each course, so this does not mean there are no conditions — ask the course before booking.</p>
      <p><strong>Not on the booking sites (official website only, not checked):</strong> {links(offi)}.</p>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— Booking Sites</div>
    <h2 class="sec-title">Booking on Jalan or Rakuten GORA</h2>
    <div class="prose">
      <p>Both sites are in Japanese only. You can read them with your browser's translate function (Chrome: right-click → Translate; Korean readers may prefer Naver Papago). Each course page on this site has buttons that open that course on Jalan or Rakuten GORA directly.</p>
      <p>Before you pay, open the plan details (<strong>プラン詳細</strong>) and read the course notice (<strong>ゴルフ場からのお知らせ</strong> / <strong>備考</strong>). That is where courses write their conditions for overseas guests, cancellation fees and dress code.</p>
    </div>
  </section>

  <section class="section section-warm">
    <div class="sec-eyebrow">— Vocabulary</div>
    <h2 class="sec-title">Japanese terms you will see</h2>
    <div class="vocab-table">
      <div class="vocab-row head"><div class="vocab-cell">Japanese</div><div class="vocab-cell">Reading</div><div class="vocab-cell">Meaning</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">平日</div><div class="vocab-cell">heijitsu</div><div class="vocab-cell">Weekday</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">土日祝</div><div class="vocab-cell">do-nichi-shuku</div><div class="vocab-cell">Sat / Sun / public holiday</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">セルフ</div><div class="vocab-cell">serufu</div><div class="vocab-cell">Self-play (no caddie)</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">キャディ付</div><div class="vocab-cell">kyadi-tsuki</div><div class="vocab-cell">With a caddie</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">昼食付</div><div class="vocab-cell">chūshoku-tsuki</div><div class="vocab-cell">Lunch included</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">スルー</div><div class="vocab-cell">surū</div><div class="vocab-cell">18 holes without the lunch break</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">メンバー同伴</div><div class="vocab-cell">membā dōhan</div><div class="vocab-cell">Must play with a club member</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">日本語</div><div class="vocab-cell">nihongo</div><div class="vocab-cell">Japanese (language)</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">入国当日</div><div class="vocab-cell">nyūkoku tōjitsu</div><div class="vocab-cell">The day you arrive in Japan</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">お断り</div><div class="vocab-cell">okotowari</div><div class="vocab-cell">Not accepted / refused</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">キャンセル料</div><div class="vocab-cell">kyanseru-ryō</div><div class="vocab-cell">Cancellation fee</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">2サム保証</div><div class="vocab-cell">tsū-samu hoshō</div><div class="vocab-cell">Guaranteed tee time for 2 players</div></div>
    </div>
  </section>

  <section class="section section-pale">
    <div class="sec-eyebrow">— FAQ</div>
    <h2 class="sec-title">Frequently asked questions</h2>
    <div class="faq-list">
      <div class="faq-item">
        <div class="faq-q">Do I need someone who speaks Japanese?</div>
        <div class="faq-a">At many courses, yes. Fifteen courses in the table above require a club member or a Japanese speaker in your group (plus five members' clubs where every visitor needs a member), and five more say they may decline guests who can't communicate in Japanese. Many of these courses also say they have no staff who speak other languages.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Can I use my overseas phone number?</div>
        <div class="faq-a">Use your real number. But be aware that some courses (for example Hisayama, Fukuoka Sunlake, Suonada, Dazaifu and Akane) say they may decline bookings registered with an overseas phone number or address.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Can I play on the day I arrive in Japan?</div>
        <div class="faq-a">Several courses refuse arrival-day bookings: Yasukogen, Moon Lake Kurate, JR Uchino and Seven Million. Fukuoka Lakeside accepts them only if you can reach the course an hour before your tee time.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">Is there a way to book in Korean?</div>
        <div class="faq-a">Fukuoka Century Golf Club points overseas travellers to the Korean booking sites Kakao VX and Hanatour. For other courses, book in Japanese on Jalan or Rakuten GORA, or contact the course.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">What about cancellation fees and dress code?</div>
        <div class="faq-a">They differ by course and plan. Check キャンセル料 and the course notice on the plan page before you pay. Several courses ask guests not to arrive or play in T-shirts, jeans or sandals.</div>
      </div>
    </div>
  </section>

'''


def section_ko():
    sites, offi, links = unchecked("ko")
    return f'''  <section class="section"><!-- {MARK} -->
    <div class="sec-eyebrow">— 먼저 읽어 주세요</div>
    <h2 class="sec-title">후쿠오카의 많은 골프장이<br>해외 고객에게 조건을 두고 있습니다.</h2>
    <div class="prose">
      <p>일본의 2대 골프 예약 사이트인 자란골프와 라쿠텐 GORA는 일본어로만 운영됩니다. 그것만이 장벽은 아닙니다. 2026년 11월 23일, 라쿠텐 GORA·자란에 각 골프장이 올린 안내와 일부 공식 사이트를 읽어 본 결과, <strong>이 사이트의 50개 골프장 중 26곳</strong>이 해외 고객에게 조건을 두고 있었습니다. 가장 많은 것은 일본어를 할 수 있는 사람이나 회원이 같은 팀에 있어야 한다는 조건과, 일본 입국 당일에는 예약할 수 없다는 조건입니다.</p>
      <p>조건을 충족하지 않고 예약하면 예약이 취소되거나 당일 거절될 수 있습니다. 해외 전화번호·주소로 등록된 예약은 거절할 수 있다고 밝힌 골프장도 있습니다. <strong>반드시 실제 정보를 입력하세요</strong> — 가짜 일본 주소나 전화번호를 쓰면 안 됩니다.</p>
    </div>
  </section>

  <section class="section section-pale">
    <div class="sec-eyebrow">— 골프장별 조건</div>
    <h2 class="sec-title">골프장별 안내 내용</h2>
    <p class="sec-desc">괄호 안 사이트에 게재된 각 골프장의 안내를 요약했습니다 (2026년 11월 23일 확인). 조건은 바뀔 수 있으니 출발 전에 골프장에 확인하세요.</p>
{table("ko")}
    <div class="prose" style="margin-top:28px;">
      <p><strong>조건을 찾지 못한 골프장:</strong> {links(sites)}. 각 골프장의 처음 몇 개 플랜만 확인했으므로 조건이 없다는 뜻은 아닙니다. 예약 전에 골프장에 확인하세요.</p>
      <p><strong>예약 사이트에 없는 골프장 (공식 사이트만·이번에 확인하지 않음):</strong> {links(offi)}.</p>
    </div>
  </section>

  <section class="section">
    <div class="sec-eyebrow">— 예약 사이트</div>
    <h2 class="sec-title">자란·라쿠텐 GORA로 예약하기</h2>
    <div class="prose">
      <p>두 사이트 모두 일본어로만 운영됩니다. 브라우저 번역 기능(크롬: 우클릭 → 번역)이나 네이버 파파고로 읽을 수 있습니다. 이 사이트의 각 골프장 페이지에는 자란·라쿠텐 GORA의 해당 골프장 페이지로 바로 가는 버튼이 있습니다.</p>
      <p>결제 전에 플랜 상세(<strong>プラン詳細</strong>)를 열어 골프장 안내(<strong>ゴルフ場からのお知らせ</strong> / <strong>備考</strong>)를 읽으세요. 해외 고객 조건·취소료·복장 규정이 여기에 적혀 있습니다.</p>
    </div>
  </section>

  <section class="section section-warm">
    <div class="sec-eyebrow">— 어휘</div>
    <h2 class="sec-title">자주 보게 되는 일본어</h2>
    <div class="vocab-table">
      <div class="vocab-row head"><div class="vocab-cell">일본어</div><div class="vocab-cell">읽는 법</div><div class="vocab-cell">뜻</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">平日</div><div class="vocab-cell">헤이지쓰</div><div class="vocab-cell">평일</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">土日祝</div><div class="vocab-cell">도니치슈쿠</div><div class="vocab-cell">토·일·공휴일</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">セルフ</div><div class="vocab-cell">세루후</div><div class="vocab-cell">셀프 플레이 (캐디 없음)</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">キャディ付</div><div class="vocab-cell">캬디쓰키</div><div class="vocab-cell">캐디 포함</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">昼食付</div><div class="vocab-cell">추쇼쿠쓰키</div><div class="vocab-cell">점심 포함</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">スルー</div><div class="vocab-cell">스루</div><div class="vocab-cell">점심 휴식 없이 18홀</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">メンバー同伴</div><div class="vocab-cell">멤바 도한</div><div class="vocab-cell">회원과 함께 플레이해야 함</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">日本語</div><div class="vocab-cell">니혼고</div><div class="vocab-cell">일본어</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">入国当日</div><div class="vocab-cell">뉴코쿠 도지쓰</div><div class="vocab-cell">일본 입국 당일</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">お断り</div><div class="vocab-cell">오코토와리</div><div class="vocab-cell">받지 않음 / 거절</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">キャンセル料</div><div class="vocab-cell">캰세루료</div><div class="vocab-cell">취소료</div></div>
      <div class="vocab-row"><div class="vocab-cell jp">2サム保証</div><div class="vocab-cell">쓰사무 호쇼</div><div class="vocab-cell">2인 플레이 보장</div></div>
    </div>
  </section>

  <section class="section section-pale">
    <div class="sec-eyebrow">— FAQ</div>
    <h2 class="sec-title">자주 묻는 질문</h2>
    <div class="faq-list">
      <div class="faq-item">
        <div class="faq-q">일본어를 할 수 있는 사람이 필요한가요?</div>
        <div class="faq-a">많은 골프장에서 필요합니다. 위 표의 15개 골프장은 회원 또는 일본어를 할 수 있는 사람의 동반이 필요하고 (모든 비지터에게 회원이 필요한 회원제 5곳 별도), 5곳은 일본어 소통이 어려운 고객을 거절할 수 있다고 밝히고 있습니다. 이 골프장들 중 다수는 일본어 외의 언어를 하는 직원이 없다고 안내합니다.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">한국 전화번호로 예약해도 되나요?</div>
        <div class="faq-a">실제 번호를 입력하세요. 다만 히사야마·후쿠오카 선레이크·스오나다·다자이후·아카네 등 일부 골프장은 해외 전화번호·주소로 등록된 예약을 거절할 수 있다고 밝히고 있습니다.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">일본에 도착한 날 플레이할 수 있나요?</div>
        <div class="faq-a">야스코겐·문레이크 쿠라테·JR 우치노·세븐 밀리언은 입국 당일 예약을 받지 않습니다. 후쿠오카 레이크사이드는 스타트 1시간 전까지 도착할 수 있는 경우에만 가능합니다.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">한국어로 예약할 수 있는 방법이 있나요?</div>
        <div class="faq-a">후쿠오카 센추리 골프 클럽은 해외 여행객에게 카카오 VX·하나투어를 통한 예약을 안내하고 있습니다. 다른 골프장은 자란·라쿠텐 GORA에서 일본어로 예약하거나 골프장에 직접 문의하세요.</div>
      </div>
      <div class="faq-item">
        <div class="faq-q">취소료와 복장 규정은요?</div>
        <div class="faq-a">골프장과 플랜마다 다릅니다. 결제 전에 플랜 페이지의 キャンセル料와 골프장 안내를 확인하세요. 티셔츠·청바지·샌들 차림의 내장·플레이를 삼가 달라는 골프장이 여러 곳 있습니다.</div>
      </div>
    </div>
  </section>

'''


FAQ_LD = '''    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": "Do I need someone who speaks Japanese to play golf in Fukuoka?",
        "acceptedAnswer": { "@type": "Answer", "text": "At many courses, yes. In November 2026, 15 Fukuoka courses stated in their booking notices that overseas guests need a club member or a Japanese speaker in the group, and five more said they may decline guests who cannot communicate in Japanese." } },
      { "@type": "Question", "name": "Can I book a Fukuoka golf course with an overseas phone number?",
        "acceptedAnswer": { "@type": "Answer", "text": "Use your real number, but some courses (for example Hisayama, Fukuoka Sunlake, Suonada, Dazaifu and Akane) say they may decline bookings registered with an overseas phone number or address." } },
      { "@type": "Question", "name": "Can I play golf on the day I arrive in Japan?",
        "acceptedAnswer": { "@type": "Answer", "text": "Several Fukuoka courses refuse arrival-day bookings, including Yasukogen, Moon Lake Kurate, JR Uchino and Seven Million. Fukuoka Lakeside accepts them only if you can arrive an hour before your tee time." } }
    ]
  }'''


def sub_between(s, start_pat, end_pat, new, label):
    i = s.find(start_pat)
    j = s.find(end_pat, i + 1)
    assert i > 0 and j > i, label
    line_start = s.rfind("\n", 0, i) + 1
    end_line = s.rfind("\n", 0, j) + 1
    return s[:line_start] + new + s[end_line:]


for root in ROOTS:
    p = os.path.join(root, F)
    s = open(p, encoding="utf-8", newline="").read()
    if MARK in s:
        print(root[-10:], "already"); continue
    nl = "\r\n" if "\r\n" in s else "\n"
    t = s.replace("\r\n", "\n")
    # 本文 (後ろから)
    t = sub_between(t, '<div class="sec-eyebrow">— 현실</div>', '<div class="sec-eyebrow">— 다음 단계</div>', section_ko(), "ko")
    t = sub_between(t, '<div class="sec-eyebrow">— The Reality</div>', '<div class="sec-eyebrow">— Next Steps</div>', section_en(), "en")
    i = t.find('<div class="sec-eyebrow">— このページについて</div>')
    j = t.find("</section>", i) + len("</section>\n")
    ls = t.rfind("\n", 0, i) + 1
    t = t[:ls] + section_ja() + t[j:]
    # JSON-LD FAQ
    t = re.sub(r'    "@type": "FAQPage",\n    "mainEntity": \[.*?\n    \]\n  \}', lambda _: FAQ_LD, t, count=1, flags=re.S)
    # hero・meta
    rep = [
        (re.compile(r'(<p class="hero-sub">)日本のゴルフ予約サイト\(じゃらん・楽天GORA\)は日本語専用。[^<]*(</p>)'),
         r"\1じゃらん・楽天GORAは日本語のみ。さらに福岡の多くのゴルフ場が、海外からの方に条件（会員や日本語話者の同伴・入国当日不可など）を付けています。コースごとの条件をまとめました。\2"),
        (re.compile(r"(<p class=\"hero-sub\">)Japan's tee-time platforms only speak Japanese[^<]*(</p>)"),
         r"\1Japan's tee-time sites are in Japanese only — and many Fukuoka courses set conditions for overseas guests. Here is what each course says, before you book.\2"),
        (re.compile(r'(<p class="hero-sub">)일본의 양대 골프 예약 사이트[^<]*(</p>)'),
         r"\1일본의 골프 예약 사이트는 일본어로만 운영되며, 후쿠오카의 많은 골프장이 해외 고객에게 조건을 두고 있습니다. 예약 전에 골프장별 조건을 확인하세요.\2"),
        (re.compile(r'<span class="hero-badge">📅 Jalan/Rakuten 直リンク付</span>'), '<span class="hero-badge">📋 コース別の条件（11/23確認）</span>'),
        (re.compile(r'<span class="hero-badge">📅 Step-by-step</span>'), '<span class="hero-badge">📋 Conditions by course (Nov 23)</span>'),
        (re.compile(r'<span class="hero-badge">📅 단계별 가이드</span>'), '<span class="hero-badge">📋 골프장별 조건 (11/23)</span>'),
        (re.compile(r'(<meta name="description" content=")[^"]*(">)'),
         r"\1外国人向け福岡ゴルフ場予約ガイド。福岡の50コースのうち26コースが海外からの方に条件（会員・日本語話者の同伴、入国当日不可など）を付けています。コースごとの条件を英語・韓国語でまとめました（2026年11月確認）。\2"),
        (re.compile(r'(<meta property="og:description" content=")[^"]*(">)'),
         r"\1Japan's tee-time sites are in Japanese only, and 26 of 50 Fukuoka courses set conditions for overseas guests — a Japanese speaker or member in your group, no arrival-day bookings. Conditions by course, checked Nov 2026.\2"),
    ]
    for rx, b in rep:
        t, n = rx.subn(b, t, count=1)
        assert n == 1, rx.pattern[:50]
    t = t.replace("    .vocab-cell.jp {", CSS + "    .vocab-cell.jp {", 1)
    for bad in ("100-0001", "80%", "English-speaking reception", "Reception speaks basic English", "70% of Fukuoka"):
        assert bad not in t, bad
    new = t.replace("\n", nl) if nl == "\r\n" else t
    assert new.count("G-PENH0Z4VT7") == s.count("G-PENH0Z4VT7")
    print(root[-10:], "rebuilt", len(s), "->", len(new))
    if APPLY:
        open(p, "w", encoding="utf-8", newline="").write(new)
print("APPLIED" if APPLY else "DRY-RUN")
