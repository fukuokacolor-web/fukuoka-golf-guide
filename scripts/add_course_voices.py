#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
コースページ (JA のみ) に「Threadsでの評判」セクションを入れる。内容は course_voices.json から生成する。

- 位置: JA の「— Getting Here」セクションの直前
- 編集部の要約だけを載せる (ユーザー名・投稿文の転載なし)。Review 等の構造化データは付けない
- 冪等: MARKER で囲んだ範囲を作り直す
Usage:
  python scripts/add_course_voices.py --dry-run               # 件数を表示 (書き込みなし)
  python scripts/add_course_voices.py --only nijo --preview   # 1件テスト: PREVIEW だけ
  python scripts/add_course_voices.py --apply                 # REPO + PREVIEW
"""
import json, os, re, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
ONLY = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
MARKER = "<!-- course-voices-v1 -->"
END = "<!-- /course-voices-v1 -->"
ANCHOR = re.compile(r'[ \t]*<section class="section[^"]*">\r?\n[ \t]*<div class="sec-eyebrow">— Getting Here</div>')
BLOCK = re.compile(re.escape(MARKER) + r".*?" + re.escape(END) + r"\r?\n", re.S)
CARD = "background:#fff;border:1px solid var(--line);border-radius:14px;padding:22px 24px;"
HEAD = "font-weight:700;font-size:15px;margin-bottom:10px;"
ITEM = "font-size:14px;line-height:1.7;padding:9px 0;border-top:1px solid var(--line);"
COUNT = "color:var(--muted);font-size:12px;white-space:nowrap;margin-left:6px;"


def items(rows):
    return "".join(f'<li style="{ITEM}">{r["text"]}<span style="{COUNT}">{r["count"]}件</span></li>' for r in rows)


def embed_card(p):
    if "instagram.com" in p["url"]:
        attrs = f'class="instagram-media" data-instgrm-permalink="{p["url"]}" data-instgrm-version="14"'
    else:
        attrs = f'class="text-post-media" data-text-post-permalink="{p["url"]}" data-text-post-version="0"'
    note = f'<p style="font-size:12px;color:var(--muted);margin:0 0 8px;">{p["note"]}</p>' if p.get("note") else ""
    return (f'<div style="min-height:420px;min-width:0;">{note}<blockquote {attrs} style="margin:0;max-width:100%;">'
            f'<a href="{p["url"]}" target="_blank" rel="noopener">{p["label"]}</a></blockquote></div>')


def embed_lines(c):
    """公式の埋め込み。スクリプトは欄が画面に近づいてから読み込む (LCP を邪魔しない)"""
    posts = c.get("embeds")
    if not posts:
        return []
    srcs = []
    if any("instagram.com" in p["url"] for p in posts):
        srcs.append("https://www.instagram.com/embed.js")
    if any("threads." in p["url"] for p in posts):
        srcs.append("https://www.threads.com/embed.js")
    names = "・".join(n for n, k in (("Instagram", "instagram.com"), ("Threads", "threads.")) if any(k in p["url"] for p in posts))
    src_js = ",".join(f"'{u}'" for u in srcs)
    return [
        f'    <div class="voices-embeds" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:24px;">{"".join(embed_card(p) for p in posts)}</div>',
        f'    <p style="margin-top:12px;font-size:12px;line-height:1.7;color:var(--muted);">投稿は{names}の公式埋め込みで紹介しています。表示されない場合は、元の投稿が削除されたか非公開になった可能性があります。掲載の取り下げは<a href="https://www.threads.com/@fukuoka_golf_guide1" target="_blank" rel="noopener">運営者のThreads</a>へご連絡ください（<a href="privacy.html">プライバシーポリシー</a>）。</p>',
        "    <script>(function(){var e=document.querySelector('.voices-embeds');if(!e)return;function l(){[" + src_js + "].forEach(function(u){var s=document.createElement('script');s.src=u;s.async=true;document.body.appendChild(s);});}"
        "if(!('IntersectionObserver' in window)){l();return;}var o=new IntersectionObserver(function(x){if(x[0].isIntersecting){o.disconnect();l();}},{rootMargin:'400px'});o.observe(e);})();</script>",
    ]


def render(c, nl):
    lines = [
        MARKER,
        '  <section class="section">',
        '    <div class="sec-eyebrow">— Voices on Threads</div>',
        '    <h2 class="sec-title">Threadsでの評判</h2>',
        f'    <p class="sec-desc">Threadsの公開投稿とコメント{c["total"]}件（{c["period"]}）を編集部が要約しました。個人の感想で、時期や条件によって変わります。</p>',
        '    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;margin-top:24px;">',
        f'      <div style="{CARD}"><div style="{HEAD}color:var(--forest);">よく挙がる良い点</div><ul style="list-style:none;margin:0;padding:0;">{items(c["good"])}</ul></div>',
        *([f'      <div style="{CARD}"><div style="{HEAD}color:var(--orange-dark);">行く前に知っておきたい点</div><ul style="list-style:none;margin:0;padding:0;">{items(c["care"])}</ul></div>'] if c["care"] else []),
        '    </div>',
        f'    <p style="margin-top:18px;font-size:14px;line-height:1.8;"><strong>編集部のまとめ：</strong>{c["fit"]}</p>',
        *embed_lines(c),
        '  </section>',
        END,
    ]
    return nl.join(lines) + nl


def apply_one(html, c):
    nl = "\r\n" if "\r\n" in html else "\n"
    block = render(c, nl)
    if MARKER in html:
        return BLOCK.sub(lambda m: block, html, count=1), "rebuilt"
    m = ANCHOR.search(html)  # 最初の一致 = JA
    if not m:
        return html, "no_match"
    return html[:m.start()] + block + html[m.start():], "inserted"


def main():
    data = json.load(open(os.path.join(REPO_ROOT, "course_voices.json"), encoding="utf-8"))["courses"]
    c = {"inserted": 0, "rebuilt": 0, "already": 0, "no_match": 0, "not_found": 0}
    for slug, v in data.items():
        if ONLY and slug != ONLY:
            continue
        name = f"course-{slug}.html"
        path = os.path.join(REPO_ROOT, name)
        if not os.path.exists(path):
            c["not_found"] += 1; continue
        src = open(path, encoding="utf-8", newline="").read()
        new, st = apply_one(src, v)
        if st == "no_match":
            print("no_match", name)
        c["already" if new == src and st == "rebuilt" else st] += 1
        if APPLY and new != src:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(new)
    print(c, "APPLIED" if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
