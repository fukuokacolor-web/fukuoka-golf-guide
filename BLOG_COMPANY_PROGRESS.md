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
| **2** | Skill 化 (workflow 自動化) | 8-12h | ⏳ **進捗 6/7・2026-05-10**(残 /create-course-page のみ) |
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

### ✅ 配置済 (6/7)

| Skill | 配置先 | 行数 | 動作確認 |
|---|---|---|---|
| **`/expert-meeting`** | `~/.claude/skills/expert-meeting/SKILL.md` | 177 | 🔲 次セッション初使用予定 |
| **`/observation-checkin`** | `~/.claude/skills/observation-checkin/SKILL.md` | 264 | 🔲 5/13 (Day 7) 初使用予定 |
| **`/sitemap-regenerate`** | `~/.claude/skills/sitemap-regenerate/SKILL.md` | 77 | 🔲 次の sitemap 更新時 |
| **`/ga4-tracking-deploy`** | `~/.claude/skills/ga4-tracking-deploy/SKILL.md` | 91 | 🔲 新規 HTML 追加時 |
| **`/decoy-pricing-apply`** | `~/.claude/skills/decoy-pricing-apply/SKILL.md` | 89 | 🔲 観測終了後 (6/3+) |
| **`/dual-dir-sync`** | `~/.claude/skills/dual-dir-sync/SKILL.md` | 129 | 🔲 次の Edit 後 |

### 仕様サマリ

| Skill | 引数 | 主動作 |
|---|---|---|
| `/expert-meeting` | `<topic> [participants]` | 9 subagent から 4-6 名招集 → 議事録自動生成 |
| `/observation-checkin` | `<day: 7/14/28/42>` | PLAYBOOK スレッショルド自動適用 → §6 更新 → Day 28 なら §5 マトリクス |
| `/sitemap-regenerate` | (なし) | dry-run → 承認 → 適用 → 差分表示 → GSC 再送信リマインド |
| `/ga4-tracking-deploy` | (なし) | dry-run → 抵触チェック → 適用 → preview 検証 |
| `/decoy-pricing-apply` | (なし) | dry-run → **観測抵触チェック (★★★)** + 倫理境界線 → 適用 |
| `/dual-dir-sync` | `<pattern>` | repo→preview コピー + 差分検証 + orphan 警告 |

### 共通設計原則

- **dry-run → 承認 → 本番** の 3 段階を厳守 (即実行禁止)
- **観測フェーズ抵触チェック** を本番実行前に必ず行う (`/decoy-pricing-apply` で最重要)
- **倫理境界線チェック** (虚偽訴求・dark pattern) を該当 skill で実施 (`/decoy-pricing-apply`)
- **両ディレクトリ規約** を全 skill が遵守 (REPO_ROOT + PREVIEW_ROOT)
- **会議再招集** が必要な状況なら `/expert-meeting` 起動を推奨

### 🔲 残候補 (1/7)

| Skill | 優先 | 工数推定 | メモ |
|---|---|---|---|
| `/create-course-page <slug>` | ★★ | 2-3h | 新規コース追加の最頻出オペレーション・Phase 3 (テンプレート化) への布石 |

→ 次セッションで Phase 2 完全完了予定

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
