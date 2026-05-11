# 🎯 次セッション 引き継ぎ指示書

**最終更新**: 2026-05-11 (★ Phase 3.4 完了・テンプレ v1.1.0 refine・Phase 3 実用段階完了)
**最終 commit**: `5758dbe` (Phase 4 Step 1 - GA4 観測ダッシュボード準備)
**前回 commit**: `289bb21` (Phase 3 - Decoy)、`6a03311` (Phase 2 - 取引KW LP)、`4c40600` (Phase 1 - 逆流ナビ+CVR)

---

## 🆕 2026-05-09 GA4 Day 3 観測ログ (Claude in Chrome 経由で実数確認)

**GA4 アクセス情報**
- アカウント ID: `389856983` / プロパティ ID: `531139357`
- 保存済エクスプロレーション (CTA Position × デバイス × click_affiliate フィルタ): https://analytics.google.com/analytics/web/#/analysis/a389856983p531139357/edit/QHDhd8usTCW-m-czokhZCQ

**✅ カスタムディメンション 8 個 全登録完了 (2026-05-09)**
CTA Position / Language / Link Text / Link URL / Nav Section / Page / Service / Target Page
→ GA4 仕様で **24-48h 後 (2026-05-10〜11)** からレポート反映開始

**📊 過去 28 日間 (2026-04-11〜2026-05-08) のイベント実数**
| イベント名 | 件数 | ユーザー | 解釈 |
|-----------|------|---------|------|
| page_view | 303 | 101 | — |
| session_start | 163 | 101 | — |
| user_engagement | 163 | 34 | — |
| scroll | 132 | 49 | — |
| first_visit | 99 | 97 | — |
| **click** | **45** | 13 | ⚠️ **要調査**: 想定外の汎用 `click` イベントが発火している (`inject_ga4_tracking.py` のロジック確認必要) |
| **click_affiliate** | **35** | 10 | ✅ 既存トラッキング稼働継続 (desktop 27 / mobile 8 / Japan 34 + Taiwan 1) |
| **internal_nav_click** | **3** | 1 | ✅ **Plan B v2.1 新規イベント発火確認** (Phase 1A 逆流ナビが実際に使われている初の証拠) |

**📈 流入・国別 (過去 7 日間)**
- アクティブユーザー: 27 (前週比 ▼61.4%) / PV: 103 / イベント: 322
- 国別: Japan 9 / **United States 8** / Germany 3 / South Korea 2 / Poland 2 / Canada 1 / Netherlands 1 → **EN/KO 流入が想定以上**
- 流入: Direct 34 / Organic Search 8 / Referral 5

**⚠️ 要調査事項 (次回優先タスク)**
1. ~~**`click` 汎用イベント 45 件の発火源**~~ → ✅ **解決 (2026-05-10)**: GA4 Enhanced Measurement の Outbound clicks 自動計測が発火源。リポジトリ全体に `gtag('event', 'click', …)` の呼び出しは無く、GTM 等の他トラッカーも未導入。`click` (GA4 自動) ⊃ `click_affiliate` (自前) の包含関係で、差分 10 件 = 非アフィリ外部離脱 (Google Maps / コース公式等)。コード修正不要・収益指標は `click_affiliate` のみ参照。詳細: `GA4_DASHBOARD.md` §1.4
2. ~~**本日 (2026-05-10) 同じエクスプロレーション再訪**~~ → ✅ **解決 (2026-05-10)**: course-keya.html で 8 種類のクリックを実機テスト + dataLayer 直接検証で**全件正しい cta_position 値が送信されている**ことを確認。エクスプロレーションでデータゼロだったのは反映遅延ではなく「5/9-5/10 のユーザークリックが少なかった」実数の問題。28 日エクスプロレーションが全件 `(not set)` なのも仕様 (登録 5/9 前のレガシーデータは再分類されない)。詳細: `GA4_DASHBOARD.md` §1.5
3. **観測スケジュール継続** — Day 7 (2026-05-13): レポート 1-3 / Day 14 (2026-05-19): 本格判定 / Day 28 (2026-06-03): Phase 4 着手判断
4. ⚠️ **観測中の HTML 改修禁止 (会議合意)** — 5/10 のテストクリック 8 件は計測ノイズとして許容 (1 ユーザー・全件 ja・direct)、全体傾向への影響は無視可能。Phase 1A/1B/3 の効果測定は **5/10 以降の自然トラフィック**で行う。
5. 📘 **`OBSERVATION_PLAYBOOK.md` (新規)** — Day 7/14/28 各日の 30 分判定フロー + 事前確定スレッショルド + 結果記入欄 + Phase 4 着手判断マトリクス。**観測フェーズ運用の正典**。確証バイアス排除のため、Day 28 当日に数値見ながらスレッショルドを動かすことを禁止。

---

## 📊 サイト全体の現状

| 項目 | 値 |
|------|------|
| ドメイン | https://fukuoka-golf-guide.com (本番運用中) |
| GA4 ID | `G-PENH0Z4VT7` (絶対変更禁止) |
| 総コース数 | **35** (5エリア完全網羅) |
| 総HTMLページ | 89+ |
| 言語 | 日本語/English/한국어 (3言語) |
| sitemap.xml | 93 URLs |
| GitHub | fukuokacolor-web/fukuoka-golf-guide (main ブランチ運用) |

---

## ✅ 直近の実装履歴 (新しい順)

1. **🆕★ ブログ会社化 Phase 3.4 完了 — テンプレ v1.1.0 refine** (`0120366` 後継 / 2026-05-11)
   - 配置先: `~/blog-template/CLAUDE.md` (約 200 行) + `~/blog-template/README.md` (v1.1.0)
   - Phase 3.2 で発見した改善点 3 件をテンプレに反映:
     - §10 をファイル役割分担表に拡張 (役割 + 更新頻度 + static/dynamic/cyclic 分類)
     - §13 プロジェクト構造サマリ新規 (カテゴリ分類 + ペルソナハブ + 特殊分類)
     - §14 Phase 履歴サマリ新規 (静的保存・NEXT_SESSION.md と役割分離)
   - 追加: §12 リスクと事故防止を表形式化 + §11 にコミット粒度
   - README.md にバージョン履歴 (v1.0.0 → v1.1.0) + 変更内容
   - **Phase 3 実用段階完了**: 3.1 (雛形) + 3.2 (逆適用実証) + 3.4 (refine) 完了・残 3.3 (実サイト要望待ち)
   - 次にテンプレから scaffold する新規サイトは、これらの section をプレースホルダ埋めで自然に整備可能
   - 観測指標に非干渉 (HTML 改修なし・メタ文書のみ)
2. **🆕★ ブログ会社化 Phase 3.2 完了 — `CLAUDE.md` 配置 (テンプレ逆適用実証)** (`e33d7a9` 後継 / 2026-05-11)
   - 配置先: `fukuoka-golf-guide/CLAUDE.md` (221 行・両ディレクトリ同期)
   - テンプレ `~/blog-template/CLAUDE.md` (157 行・全 `[REPLACE]` プレースホルダ) を実値で全埋め
   - fukuoka 固有セクション 3 つ追加:
     - §10 ファイル役割分担表 (CLAUDE.md / NEXT_SESSION.md / OBSERVATION_PLAYBOOK.md 等の更新頻度)
     - §13 5 エリア × 35 コース構造 + ペルソナハブ 4 個 + 多言語 Tier 1-5 分類
     - §14 Phase 履歴サマリ (Phase 1A/1B/2/3/4 Step1 + ブログ会社化 Phase 1/2/3.1/3.2)
   - 過去事故 4 件を §12 リスクと事故防止に表形式で記録 (course_data 破壊・観測中改修・量産記事・lastmod 陳腐化)
   - アフィリ除外コース 8 件 (楽天 4 + じゃらん 4・差分 akane/aburayama) を §9 禁止事項 #4 に明文化
   - Phase 3.2 で発見されたテンプレ改善点 3 件 (BLOG_COMPANY_PROGRESS.md に記録・Phase 3.4 で反映予定)
   - **wakamiya 公式 KO ページ生存確認済 (2026-05-11)**: HTTP 正常・韓国語コンテンツ正常 → Phase 4-B 前提条件維持
   - 衛生作業: Day 2 観測中・観測指標に非干渉 (HTML 改修なし・メタ文書のみ)
2. **🆕★★★ ブログ会社化 Phase 3.1 完了 — `~/blog-template/` 雛形配置** (`5110d58` 後継 / 2026-05-10)
   - 配置先: `~/blog-template/` (ユーザーレベル・新規ブログサイト立ち上げ時の雛形)
   - 配置済 7 ファイル / 940 行:
     - `README.md` (152 行・テンプレ使い方 + 9 subagent + 7 skill カタログ)
     - `CLAUDE.md` (157 行・運用規約共通 + サイト固有プレースホルダ `[REPLACE]`)
     - `NEXT_SESSION.template.md` (159 行・引き継ぎ正典 skeleton)
     - `docs/ARCHITECTURE.md` (128 行・設計思想 + 規約根拠 7 軸)
     - `docs/OBSERVATION_PLAYBOOK.template.md` (161 行・観測判定インフラ skeleton)
     - `docs/BLOG_COMPANY_PROGRESS.template.md` (79 行・新規サイト用進捗管理)
     - `scripts/README.md` (104 行・共通 scripts コピー手順 + サイト固有 vs 共通の判断基準)
   - 設計判断:
     - CLAUDE.md は共通 + プレースホルダ (`[REPLACE]` マークアップ)
     - subagent/skill は ~/.claude/ で全プロジェクト共通 (テンプレ内には複製しない)
     - scripts は fukuoka-golf-guide からコピー (テンプレに同梱しない・README で案内)
     - 両ディレクトリ規約はオプション (Single/Dual ディレクトリ選択式)
   - **次の活用パターン**: 新サイトは `cp -r ~/blog-template/* {新サイトdir}/` + CLAUDE.md `[REPLACE]` 埋めで scaffold 完了
   - Phase 3 残: 3.2 (既存 fukuoka-golf-guide に CLAUDE.md 逆適用・1-2h) / 3.3 (2 サイト目実証・5-8h・実サイト要望待ち) / 3.4 (テンプレ refine・2-3h)
2. **🆕★★★ ブログ会社化 Phase 2 完全完了 — `/create-course-page` 配置 (7/7)** (`4fce582` 後継 / 2026-05-10)
   - 配置先: `~/.claude/skills/create-course-page/SKILL.md` (195 行・最複雑な複合 skill)
   - 引数: `<slug> [--skip-decoy] [--skip-deeplink]`
   - 動作: 新規コースを 1 コマンドで全展開
     - Pre-flight 4 チェック (course_data 存在 / 重複 / mapping / 観測抵触)
     - HTML 生成 (course-{slug}.html + access-{slug}.html・3 言語)
     - エリアハブ統合 (area-{area}.html + 該当 hub-* + sitemap-guide.html)
     - 7 post-processing スクリプト順次実行 (Phase 1A 逆流ナビ + 1B CVR + 3 Decoy + 4 GA4 + jalan/rakuten deep link + hreflang + og:locale)
     - sitemap.xml 更新 (両ディレクトリ自動)
     - 両ディレクトリ同期確認
     - preview tool で 3 言語 + dataLayer + JSON-LD 検証
     - NEXT_SESSION.md 自動更新 + GSC 再送信リマインド
   - **Phase 2 完全完了 (7/7)・残 0**
   - 合計 7 skill / 1,022 行・全プロジェクト横断利用可
   - **次セッションから skill が即時利用可** (skill ファイル直編集はディレクトリ監視で即時反映)
   - Phase 3 着手準備: テンプレート化 (`~/blog-template/` 雛形 + サイト固有 CLAUDE.md 分離・12-20h)
   - `/sitemap-regenerate` (77 行): `scripts/generate_sitemap.py` ラッパー・dry-run → 承認 → 適用 → diff 表示 → GSC 再送信リマインド
   - `/ga4-tracking-deploy` (91 行): `scripts/inject_ga4_tracking.py` ラッパー・観測抵触チェック → preview 検証 (dataLayer 直接読取で event 確認)
   - `/decoy-pricing-apply` (89 行): `scripts/decoy_pricing_redesign.py` ラッパー・**★★★ 観測抵触チェック最重要 + 倫理境界線チェック (虚偽訴求・dark pattern 拒否)**
   - `/dual-dir-sync <pattern>` (129 行): repo↔preview 同期強制・identical/diff/orphan の 3 値分類 + 検証 + orphan 警告
   - 共通設計原則: dry-run → 承認 → 本番 の 3 段階厳守・観測抵触チェック必須・両ディレクトリ規約遵守・会議再招集判断 (`/expert-meeting` 起動推奨)
   - Phase 2 残: `/create-course-page <slug>` のみ (★★・2-3h・新規コース追加自動化・Phase 3 テンプレート化への布石)
2. **🆕★ ブログ会社化 Phase 2 — `/observation-checkin` skill 配置 (2/7)** (`17b1703` 後継 / 2026-05-10)
   - 配置先: `~/.claude/skills/observation-checkin/SKILL.md` (ユーザーレベル・全プロジェクト横断)
   - 引数: `<day: 7 | 14 | 28 | 42>`
   - 動作: OBSERVATION_PLAYBOOK §3 のスレッショルドを GA4 5 レポートに自動適用 → §6 Day {day} 結果記入欄を Edit で更新 → Day 28 なら §5 判定マトリクスから Phase 4 着手判断機械決定
   - GA4 アクセス: Mode A (Chrome MCP 自動取得) or Mode B (Manual・ユーザー手入力) を自動選択
   - 機械判定ロジック: 5 レポート × GO/HOLD/NO/延長 を事前確定スレッショルドで離散化 (確証バイアス排除)
   - ノイズ除外: 5/10 テストクリック 8 件・internal_fees・登録前 `(not set)` 期間外データ
   - **Day 7 (5/13・3 日後) 初使用予定**: `/observation-checkin 7` で 30 分判定が 5 分に短縮
   - Day 7 規約: GO/NO 確定しない (異常値検出のみ・PLAYBOOK §4 遵守)・Day 14 以降で本格判定
   - 大きな判定変動時は `/expert-meeting "Day X 判定結果踏まえた次手判断"` を自動推奨
2. **🆕★ ブログ会社化 Phase 2 着手 — `/expert-meeting` skill 配置 (1/7)** (`51577cf` 後継 / 2026-05-10)
   - 配置先: `~/.claude/skills/expert-meeting/SKILL.md` (ユーザーレベル・全プロジェクト横断)
   - 引数: `<topic> [participants 任意・カンマ区切り]`
   - 動作: 配置済 9 subagent から 4-6 名を議題から自動選定 (or 明示指定) → 単一メッセージで並列招集 → 議事録 Markdown を自動生成
   - 出力構造: 各専門家提案サマリテーブル + Tier 1-3 コンセンサス分類 + 今日の最初の 1 手の推奨
   - ルール: 全員 ○ で Tier 1 / 1 名でも × あれば Tier 2 降格 + 抵触理由明記・ファクトチェック議題は primary + secondary 必ずペア招集
   - 動作検証: 次セッションで初使用予定 (skill ファイル直接編集後はディレクトリ監視で即時反映 or 新規ディレクトリは要再起動)
   - **次セッションで使う方法**: `/expert-meeting Phase 4-B 着手判断` のように topic を渡すだけ → 4-6 名招集 + 議事録が自動で返る
   - Phase 2 残: /observation-checkin (★★★・Day 7 用に最優先) / /create-course-page / /dual-dir-sync / /decoy-pricing-apply / /ga4-tracking-deploy / /sitemap-regenerate (6 件・残工数 6-9h)
2. **🆕★★ ブログ会社化 Phase 1 完了 — 9 専門家全員 subagent 配置完了** (`d635f43` 後継 / 2026-05-10)
   - 全 9 名を `~/.claude/agents/<name>.md` に配置 (ユーザーレベル・全プロジェクト横断利用可)
   - 配置完了リスト: `content-strategist` (山本) / `seo-strategist` (田中) / `cvr-optimizer` (佐藤) / `ia-architect` (鈴木玲奈) / `behavioral-economist` (教授) / `fact-checker-primary` (鈴木一郎) / `fact-checker-secondary` (中村麻衣) / `inbound-strategist` (金星) / `payment-specialist` (David Chen)
   - 共通骨格 8 セクション: frontmatter + ペルソナ紹介 + 核となる信念 + 思考プロセス + 出力規約 + 文脈読込 + 典型タスク + 自己却下案 + Cross-checking 連携
   - 平均 74 行 / file (合計 668 行)・tools 設定はロール別に最適化 (fact-checker は read-only / 他は Write/Edit/Bash 含む)
   - 動作検証: `content-strategist` のみ実証済 (山本タスクで生成)・他 8 名は新セッションで初使用予定
   - 新規ドキュメント: `BLOG_COMPANY_PROGRESS.md` (4 フェーズ進捗管理)
   - **次セッションで使う方法**: 主会話で `Agent` ツールに `subagent_type: <name>` で 4-6 名を並列招集・専門家会議が高速化
   - Phase 2 着手準備: skill 化候補 7 件抽出 (`/expert-meeting` `/observation-checkin` `/create-course-page` 等・上位 3 件で Phase 2 実質完了可)
2. **🆕★ ブログ会社化 Phase 1 着手 + 山本 INTERVIEW タスク完了** (`9b38d11` 後継 / 2026-05-10)
   - **★ 戦略転換**: 1 サイト運用 → 「複数サイト効率運用ブログ会社」体制への移行決定 (Phase 0-4 アーキテクチャ確定)
   - **Phase 1 第一歩**: `~/.claude/agents/content-strategist.md` 新規作成 (山本誠一 persona の subagent 化・ユーザーレベル配置で全プロジェクト横断利用可)
   - subagent 仕様確認: 必須 (name/description) / 任意 (tools/model/permissionMode 等)・本文に E-E-A-T 信念 + 思考プロセス + 出力規約 + 自己却下案を明文化・新セッションで `subagent_type: content-strategist` で起動可
   - **動作検証**: general-purpose に persona ファイル注入で疑似実行 → 同等動作確認・成果物 2 ファイル生成
   - **山本タスク成果物**:
     - `INTERVIEW_CANDIDATES.md` (268 行・35 コース 5 軸スコアリング + 5 件確定: 小倉 19 / 芥屋 21 / 福岡国際 19 / 二丈 20 / 若宮 19 + 補欠 7 件)
     - `INTERVIEW_PROTOCOL_DRAFT.md` (399 行・打診メール 3 種テンプレ + 取材ガイド + JSON-LD InterviewSchema + リスク遵守事項)
   - 戦略バランス: 老舗名門 + 単独 + PGM + Accordia + インバウンド差別化 (wakamiya) の 5 セグメント分散
   - ハルシネーション排除: 人物実名は全て「(要追加調査)」明記・観測終了後に公式サイト直確認必須化
   - Phase 1 残タスク: 8 名の subagent 化 (seo-strategist / cvr-optimizer / ia-architect / behavioral-economist / fact-checker × 2 / inbound-strategist / payment-specialist)
2. **🆕 KO 市場リサーチ (金星誠タスク) — `KO_MARKET_RESEARCH.md` 新規** (`583deef` 後継 / 2026-05-10)
   - 専門家会議 Tier 2 (金星 インバウンド) として実装。Day 28 GO 後の launch 速度を 1 週間→1 日に短縮するための事前リサーチ
   - **被リンク獲得候補 14 件**: 高 ROI Tier (難度 1-2 / 6 件: 딜바다・DC 갤・TOM Cafe・Threads × 2・Calarca) + 中 ROI Tier (難度 3-4 / 8 件: Brunch × 2・InsightKorea 等)
   - **Influencer**: 도쿄린짱 (한국 대상 일본 골프 専門 YouTuber・第 1 候補) / Threads @japantoyotarent / @fine___tour が Tier 1 候補
   - **Naver SERP 分析** (3 主 KW): 商用여행사が独占 → 와카미야 ロングテール 5 KW 戦略を確定 (와카미야 골프 / 트라이얼 골프 리조트 / 후쿠오카 4000엔 골프 / 후쿠오카 한국어 골프장 / 미야와카 온천 골프・累計 月 250-830 Vol 推定 / 競争度 1-2)
   - **新発見**: VISIT FUKUOKA 韓国語版 (crossroadfukuoka.jp/kr/spot/10351) が wakamiya を既掲載 → 公式観光局認定として訴求材料に活用可能
   - Day 28 GO 後 90 日で月¥10 万到達ロードマップ確定 (KO ¥3-5 万 + EN/JP 累積 ¥7-10 万)
   - HTML 改修禁止抵触なし (Markdown 文書のみ)
   - 観測中の更新タスク: Day 7/14/28 で §1 KR セッション数を毎週更新
2. **🆕 IA 改善 (鈴木玲奈タスク) — sitemap.xml lastmod 修復 + priority 体系再編** (`d3a13ab` 後継 / 2026-05-10)
   - 専門家会議 (5 名) の Tier 1 衛生作業として実装。鈴木 IA 案 a+c (lastmod 修復 + priority 整理)
   - **lastmod 修復**: `scripts/generate_sitemap.py` を「既存 sitemap 値継承」→「git log の最新コミット日」へロジック変更。これにより Phase 1A/1B/3 改修分 (5/5-5/6) や hreflang 全ページ更新 (5/9) が **`<lastmod>2026-04-03</lastmod>` 等のまま陳腐化していた問題**を解消 (98 URL 全件 5/8〜5/9 に更新)
   - **priority 体系**: 0.9 HIGH (10件・area + airport + course-kokura + Phase 2 LP × 3) / 0.8 MEDIUM (5 件・**4 ペルソナハブ + book-fukuoka-golf-foreigner**・新設) / 0.7 default (81) / 0.6 LOW (editorial-policy 1) を 5 階層化。手動編集された Phase 2 LP の 0.9 / editorial-policy の 0.6 / monthly changefreq 2 件を **規約として明文化**して保護
   - スクリプト機能追加: `--dry-run` フラグ / 両ディレクトリ処理 / git log fallback (mtime → today)
   - **ユーザー側次タスク**: GSC で sitemap 再送信 → クローリング更新を 5/13 (Day 7) までに反映予測。観測サンプルサイズの底上げに直結
   - ROI 期待: Phase 1A/1B/3 のインデックス反映 2-3 週→3-5 日に短縮 / 観測中の自然流入 +200-500 PV/月 (副次効果)
   - HTML 改修禁止抵触なし (sitemap.xml は HTML ではなく メタファイル・観測指標に非干渉)
2. **🆕 OBSERVATION_PLAYBOOK.md 新設 + GA4 v2.1 計測本番検証** (`d3a13ab` / 2026-05-10)
   - `OBSERVATION_PLAYBOOK.md` 新規 (Day 7/14/28 判定インフラ・5 探索レポート × 事前確定スレッショルド・必要 N 計算・結果記入欄テンプレ・Phase 4 着手判断マトリクス 8 シナリオ)
   - GA4_DASHBOARD.md §1.4 追記: 汎用 `click` 45 件は GA4 Enhanced Measurement の自動 Outbound clicks。リポジトリ全体に `gtag('event','click')` の呼び出し無し・GTM 未導入確認
   - GA4_DASHBOARD.md §1.5 追記: 8 種クリックパス本番検証完了 (hero/ftv/sticky/price_default/price_featured/booking_grid + internal_nav_click)・dataLayer 直接読取で全件正常動作確認
   - ノイズ: 5/10 のテストクリック 8 件 (1 ユーザー・direct・ja・desktop・全体傾向への影響微小)
   - 専門家会議 5 名招集 (田中/佐藤/鈴木/金星/山本) → 24 日観測フェーズ中の Tier 1 タスクとして佐藤 (CVR) PLAYBOOK + 鈴木 (IA) sitemap 修復を承認
3. **🆕 Phase 4 Step 1 — GA4 観測ダッシュボード準備** (未コミット / 2026-05-06)
   - 専門家会議 6 名招集 (SEO 田中 / CVR 佐藤 / IA 鈴木 / 行動経済学 教授 / インバウンド 金星 / Content 山本) → コンセンサス: **GA4 観測フェーズ最優先**、Phase 4 候補 A/B/C/D を一旦保留 (会議で 4 名が「観測なき積層」を懸念)
   - 山本 (Content) は Phase 4-B「覆面ラウンド記」を**自ら却下** (E-E-A-T Experience 偽装リスク) → 代替案「現役プロ・支配人インタビュー 5 本」を提示 (将来の Step 候補)
   - **Plan B (GA4 tracking v2.1)**: 既存 click handler を拡張 → `cta_position` 自動判定 (hero/ftv/sticky/price_featured/price_default/booking_grid/explore_nav/other) + 内部リンク用 `internal_nav_click` イベント新設
   - これにより **Phase 1A 逆流ナビ** と **Phase 3 Decoy 価格カード** が初めて計測可能に (これまで 2 施策の効果は未測定だった)
   - スクリプト: `scripts/inject_ga4_tracking.py` (冪等・dry-run・両ディレクトリ)
   - 展開: 196 ファイル自動置換 (バリアント B 系) + index.html 個別 Edit (バリアント A・既存 `function trackAffiliate` 温存・preview 検証で二重カウントなし確認)
   - 計測対象外: sitemap-guide.html (アフィリ・逆流ナビなしのため計測不要)
   - 検証: preview tool で 13 イベント × 3 言語発火確認・console エラーゼロ
   - ドキュメント新規: `GA4_DASHBOARD.md` (5 探索レポート定義 + 28 日観測スケジュール + カスタムディメンション 8 個登録手順) / `GSC_CANNIBALIZATION_GUIDE.md` (Phase 2 LP のカニバリ検出 + 重大カニバリ時の対応)
   - 観測期間: 14日 (最低) / 28日 (推奨) — **観測中の HTML 改修禁止** (効果測定の交絡因子防止・会議合意)
   - ユーザー側次タスク: GA4 管理画面でカスタムディメンション 8 個登録 (24-48h で反映)
2. **🆕 Phase 3 — Decoy + Default 価格カード再設計** (`289bb21` / 2026-05-05)
   - 教授/行動経済学提案を 31 標準コース × 3言語 = 93 価格グリッドに適用
   - HTML 構造変更ゼロ、CSS only で 4 つの介入:
     * Center-stage 効果: featured を視覚中央 (desktop) / 最上部 (mobile) に配置
     * Default 強調: border 2→3px、orange shadow、translateY(-6px)
     * BEST VALUE バッジ強化: 🌟emoji + overhanging 配置
     * Hick's Law 対策: Phase 1B sticky CTA と組み合せ
   - 倫理性: 「90%が選ぶ」マイクロコピーは GA4 実データなしのため除外(虚偽広告リスク回避)
   - スクリプト: `scripts/decoy_pricing_redesign.py` (冪等・dry-run対応)
   - 期待効果: featured カードへの視線集中 → CTR +30-50% / 成約率 2 倍 (教授予測)
2. **🆕 Phase 2 — 取引KW専用 SEO landing 3 ページ新設** (`6a03311` / 2026-05-05)
   - 田中健太郎/SEO 提案の高購買意図 KW を3ページで網羅
   - **book-fukuoka-cheap.html** (494行・24コース全件比較表): KW「福岡 ゴルフ 平日 安い」
   - **book-fukuoka-tomorrow.html** (413行・15コース大手チェーン優先): KW「福岡 ゴルフ 当日予約」
   - **book-fukuoka-solo.html** (418行・12コース★マッチ率付): KW「福岡 ゴルフ 1人予約」
   - **段階的実行**: 各ページ作成→チェッカーエージェント招集(ファクトチェック+SEO+CVR)→致命的問題修正→次ページ
   - 検出&修正済の致命的問題:
     * cheap: jalan_id 02347/02355 誤り(02341/02353に)・wakamiya 名称・aco/PGM フリーパス記述ミス
     * tomorrow: 「PGM 8コース」→「PGM 5+アコ 3」、福岡国際=宗像市・セブンミリオン=早良区
     * solo: 古賀/久山「福岡市」→「福岡近郊」・FAQ矛盾解消・「月3,000件」根拠ぼかし
   - 全ページ JSON-LD 3種(Article/Breadcrumb/FAQPage)・canonical/OGP・jalan deep link
   - sitemap.xml +3 (97 URLs) / sitemap-guide.html 3言語に追加
   - hub-budget.html「Quick Booking Guides 3選」セクション + index.html ②③ ブロックから内部リンク
   - 期待効果: 月+2-4kPV / CVR 2-3% で月+¥8-15万収益寄与
2. **🆕 Phase 1 — 逆流ナビ + CVR 改善 (専門家会議結果)** (`4c40600` / 2026-05-05)
   - **Phase 1A (鈴木玲奈/IA)**: 全 35 course-*.html × 3言語 = 105 セクションに「Explore More」逆流ナビ挿入
     - 5 エリアハブ (該当エリアをオレンジハイライト) + 4 ペルソナハブ + 3 ガイド
     - スクリプト: `scripts/inject_explore_nav.py` (冪等・dry-run対応)
     - 期待効果: ハブ受信 PR +30-50%・回遊率 +15-25%
   - **Phase 1B (佐藤美咲/CVR)**: 標準 30 コースに hero 内 CTA + sticky 価格込み + KO 楽天追加
     - Hero CTA: hero-badges 直後にオレンジ「📅 このコースを予約する」ボタン
     - Sticky CTA: hero-badge から最安値抽出して「📅 じゃらん ¥3,500〜」形式に
     - KO sticky: 1ボタン (Jalan のみ) → 2ボタン (Jalan + Rakuten・🇯🇵 マーカー保持)
     - 除外 4件: fukuokacc/wakamatsu (会員制)・akane/genkai (sticky 非表示)・自動 skip 1件: aburayama (Jalan 未掲載)
     - スクリプト: `scripts/cvr_enhance.py` (冪等・dry-run対応)
     - 期待効果: CVR 1.2% → 2.4%・月収益 +¥18-35k
   - **専門家会議**: SEO/CVR/IA/インバウンド/行動経済学/コンテンツの 6 名並列招集→議事録ベースで Phase 1 着手決定
2. **🆕 「How to Book」記事をサイト全体に接続** (`e0e6d64` / 2026-05-04)
   - Phase A バナー (45ファイル × 2dir = 90 files) の「coming soon」placeholder を実リンクに置換
   - 対象: 35 course pages + 5 area pages + 4 hub pages + index (EN+KO 両方)
   - hub-traveler.html: article-grid (EN/KO) 冒頭に featured カード追加 (orange border emphasis)
   - スクリプト: scripts/link_inbound_guide.py (再利用可能)
   - 結果: 記事への参照 1 → 48 ファイル
   - 期待効果: 全コースページから 1 hop で記事到達 → 行動経済学的「予約できる橋」が機能
2. **「How to Book Fukuoka Golf as a Foreigner」 EN/KO 記事新規** (`5540ac9` / 2026-05-04)
   - 戦略会議で次タスクと決定された記事を新規作成
   - book-fukuoka-golf-foreigner.html (976行・EN+KO で約3000語)
   - 構成: Hero / Why Fukuoka / 予約プラットフォーム比較 / 7ステップ予約手順 / 日本語12語表 / 当日の流れ / 推奨3コース(jalan deep link CTA) / FAQ7項目
   - SEO: Article + BreadcrumbList + FAQPage の JSON-LD・hreflang・canonical
   - sitemap.xml +1 (94 URLs) / sitemap-guide.html 3言語に追加
   - 推奨3コース: Saitozaki(gc02313) / Hisayama(gc02334) / Keya(gc02351) → jalan deep link CTA 6件
   - 期待効果: 月数百PV(EN+KO ロングテールSEO)+ASP承認時に CTA 即埋込可能
2. **akane へじゃらんCTA復活完了** (`698c901` / 2026-05-03)
   - 茜ゴルフクラブ (gc02344) の jalan booking-card を3言語の空 booking-grid に挿入
   - 楽天除外時に一緒に削除されていたが、じゃらん掲載確認後に復活
   - 期待効果: 月¥3-5k 追加収益
2. **じゃらんゴルフ Deep Link 化完了** (`9332513` / 2026-05-03)
   - 約690件のじゃらんトップURLをコース個別ページ (`https://golf-jalan.net/gc{ID}/`) へ deep link 化
   - 35コース分の jalan_id 全件収集 (WebSearch + golf-jalan.net prefecture page)
   - 単体: 910 件置換 / multi-course: 468 件置換 + 34 件除外CTA削除
   - 楽天 mapping との差分:
     * **akane** (gc02344): 楽天未掲載だがじゃらん掲載 → 現HTMLにCTA無く no-op (要復活検討・別タスク)
     * **aburayama**: 楽天 c_id=520392 だがじゃらん未掲載 → 16件削除 + sticky CTA を rakuten のみに変更
   - 残存トップページCTA 7件 (fees/beginner-cards/area-kitakyushu): コース文脈なし汎用CTA・意図的に保持
   - 期待効果: 楽天と並走で月¥30-50k 程度の追加収益見込み
2. **aburayama 旧名→新名 横断更新完了** (`245a0d7` / 2026-05-03)
   - 7ファイル × 3言語(JA/EN/KO) で「ララヒルズ油山(旧 油山ゴルフクラブ)」へ統一
   - 対象: access-aburayama / area-fukuokacity / hub-beginner / recommend / index / sitemap-guide / fees
   - IA推奨「新旧併記6ヶ月」に従い、タイトル/H1/structured data は新名、本文は併記
   - **recommend.html 事実訂正**: 18H Par72/山岳→10H ショート(canonical course-aburayama基準・3言語)
   - KO「라라힐즈」→「라라 힐스」統一(sitemap-guide.html含む)
   - 略称「油山GC/Aburayama GC」「物理看板」「Google Maps検索URL」は旧名のまま保持(SEO)
2. **3コンテンツ修正完了** (`c6a6436` / 2026-05-03)
   - aburayama → ララヒルズ油山に名称統一・2025リニューアルnotice
   - kokura → 株主会員制(ビジター枠あり)リブランディング+楽天/じゃらんCTA追加(8件/15件)
   - genkai → 営業中(2023リニューアル)+JGA Open開催notice、楽天/じゃらんは非掲載のためCTA除外継続+公式/GDO推奨
   - 4エージェント並列稼働: ファクトチェック×2 + CVR + IA
2. **🆕 楽天GORA Deep Link 化完了** (`82332dc` / 2026-05-03)
   - 約480件の楽天URLをコース個別ページへ deep link 化
   - A8.netフリーリンク (4P34KY+BW8O1) 利用
   - URL構造: `pc=https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{ID}`
   - 期待効果: クリック→予約 CVR 0.5-1% → 3-5%
2. **Phase B 完了** (`5eaa266`) — Jalan/楽天ボタンの EN/KO に🇯🇵(JP site) マーカー
3. **Phase A 完了** (`5f0888c`) — EN/KO セクション冒頭に「Japanese only」警告バナー
4. **index.html Pillar Page 化** (`a77b432`) — 1187→2831行・FAQ schema・Top Rankings・3-Step
5. **4ペルソナハブ作成** (`e13c6b4`) — beginner/traveler/business/budget

---

## 🆕 楽天GORA Deep Link 仕様（重要）

### URL テンプレート
```
https://rpx.a8.net/svt/ejp?
  a8mat=4B1D5J+4P34KY+2HOM+BW8O1                 ← フリーリンクコード
  &rakuten=y
  &a8ejpredirect=http%3A%2F%2Fhb.afl.rakuten.co.jp%2Fhgc%2F
    0eb4cf04.fd65a65c.0eb4cf05.fa3f041c
    %2Fa26040498058_4B1D5J_4P34KY_2HOM_BW8O1
    %3Fpc%3D{コース個別URL_2重エンコード}
    %26m%3D{コース個別URL_2重エンコード}
```

### コース個別URL
```
https://booking.gora.golf.rakuten.co.jp/guide/disp/c_id/{c_id}
```

### 既存スクリプト
- `scripts/deeplink_rakuten.py` — course-*.html 単体ファイル一括書き換え
- `scripts/deeplink_multi_course.py` — multi-course ファイル文脈推定書き換え
- `rakuten_gora_mapping.json` — c_id↔ファイル名マッピング (35コース・除外フラグ付き)

### 再実行方法
```bash
cd C:/Users/Owner/fukuoka-golf-guide
python scripts/deeplink_rakuten.py --dry-run        # 確認
python scripts/deeplink_rakuten.py                   # 適用
python scripts/deeplink_multi_course.py --dry-run    # 確認
python scripts/deeplink_multi_course.py              # 適用
```

---

## 🆕 じゃらんゴルフ Deep Link 仕様（重要）

### URL テンプレート
```
https://px.a8.net/svt/ejp?
  a8mat=4B1D5J+5JG8FM+36SI+BW8O2                  ← フリーリンクコード
  &a8ejpredirect=https%3A%2F%2Fgolf-jalan.net%2Fgc{ID}%2F
                                                  ← single URL encode
```

### コース個別URL
```
https://golf-jalan.net/gc{jalan_id}/   ※ ID は 5桁 (例: 02326)
```

### 既存スクリプト
- `scripts/deeplink_jalan.py` — course-*.html 単体ファイル一括書き換え
- `scripts/deeplink_multi_course_jalan.py` — multi-course ファイル文脈推定書き換え
- `jalan_golf_mapping.json` — jalan_id↔ファイル名マッピング (35コース)

### 再実行方法
```bash
cd C:/Users/Owner/fukuoka-golf-guide
python scripts/deeplink_jalan.py --dry-run            # 確認
python scripts/deeplink_jalan.py                       # 適用
python scripts/deeplink_multi_course_jalan.py --dry-run  # 確認
python scripts/deeplink_multi_course_jalan.py            # 適用
```

---

## 🚫 アフィリCTA 除外コース（楽天 / じゃらん 別管理・厳守）

**ファクトチェック2エージェント並列クロスチェック確定（2026-05-03）**

### 楽天GORA 除外 (4件)
| コース | 理由 | 状態 |
|--------|------|------|
| **course-fukuokacc** | 会員制（メンバー同伴/紹介必須）・GORAプラン非掲載 | 既にCTAなし ✓ |
| **course-wakamatsu** | 会員制・GORA予約不可 | 既にCTAなし ✓ |
| **course-akane** | 楽天GORA未掲載（あかねCC） | CTA削除済 ✓ |
| **course-genkai** | 2023/1〜長期クローズ表示中 (※ 要追跡) | CTA削除済 ✓ |

### じゃらんゴルフ 除外 (3件)
| コース | 理由 | 状態 |
|--------|------|------|
| **course-fukuokacc** | 会員制 | 既にCTAなし ✓ |
| **course-wakamatsu** | 会員制 | 既にCTAなし ✓ |
| **course-genkai** | 長期休場 | 既にCTAなし ✓ |
| **course-aburayama** | じゃらん未掲載 (10Hショート) | 9332513 で削除済 ✓ |

### 楽天⇔じゃらん 差分（重要・対応済）
- **akane** (gc02344): 楽天は除外だがじゃらんは掲載 → 698c901 で復活済 ✓
- **aburayama** (c_id=520392): 楽天は掲載だがじゃらんは未掲載 → 既にじゃらん削除済

**※ 注意**：以前 NEXT_SESSION.md に「福岡CC・若松・玄海」と書いていたが、**小倉CCは株主会員制でビジター枠あり**（土日¥19,014公表）のため CTA 維持。誤記訂正済。

---

## 📝 未完了タスク（優先順）

### ✅ 完了済 (2026-05-05) — `289bb21` (Phase 3)
- ~~**Phase 3: 教授デコイ価格カード再設計**~~ → 完了 (CSS only・倫理リスクゼロ版)
  - スクリプト: `scripts/decoy_pricing_redesign.py`

### ✅ 完了済 (2026-05-05) — `6a03311` (Phase 2)
- ~~**Phase 2: 田中SEO 取引KW 3 ページ新設**~~ → 完了 (cheap/tomorrow/solo)
  - 段階的実行: ページ作成→チェッカーAgent→致命的問題修正→次ページ
- 期待効果: 月+2-4kPV / +¥8-15万収益寄与

### ✅ 完了済 (2026-05-05) — `4c40600` (Phase 1)
- ~~**Phase 1A**: 全 35 コース×3言語に逆流ナビ挿入 (鈴木玲奈/IA 提案)~~ → 完了
- ~~**Phase 1B**: 標準 30 コースに hero CTA + sticky 価格 + KO 楽天 (佐藤美咲/CVR 提案)~~ → 完了
- 専門家会議 6 名招集→議事録ベースで決定
- スクリプト: `inject_explore_nav.py` + `cvr_enhance.py`

### 🟡 次に着手候補 (Phase 4 — 会議で議論済 + 2026-05-06 追加調査反映)

#### Phase 4-A (インバウンド) — 金星誠の方針再判定 (2026-05-06)
**事前調査済**: `i18n_course_compatibility.json` (35 コース全件・Tier 1-5 分類)
- Tier 1 (公式 KO 直対応): **wakamiya 1 コースのみ** ← 致命的に少ない
- Tier 2-3 (予約ポータル機械翻訳): 7 コース (Accordia: nijo/central/pheasant・PGM: fukuokakokusai/kitakyushu/moonlake/lakeside)
- Tier 4 (限定 EN のみ): 2 コース (hisayama 外部リンク / sevenmillion メニュー併記)
- Tier 5 (非対応): 25 コース

**金星 戦略推奨** (2026-05-06):
- **Option A**: バッジ実装 (6-8h) — Tier 別 3 種文言必須 (機械翻訳は明示・隠蔽炎上リスク)
  - 文言例: Tier 1「공식 한국어 페이지」(緑/星) / Tier 2-3「예약 사이트 한국어 (자동번역)」(黄) / Tier 4「영어 안내 가능」(青)
  - ROI 下方修正: KO CVR 0.5% → **0.8-1.0%** (当初予測 1.8% は楽観的・Tier 1 が 1 件のみ)
- **Option B (推奨)**: wakamiya 単独訴求 LP (5h) — 集中突破戦略
  - 「福岡で唯一の公式韓国語対応コース」差別化・韓国旅行ブログ被リンク獲得・SEO「후쿠오카 골프 한국어」1 位狙い
  - 設計書: `WAKAMIYA_KO_LP_DESIGN.md` (Day 28 GO 後すぐ実装可能な完成度・8 セクション LP 構造・KPI・リスク含む)
  - 韓国語草稿: `WAKAMIYA_KO_LP_DRAFT.md` (8 セクション + meta + footer・**ネイティブ校正必須** Lancers/Crowdworks で 1-2 万円程度)

**Day 28 観測判断基準**:
- KO セッション > 月 50 + 直帰率 < 70% → Option A 実装 GO
- KO セッション < 月 20 → **Option A 見送り・Option B (単独 LP) 優先**
- hisayama / sevenmillion (EN のみ) は別セグメント (台湾・香港・在日米軍家族) として扱う

#### その他 Phase 4 候補
- **山本誠一/編集**: 「現役プロ・支配人インタビュー 5 本」(山本案 E・覆面ラウンド記の代替案)
  - 工数 18-22h・E-E-A-T 強化・実名取材で被リンク獲得
- **GA4 観測フェーズ**: Phase 1-3 効果測定 (Day 14-28 進行中・`GA4_DASHBOARD.md` 参照)
- **Google AdSense**: 月 10,000 PV 突破まで保留 (現状アフィリ単価が AdSense の 30 倍)

#### 公式 URL 訂正候補 (調査で発見・観測終了後に course-*.html / access-*.html を修正)
- ito: itogolf.jp → ito-gc.com
- asoiizuka: asoiizuka-gc.jp → aigc.jp
- kyushugc: kyushu-gc.jp/yahata/ → kg-yahata.com

### ✅ 完了済 (2026-05-04) — `5540ac9`
- ~~「How to Book Fukuoka Golf as a Foreigner」 EN/KO 記事新規~~ → 完了
  - book-fukuoka-golf-foreigner.html (976行・EN+KO で約3000語)
  - 7セクション構成・推奨3コース jalan deep link CTA・FAQPage JSON-LD
  - sitemap.xml + sitemap-guide.html 3言語に登録

### ✅ 完了済 (2026-05-03 5回目) — `698c901`
- ~~akane へのじゃらんCTA 復活 (gc02344)~~ → 完了 (3言語 single-column booking-card)

### ✅ 完了済 (2026-05-03 4回目) — `9332513`
- ~~じゃらんゴルフ Deep Link 化 (約690件)~~ → 完了 (35コース全件マッピング)
  - jalan_golf_mapping.json + deeplink_jalan.py + deeplink_multi_course_jalan.py
  - aburayama: 削除 + sticky CTA 整理 / その他: deep link 化

### ✅ 完了済 (2026-05-03 3回目) — `245a0d7`
- ~~aburayama 旧名→新名 7ファイル横断更新~~ → 完了 (3言語・IA推奨併記方式)
  - access-aburayama.html / area-fukuokacity.html / hub-beginner.html
  - recommend.html (+ 18H→10H 事実訂正) / index.html / sitemap-guide.html / fees.html
- ~~KO表記「라라힐즈」→「라라 힐스」統一~~ → 完了

### ✅ 完了済 (2026-05-03 2回目)
- ~~course-genkai.html notice バナー追加~~ → 完了 (営業中・公式/GDO誘導)
- ~~course-aburayama.html ララヒルズ統一~~ → 完了 (本体ファイルのみ)
- ~~course-kokura.html リブランディング+CTA~~ → 完了

### 🟡 中優先：Phase C インバウンド改善
**ユーザー側作業 (ASP申請)**:
1. **GolfStay** (https://www.golfstay.jp/) — KO/EN/中対応・福岡30+カバー
   - 「お問い合わせ」から「アフィリエイト希望」連絡
   - 報酬 5-8%・申請1-2週間
2. **GoGolfNippon** (https://gogolfnippon.com/) — 米欧専門
3. **KKDay** (https://affiliate.kkday.com/) — 将来・台湾向け

**サイト側作業 (Claude Code が実行)**:
1. ASP承認後、EN/KO の Jalan/楽天 を **完全置換** (GolfStay/GoGolfNippon へ)
2. ~~**「How to book Fukuoka golf as a foreigner」記事** 新規作成 (EN/KO ・ ゼロ競合SEO枠)~~ → 完了 (5540ac9)
3. **「英語/韓国語予約可能コース」フィルター** 機能実装
4. **hub-international.html** 新設検討 (4→5ペルソナハブに昇格)
   - 「How to Book」記事を母体として展開可能

### 🟢 低優先
- [ ] GA4 で `click_affiliate` イベントの実数値検証（1〜2週間後）
- [ ] 汎用GORAトップ CTA（fees.html等4ファイル・約8件）を福岡県検索ページに変更検討
  - 候補URL: `https://search.gora.golf.rakuten.co.jp/?prefecture=40`

---

## 🎤 会議メンバー (継続使用可)

ユーザーが「会議で決めて」と言った際にエージェントとして招集する想定:

| 役割 | 名前 | 専門 |
|------|------|------|
| SEO | 田中健太郎 | KW戦略・トピッククラスタ・E-E-A-T |
| CVR | 佐藤美咲 | アフィリ最適化・年商3000万実績 |
| Content | 山本誠一 | ゴルフ雑誌元編集長・YouTube15万人 |
| IA | 鈴木玲奈 | サイト構造・PageRank・10年実績 |
| 行動経済学 | 教授 | サンクコスト・アンカリング・選択アーキテクチャ |
| ファクトチェック#1 | 鈴木一郎 | 1次調査・公式サイト確認 |
| ファクトチェック#2 | 中村麻衣 | 独立検証・反証 |
| インバウンド | 金星誠 | JTBグローバル10年・韓国/米国実績 |
| 国際決済 | David Chen | Klook元PM・5年経験 |

**⚠️ 重要原則** (前セッションで確立):
- コース情報は **必ず公式サイトで確認** してから掲載 (両ファクトチェッカーがクロスチェック)
- ハルシネーションされた架空コース掲載は厳禁
- 数値の誤りは即修正（小倉CC「会員制」表記の見直しなど）

---

## 🛠 重要ファイル・スクリプト

### スクリプト (`scripts/` 配下)
- `update_canonical.py` — 全HTMLにcanonicalタグ正規化
- `update_ogp.py` — og:url/og:image 正規化
- `generate_sitemap.py` — sitemap.xml再生成 (priority 0.9維持)
- `add_ftv_cta.py` — FV CTA strip 一括挿入
- `add_intl_notice.py` — Phase A: 国際通知バナー挿入
- `mark_jalan_jp_only.py` — Phase B: Jalan/楽天 ボタンマーカー
- 🆕 `deeplink_rakuten.py` — 楽天GORA deep link 化 (course-*.html)
- 🆕 `deeplink_multi_course.py` — multi-course ファイル deep link 化

### データファイル
- `course_data.json` — **【重要・絶対上書き禁止】** 全コース詳細データ (2255行・extract_course_data.py / generate_course_v2.py で使用)
- 🆕 `rakuten_gora_mapping.json` — 楽天GORA c_id マッピング (35コース)

### 参照ドキュメント
- `claude-code-domain-migration.md` — ドメイン移行の完全ランブック (v2.2)

### 引き継ぎメモ
- `C:\Users\Owner\Documents\新しいPJ\引き継ぎメモ.md` — 詳細な作業ログ

---

## 🚫 絶対の禁止事項

1. **GA4 タグ (`G-PENH0Z4VT7`) を絶対変更しない**
2. **CNAME ファイルを編集しない** (`fukuoka-golf-guide.com`)
3. **公式サイト確認なしでコース情報を追加しない** (ハルシネーション防止)
4. **アフィリCTA除外コース** (福岡CC・若松・あかね・玄海) に Jalan/楽天 CTA を載せない (公式のみ)
5. **本ドキュメント (`NEXT_SESSION.md`) を一括置換 script で書き換えない** (`fukuokacolor-web` は履歴用)
6. 🆕 **`course_data.json` を絶対上書きしない**（マスター 2255行・破壊事故あり 2026-05-03）
   - c_id マッピングは別ファイル `rakuten_gora_mapping.json` を使う

---

## 🎯 推奨される次セッションの最初の一手

**選択肢**:

### A. コンテンツ修正（高優先・短時間）
- genkai 休場 notice + aburayama 名称統一 + kokura 会員制表記+CTA追加
- 30〜60分で完了見込み

### B. じゃらんゴルフ deep link 化
- 楽天と同じ手法で約500件をdeep link化
- 全コースのjalan c_id収集が前提（30分〜）

### C. ASP承認待ちの間に「How to book as a foreigner」記事先行作成
- EN/KO で 1500語ずつ
- 競合ゼロのSEO金鉱
- 公開後 GolfStay 承認時に CTA を埋め込めば即収益化

### D. GA4 観測フェーズ
- 2-4週間データ蓄積
- Phase A/B/Deep link の効果測定
- 次の施策をデータドリブンで決定

### E. ユーザー指定の別タスク

---

## 💡 セッション開始時のテンプレ質問

次セッションで Claude Code 起動時に、ユーザーが以下を貼ると効率的:

```
NEXT_SESSION.md を読んでください。
今日は [A / B / C / D / その他] を進めたいです。
```

---

## 📈 期待されるサイト成長 (田中SEO予測)

| 期間 | PV予測 | 月収益予測 |
|------|------|------|
| 現状 (2026-05) | 500-1,500 PV/月 | ¥30-60k |
| 3ヶ月後 (2026-08) | 3,000-5,000 PV/月 | ¥80-120k |
| 6ヶ月後 (2026-11) | **8,000-15,000 PV/月** | **¥150-220k** |
| 月¥30万到達時期 | 8-10ヶ月 (2026-12〜2027-02) |

**Deep link 化の追加効果（2026-05-03 反映）**:
- CVR 5倍化で **月¥30-50k 上乗せの可能性**

**EN/KO 改善後の追加効果**:
- インバウンド客単価¥30-50k×CVR向上で **月+¥30-80k** 上乗せ可能性

---

**Good luck for the next session!** 🌟

ご不明な点があれば、各ファイル冒頭のコメントや過去のcommit messageを参照してください。
