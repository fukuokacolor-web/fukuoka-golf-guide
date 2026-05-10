# 🇰🇷 KO 市場リサーチ報告書 (Phase 4-B 準備)

**作成日**: 2026-05-10 (専門家会議 Tier 2 / 金星誠 インバウンドタスク)
**目的**: Day 28 (2026-06-03) の wakamiya 単独 KO LP 着手判断 + GO 確定後の launch 速度を 1 週間→1 日に短縮するための事前リサーチ
**対象**: 韓国市場 (KR ゴルファー・福岡空港 30 分圏 wakamiya 集中訴求)
**実行時間**: 約 5h (調査 4h + 文書化 1h)
**観測ノイズ**: 0 (HTML 改修なし・GA4 計測非干渉)

---

## 1. KO 流入の現状 (Day 3 観測時点・2026-04-12〜2026-05-08 の 28 日累計)

| 指標 | 値 | 注記 |
|---|---|---|
| 7 日 KR セッション数 | 2 | NEXT_SESSION.md Day 3 観測 |
| 28 日換算 (推定) | ~8 | 線形推定 |
| 28 日 KR `click_affiliate` | **0** | 直近 7 日の Japan 34 + Taiwan 1 = 35 件には KR 含まれず |
| KR トラフィックソース | **不明** | カスタムディメンション登録 5/9 後に詳細追跡可 |

**判定基準** (`OBSERVATION_PLAYBOOK.md` §5):
| KR セッション (月換算) | Phase 4-B Option | 着手判定 |
|---|---|---|
| > 50 | A (Tier 別バッジ全件・wakamiya 含む 8 コース) | GO |
| 20-50 | A or B 検討 | HOLD |
| **< 20** ← **現状** | **B (wakamiya 単独 LP) 優先** | **本報告書の準備が活きる** |

**現実認識**: 線形推定 8/月 = 月20未満 → **Option B (wakamiya 単独 LP) ルートが最有力**。本報告書はそれ前提で構築。

### 観測中の更新タスク

OBSERVATION_PLAYBOOK 沿って Day 7 (5/13) / Day 14 (5/19) / Day 28 (6/3) で本セクション §1 の値を更新。

---

## 2. wakamiya 差別化ポジション再確認

`WAKAMIYA_KO_LP_DESIGN.md` で確定済の差別化軸を本報告書視点で再評価:

| 強み | 韓国市場での相対価値 | 補足 |
|---|---|---|
| **公式 /ko-index 直対応** | ★★★ (差別化の核心) | 福岡 35 コース中 唯一・「機械翻訳 vs 公式」訴求 |
| ¥4,000 から | ★★★ (KR 国内 ¥15-25k 比 1/4-1/6) | 価格訴求は最強 |
| 福岡空港 30 分 | ★★ (LCC 直行便豊富) | アクセス難ハードル低 |
| 18H Par 72 | ★★ (本格コース) | 評価ポイント |
| 미야와카 온천 (1 박 2 일) | ★★★ (韓国客の旅行スタイルに合致) | 公式 KO サイトもプッシュ |
| 1 인 예약 (2026-05〜) | ★★ (KR でも増加中の単独ゴルフ) | wakamiya の新サービス |

### 🆕 公式被リンク発見

調査中に判明:
- **VISIT FUKUOKA 韓国語版** (https://www.crossroadfukuoka.jp/kr/articles/golf_fukuoka) で福岡ゴルフ場特集
- 同サイト wakamiya 紹介ページ: https://www.crossroadfukuoka.jp/kr/spot/10351
- → **公式観光局による被リンク基盤が既に存在**。Phase 4-B 公開時に「VISIT FUKUOKA 認定」を訴求材料に活用可能 (wakamiya 公式 + VISIT FUKUOKA + fukuoka-golf-guide.com の 3 層信頼)

---

## 3. Naver SERP 上位ドメイン分析 (主 KW × 3)

### KW1: 「후쿠오카 골프」(月 Vol 推定 3,500-6,000 / 難度 4)

| 順位 | ドメイン | 種別 |
|---|---|---|
| 1 | crossroadfukuoka.jp/kr | 公式観光局 |
| 2 | kr.trip.com | 旅行사이트 |
| 3 | jgolfclub.com | 일본골프 専門여행사 |
| 4 | ilbongolf.com | 일본골프닷컴 (商用) |
| 5 | tourvis.com | 旅行패키지 |
| 6 | dealbada.com/forum_golf | **커뮤니티** |
| 7 | crossroadfukuoka.jp/kr/spot/10344 | 公式 (별 코스) |
| 8 | wtg.kr | 차량서비스 |
| 9 | experiences.myrealtrip.com | 旅行사이트 |
| 10 | tripstore.kr/blog | 블로그/商用 |

### KW2: 「큐슈 골프」(月 Vol 推定 1,200-2,500 / 難度 3)

| 順位 | ドメイン | 種別 |
|---|---|---|
| 1 | accordiagolf.com/kr/kyushu | 公式 골프장 운영사 |
| 2 | insightkorea.co.kr | 뉴스 |
| 3 | tourvis.com | 旅行패키지 |
| 4 | travel.interpark.com | 旅行사이트 |
| 5 | 5golf.co.kr/GolfKyushu | 商用 |
| 6 | impacttour.co.kr/큐슈 | 商用 |
| 7 | ssg.com | 商用 (큐슈 골프 상품) |
| 8 | savetour.co.kr | 商用 |
| 9 | okgolftour.kr | 商用 |
| 10 | cafe.daum.net/t.o.mgolf | **커뮤니티/카페** |

### KW3: 「일본 골프 여행」(月 Vol 推定 8,000-15,000 / 難度 5)

| 順位 | ドメイン | 種別 |
|---|---|---|
| 1 | ilbongolf.com | 商用 |
| 2 | kr.trip.com/blog/japan-golf-travel | 旅行사이트 |
| 3 | tripstore.kr/blog | 블로그 |
| 4 | brunch.co.kr/@18fdc03ebd99494 (RYUKANG) | 블로그 |
| 5 | brunch.co.kr/@travie | 블로그 |
| 6 | golfscanner.co.kr | 商用 |
| 7 | goodshotjuntour.com/Japan | 商用 |
| 8 | irumtour.net | 商用 |
| 9 | ybtour.co.kr (노랑풍선) | 大手여행사 |
| 10 | hanatour.com | 大手여행사 |

### 構造的観察

- **重複排除後 27 ドメイン中、純粋 블로그/뉴스/커뮤니티は 7 件のみ** (商用여행사が圧倒的)
- 主 KW での被リンクアウトリーチは **商用여행사の壁**で困難
- → **ロングテール KW (와카미야 골프 等) + Influencer 連携** が ROI 最適 (§5・§6)

---

## 4. 被リンク獲得候補リスト (10-15 件)

実装難易度は 1 (容易・自由投稿可) 〜 5 (極難・大手商用との交渉) で評価。

### 高 ROI Tier (難度 1-2・最初に着手)

| サイト | URL | 種別 | PA | 連絡 | 難度 |
|---|---|---|---|---|---|
| **딜바다 골프포럼** | http://www.dealbada.com/bbs/board.php?bo_table=forum_golf | 커뮤니티 | 中 | 自由投稿 | 1 |
| **DCInside 골프 갤러리** | https://gall.dcinside.com/board/lists/?id=golf | 커뮤니티 | 中 | 익명 글 | 1 |
| **TOM Golf 카페 (Daum)** | https://m.cafe.daum.net/t.o.mgolf | 카페 | 中 | 가입 후 글 | 2 |
| **@japantoyotarent (Threads)** | https://www.threads.com/@japantoyotarent | influencer | 中 | DM | 2 |
| **@fine___tour (Threads)** | https://www.threads.com/@fine___tour | influencer | 中 | DM (큐슈 패키지専門) | 2 |
| **Calarca My Store 블로그** | https://calarca.net/ | 블로그 | 低-中 | 댓글 + 이메일 | 2 |

### 中 ROI Tier (難度 3-4・第2 wave)

| サイト | URL | 種別 | PA | 連絡 | 難度 |
|---|---|---|---|---|---|
| Brunch RYUKANG | https://brunch.co.kr/@18fdc03ebd99494/598 | 블로그 | 中 | brunch 메시지 | 3 |
| Brunch Travie | https://brunch.co.kr/@travie/525 | 블로그 | 中 | brunch 메시지 | 3 |
| InsightKorea 산업 섹션 | https://www.insightkorea.co.kr/ | 뉴스 | 高 | 보도자료 | 3 |
| GolfMagazineKorea | https://www.golfmagazinekorea.com/ | 뉴스 | 高 | 보도자료 | 3 |
| TripStore Blog | https://www.tripstore.kr/blog/ | 旅行사이트 | 高 | blog@tripstore.kr | 4 |
| GolfNTour 후기 | https://www.golfntour.co.kr/review/ | 商用 | 中 | 와카미야CC 후기 既掲載で参考 | 4 |
| TeraTour 마스터 | https://www.teratour.co.kr/ | 商用 | 中 | 提携プロモ枠 | 4 |
| Triple Guide | https://triple.guide/ | 旅行사이트 | 中 | 컨텐츠 파트너십 | 4 |

### 低 ROI Tier (難度 5・予算/時間あれば)

| サイト | URL | 種別 | PA | 連絡 | 難度 |
|---|---|---|---|---|---|
| Trip.com Korea Blog | https://kr.trip.com/blog/ | 旅行사이트 | 高 | contributor program | 5 |

→ **Day 28 GO 後の最初 2 週間は高 ROI Tier (難度 1-2) 6 件に集中**。1 日 2-3 件アウトリーチで 1 週間で網羅可能。

---

## 5. Naver Cafe / Kakao コミュニティ

韓国人ゴルファーの主要交流場:

| 名前 | URL | 활동 인원推定 | 福岡関連 | 寄稿性 |
|---|---|---|---|---|
| **TOM Golf 카페 (Daum)** | https://m.cafe.daum.net/t.o.mgolf | 5万+ | 일본 카테고리 別途・후쿠오카 자료多 | 高 (자유게시판) |
| 「자유 골프인 (자골인)」 Naver 카페 | (Naver で要検索) | 10万+ 推定 | 일본 갈래有 | 中 |
| 「일본 골프투어 정보공유」 Naver 카페 | (Naver で要検索) | 1-3 万 | 후쿠오카 스레多 | 中 |
| **딜바다 골프포럼** | http://www.dealbada.com/bbs/group.php?gr_id=forum | 30 万+ | 후쿠오카 스레 10件+ | 高 |
| **DCInside 골프 갤러리** | https://gall.dcinside.com/board/lists/?id=golf | 일일 1000+ | 후쿠오카・구마모토 후기多 | 高 (익명) |
| Kakao Open Chat 「일본 골프 투어 정보방」 | (kakao 검색) | 200-500 推定 | 中 (관리자 협의要) | 中 |

### 構造的観察

- **Naver Cafe は閉鎖性ゆえ Google にインデックスされにくい** (cafe.naver.com の壁)
- **Daum TOM Golf + 딜바다 + DC 골프갤이 実用的な 3 強** (オープン構造で SEO 価値も発生)
- Naver Cafe への投稿は SEO 流入には貢献しにくいが、コミュニティ内バイラルで KO セッション増加に寄与

---

## 6. 韓国 YouTuber / Influencer

| チャンネル | URL | 구독자 | 일본 골프 비율 | 협업 가능性 |
|---|---|---|---|---|
| **★ 도쿄린짱 골프채널TV** | https://www.youtube.com/channel/UC9oN1rUHHN8DFLcHul5ssrQ | 推定 3-10 万 | **100%** (전국 골프장 리뷰특화) | **높음** (한국 대상 일본 골프 専門・第一候補) |
| **★ @japantoyotarent (Threads)** | https://www.threads.com/@japantoyotarent | 1-3 만 | 高 (TOP 5 시리즈で福岡言及) | 高 (DM・既存ラリエスト) |
| **★ @fine___tour (Threads)** | https://www.threads.com/@fine___tour | 数千 | 큐슈/가고시마 골프 100% | 高 (DM・큐슈 専門) |
| Chris (@golife_chris) | https://www.instagram.com/golife_chris/ | 1-5 万 | 中 (一部日本) | 中 |
| 칼리 (@inno7373) | https://www.instagram.com/inno7373/ | 1-3 만 | 中 (일본 + 베트남) | 中 |
| 김국진TV 거침없는 골프 | https://www.youtube.com/@gookjin_tv | 16.7 만 | 低-中 | 中 (연예인・비용 高) |
| KLEPORTSTV 한국레포츠TV | https://www.youtube.com/channel/UCQhjZv3NVzU8dqsbbIWrw2Q | 1-3 만 | 中 | 中 |

**Tier 1 候補 (★)** に集中。

### 推奨アプローチ

1. **도쿄린짱**: 1 편 협찬영상 (와카미야 라운드 리뷰) → 위 사용 가능 추정 비용 30-100 만원・流入 倍化期待
2. **@japantoyotarent**: 既存 「福岡 TOP5」コンテンツへの wakamiya 追加掲載交渉 → 0-10 만원 (記事掲載提供者として)
3. **@fine___tour**: 큐슈 패키지 콘텐츠で wakamiya 紹介 → 0-30 만원

→ **Day 28 GO 後 1 ヶ月以内に 도쿄린짱 1 편 + Threads 2 件**で初期 KO 流入の倍増を狙う。

### 避けるべき選択肢

- 박세리 (SERl_PAK 60 만+) や 김국진TV (16.7 만): 비용対効果 低い (1 편 500 만원~/Tier 1 인플루언서)
- 도쿄규짱: 논란 이력あり

---

## 7. SEO 戦略・低競争 KW 5 個

主 KW (难度 3-5) は商用여행사が独占 → **ロングテール戦略**で wakamiya 専用 KW を 6 ヶ月以内に上位独占:

| KW | 月 Vol 推定 | 競争度 | 難度 | 狙う順位 |
|---|---|---|---|---|
| **와카미야 골프** | 50-200 | 1 | 1 | 1 位 (3 ヶ月) |
| **트라이얼 골프 리조트** | 100-300 | 2 | 2 | 1 位 (3 ヶ月) |
| **후쿠오카 4000엔 골프** | 50-150 | 1 | 1 | 1 位 (3 ヶ月) |
| **후쿠오카 한국어 골프장** | 30-100 | 1 | 1 | 1 位 (1 ヶ月) — 公式 /ko-index と棲み分け |
| **미야와카 온천 골프** | 20-80 | 1 | 1 | 1 位 (3 ヶ月) |

**累計推定**: 月 250-830 検索ボリューム → CTR 25% 仮定で **月 60-200 KO 流入** (Phase 4-B GO 判定基準 50/月をクリア可能)

主 KW でランクインを狙う場合の戦略:

- 「후쿠오카 골프」: **見送り** (商用 SERP 飽和・短期 ROI 期待薄)
- 「큐슈 골프」: **長期 (12 ヶ月)** 視点で被リンク蓄積 → 10 位入り狙う
- 「일본 골프 여행」: **見送り** (大手여행사の独占・SEO 競争不利)

---

## 8. Day 28 GO 後マイルストーン (月 ¥10 万到達)

| 日 | 作業 | 担当 | 工数/コスト |
|---|---|---|---|
| **D28 (6/3)** | GO 判定・本報告書最新化・ネイティブ校正発注 (Lancers ¥1.5 万) | User+Claude | 1h+1.5 万円 |
| D28+5 (6/8) | 校正納品・LP HTML 実装 (course-*.html テンプレ流用) | Claude | 5h |
| D28+6 (6/9) | sitemap/hreflang/JSON-LD/内部リンク・wakamiya 公式に画像許諾依頼 | Claude+User | 1h |
| **D28+7 (6/10)** | **公開**・GSC KR インデックス申請・Naver Webmaster 登録 | User | 1h |
| D28+8〜21 | アウトリーチ第1 wave (難度 1-2 / 6 件): 딜바다・DC 갤・TOM Cafe・Threads × 2・Calarca | User+Claude | 3h |
| D28+10 (6/13) | **도쿄린짱 협업打診** (DM + 와카미야 라운드 리뷰 提案) | User | 0.5h |
| D28+15 (6/18) | アウトリーチ第2 wave (難度 3 / 4 件): Brunch × 2・InsightKorea・GolfMagazine | User+Claude | 2h |
| D28+30 (7/3) | **判定**: KO セッション 50+ / LP→公式 CTR 25%+ / アフィリ CVR 3%+ | — | — |
| D28+45 (7/18) | 月¥3-5 万収益化 (KO 専用ASP **GolfStay 申請**並行) | User | 1h |
| D28+60 (8/2) | 도쿄린짱 협업영상 公開 (協賛料 30-100 万원予算下りた場合) | User | コスト 30-100 万원 |
| **D28+90 (9/1)** | **月¥10 万到達 (累積)**: KO ¥3-5 万 + EN/JP 通常成長 ¥7-10 万 | — | — |

---

## 9. リスクと対応

| リスク | 兆候 | 対応 |
|---|---|---|
| KR セッション増えない (Day 28 < 月 20) | 観測中の自然成長ゼロ | Phase 4-B Option B 着手・本報告書活用 (見送りでなく) |
| 翻訳品質問題 | 「자동번역 같다」批判が SNS で発生 | ネイティブ校正必須 (Lancers ¥1.5 万)・wakamiya 公式コピー流用 |
| wakamiya 公式 KO ページ消失 | 차후 wakamiya 측 KO 페이지 削除 | 3 ヶ月毎の生死確認 (NEXT_SESSION.md 定期 task) |
| Naver SEO で評価されない | 6 ヶ月後も主 KW 50 位外 | hreflang ko + 韓国 IP からの被リンク必須・(Lancers でNaver SEO エキスパート発注) |
| 도쿄린짱 협업拒否 | 返信なし or 高額提示 | Tier 2 의 @japantoyotarent ・ @fine___tour に切り替え |
| 商用여행사の妨害 | 「와카미야 패키지」を強奪する商用記事の発行 | 직접 LP 의 E-E-A-T 강화 (저자명・조사일・독립적 검증)・商用 vs 中立サイトの差別化 |

---

## 10. 次セッション引き継ぎ

### 即行動可能 (Day 28 待たずに)

- **wakamiya 公式 KO ページの生存確認** (https://trial-golf-resort-wakamiya-course.com/ko-index): 5/13 / 5/19 / 6/3 各 Day で確認、消えていたら本報告書 §2 から差別化軸を再評価
- **Naver Webmaster Tools 登録準備**: site:fukuoka-golf-guide.com を Naver にインデックス申請 (Day 28 GO 後すぐ)
- **VISIT FUKUOKA との被リンク交渉**: 公式観光局 wakamiya 紹介ページ (crossroadfukuoka.jp/kr/spot/10351) へ「追加情報源」として相互被リンク提案メール下書き

### Day 28 GO 後 (本報告書活用)

- §4 高 ROI Tier 6 件のアウトリーチを最優先
- §6 도쿄린짱 + Threads × 2 への打診開始
- §7 ロングテール 5 KW で wakamiya LP の SEO 設計を確定 (`WAKAMIYA_KO_LP_DESIGN.md` §4 と整合)

### 観測中の更新タスク (本報告書 §1 の値を毎週更新)

- Day 7 (5/13): KR セッション数・新規流入元 (もしあれば) を §1 に追記
- Day 14 (5/19): 同上
- Day 28 (6/3): 同上 + Phase 4-B 判定 (Option A / B / 見送り)

---

## 11. 結論

- **現状の KR セッション (~8/月推定) は Phase 4-B Option A の閾値 (50/月) に届かない** → Option B (wakamiya 単独 LP) ルートが現実解
- 主 KW (후쿠오카 골프 等) は商用여행사が SERP を独占・短期投資効果薄 → **ロングテール 5 KW + Influencer 連携** が ROI 最適
- 도쿄린짱 (한국 대상 일본 골프 専門 YouTuber) + Threads 2 件 (@japantoyotarent / @fine___tour) が **韓国市場アクセスの最短経路**
- 公式 VISIT FUKUOKA に wakamiya 既掲載 → 「公式観光局認定」を訴求材料に活用可能 (差別化 = 公式直対応 + 公式観光局)
- Day 28 GO 後 90 日で月¥10 万 (KO ¥3-5 万 + EN/JP 累積 ¥7-10 万) が達成可能ロードマップ
