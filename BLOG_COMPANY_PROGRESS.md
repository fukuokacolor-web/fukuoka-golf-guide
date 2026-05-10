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
| **2** | Skill 化 (workflow 自動化) | 8-12h | 🔲 着手準備中 |
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

## Phase 2 着手準備 (Skill 化候補)

頻出ワークフローで skill 化 ROI が高いもの:

| Skill 候補 | 内容 | 優先 | 工数推定 |
|---|---|---|---|
| `/expert-meeting <topic> <participants>` | 4-6 名並列招集 → 議事録自動生成 → コンセンサス + 推奨実行順 | ★★★ | 1.5-2h |
| `/observation-checkin <day>` | OBSERVATION_PLAYBOOK の Day 7/14/28 自動実行 | ★★★ | 1.5-2h |
| `/create-course-page <slug>` | コース新規追加 (HTML 生成 + sitemap 更新 + area 追加 + 計測展開) | ★★ | 2-3h |
| `/dual-dir-sync <pattern>` | repo + preview 両ディレクトリ強制同期 (規約強制) | ★★ | 1h |
| `/decoy-pricing-apply` | Phase 3 Decoy ロジック適用 (CSS only) | ★ | 1h |
| `/ga4-tracking-deploy` | inject_ga4_tracking.py 適用 (両ディレクトリ + 検証) | ★ | 0.5h |
| `/sitemap-regenerate` | scripts/generate_sitemap.py 実行 + 差分確認 | ★ | 0.3h |

合計工数: 8-10h (一部上位 3 件で Phase 2 を実質完了可)

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
