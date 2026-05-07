# wakamiya 単独訴求 LP 設計書 (Phase 4-A Option B)

**作成日**: 2026-05-06
**目的**: 福岡県内で唯一の「公式韓国語ページ直対応」コースである wakamiya を、韓国人ゴルフ客向けに集中訴求する韓国語 SEO ランディングページを設計
**実装タイミング**: 観測フェーズ Day 28 後 (KO セッション数次第で GO/見送り判断)
**前提**: `i18n_course_compatibility.json` で wakamiya を Tier 1 (公式 KO ページ直対応・/ko-index 確認済) と確定
**戦略**: 金星誠 (インバウンド) Option B 推奨 — Tier 1 が 1 件のみという現実は「分散実装」より「集中突破」が合理的

---

## 1. wakamiya 基本情報 (公式サイト調査結果・2026-05-06 時点)

| 項目 | 値 |
|------|------|
| 公式名 (JA) | トライアルゴルフ&リゾート WAKAMIYA COURSE (旧 若宮ゴルフクラブ) |
| 公式名 (EN) | Trial Golf & Resort Wakamiya Course |
| 所在地 | 福岡県宮若市乙野 1121 |
| 公式 URL | https://trial-golf-resort-wakamiya-course.com/ |
| KO ページ | /ko-index (★ 公式直対応・機械翻訳ではない) |
| EN ページ | /en-index |
| 福岡空港からの所要時間 | 都市高速・博多東IC経由 約30分 / 九州自動車道・福岡IC経由 約20-35分 / 天神・博多駅から約60分 |
| ホール数 | 18H |
| 最低料金 | ¥4,000 (午後スルー) |
| 平日料金 | ¥8,000〜15,500 |
| 土日祝料金 | ¥12,500〜17,000 |
| 午後スルー | ¥4,000〜7,000 (featured) |
| KO 予約方法 | 公式オンライン (valuegolf.co.jp 経由) / 電話 +81-949-54-0595 |
| jalan_id | gc02341 |
| rakuten c_id | 400051 |
| 既存サイト内リンク | course-wakamiya.html (3 言語) |

---

## 2. ターゲットペルソナ

**韓国 (ソウル / 釜山 等) 在住のゴルフ愛好家**:
- 福岡空港・北九州空港経由で 1.5-2h 圏内 (LCC 直行便豊富)
- ラウンド料金感覚: 韓国国内 ¥15-25k vs 福岡 ¥4-15k = **大幅安**
- 言語不安: 「予約フォーム・現地スタッフが日本語のみ」 → ボトルネック
- 情報源: Naver Cafe / Naver ブログ / Kakao グループ
- 旅行スタイル: 1 泊 2 日 / 2 泊 3 日のグループ旅行 (3-6 名)

---

## 3. 差別化ポジショニング: The One

| 要素 | 他 7 KO 対応コース | **wakamiya** |
|------|-------------------|--------------|
| KO UI | ❌ 機械翻訳 (Accordia/PGM ポータル) | ✅ **公式直対応** /ko-index |
| 信頼性 | △ 「번역기에 의존」感 | ✅ 「공식 한국어」感 |
| 顧客サポート | ❌ JP only (Tier 2-3) | △ JP + 公式 KO 予約フォーム |
| 周辺リゾート | △ 単独コース | ✅ **宮若温泉郷 + グループ施設** = 1 泊滞在型 |
| アクセス | 平均 30-50 分 | 福岡空港から 30-50 分 (同等) |

**コアメッセージ**: 「機械翻訳ではなく、**公式が韓国語で語りかける**福岡で唯一のコース」

---

## 4. SEO 戦略

### 主 KW (狙い順)
1. 「후쿠오카 골프 한국어」 (Fukuoka golf in Korean)
2. 「와카미야 골프 리조트」 (Wakamiya Golf Resort 韓国語表記)
3. 「Trial Golf Resort 한국어 예약」

### 副 KW
- 「후쿠오카 공항 골프」
- 「후쿠오카 1박 2일 골프」
- 「큐슈 골프 한국어 가능」
- 「후쿠오카 온천 골프」 (温泉訴求)
- 「와카미야 코스 가격」

### URL 候補
- ★ **`book-wakamiya-ko.html`** (Phase 2 LP の `book-*` 系列と整合・推奨)
- `wakamiya-korean-guide.html` (KW スタッフィング)
- `golf-wakamiya-korean.html`

### title / meta description
```
title: 후쿠오카 와카미야 골프 리조트 - 공식 한국어 페이지로 예약 | 후쿠오카 골프 가이드
description: 후쿠오카에서 유일하게 공식 한국어 페이지가 있는 골프장. 후쿠오카 공항에서 30-50분, ¥4,000부터. 온천 1박 2일 패키지 가능. 코스 정보·예약 방법·체크리스트.
```

---

## 5. LP 構造案 (8 セクション)

### Hero (ファーストビュー)
- 背景: コース写真 (春の森 / グリーン)
- H1 (KO): **「후쿠오카에서 유일한 공식 한국어 골프장」**
- 副題: TRIAL GOLF & RESORT WAKAMIYA COURSE
- バッジ群: ✈️ 후쿠오카 공항 30-50분 | ⛳ 18H | 💴 ¥4,000부터 | 🇰🇷 한국어 공식 사이트
- CTA: 「[공식 한국어 페이지에서 예약하기 →]」(公式 /ko-index へ external link・差別化要因の核心)

### Section 1: なぜ wakamiya だけが「公式韓国語」なのか
- 福岡 35 コース調査結果のサマリー (Tier 1 = 1 件のみ)
- 機械翻訳 vs 公式翻訳の違い (信頼性アピール・スクショ併記)
- データ出典: 「fukuoka-golf-guide.com 編集部 2026-05-06 全 35 コース調査」(E-E-A-T)

### Section 2: コース基本情報
- 18 ホール・パー (要追加 fetch・公式に確認)
- 福岡空港からのアクセス (都市高速 30 分 / 九州道 20-35 分)
- 価格表: 平日 ¥8,000-15,500 / 土日祝 ¥12,500-17,000 / **午後스루 ¥4,000-7,000** (featured)
- 2026 年 5 月から **1 인 예약** 開始 (公式情報・KO 客に魅力)
- 8 月から **카트 진입** 開始 (公式情報)

### Section 3: 韓国語予約の流れ (5 ステップ)
1. 公식 /ko-index 페이지에 접속
2. 온라인 예약 폼 (valuegolf.co.jp) 입력
3. 또는 전화: **+81-949-54-0595** (9-17 시)
4. 확인 메일 수신
5. 당일 체크인 (필요한 한국어 핵심 표현 12 개 표 — 既存 book-fukuoka-golf-foreigner.html から流用)

### Section 4: 주변 리조트·온천 (1 泊 2 日 패키지)
- 미야와카 온센쿄 (徒歩圏内 / 그룹 시설)
- 그룹 식사 시설 (정성스럽게 준비한 식사 - 公式 KO コピー流用)
- 추천 패키지 모델 (1 박 2 일 / 2 박 3 일)

### Section 5: 당일 흐름 체크리스트
- 카트 운행 (8 월 이후)
- 렌탈 클럽 / 슈즈 (요 확인)
- 식사 / 음료 (한국어 메뉴 유무 확인 — 公式へ依頼)
- 복장 규정 (드레스 코드)

### Section 6: FAQ (韓国人客特有の 7 問)
- Q1: 한국어 스태프가 상주합니까?
- Q2: 한국 원화 (KRW) 결제 가능합니까?
- Q3: KakaoTalk 으로 예약할 수 있습니까?
- Q4: 당일 취소 정책은?
- Q5: 한국 PGA 회원증 사용 가능합니까?
- Q6: 후쿠오카 공항에서 코스까지 셔틀이 있습니까?
- Q7: 그린피에 카트비 포함입니까?

### Section 7: 신뢰의 근거 (E-E-A-T)
- 제 3 자 가이드 (fukuoka-golf-guide.com) 의 독립적 검증
- 2026-05-06 35 코스 다국어 대응 조사 결과 (Tier 1 인정)
- 편집부 추천 이유

### Section 8: 최종 CTA
- 큰 버튼: 「[공식 한국어 페이지에서 예약 →]」(/ko-index)
- 보조: 「[전화 +81-949-54-0595]」(tap-to-call)
- 보조: 「[후쿠오카 다른 골프장 비교 →]」(内部リンク・hub-international 또는 sitemap-guide.html)

### Footer 共通
- breadcrumb / hreflang (ja, en, ko) / OGP

---

## 6. CTA 戦略 (優先順位)

| 優先 | CTA | 目的 | 実装 |
|------|-----|------|------|
| 1 | 公式 KO ページ (/ko-index) | 差別化の核心・信頼ある体験 | external link・rel="noopener" |
| 2 | 電話 +81-949-54-0595 | 韓国携帯から直接予約 | tel: link (모바일) |
| 3 | アフィリ (jalan/rakuten) | 副的・KO 対応不明確 | 「예약 사이트 (자동번역)」と明示 |
| 4 | (将来) GolfStay / GoGolfNippon | KO 専門 ASP 承認後に CTA 完全置換 | Phase C 完了後 |

---

## 7. JSON-LD / SEO 詳細

```jsonld
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "후쿠오카 와카미야 골프 리조트 - 공식 한국어 페이지로 예약",
  "inLanguage": "ko",
  "author": {"@type":"Organization","name":"fukuoka-golf-guide.com 편집부"},
  "datePublished": "2026-06-XX",
  "about": {"@type":"GolfCourse","name":"TRIAL GOLF & RESORT WAKAMIYA COURSE","address":"福岡県宮若市乙野 1121"}
}
```

- `<link rel="canonical" href="https://fukuoka-golf-guide.com/book-wakamiya-ko.html">`
- `<link rel="alternate" hreflang="ko" href="..." />` (ja, en も同様)
- `<meta property="og:locale" content="ko_KR">`
- BreadcrumbList / FAQPage schema 併記

---

## 8. 実装工数見積 (Day 28 GO 時)

| 作業 | 工数 |
|------|------|
| KO ライティング (ネイティブ翻訳者監修推奨・必要なら ChatGPT 草稿+人間レビュー) | 2.5h |
| HTML 構造実装 (course-*.html テンプレ流用 + KO 専用カスタマイズ) | 1h |
| 写真選定・配置 (公式から許諾済みのみ・images/wakamiya-*.webp) | 0.5h |
| JSON-LD 3 種 / hreflang / canonical / OGP | 0.5h |
| sitemap.xml + sitemap-guide.html (3 言語) 追加 | 0.1h |
| 内部リンク (index, hub-traveler, book-fukuoka-golf-foreigner から流入経路) | 0.3h |
| QA (Korea VPN・Naver SEO チェック) | 0.5h |
| **合計** | **約 5h** |

---

## 9. 公開後 KPI (Day 60 = 公開 1 ヶ月後)

| 指標 | 目標 | 判定 |
|------|------|------|
| LP KO セッション | ≥ 50 / 月 | 達成 → 継続強化 / 未達 → 韓国 SNS プロモーション併用 |
| Naver / Google JP「와카미야 골프 한국어」順位 | ≤ 10 位 | 達成 → 上位独占維持 / 未達 → 被リンク獲得策 |
| LP → 公式 /ko-index CTR | ≥ 25% | 達成 → 差別化機能・継続 / 未達 → CTA UI 改善 |
| LP → アフィリ click CVR | ≥ 3% | 達成 → 副チャネル健全 / 未達 → KO 客は公式直予約志向と判断 |

---

## 10. リスクと対応

| リスク | 内容 | 対応 |
|------|------|------|
| 翻訳品質 | ネイティブ翻訳者監修ないと差別化の意味が消える | ChatGPT 草稿 → KakaoTalk 韓国人友人レビュー or Lancers で 1-2 万円のネイティブ校正発注 |
| 公式 KO ページの寿命 | wakamiya 側が将来 KO ページ削除 → LP 意義消失 | 3 ヶ月毎の生死確認 (NEXT_SESSION.md に記載) |
| アフィリ整合性 | KO ユーザーをじゃらん/楽天に流すと混乱 | 「예약 사이트 (한국어 자동번역)」と明示・公式 KO を最優先 CTA |
| 観測ノイズ | HTML 追加でサイトトラフィック分布変化 | **観測終了後 (Day 28+) に追加** (本設計書の前提) |
| Naver SEO | 日本国外サイトは Naver で評価されにくい | hreflang ko + 韓国旅行ブログへのアウトリーチで被リンク獲得 |

---

## 11. 観測中の準備タスク (Day 28 までにユーザーが実行可能)

| タスク | 工数 | 担当 |
|------|------|------|
| KO ライティング草稿 (ChatGPT GPT-4 で生成) | 30 分 | Claude Code (依頼受け次第) |
| ネイティブ校正の発注先選定 (Lancers/Crowdworks) | 30 分 | ユーザー |
| 公式 KO ページ写真使用許諾の問合せ | 30 分 | ユーザー (公式に問合せ) |
| Naver Cafe / Naver Blog のリンク先候補リスト | 1h | Claude Code (KO アウトリーチ計画として別タスク化可能) |

---

## 12. NEXT_SESSION.md 申し送り

Day 28 後の判断:
- KO セッション > 月 50 + LP 設計書 (本ファイル) 採用 → **5h で実装**
- KO セッション < 月 20 → 実装見送り・本ファイルは保留 (再評価は次年度)

定期確認:
- 3 ヶ月毎に wakamiya 公式 /ko-index の生存確認 (LP の前提が崩れないかチェック)

---

**作成完了**。Day 28 観測終了後に再起動可能な完成度で待機状態。
