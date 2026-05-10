# 🏢 ブログ会社化アーキテクチャ進捗管理

**戦略決定日**: 2026-05-10
**目的**: fukuoka-golf-guide.com の 1 サイト運用を起点に、Claude Code の Subagent / Skill / Slash Command / Hook / Plugin で **複数サイトを効率運用するブログ会社体制**へ移行する
**全体工数見積**: 25-37h (4 フェーズ合計)

---

## 4 フェーズ計画

| Phase | 内容 | 工数 | 状態 |
|---|---|---|---|
| **0** | 棚卸し (BLOG_COMPANY_INVENTORY.md) | 3-4h | 🔲 未着手 (省略可・暗黙的に Phase 1-4 で実行) |
| **1** | Subagent 化 (9 専門家) | 4-6h | ✅ **完了 (2026-05-10)** |
| **2** | Skill 化 (workflow 自動化) | 8-12h | ⏳ **着手中 (2/7・2026-05-10)** |
| **3** | テンプレート化 (複数サイト雛形) | 12-20h | 🔲 未着手 |
| **4** | Plugin 化 (配布可能パッケージ) | 4-6h | 🔲 未着手 |

---

## Phase 1 成果物 (2026-05-10 完了)

### ✅ 9 専門家 subagent 配置済

全て **`C:/Users/Owner/.claude/agents/<name>.md`** に配置 (ユーザーレベル・全プロジェクト横断利用可)。
新セッションで `Agent` ツールに `subagent_type: <name>` で起動可能。

| # | name | 元ペルソナ | 専門領域 | tools |
|---|---|---|---|---|
| 1 | `content-strategist` | 山本誠一 | E-E-A-T・取材ドリブン編集・エバーグリーン | Read, Grep, Glob, WebSearch, WebFetch, Write, Edit |
| 2 | `seo-strategist` | 田中健太郎 | KW 戦略・トピッククラスタ・GSC 分析・カニバリ | + Bash |
| 3 | `cvr-optimizer` | 佐藤美咲 | CTA 設計・観測プレイブック・二項検定 N 計算 | + Bash |
| 4 | `ia-architect` | 鈴木玲奈 | サイト構造・sitemap・hreflang・JSON-LD | + Bash |
| 5 | `behavioral-economist` | 教授 | Decoy・Center-stage・アンカリング・倫理境界 | (subset) |
| 6 | `fact-checker-primary` | 鈴木一郎 | 公式サイト直確認・1 次調査・3 ソース原則 | (read-only) |
| 7 | `fact-checker-secondary` | 中村麻衣 | 独立検証・反証・両者合意ライン | (read-only) |
| 8 | `inbound-strategist` | 金星誠 | KO/EN 多言語 SEO・Naver・Influencer 連携 | (subset) |
| 9 | `payment-specialist` | David Chen | 国際決済・ASP 比較・通貨換算 UX | (subset) |

### 共通骨格 (8 セクション)

各 subagent ファイルは以下の構造で統一:

```
1. frontmatter (name / description / tools / model)
2. ペルソナ紹介 (1 行)
3. 核となる信念 (絶対) — 5-7 項目
4. 思考プロセス — 5-7 ステップ
5. 出力フォーマット規約
6. プロジェクト固有の文脈読込み (作業前必読)
7. 専門家会議で求められる典型タスク
8. 自己却下する案 (再提案禁止)
9. 連携 (Cross-checking) — 他専門家との協業ポイント
```

### 動作検証

- `content-strategist` で実証済 (`INTERVIEW_CANDIDATES.md` + `INTERVIEW_PROTOCOL_DRAFT.md` 生成)
- 他 8 名は次セッションで初使用予定 (subagent はファイル直接編集後はセッション再起動が必要)

---

## Phase 2 進捗 (Skill 化)

### ✅ 配置済 (2/7)

| Skill | 配置先 | 動作確認 |
|---|---|---|
| **`/expert-meeting`** | `~/.claude/skills/expert-meeting/SKILL.md` | 🔲 次セッション初使用予定 |
| **`/observation-checkin`** | `~/.claude/skills/observation-checkin/SKILL.md` | 🔲 5/13 (Day 7) 初使用予定 |

`/expert-meeting` 仕様 (2026-05-10 配置):
- 引数: `<topic> [participants 任意・カンマ区切り]`
- 動作: 配置済 9 subagent から 4-6 名を議題から自動選定 (or 明示指定) → 単一メッセージで並列招集 → 議事録自動生成
- 出力: Markdown 議事録 (各専門家提案サマリ + Tier 1-3 コンセンサス + 今日の最初の 1 手)
- 全員 ○ で Tier 1 / 1 名でも × あれば Tier 2 降格・抵触理由明記
- ファクトチェック議題は primary + secondary 必ずペア招集

`/observation-checkin` 仕様 (2026-05-10 配置):
- 引数: `<day: 7 | 14 | 28 | 42>`
- 動作: OBSERVATION_PLAYBOOK §3 のスレッショルドを GA4 5 レポートに自動適用 → §6 結果記入欄を Edit で更新 → Day 28 なら §5 判定マトリクスから Phase 4 着手判断
- GA4 アクセス: Mode A (Chrome MCP 自動) or Mode B (Manual・ユーザー手入力)
- ノイズ除外: 5/10 テストクリック 8 件・internal_fees・登録前 `(not set)` 期間外データ
- Day 7 は GO/NO 確定しない (異常値検出のみ・PLAYBOOK §4 規約)・Day 14 以降で本格判定
- 両ディレクトリ同期 (PLAYBOOK が repo + preview 両方にある場合)
- 会議再招集要否を出力 (大きな判定変動時に `/expert-meeting` 起動推奨)

### 🔲 残候補 (5/7・優先順)

| Skill | 優先 | 工数推定 |
|---|---|---|
| `/create-course-page <slug>` | ★★ | 2-3h |
| `/dual-dir-sync <pattern>` | ★★ | 1h |
| `/decoy-pricing-apply` | ★ | 1h |
| `/ga4-tracking-deploy` | ★ | 0.5h |
| `/sitemap-regenerate` | ★ | 0.3h |

残工数: 4.5-7h・上位 2 件 (`/create-course-page` + `/dual-dir-sync`) で 3-4h で Phase 2 実質完了可

---

## Phase 3 計画 (テンプレート化)

複数サイト立ち上げのスケーラビリティ:

- `~/blog-template/` 標準雛形ディレクトリ
- `CLAUDE.md` を 共通 (運用規約) + サイト固有 (ドメイン/GA4 ID/収益モデル) に分離
- 新サイト = 雛形コピー + サイト固有 CLAUDE.md カスタマイズ
- 既存 9 subagents + Phase 2 skills を 即利用可

---

## Phase 4 計画 (Plugin 化)

`claude-fukuoka-blog-toolkit.plugin` として:
- 9 subagents バンドル
- 全 skills バンドル
- 共通 hooks (両ディレクトリ同期強制・観測中の HTML 改修ブロック等)
- 1 コマンドで他サイトに導入可能

---

## 重要な原則 (再掲)

1. **Subagent から subagent を直接呼べない** (Claude Code 仕様)・チェーンは主会話から制御
2. **専門家会議の人格を変える時は subagent ファイルと NEXT_SESSION.md 両方を更新** (二重管理)
3. **9 名以外の subagent 増殖は慎重に** (役割重複は意思決定ノイズ・既存 9 名で吸収可能か検討してから追加)
4. **Subagent のファイル直接編集後はセッション再起動が必要** (`/agents` UI 経由なら即時反映)
5. **配置はユーザーレベル (`~/.claude/agents/`)** が原則・プロジェクト固有の調整が必要な場合のみ `.claude/agents/` でオーバーライド

---

## 次セッション以降のテンプレ

新セッションで「専門家会議を招集して」と言われたら:

```python
# 主会話で 4-6 名を並列招集
Agent(subagent_type="seo-strategist", description="SEO 観点", prompt=...)
Agent(subagent_type="cvr-optimizer", description="CVR 観点", prompt=...)
Agent(subagent_type="ia-architect", description="IA 観点", prompt=...)
Agent(subagent_type="content-strategist", description="Content 観点", prompt=...)
# 必要に応じて behavioral-economist, inbound-strategist, payment-specialist
```

事実確認が必要な議題には:

```python
Agent(subagent_type="fact-checker-primary", ...)
# 結果を受けて
Agent(subagent_type="fact-checker-secondary", ...)  # 独立検証
```

---

**最終更新**: 2026-05-10 (Phase 1 完了)
