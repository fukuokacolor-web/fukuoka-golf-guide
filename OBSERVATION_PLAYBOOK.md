# 📊 観測フェーズ判定プレイブック (Phase 1-3 効果測定)

**作成日**: 2026-05-10 (Day 0+4)
**作成**: 専門家会議 (佐藤美咲/CVR 提案・5名合議承認)
**目的**: Day 7 (5/13) / Day 14 (5/19) / Day 28 (6/3) の観測判定を「事前確定スレッショルド + 30 分判定フロー」で機械的に処理し、確証バイアスを排除する
**観測期間**: 2026-05-09 (カスタムディメンション登録日) 〜 2026-06-03 (Day 28)
**前提**: HTML 改修禁止 (会議合意・観測中の交絡因子防止)・GA4 v2.1 計測検証完了 (2026-05-10)

> **✋ 使い方**: Day 7/14/28 各日に本ファイルを開き、上から順に GA4 URL を踏んで「結果記入欄」を埋め、最下部の判定マトリクスに沿って自動判定する。議論余地を残さない。

---

## 1. 既存ベースライン (Day 3 観測 / 2026-04-12〜2026-05-08 / 28日累計)

| 指標 | Day 3 累計 | 月換算 | 注記 |
|---|---|---|---|
| page_view | 303 | 325 | 7日 PV 103 = 月 442 (前週ピーク) |
| session_start | 163 | 175 | — |
| user_engagement | 163 | 175 | engaged_users 34 |
| scroll | 132 | 141 | 90% スクロール到達 |
| first_visit | 99 | 106 | ユーザー 97 |
| **`click_affiliate` (自前)** | **35** | **38** | **登録前データ (cta_position 全件 not set)** |
| `click` (GA4 自動) | 45 | 48 | うち 35 = click_affiliate / 差分 10 = 非アフィリ外部離脱 |
| `internal_nav_click` (自前) | 3 | 3 | 登録前データ (target_page 全件 not set)・1 ユーザー |
| アクティブユーザー (7日) | 27 | — | 前週比 ▼61.4% |

**国別 (7日)**: Japan 9 / United States 8 / Germany 3 / South Korea 2 / Poland 2 / Canada 1 / Netherlands 1
**流入 (7日)**: Direct 34 / Organic Search 8 / Referral 5
**デバイス (28日 click_affiliate)**: desktop 27 / mobile 8

### ⚠️ ベースラインの注意点

- **5/9 カスタムディメンション登録**前のイベントは GA4 仕様で `cta_position`/`target_page` 等のディメンション値が**全件 `(not set)`** として記録される (再分類されない)
- → Phase 1A/1B/3 の効果測定に使えるデータは **5/9 以降の新規イベントのみ**
- → 月 38 件ペースで観測スタートしたとして、5/9-6/3 の 25 日間で累積 **~31 件** が期待値 (点推定)
- → **N 不足リスク**は最初から織り込む必要がある

---

## 2. 必要サンプルサイズ計算 (二項検定)

### 2.1 Phase 3 Decoy 効果検証 (featured vs default)

| 検出したい効果 | 仮説 | 必要 N | 25 日で達成可能性 |
|---|---|---|---|
| 60% vs 50% (薄い差) | H0: p=0.5, H1: p=0.6, α=0.05, power 80% | **~153** | **不可能** (期待値 ~31 × 80% = 25 件) |
| 65% vs 50% (中程度) | 同上, p=0.65 | **~70** | 厳しい |
| 70% vs 50% (大きい) | 同上, p=0.70 | **~38** | 達成可能 |

### 2.2 実用判定ルール (会議合議)

統計的厳密性に固執すると判定不能になるため、**ヒューリスティック判定**を採用:

| N (price_featured + price_default) | featured 比率 | 判定 |
|---|---|---|
| ≥ 30 | ≥ 65% | **GO** (Decoy 効果あり・Phase 3 成功) |
| ≥ 30 | 55-64% | **HOLD** (観測延長 Day 42 / 効果不明確) |
| ≥ 30 | < 55% | **NO** (Decoy 効果薄・CSS 強化または「90%が選ぶ」マイクロコピー再検討) |
| < 30 | — | **観測延長 Day 42 (6/17)** |

### 2.3 N 不足時の自動延長基準

- Day 28 (6/3) の N (price_featured + price_default) を確認
- N < 30 → Day 42 (6/17) まで自動延長
- Day 42 でも N < 20 → 観測継続を諦め、別指標 (CTR / 滞在時間) で代替判定 → 専門家会議再招集

---

## 3. 5 探索レポート × 事前確定スレッショルド

### レポート 1 (★最重要): Phase 3 Decoy 効果

**GA4 URL**: 探索 → 自由形式 → `cta_position` × `service` (詳細は GA4_DASHBOARD.md §3 レポート 1 参照)

**設定**: 行=`cta_position` (フィルタ: price_featured または price_default) / 列=`service` / 値=イベント数 / 期間=**5/9 以降**

**判定**:
| N (合計) | featured 比率 | 判定 | 次手 |
|---|---|---|---|
| ≥ 30 | ≥ 65% | ✅ **GO** | Phase 3 を維持・Decoy 強化案を将来候補化 |
| ≥ 30 | 55-64% | ⏸ **HOLD** | Day 42 まで延長観測 |
| ≥ 30 | < 55% | ❌ **NO** | featured カードの CSS 強化 (border 4px / glow / 大型化)・「90%が選ぶ」マイクロコピー導入検討 (倫理性は GA4 実績で再評価可) |
| < 30 | — | ⏳ **延長** | Day 42 まで観測継続 |

### レポート 2: Phase 1A 逆流ナビ クリック分布

**設定**: イベント名=`internal_nav_click` / 行=`target_page` / 列=`lang` / 値=イベント数 / 期間=**5/9 以降**

**判定**:
| 指標 | スレッショルド | 判定 |
|---|---|---|
| 全 internal_nav_click / 全 course-* PV | ≥ 5% | ✅ **GO** (Phase 1A 成功・回遊率改善実証) |
| 全 internal_nav_click / 全 course-* PV | 2-5% | ⏸ **HOLD** (継続観測・部分的成功) |
| 全 internal_nav_click / 全 course-* PV | < 2% | ❌ **NO** (逆流ナビが視認されていない・ファーストビュー上方移動 or デザイン強化を将来検討) |
| target_page 上位の傾向 | `area-*` > `hub-*` > `book-*` | 設計通り (合格) |
| KO の internal_nav_click / JA の internal_nav_click | < 30% | ⚠️ KO 翻訳・インバウンド改善優先 (Phase 4 候補 A 強い根拠) |

### レポート 3: Phase 1B CTA 経路別 CTR

**設定**: イベント名=`click_affiliate` AND `service NOT IN ('internal_fees')` / 行=`cta_position` / 列=`service` / 期間=**5/9 以降**

**判定**:
| 指標 | スレッショルド | 判定 |
|---|---|---|
| (hero + sticky + ftv) 比率 | ≥ 70% | ✅ **GO** (CTA 配置成功・想定どおり) |
| (hero + sticky + ftv) 比率 | 50-70% | ⏸ **HOLD** (許容範囲・最適化余地あり) |
| (hero + sticky + ftv) 比率 | < 50% | ❌ **要見直し** (booking_grid のみ多 = hero/sticky 視認性問題 / other 多 = 想定外位置からクリック) |
| `other` の比率 | > 15% | ⚠️ 想定外位置の特定要 (link_text / link_url で深掘り) |
| service: jalan vs rakuten_gora | jalan 優勢 (60%以上) | 想定通り (じゃらん deep link 経由が主収益源) |

### レポート 4: 言語別ファネル

**設定**: 探索 → ファネル / ステップ1=`page_view` / ステップ2=`click_affiliate` / 内訳=`lang` / 期間=**5/9 以降**

**判定**:
| 指標 | スレッショルド | 判定 |
|---|---|---|
| KO_CTR / JA_CTR | ≤ 50% | ⚠️ **インバウンド改善優先** (Phase 4-A or 4-B 強い根拠) |
| KO_CTR / JA_CTR | 50-80% | ⏸ **継続観測** (許容範囲) |
| KO_CTR / JA_CTR | > 80% | ✅ **インバウンド施策の優先度低** (Phase 4 別候補を再考) |
| EN_CTR / JA_CTR | ≤ 50% | ⚠️ EN 流入の質 or LP の問題 (How to Book 記事の効果検証要) |
| KO セッション数 | > 50 / 月 | Phase 4-B (wakamiya KO LP) Option A (Tier 別バッジ全件) GO |
| KO セッション数 | < 20 / 月 | Phase 4-B Option B (wakamiya 単独 LP) 優先 |

### レポート 5: ページ別 PV と LP 効果

**設定**: 標準レポート → ページとスクリーン / ディメンション=`page_path` / 指標=表示回数 / ユーザー / `click_affiliate` (セカンダリ) / 期間=**5/9 以降の月換算**

**判定**:
| ページ | 指標 | スレッショルド | 判定 |
|---|---|---|---|
| book-fukuoka-cheap.html | PV | ≥ 300 / 月 | ✅ Phase 2 成功 (期待値 +2-4kPV/月の下限) |
| book-fukuoka-cheap.html | PV | 100-299 / 月 | ⏸ HOLD (SEO 順位上昇継続中の可能性) |
| book-fukuoka-cheap.html | PV | < 100 / 月 | ❌ SEO カニバリ疑い → `GSC_CANNIBALIZATION_GUIDE.md` 適用 (田中タスク C 連動) |
| book-fukuoka-tomorrow.html | PV | ≥ 200 / 月 | ✅ 成功 |
| book-fukuoka-solo.html | PV | ≥ 200 / 月 | ✅ 成功 |
| LP CTR (click_affiliate / PV) | ≥ 5% | ✅ CVR 健全 |
| LP CTR | < 3% | ❌ 改善余地 (CTA 視認性・コンテンツ訴求力) |

---

## 4. Day 7 / 14 / 28 実行手順

### Day 7 (2026-05-13・初期傾向確認)

**所要時間**: 30 分
**目的**: サンプル少数前提で「異常値検出のみ」(本格判定はしない)

1. **GA4 → リアルタイム → 概要** で当日の click_affiliate 発火数を確認 (5 分)
2. **レポート 1-3** で 5/9 以降の累計を確認 (15 分)
3. **本ファイル §6「結果記入欄 Day 7」**に下記を埋める:
   - 全 click_affiliate 件数 (5/9-5/13)
   - cta_position 上位 3 値と件数
   - internal_nav_click 件数
   - 異常値の有無 (ゼロ件継続・想定外位置からのクリックの集中等)
4. 異常があれば **専門家会議再招集**、なければ「観測継続」とコメントして終了 (5 分)

⚠️ **Day 7 では GO/NO 判定しない**。N 不足が前提・スレッショルド適用は Day 14 以降。

### Day 14 (2026-05-19・本格判定 + GSC カニバリ分析)

**所要時間**: 60 分
**目的**: レポート 1-5 で初の本格判定 + GSC エクスポート (田中タスク C 連動)

1. **レポート 1-5** を順に開いて結果記入欄 Day 14 を埋める (30 分)
2. **§3 のスレッショルド表に沿って GO/HOLD/NO/延長 を機械的に記入** (10 分)
3. **GSC** で Phase 2 LP 3 本 + 競合候補 (hub-budget/fees/hub-traveler/recommend) の Page × Query を CSV エクスポート → 田中タスク C へ連携 (15 分)
4. 判定結果を NEXT_SESSION.md に転記 → 必要なら会議再招集 (5 分)

### Day 28 (2026-06-03・最終判定 + Phase 4 着手判断)

**所要時間**: 30 分 (本ファイルが完備されているため・佐藤の主目的)
**目的**: 全レポート最終判定 → 6/3 中に Phase 4 着手 1 件確定 → 即実装

1. **レポート 1-5** 結果記入欄 Day 28 を埋める (10 分)
2. **判定マトリクス §5** で Phase 4 着手候補を機械的に決定 (10 分)
3. **NEXT_SESSION.md 更新** + 必要なら会議再招集 (10 分)
4. **6/3 当日中**: 田中タスク C の Title/H2/内部リンク改修案を 1 commit で投入 (改修案完成済前提・実装 1-2 h)

---

## 5. Day 28 判定マトリクス → Phase 4 着手判断

5/13 と 5/19 の中間判定を経た上で、Day 28 に下記マトリクスで Phase 4 着手を決定する。**論理 AND** で複数条件を結合し、最も強いシグナルを優先。

| Day 28 観測結果 | Phase 4 着手判断 | 着手内容 |
|---|---|---|
| Decoy NO + LP-cheap PV < 100 | **C 着手** | GSC カニバリ修正 (Title/H2/内部リンク) を 1 commit |
| Decoy GO + LP-cheap PV ≥ 300 | **A 着手** (実装) | Phase 1A/1B/3 の派生施策へ展開 (例: Decoy を index.html・hub-* にも適用) |
| KO セッション > 50 + KO_CTR / JA_CTR ≤ 50% | **A or B (Phase 4-B Option A)** | Tier 別バッジ全件展開 (wakamiya 含む 8 コース・6-8h) |
| KO セッション < 20 | **B (Phase 4-B Option B)** | wakamiya 単独 LP を実装 (5h) + 韓国語ネイティブ校正発注 |
| EN_CTR / JA_CTR ≤ 50% | **EN 改善** | hisayama / sevenmillion の EN-only セグメント (台湾・在日米軍家族) 向け LP 検討 |
| (hero+sticky+ftv) < 50% | **CTA 配置最適化** | 観測対象復帰前提で CSS 微調整・hero CTA を ATF (above-the-fold) 強化 |
| 全指標 HOLD | **延長 Day 42 (6/17)** | 6/3 では判断せず観測継続 |
| 全指標 NO + LP PV 全滅 | **戦略再検討** | 専門家会議全員招集・別軸 (AdSense / 別 KW セット / 別 ASP) |

---

## 6. 結果記入欄 (Day 7 / 14 / 28 で埋める)

### Day 7 (2026-05-13)

```
記入日:
記入者:

[レポート 1] Decoy
  - N (price_featured + price_default):
  - featured 比率:
  - 判定: 観測継続 (Day 7 では判定しない)

[レポート 2] Phase 1A 逆流ナビ
  - internal_nav_click 件数:
  - target_page 上位 3:
  - 判定: 観測継続

[レポート 3] Phase 1B CTA
  - click_affiliate 全件:
  - cta_position 上位 3:
  - 判定: 観測継続

異常値の有無:
  - ゼロ件継続? (NO/YES):
  - 想定外位置からの集中? (NO/YES):

会議再招集の要否:
コメント:
```

### Day 14 (2026-05-19 → 実施 2026-05-22)

```
記入日: 2026-05-22
記入者: Claude (/observation-checkin 14 skill 自動実行)
観測期間: 2026-05-09 〜 2026-05-22 (14日間)
raw データ: page_view=103 / click_affiliate=16 / internal_nav_click=2 / users=35

[レポート 1] Decoy
  - N (price_featured + price_default): 4 (featured=1 / default=3)
  - featured 比率: 25% (1/4)
  - 判定: ⏳ 延長 (N=4 < 30・Day 42 まで継続)

[レポート 2] Phase 1A 逆流ナビ
  - internal_nav_click: 2 件 (1ユーザー / course-keya.html から hub-beginner + hub-traveler)
  - 全 course-* PV: 28 (moonlake=7, central=3, hisayama=2, keya=2, koga=2, 他×1×12)
  - internal_nav_click / course-* PV: 2/28 = 7.1% / 判定: ✅ GO (≥5%)
  - ⚠️ 注意: N=2 の 1 ユーザー由来・統計的信頼性低い
  - KO/JA 比: 0/2 = 0% / 判定: ⚠️ KO 改善優先 (< 30%)

[レポート 3] Phase 1B CTA
  - hero=2 / sticky=3 / ftv=2 → (hero+sticky+ftv) = 7
  - (hero+sticky+ftv) 比率: 7/16 = 43.75% / 判定: ❌ 要見直し (< 50%)
  - other 比率: 3/16 = 18.75% ⚠️ (> 15%・golf-wear Amazon + 未分類リンクが混入)
  - booking_grid: 2/16 = 12.5% / price_default: 3 / price_featured: 1
  - jalan / rakuten_gora 比: 12:3 = 80%:20% (jalan 優勢 ✓)

[レポート 4] 言語別ファネル
  - click_affiliate 言語内訳: ja=16 (100%) / en=0 / ko=0
  - JA_CTR: 16/103 ≈ 15.5% (全 PV 分母・参考値)
  - EN_CTR: 0% / KO_CTR: 0%
  - KO_CTR / JA_CTR: 0% → ⚠️ インバウンド改善優先
  - EN_CTR / JA_CTR: 0% → ⚠️ EN 改善要
  - KO セッション数 (月換算): <5 (click_affiliate KO=0 より推定)
  - 判定: ⚠️ インバウンド改善優先 → Phase 4-B Option B (wakamiya 単独 LP) 優先

[レポート 5] LP 効果
  - book-fukuoka-cheap PV (14日実績→月換算): 2 → 約 4/月 / 判定: ❌ NO (< 100/月)
  - book-fukuoka-tomorrow PV: 0 / 判定: ❌ NO (リスト未掲載=ゼロ)
  - book-fukuoka-solo PV: 0 / 判定: ❌ NO (リスト未掲載=ゼロ)
  - 各 LP CTR: 0% (LP からのクリック実績なし) / 判定: ❌ 改善余地
  - → SEO カニバリ or 未インデックス疑い (田中タスク C 前倒し強く推奨)

[異常値・要注意]
  - LP 3本全滅: book-cheap 4/月・tomorrow 0・solo 0 → GSC で順位・インデックス確認必須
  - KO/EN ゼロ変換: 全 16 click_affiliates が ja のみ (インバウンドほぼ機能せず)
  - CTA other 超過: 18.75% > 15% → golf-wear.html (Amazon・cta_position=other) が混入
  - report-kurume URL 二重: /report-kurume (2PV) と /report-kurume.html (1PV) が別記録
    → canonical タグ確認 or リダイレクト設定を観測終了後に対処

[GSC エクスポート]
  - 完了日: (要ユーザー実行・GSC ログイン必要)
  - 田中タスク C へ連携済: NO (要実施・LP 3本全滅のため前倒し推奨)

会議再招集の要否: YES (LP 全滅 + KO/EN ゼロ = 複数指標で NO → 戦略再確認推奨)
コメント: N が小さく統計的確度は低いが、LP 3本(Phase 2)の流入ゼロは SEO 問題の強いシグナル。
  GSC でのカニバリ・インデックス確認を Day 28 前に実施すべき。
  観測終了後の Phase 4 候補は現時点の傾向として C (GSC カニバリ修正) が最有力。
```

### Day 28 (2026-06-03)

```
記入日:
記入者:

[レポート 1-5 全項目]
  - (Day 14 と同じテンプレで記入)

[Day 28 判定マトリクス §5]
  - Decoy: GO / HOLD / NO
  - LP: cheap __, tomorrow __, solo __
  - KO: __ / EN: __
  - CTA 配置: __

[Phase 4 着手決定]
  - 着手項目: A / B (Option A or B) / C / EN 改善 / 延長 / 戦略再検討
  - 6/3 中の実装内容:
  - 6/3 commit hash:

NEXT_SESSION.md 更新済 (YES/NO):
コメント:
```

---

## 7. 既知のノイズと除外事項

- **5/10 のテストクリック 8 件 (1 ユーザー / direct / ja / desktop)**: 計測ノイズとして許容。集計除外不要 (誤差範囲)
- **`service: internal_fees` (内部 fees.html CTA・3 箇所×3 言語)**: 全レポートで `service NOT IN ('internal_fees')` フィルタ
- **GA4 自動 `click` イベント**: 自前 `click_affiliate` (⊂ `click`) のみ参照 (詳細 GA4_DASHBOARD.md §1.4)
- **`(not set)` 値**: 5/9 登録前のレガシーイベント。期間フィルタ「5/9 以降」で除外可能

---

## 8. リスクシナリオと対応

| リスク | 兆候 | 対応 |
|---|---|---|
| 全期間 N < 30 | Day 28 時点で click_affiliate 累計 < 30 | Day 42 延長 / 観測 KW SEO 改善併走 (田中タスク C 前倒し) |
| Phase 1A 逆流ナビ 0 件継続 | Day 14 で internal_nav_click ゼロ | コード機能不全の再検証 (5/10 検証済だが念のため再現テスト) |
| 想定外イベント爆発 | `click` が `click_affiliate` の 3 倍超 | 非アフィリ外部離脱の link_url 集計 → 公式サイト誘導の漏れバケツ修正検討 (但し観測終了後) |
| GA4 ID 変更 | データ流入断絶 | NEXT_SESSION.md 禁止事項 #1 違反 / 即原状復帰 |
| Day 28 判断ミス | 判定マトリクス不一致 | 本プレイブック §5 マトリクスに従う・恣意的解釈禁止 (確証バイアス排除の主旨) |

---

## 9. プレイブック使用後の更新

- Day 7/14/28 各日の記入完了後、本ファイル §6 を保存 (両ディレクトリ同期)
- Day 28 判定が確定したら NEXT_SESSION.md にも転記
- 次回観測サイクル (Phase 4 実装後の効果測定) では本ファイルをテンプレ化して新規作成 (PHASE5_OBSERVATION_PLAYBOOK.md 等)

---

**🎯 設計思想**: Day 28 当日に「数値を見ながら結論を動かす」ことを禁止する。スレッショルドは事前確定 (本ファイル) + 結果記入のみ (§6) → マトリクス参照で機械判定 (§5)。これにより 30 分判定 + 確証バイアスゼロを両立する。
