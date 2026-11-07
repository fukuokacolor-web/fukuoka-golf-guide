#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
午後スルーの記述を、プラン名の確認結果に合わせて直す。

841ab79 で area-fukuokacity に「久山に午後スルーなし」と書いたのは誤り。プラン名の検索が「午後スルー」の文字だけで、
久山の「PMスルー」(土日祝) を見落としていた。

じゃらん 11/2〜11/15 (14日間) のプラン名に午後スルー (午後スルー・午後1Rスルー・PMスルー) があったコース:
  レイクサイド 平日8日/土日祝2日・北九州CC 平日8日・チサン遠賀 平日7日/土日祝1日・皐月竜王 平日2日/土日祝1日・久山 土日祝2日
  ※大博多・フェザント・浮羽はなし。あかねはじゃらん枠なし
index.html の FAQ「フェザント・あかね・浮羽・大博多でよく実施」「午後スルーフィルター」と大博多の「午後スルー対応」は根拠なし。
出典: scripts/.cache/jalan_{gc}_202611*.html (checked 2026-11-01)
冪等: 置換元が無く置換後がある場合は already。
Usage:
  python scripts/fix_thru_correction_2026_11.py            # dry-run
  python scripts/fix_thru_correction_2026_11.py --preview  # PREVIEW だけ (index は fix_index_2026_11.py --preview の後に)
  python scripts/fix_thru_correction_2026_11.py --apply    # REPO + PREVIEW
"""
import os, sys

REPO_ROOT = "C:/Users/Owner/fukuoka-golf-guide"
PREVIEW_ROOT = "C:/Users/Owner/Documents/新しいPJ"
APPLY = "--apply" in sys.argv or "--preview" in sys.argv
ROOTS = [PREVIEW_ROOT] if "--preview" in sys.argv else [REPO_ROOT, PREVIEW_ROOT]
A = '<a href="course-{}.html">{}</a>'

# {ファイル: [(旧, 新, 出現回数)]}
FILES = {
    "area-fukuokacity.html": [
        ('ただし2026年11月前半のじゃらんでは、久山・大博多・セブンミリオン・筑紫ヶ丘に午後スルーのプランはありませんでした。',
         'ただし2026年11月前半のじゃらんでは、午後スルーは久山の土日祝（2日）だけで、大博多・セブンミリオン・筑紫ヶ丘にはありませんでした。', 1),
        ('2026年11月前半のじゃらんでは久山・大博多・セブンミリオン・筑紫ヶ丘に午後スルーのプランはありませんでした。',
         '2026年11月前半のじゃらんでは久山の土日祝（2日）だけで、大博多・セブンミリオン・筑紫ヶ丘にはありませんでした。', 1),
        ('In the first half of November 2026, though, Jalan listed no afternoon-thru plans at Hisayama, Dai-Hakata, Seven Million or Chikushigaoka.',
         'In the first half of November 2026, though, Jalan listed afternoon-thru plans only at Hisayama, on 2 weekend days, and none at Dai-Hakata, Seven Million or Chikushigaoka.', 1),
        ('In the first half of November 2026, Jalan listed none at Hisayama, Dai-Hakata, Seven Million or Chikushigaoka.',
         'In the first half of November 2026, Jalan listed them only at Hisayama, on 2 weekend days, and none at Dai-Hakata, Seven Million or Chikushigaoka.', 1),
        ('다만 2026년 11월 전반 자란에서는 히사야마·다이하카타·세븐밀리언·지쿠시가오카에 오후 스루 플랜이 없었습니다.',
         '다만 2026년 11월 전반 자란에서 오후 스루는 히사야마의 주말(2일)뿐이었고, 다이하카타·세븐밀리언·지쿠시가오카에는 없었습니다.', 1),
        ('2026년 11월 전반 자란에서는 히사야마·다이하카타·세븐밀리언·지쿠시가오카에 오후 스루 플랜이 없었습니다.',
         '2026년 11월 전반 자란에서는 히사야마의 주말(2일)뿐이었고, 다이하카타·세븐밀리언·지쿠시가오카에는 없었습니다.', 1),
    ],
    "index.html": [
        ('"text": "午後スルー(ハーフ後にそのまま続けて18Hプレー)は、平日のフェザントCC・あかねCC・浮羽CC・大博多CCなどでよく実施されます。半日プレーで済むので出張・弾丸ゴルフに最適。予約サイト(じゃらんゴルフ・楽天GORA)で「午後スルー」フィルターを使うと探しやすいです。"',
         '"text": "じゃらんの2026年11月2日〜15日のプランで午後スルーを確認できたのは、平日が福岡レイクサイドCC・北九州CC（各8日）、チサン遠賀CC（7日）、皐月GC 竜王コース（2日）、土日祝のみが久山CC（2日）でした。設定はコースと時期で変わるので、予約サイトで最新をご確認ください。"', 1),
        ('<div class="faq-a">午後スルー(ハーフ後そのまま18Hプレー)は、平日の' + A.format("pheasant", "フェザントCC") + '・' + A.format("akane", "あかねCC") + '・' + A.format("ukiha", "浮羽CC") + '・' + A.format("daihakata", "大博多CC") + 'などでよく実施。半日プレーで済むので出張・弾丸ゴルフに最適。予約サイト(じゃらんゴルフ・楽天GORA)で「午後スルー」フィルターを使うと探しやすいです。',
         '<div class="faq-a">じゃらんの2026年11月2日〜15日のプランで午後スルーを確認できたのは、平日が' + A.format("lakeside", "福岡レイクサイドCC") + '・' + A.format("kitakyushu", "北九州CC") + '（各8日）、' + A.format("chisan-onga", "チサン遠賀CC") + '（7日）、' + A.format("satsuki-ryuoh", "皐月GC 竜王コース") + '（2日）、土日祝のみが' + A.format("hisayama", "久山CC") + '（2日）でした。設定はコースと時期で変わるので、予約サイトで最新をご確認ください。', 1),
        ('<div class="faq-a">Afternoon-Through (continuing 18H without a break) is common on weekdays at ' + A.format("pheasant", "Pheasant CC") + ', ' + A.format("akane", "Akane CC") + ', ' + A.format("ukiha", "Ukiha CC") + ', and ' + A.format("daihakata", "Dai-Hakata CC") + '. Rounds finish in half a day — ideal for business trips. Filter "Afternoon Through" on Jalan or GORA.',
         '<div class="faq-a">On Jalan for Nov 2–15, 2026, Afternoon-Through plans appeared on weekdays at ' + A.format("lakeside", "Fukuoka Lakeside CC") + ' and ' + A.format("kitakyushu", "Kitakyushu CC") + ' (8 days each), ' + A.format("chisan-onga", "Chisan Onga CC") + ' (7 days) and ' + A.format("satsuki-ryuoh", "Satsuki GC Ryuoh Course") + ' (2 days), and on weekends only at ' + A.format("hisayama", "Hisayama CC") + ' (2 days). Availability changes by course and season, so check the booking site.', 1),
        ('<div class="faq-a">오후 스루(하프 후 그대로 18H 플레이)는 평일의 ' + A.format("pheasant", "페전트 CC") + '·' + A.format("akane", "아카네 CC") + '·' + A.format("ukiha", "우키하 CC") + '·' + A.format("daihakata", "다이하카타 CC") + ' 등에서 자주 실시. 반나절 플레이로 끝나기 때문에 출장·당일치기 골프에 최적. 예약 사이트(자란 골프·라쿠텐 GORA)에서 "오후 스루" 필터를 사용하면 찾기 쉽습니다.',
         '<div class="faq-a">자란의 2026년 11월 2일〜15일 플랜에서 오후 스루를 확인한 곳은 평일 ' + A.format("lakeside", "후쿠오카 레이크사이드 CC") + '·' + A.format("kitakyushu", "기타큐슈 CC") + '(각 8일), ' + A.format("chisan-onga", "치산 온가 CC") + '(7일), ' + A.format("satsuki-ryuoh", "사쓰키 GC 류오 코스") + '(2일), 주말만 ' + A.format("hisayama", "히사야마 CC") + '(2일)였습니다. 설정은 코스와 시기에 따라 다르니 예약 사이트에서 확인하세요.', 1),
        ('<div class="rank-meta">JR送迎可・午後スルー対応・出張に強い</div>', '<div class="rank-meta">JR送迎可・出張に強い</div>', 1),
        ('<div class="rank-meta">JR shuttle · Afternoon-thru friendly</div>', '<div class="rank-meta">JR shuttle · Good for business trips</div>', 1),
        ('<div class="rank-meta">JR 셔틀 가능 · 오후 스루 대응 · 출장에 강함</div>', '<div class="rank-meta">JR 셔틀 가능 · 출장에 강함</div>', 1),
    ],
}


def main():
    for name, reps in FILES.items():
        # index.html は fix_index_2026_11.py の後に当てる。--preview では PREVIEW の版を土台にする
        base = PREVIEW_ROOT if "--preview" in sys.argv else REPO_ROOT
        src = open(os.path.join(base, name), encoding="utf-8", newline="").read()
        t = src
        c = {"replaced": 0, "already": 0}
        for old, new, n in reps:
            k = t.count(old)
            if k == n:
                t = t.replace(old, new); c["replaced"] += 1
            elif k == 0 and t.count(new) >= n:
                c["already"] += 1
            else:
                raise SystemExit(f"NO_MATCH {name} ({k}/{n}): {old[:70]}")
        print(name, c, "変更あり" if t != src else "変更なし")
        if APPLY and t != src:
            for root in ROOTS:
                open(os.path.join(root, name), "w", encoding="utf-8", newline="").write(t)
    print("APPLIED " + ",".join(r[-12:] for r in ROOTS) if APPLY else "DRY-RUN")


if __name__ == "__main__":
    main()
