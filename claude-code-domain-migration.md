# Claude Code 作業指示書 v2.2
## 独自ドメイン移行に伴うサイト側対応 (Post-Domain Migration Tasks)

> **このドキュメントは v1 → v2.0 (1巡目レビュー反映) → v2.1 (2巡目反映) → v2.2 (3巡目最終調整) と段階的に修正された最終版です。**
> リポジトリのルートに `claude-code-domain-migration.md` として保存し、Claude Code に
> 「`claude-code-domain-migration.md` を読んで、Phase 0 から順番に作業して。各 Phase 完了ごとに私に確認してから次に進んで」
> と指示してください。

---

## 修正履歴 (v1 → v2.0 → v2.1 → v2.2)

レビューで見つかった問題を以下のとおり反映しています。

### v2.1 → v2.2 (3巡目最終調整)

| # | 問題 | 対応 |
|---|------|------|
| α | Phase 0 完了報告に「→ Phase 0.5 へ」とあるが実際は Phase 1 が先 | 「→ Phase 1 → Phase 0.5 の順」と明記 |
| β | Phase 10 の「新ドメイン出現数 622以上」表現が曖昧 (canonical/OGP 追加後は 700+ になる) | 「622 + canonical/OGP/sitemap 追加分」と説明文を追加 |
| γ | `load_existing_lastmods` の正規表現が `<loc>` と `<lastmod>` の隣接を仮定 (`<priority>` 等が間に挟まると lastmod 継承が失敗するリスク) | `<url>...</url>` ブロック単位での抽出に変更 (要素順非依存・堅牢) |
| δ | Phase 4・Phase 6 で `mkdir -p scripts` が抜けていた (Phase 3 で作成済み前提) | 冪等性確保のため両方に追加 |

### v2.0 → v2.1 (2巡目レビュー反映)

| # | 問題 | 対応 |
|---|------|------|
| A | Phase 2 の perl が `*.md` を対象とするため、本ランブック自身が書き換えられて壊れる | `-not -name "claude-code-domain-migration.md"` を全置換コマンドに追加。ランブック内の旧URL参照は意図的に保持 |
| B | Phase 0.5 の CNAME コミットが `main` に乗ってしまう (Phase 1 の説明と矛盾) | Phase 1 (ブランチ作成) を先に実行する順序に変更。CNAME コミットは feature ブランチ上に乗る |
| C | CNAME ファイルが末尾改行なしで作成される (GitHub UI 出力形式と不一致) | `printf "...\n"` に変更。`wc -c` の期待値も 22 → 23 に更新 |
| D | `gh` CLI が前提情報に明記されていなかった | 前提情報テーブルに追記 |
| E | sitemap 自動生成で `<changefreq>` を全URLに追加するが、コミットメッセージで触れていなかった | コミットメッセージに明記 |
| F | EXCLUDE_FILES がスクリプトごとに違う理由が不明瞭 | 各スクリプトにコメント追加 |

### v1 → v2.0 (1巡目レビュー反映)

| # | v1 の問題 | v2 の対応 | 重大度 |
|---|---------|---------|------|
| 1 | CNAME ファイルが存在しないのに「中身を確認」前提だった | **Phase 0.5 を新設**して CNAME 作成と GitHub Pages 設定を行う | 🔴 致命 |
| 2 | `python3` が Windows Store スタブにリダイレクトされ実行不可 | 全コマンドを `python` に変更 | 🔴 致命 |
| 3 | Phase 2 の Perl 置換対象に `*.py` が無く、`generate_course_v2.py` の旧URL 5箇所が取り残される | Phase 2 の対象拡張子に `*.py` を追加 | 🔴 致命 |
| 4 | Phase 6 の sitemap 自動生成で priority 0.9 の6エントリが消失 | `HIGH_PRIORITY_PAGES` 集合 + 既存 lastmod 継承ロジックを追加 | 🔴 致命 |
| 5 | Phase 5 が「目視検証のみ」で JSON-LD 内 117ブロックの取り残し検出が不十分 | grep ベースの 0件確認に格上げ | 🔴 致命 |
| 6 | OGP 正規表現が属性順序 `property=...content=...` を仮定（リバース順を取りこぼす） | 両順序に対応する 2パス置換に変更 | 🟡 警告 |
| 7 | `lastmod` を全URL「今日」に統一 → SEO上「全部更新」の誤シグナル | 既存 sitemap.xml から lastmod を継承 | 🟡 警告 |
| 8 | Phase 11 で「PR か直接マージ」を選択肢にしていた | **PR必須**に変更（80+ファイル変更のため） | 🟡 警告 |
| 9 | Phase 10 の `kill $SERVER_PID` が Git Bash + Windows Python で失敗する | `taskkill` を使用 | 🟡 警告 |
| 10 | 「Enforce HTTPS」確認が Phase 8 にあるが、http→https 化の Phase 2 より前に確認すべき | Phase 0 に確認ステップを前倒し | 🟡 警告 |
| 11 | 複数 canonical タグの場合 `count=1` で2個目以降が残る | 検出時に警告ログ出力 | 🟡 警告 |
| 12 | 「メタリフレッシュ・フォールバックを追加せよ」というレビュー意見 | **不要と判断**：GitHub Pages はカスタムドメイン設定時に旧URLから自動で 301 リダイレクトを返す | ❌ 棄却 |
| 13 | 「og:* リバース順対応」をブロッカーとする意見 | **このリポジトリには該当なし**を実機確認、警告に降格 | ⬇️ 降格 |

---

## 0. 前提情報 (変更不可・基準値)

| 項目 | 値 |
|---|---|
| リポジトリ | `fukuokacolor-web/fukuoka-golf-guide` |
| ホスティング | GitHub Pages |
| 旧公開URL | `https://fukuokacolor-web.github.io/fukuoka-golf-guide/` |
| 新ドメイン (canonical) | `https://fukuoka-golf-guide.com` |
| www サブドメイン | GitHub が自動で apex にリダイレクト (設定不要) |
| HTTPS | 「Enforce HTTPS」を Phase 0 で確認する |
| CNAME ファイル | **現状は不在。Phase 0.5 で作成する** |
| 言語 | 日本語 (ja) / 英語 (en) / 韓国語 (ko) ※現状は同一 HTML 内に共存 |
| GA4 | 既存設定あり (`G-PENH0Z4VT7`)。**タグは絶対に変更・削除しない** |
| HTML ファイル数 | リポジトリ直下 79 ファイル (フラット構造) |
| 旧URL出現箇所 | **約 622箇所 / 80ファイル** (HTML, sitemap.xml, robots.txt, generate_course_v2.py)。本ランブック (`claude-code-domain-migration.md`) 自体には参考用に約24箇所含まれているが、置換対象外とする |
| Phase 2 (言語別URL化) | このドキュメントの**範囲外** (別指示書で扱う) |
| Python | `python` を使う。**`python3` は Windows Store スタブのため実行不可** |
| GitHub CLI | `gh` コマンドを Phase 11 の PR 作成で使用する。インストール・認証済みであること |
| 本ランブック自体の扱い | `claude-code-domain-migration.md` は**全ての置換・スクリプトの対象から除外する** (`-not -name "claude-code-domain-migration.md"` を find に付与) |

---

## 1. 全体ルール (Claude Code が常に守ること)

### 1-1. 安全策
1. 作業開始前に必ず `git status` を確認し、クリーンであることを確認する
2. 作業前に新ブランチを切る:`feature/domain-migration`
3. 各 Phase 完了ごとに**ユーザー確認を求めてから**次に進む
4. **GA4 関連のタグ (`gtag`, `G-PENH0Z4VT7`, `googletagmanager.com`) は絶対に編集しない**
5. **Phase 0.5 で CNAME を作成する以外、CNAME ファイルは編集しない**
6. 一括置換の前には必ず `grep -rn` で対象を全件提示し、ユーザー承認を得る
7. ファイル削除は禁止 (リダイレクト用に必要なファイルがあるため)
8. **Python コマンドは `python` を使う。`python3` は使わない**

### 1-2. コミット規約
- Conventional Commits を使用
- 1 コミット 1 目的
- 例: `fix: replace old GitHub Pages URLs with new custom domain`
- 例: `feat: add canonical tags to all HTML pages`
- 例: `chore: update sitemap.xml with new domain`

### 1-3. 禁止事項
- `git reset --hard`、`git push --force` の実行 (必要時はユーザー確認必須)
- `node_modules/`、`.DS_Store`、`.env` などのコミット
- 言語切替UI(JS) の論理変更 (Phase 2 の領域)
- レイアウト・デザインの変更
- コンテンツの翻訳・本文修正
- **直接 main へのマージ** (Phase 11 で PR 経由必須)

---

## 2. Phase 0: 現状調査 (必ず最初に実行)

### 2-1. リポジトリ構造の把握

```bash
# 全体構造
ls -la
find . -maxdepth 2 -type d | grep -v node_modules | grep -v .git

# HTML ファイル一覧と数 (フラット構造のため maxdepth 2 で十分)
find . -maxdepth 2 -type f -name "*.html" -not -path "./.git/*" | wc -l
find . -maxdepth 2 -type f -name "*.html" -not -path "./.git/*" | sort

# サイトマップ・robots
ls -la sitemap*.xml robots.txt 2>/dev/null

# CNAME 確認 (本リポジトリでは不在を想定 — Phase 0.5 で作成)
ls -la CNAME 2>/dev/null && echo "EXISTS" || echo "MISSING (will create in Phase 0.5)"
```

### 2-2. GitHub Pages 「Enforce HTTPS」設定の確認 (新規追加)

ブラウザで以下を確認:

1. https://github.com/fukuokacolor-web/fukuoka-golf-guide/settings/pages にアクセス
2. **「Enforce HTTPS」** チェックボックスが ✅ になっていることを確認
3. もし無効なら **Phase 2 (http→https 化) の前に有効化する**

ユーザーに「Enforce HTTPS が有効ですか？」と質問し確認を取る。

### 2-3. 旧URL の埋め込み箇所を全件抽出

**v1 から変更**: `*.py` を追加 (generate_course_v2.py に5箇所あるため)

```bash
echo "=== 旧URL: fukuokacolor-web.github.io ==="
# 本ランブック (claude-code-domain-migration.md) は除外して計測
grep -rn "fukuokacolor-web\.github\.io" \
  --include="*.html" --include="*.xml" --include="*.txt" \
  --include="*.md" --include="*.json" --include="*.js" \
  --include="*.css" --include="*.py" \
  --exclude="claude-code-domain-migration.md" \
  -- . | tee /tmp/old-url-occurrences.txt

echo ""
echo "=== 件数サマリ (ランブック自身は除外) ==="
echo "総出現数: $(wc -l < /tmp/old-url-occurrences.txt) 件 (期待値: 約 622)"
echo "対象ファイル数: $(awk -F: '{print $1}' /tmp/old-url-occurrences.txt | sort -u | wc -l) 件 (期待値: 80)"
```

### 2-4. GA4 タグの存在確認 (編集禁止対象の特定)

```bash
echo "=== GA4 関連タグ (編集禁止対象) ==="
grep -rn -E "(gtag|googletagmanager\.com|G-[A-Z0-9]+)" \
  --include="*.html" --include="*.js" \
  -- . | head -30
```

期待値: `G-PENH0Z4VT7` が約 78ファイルに存在。

### 2-5. 既存メタタグの状況

```bash
# canonical の存在状況
echo "=== canonical タグの有無 ==="
for f in $(find . -maxdepth 2 -name "*.html" -not -path "./.git/*"); do
  if grep -q 'rel="canonical"' "$f"; then
    echo "[OK] $f"
  else
    echo "[NO] $f"
  fi
done | head -50

# OGP の状況
echo ""
echo "=== og:url タグの有無 ==="
for f in $(find . -maxdepth 2 -name "*.html" -not -path "./.git/*"); do
  if grep -q 'property="og:url"' "$f"; then
    echo "[OK] $f"
  else
    echo "[NO] $f"
  fi
done | head -50
```

期待値: og:url は約 75ファイルに存在 (4ファイルは未設定 → Phase 4 で追加検討)。

### Phase 0 完了報告

ユーザーに以下を報告してから次の Phase へ進む:
- HTML ファイル総数 (期待: 79)
- 旧URL の出現件数 (期待: 622)
- 「Enforce HTTPS」の状態 (有効/無効)
- CNAME の状態 (不在を確認 → Phase 1 でブランチ作成 → Phase 0.5 で CNAME 作成 の順)
- GA4 タグが存在するファイル数 (編集禁止リストとして共有)
- canonical / og:url の現状

**ユーザーの「次へ進んで」の確認を待つこと。**

---

## 3. Phase 1 (順序変更): 作業ブランチ作成 ← 先に切る

**v2.1 で Phase 1 を先に実行する順序に変更**。理由: Phase 0.5 で行う CNAME コミットを main ではなく feature ブランチに乗せるため。

```bash
git status
# クリーンでない場合はユーザーに確認

git checkout main
git pull origin main
git checkout -b feature/domain-migration
git status
```

完了後、ユーザーに「ブランチを切りました。Phase 0.5 に進みます」と報告。

---

## 4. Phase 0.5: CNAME ファイル作成 + GitHub Pages 設定確認 (Phase 1 後に実行)

### 4-1. CNAME ファイルの作成

```bash
# CNAME 不在を再確認
ls -la CNAME 2>/dev/null && echo "ALREADY EXISTS" || echo "CREATING..."

# 末尾改行付きで作成 (GitHub Pages の UI が出力する形式に揃える)
printf "fukuoka-golf-guide.com\n" > CNAME

# 確認
cat CNAME
wc -c CNAME  # 期待: 23 文字 (URL 22 文字 + 改行 1)
```

### 4-2. GitHub Pages 側の設定確認

**ユーザーに依頼**:

1. https://github.com/fukuokacolor-web/fukuoka-golf-guide/settings/pages にアクセス
2. 「Custom domain」欄に `fukuoka-golf-guide.com` を入力 → Save
3. DNS 確認後、**「Enforce HTTPS」** にチェック
4. SSL 証明書プロビジョニング待ち (数分〜最大1時間)

### 4-3. CNAME のコミット (feature ブランチ上に乗る)

```bash
# 現在のブランチが feature/domain-migration であることを確認
git branch --show-current  # 期待: feature/domain-migration

git add CNAME
git commit -m "feat: add CNAME for custom domain fukuoka-golf-guide.com"
```

ユーザー確認 → Phase 2 へ。

---

## 5. Phase 2: 旧URL の一括置換

### 5-1. 置換ルール (厳守)

| 元のパターン | 置換後 | 理由 |
|---|---|---|
| `https://fukuokacolor-web.github.io/fukuoka-golf-guide` | `https://fukuoka-golf-guide.com` | 絶対URL の新ドメイン化 |
| `http://fukuokacolor-web.github.io/fukuoka-golf-guide` | `https://fukuoka-golf-guide.com` | http → https 化込み |
| `fukuokacolor-web.github.io/fukuoka-golf-guide` (スキームなし) | `fukuoka-golf-guide.com` | プロトコル相対 / プレーンテキストパターン |

### 5-2. 内部リンクのルート相対化 (任意)

**判断基準**:
- 既存リンクが `https://fukuoka-golf-guide.com/area-fukuokacity.html` 形式 → そのまま (絶対URL維持)
- 既存リンクが `/fukuoka-golf-guide/area-fukuokacity.html` 形式 → `/area-fukuokacity.html` に短縮

**本リポジトリでは絶対URL形式が主流のため、ルート相対化は今回スキップする (将来 Phase 2 で対応)**

### 5-3. 実行手順

```bash
# 対象ファイル一覧をユーザーに提示 (承認待ち)
awk -F: '{print $1}' /tmp/old-url-occurrences.txt | sort -u

# ユーザー承認後、一括置換を実行
# v2: *.py を追加 (generate_course_v2.py 対応)
# v2.1: 本ランブック自身を除外 (-not -name "claude-code-domain-migration.md")
find . -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" \
  -o -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -not -path "./node_modules/*" -not -path "./.git/*" \
  -not -name "claude-code-domain-migration.md" \
  -exec perl -i -pe 's|https?://fukuokacolor-web\.github\.io/fukuoka-golf-guide|https://fukuoka-golf-guide.com|g' {} +

find . -type f \( -name "*.html" -o -name "*.xml" -o -name "*.txt" \
  -o -name "*.md" -o -name "*.json" -o -name "*.py" \) \
  -not -path "./node_modules/*" -not -path "./.git/*" \
  -not -name "claude-code-domain-migration.md" \
  -exec perl -i -pe 's|fukuokacolor-web\.github\.io/fukuoka-golf-guide|fukuoka-golf-guide.com|g' {} +
```

### 5-4. 検証

```bash
# 置換漏れの確認 (0件であるべき・ランブック自身は除外)
echo "=== 置換漏れチェック (0件であるべき) ==="
grep -rn "fukuokacolor-web\.github\.io" \
  --include="*.html" --include="*.xml" --include="*.txt" \
  --include="*.md" --include="*.json" --include="*.py" \
  --exclude="claude-code-domain-migration.md" \
  -- . | grep -v "^.git/" || echo "OK: 旧URLは全て置換されました"

# 新URL が正しく入っているか確認
echo ""
echo "=== 新URL 出現箇所サンプル ==="
grep -rn "fukuoka-golf-guide\.com" \
  --include="*.html" \
  -- . | head -10
```

### 5-5. コミット

```bash
git add -A
git status
# ユーザーに差分確認を促す: git diff --cached --stat

git commit -m "fix: replace old GitHub Pages URLs with new custom domain

- Replace https://fukuokacolor-web.github.io/fukuoka-golf-guide with https://fukuoka-golf-guide.com
- Apply across HTML, XML, JSON, MD, PY files (622 occurrences in 80 files)
- GA4 tags untouched"
```

ユーザーに「Phase 2 完了。Phase 3 に進みます」と報告し、確認を待つ。

---

## 6. Phase 3: Canonical タグの整備

### 6-1. 方針

- 各 HTML の `<head>` 内に self-canonical を1つだけ置く
- 既存の canonical があれば**新ドメインに更新** (Phase 2 で済んでいるはずだが念のため正規化)
- なければ**新規挿入**
- 言語別ページ (現状は同一 HTML) は **JS タブ切替なので canonical は1つで十分** (Phase 2 で言語別URL化したら hreflang を別途整備)
- **複数 canonical を検出した場合は警告を出力** (実害があるため)

### 6-2. canonical 自動挿入スクリプト

`scripts/update_canonical.py` を作成:

```python
#!/usr/bin/env python
"""
全 HTML ファイルに canonical タグを挿入/更新する。
- 既存の canonical があれば新ドメインの値で上書き (1個目のみ)
- 複数 canonical を検出したら警告
- なければ </head> 直前に挿入
- ルート相対パス (/foo.html) から canonical URL を組み立てる
"""
import re
import sys
from pathlib import Path

DOMAIN = "https://fukuoka-golf-guide.com"

# 除外ディレクトリ
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# canonical 不要なテンプレート/ユーティリティHTML
# ※ 404.html は独自に canonical を持つため除外しない (現状維持)
EXCLUDE_FILES = {"seo-meta.html", "menu-multilang.html"}

def build_canonical(html_path: Path, root: Path) -> str:
    """HTML ファイルのパスから canonical URL を作る"""
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    # サブディレクトリ内 index.html (本リポジトリでは該当なしだが念のため)
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
        return f"{DOMAIN}/{rel}"
    return f"{DOMAIN}/{rel}"

def update_html(html_path: Path, root: Path) -> str:
    text = html_path.read_text(encoding="utf-8")
    canonical_url = build_canonical(html_path, root)
    new_tag = f'<link rel="canonical" href="{canonical_url}" />'

    canonical_re = re.compile(
        r'<link[^>]*\brel=["\']canonical["\'][^>]*/?>',
        re.IGNORECASE,
    )

    matches = canonical_re.findall(text)
    if len(matches) > 1:
        print(f"WARNING: {html_path} has {len(matches)} canonical tags (only first will be replaced)")

    if matches:
        new_text = canonical_re.sub(new_tag, text, count=1)
        action = "UPDATED"
    else:
        if "</head>" in text:
            new_text = text.replace("</head>", f"  {new_tag}\n</head>", 1)
            action = "INSERTED"
        else:
            return f"SKIP (no </head>): {html_path}"

    if new_text != text:
        html_path.write_text(new_text, encoding="utf-8")
    return f"{action}: {html_path} -> {canonical_url}"

def iter_html_files(root: Path):
    for path in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in path.parts):
            continue
        if path.name in EXCLUDE_FILES:
            continue
        yield path

def main():
    root = Path(".").resolve()
    count = {"UPDATED": 0, "INSERTED": 0, "SKIP": 0}
    for html in iter_html_files(root):
        result = update_html(html, root)
        print(result)
        for k in count:
            if result.startswith(k):
                count[k] += 1
    print()
    print(f"Summary: UPDATED={count['UPDATED']}, INSERTED={count['INSERTED']}, SKIP={count['SKIP']}")

if __name__ == "__main__":
    main()
```

### 6-3. 実行と検証

```bash
mkdir -p scripts
# 上記スクリプトを scripts/update_canonical.py に保存

# v2: python (NOT python3) を使う
python scripts/update_canonical.py

# 検証: 全 HTML に canonical があるか
echo "=== canonical 不在ファイル (0件であるべき・除外ファイル除く) ==="
for f in $(find . -maxdepth 2 -name "*.html" -not -path "./.git/*"); do
  case "$(basename "$f")" in
    seo-meta.html|menu-multilang.html) continue ;;
  esac
  if ! grep -q 'rel="canonical"' "$f"; then
    echo "MISSING: $f"
  fi
done | head -20
```

### 6-4. コミット

```bash
git add scripts/update_canonical.py
git add -A "*.html"
git commit -m "feat: add/update canonical tags to all HTML pages

- Self-canonical pointing to https://fukuoka-golf-guide.com/<path>
- Inserts before </head> if missing, replaces existing tag otherwise
- Warns on multiple canonical tags
- Excludes seo-meta.html and menu-multilang.html (templates)
- Script: scripts/update_canonical.py"
```

ユーザー確認 → Phase 4 へ。

---

## 7. Phase 4: OGP (og:url, og:image) と Twitter Card の更新

### 7-1. 方針

- `og:url` は canonical と同じ URL にする
- `og:image` が**相対 URL** または**旧ドメイン**だったら、新ドメイン絶対 URL に変換
- `og:site_name` などの他の OGP は触らない
- Twitter Card の `twitter:url`, `twitter:image` も同様に処理
- **属性順序の両方 (`property=...content=...` と `content=...property=...`) に対応**

### 7-2. 実行スクリプト

`scripts/update_ogp.py`:

```python
#!/usr/bin/env python
"""og:url, og:image, twitter:url, twitter:image を新ドメイン基準で正規化する。
属性順序の両方 (property→content / content→property) に対応。"""
import re
from pathlib import Path
from urllib.parse import urljoin

DOMAIN = "https://fukuoka-golf-guide.com"
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# OGP 不要なテンプレート/ユーティリティHTML
# ※ 404.html は独自の OGP を持つため除外しない
EXCLUDE_FILES = {"seo-meta.html", "menu-multilang.html"}

def page_url(html_path: Path, root: Path) -> str:
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{rel}"

def normalize_image_url(value: str) -> str:
    """og:image を絶対URL に正規化"""
    if value.startswith(("http://", "https://")):
        # 旧ドメインなら新ドメインに (Phase 2 で済んでいるはずだが冪等性確保)
        return value.replace("http://fukuoka-golf-guide.com", DOMAIN) \
                    .replace("https://fukuoka-golf-guide.com", DOMAIN)
    # 相対 URL → 絶対 URL
    return urljoin(DOMAIN + "/", value.lstrip("/"))

def replace_meta_url(text: str, attr_kind: str, attr_name: str, new_value: str) -> str:
    """
    <meta {attr_kind}="{attr_name}" content="..."> または
    <meta content="..." {attr_kind}="{attr_name}"> の content を new_value で置換。
    attr_kind: 'property' (OGP) または 'name' (Twitter)
    """
    # パターンA: attr_kind が先, content が後
    pattern_a = (
        rf'(<meta[^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*\bcontent=["\'])'
        r'([^"\']*)'
        r'(["\'][^>]*/?>)'
    )
    text = re.sub(pattern_a, lambda m: f'{m.group(1)}{new_value}{m.group(3)}', text, flags=re.IGNORECASE)

    # パターンB: content が先, attr_kind が後
    pattern_b = (
        r'(<meta[^>]*\bcontent=["\'])'
        r'([^"\']*)'
        rf'(["\'][^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*/?>)'
    )
    text = re.sub(pattern_b, lambda m: f'{m.group(1)}{new_value}{m.group(3)}', text, flags=re.IGNORECASE)

    return text

def replace_meta_image(text: str, attr_kind: str, attr_name: str) -> str:
    """og:image / twitter:image の値を絶対URL に正規化"""
    pattern_a = (
        rf'(<meta[^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*\bcontent=["\'])'
        r'([^"\']+)'
        r'(["\'][^>]*/?>)'
    )
    text = re.sub(pattern_a, lambda m: f'{m.group(1)}{normalize_image_url(m.group(2))}{m.group(3)}', text, flags=re.IGNORECASE)
    pattern_b = (
        r'(<meta[^>]*\bcontent=["\'])'
        r'([^"\']+)'
        rf'(["\'][^>]*\b{attr_kind}=["\']' + re.escape(attr_name) + r'["\'][^>]*/?>)'
    )
    text = re.sub(pattern_b, lambda m: f'{m.group(1)}{normalize_image_url(m.group(2))}{m.group(3)}', text, flags=re.IGNORECASE)
    return text

def update_ogp(html_path: Path, root: Path):
    text = html_path.read_text(encoding="utf-8")
    original = text
    page = page_url(html_path, root)

    # og:url, twitter:url を canonical と同じURLに
    text = replace_meta_url(text, "property", "og:url", page)
    text = replace_meta_url(text, "name", "twitter:url", page)

    # og:image, twitter:image を絶対URLに正規化
    text = replace_meta_image(text, "property", "og:image")
    text = replace_meta_image(text, "name", "twitter:image")

    if text != original:
        html_path.write_text(text, encoding="utf-8")
        print(f"UPDATED: {html_path}")
    else:
        print(f"NOCHANGE: {html_path}")

def main():
    root = Path(".").resolve()
    for html in root.rglob("*.html"):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue
        if html.name in EXCLUDE_FILES:
            continue
        update_ogp(html, root)

if __name__ == "__main__":
    main()
```

### 7-3. 実行とコミット

```bash
mkdir -p scripts  # Phase 3 で作成済みのはずだが冪等性確保
python scripts/update_ogp.py

# 検証
echo "=== og:url サンプル ==="
grep -rn 'og:url' --include="*.html" -- . | head -5
echo ""
echo "=== og:image 旧ドメイン残存チェック (0件であるべき) ==="
grep -rEn 'og:image[^>]*fukuokacolor-web' --include="*.html" -- . || echo "OK"
echo ""
echo "=== og:image 相対URL 残存チェック (0件であるべき) ==="
grep -rEn 'property=["\x27]og:image["\x27][^>]*content=["\x27]/' \
  --include="*.html" -- . | head -10 || echo "OK"

git add scripts/update_ogp.py
git add -A "*.html"
git commit -m "feat: normalize OGP and Twitter Card URLs to new domain

- og:url, twitter:url match canonical URL per page
- og:image, twitter:image normalized to absolute URLs on new domain
- Handles both attribute orders (property→content / content→property)"
```

ユーザー確認 → Phase 5 へ。

---

## 8. Phase 5: JSON-LD (構造化データ) の URL 検証

### 8-1. 方針

- Phase 2 の Perl 一括置換で `<script type="application/ld+json">` 内の旧URL も置換済みのはず
- 念のため**grep ベースの 0件確認**を行う (v1 の目視検証から格上げ)
- 残っていれば手動修正

### 8-2. 実行

```bash
echo "=== JSON-LD ブロック数 (期待: 117ブロック / 74ファイル) ==="
grep -rn 'application/ld+json' --include="*.html" -- . | wc -l

echo ""
echo "=== JSON-LD 内の旧URL 残存チェック (0件であるべき) ==="
# 各HTMLの JSON-LD ブロックを抽出して旧URLを探す
for f in $(find . -maxdepth 2 -name "*.html" -not -path "./.git/*"); do
  python -c "
import re, sys
text = open('$f', encoding='utf-8').read()
for m in re.finditer(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', text, re.DOTALL | re.IGNORECASE):
    if 'fukuokacolor-web' in m.group(1):
        print(f'FOUND in $f')
        break
"
done | head -20

# シンプル版 (補助確認)
echo ""
echo "=== HTML 全体の旧URL 残存チェック (0件であるべき) ==="
grep -rn "fukuokacolor-web" --include="*.html" -- . || echo "OK: 全HTMLから旧URL消滅"
```

残っていれば手動修正、なければそのまま Phase 6 へ。コミットは不要 (Phase 2 に含まれている)。

---

## 9. Phase 6: sitemap.xml の更新 (priority 0.9 と既存 lastmod を保持)

### 9-1. 既存 sitemap の確認

```bash
ls -la sitemap*.xml 2>/dev/null
wc -l sitemap.xml
grep -c "<loc>" sitemap.xml  # 期待: 76エントリ
grep -c "priority>0\.9" sitemap.xml  # 期待: 6エントリ
```

### 9-2. 自動生成スクリプト (priority と lastmod 継承対応)

`scripts/generate_sitemap.py`:

```python
#!/usr/bin/env python
"""リポジトリ内の HTML ファイルから sitemap.xml を生成する。
- priority 0.9 の重要ページを HIGH_PRIORITY_PAGES で指定
- 既存 sitemap.xml から lastmod を継承 (新規HTMLは今日付)
"""
import datetime
import re
from pathlib import Path

DOMAIN = "https://fukuoka-golf-guide.com"
OLD_DOMAIN = "https://fukuokacolor-web.github.io/fukuoka-golf-guide"
EXCLUDE_DIRS = {".git", "node_modules", "scripts", ".github"}
# sitemap 非収録: 404 ページとテンプレート/ユーティリティHTML
# ※ canonical/OGP スクリプトとは EXCLUDE_FILES が異なる (意図的)
EXCLUDE_FILES = {"404.html", "seo-meta.html", "menu-multilang.html"}

# v2 新規: 重要ページは priority 0.9 を維持
HIGH_PRIORITY_PAGES = {
    "airport-access-top5.html",
    "area-kitakyushu.html",
    "area-itoshima.html",
    "area-chikugo.html",
    "area-fukuokacity.html",
    "course-kokura.html",
}

def page_url(html_path: Path, root: Path) -> str:
    rel = html_path.relative_to(root).as_posix()
    if rel == "index.html":
        return f"{DOMAIN}/"
    return f"{DOMAIN}/{rel}"

def load_existing_lastmods(sitemap_path: Path) -> dict:
    """既存 sitemap.xml から URL → lastmod のマップを作る。
    `<url>...</url>` ブロック単位で抽出するため、要素間に他のタグ
    (<priority>, <changefreq> など) が挟まっても正しく動作する。
    """
    if not sitemap_path.exists():
        return {}
    text = sitemap_path.read_text(encoding="utf-8")
    result = {}
    # <url>...</url> ブロックを取り出して、各ブロック内で <loc> と <lastmod> を独立に探す
    for url_block in re.findall(r'<url>(.*?)</url>', text, re.DOTALL):
        loc_match = re.search(r'<loc>([^<]+)</loc>', url_block)
        lastmod_match = re.search(r'<lastmod>([^<]+)</lastmod>', url_block)
        if loc_match and lastmod_match:
            # 旧ドメイン → 新ドメインへ正規化
            normalized = loc_match.group(1).replace(OLD_DOMAIN, DOMAIN)
            result[normalized] = lastmod_match.group(1)
    return result

def main():
    root = Path(".").resolve()
    today = datetime.date.today().isoformat()
    sitemap_path = Path("sitemap.xml")
    existing_lastmods = load_existing_lastmods(sitemap_path)

    urls = []
    for html in sorted(root.rglob("*.html")):
        if any(part in EXCLUDE_DIRS for part in html.parts):
            continue
        if html.name in EXCLUDE_FILES:
            continue
        urls.append((page_url(html, root), html.name))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>']
    lines.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    for url, fname in urls:
        # priority: top=1.0, 重要ページ=0.9, 通常=0.7
        if url == f"{DOMAIN}/":
            priority = "1.0"
        elif fname in HIGH_PRIORITY_PAGES:
            priority = "0.9"
        else:
            priority = "0.7"

        # lastmod: 既存値を継承、なければ今日付
        lastmod = existing_lastmods.get(url, today)

        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append(f"    <lastmod>{lastmod}</lastmod>")
        lines.append(f"    <changefreq>weekly</changefreq>")
        lines.append(f"    <priority>{priority}</priority>")
        lines.append("  </url>")
    lines.append("</urlset>")

    Path("sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Generated sitemap.xml with {len(urls)} URLs")
    print(f"  - High priority (0.9): {sum(1 for _, n in urls if n in HIGH_PRIORITY_PAGES)}")
    print(f"  - Top (1.0): 1")
    print(f"  - Lastmod inherited: {sum(1 for u, _ in urls if u in existing_lastmods)}")
    print(f"  - Lastmod new (today): {sum(1 for u, _ in urls if u not in existing_lastmods)}")

if __name__ == "__main__":
    main()
```

### 9-3. 実行とコミット

```bash
mkdir -p scripts  # Phase 3 で作成済みのはずだが冪等性確保
python scripts/generate_sitemap.py

# 検証
head -20 sitemap.xml
echo ""
echo "=== priority 0.9 エントリ数 (期待: 6) ==="
grep -c "priority>0\.9" sitemap.xml

echo ""
echo "=== lastmod 継承確認 ==="
grep -E "(area-kitakyushu|area-fukuokacity|course-kokura)" sitemap.xml -A 1 | head -20

git add scripts/generate_sitemap.py sitemap.xml
git commit -m "chore: regenerate sitemap.xml with new domain URLs

- Preserves lastmod from previous sitemap (no false 'all updated' signal)
- Maintains priority 0.9 for area guides + airport-access-top5 + course-kokura
- Adds <changefreq>weekly</changefreq> and <priority> to all URLs (was sparse before)
- Excludes 404.html, seo-meta.html, menu-multilang.html"
```

ユーザー確認 → Phase 7 へ。

---

## 10. Phase 7: robots.txt の更新

### 10-1. 既存確認

```bash
cat robots.txt
# 期待: Sitemap が旧ドメインのまま残っているはず
```

### 10-2. 新規作成 / 更新

```bash
cat > robots.txt <<'EOF'
User-agent: *
Allow: /

Sitemap: https://fukuoka-golf-guide.com/sitemap.xml
EOF

cat robots.txt

git add robots.txt
git commit -m "chore: update robots.txt with new sitemap URL"
```

ユーザー確認 → Phase 8 へ。

---

## 11. Phase 8: GA4 タグの動作確認 (編集禁止)

### 11-1. 編集が入っていないことを確認

```bash
echo "=== GA4 タグの最終確認 ==="
grep -rn -E "(gtag\(|googletagmanager\.com|G-PENH0Z4VT7)" \
  --include="*.html" --include="*.js" -- . | head -20

echo ""
echo "=== GA4 ID が変わっていないか ==="
COUNT=$(grep -rln "G-PENH0Z4VT7" --include="*.html" -- . | wc -l)
echo "G-PENH0Z4VT7 出現ファイル数: $COUNT (期待: 約78)"
```

### 11-2. ユーザーに以下を伝える

> GA4 タグは Phase 0 の調査時点と完全に同じ状態を維持しています。
> ただし、ドメイン変更後は **GA4 管理画面側で**以下の作業が必要です (これは Claude Code の作業範囲外):
> 1. GA4 管理画面 → 管理 → データストリーム → 既存ストリームを確認
> 2. 「ウェブストリームの URL」を `https://fukuoka-golf-guide.com` に更新 (必要なら)
> 3. リアルタイムレポートで新ドメインからの計測が来ているか確認

---

## 12. Phase 9: 404 ページの整備 (任意・既存維持)

### 12-1. 既存 404.html の確認

```bash
ls -la 404.html
echo ""
echo "=== 404.html 内の旧URL 残存チェック (0件であるべき) ==="
grep -n "fukuokacolor-web" 404.html || echo "OK: 404.html は新ドメインに更新済み"
```

Phase 2 で対処済み。修正不要。

---

## 13. Phase 10: 最終検証

### 13-1. ローカル動作確認

```bash
# v2: python (NOT python3) を使う
python -m http.server 8000 &
SERVER_PID=$!
sleep 2

# トップページ確認
curl -sI http://localhost:8000/ | head -5

# 主要ページが200を返すか
for page in index.html area-fukuokacity.html area-itoshima.html area-kitakyushu.html area-chikugo.html fees.html access.html; do
  if [ -f "$page" ]; then
    code=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:8000/$page")
    echo "[$code] /$page"
  fi
done

# サイトマップ確認
curl -s http://localhost:8000/sitemap.xml | head -20

# robots 確認
curl -s http://localhost:8000/robots.txt

# サーバー停止 (v2: Windows用 taskkill)
# Git Bash 上では taskkill のスラッシュは // でエスケープ
taskkill //F //PID $SERVER_PID 2>/dev/null || kill $SERVER_PID 2>/dev/null
```

### 13-2. 内部リンクチェック

```bash
# HTML 内の壊れた絶対 URL 検出 (ランブック自身は除外)
echo "=== 旧ドメイン残存最終チェック (0件であるべき) ==="
grep -rn "fukuokacolor-web\.github\.io" \
  --include="*.html" --include="*.xml" --include="*.txt" \
  --include="*.md" --include="*.json" --include="*.py" \
  --exclude="claude-code-domain-migration.md" \
  -- . || echo "OK"

# 新ドメインの出現確認
echo ""
echo "=== 新ドメイン出現数 (参考値: 622+ canonical/OGP/sitemap 追加分) ==="
echo "    (Phase 3-7 で canonical, og:url, og:image, twitter:url, twitter:image, sitemap, robots を追加・更新するため、622 を超えて当然)"
grep -rn "fukuoka-golf-guide\.com" \
  --include="*.html" --include="*.xml" --include="*.txt" \
  --include="*.md" --include="*.json" --include="*.py" \
  --exclude="claude-code-domain-migration.md" \
  -- . | wc -l
```

### 13-3. 主要メタタグの抽出 (目視確認用)

```bash
# index.html の重要タグ
echo "=== index.html の主要メタタグ ==="
grep -E '(canonical|og:url|og:image|twitter:url)' index.html

# 任意のサブページ
echo ""
echo "=== area-fukuokacity.html のメタタグ ==="
grep -E '(canonical|og:url|og:image|twitter:url)' area-fukuokacity.html 2>/dev/null
```

---

## 14. Phase 11: プッシュと PR (直接マージ禁止)

### 14-1. 差分サマリ確認

```bash
git log --oneline main..feature/domain-migration
git diff --stat main..feature/domain-migration
```

### 14-2. プッシュ

```bash
git push -u origin feature/domain-migration
```

### 14-3. **PR 作成 (必須)**

v1 では「PR か直接マージ」を選択肢としていたが、v2 では**PR必須**。
変更ファイル数が80+のためレビュー・ロールバックの観点で PR 経由とする。

```bash
gh pr create --title "Domain migration: github.io → fukuoka-golf-guide.com" --body "$(cat <<'EOF'
## Summary
- Migrate site from `https://fukuokacolor-web.github.io/fukuoka-golf-guide/` to `https://fukuoka-golf-guide.com`
- Replace 622 old URL occurrences across 80 files
- Add CNAME, update canonical/OGP/sitemap/robots
- GA4 tags untouched

## Changes
- `CNAME` (new): custom domain marker
- `*.html` (79 files): URL replacement, canonical, OGP normalization
- `sitemap.xml`: regenerated, lastmod preserved, priority 0.9 maintained for 6 pages
- `robots.txt`: new sitemap URL
- `generate_course_v2.py`: hardcoded URLs replaced
- `scripts/update_canonical.py` (new)
- `scripts/update_ogp.py` (new)
- `scripts/generate_sitemap.py` (new)

## Test plan
- [x] Local server: all main pages return 200
- [x] Old URL grep: 0 hits across all tracked files
- [x] GA4 tags: unchanged (G-PENH0Z4VT7 still in ~78 files)
- [x] Priority 0.9 sitemap entries: 6 maintained
- [ ] Post-merge: verify https://fukuoka-golf-guide.com/ serves correctly
- [ ] Post-merge: verify https://fukuokacolor-web.github.io/fukuoka-golf-guide/ → 301 redirect

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### 14-4. ユーザーに以下を報告

- PR URL
- 変更ファイル数・追加スクリプト一覧
- マージ後の GitHub Pages デプロイ完了まで待つ目安 (数分)
- マージ後に確認すべき項目 (Phase 11.5)

---

## 15. Phase 11.5 (新規追加): マージ後の検証

PR がマージされ、GitHub Pages のデプロイが完了したら以下を確認:

### 15-1. 新ドメインで動作するか

```bash
# トップ
curl -sI https://fukuoka-golf-guide.com/ | head -5
# Expected: HTTP/2 200

# サブページ
curl -sI https://fukuoka-golf-guide.com/area-fukuokacity.html | head -5
# Expected: HTTP/2 200
```

### 15-2. 旧 URL から自動 301 リダイレクト (GitHub Pages 機能)

```bash
# 旧URL → 新URL への 301 自動リダイレクト確認
curl -sI https://fukuokacolor-web.github.io/fukuoka-golf-guide/ | head -5
# Expected: HTTP/2 301
# Expected: Location: https://fukuoka-golf-guide.com/

curl -sI https://fukuokacolor-web.github.io/fukuoka-golf-guide/area-fukuokacity.html | head -5
# Expected: HTTP/2 301
# Expected: Location: https://fukuoka-golf-guide.com/area-fukuokacity.html
```

**重要**: GitHub Pages は CNAME 設定後、旧サブパス URL から新カスタムドメインへ**サーバー側で自動的に 301 リダイレクト**を返します。これは Google が「サイト移転」シグナルとして正規に扱うため、メタリフレッシュ等のフォールバックは**不要**です。

### 15-3. 新サイトの SEO チェック

- https://search.google.com/test/rich-results で構造化データを検証
- https://www.google.com/search?q=site:fukuoka-golf-guide.com で初期インデックスを確認

---

## 16. デプロイ後にユーザーが手動でやること

Claude Code の作業範囲外。

### 16-1. Google Search Console
1. 新プロパティ `https://fukuoka-golf-guide.com` を追加
2. 所有権確認 (HTML タグ確認 or DNS TXT 確認)
3. `sitemap.xml` を送信
4. **旧プロパティ** (`fukuokacolor-web.github.io/fukuoka-golf-guide`) で「アドレス変更」ツールは使わない (GitHub Pages のサブパスからのドメイン移行は対象外のため、新プロパティで地道にインデックス再構築)
5. ただし GitHub Pages の自動 301 が効いているため、Google は数週間で被リンク・インデックスを新ドメインへ引き継いでくれる

### 16-2. Google Analytics 4
1. 管理 → データストリーム → ウェブストリームを確認
2. URL が新ドメインに更新されているか確認
3. リアルタイムで自分の閲覧が計測されるかテスト

### 16-3. 外部サービス・ツール
- A8.net、バリューコマースなどの ASP に登録している場合、サイト URL を新ドメインに更新申請
- SNS のプロフィール欄リンク差し替え
- 名刺・印刷物などの URL 更新 (必要に応じて)

### 16-4. GitHub Pages 側
- Settings → Pages の「Custom domain」が `fukuoka-golf-guide.com` になっていることを再確認
- 「Enforce HTTPS」が ✅ 状態であることを再確認
- DNS の伝搬完了 (`dig fukuoka-golf-guide.com` で 185.199.108.153 〜 111.153 のいずれかが返る)

---

## 17. ロールバック手順 (緊急時)

何か問題が起きた場合:

```bash
# 直前のコミットに戻す
git reset --soft HEAD~1   # 変更は残してコミットだけ取り消し

# Phase 単位で巻き戻す
git log --oneline feature/domain-migration
git reset --hard <戻したいコミットハッシュ>   # ⚠️ 変更が消える。ユーザー確認必須

# ブランチごと破棄して main に戻る
git checkout main
git branch -D feature/domain-migration

# 緊急時: PR がマージ済みで切り戻したい場合
# → main を1つ前のコミットに戻す revert PR を作る (force push 厳禁)
git checkout main
git revert <マージコミット>
git push origin main
```

---

## 18. チェックリスト (完了確認)

- [ ] Phase 0: 現状調査完了、レポート提出 (HTML 79 / 旧URL 約622 / GA4 ID 確認 / Enforce HTTPS 確認 / CNAME 不在確認)
- [ ] Phase 1: ブランチ `feature/domain-migration` 作成 ← **v2.1で順序前倒し**
- [ ] Phase 0.5: CNAME ファイル作成 (feature ブランチ上にコミット)、GitHub Pages Custom Domain 設定 ← **新規**
- [ ] Phase 2: 旧 URL 置換 (HTML/XML/JSON/MD/PY、ランブック自身は除外)、置換漏れ 0件
- [ ] Phase 3: 全 HTML に canonical タグ
- [ ] Phase 4: og:url, twitter:url, og:image, twitter:image 正規化 (両属性順対応)
- [ ] Phase 5: JSON-LD 内の旧 URL なし (grep 0件確認)
- [ ] Phase 6: sitemap.xml 再生成 (priority 0.9 維持、lastmod 継承)
- [ ] Phase 7: robots.txt 更新
- [ ] Phase 8: GA4 タグ無傷確認
- [ ] Phase 9: 404 ページ確認
- [ ] Phase 10: 最終検証 (ローカル動作・残存チェック)
- [ ] Phase 11: プッシュ + **PR 作成** (直接マージ禁止)
- [ ] Phase 11.5: マージ後の新ドメイン動作確認 + 自動 301 確認 ← **新規**

---

## 19. 補足: このドキュメントで対象外のこと

以下は別の指示書で扱うため、今回は**実装しない**:

- 言語別 URL 構造への分離 (`/ja/` `/en/` `/ko/`)
- hreflang タグの再構築 (現状は `#en`/`#ko` フラグメント形式で SEO 上機能していないが、ドメイン移行とは別件)
- 旧 URL からのメタリフレッシュ・リダイレクト (GitHub Pages の自動 301 が効くため不要)
- GolfCourse / LocalBusiness の構造化データ追加
- WebP 化や画像最適化
- Cloudflare などの CDN 導入

これらは **Phase 2 (言語別 URL 化) 指示書**で別途処理する。

---

## 20. レビューで棄却された改修案 (記録用)

レビューで提案されたが、検証の結果**不要と判断**した項目:

| 提案 | 棄却理由 |
|------|---------|
| メタリフレッシュ・フォールバック (旧 URL に `<meta http-equiv="refresh">` を埋め込む) | GitHub Pages はカスタムドメイン設定時に旧サブパス URL → 新カスタムドメインへ**サーバー側で自動 301 リダイレクト**を返す。これは Google が正規の「サイト移転」シグナルとして扱うため、フォールバック不要 |
| og:image / og:url の属性順序リバース対応 (ブロッカー扱い) | 本リポジトリの全 og: タグは `property=...content=...` 順に統一済みを実機確認。スクリプトのバグはあるが今回の移行には影響しないため警告レベル。ただし v2 では将来の汎用性のため両順対応の正規表現に強化済み |
| BeautifulSoup 等のパーサー導入 | 現行リポジトリの HTML は十分機械的で正規表現で安全に処理可能。依存追加のコストの方が大きい |

---

作業開始前にこの指示書全体を通読し、不明点があれば質問すること。
