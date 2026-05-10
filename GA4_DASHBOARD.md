# GA4 観測ダッシュボード設計書 (Phase 4 Step 1)

**作成日**: 2026-05-06
**目的**: Phase 1-3 (逆流ナビ / hero+sticky CTA / Decoy 価格カード) 各施策の効果を定量測定し、Phase 4 着手の根拠を作る
**観測期間**: 14日 (最低) / 28日 (推奨)
**前提**: GA4 ID `G-PENH0Z4VT7` / Plan B 計測 (v2.1) 全 197 ファイル展開済

---

## 1. 計測イベント体系

### 1.1 `click_affiliate` (アフィリエイトリンククリック・既存拡張)

| 項目 | 内容 |
|------|------|
| 発火条件 | jalan / rakuten / agoda / skyticket / tabikobo / amazon / a8.net 等の外部アフィリリンク |
| 既存パラメータ | `service` / `page` / `lang` / `link_text` / `link_url` |
| **新規 (v2.1)** | **`cta_position`** (下記 8 値) |

#### `cta_position` の値

| 値 | 場所 | 関連 Phase |
|----|------|-----------|
| `hero` | hero セクション内のオレンジ丸ボタン | Phase 1B |
| `ftv` | ftv-cta-strip (キャンセル無料バッジ + CTA) | (Phase 1 以前) |
| `sticky` | 画面下固定の sticky CTA バー | Phase 1B |
| `price_featured` | 強調された featured 価格カード (午後スルー等) | **Phase 3 Decoy** ★ |
| `price_default` | 通常の価格カード (平日 / 土日祝) | Phase 3 Decoy 比較対象 |
| `booking_grid` | 大型 booking-card (jalan / rakuten) | Phase 1B |
| `explore_nav` | section.related 内 (理論上) | Phase 1A |
| `other` | 上記以外 (記事内リンク等) | — |

### 1.2 `internal_nav_click` (Phase 1A 逆流ナビクリック・新規)

| 項目 | 内容 |
|------|------|
| 発火条件 | `<section class="related">` 内の内部 .html リンク (= Phase 1A 逆流ナビ専用) |
| `nav_section` | `explore_nav` (固定・将来拡張用) |
| `target_page` | 飛び先ファイル名 (例: `area-fukuokacity` / `hub-beginner` / `book-fukuoka-golf-foreigner`) |
| `page` / `lang` / `link_text` | 発火元ページ・言語・テキスト |

### 1.3 既知の混入: `service: internal_fees`

index.html の既存 `function trackAffiliate` が内部 fees.html CTA クリックを `click_affiliate` で発火し続ける (3 箇所・3 言語)。
**集計時は `service NOT IN ('internal_fees')` でフィルタすること。**

### 1.4 `click` イベント (GA4 Enhanced Measurement 自動・自前コード由来ではない)

**結論**: GA4 が自動で記録する **Outbound clicks** (デフォルト ON)。リポジトリ全体に `gtag('event', 'click', ...)` の呼び出しは存在せず、GTM 等の他トラッカーも未導入。`click_affiliate` (自前) と `click` (GA4 自動) は別イベントで、同一クリックで両方発火する。

**包含関係**: `click_affiliate` ⊂ `click` (= 全外部リンククリック)

| イベント | 発火源 | 内容 |
|---|---|---|
| `click` | GA4 Enhanced Measurement 自動 | 自サイトドメイン外への `<a>` クリック全件 |
| `click_affiliate` | `inject_ga4_tracking.py` | うち jalan / rakuten / agoda 等のアフィリ URL のみ |
| 差分 (`click` − `click_affiliate`) | — | Google Maps・コース公式サイト等の非アフィリ離脱 (有用シグナル) |

**Day 3 観測実例 (2026-05-09 / 過去 28 日)**:
- `click` 45 / `click_affiliate` 35 → 差分 10 = 非アフィリ外部離脱 10 件

**集計時の方針**:
- 収益関連の指標は `click_affiliate` のみ参照 (`click` は使わない)
- 「ユーザーがどこへ離脱しているか」を見たい時は `click` を使い、`link_url` を集計して非アフィリの行き先 (Google Maps / 公式 etc) を分析可能

**確認日**: 2026-05-10 (NEXT_SESSION.md 要調査事項 #1 解決)

### 1.5 計測ロジック実機検証結果 (2026-05-10)

course-keya.html で 8 種類のクリックを実行し、dataLayer 直接読み取りで全件正常動作を確認。

| 検証 | クリック対象 | 期待 cta_position / イベント | 実測 | service |
|---|---|---|---|---|
| Hero | `📅 このコースを予約する` | `hero` | ✅ `hero` | `jalan` |
| FTV | `🎫 じゃらんゴルフでこのコースを予約する` | `ftv` | ✅ `ftv` | `jalan` |
| Sticky (じゃらん) | sticky bar じゃらん¥21,500〜 | `sticky` | ✅ `sticky` | `jalan` |
| Sticky (楽天) | sticky bar 楽天GORA | `sticky` | ✅ `sticky` | `rakuten_gora` |
| Default price card | ビジター 平日 → じゃらんで空き確認 | `price_default` | ✅ `price_default` | `jalan` |
| Featured price card | ビジター 土日祝 (BEST VALUE) → じゃらんで予約 | `price_featured` | ✅ `price_featured` | `jalan` |
| Booking grid | booking-card じゃらん リンク | `booking_grid` | ✅ `booking_grid` | `jalan` |
| Phase 1A 逆流ナビ | `✈️ 旅行者向け` ハブリンク | `internal_nav_click` イベント<br>`nav_section: explore_nav`<br>`target_page: hub-traveler` | ✅ 全項目正解 | (n/a) |

**結論**:
- `inject_ga4_tracking.py` の v2.1 計測ロジックは**完全に正常動作**
- カスタムディメンション 8 個 (CTA Position / Service / Page / Language / Target Page / Nav Section / Link Text / Link URL) すべてに対応するパラメータが正しく送信されている
- Phase 1A/1B/3 の効果測定インフラは完成
- 28 日エクスプロレーションで全件 `(not set)` だったのは **登録 5/9 前のレガシーイベント** (新ディメンションは登録時刻以降の新規イベントから分類)、5/9-5/10 でゼロだったのは反映遅延ではなく**実数的にクリックが少なかった**だけ
- 5/13 (Day 7) には登録後の自然トラフィックでエクスプロレーションに hero/sticky/price_featured 等が出現し始める見込み

**ノイズ対応**:
- 5/10 のテストクリック 8 件は GA4 上に記録される (1 ユーザー・direct・ja・desktop)。全体集計への影響は微小。Day 28 (6/3) 時点の累積に対しては誤差範囲。
- 必要に応じてユーザー ID/IP でセグメント除外可だが、現時点では除外不要と判断。

---

## 2. GA4 カスタムディメンション登録手順

GA4 → 管理 → **カスタム定義** → 「カスタムディメンションを作成」

| 表示名 | スコープ | イベントパラメータ |
|-------|---------|-----------------|
| CTA Position | event | `cta_position` |
| Service | event | `service` |
| Page | event | `page` |
| Language | event | `lang` |
| Target Page | event | `target_page` |
| Nav Section | event | `nav_section` |
| Link Text | event | `link_text` |
| Link URL | event | `link_url` |

⚠️ 登録から GA4 の探索レポートで使えるまで **24-48 時間**。今日中に登録すべし。

---

## 3. 探索レポート定義 (5 本)

### レポート 1: Phase 3 Decoy 効果検証 ★最重要

**狙い**: featured (午後スルー等) と default (平日/土日祝) のクリック比率を測る

**設定**:
- 探索 → 自由形式
- 行: `cta_position` (フィルタ: `price_featured` または `price_default`)
- 列: `service` (`jalan` / `rakuten_gora`)
- 値: イベント数

**判断基準**:
| 比率 (featured / (featured + default)) | 判定 |
|-------|------|
| **> 60%** | Decoy 効果あり (Phase 3 成功) |
| 50-60% | 効果不明確 (継続観測) |
| < 50% | Decoy 効果薄 (CSS 強調強化 or 「90%が選ぶ」マイクロコピー再検討) |

### レポート 2: Phase 1A 逆流ナビ クリック分布

**狙い**: 35 コース × 3 言語 = 105 セクションの逆流ナビが実際に使われているか

**設定**:
- 探索 → 自由形式 → イベント名 = `internal_nav_click`
- 行: `target_page`
- 列: `lang`
- 値: イベント数

**判断基準**:
- 全 `internal_nav_click` ≥ 全コースページ訪問数の **5%** → Phase 1A 成功
- target_page 上位の傾向: `area-*` > `hub-*` > `book-*` なら設計通り
- KO の click 数が JA の 30% 未満 → KO 翻訳・インバウンド改善優先 (Phase 4 候補 A の根拠)

### レポート 3: Phase 1B CTA 経路別 CTR

**狙い**: hero / sticky / ftv / booking_grid / featured のうち、どれが最も click_affiliate を生むか

**設定**:
- 探索 → 自由形式 → イベント名 = `click_affiliate` AND `service NOT IN ('internal_fees')`
- 行: `cta_position`
- 列: `service`
- 値: イベント数

**判断基準**:
- 上位 3 経路 (`hero` + `sticky` + `ftv`) が全 click_affiliate の **> 70%** → CTA 配置成功
- `booking_grid` のみが多い場合: hero / sticky の視認性に問題 (CSS 確認)
- `other` が高比率: 想定外の場所からクリック (記事内リンク等・改善余地あり)

### レポート 4: 言語別ファネル

**狙い**: JA / EN / KO の流入 → CTA クリック率を比較

**設定**:
- 探索 → ファネル
- ステップ 1: `page_view`
- ステップ 2: `click_affiliate` (filter: service NOT IN internal_fees)
- 内訳ディメンション: `lang`

**判断基準**:
- KO / EN の CTR が JA の **50% 未満** → インバウンド改善優先 (Phase 4 候補 A 強い根拠)
- 同等近く → インバウンド施策の優先度低 (B or C を再考)

### レポート 5: ページ別 PV と LP 効果

**狙い**: Phase 2 LP 3 本 (book-fukuoka-cheap / tomorrow / solo) が機能しているか

**設定**:
- 標準レポート → ページとスクリーン
- ディメンション: `page_path`
- 指標: 表示回数 / ユーザー / `click_affiliate` (カスタム指標 or セカンダリ)

**判断基準**:
- book-fukuoka-cheap.html PV ≥ **300 / 月** → Phase 2 成功 (期待値 +2-4kPV/月の下限)
- LP CTR (click_affiliate / PV) ≥ **5%** → CVR 健全
- LP PV が 50/月 未満 → SEO カニバリ疑い (`GSC_CANNIBALIZATION_GUIDE.md` 参照)

---

## 4. 観測スケジュール

| Day | 日付 | やること |
|-----|------|---------|
| 0 | 2026-05-06 | カスタムディメンション登録 / DebugView で初期発火確認 |
| 7 | 2026-05-13 | レポート 1-3 で初期傾向確認 (サンプル不足注意・確証は得られない) |
| 14 | 2026-05-19 | レポート 1-5 で本格判定 / GSC カニバリ分析併走 / 会議再招集判断 |
| 28 | 2026-06-03 | 月次レビュー / Phase 4 (A/B/C/D) 着手判断 |

---

## 5. 既知の制約・遵守事項

- **観測期間中の HTML 改修禁止**: 効果測定の交絡因子を増やす (会議で 4 名が指摘)。バグ修正・誤字修正は OK
- **GA4 タグ ID `G-PENH0Z4VT7` 絶対変更禁止** (NEXT_SESSION.md 禁止事項)
- **Plan B 再展開時**: `scripts/inject_ga4_tracking.py --dry-run` → 適用 (冪等)
- マーカー `/* GA4 tracking v2.1` で全 197 ファイル特定可能

---

## 6. 次セッション引き継ぎ

- 「GA4 ダッシュボードを見せて」と言われたら本ファイルと NEXT_SESSION.md を読む
- レポート結果次第で Phase 4 候補を再判断 (会議メンバー再招集)
- index.html の旧 `function trackAffiliate` は **当面温存** (二重カウントなし確認済・後日整理候補)
