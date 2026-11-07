#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
privacy.html を editorial-policy.html の head (GA4・CSS) を流用して生成する (JA のみ)。
冪等: 生成結果が同じなら上書きしても差分なし。
Usage:
  python scripts/build_privacy_page.py            # dry-run
  python scripts/build_privacy_page.py --preview  # PREVIEW だけ
  python scripts/build_privacy_page.py --apply    # REPO + PREVIEW
"""
import os, re, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
URL = "https://fukuoka-golf-guide.com/privacy.html"
TITLE = "プライバシーポリシー | 福岡ゴルフ場ガイド"
DESC = "福岡ゴルフ場ガイドのプライバシーポリシー。アクセス解析、広告リンク、地図、SNS投稿の埋め込みなどで外部に送信される情報と、停止の方法、削除依頼の窓口を案内します。"


def row(name, company, purpose, url):
    return f'<tr><td>{name}</td><td>{company}</td><td>{purpose}</td><td><a href="{url}" target="_blank" rel="noopener">公式の説明</a></td></tr>'


ROWS = [
    row("Google Analytics 4", "Google LLC", "アクセス解析（閲覧ページ、クリック、端末、おおよその地域など）", "https://policies.google.com/technologies/partner-sites?hl=ja"),
    row("Google Fonts", "Google LLC", "文字の表示（IPアドレスなどが送信されます）", "https://policies.google.com/privacy?hl=ja"),
    row("Googleマップ", "Google LLC", "地図の表示（地図のあるページ）", "https://policies.google.com/privacy?hl=ja"),
    row("Googleフォーム", "Google LLC", "お問い合わせページのフォームの受付", "https://policies.google.com/privacy?hl=ja"),
    row("A8.net", "株式会社ファンコミュニケーションズ", "アフィリエイト広告の表示と成果の計測", "https://www.a8.net/privacy.html"),
    row("楽天アフィリエイト・楽天GORA", "楽天グループ株式会社", "広告リンクの先での成果の計測", "https://privacy.rakuten.co.jp/"),
    row("じゃらんゴルフ", "株式会社リクルート", "広告リンクの先での予約", "https://www.recruit.co.jp/privacy/"),
    row("Threads（投稿の埋め込み）", "Meta Platforms, Inc.", "投稿の表示（埋め込みのあるページを開いたとき）", "https://help.instagram.com/515230437301944"),
]

BODY = f"""<body>

<a href="index.html" class="back-link">← Top</a>

<div id="c-ja" class="content on">
  <section class="hero">
    <h1>プライバシーポリシー</h1>
    <p>福岡ゴルフ場ガイド（fukuoka-golf-guide.com）が扱う情報と、外部に送信される情報について</p>
  </section>

  <div class="container">

    <div class="section">
      <h2>1. 取得する情報</h2>
      <p>当サイトには会員登録がなく、閲覧のために氏名やメールアドレスを入力していただく必要はありません。次の情報を扱います。</p>
      <ul>
        <li>アクセス解析と広告の計測で、Cookieなどにより自動で送信される情報（閲覧したページ、クリック、端末やブラウザの種類、IPアドレス、おおよその地域など）</li>
        <li>お問い合わせの際にお送りいただいた内容</li>
      </ul>
    </div>

    <div class="section">
      <h2>2. 利用の目的</h2>
      <ul>
        <li>サイトの利用状況を把握し、内容を改善するため</li>
        <li>広告の成果を計測するため</li>
        <li>お問い合わせに返信するため</li>
      </ul>
    </div>

    <div class="section">
      <h2>3. 外部に送信される情報</h2>
      <p>当サイトでは次のサービスを利用しており、ページを開いたときやリンクを押したときに、お使いの端末から各社へ情報が送信されることがあります。各社での扱いは、それぞれの説明をご覧ください。</p>
      <div style="overflow-x:auto;">
      <table class="meta-table">
        <thead><tr><th>サービス</th><th>提供者</th><th>目的</th><th>詳細</th></tr></thead>
        <tbody>
        {chr(10).join(ROWS)}
        </tbody>
      </table>
      </div>
    </div>

    <div class="section">
      <h2>4. 送信を止める方法</h2>
      <ul>
        <li>Google Analyticsは、Googleの<a href="https://tools.google.com/dlpage/gaoptout?hl=ja" target="_blank" rel="noopener">オプトアウトアドオン</a>で止められます。</li>
        <li>ブラウザの設定でCookieを無効にしたり削除したりできます。一部の機能や広告の計測が働かなくなることがあります。</li>
      </ul>
    </div>

    <div class="section">
      <h2>5. SNS投稿の埋め込みと掲載の取り下げ</h2>
      <p>コースページでは、ThreadsやInstagramの公開投稿を、各サービスの公式の埋め込み機能で紹介することがあります。投稿の画像や文章は当サイトに保存していません。元の投稿が削除されたり非公開になったりすると、表示されなくなります。</p>
      <p>ご自身の投稿や、写っている方から取り下げのご希望があれば、<a href="https://www.threads.com/@fukuoka_golf_guide1" target="_blank" rel="noopener">運営者のThreads（@fukuoka_golf_guide1）</a>へお知らせください。確認でき次第、速やかに外します。</p>
    </div>

    <div class="section">
      <h2>6. お問い合わせの窓口と内容の扱い</h2>
      <p>このページの内容についてのお問い合わせは、<a href="https://www.threads.com/@fukuoka_golf_guide1" target="_blank" rel="noopener">運営者のThreads（@fukuoka_golf_guide1）</a>で受け付けています。お問い合わせの内容は、返信と対応のためにだけ使います。法令に基づく場合を除き、ご本人の同意なく第三者に提供しません。</p>
    </div>

    <div class="section">
      <h2>7. このページの変更</h2>
      <p>利用するサービスの変更などに応じて、内容を変更することがあります。変更後の内容は、このページに掲載した時点から適用します。</p>
      <p>制定：2026年11月7日</p>
    </div>

  </div>
</div>

<footer>
  <a href="index.html">← トップへ</a> ｜
  <a href="sitemap-guide.html">サイトマップ</a> ｜
  <a href="editorial-policy.html">編集ポリシー</a> ｜
  <a href="contact.html">お問い合わせ</a>
</footer>

</body>
</html>
"""


def main():
    s = open(os.path.join(REPO_ROOT, "editorial-policy.html"), encoding="utf-8", newline="").read()
    head = s[:s.index("<body>")]
    head = re.sub(r'[ \t]*<script type="application/ld\+json">.*?</script>\r?\n', "", head, flags=re.S)
    head = re.sub(r'[ \t]*<link rel="alternate" hreflang="[^"]+" href="[^"]+">\r?\n', "", head)
    head = re.sub(r"<title>.*?</title>", f"<title>{TITLE}</title>", head)
    head = re.sub(r'(<meta name="description"[^>]*?) content="[^"]*"', rf'\1 content="{DESC}"', head)
    head = head.replace('<meta name="description" content="', '<meta name="description" content="', 1)
    head = re.sub(r'(<meta property="og:title" content=")[^"]*', rf"\g<1>{TITLE}", head)
    head = re.sub(r'(<meta property="og:description" content=")[^"]*', rf"\g<1>{DESC}", head)
    head = head.replace("https://fukuoka-golf-guide.com/editorial-policy.html", URL)
    assert head.count("G-PENH0Z4VT7") >= 1 and "editorial-policy" not in head
    new = (head + BODY.replace("\r\n", "\n").replace("\n", "\r\n"))
    print("privacy.html", len(new), "chars", "G-tag", new.count("G-PENH0Z4VT7"))
    if APPLY:
        for root in ROOTS:
            open(os.path.join(root, "privacy.html"), "w", encoding="utf-8", newline="").write(new)
        print("APPLIED", ROOTS)
    else:
        print("DRY-RUN")


if __name__ == "__main__":
    main()
