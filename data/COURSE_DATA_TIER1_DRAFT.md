# Tier 1 新規追加 15 件 course_data.json 雛形 (Phase B 着手準備)

**作成日**: 2026-05-12
**ファイル**: `data/COURSE_DATA_TIER1_DRAFT.json` (JSON 配列 15 件)
**観測抵触チェック**: ○ (data/ 配下のドラフト・実反映なし)

---

## §1 ファイル説明

### COURSE_DATA_TIER1_DRAFT.json
- 既存 `course_data.json` のスキーマに完全準拠した 15 件分の JSON 配列
- Phase B 着手時 (Day 28 GO 後) に `course_data.json` の末尾 (`]` の直前) にマージ追加する
- **絶対に course_data.json を上書きしない** (CLAUDE.md §9 #7・過去事故 2026-05-03)
- マージ方法: 手動 Edit で `course_data.json` の最終 `]` を `,` に変更 → このドラフトの内容を貼付け → 最終 `]` を追加

---

## §2 slug 命名規約

| # | コース | slug | file | 理由 |
|---|---|---|---|---|
| 1 | ザ・クラシック GC | `classic` | course-classic.html | シンプル・既存 35 と命名一貫 |
| 2 | 志摩シーサイド CC | `shimaseaside` | course-shimaseaside.html | 地名 + コースタイプ連結 |
| 3 | 福岡雷山 GC | `raizan` | course-raizan.html | 雷山地名のみ |
| 4 | NEW ユーアイ GC | `newui` | course-newui.html | 公式略称踏襲 |
| 5 | 周防灘 CC | `suonada` | course-suonada.html | 海域名 |
| 6 | 皐月天拝 [PGM] | `satsuki-tenpai` | course-satsuki-tenpai.html | ブランド + コース名 (兄弟識別) |
| 7 | 皐月竜王 [PGM] | `satsuki-ryuoh` | course-satsuki-ryuoh.html | 同上 |
| 8 | かほ GC | `kaho` | course-kaho.html | 公式略称 |
| 9 | チサン遠賀 [PGM] | `chisan-onga` | course-chisan-onga.html | ブランド + 地名 |
| 10 | 瀬板の森 | `seitanomori` | course-seitanomori.html | 地名 |
| 11 | 西日本 CC | `nishinihon` | course-nishinihon.html | コース名ローマ字 |
| 12 | JR 内野 CC | `jruchino` | course-jruchino.html | JR ブランド連結 |
| 13 | 夜須高原 CC | `yasukogen` | course-yasukogen.html | 地名 |
| 14 | 八女上陽 GC | `yamejoyo` | course-yamejoyo.html | 地名連結 |
| 15 | 福岡サンレイク GC | `sunlake` | course-sunlake.html | コース名 |

---

## §3 hero_img 割当

| # | コース | hero_img | 根拠 |
|---|---|---|---|
| 1 | ザ・クラシック | spring-forest.webp | 林間・名門 |
| 2 | 志摩シーサイド | itoshima-sea.webp | 玄界灘・シーサイド |
| 3 | 福岡雷山 | sakura-river.webp | 糸島内陸・自然 |
| 4 | NEW ユーアイ | fukuoka-bay.webp | 玄界灘オーシャンビュー |
| 5 | 周防灘 | fukuoka-overview.webp | ヒルトップビュー |
| 6 | 皐月天拝 | spring-forest.webp | 丘陵 |
| 7 | 皐月竜王 | golf-mountain.webp | 山岳・標高 |
| 8 | かほ | sakura-river.webp | 丘陵 |
| 9 | チサン遠賀 | sakura-road.webp | 丘陵 |
| 10 | 瀬板の森 | island-view.webp | 林間湖畔 |
| 11 | 西日本 | golf-mountain.webp | 丘陵チャンピオン |
| 12 | JR 内野 | spring-forest.webp | 丘陵フラット |
| 13 | 夜須高原 | **aso-grassland.webp** | 標高 300m 高原 (既存未使用画像・最適) |
| 14 | 八女上陽 | fukuoka-overview.webp | 耳納連山ビュー |
| 15 | 福岡サンレイク | itoshima-bay.webp | 池戦略・水景 |

---

## §4 エリア分類 (IA 鈴木玲奈確定)

| # | コース | area_primary | area_secondary |
|---|---|---|---|
| 1 | ザ・クラシック | kitakyushu | chikuho |
| 2 | 志摩シーサイド | itoshima | — |
| 3 | 福岡雷山 | itoshima | — |
| 4 | NEW ユーアイ | kitakyushu | — |
| 5 | 周防灘 | kitakyushu | — |
| 6 | 皐月天拝 | chikugo | — |
| 7 | 皐月竜王 | chikuho | — |
| 8 | かほ | chikuho | — |
| 9 | チサン遠賀 | kitakyushu | — |
| 10 | 瀬板の森 | kitakyushu | — |
| 11 | 西日本 | chikuho | kitakyushu |
| 12 | JR 内野 | chikuho | — |
| 13 | 夜須高原 | chikugo | chikuho |
| 14 | 八女上陽 | chikugo | — |
| 15 | 福岡サンレイク | chikugo | — |

---

## §5 アフィリ ASP マッピング (mapping ファイル拡張ドラフト)

### jalan_golf_mapping.json 追記 (15 件)
```json
{"file": "course-classic",        "name": "ザ・クラシックゴルフ倶楽部",                  "jalan_id": "02340", "deeplink": true},
{"file": "course-shimaseaside",   "name": "志摩シーサイドカンツリークラブ",             "jalan_id": "02352", "deeplink": true},
{"file": "course-raizan",         "name": "福岡雷山ゴルフ倶楽部",                       "jalan_id": "02330", "deeplink": true},
{"file": "course-newui",          "name": "NEWユーアイゴルフクラブ",                    "jalan_id": "02336", "deeplink": true},
{"file": "course-suonada",        "name": "周防灘カントリークラブ",                     "jalan_id": "02363", "deeplink": true},
{"file": "course-satsuki-tenpai", "name": "皐月ゴルフ倶楽部 天拝コース【PGM】",        "jalan_id": "02323", "deeplink": true},
{"file": "course-satsuki-ryuoh",  "name": "皐月ゴルフ倶楽部 竜王コース【PGM】",        "jalan_id": "02318", "deeplink": true, "note": "2024/4/1 スループレー・セルフ・レストラン廃止"},
{"file": "course-kaho",           "name": "かほゴルフクラブ【アコーディア】",          "jalan_id": "02347", "deeplink": true, "note": "2025/6/1 FW乗入有料化"},
{"file": "course-chisan-onga",    "name": "チサンカントリークラブ遠賀【PGM】",         "jalan_id": "02337", "deeplink": true},
{"file": "course-seitanomori",    "name": "瀬板の森北九州ゴルフコース",                 "jalan_id": "02311", "deeplink": true, "note": "北九州市営"},
{"file": "course-nishinihon",     "name": "西日本カントリークラブ",                     "jalan_id": "02317", "deeplink": true, "note": "ゲーリー・プレーヤー設計"},
{"file": "course-jruchino",       "name": "JR内野カントリークラブ",                     "jalan_id": "02345", "deeplink": true, "note": "JR九州系・公式KO/EN対応"},
{"file": "course-yasukogen",      "name": "夜須高原カントリークラブ",                   "jalan_id": "02349", "deeplink": true, "note": "楽天評価4.4/2,629件"},
{"file": "course-yamejoyo",       "name": "八女上陽ゴルフ倶楽部",                       "jalan_id": "02355", "deeplink": true, "note": "宿泊併設・ふるさと納税対象"},
{"file": "course-sunlake",        "name": "福岡サンレイクゴルフ倶楽部",                 "jalan_id": "02357", "deeplink": true}
```

### rakuten_gora_mapping.json 追記 (15 件)
```json
{"file": "course-classic",        "name": "ザ・クラシックゴルフ倶楽部",                  "c_id": "400022", "deeplink": true},
{"file": "course-shimaseaside",   "name": "志摩シーサイドカンツリークラブ",             "c_id": "400024", "deeplink": true},
{"file": "course-raizan",         "name": "福岡雷山ゴルフ倶楽部",                       "c_id": "400043", "deeplink": true},
{"file": "course-newui",          "name": "NEWユーアイゴルフクラブ",                    "c_id": "400052", "deeplink": true, "note": "公式KO直対応"},
{"file": "course-suonada",        "name": "周防灘カントリークラブ",                     "c_id": "400025", "deeplink": true},
{"file": "course-satsuki-tenpai", "name": "皐月ゴルフ倶楽部 天拝コース【PGM】",        "c_id": "400004", "deeplink": true},
{"file": "course-satsuki-ryuoh",  "name": "皐月ゴルフ倶楽部 竜王コース【PGM】",        "c_id": "400005", "deeplink": true, "note": "2024/4/1 完全セルフ化"},
{"file": "course-kaho",           "name": "かほゴルフクラブ【アコーディア】",          "c_id": "400017", "deeplink": true},
{"file": "course-chisan-onga",    "name": "チサンカントリークラブ遠賀【PGM】",         "c_id": "400035", "deeplink": true},
{"file": "course-seitanomori",    "name": "瀬板の森北九州ゴルフコース",                 "c_id": "400026", "deeplink": true, "note": "北九州市営"},
{"file": "course-nishinihon",     "name": "西日本カントリークラブ",                     "c_id": "400036", "deeplink": true},
{"file": "course-jruchino",       "name": "JR内野カントリークラブ",                     "c_id": "400023", "deeplink": true, "note": "JR九州系・公式KO/EN対応"},
{"file": "course-yasukogen",      "name": "夜須高原カントリークラブ",                   "c_id": "400048", "deeplink": true, "note": "楽天評価4.4/2,629件"},
{"file": "course-yamejoyo",       "name": "八女上陽ゴルフ倶楽部",                       "c_id": "400049", "deeplink": true, "note": "宿泊併設"},
{"file": "course-sunlake",        "name": "福岡サンレイクゴルフ倶楽部",                 "c_id": "400053", "deeplink": true}
```

---

## §6 既知の未確認項目 (Phase B 着手時に対処要)

### 高優先
- **福岡雷山 GC 料金** (S-4 残課題・公式 SSL 問題) — `fees_ja/en/ko` で「(要追加調査)」と保留中
- **瀬板の森 指定管理者名・市民料金** (公式 403 継続) — 北九州市スポーツ部問合せ要

### 中優先
- 皐月天拝 電話番号: 092-929-3111 (PGM 公式) vs 092-925-0002 (楽天) → 092-929-3111 採用 (要電話確認)
- 皐月天拝 ヤード: 6,624Y 採用 (3 ソース不一致・暫定)
- 八女上陽 ヤード: 6,802Y 採用 (4 ソース不一致・暫定)
- 瀬板の森 ヤード: 6,377Y 採用 (3 ソース不一致・暫定)

### 低優先
- 各コースの福岡空港・博多駅からの正確な所要時間 (推定値で記載・要 Google Maps 検証)
- カートタイプ詳細 (FW 乗入可否等)

---

## §7 Phase B 着手フロー (Day 28 GO 後)

### Step 1: バックアップ
```bash
cp course_data.json course_data.json.backup-pre-tier1-2026-06-XX
```

### Step 2: マージ
1. `course_data.json` を開く
2. 最終 `]` の前の `}` の後ろに `,` を追加
3. `COURSE_DATA_TIER1_DRAFT.json` の中身 (`[` `]` を除く 15 件) を貼付け
4. 最終 `]` を確認

### Step 3: jalan_golf_mapping.json / rakuten_gora_mapping.json 拡張
- §5 の追記コードを `courses` 配列末尾に追加 (同様の手順)

### Step 4: パイロット 1 件選定 + `/create-course-page` 実行
**IA 推奨**: 志摩シーサイド (最シンプル・skill 動作検証)
**secondary 推奨**: ザ・クラシック (data 確実性・テンプレ横展開)

ユーザー判断で 1 件選定 → `/create-course-page <slug>` 実行

### Step 5: パイロット検証成功後、残 14 件を順次追加 (2-3 件/日)

---

## §8 注意事項

- **`course_data.json` 既存 35 件への影響: ゼロ** (マージ追加のみ)
- **Phase B 着手前にユーザーが対処すべき項目**:
  - GA4 観測フェーズの判定 (Day 28 = 2026-06-03 = `/observation-checkin 28`)
  - GO 判定後にこの DRAFT を course_data.json に反映する権限委譲
  - 福岡雷山の料金電話確認 (公式 SSL 問題)
- **既存 35 コースとの slug 衝突: なし** (全 15 slug が新規)

---

## §9 詳細データ参照

- 公式情報: `tier1_batch1_research.md` / `tier1_batch2_research.md` / `tier1_batch3_research.md`
- 反証検証: `tier1_secondary_verification.md`
- エリア分類: `AREA_CLASSIFICATION.md`
- 八女上陽設計者: `yamejoyo_designer_verification.md` (今回は採用しない方針)
- 統合サマリ: `TIER1_SUMMARY.md`
