# Tier 1 新規追加 15 候補 統合サマリ (Phase A データ収集)

**作成日**: 2026-05-12
**フェーズ**: Phase A データ収集 (HTML 改修ゼロ・観測抵触なし)
**Status**: Batch 1/2/3 公式情報収集完了 → secondary 独立検証待ち

---

## 1. Tier 1 全 15 件 一覧 (基本情報)

| # | コース名 | エリア | H/Par | 開場 | 設計者 | 運営 | 平日 セルフ | jalan_id | rakuten c_id |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ザ・クラシック GC | 宮若 | 27H Par108 | 1990 | 鈴木正一 | CMG | ¥17,070 | 02340 | 400022 |
| 2 | 志摩シーサイド CC | 糸島 | 18H Par72 6,660Y | 1977 | 阿部恒雄 | 小郡 CC ? | ¥19,000 | 02352 | 400024 |
| 3 | 福岡雷山 GC ⚠ | 糸島 | 18H Par72 6,956Y | 1996 | ポリテクニックC・谷平考 | (独立) | 要調査 | 02330 | 400043 |
| 4 | NEW ユーアイ GC ★ | 宗像 | 18H Par72 6,906Y | 2000 | 陳清波 | 未記載 | ¥6,910〜 | 02336 | 400052 |
| 5 | 周防灘 CC | 築上 | 18H Par72 7,069Y | 1974 | 大成建設 | 周防灘 CC 株 | ¥9,200 | 02363 | 400025 |
| 6 | 皐月天拝 [PGM] | 筑紫野 | 18H Par72 6,624Y | 1982 | 大洋緑化 | PGM | ¥7,241〜 | 02323 | 400004 |
| 7 | 皐月竜王 [PGM] ★2024改装 | 飯塚 | 18H Par71 5,827Y | 1978 | 要調査 | PGM | ¥3,332〜 | 02318 | 400005 |
| 8 | かほ GC [アコーディア] | 飯塚 | 18H Par72 6,556Y | 1975 | 島村祐正 | アコーディア | ¥5,869〜 | 02347 | 400017 |
| 9 | チサン遠賀 [PGM] | 遠賀 | 27H Par108 9,257Y | 1973 | 地産緑化 | PGM | ¥5,878〜 | 02337 | 400035 |
| 10 | 瀬板の森 [市営] ⚠ | 北九州八幡西 | 18H Par72 6,377Y | 1997 | 西武建設 | 北九州市 + 指定管理 | ¥7,728〜 | 02311 | 400026 |
| 11 | 西日本 CC ★ | 直方 | 18H Par72 6,842Y | 1975 | **ゲーリー・プレーヤー** | CMG | ¥7,810〜 | 02317 | 400036 |
| 12 | JR 内野 CC ★ | 飯塚 | 18H Par72 6,587Y | 1992 | 小笹昭三 | **JR 九州リゾート開発** | ¥9,500〜 | 02345 | 400023 |
| 13 | 夜須高原 CC ★楽天4.4 | 朝倉郡筑前町 | 27H Par108 10,280Y | 1974 | 安田幸吉・川村四郎 | 三和スポーツ | ¥10,510〜 (要確認) | 02349 | 400048 |
| 14 | 八女上陽 GC ★宿泊併設 | 八女 | 18H Par72 6,802Y | 1992 | **イアン・ベーカー・フィンチ** | 上陽観光開発 | ¥7,146〜 | 02355 | 400049 |
| 15 | 福岡サンレイク GC | みやま | 18H Par72 6,723Y | 2003 | (株)ガイア | サンレイク GC 株 | ¥10,000 | 02357 | 400053 |

**凡例**:
- ★ = 特別な強み (KO/EN 公式対応 / 名設計家 / 高評価 / 宿泊併設 等)
- ⚠ = 公式サイトアクセス問題あり (要追加調査)

---

## 2. 重要発見 (戦略インパクトの大きい順)

### 2.1 公式 KO ページ保有 2 件 (既存 wakamiya 1 件のみだった Tier 1 KO 戦略を更新)

| コース | KO URL | EN URL | 翻訳品質 | 想定 Tier |
|---|---|---|---|---|
| **NEW ユーアイ GC** | https://m-uigc.com/kr/index.html | なし | 機械か独自か評価が割れた・要検証 | **1.5** (公式 KO 直対応・品質要確認) |
| **JR 内野 CC** | https://www.jruchino.cc/apps/kr | https://www.jruchino.cc/apps/en | **機械翻訳** (「컴룸」等不自然) | **3** (機械翻訳・「자동번역」明示要) |

→ **i18n_course_compatibility.json 更新候補** (Phase B 着手時に Tier 1-5 再分類)
→ **Day 28 GO 後の Phase 4-B (wakamiya 単独 LP) 戦略を「Tier 1 公式 KO 対応 2-3 コースクラスタ」に拡張可能**

### 2.2 コンテンツフック (取材・SEO 強化材)

| コース | フック | 活用先 |
|---|---|---|
| **ザ・クラシック GC** | 2028 日本女子オープン開催・名門 | 取材候補 (INTERVIEW_CANDIDATES.md 拡張) / hub-business |
| **西日本 CC** | **ゲーリー・プレーヤー設計** | SEO「ゲーリー・プレーヤー 福岡」/ コンテンツ強 |
| **八女上陽 GC** | **イアン・ベーカー・フィンチ設計** (全英オープン優勝者) + 宿泊併設 | hub-traveler / ゴルフ旅行記事 |
| **NEW ユーアイ GC** | オーシャンビュー + 公式 KO ページ | インバウンド KO 記事 |
| **志摩シーサイド CC** | 「日本のペブルビーチ」(玄界灘ビュー) | hub-traveler / インバウンド |
| **夜須高原 CC** | 標高 300m 高原 + 楽天 4.4/2,629 件 | hub-business / 夏のゴルフ訴求 |
| **皐月竜王 [PGM]** | 平日 ¥3,332〜 + 2024 完全セルフ・スループレー化 | hub-budget 強化 |

### 2.3 観測抵触最小化のためのページ設計上の注意

- ★ **ザ・クラシック**: 「日曜プレー = メンバー同伴必須」を CTA 文面に注意書き必須
- ★ **皐月竜王**: 「2024/4/1 完全セルフ・スループレー専用・レストラン廃止 (キッチンカー)・浴槽廃止 (シャワーのみ)」を必ず明記
- ★ **かほ GC**: 「2025/6/1 から FW 乗入有料化 (平日 ¥500・土日祝 ¥1,000)」を明記
- ★ **瀬板の森**: 公式 403 のため一部情報 (指定管理者名・市民料金) が未確認 → 掲載文面は楽天 GORA / じゃらん情報のみで簡素に

---

## 3. 公式アクセス問題 (2 件・要対処)

| コース | 問題 | 対処 |
|---|---|---|
| **福岡雷山 GC** | http://raizan-gc.co.jp/ SSL 自己署名証明書エラー | ブラウザ直接アクセス or TEL: 092-323-8181 で料金確認 / 公式 SSL 修正待ち |
| **瀬板の森** | https://www.seitanomorigc.com/ HTTP 403 全ページ | 北九州市スポーツ部に指定管理者名 + 市民料金問い合わせ |

---

## 4. 数値不一致 (公式 vs 二次情報・8 件)

| コース | 項目 | 公式/A | 二次/B | 採用判定 |
|---|---|---|---|---|
| 皐月天拝 | 電話番号 | 092-929-3111 (公式 + じゃらん) | 092-925-0002 (楽天) | 092-929-3111 (2 vs 1) |
| 皐月天拝 | ヤード | 楽天 guide 6,629Y | 各ホール積算 6,624Y | 6,624Y |
| 皐月竜王 | ヤード | 楽天 guide 5,847Y / じゃらん 5,555Y | 各ホール積算 5,827Y | 5,827Y |
| かほ | ヤード | アコーディア detail 6,610Y | レイアウト積算 + 楽天 6,556Y | 6,556Y |
| 瀬板 | ヤード | kitakyu-net 6,426Y | 楽天 GORA 6,377Y | 6,377Y |
| 福岡サンレイク | ヤード | 公式 6,723Y | じゃらん / ホームメイト 6,880Y | **secondary 検証推奨** |
| 八女上陽 | ヤード | 楽天 GORA 6,802Y | ゴルフホットライン 6,776Y | 6,802Y |
| ザ・クラシック | 開場日 | 公式「1990 年」のみ | Wikipedia 9/22 | 「1990 年」採用 |

---

## 5. 未確認項目総まとめ (全 15 件横断)

### 5.1 全件横断未確認
- **福岡空港・博多駅からの所要時間** (15 件中 12 件公式未記載)
- **両替・クレジットカード対応** (15 件中 14 件未確認・NEW ユーアイのみ「カード可」)
- **カートタイプ詳細** (FW 乗入可否・GPS 仕様等)

### 5.2 個別重要未確認
- 福岡雷山: 料金全般 (公式アクセス不能)
- 瀬板の森: 指定管理者名 / 市民料金 (公式 403)
- 皐月竜王: 設計者 (天拝同じ大洋緑化の可能性)
- 夜須高原: ビジター平日標準料金 (公式はメンバー中心)
- 八女上陽: ふるさと納税返礼品有無
- ザ・クラシック: 開場正確日付 / カートタイプ詳細
- 志摩シーサイド: 運営会社の法人登記照合

---

## 6. アフィリ ASP マッピング (一括追記用)

### 6.1 jalan_golf_mapping.json 追記候補 (15 件全件追加)

```json
{"file": "course-classic",       "name": "ザ・クラシックゴルフ倶楽部",                  "jalan_id": "02340", "deeplink": true},
{"file": "course-shimaseaside",  "name": "志摩シーサイドカンツリークラブ",             "jalan_id": "02352", "deeplink": true},
{"file": "course-raizan",        "name": "福岡雷山ゴルフ倶楽部",                       "jalan_id": "02330", "deeplink": true},
{"file": "course-newui",         "name": "NEWユーアイゴルフクラブ",                    "jalan_id": "02336", "deeplink": true},
{"file": "course-suonada",       "name": "周防灘カントリークラブ",                     "jalan_id": "02363", "deeplink": true},
{"file": "course-satsuki-tenpai","name": "皐月ゴルフ倶楽部 天拝コース【PGM】",        "jalan_id": "02323", "deeplink": true},
{"file": "course-satsuki-ryuoh", "name": "皐月ゴルフ倶楽部 竜王コース【PGM】",        "jalan_id": "02318", "deeplink": true, "note": "2024/4/1 スループレー・セルフ・レストラン廃止"},
{"file": "course-kaho",          "name": "かほゴルフクラブ【アコーディア】",          "jalan_id": "02347", "deeplink": true, "note": "2025/6/1 FW乗入有料化"},
{"file": "course-chisan-onga",   "name": "チサンカントリークラブ遠賀【PGM】",         "jalan_id": "02337", "deeplink": true},
{"file": "course-seitanomori",   "name": "瀬板の森北九州ゴルフコース",                 "jalan_id": "02311", "deeplink": true, "note": "北九州市営"},
{"file": "course-nishinihon",    "name": "西日本カントリークラブ",                     "jalan_id": "02317", "deeplink": true, "note": "ゲーリー・プレーヤー設計"},
{"file": "course-jruchino",      "name": "JR内野カントリークラブ",                     "jalan_id": "02345", "deeplink": true, "note": "JR九州系・公式KO/EN対応"},
{"file": "course-yasukogen",     "name": "夜須高原カントリークラブ",                   "jalan_id": "02349", "deeplink": true},
{"file": "course-yamejoyo",      "name": "八女上陽ゴルフ倶楽部",                       "jalan_id": "02355", "deeplink": true, "note": "宿泊併設"},
{"file": "course-sunlake",       "name": "福岡サンレイクゴルフ倶楽部",                 "jalan_id": "02357", "deeplink": true}
```

### 6.2 rakuten_gora_mapping.json 追記候補 (15 件全件追加)

```json
{"file": "course-classic",       "name": "ザ・クラシックゴルフ倶楽部",                  "c_id": "400022", "deeplink": true},
{"file": "course-shimaseaside",  "name": "志摩シーサイドカンツリークラブ",             "c_id": "400024", "deeplink": true},
{"file": "course-raizan",        "name": "福岡雷山ゴルフ倶楽部",                       "c_id": "400043", "deeplink": true},
{"file": "course-newui",         "name": "NEWユーアイゴルフクラブ",                    "c_id": "400052", "deeplink": true, "note": "公式KO直対応"},
{"file": "course-suonada",       "name": "周防灘カントリークラブ",                     "c_id": "400025", "deeplink": true},
{"file": "course-satsuki-tenpai","name": "皐月ゴルフ倶楽部 天拝コース【PGM】",        "c_id": "400004", "deeplink": true},
{"file": "course-satsuki-ryuoh", "name": "皐月ゴルフ倶楽部 竜王コース【PGM】",        "c_id": "400005", "deeplink": true, "note": "2024/4/1 完全セルフ化"},
{"file": "course-kaho",          "name": "かほゴルフクラブ【アコーディア】",          "c_id": "400017", "deeplink": true},
{"file": "course-chisan-onga",   "name": "チサンカントリークラブ遠賀【PGM】",         "c_id": "400035", "deeplink": true},
{"file": "course-seitanomori",   "name": "瀬板の森北九州ゴルフコース",                 "c_id": "400026", "deeplink": true, "note": "北九州市営"},
{"file": "course-nishinihon",    "name": "西日本カントリークラブ",                     "c_id": "400036", "deeplink": true},
{"file": "course-jruchino",      "name": "JR内野カントリークラブ",                     "c_id": "400023", "deeplink": true, "note": "JR九州系・公式KO/EN対応"},
{"file": "course-yasukogen",     "name": "夜須高原カントリークラブ",                   "c_id": "400048", "deeplink": true, "note": "楽天評価4.4/2,629件"},
{"file": "course-yamejoyo",      "name": "八女上陽ゴルフ倶楽部",                       "c_id": "400049", "deeplink": true, "note": "宿泊併設"},
{"file": "course-sunlake",       "name": "福岡サンレイクゴルフ倶楽部",                 "c_id": "400053", "deeplink": true}
```

**注**: slug 命名規約 (推奨)
- 既存 35 コースは単一トークン (course-keya / course-wakamiya) が主流
- 複合系 (皐月天拝・皐月竜王) は ハイフン連結 (course-satsuki-tenpai / course-satsuki-ryuoh)
- 個別判断要: course-classic (一般名詞すぎる・course-the-classic 案あり)・course-newui (course-new-ui 案あり)

→ **slug 命名は course_data.json 追加時にユーザー承認必要**

---

## 7. エリア分布 (既存 5 エリア体系での割当)

| エリア | 既存数 | 追加候補 | 追加コース |
|---|---|---|---|
| **fukuokacity** (福岡市) | 7+ | 0 | — (15 件中、福岡市内コースなし) |
| **itoshima** (糸島) | 4 | **+3** | 志摩シーサイド・福岡雷山・(NEW ユーアイは宗像市・別エリア検討要) |
| **kitakyushu** (北九州) | 9 | **+3** | チサン遠賀・瀬板の森・周防灘 |
| **chikugo** (筑後) | 6 | **+5** | 皐月天拝・夜須高原・八女上陽・福岡サンレイク・(JR 内野は飯塚で chikuho か?) |
| **chikuho** (筑豊) | 6 | **+4** | 皐月竜王・かほ・西日本・JR 内野・(夜須高原は朝倉郡で chikugo か?) |
| **新エリア候補?** | — | +1 | NEW ユーアイ (宗像市) / ザ・クラシック (宮若市) — 既存「kitakyushu」or「fukuokacity 拡張」?

→ **エリア再分類が必要** (鈴木玲奈/IA に専門家会議で判断要請推奨)

---

## 8. 次のステップ

### 8.1 直近 (Phase A 完了に必要)
- [ ] **secondary (中村麻衣) による独立検証** (15 件・特に: 数値不一致 8 件 / 公式 KO 翻訳品質 2 件 / 公式アクセス問題 2 件)
- [ ] **エリア分類の確定** (鈴木玲奈/IA 判定: 既存 5 エリアに収まるか / 新エリア必要か / 宮若・宗像の分類)
- [ ] **slug 命名規約の確定** (15 件・特に複合系)
- [ ] **course_data.json 追加用 JSON 雛形 15 件生成** (実適用は Phase B)

### 8.2 中期 (Day 28 GO 後 = Phase B)
- [ ] **試行追加 1 件** (推奨: ザ・クラシック GC or 志摩シーサイド CC or NEW ユーアイ GC)
- [ ] **/create-course-page skill 検証** (Pre-flight 4 チェック・post-processing 7 スクリプト動作)
- [ ] **preview 検証** (3 言語・dataLayer・JSON-LD)

### 8.3 長期 (試行成功後 = Phase C)
- [ ] **残 14 件順次追加** (2-3 件/日ペース)
- [ ] **取材候補拡張** (ザ・クラシック・西日本・八女上陽を INTERVIEW_CANDIDATES.md に追加)
- [ ] **i18n_course_compatibility.json 更新** (NEW ユーアイ Tier 1.5 / JR 内野 Tier 3)
- [ ] **wakamiya 単独 KO LP 戦略を「Tier 1 KO 公式対応クラスタ (wakamiya + NEW ユーアイ)」に拡張検討**

---

## 9. 観測抵触チェック (現時点)

✓ **Phase A 作業 (data/ 配下 .md ファイル作成のみ)**
- HTML 改修ゼロ
- course_data.json 等の JSON 改変なし
- sitemap.xml / robots.txt 変更なし
- 観測サンプル (click_affiliate / internal_nav_click) への影響ゼロ
- **CLAUDE.md §6 観測期間規約に完全準拠**

---

## 10. 詳細レポート

- [Batch 1 詳細 (糸島・インバウンド系)](tier1_batch1_research.md)
- [Batch 2 詳細 (PGM/アコーディア系)](tier1_batch2_research.md)
- [Batch 3 詳細 (独立・地域分散)](tier1_batch3_research.md)

---

**最終確認**: Phase A は **secondary 独立検証 + エリア分類・slug 命名の確定** で完了。Phase B 着手は **Day 28 (2026-06-03) 観測 GO 判断後** を推奨。
