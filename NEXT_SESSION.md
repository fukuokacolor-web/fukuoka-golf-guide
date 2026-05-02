# 🎯 次セッション 引き継ぎ指示書

**作成日**: 2026-05-02
**最終 commit**: `5eaa266` (Phase B Jalan/Rakuten JP-only マーカー)

---

## 📊 サイト全体の現状

| 項目 | 値 |
|------|------|
| ドメイン | https://fukuoka-golf-guide.com (本番運用中) |
| GA4 ID | `G-PENH0Z4VT7` (絶対変更禁止) |
| 総コース数 | **35** (5エリア完全網羅) |
| 総HTMLページ | 89+ (course×35, access×35, area×5, hub×4, index, +α) |
| 言語 | 日本語/English/한국어 (3言語) |
| sitemap.xml | 93 URLs |
| GitHub | fukuokacolor-web/fukuoka-golf-guide (main ブランチ運用) |

---

## ✅ 直近の実装履歴 (新しい順)

1. **Phase B 完了** (`5eaa266`) — Jalan/楽天ボタンの EN/KO に🇯🇵(JP site) マーカー
2. **Phase A 完了** (`5f0888c`) — EN/KO セクション冒頭に「Japanese only」警告バナー
3. **index.html Pillar Page 化** (`a77b432`) — 1187→2831行・FAQ schema・Top Rankings・3-Step
4. **4ペルソナハブ作成** (`e13c6b4`) — beginner/traveler/business/budget
5. **6 access ページ作成** (`7c6d1e2`) — 新規6コース分
6. **エリアガイド整合性更新** (`b078d01`) — 新規6コースを各エリアガイドに統合
7. **Step 2: 3コース追加** (`123ccd9`) — 玄海GC・鷹羽ロイヤル・福岡フェザント
8. **Step 1: 3コース追加** (`668a81d`) — 福岡国際CC・若松GC・浮羽CC
9. **芥屋GC料金修正** (`3c77ef4`) — ¥8,000→¥21,500〜の正確値へ
10. **福岡CC料金修正** (`42eea4c`) — 会員制クラブとして正規化
11. **CVR Phase 1 Week 1** (`58194ff`) — FV CTA strip 全29コース
12. **ドメイン移行** (`2ea3cfe` 周辺) — github.io → fukuoka-golf-guide.com

---

## 🚧 進行中: インバウンド改善 (Phase A→B→C)

### ✅ Phase A (完了)
EN/KO 各セクション冒頭に「⚠️ Japanese booking sites require JP phone/card」バナー追加

### ✅ Phase B (完了)
Jalan/楽天ボタンに `🇯🇵 (JP site)` インラインマーカー追加(42ファイル)

### 🔴 Phase C (未着手 — 次セッションで実行)

**ユーザー側作業 (ASP申請)**:
1. **GolfStay** (https://www.golfstay.jp/) — KO/EN/中対応・福岡30+カバー
   - 「お問い合わせ」から「アフィリエイト希望」連絡
   - 報酬 5-8%・申請1-2週間
2. **GoGolfNippon** (https://gogolfnippon.com/) — 米欧専門
   - B2B個別契約 (¥5,000-10,000/件)
3. **KKDay** (https://affiliate.kkday.com/) — 将来・台湾向け

**サイト側作業 (Claude Code が実行)**:
1. ASP承認後、EN/KO の Jalan/楽天 を **完全置換** (GolfStay/GoGolfNippon へ)
2. **「How to book Fukuoka golf as a foreigner」記事** 新規作成 (EN/KO ・ ゼロ競合SEO枠)
3. **「英語/韓国語予約可能コース」フィルター** 機能実装
4. **hub-international.html** 新設検討 (4→5ペルソナハブに昇格)

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
- ハルシネーションされた架空コース掲載は厳禁 (前回 8コース中6コース架空だった事故あり)
- 数値の誤りは即修正(芥屋¥8,000→¥21,500、福岡CC会員制扱いなど)

---

## 🛠 重要ファイル・スクリプト

### スクリプト (`scripts/` 配下)
- `update_canonical.py` — 全HTMLにcanonicalタグ正規化
- `update_ogp.py` — og:url/og:image 正規化
- `generate_sitemap.py` — sitemap.xml再生成 (priority 0.9維持)
- `add_ftv_cta.py` — FV CTA strip 一括挿入
- `add_intl_notice.py` — Phase A: 国際通知バナー挿入
- `mark_jalan_jp_only.py` — Phase B: Jalan/楽天 ボタンマーカー

### 参照ドキュメント
- `claude-code-domain-migration.md` — ドメイン移行の完全ランブック (v2.2)

### 引き継ぎメモ
- `C:\Users\Owner\Documents\新しいPJ\引き継ぎメモ.md` — 詳細な作業ログ

---

## 🚫 絶対の禁止事項

1. **GA4 タグ (`G-PENH0Z4VT7`) を絶対変更しない**
2. **CNAME ファイルを編集しない** (`fukuoka-golf-guide.com`)
3. **公式サイト確認なしでコース情報を追加しない** (ハルシネーション防止)
4. **会員制コース** (福岡CC・若松・玄海) に Jalan/楽天 CTA を載せない (公式のみ)
5. **本ドキュメント (`NEXT_SESSION.md`) を一括置換 script で書き換えない** (`fukuokacolor-web` は履歴用)

---

## 🎯 推奨される次セッションの最初の一手

**選択肢**:

### A. ASP承認待ちの間に「How to book as a foreigner」記事先行作成
- EN/KO で 1500語ずつ
- 競合ゼロのSEO金鉱
- 公開後 GolfStay 承認時に CTA を埋め込めば即収益化

### B. GA4 観測フェーズ
- 2-4週間データ蓄積
- Phase A/B の効果測定
- 次の施策をデータドリブンで決定

### C. 既存のスポーク強化
- hub-business.html 用の「接待ガイド完全版」記事
- Pillar Page から spoke への内部リンク強化

### D. ユーザー指定の別タスク

---

## 💡 セッション開始時のテンプレ質問

次セッションで Claude Code 起動時に、ユーザーが以下を貼ると効率的:

```
NEXT_SESSION.md を読んでください。
今日は [A / B / C / その他] を進めたいです。
```

または:

```
NEXT_SESSION.md を読んで、状況を把握したら、
Phase C の進捗を確認しながら、まず公式サイトの ASP承認状況を確認するところから始めてください。
```

---

## 📈 期待されるサイト成長 (田中SEO予測)

| 期間 | PV予測 | 月収益予測 |
|------|------|------|
| 現状 (2026-05) | 500-1,500 PV/月 | ¥30-60k |
| 3ヶ月後 (2026-08) | 3,000-5,000 PV/月 | ¥80-120k |
| 6ヶ月後 (2026-11) | **8,000-15,000 PV/月** | **¥150-220k** |
| 月¥30万到達時期 | 8-10ヶ月 (2026-12〜2027-02) |

**EN/KO 改善後の追加効果**:
- インバウンド客単価¥30-50k×CVR向上で **月+¥30-80k** 上乗せ可能性

---

**Good luck for the next session!** 🌟

ご不明な点があれば、各ファイル冒頭のコメントや過去のcommit messageを参照してください。
