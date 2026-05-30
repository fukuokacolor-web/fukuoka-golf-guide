# Phase 4 Day 28 キックオフ手順書

**対象日**: 2026-06-03 (Day 28・観測終了日)
**目標**: /observation-checkin 28 実行 → 30分以内に Phase 4 着手 1件を確定 → 当日 commit
**前提**: OBSERVATION_PLAYBOOK.md §5 判定マトリクスに従い、数値を見てから閾値を動かさない（確証バイアス禁止）

---

## 0. セッション開始時に読むファイル

```
1. NEXT_SESSION.md        ← 最新状態の確認
2. OBSERVATION_PLAYBOOK.md §5-6 ← 判定マトリクスと記入欄
3. 本ファイル             ← 当日の実装手順
```

---

## 1. 観測チェックイン (30分)

```
/observation-checkin 28
```

GA4 5レポートを自動取得し、§6 Day 28 記入欄を埋める。

**重要**: Day 28 当日に「数値を見て閾値を調整」することは**絶対禁止** (CLAUDE.md §6)。
事前確定スレッショルドで機械判定のみ。

---

## 2. 判定 → 着手項目の決定 (5分)

OBSERVATION_PLAYBOOK §5 のマトリクスを参照。以下のどれに該当するか確認:

| 着手項目 | 条件 | 準備状況 |
|---|---|---|
| **Task C** (GSC カニバリ修正) | LP PV が 100 未満 + Decoy HOLD/NO | 本ファイル §3 参照 |
| **Task B** (wakamiya KO LP デプロイ) | KO CTR が JA の 30% 未満 + GO | 本ファイル §4 参照 |
| **Task A** (Decoy 強化) | featured 比率 40-60% + N≥30 | 本ファイル §5 参照 |
| **延長 Day 42** | 全指標 HOLD + N 不足 | 6/17 に再判定 |

---

## 3. Task C: LP 3本 SEO 最適化 (1-2h)

### 3.1 対象ファイルと現状

| ファイル | 現 title (文字数) | 現 meta description | 推定問題 |
|---|---|---|---|
| `book-fukuoka-cheap.html` | 「福岡ゴルフ 平日¥6,000以下24コース最安比較｜福岡ゴルフ場ガイド」(34字) | 「福岡35コース中、平日¥6,000以下で予約できる24コース...」 | インデックス遅延 or KW ミスマッチ |
| `book-fukuoka-tomorrow.html` | 「福岡ゴルフ 当日・明日予約OK 15コース即枠取得ガイド｜福岡ゴルフ場ガイド」(39字) | 「福岡ゴルフ場の当日・明日予約に強い15コース...」 | インデックス遅延 |
| `book-fukuoka-solo.html` | 「福岡ゴルフ 1人予約マッチング率高い12コース完全ガイド｜福岡ゴルフ場ガイド」(41字) | 「福岡ゴルフ場の「1人予約」マッチング率が高い12コース...」 | インデックス遅延 |

### 3.2 GSC データ取得後の判定フロー

Day 28 当日に GSC → 検索パフォーマンス → ページフィルタで各 LP を確認:

```
- Impression > 100/月 かつ CTR < 2% → title を KW 含有に最適化
- Impression < 50/月 → インデックス問題 → まず URL検査 → 再インデックスリクエスト
- Position < 15 かつ CTR < 3% → meta description に CTA 追加
- 他ページとクエリ重複 (Pos < 30 複数ページ) → 重複 H2 差別化
```

### 3.3 改善案 (GSC 確認後に調整)

**book-fukuoka-cheap.html** — 想定 KW「福岡 ゴルフ 格安」「福岡 ゴルフ 平日 安い」

```
現 title: 福岡ゴルフ 平日¥6,000以下24コース最安比較｜福岡ゴルフ場ガイド
改 title: 福岡ゴルフ格安まとめ｜平日¥3,000台〜24コース最安値比較【2026年版】
      ↑ 「格安」を前方に / 年版を追加 / 文字数 35字

現 meta: 福岡35コース中、平日¥6,000以下で予約できる24コース最安価格順に完全比較...
改 meta: 福岡ゴルフ格安ランキング。平日¥3,000台〜¥6,000以下24コースを最安値順に徹底比較。
         じゃらんゴルフ deep link で今すぐ空き確認。料金・コース特徴・穴場コースも掲載。
```

**book-fukuoka-tomorrow.html** — 想定 KW「福岡 ゴルフ 当日 予約」

```
現 title: 福岡ゴルフ 当日・明日予約OK 15コース即枠取得ガイド｜福岡ゴルフ場ガイド
改 title: 福岡ゴルフ当日予約できるコース15選【今日・明日OK】じゃらん即枠ガイド
      ↑ 「当日予約」を先頭 / 「今日・明日」明示 / 38字
```

**book-fukuoka-solo.html** — 想定 KW「福岡 ゴルフ 一人」「ひとり ゴルフ 福岡」

```
現 title: 福岡ゴルフ 1人予約マッチング率高い12コース完全ガイド｜福岡ゴルフ場ガイド
改 title: 福岡ゴルフ一人予約【2026年版】マッチング率高い12コースとじゃらんの使い方
      ↑ 「一人予約」強調 / 年版追加 / 41字
```

### 3.4 内部リンク追加 (観測終了後に実施可能)

以下のページから LP へのリンクを追加 (観測フェーズ終了後):

| 送り出しページ | 追加リンク先 | アンカーテキスト案 |
|---|---|---|
| `hub-budget.html` | `book-fukuoka-cheap.html` | 「24コース格安比較表はこちら →」 |
| `hub-traveler.html` | `book-fukuoka-solo.html` | 「ひとり参加OKコース一覧 →」 |
| `fees.html` | `book-fukuoka-cheap.html` | 「平日格安コースまとめ →」 |
| `index.html` | `book-fukuoka-tomorrow.html` | 「今日・明日で予約できるコース →」 |

### 3.5 実装コマンド (Day 28 当日)

```bash
# dry-run で確認
python scripts/phase4_lp_title_fix.py --dry-run

# 承認後に実行
python scripts/phase4_lp_title_fix.py

# commit
git add book-fukuoka-cheap.html book-fukuoka-tomorrow.html book-fukuoka-solo.html
git commit -m "perf(seo): LP3本 title/meta 最適化 (Phase 4 Task C)"
git push origin main
```

---

## 4. Task B: book-wakamiya-ko.html デプロイ (30分 + 校正待ち)

**現状**: `book-wakamiya-ko.html` は 2026-05-29 に作成済み・push済み

### 4.1 Day 28 当日にやること

```
① GSC で book-wakamiya-ko.html が既にインデックス済か確認
② KO ネイティブ校正の手配 (Lancers/Crowdworks ¥1.5万・所要 3-5 日)
③ Naver Webmaster Tools へのサイト登録: https://searchadvisor.naver.com/
④ sitemap.xml が既に book-wakamiya-ko.html を含むことを確認 ← ✅ 済み (priority 0.8)
```

### 4.2 Naver 登録手順 (5分)

```
1. https://searchadvisor.naver.com/ → ログイン (Naver アカウント必要)
2. 「사이트 등록」→ https://fukuoka-golf-guide.com を入力
3. HTML ファイル認証 or meta タグ認証でオーナー確認
4. サイトマップ送信: sitemap.xml URL を入力
```

### 4.3 校正発注テンプレート (Lancers 用)

```
【依頼内容】
韓国語ウェブページの校正・自然な表現への修正

【対象ファイル】
book-wakamiya-ko.html (約 38KB・韓国語のみ)

【依頼内容】
1. 自然な韓국語表現への修正（日本語直訳感の除去）
2. 존댓말（습니다体）の統一確認
3. 골프 관련 전문 용어 정확성 확인
4. 고유명사 표기 통일（와카미야 / 미야와카 / Trial Golf 等）
5. CTA 문구의 자연스러운 한국어 표현

【予算】 ¥10,000-15,000
【納期】 3-5日
【ファイル】 HTML ファイル送付（テキスト部分のみ修正可）
```

---

## 5. Task A: Decoy 価格カード強化 (N≥30 の場合のみ)

**条件**: Day 28 で click_affiliate(price_featured + price_default) N ≥ 30

現状 Day 14 で N=4 → N=30 到達は楽観的に見て Day 50-60 以降か。
**Day 28 では多くの場合 HOLD のまま。** N 不足なら Task A は着手しない。

着手条件を満たした場合の実装:
```
# CSS のみ変更・冪等スクリプト
python scripts/decoy_pricing_redesign.py --dry-run
python scripts/decoy_pricing_redesign.py
```

---

## 6. Day 28 当日タイムライン

| 時刻 | 作業 | 所要時間 |
|---|---|---|
| T+0 | `/observation-checkin 28` 実行 | 30分 |
| T+30 | 判定マトリクス確認 → 着手項目確定 | 5分 |
| T+35 | GSC で LP 3本インデックス確認 | 10分 |
| T+45 | **Task C 実行** (title/meta 修正) | 60分 |
| T+105 | **Task B** Naver 登録 + 校正発注 | 20分 |
| T+125 | NEXT_SESSION.md + OBSERVATION_PLAYBOOK §6 更新 | 10分 |
| T+135 | commit + push | 5分 |
| T+140 | **完了** | — |

---

## 7. 最悪ケース (全 HOLD / N 不足)

判定マトリクスで全項目 HOLD の場合:

```
着手判断: 延長 Day 42 (6/17)
実施内容:
  - book-wakamiya-ko.html の Naver 登録のみ実行 (観測に非干渉)
  - GSC インデックス未登録ページの再登録リクエスト
  - 次回 Day 42 で同判定フロー再実行
```

---

## 8. scripts/phase4_lp_title_fix.py の事前確認

以下のスクリプトを Day 28 前に作成済み:

```
C:/Users/Owner/fukuoka-golf-guide/scripts/phase4_lp_title_fix.py
```

作成状況: **未作成** → Day 28 前に作成予定 or Day 28 当日に作成
（GSC の実データを見てから title を確定するため、Day 28 直前に作成が望ましい）

---

## 9. 禁止事項 (Day 28 当日)

- ❌ 「数値を見て閾値を調整」しない
- ❌ Phase 4 未決定なのに HTML を改修しない  
- ❌ `course_data.json` を触らない
- ❌ GA4 タグ `G-PENH0Z4VT7` を変更しない
- ❌ CLAUDE.md / NEXT_SESSION.md を一括 script で書き換えない

---

*最終更新: 2026-05-29*
