# 🎯 次セッション 引き継ぎ指示書

**最終更新**: 2026-05-06
**最終 commit**: `5758dbe` (Phase 4 Step 1 - GA4 観測ダッシュボード準備)
**前回 commit**: `289bb21` (Phase 3 - Decoy)、`6a03311` (Phase 2 - 取引KW LP)、`4c40600` (Phase 1 - 逆流ナビ+CVR)

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

1. **🆕 Phase 4 Step 1 — GA4 観測ダッシュボード準備** (未コミット / 2026-05-06)
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
