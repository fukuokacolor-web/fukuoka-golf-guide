# 🎯 次セッション 引き継ぎ指示書

**最終更新**: 2026-05-03 (2回目)
**最終 commit**: `c6a6436` (3コンテンツ修正 aburayama/kokura/genkai)
**前回 commit**: `82332dc` (Deep link 楽天GORA), `dc53ebc` (NEXT_SESSION update)

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

1. **🆕 3コンテンツ修正完了** (`c6a6436` / 2026-05-03)
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

## 🚫 アフィリCTA 除外コース 4件（厳守）

**ファクトチェック2エージェント並列クロスチェック確定（2026-05-03）**

| コース | 理由 | 状態 |
|--------|------|------|
| **course-fukuokacc** | 会員制（メンバー同伴/紹介必須）・GORAプラン非掲載 | 既にCTAなし ✓ |
| **course-wakamatsu** | 会員制・GORA予約不可 | 既にCTAなし ✓ |
| **course-akane** | 楽天GORA未掲載（あかねCC） | CTA削除済 ✓ |
| **course-genkai** | 2023/1〜長期クローズ表示中 (※ 要追跡) | CTA削除済 ✓ |

**※ 注意**：以前 NEXT_SESSION.md に「福岡CC・若松・玄海」と書いていたが、**小倉CCは株主会員制でビジター枠あり**（土日¥19,014公表）のため CTA 維持。誤記訂正済。

---

## 📝 未完了タスク（優先順）

### 🔴 高優先：aburayama 旧名の他ファイル更新（IA推奨：新旧併記6ヶ月）
3ファイル修正 (`c6a6436`) で course-aburayama.html 本体は完了。残り：
- [ ] `access-aburayama.html` (28箇所) — タイトル/H1のみララヒルズに変更、本文は旧名併記
- [ ] `area-fukuokacity.html` (2箇所) — エリアガイド内のコース名表記
- [ ] `hub-beginner.html` (2箇所) — 初心者ハブのコース名
- [ ] `recommend.html` (1箇所) — レコメンド記事のコース名
- [ ] `index.html` — トップページにあれば
- [ ] `sitemap-guide.html` — サイトマップガイド表記

### ✅ 完了済 (2026-05-03 2回目)
- ~~course-genkai.html notice バナー追加~~ → 完了 (営業中・公式/GDO誘導)
- ~~course-aburayama.html ララヒルズ統一~~ → 完了 (本体ファイルのみ)
- ~~course-kokura.html リブランディング+CTA~~ → 完了

### 🟡 中優先：じゃらんゴルフ Deep Link 化
- [ ] じゃらんゴルフも同様の deep link 化（楽天と並走）
- 既存じゃらんアフィリ：`a8mat=4B1D5J+5JG8FM+36SI+BW8O2` (フリーリンクコード判明済)
- URL形式：`https://golf-jalan.net/gc{ID}/` または `https://golf.jalan.net/golf/courseDetail/{ID}/`
- **未取得の jalan c_id**：35コース分の収集スクリプト or Webfetch 必要

### 🟡 中優先：Phase C インバウンド改善
**ユーザー側作業 (ASP申請)**:
1. **GolfStay** (https://www.golfstay.jp/) — KO/EN/中対応・福岡30+カバー
   - 「お問い合わせ」から「アフィリエイト希望」連絡
   - 報酬 5-8%・申請1-2週間
2. **GoGolfNippon** (https://gogolfnippon.com/) — 米欧専門
3. **KKDay** (https://affiliate.kkday.com/) — 将来・台湾向け

**サイト側作業 (Claude Code が実行)**:
1. ASP承認後、EN/KO の Jalan/楽天 を **完全置換** (GolfStay/GoGolfNippon へ)
2. **「How to book Fukuoka golf as a foreigner」記事** 新規作成 (EN/KO ・ ゼロ競合SEO枠)
3. **「英語/韓国語予約可能コース」フィルター** 機能実装
4. **hub-international.html** 新設検討 (4→5ペルソナハブに昇格)

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
