# プロジェクト運用規約 (CLAUDE.md)

**プロジェクト名**: fukuoka-golf-guide.com
**カテゴリ**: ゴルフ場アフィリエイトサイト (福岡県内 35 コース・3 言語)
**派生元**: blog-template v1.0 (2026-05-10 逆適用)
**現行 Phase**: 観測フェーズ 進行中 (2026-05-10 ~ 2026-06-03・Day 28 で Phase 4 着手判断)

---

## 1. 基本情報

| 項目 | 値 |
|---|---|
| ドメイン | https://fukuoka-golf-guide.com |
| 言語 | ja + en + ko (3 言語切替・全 URL 共通・content.c-{lang} クラスで切替) |
| 収益モデル | A8.net 経由アフィリエイト (じゃらんゴルフ + 楽天 GORA) |
| GA4 ID | **`G-PENH0Z4VT7`** (絶対変更禁止) |
| GA4 プロパティ ID | `531139357` / アカウント ID `389856983` |
| 主要 ASP | A8.net (フリーリンク `4B1D5J+...`) |
| データファイル | `course_data.json` (2,255 行・35 コース・**絶対上書き禁止**) |
| ASP マッピング | `jalan_golf_mapping.json` + `rakuten_gora_mapping.json` |
| 詳細ページ命名 | `course-{slug}.html` (35 件・3 言語 = 105 セクション) |
| アクセスページ | `access-{slug}.html` (35 件・3 言語) |
| 総 HTML | 98 ファイル (2026-05-10 時点) |
| sitemap.xml | 98 URLs / priority 5 階層 (1.0/0.9/0.8/0.7/0.6) |
| GitHub | `fukuokacolor-web/fukuoka-golf-guide` (main ブランチ運用) |

## 2. ディレクトリ規約 — Dual (Option B)

このプロジェクトは **デュアル ディレクトリ規約** を採用:

- **REPO_ROOT**: `C:/Users/Owner/fukuoka-golf-guide` (git repo・本番デプロイ元)
- **PREVIEW_ROOT**: `C:/Users/Owner/Documents/新しいPJ` (launch.json で port 3001・dev server 用コピー)

**運用ルール**:
- 全 mass apply スクリプトは `ROOTS = [REPO_ROOT, PREVIEW_ROOT]` パターンで両方処理 (例: `link_inbound_guide.py` / `generate_sitemap.py`)
- Edit ツールで repo を更新したら preview に手動同期が必要 → **`/dual-dir-sync <pattern>`** skill で強制同期
- Markdown ドキュメント (NEXT_SESSION.md / OBSERVATION_PLAYBOOK.md 等) も両ディレクトリ同期対象
- preview の sitemap.xml / sitemap-ko.xml は dev server の動作確認用・本番デプロイには使わない

## 3. 専門家会議文化 (★ 最重要)

大きな決断の前に **`/expert-meeting <topic>`** で 4-6 名の subagent を招集して議事録を作る。

### 利用可能な専門家 (`~/.claude/agents/`・全プロジェクト共通)

| name | 元ペルソナ | 専門 |
|---|---|---|
| `content-strategist` | 山本誠一 | E-E-A-T・取材ドリブン編集 |
| `seo-strategist` | 田中健太郎 | KW 戦略・トピッククラスタ・GSC |
| `cvr-optimizer` | 佐藤美咲 | CTA 設計・観測・二項検定 |
| `ia-architect` | 鈴木玲奈 | サイト構造・sitemap・hreflang |
| `behavioral-economist` | 教授 | Decoy・選択アーキテクチャ・倫理境界 |
| `fact-checker-primary` | 鈴木一郎 | 公式直確認・1 次調査 |
| `fact-checker-secondary` | 中村麻衣 | 独立検証・反証 |
| `inbound-strategist` | 金星誠 | KO/EN/中・Naver・Influencer |
| `payment-specialist` | David Chen | 国際決済・ASP・通貨換算 |

### 会議運営原則
- 4-6 名招集 (3 名以下は議論薄・7 名以上は意思決定ノイズ)
- ファクトチェックが必要な議題は **primary + secondary 必ずペア**
- 出力は Tier 1-3 で離散化 (全員 ○ で Tier 1)
- 「今日の最初の 1 手」推奨を必ず生成

## 4. 段階実行ワークフロー

新たな改修パターンは **常に段階を踏む**:
1. **1 ファイルでテスト** → 結果スクリーンショット / 数値で確認
2. **ユーザー承認依頼** (即時全件適用しない)
3. **mass apply** (冪等性 + dry-run 対応スクリプト経由)

### mass apply スクリプトの規約
- 冪等 (再実行で同結果・MARKER で重複防止)
- `--dry-run` フラグ必須
- 両ディレクトリ処理 (ROOTS パターン)
- 結果サマリ出力 (replaced / already / no_match / not_found 等)

## 5. dry-run → 承認 → 本番

全 skill / 全スクリプトで **3 段階厳守**:
1. **dry-run**: 内容確認 (件数・差分プレビュー)
2. **ユーザー承認**: 「これで実行しますか?」
3. **本番実行**: 適用

即実行禁止。

## 6. 観測フェーズ規約 (★ 現行進行中)

**観測期間**: 2026-05-10 〜 2026-06-03 (Day 0 〜 Day 28)

- **観測中の HTML 改修禁止** (交絡因子防止)・Phase 1A 逆流ナビ / Phase 1B CTA / Phase 3 価格カード が観測対象
- `OBSERVATION_PLAYBOOK.md` の 5 探索レポート × 事前確定スレッショルドで判定
- Day 7 (5/13) / Day 14 (5/19) / Day 28 (6/3) で **`/observation-checkin <day>`** 実行
- Day 28 当日に「数値見ながらしきい値を動かす」を**絶対禁止** (確証バイアス排除)

### 観測期間中の許容例外
- バグ修正・誤字訂正
- メタファイル (sitemap.xml / robots.txt / structured data) の調整
- 新規ページ追加 (既存ファイル不変・但し観測サンプル加算は警告)
- ドキュメント (Markdown) の追加・更新

## 7. ハルシネーション禁止 (★ 絶対)

事実情報の捏造を絶対に許さない:
- 価格・電話・URL・住所・人物名・実績数値は **公式サイトでクロスチェック**
- AI 生成コンテンツの掲載前に **`fact-checker-primary` + `fact-checker-secondary` のペア検証** (2 ソース原則・3 ソース推奨)
- 確認できなかった項目は「(要追加調査)」と明記・推測で埋めない
- 「たぶん」「常識」「業界周知」を「事実」として書かない

## 8. 倫理境界線

行動経済学的なナッジは「**読者の長期的利益と一致する方向**」のみ:

### ❌ 禁止 (短期 CVR 増・長期 Trust 棄損 + 法規制リスク)
- 「90% が選ぶ」マイクロコピー (実データなし → 景表法・薬機法違反)
- カウントダウンタイマー / 赤字大文字煽り
- dark pattern (default チェック解除困難・購入解除フロー煩雑化)
- 偽装 Experience コンテンツ (覆面体験記等)・**山本案 E-1「覆面ラウンド記」は却下済**
- 機械翻訳をネイティブ翻訳と偽る (Tier 2-3 ポータルの KO/EN は「예약 사이트 (자동번역)」と明示)

### ✅ 推奨 (Trust 蓄積)
- 「キャンセル無料」「公式サイト直リンク」の損失回避訴求
- 実データに基づく社会的証明 (GA4 統計などで裏付け済の場合)
- 実名取材・第三者検証によるコンテンツ (山本案 E「現役プロ・支配人インタビュー 5 本」)
- 透明な手数料・通貨表記

## 9. 禁止事項 (絶対)

1. **GA4 タグ `G-PENH0Z4VT7` を絶対変更しない**
2. **CNAME ファイルを編集しない** (`fukuoka-golf-guide.com`)
3. **公式サイト確認なしでコース情報を追加しない** (ハルシネーション防止)
4. **アフィリ CTA 除外コース** に Jalan/楽天 CTA を載せない (公式のみ):
   - **楽天 GORA 除外** (4件): course-fukuokacc / course-wakamatsu / course-akane / course-genkai
   - **じゃらんゴルフ除外** (4件): course-fukuokacc / course-wakamatsu / course-genkai / course-aburayama
   - 差分: akane は jalan 掲載・aburayama は rakuten 掲載 (個別運用)
5. **本ドキュメント (`CLAUDE.md`) を一括置換 script で書き換えない** (手動 Edit のみ)
6. **`NEXT_SESSION.md` も一括置換禁止** (手動 Edit のみ)
7. **`course_data.json` を絶対上書きしない** (マスタ 2,255 行・破壊事故 2026-05-03)
   - c_id マッピングは別ファイル `rakuten_gora_mapping.json` を使う
   - jalan_id マッピングは別ファイル `jalan_golf_mapping.json`

## 10. メモリ・引き継ぎ・ファイル役割分担

| ファイル | 役割 | 更新頻度 |
|---|---|---|
| `CLAUDE.md` (本ファイル) | プロジェクト運用規約・**静的・timeless** | 規約変更時のみ (年 0-2 回) |
| `NEXT_SESSION.md` | 引き継ぎ正典・最新の Phase 履歴・直近実装ログ | 毎セッション・コミット後 |
| `OBSERVATION_PLAYBOOK.md` | 観測フェーズ判定インフラ・スレッショルド事前確定 | Day 7/14/28 で結果記入 |
| `GA4_DASHBOARD.md` | GA4 計測コード仕様・カスタムディメンション登録手順 | 計測ロジック変更時 |
| `BLOG_COMPANY_PROGRESS.md` | ブログ会社化 Phase 1-4 進捗 | Phase 完了時 |
| `KO_MARKET_RESEARCH.md` | 韓国市場リサーチ (Phase 4-B 準備) | Day 7/14/28 で §1 更新 |
| `INTERVIEW_CANDIDATES.md` + `INTERVIEW_PROTOCOL_DRAFT.md` | 取材候補 5 件 + プロトコル | 取材確定時 |
| `~/.claude/projects/<id>/memory/` | auto memory | 自動 |

## 11. コミット規約

- **コミットメッセージ**: `<type>(<scope>): <subject>` 形式
  - type: `feat` / `fix` / `docs` / `refactor` / `perf` / `test` / `chore`
  - scope: `seo` / `cvr` / `content` / `arch` / `research` / `observation` / `ia` / `inbound` 等
- **HEREDOC で改行・特殊文字を保護**
- **Co-Authored-By: Claude Opus 4.7 <noreply@anthropic.com>** 行を含める
- **--no-verify / --no-gpg-sign 使わない** (規約違反)
- **新規 commit 優先**・amend は published commit に対して厳禁
- **コミット粒度**: Phase 完了・機能完成・修正完了の単位 (中間状態を残さない)

## 12. リスクと事故防止 (過去の教訓)

| 日付 | 事故 | 教訓 |
|---|---|---|
| 2026-05-03 | `course_data.json` を一括 script で上書き・マスタデータ破壊 | マスタは read only・c_id 等のマッピングは別ファイル化 |
| (継続) | 観測中の HTML 改修で計測指標が交絡 | Day 0 から `OBSERVATION_PLAYBOOK.md` で改修禁止期間を明示 |
| (継続) | ChatGPT 量産記事の薄さで E-E-A-T 評価毀損 | 取材ドリブン・実名 + 一次資料 (`content-strategist` の信念) |
| 2026-05-10 | `generate_sitemap.py` の lastmod 継承ロジックで 4/3 のまま陳腐化 | git log ベースに修正・MEDIUM_PRIORITY tier 追加 |

## 13. 5 エリア × 35 コースの基本構造

| エリア | コース数 | 主要コース例 |
|---|---|---|
| fukuokacity (福岡市) | 7+ | aburayama / fukuokacc / hisayama / keya / saitozaki 等 |
| itoshima (糸島) | 4 | ito / keya / nijo / queenshill |
| kitakyushu (北九州) | 9 | fukuokakokusai / kokura / wakamiya / wakamatsu 等 |
| chikugo (筑後) | 6 | ariake / century / dazaifu / kurume 等 |
| chikuho (筑豊) | 6 | akane / asoiizuka / central / lakeside 等 |

### ペルソナハブ (4 個)
- `hub-budget.html` (¥10k 以下中心)
- `hub-beginner.html` (短いコース・フラット)
- `hub-traveler.html` (絶景・観光連携)
- `hub-business.html` (会員制・接待向け)

### 多言語 Tier (i18n_course_compatibility.json)
- **Tier 1 (公式 KO 直対応)**: wakamiya のみ (1 件) → Phase 4-B 単独 LP 候補
- **Tier 2 (Accordia ポータル機械翻訳)**: nijo / central / pheasant (3 件)
- **Tier 3 (PGM ポータル機械翻訳)**: fukuokakokusai / kitakyushu / moonlake / lakeside (4 件)
- **Tier 4 (限定 EN のみ)**: hisayama / sevenmillion (2 件)
- **Tier 5 (日本語のみ)**: 25 件

## 14. Phase 履歴サマリ (2026-04 〜 2026-05)

完了済 Phase (詳細は `NEXT_SESSION.md` の実装履歴):

- ✅ **Phase 1A**: 全 35 コース × 3 言語 = 105 セクションに逆流ナビ挿入 (`4c40600` / 2026-05-05)
- ✅ **Phase 1B**: 標準 30 コースに hero CTA + sticky CTA + KO 楽天追加 (`4c40600`)
- ✅ **Phase 2**: 取引KW LP 3 ページ (cheap / tomorrow / solo) (`6a03311` / 2026-05-05)
- ✅ **Phase 3**: Decoy 価格カード CSS 介入 (`289bb21` / 2026-05-05)
- ✅ **Phase 4 Step 1**: GA4 計測 v2.1 (`5758dbe` / 2026-05-06)
- ⏳ **観測フェーズ進行中** (2026-05-10 〜 2026-06-03)
- ⏳ **Phase 4-B 準備済** (wakamiya 単独 KO LP・Day 28 GO 判定後に実装)

ブログ会社化 Phase (詳細は `BLOG_COMPANY_PROGRESS.md`):
- ✅ Phase 1: 9 subagent 配置 (`51577cf` / 2026-05-10)
- ✅ Phase 2: 7 skill 配置 (`5110d58` / 2026-05-10)
- ⏳ Phase 3.1: テンプレート雛形配置 (`e33d7a9` / 2026-05-10)・残 3.2-3.4
- 🔲 Phase 4: Plugin 化

---

**次に読むべきファイル**:
1. `NEXT_SESSION.md` — 引き継ぎ正典・直近の実装履歴
2. `OBSERVATION_PLAYBOOK.md` — 観測中なら判定フローを確認
3. `BLOG_COMPANY_PROGRESS.md` — ブログ会社化の進捗
