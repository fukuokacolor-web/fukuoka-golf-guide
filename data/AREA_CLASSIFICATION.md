# Tier 1 新規追加 15 件 エリア分類・IA 設計 (鈴木玲奈)

**作成日**: 2026-05-12
**担当**: 鈴木玲奈 (ia-architect)
**観測抵触チェック**: ○ (本ドキュメントは data/ 配下 Markdown のみ・HTML/JSON 改修ゼロ・観測フェーズに完全準拠)

---

## §1 既存 5 エリアの境界線定義 (今回明文化)

既存 area-*.html 5 件の headings・meta description・ItemList を読解し、実際にどの市町村がどのエリアに収まっているかを逆算した。

### 1.1 現行エリア境界 (実データ逆算)

| area slug | 現行タイトル表記 | 実収録コースの所在市町村 | 暗黙の境界 |
|---|---|---|---|
| fukuokacity | 「福岡市エリア 8 コース」 | 福岡市東区 (福岡CC) / 早良区 (アブラヤマ) / 東区 (西戸崎) / 新宮町 (セブンミリオン) / 宇美町 (筑紫ヶ丘) / 糟屋郡粕屋町 (大博多) / 糟屋郡久山町 (久山) / 古賀市 (古賀GC) | 福岡市 + **糟屋郡全域** + 古賀市 + 新宮町まで拡張済 |
| itoshima | 「糸島エリア 4 コース」 | 糸島市 (芥屋/伊都/二丈/クイーンズヒル) | 糸島市のみ (西区は含まず) |
| kitakyushu | **「北九州・宗像エリア 10 コース」** | 北九州市 (小倉/九州GC/北九州CC/門司) / 宮若市 (若宮) / **宗像市 (若松・玄海)** / 鞍手郡鞍手町 (ムーンレイク) / 遠賀郡芦屋町 (ミッション) / 宮若市 (wakamiya) | **宗像市は既に kitakyushu エリアに取り込み済** / 遠賀郡・鞍手郡含む |
| chikugo | 「筑後・久留米エリア 7 コース」 | 久留米市 (久留米CC) / 筑紫野市 (筑紫野CC) / 小郡市 (小郡CC) / **朝倉郡筑前町 (セントラル福岡)** / 大川市 (有明CC) / 太宰府市 (太宰府GC) / うきは市 (浮羽CC) | 太宰府市・筑紫野市・**朝倉郡筑前町まで北上して含む** |
| chikuho | **「筑豊・田川・朝倉 6 コース」** | 飯塚市 (麻生飯塚/レイクサイド/茜) / 田川郡 (鷹羽ロイヤル) / 糟屋郡篠栗町 (アコーディア フェザント) | 飯塚市中心・鞍手郡含む。**「朝倉」がタイトルに入るがセントラル福岡は chikugo 側** |

### 1.2 重要発見: エリア境界の既存「拡張」実績

**area-kitakyushu は既に「北九州・宗像エリア」と明名されている。**
現行 ItemList には若松 GC (北九州市若松区) と玄海 GC (宗像市) が収録済。
つまり「宗像市 → kitakyushu に含める」はすでに実施済の設計判断であり、今回の NEW ユーアイ GC (宗像市) も同じロジックで自然に収まる。

**area-chikuho はタイトルに「朝倉」を含むが、セントラル福岡 (朝倉郡筑前町) は area-chikugo 側に収録されている。**
この分割は「朝倉郡筑前町だが久留米商圏向けルートで来場するため chikugo にした」という観光動線優先の設計と読める。今回の夜須高原 CC (朝倉郡筑前町) は同じ条件のため chikugo に収録するか否かが論点になる (§2 で詳述)。

### 1.3 境界線を確定する 2 つの基準 (今後の運用基準として明文化)

1. **行政区分 (1 次)**: 市町村の実際の行政区域を基準にする
2. **来場動線 (2 次・タイブレーカー)**: 福岡市からと北九州からのどちらを主な来場者と想定するか。どちらとも判断できない場合は「より距離が近いエリアハブ」に割り当て、area_secondary で補足する。

---

## §2 推奨エリア分類 (15 件)

### 2.1 判定マトリクス

| # | コース | 市町村 | 行政区分 | 来場動線主体 | 推奨 area_primary | area_secondary | 判定根拠 |
|---|---|---|---|---|---|---|---|
| 1 | ザ・クラシック GC | 宮若市 | 宮若市 (筑豊系) | 福岡市 / 北九州市 両方 | **kitakyushu** | chikuho | 若宮 IC (九州道) 10 分・area-kitakyushu に若宮コース (宮若市) が既収録 |
| 2 | 志摩シーサイド CC | 糸島市志摩野北 | 糸島市 | 福岡市 | **itoshima** | なし | 同市・異論なし |
| 3 | 福岡雷山 GC | 糸島市川原 | 糸島市 | 福岡市 | **itoshima** | なし | 同市・異論なし |
| 4 | NEW ユーアイ GC | 宗像市牟田尻 | 宗像市 | 福岡市 / 北九州市 両方 | **kitakyushu** | なし | 既存 area-kitakyushu が「北九州・宗像エリア」を明示・玄海 GC (宗像市) も同エリア収録済 |
| 5 | 周防灘 CC | 築上郡築上町 | 旧豊前国・東端 | 北九州市 / 大分方面 | **kitakyushu** | なし | 東九州道 椎田南 IC 2km・北九州方面からの来場が主体 |
| 6 | 皐月天拝 [PGM] | 筑紫野市大字山口 | 筑紫野市 | 福岡市 | **chikugo** | なし | 筑紫野 IC から 7 分・太宰府天満宮圏・既存 area-chikugo に筑紫野 CC (筑紫野市) 収録済 |
| 7 | 皐月竜王 [PGM] | 飯塚市八木山 | 飯塚市 | 福岡市 / 飯塚 | **chikuho** | なし | 飯塚市内・異論なし |
| 8 | かほ GC [アコーディア] | 飯塚市筒野 | 飯塚市 | 飯塚 | **chikuho** | なし | 飯塚市内・異論なし |
| 9 | チサン遠賀 [PGM] | 遠賀郡遠賀町虫生津 | 遠賀郡 | 北九州市 / 福岡市 両方 | **kitakyushu** | なし | 遠賀川駅・鞍手 IC 圏・既存 area-kitakyushu にミッションバレー (遠賀郡芦屋町) 収録済 |
| 10 | 瀬板の森 | 北九州市八幡西区 | 北九州市 | 北九州市 | **kitakyushu** | なし | 市内・異論なし |
| 11 | 西日本 CC | 直方市中泉 | 直方市 (筑豊系) | 北九州市 / 福岡市 両方 | **chikuho** | kitakyushu | 直方市・北九州都市高速 金剛出口利用。直方は旧筑豊炭田圏 (chikuho の語源) に包含 |
| 12 | JR 内野 CC | 飯塚市弥山 | 飯塚市 | 飯塚 / 福岡市 | **chikuho** | なし | 飯塚市内・異論なし |
| 13 | 夜須高原 CC | 朝倉郡筑前町 | 朝倉郡 | 福岡市 / 久留米方面 | **chikugo** | chikuho | セントラル福岡と同じ朝倉郡筑前町。既存の設計判断 (chikugo 収録) と整合。楽天評価 4.4 の来場者の多くは筑紫野 IC 経由の福岡市・久留米方面 |
| 14 | 八女上陽 GC | 八女市上陽町 | 八女市 | 久留米方面 | **chikugo** | なし | 八女市・異論なし |
| 15 | 福岡サンレイク GC | みやま市高田町 | みやま市 | 久留米 / 大牟田 | **chikugo** | なし | みやま市・異論なし |

### 2.2 エリア別追加コース数サマリ

| エリア | 現行数 | 追加数 | 追加後 | 追加コース |
|---|---|---|---|---|
| fukuokacity | 8 | 0 | 8 | なし |
| itoshima | 4 | **+2** | 6 | 志摩シーサイド / 福岡雷山 |
| kitakyushu | 10 | **+4** | 14 | ザ・クラシック / NEW ユーアイ / チサン遠賀 / 瀬板の森 + (周防灘) ※ |
| chikugo | 7 | **+4** | 11 | 皐月天拝 / 夜須高原 / 八女上陽 / 福岡サンレイク |
| chikuho | 6 | **+3** | 9 | 皐月竜王 / かほ / 西日本 CC / JR 内野 |

※ 周防灘 CC を含めると kitakyushu +5 で計 15 件。周防灘を個別に「遠距離サブエリア」扱いにする Option は §3 で述べる。

### 2.3 宮若市の判定補足 (ザ・クラシック GC)

宮若市は行政上「嘉穂郡・鞍手郡の合併自治体」であり、筑豊地域に分類される。しかし若宮 IC (九州自動車道) から 5〜10 分という立地から「北九州側からも福岡市側からもアクセス可能」な中間地点に位置する。既に area-kitakyushu には若宮コース (`course-wakamiya`: 宮若市若宮) が収録されている事実が決定打となる。ザ・クラシックも若宮エリアに立地 (宮若市倉久) するため、kitakyushu へ収録することで既存 area-kitakyushu ページの「若宮 IC 周辺」クラスタが充実する。

---

## §3 新エリア追加の是非 (Option A/B/C 評価)

### 3.1 各 Option の詳細評価

**Option A: 既存 5 エリアに吸収 (推奨)**

| 評価軸 | スコア | 理由 |
|---|---|---|
| 実装コスト | ★★★★★ | area-*.html 追加なし・既存 5 ページに課題追加のみ |
| SEO 影響リスク | ★★★★★ | 既存エリアハブの PageRank が分散しない |
| ユーザー地理感覚 | ★★★☆☆ | 宮若市が kitakyushu は違和感あり (ただし「若宮 IC 10 分」の文脈で納得感を作れる) |
| Hub-and-Spoke 維持 | ★★★★★ | 3 階層構造を壊さない |

実際にこれが機能する根拠: area-kitakyushu.html は既に「北九州・宗像エリア」の複合タイトルを採用しており、ユーザーに「北九州 = この地域全体の呼称」と刷り込む設計になっている。宮若・遠賀も「北九州エリア」と呼ばれることに抵抗が少ない。

**Option B: 新エリア追加 (非推奨)**

| 評価軸 | スコア | 理由 |
|---|---|---|
| 実装コスト | ★☆☆☆☆ | area-munakata.html or area-fukuokakita.html の新規作成・sitemap / hub-* への追加・3 言語対応で推定 15〜20h |
| SEO 影響 | ★★☆☆☆ | area-kitakyushu の内部リンク・PageRank を新エリアに分散させる。特に現在観測中の逆流ナビへの影響が懸念 |
| コース数 | ★★☆☆☆ | 「新宗像エリア」に入れるコースは NEW ユーアイ 1 件のみ。1 コースのためにハブを作るのは SEO 的に薄い |
| 観測抵触 | × | 観測期間中に area-*.html を新規作成すると、index → area の内部リンク変更が発生し Phase 1A 逆流ナビ計測の交絡因子になる可能性 |

**鈴木玲奈の自己却下**: Option B は Day 28 以降に「宗像エリア専用コンテンツが 5 コース以上になった場合」に限り再検討する。現時点では不適。

**Option C: area_primary + area_secondary の二重所属 (部分採用)**

area_secondary は HTML の実装ではなく、**course_data.json の metadata フィールドとしてのみ保持**する。これにより:
- area-*.html の実装は Option A と同じ (simple)
- generate_sitemap.py や将来の area-page スクリプトが area_secondary を参照して「このコースは隣のエリアにも関連します」リンクを挿入できる
- 内部リンク密度向上のメリットを得つつ、HTML 構造はシンプルに保てる

**推奨: Option A + Option C の metadata 部分のみ採用**

---

## §4 各コースの推奨 slug 命名

### 4.1 slug 命名原則 (既存 35 件から抽出した規約)

既存 slug パターンを分析すると以下のルールが見える:

- 単一の固有名詞はそのままローマ字化 (keya / kokura / hisayama)
- 運営会社名 (PGM 等) は slug に含めない
- ブランドプレフィックスが固有名詞の一部の場合は含める (course-kyushugc / course-lakeside)
- 複数単語は小文字 + ハイフン連結 (course-sevenmillion / course-chikushigaoka)

### 4.2 15 件推奨 slug

| # | コース名 | 推奨 slug | 根拠・代替案 |
|---|---|---|---|
| 1 | ザ・クラシック GC | `course-classic` | 現行 TIER1_SUMMARY の提案通り。「ザ・」は慣例通り除去。一般名詞問題は英語 title タグで「The Classic Golf Club」と明示することで解決。`course-the-classic` は冗長 |
| 2 | 志摩シーサイド CC | `course-shimaseaside` | 既存 `course-saitozaki` (西戸崎シーサイド) と混同しないよう地名 (shima) を付与 |
| 3 | 福岡雷山 GC | `course-raizan` | 地名由来・短く明快 |
| 4 | NEW ユーアイ GC | `course-newui` | 既存 TIER1_SUMMARY 通り。`course-new-ui` は UI (ユーザーインターフェース) と誤読リスクあり・`newui` の方が安全 |
| 5 | 周防灘 CC | `course-suonada` | 地名 (周防灘) のローマ字 |
| 6 | 皐月天拝 [PGM] | `course-satsuki-tenpai` | 「皐月」は PGM ブランドの一部・「天拝」が固有識別子。ハイフン連結で既存規約に準拠 |
| 7 | 皐月竜王 [PGM] | `course-satsuki-ryuoh` | 同上。竜王のローマ字 = ryuoh (ryuo も可だが oh 表記が一般的) |
| 8 | かほ GC [アコーディア] | `course-kaho` | 固有地名「嘉穂 (かほ)」由来・短く明快 |
| 9 | チサン遠賀 [PGM] | `course-chisan-onga` | 「チサン」= ブランド (地産)。「遠賀」が固有識別子。既存 `course-moonlake` の命名規約と同水準 |
| 10 | 瀬板の森 | `course-seitanomori` | 正式名称「瀬板の森北九州ゴルフコース」の中核部分。`seitanomori` は公式ドメイン名 (seitanomorigc.com) と一致するため認知度高い |
| 11 | 西日本 CC | `course-nishinihon` | 既存の `course-fukuokakokusai` (福岡国際) と同水準のローマ字化。`course-ncc` は汎用すぎる |
| 12 | JR 内野 CC | `course-jruchino` | 既存 TIER1_SUMMARY 通り。JR ブランドを含めることで公式ドメイン (jruchino.cc) との整合性確保 |
| 13 | 夜須高原 CC | `course-yasukogen` | 「夜須高原 (やすこうげん)」のローマ字短縮形。公式ドメイン (yasukogen.com) と一致 |
| 14 | 八女上陽 GC | `course-yamejoyo` | 「八女上陽」のローマ字連結 |
| 15 | 福岡サンレイク GC | `course-sunlake` | 公式ドメイン (sunlake.jp) と一致・短く明快。「福岡」は除去 (他コースも「福岡レイクサイド → lakeside」等で除去済) |

### 4.3 衝突チェック (既存 35 件との重複確認)

| 推奨 slug | 既存 slug | 衝突 |
|---|---|---|
| course-classic | なし | 問題なし |
| course-shimaseaside | course-saitozaki (シーサイドあり) | 語義違い・問題なし |
| course-raizan | なし | 問題なし |
| course-newui | なし | 問題なし |
| course-suonada | なし | 問題なし |
| course-satsuki-tenpai | なし | 問題なし |
| course-satsuki-ryuoh | なし | 問題なし |
| course-kaho | なし | 問題なし |
| course-chisan-onga | なし | 問題なし |
| course-seitanomori | なし | 問題なし |
| course-nishinihon | なし | 問題なし |
| course-jruchino | なし | 問題なし |
| course-yasukogen | なし | 問題なし |
| course-yamejoyo | なし | 問題なし |
| course-sunlake | なし | 問題なし |

全 15 件、既存 35 件との衝突なし。

---

## §5 hub-* 4 ペルソナへの割当

### 5.1 判定基準

- hub-budget: 平日セルフ料金 ¥10,000 以下 OR 「コスパ」訴求が主訴
- hub-beginner: 高低差が少ない・フラット・コース幅広・初心者歓迎記載
- hub-traveler: 絶景 / 宿泊施設 / 観光地連携 / 世界遺産近接 / シーサイド
- hub-business: 名門 / チャンピオンシップ / 接待向け / キャディ付対応 / 大会開催実績

### 5.2 割当マトリクス (主 / 副)

| # | コース | hub-budget | hub-beginner | hub-traveler | hub-business | 主ハブ | 副ハブ | 根拠 |
|---|---|---|---|---|---|---|---|---|
| 1 | ザ・クラシック GC | - | - | - | ★★★ | **business** | - | ¥17,070・名門・27H・日曜 member 同伴・2028 日本女子オープン |
| 2 | 志摩シーサイド CC | - | - | ★★★ | ★★ | **traveler** | business | 玄界灘一望・「日本のペブルビーチ」・¥19,000 で高単価 |
| 3 | 福岡雷山 GC | - | ★★ | ★★★ | - | **traveler** | beginner | 糸島観光連携・「フラット」記載あり・料金未確認だが糸島周遊客向け |
| 4 | NEW ユーアイ GC | ★★ | - | ★★★ | - | **traveler** | budget | ¥6,910〜・オーシャンビュー・宗像大社 (世界遺産) 10 分・公式 KO ページ |
| 5 | 周防灘 CC | ★ | - | ★★★ | ★★ | **traveler** | business | 全ホール周防灘ビュー・¥9,200・遠距離 = 旅行要素高い・PGA シニアトーナメント開催 |
| 6 | 皐月天拝 [PGM] | ★ | ★★ | ★★ | - | **beginner** | traveler | 太宰府天満宮 10 分の観光連携・¥7,241〜・設計はやや平易 |
| 7 | 皐月竜王 [PGM] | ★★★ | ★★ | - | - | **budget** | beginner | ¥3,332〜・スループレー = 入門者向け体験・hub-budget 最強候補 |
| 8 | かほ GC | ★★★ | ★ | - | - | **budget** | - | ¥5,869〜・既存 hub-budget に収録済コースと同水準 |
| 9 | チサン遠賀 [PGM] | ★★ | ★★ | - | - | **budget** | beginner | ¥5,878〜・27H で選択肢多い・初心者がスコアをまとめやすい遠賀コースあり |
| 10 | 瀬板の森 | ★★★ | ★★ | - | - | **budget** | beginner | ¥7,728〜・市営 = 地元価格感・北九州市内アクセス良 |
| 11 | 西日本 CC | - | - | - | ★★★ | **business** | - | ゲーリー・プレーヤー設計・¥7,810〜でチャンピオンコース・名門感 |
| 12 | JR 内野 CC | - | ★★★ | - | ★ | **beginner** | business | 「フラットにデザイン」公式明記・JR ブランドで接待利用可・¥9,500〜 |
| 13 | 夜須高原 CC | - | - | ★★★ | ★★ | **traveler** | business | 標高 300m・夏涼しい・楽天 4.4/2,629 件・27H で長期滞在向け |
| 14 | 八女上陽 GC | - | - | ★★★ | ★★ | **traveler** | business | 宿泊施設 15 室+5 棟・イアン・ベーカー・フィンチ設計・絶景 3 方向 |
| 15 | 福岡サンレイク GC | ★ | ★ | ★★ | - | **traveler** | budget | 柳川掘割川 15 分・楽天 4.3/1,515 件・¥10,000 |

### 5.3 ハブ別 集計

| ハブ | 新規追加コース | 追加後総数 (推定) |
|---|---|---|
| hub-budget | 皐月竜王 / かほ / チサン遠賀 / 瀬板の森 (主) + NEW ユーアイ (副) | 既存 + 4〜5 件 |
| hub-beginner | JR 内野 (主) + 皐月天拝 / 皐月竜王 / チサン遠賀 / 瀬板の森 (副) | 既存 + 1〜5 件 |
| hub-traveler | NEW ユーアイ / 志摩シーサイド / 福岡雷山 / 周防灘 / 夜須高原 / 八女上陽 / 福岡サンレイク (主) | 既存 + 7 件 |
| hub-business | ザ・クラシック / 西日本 CC (主) + 志摩シーサイド / 周防灘 / 夜須高原 / 八女上陽 (副) | 既存 + 2〜6 件 |

hub-traveler への集中 (7 件) は「絶景・観光連携コースが多い」という新規 15 件の特性を反映している。これは hub-traveler ページの充実 (コンテンツボリューム・内部リンク密度) に直結するため、SEO 上プラスに働く。

---

## §6 sitemap.xml priority 割当

### 6.1 既存 priority 体系

| tier | priority | 対象 |
|---|---|---|
| TOP | 1.0 | index.html のみ |
| HIGH | 0.9 | area-*.html / hub-*.html / LP 3 件 / airport-access-top5 等 |
| MEDIUM | 0.8 | 主要 course-*.html (上位陣) |
| DEFAULT | 0.7 | access-*.html / 標準 course-*.html |
| LOW | 0.6 | 薄いコンテンツ / クローズ中コース等 |

### 6.2 新規 15 件の推奨 priority

priority 判定基準:
- 0.8 (MEDIUM) 付与条件: 以下のうち 2 つ以上該当
  - 大会開催実績 (過去 or 予定)
  - 著名設計者 (国際名)
  - インバウンド公式 KO/EN 対応
  - 楽天評価 4.3 以上 + レビュー 1,000 件超
  - ユニークな施設 (宿泊・シーサイド等)
  - エリア内トップ集客 KW 候補

| # | コース | 推奨 priority | 0.8 判定理由 |
|---|---|---|---|
| 1 | ザ・クラシック GC | **0.8** | 2028 日本女子オープン予定・27H 名門・CMG 直 |
| 2 | 志摩シーサイド CC | **0.8** | シーサイドリゾート・「日本のペブルビーチ」・itoshima エリア追加後の主力 |
| 3 | 福岡雷山 GC | **0.7** | 料金未確認・公式 SSL 問題あり → 確認後に 0.8 昇格可 |
| 4 | NEW ユーアイ GC | **0.8** | 公式 KO ページ + オーシャンビュー + 宗像大社隣接 |
| 5 | 周防灘 CC | **0.8** | 全ホール周防灘ビュー・PGA シニアトーナメント・50 周年 |
| 6 | 皐月天拝 [PGM] | **0.7** | 太宰府近接は強みだが PGM 標準コース |
| 7 | 皐月竜王 [PGM] | **0.7** | hub-budget の筆頭候補だが 2024 セルフ化で差別化は価格のみ |
| 8 | かほ GC | **0.7** | 標準コース |
| 9 | チサン遠賀 [PGM] | **0.7** | 標準 PGM 27H |
| 10 | 瀬板の森 | **0.7** | 市営・公式 403 問題あり |
| 11 | 西日本 CC | **0.8** | ゲーリー・プレーヤー設計・SEO フックとして強力 |
| 12 | JR 内野 CC | **0.8** | 公式 KO/EN + JR ブランド + フラット設計明記 |
| 13 | 夜須高原 CC | **0.8** | 楽天 4.4/2,629 件・27H 高原・三和スポーツ運営 |
| 14 | 八女上陽 GC | **0.8** | 宿泊施設 15 室+5 棟・イアン・ベーカー・フィンチ設計・希少性 |
| 15 | 福岡サンレイク GC | **0.7** | 楽天 4.3/1,515 件は評価高いが突出したフックは薄い |

MEDIUM (0.8) 判定: 8 件 / DEFAULT (0.7) 判定: 7 件
既存 35 件の priority 0.8 コース数と比較して妥当な水準。

### 6.3 access-*.html の priority

新規 15 件に対応する `access-{slug}.html` は既存と同じ **0.7** を適用。

---

## §7 area-*.html / hub-*.html / sitemap-guide.html への追加方法

### 7.1 観測フェーズ抵触チェック

**HTML 改修は Day 28 (2026-06-03) GO 後まで禁止。**
以下の §7 は「Phase B 着手後の実装設計」として今から設計を確定しておくことが目的。実際の HTML ファイル変更は Phase B 着手まで行わない。

### 7.2 area-*.html への追加 (追加対象 4 エリア)

**area-itoshima.html** (4 → 6 コース)
- 追加: `course-shimaseaside` (pos.5) / `course-raizan` (pos.6)
- ItemList の numberOfItems を 4 → 6 に更新
- meta description の「4 コース」を「6 コース」に更新 (ja/en/ko 3 言語)
- `<title>` タグの「4 コース」を「6 コース」に更新
- BreadcrumbList は変更不要
- structured data の Article の description 更新 (6 コース記載)

**area-kitakyushu.html** (10 → 14 または 15 コース)
- 追加: `course-classic` / `course-newui` / `course-chisan-onga` / `course-seitanomori` (+ `course-suonada` で +5)
- タイトルは「北九州・宗像エリア」のまま変更不要 (周防灘の拡張は「旧豊前」地域まで含む広義の北九州生活圏)
- meta description への「14 コース」または「15 コース」への更新
- ItemList に追加コースの ListItem を append

**area-chikugo.html** (7 → 11 コース)
- 追加: `course-satsuki-tenpai` / `course-yasukogen` / `course-yamejoyo` / `course-sunlake`
- 皐月天拝の追加で「筑紫野市」が初登場 (既存は太宰府・小郡・久留米中心) → meta description に「筑紫野・八女・みやま」を追記

**area-chikuho.html** (6 → 9 コース)
- 追加: `course-satsuki-ryuoh` / `course-kaho` / `course-nishinihon` / `course-jruchino`
- ただし西日本 CC (直方市) の追加で「直方市」が初登場 → meta description の地名リストに追記

### 7.3 hub-*.html への追加 (Phase B)

**hub-budget.html**
- 追加コース (主): 皐月竜王 (¥3,332〜・最安値候補) / かほ (¥5,869〜) / チサン遠賀 (¥5,878〜) / 瀬板の森 (¥7,728〜)
- 追加の際は Decoy 価格カード CSS (Phase 3) との整合を佐藤美咲 (cvr-optimizer) に確認

**hub-beginner.html**
- 追加コース (主): JR 内野 CC (「フラットにデザイン」公式明記)
- 追加コース (副): 皐月天拝 / チサン遠賀 (遠賀コース)

**hub-traveler.html**
- 追加コース (主): NEW ユーアイ / 志摩シーサイド / 夜須高原 / 八女上陽 / 周防灘
- 追加コース (副): 福岡雷山 / 福岡サンレイク
- 八女上陽 GC は「宿泊込みプラン」専用セクションを新設することを検討 (cvr-optimizer 連携推奨)

**hub-business.html**
- 追加コース (主): ザ・クラシック GC (2028 日本女子オープン) / 西日本 CC (ゲーリー・プレーヤー設計)
- 追加コース (副): 志摩シーサイド / 夜須高原 / 八女上陽

### 7.4 逆流ナビ (Phase 1A「Explore More」) の宛先設計

新規各コースの詳細ページ内 Related セクションで表示する「同エリア・同ペルソナのコース」の宛先候補:

| コース | Related 推奨宛先 (3 件) |
|---|---|
| ザ・クラシック GC | 西日本 CC (同ハブ) / 若宮コース (同エリア) / 福岡国際 CC (大会開催繋がり) |
| 志摩シーサイド CC | 芥屋 GC (同エリア・筆頭) / NEW ユーアイ (海景色) / クイーンズヒル (同エリア) |
| 福岡雷山 GC | 志摩シーサイド (同エリア) / 芥屋 GC (同エリア) / 伊都 GC (同エリア) |
| NEW ユーアイ GC | 志摩シーサイド (海景色) / チサン遠賀 (同エリア) / 若宮コース (同エリア) |
| 周防灘 CC | 門司 GC (同エリア・遠端) / 北九州 CC / 瀬板の森 (北九州系) |
| 皐月天拝 [PGM] | 皐月竜王 (同ブランド) / 太宰府 GC (太宰府近接) / 筑紫野 CC (同市) |
| 皐月竜王 [PGM] | 皐月天拝 (同ブランド) / かほ (同エリア・budget) / チサン遠賀 (同ブランド) |
| かほ GC | 皐月竜王 (同エリア) / 麻生飯塚 (同市) / JR 内野 (同市) |
| チサン遠賀 [PGM] | NEW ユーアイ (同エリア) / ミッションバレー (同エリア遠賀郡) / 皐月竜王 (同ブランド) |
| 瀬板の森 | 九州 GC 八幡 (同市周辺) / 北九州 CC / チサン遠賀 (北九州系 budget) |
| 西日本 CC | ザ・クラシック (同グループ CMG) / 北九州 CC / 直方周辺コース |
| JR 内野 CC | かほ (同市) / 麻生飯塚 (同市) / 皐月竜王 (beginner 系) |
| 夜須高原 CC | 皐月天拝 (朝倉郡隣接) / セントラル福岡 (朝倉郡同) / 八女上陽 (南福岡旅行セット) |
| 八女上陽 GC | 夜須高原 (旅行セット) / 久留米 CC (筑後代表) / 福岡サンレイク (同エリア南部) |
| 福岡サンレイク GC | 有明 CC (筑後南部) / 八女上陽 (同エリア) / 久留米 CC (筑後代表) |

---

## §8 hreflang / og:locale 設計

### 8.1 一般方針 (13 件・Tier 5 日本語のみ)

既存 35 件の area-*.html / course-*.html と同じ構造を適用。
URL 共通 (単一 URL) + content.c-{lang} クラスで言語切替の設計のため、hreflang は同一 URL で ja/en/ko/x-default を全て自己参照する。

```html
<link rel="alternate" hreflang="ja" href="https://fukuoka-golf-guide.com/course-{slug}.html">
<link rel="alternate" hreflang="en" href="https://fukuoka-golf-guide.com/course-{slug}.html">
<link rel="alternate" hreflang="ko" href="https://fukuoka-golf-guide.com/course-{slug}.html">
<link rel="alternate" hreflang="x-default" href="https://fukuoka-golf-guide.com/course-{slug}.html">
```

og:locale は既存と同じ `ja_JP` 基準。

### 8.2 KO 公式対応 2 件 (NEW ユーアイ / JR 内野) の特別設計

#### 基本方針: 「外部 KO ページへの誘導リンク」を加えるが、hreflang の URL 設計は変えない

**理由**: 既存 wakamiya (Tier 1) の設計と整合を保つ。wakamiya はすでに Tier 1 (公式 KO 直対応) として i18n_course_compatibility.json に記録されているが、hreflang の URL 構造は他コースと同一 (単一 URL の自己参照) のはず。これを崩すと全 hreflang 設計に影響が出る。

**KO 公式ページを持つ 2 件の具体的差別化**:

- KO コンテンツセクション (`content.c-ko` クラス) の中に外部 KO ページへの直接リンクを CTA として設置
  ```html
  <a href="https://m-uigc.com/kr/index.html" target="_blank" rel="noopener">
    공식 한국어 페이지
  </a>
  ```
- structured data (JSON-LD) の SportsActivityLocation または LodgingBusiness の `sameAs` フィールドに公式 KO ページ URL を追加
  ```json
  "sameAs": [
    "https://m-uigc.com/",
    "https://m-uigc.com/kr/index.html"
  ]
  ```

#### NEW ユーアイ GC の翻訳品質問題

公式 KO ページの翻訳品質判定が一次調査で割れている (評価 A「自然」vs 評価 B「機械翻訳」)。
**対処**: 当サイトの KO コンテンツセクション内で「공식 한국어 사이트로 이동」とリンクするのみとし、翻訳品質の評価はしない。ただし当サイト側の KO コンテンツには「자동번역」表示の有無を secondary 検証結果に基づいて判断する。

#### JR 内野 CC の KO/EN 対応

機械翻訳であることが明確 (「컴룸」等不自然な直訳確認済)。
当サイトの KO/EN セクション内に「자동번역 안내: JR내야 컨트리 클럽 공식 사이트의 한국어 페이지는 자동번역입니다.」と注記を推奨。CLAUDE.md §8 の倫理方針「機械翻訳をネイティブ翻訳と偽る」禁止に準拠。

#### i18n_course_compatibility.json 更新案 (Phase B 着手時)

```json
{"file": "course-newui",    "name": "NEWユーアイゴルフクラブ", "tier": 1.5,
 "ko_url": "https://m-uigc.com/kr/index.html", "ko_quality": "要ネイティブ検証",
 "en_url": null, "note": "公式KO直対応・品質確認後Tier1昇格判断"},
{"file": "course-jruchino", "name": "JR内野カントリークラブ",    "tier": 3,
 "ko_url": "https://www.jruchino.cc/apps/kr", "ko_quality": "machine",
 "en_url": "https://www.jruchino.cc/apps/en", "en_quality": "machine",
 "note": "JR九州系・自動번역明示必要"}
```

---

## §9 Phase B 着手時の推奨実装順序

### 9.1 前提 (Day 28 GO 後)

`OBSERVATION_PLAYBOOK.md` の判定スレッショルドを Day 28 (2026-06-03) に照合し、GO が出た段階で以下の順序で着手する。観測中の HTML 改修禁止は Day 28 終了まで厳守。

### 9.2 推奨実装順序 (15 件 + 関連ページ)

**Phase B-0: 前準備 (1〜2h)**
1. `jalan_golf_mapping.json` に 15 件追記 (TIER1_SUMMARY.md §6.1 の JSON を適用)
2. `rakuten_gora_mapping.json` に 15 件追記 (TIER1_SUMMARY.md §6.2 の JSON を適用)
3. `i18n_course_compatibility.json` に NEW ユーアイ (Tier 1.5) / JR 内野 (Tier 3) を追記
4. `generate_sitemap.py` の COURSES リストに 15 件を追加 (priority 値は §6.2 通り)

**Phase B-1: パイロット 1 件 (4〜6h)**

推奨: **志摩シーサイド CC** (`course-shimaseaside`)
選定理由:
- itoshima エリアの既存 4 件と完全に同構造 (18H/シーサイド/日本語のみ/Tier 5)
- 料金確認済 (¥19,000 / 公式直確認)
- 公式アクセス問題なし
- hub-traveler という既存ハブへの追加テストとして最適

手順:
1. `/create-course-page course-shimaseaside` (pre-flight 4 チェック実行)
2. `course-shimaseaside.html` + `access-shimaseaside.html` 生成 (preview)
3. 3 言語切替 / dataLayer / JSON-LD / hreflang 確認
4. area-itoshima.html の ItemList に追加 (preview で確認)
5. ユーザー承認後に REPO_ROOT にも反映

**Phase B-2: HIGH priority コース 3 件 (推定 2 件/日)**

順序: ザ・クラシック GC → NEW ユーアイ GC → 西日本 CC

選定理由:
- ザ・クラシック: 2028 日本女子オープン関連 KW での早期インデックス効果 (時間軸が重要)
- NEW ユーアイ: 公式 KO ページ連携 + wakamiya クラスタ拡張 → Phase 4-B KO 戦略に直結
- 西日本 CC: ゲーリー・プレーヤー設計 KW は競合が少ない → 早期上位表示狙い

**Phase B-3: hub-traveler 強化コース 4 件**

順序: 八女上陽 GC → 夜須高原 CC → 周防灘 CC → 福岡サンレイク GC

選定理由: hub-traveler のコンテンツ充実 + 宿泊 KW (八女上陽) は PV 単価が高い

**Phase B-4: chikuho 充実コース 4 件**

順序: 皐月竜王 → かほ → チサン遠賀 → JR 内野 CC

選定理由: chikuho エリアの budget ゾーン強化 + JR 内野の KO/EN 対応でインバウンド補強

**Phase B-5: 残り 3 件**

順序: 瀬板の森 → 皐月天拝 → 福岡雷山 GC

留意:
- 瀬板の森: 公式 403 問題のため「じゃらん + 楽天のみ根拠」で簡素なページ構成
- 福岡雷山 GC: 料金未確認のため「要確認」扱いで公開 OR secondary 検証後に公開

### 9.3 sitemap.xml 更新タイミング

15 件を全件追加後に `generate_sitemap.py` を 1 回実行して sitemap.xml を更新する。個別追加のたびに sitemap を更新する必要はない (バッチ更新)。ただし B-1 パイロット後にドライランで件数確認は必須。

---

## §10 リスクと回避策

### 10.1 既存 35 コースへの影響

| リスク | 深刻度 | 回避策 |
|---|---|---|
| area-kitakyushu の「10 コース」が「14〜15 コース」になると meta description が古くなる | 低 | Phase B 着手時に数字更新。観測中は変更しない |
| area-chikugo に皐月天拝を追加すると「筑後」ページに「筑紫野市」が混在する | 低〜中 | 見出しに「筑紫野・朝倉エリア」を追記して整合性を持たせる。既にセントラル福岡 (朝倉郡) が chikugo に収録されており前例あり |
| area-chikuho に西日本 CC (直方市) を追加すると「筑豊・直方」の説明が必要 | 低 | 直方市は「旧筑豊炭田圏」の核心都市。chikuho の本来の定義に含まれるため説明は容易 |
| chikuho の課題 15 件 (現行 6 + 追加 4 = 10 件目前) が area-chikugo (7 → 11) と拮抗 | 低 | コース数の均等化は SEO 上問題なし。各ページが適切な地域を代表していれば良い |
| 皐月天拝・夜須高原ともに「朝倉郡筑前町」のため同一市町村重複 | 低 | 別コースなので問題なし。ただし Related セクションで相互リンクを設置すれば内部リンク密度向上に活用できる |

### 10.2 SEO リスク (エリア再分類起因)

| リスク | 深刻度 | 回避策 |
|---|---|---|
| ザ・クラシック GC を kitakyushu に入れると「宮若市 ゴルフ場」KW で「筑豊」ページが上位に来ないリスク | 低〜中 | course-classic.html の本文に「宮若市 ゴルフ」KW を明示。エリアハブからのクリックは「宮若 IC 10 分・北九州エリア」と文脈化する |
| 新エリアを作らなかったことで「宗像市 ゴルフ場」の専用ページがない | 低 | area-kitakyushu が「北九州・宗像エリア」を謳っているため、既存のエリアページが「宗像市 ゴルフ場」KW でもインデックスされている可能性がある。追加コースが増えれば自然強化される |
| 福岡雷山 GC の料金未確認のまま公開すると E-E-A-T 低下 | 高 | CLAUDE.md §7 ハルシネーション禁止に従い、料金は「公式サイトでご確認ください (TEL: 092-323-8181)」として暫定公開 OR 料金確認後に公開 |
| 「夜須高原 ゴルフ 料金」KW で楽天 GORA が上位に出続けビジター平日標準料金が曖昧 | 中 | secondary 検証で確定後に掲載。掲載前は「¥10,510〜」(セルフデー料金) と最低価格のみ記載し「要公式確認」を明記 |

### 10.3 カニバリゼーションリスク

| 懸念 | 深刻度 | 判定 |
|---|---|---|
| 皐月天拝 + 皐月竜王 (同ブランド・同地域) でカニバリ | 中 | 料金帯・コース性格・2024 年改装の有無で明確に差別化できる。それぞれ別の course-*.html を持つことは適切 |
| 夜須高原 CC + セントラル福岡 (同じ朝倉郡筑前町) | 低 | コース性格・運営・料金が全く異なる。カニバリにはならない |
| 志摩シーサイド CC + 西戸崎シーサイド (どちらも「シーサイド」) | 低 | 糸島と福岡市という別エリア。「シーサイド」KW は共有するが地名 KW で分離される |

田中健太郎 (seo-strategist) への確認依頼: 皐月天拝・皐月竜王の同ブランド 2 コース同時追加について、「皐月ゴルフ 福岡」KW でのカニバリ判定を依頼することを推奨する。

### 10.4 工数と ROI 推計

| フェーズ | 推定工数 | 推定 ROI |
|---|---|---|
| Phase B-0 (前準備) | 1〜2h | 直接 PV 増なし・基盤整備 |
| Phase B-1 (パイロット 1 件) | 4〜6h | +50〜100 PV/月 (糸島 KW での早期インデックス) |
| Phase B-2 (HIGH priority 3 件) | 6〜10h | +200〜400 PV/月 (「2028 女子オープン」「ゲーリー・プレーヤー 福岡」等 Long-tail) |
| Phase B-3 (traveler 4 件) | 8〜12h | +150〜300 PV/月 (「ゴルフ 宿泊 福岡」「夜須高原 ゴルフ」等) |
| Phase B-4 (chikuho 4 件) | 6〜10h | +200〜350 PV/月 (「飯塚 ゴルフ 安い」「JR 内野 ゴルフ」等) |
| Phase B-5 (残 3 件) | 4〜8h | +80〜150 PV/月 |
| **合計** | **29〜48h** | **+680〜1,300 PV/月 (3〜4 ヶ月後の安定値推計)** |

ROI 計算根拠: 既存 35 コースの平均 PV/コース/月 を基準に「新規コース 1 件 = 平均 +40〜85 PV/月」と推計。ザ・クラシック / 西日本 CC / 夜須高原 CC は Long-tail KW の固有性から上振れを見込む。アフィリエイト貢献はクリック数 × コンバージョン率で別途計測。

---

## 付録 A: 観測抵触チェック (再確認)

| 確認項目 | 結果 |
|---|---|
| HTML ファイル改修 | ○ (今回ゼロ) |
| JSON マッピング改修 | ○ (今回ゼロ・Phase B 着手後の追記案のみ) |
| sitemap.xml 変更 | ○ (今回ゼロ) |
| GA4 タグ変更 | ○ (今回ゼロ) |
| course_data.json 変更 | ○ (今回ゼロ) |
| 観測サンプルへの影響 | ○ (なし・data/ 配下 Markdown 作成のみ) |

**本ドキュメントは CLAUDE.md §6「観測期間中の許容例外 - ドキュメント (Markdown) の追加・更新」に完全準拠。**

---

## 付録 B: 専門家連携依頼事項

| 依頼先 | 依頼内容 | 優先度 |
|---|---|---|
| 田中健太郎 (seo-strategist) | 皐月天拝・皐月竜王の同ブランド 2 コース追加によるカニバリ判定。「皐月ゴルフ 福岡」KW での評価 | 高 |
| 佐藤美咲 (cvr-optimizer) | hub-budget の Decoy 価格カード (Phase 3) に皐月竜王 ¥3,332 を追加する際の配置設計 | 中 |
| 金星誠 (inbound-strategist) | NEW ユーアイ GC の公式 KO ページ翻訳品質の最終判定。wakamiya + NEW ユーアイ + JR 内野の「Tier 1 KO クラスタ」戦略への組み込み方 | 高 |
| 中村麻衣 (fact-checker-secondary) | 夜須高原 CC のビジター平日標準料金 / 福岡サンレイク GC のヤード数不一致 (6,723 vs 6,880) / NEW ユーアイ KO 翻訳品質の独立検証 | 高 |
