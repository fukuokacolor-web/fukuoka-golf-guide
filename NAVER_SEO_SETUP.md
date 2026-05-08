# Naver SEO セットアップ手順書 (ユーザー作業ガイド)

**作成日**: 2026-05-06
**目的**: 韓国 Naver 検索での SEO を強化するための土台 (Naver Search Advisor 認証 + sitemap 提出) を整える
**ユーザー側作業**: 累計 30-40 分 (アカウント作成 + サイト登録 + 認証 ID 取得・送信のみ)
**Claude 側作業**: 認証 ID 受領後・全 HTML への meta 挿入 (10 分)

---

## なぜ Naver Search Advisor が必要か

Naver は韓国国内検索の **70%+ シェア**。Google ではなく Naver で評価されるためには:
1. Naver Search Advisor (https://searchadvisor.naver.com) にサイト登録
2. 認証メタタグ追加で「サイト所有者」を証明
3. sitemap.xml を提出

これがないと、韓国 Naver での評価が始まらず、wakamiya KO LP (Day 28 後実装予定) も韓国検索で見つかりにくい。

---

## ユーザー側手順 (累計 30-40 分)

### Step 1: Naver アカウント取得 (10 分・既にあればスキップ)
1. https://www.naver.com/ にアクセス
2. 右上「회원가입」(会員登録)
3. 実名 + 韓国携帯 or メール
4. ⚠️ **海外ユーザーは認証が複雑**: LINE 認証 / SMS 認証 / 韓国知人の協力が必要な場合あり
5. もし日本から登録困難なら: **Bing Webmaster Tools** で代替する手も (Naver より弱いが日本から登録可能)

### Step 2: Naver Search Advisor サイト登録 (5 分)
1. https://searchadvisor.naver.com にアクセス
2. ログイン
3. 「웹마스터 도구」 → 「사이트 등록」 (サイト登録)
4. URL 入力: `https://fukuoka-golf-guide.com`
5. 「추가」 (追加) ボタン

### Step 3: 認証 ID 取得 (5 分)
1. 認証方法選択画面で **「HTML 태그」** を選ぶ (おすすめ・recommended)
2. 提示される メタタグをコピー (例):
   ```html
   <meta name="naver-site-verification" content="abc123def456..." />
   ```
3. **`content="..."` の値だけ Claude に伝える**
4. Claude が全 HTML ファイルに挿入する `scripts/inject_naver_meta.py` を実行 (受領後 10 分で完了)
5. ユーザーが Search Advisor 画面に戻り「확인」ボタンを押すと認証完了 (本番反映後 = git push 後)

### Step 4: sitemap 提出 (5 分・認証完了後)
1. Search Advisor → 「sitemap 제출」(sitemap 提出)
2. URL: `https://fukuoka-golf-guide.com/sitemap.xml`
3. 同じく `https://fukuoka-golf-guide.com/sitemap-ko.xml` (Claude が作成済) も提出
4. 「상태」(状態) が「검증 완료」(検証完了) になれば OK

### Step 5: 確認 (5 分・Day 7+ で実施)
- 「검색 노출」(検索露出) ダッシュボードで索引化確認
- 主要 KW (例: 「후쿠오카 골프 한국어」) で順位確認 (反映に 2-4 週間)

---

## Claude 側の事前準備 (本日完了)

| 成果物 | 内容 | 状態 |
|------|------|------|
| 全 HTML に `og:locale="ja_JP"` 追加 | OGP 言語明示 | 本日 commit |
| `sitemap-ko.xml` 生成スクリプト | KO 関連 URL のみ抽出 | 本日 commit |
| `robots.txt` に sitemap-ko.xml 追記 | 検索エンジンが認識 | 本日 commit |
| `scripts/inject_naver_meta.py` (placeholder) | 認証 ID 受領後実行 | 本日 commit |

---

## 全体スケジュール

| Day | やること | 担当 |
|-----|---------|------|
| **Day 0 (今日)** | og:locale + sitemap-ko.xml + robots.txt 更新 | Claude (完了予定) |
| **Day 0 or 1** | Step 1-3: Naver 登録 + 認証 ID 取得 | ユーザー (30 分) |
| **Day 1** | 認証 ID を Claude に通知 → 全 HTML に挿入 → push | Claude + ユーザー (15 分) |
| **Day 2-3** | Naver crawl → 認証完了 | (待機) |
| **Day 4** | sitemap 提出 (Step 4) | ユーザー (5 分) |
| **Day 7-30** | Naver 索引化開始 | (待機) |
| **Day 30+** | 韓国検索順位データ蓄積 → Day 28 観測判断と統合 | (Claude 分析) |

---

## 補足: Bing Webmaster Tools (Plan B・Naver 登録困難時)

もし Naver アカウント取得が難しい場合の代替策:
- https://www.bing.com/webmasters
- Bing は Yahoo Korea にも反映される (Naver ほどではないが補完的)
- 認証メタタグ方式 + sitemap 提出 (Naver と同じ手順)
- ユーザー側作業: 5-10 分 (Microsoft アカウントで登録可能)

両方やっても所要時間は累計 1 時間以内。

---

## 補足: Google Search Console (Japan) も併用

すでに登録済の場合はスキップ。未登録なら:
- https://search.google.com/search-console
- KO 関連クエリの順位確認には GSC が最強 (`GSC_CANNIBALIZATION_GUIDE.md` 参照)
- 認証メタタグ方式・5 分で完了

---

## ⚠️ 注意事項

- **Naver は外部日本サイトの評価が低め**: 即効性は低いが、長期的な KO 流入チャネル拡大に必須
- **韓国 IP からのアクセス・韓国語コンテンツ・hreflang ko の整合性**が必要 (本日対応済)
- **wakamiya KO LP 公開後に効果が出やすい**: Tier 1 LP → Tier 1 単独 SEO の流れ

---

## 次のステップ (Claude が今すぐやる)

1. `scripts/inject_og_locale.py` で全 HTML に `og:locale="ja_JP"` 追加
2. `scripts/generate_sitemap_ko.py` で `sitemap-ko.xml` 生成
3. `robots.txt` に sitemap-ko.xml の参照を追記
4. すべて両ディレクトリ同期 + commit
5. ユーザーが Naver 認証 ID 取得した後、`scripts/inject_naver_meta.py` で全 HTML に挿入

**ユーザーは Step 1-3 (Naver 登録 + 認証 ID 取得) を今すぐ着手して OK**。Claude 側準備は本セッション内に完了します。
