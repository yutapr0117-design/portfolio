#!/usr/bin/env python3
"""mutation_samples.py — Curated mutation DATA for mutation_probe.py (runner is separate).

mutation_probe.py (runner / completeness-critic) から**データのみ**を分離した葉モジュール。
肥大化解消 (自走効率 + 保守性): runner ロジックと curated mutation データを分ける。さらに
データ自体も log-rotation 方式で分割した (1000 行しきい値対応):

- MUTATIONS_ARCHIVE  : mutation_samples_archive.py (最古 / rotated part 1)。
- MUTATIONS_ARCHIVE2 : mutation_samples_archive2.py (次に古い / rotated part 2, 2026-07-28 新設)。
- 本ファイル tail    : 新しい側の entries (新規追記は常に本ファイルの MUTATIONS 末尾へ)。
- MUTATIONS          : ARCHIVE + ARCHIVE2 + tail の連結 (mutation_probe が import する公開 API・不変)。
- E2E_MUTATIONS      : behavior e2e 安全網用 (--e2e モード)。

【追記規約 (生じないように / 恒久)】新規 mutation は本ファイルの MUTATIONS 末尾 (tail) に追記する。
本ファイルが ~900 行を超えたら、最古の tail entries を最新の archive part へ移して rotate する。
part 1/2 が Check 365 の 1,000 cap に近接したら part をさらに増やす (mutation_samples_archive3.py 等)。

各 mutation の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring を参照。
本ファイルはデータ (dict の list) のみで、副作用も実行ロジックも持たない。
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    print("ERROR: mutation_samples.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

from mutation_samples_common import ROOT, CHECK  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
from mutation_samples_archive3 import MUTATIONS_ARCHIVE3
from mutation_samples_archive2 import MUTATIONS_ARCHIVE2
from mutation_samples_e2e_archive import E2E_MUTATIONS_ARCHIVE
from mutation_samples_e2e_archive3 import E2E_MUTATIONS_ARCHIVE3
from mutation_samples_e2e_archive2 import E2E_MUTATIONS_ARCHIVE2

# 新しい側の curated mutation (新規追記は本リスト末尾へ / 上記「追記規約」参照)。
_MUTATIONS_TAIL = [
    # 注: Check 362 (mutation anchor resolution) の curated meta-mutation は敢えて置かない。
    # anchor を orphan 化する mutation は mutation_samples.py 自身の `"find":` 行を quote する
    # 自己参照になり、mutation_probe の replace(find, replace, 1) が先頭 (= その mutation 自身の
    # find 値) に当たって挙動が不安定になるため。Check 362 の非 vacuous 性は手動で実証済
    # (mutation の file を誤り先へ変えると Check 362 が RED・restore で緑)。
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。










# ── Check 441 (ACD-1.0 ライセンス本文の構造整合と配線) ──────────────────────────
# NOTE: **Check 442 (binary metadata の到達可能性) には mutation を登録できない。**
#   mutation_probe は対象 file を `read_text(encoding="utf-8")` で読むので、WebP / MP3 は
#   UnicodeDecodeError になり適用そのものが成立しない。非 vacuity は 2026-08-23 に手動で
#   実測済 (COMM の size を過大値へ戻す → 442a/442b が RED / RIFF size を 1 ずらす → 442c が RED)。
#   RED を実測できない mutation を安全網に混ぜないための非登録であって、被覆漏れではない。











_MUTATIONS_TAIL.append({
    "name": "Check 448 (Agent Skills 仕様適合): 必須 field `description` を落とす —— 仕様の設計は "
            "「agent は起動時に name と description だけを読んで関連性を判断する」progressive "
            "disclosure なので、欠けると **agent は中身を取ってみるまで用途が判らない**。"
            "2026-08-23 まで実際に全 entry で欠落しており、宣言した $schema で検証する agent は "
            "index ごと拒否していた",
    "file": ROOT / ".well-known" / "agent-skills" / "index.json",
    "find": '"description": "Read the authoritative machine-readable context',
    "replace": '"_description_removed_by_probe": "Read the authoritative machine-readable context',
})

_MUTATIONS_TAIL.append({
    "name": "Check 449a (RFC 9727 関係型): カタログのメンバーを `item` ではなく `api-catalog` "
            "関係で列挙する —— RFC 9727 でこの関係は「**別の API カタログへの入れ子**」を意味する "
            "ので、`llms-full.txt` などカタログでないリソースを「これらは全てカタログだ」と偽って "
            "宣言することになり、**仕様に従う agent はそれらを linkset として parse しようとして "
            "失敗する**。2026-08-23 まで実際に 7 件すべてがこの状態で、Check 165 は JSON 構造と "
            "anchor しか見ないため検出層が存在しなかった",
    "file": ROOT / ".well-known" / "api-catalog",
    "find": '"item": [',
    "replace": '"api-catalog": [',
})

_MUTATIONS_TAIL.append({
    "name": "Check 450 (非日本語スクリプト混入): 規範層の「権威テキスト」前半 3 字をキリル文字へ "
            "戻す —— 字形が近いため目視では気付けず、spell-check は走らず lint は JS しか読まず "
            "prose は何とも比較されないので **どの層も検出しない**。2026-08-23 まで実際に規範層 "
            "(C6 を説明する行) と decision record の 2 箇所に残存していた",
    "file": ROOT / "docs" / "architecture" / "repository-maintainability-map.md",
    "find": "\u6a29\u5a01\u30c6\u30ad\u30b9\u30c8",
    "replace": "\u6a29\u5a01\u0442\u0435\u043a\u30b9\u30c8",
})

_MUTATIONS_TAIL.append({
    "name": "Check 436 (裁可待ち文言・scope + 綴り拡張): agent 定義の pre-edit checklist を "
            "「承認が記録されていなければ REFUSE」へ戻す —— `.claude/agents/` は**エージェントの "
            "挙動を実際に駆動する層**で、ここに承認ゲートがあると AIO 編集を通すたびに canon が "
            "存在しないと明記した「裁可待ち」を再生産する。旧 scope は `.claude/` を一度も見て "
            "おらず、しかも照合が case-sensitive だったため先頭大文字の実在文言を素通りしていた",
    "file": ROOT / ".claude" / "agents" / "aio-guardian.md",
    "find": "1. **Is every claim true and non-fabricated?**",
    "replace": "1. **Orchestrator approval recorded?** If not, REFUSE.",
})

_MUTATIONS_TAIL.append({
    "name": "Check 436 (mirror 面 scope): docs/files/ mirror の C6 記述を承認ゲート型へ戻す —— "
            "mirror doc は「この file を編集するとき何を満たすか」を述べる規範面として読まれる。"
            "2026-08-23 に手作業で 9 枚を掃引したが **綴りを 3 つ見落として 4 枚が残った** ゆえ、"
            "per-instance では閉じない class として構造封じへ昇華した",
    "file": ROOT / "docs" / "files" / "llms-full.txt.md",
    "find": "semantic \u7de8\u96c6\u306f C6 \u306e 3 \u4e0d\u5909\u6761\u4ef6",
    "replace": "semantic \u7de8\u96c6\u306f orchestrator \u660e\u793a\u627f\u8a8d\u5fc5\u9808",
})

_MUTATIONS_TAIL.append({
    "name": "Check 454 (危険域 file の予算登録): BUDGET-DATA から check_repository_consistency.py の "
            "登録行を除去 → その file は Check 52 の advisory 対象から外れ、**早期警告が一度も出ないまま** "
            "Check 365 の 1,000 行 BLOCKING へ飛ぶ状態へ戻る。導入時に実在の未登録 5 file を検出した "
            "class の回帰防止 (帰属実測済: 発火するのは 454 のみ。52/59/365 は緑のまま —— "
            "エラー本文中の参照を grep が拾って 4 件と誤読しかけたので、先頭の Check 番号で帰属し直した)。"
            "\n\n    NOTE: **この mutation の前提はデータ条件** (対象 file が >800 行であること) である。"
            "対象を分割・圧縮すると Check 454 が対象外と判断し、mutation は **silent に vacuous 化する**。"
            "実際 2026-08-26 に checks_behavioral.py (924 → 589 行) を指しており、同じセッションの後続 PR で"
            "分割した結果 probe が SURVIVED を報告した。**Check 362 (anchor 解決) も 420 (一意性) も"
            "これを捕捉しない** —— anchor は解決するし一意でもあり、ただ load-bearing でなくなるだけだから。"
            "捕捉層は probe だけである。SURVIVED になったら、危険域に残っている file へ**指し直す**こと"
            "(対象は `git ls-files` で >800 行の登録済み file を数えれば分かる)。"
            "現在の対象は分割トラック完遂後の薄い dispatcher なので、これ以上縮む予定は無い",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": ".github/scripts/check_repository_consistency.py | 950 | advisory\n",
    "replace": "",
})


_MUTATIONS_TAIL.append({
    "name": "Check 455 (strong-advisory の tightness): main.js の予算を Stage 5 前の 6,400 へ戻す —— "
            "実測 1,356 に対し 4.7 倍で **advisory が永久に鳴らない**状態。main.js は Check 365 の "
            "hard ceiling 対象外ゆえ、この予算が**唯一のサイズ信号**であり、緩めた瞬間にサイズの "
            "観測手段が完全に失われる。§1 の分類表が strong-advisory に与えた定義 "
            "(「現行行数に近い tight な上限」) と実態が真逆になる drift の回帰防止 "
            "(帰属実測済: 発火するのは 455 のみ)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "\nmain.js | 1500 | strong-advisory\n",
    "replace": "\nmain.js | 6400 | strong-advisory\n",
})


_MUTATIONS_TAIL.append({
    "name": "Check 456 (__main__ ガード後の def): rotate ツールのガード直後に関数定義を足す —— "
            "ガード本体 (sys.exit(main())) はその場で実行されるので、後ろの def は"
            "**スクリプト実行時にはまだ束縛されていない**。import すると定義されるため "
            "import 経由のテストでは動くのに CLI では NameError になる非対称。実測 (2026-08-26): "
            "`_wire_new_archive` がこの位置にあり「受け皿が埋まったら次を起こす」機能が "
            "npm run rotate-mutations からは一度も動いていなかった (帰属実測済: 456 のみ発火)",
    "file": ROOT / ".github" / "scripts" / "rotate_mutation_samples.py",
    "find": "if __name__ == \"__main__\":\n    sys.exit(main())\n",
    "replace": "if __name__ == \"__main__\":\n    sys.exit(main())\n\n\ndef _unreachable_after_guard():\n    return None\n",
})


_MUTATIONS_TAIL.append({
    "name": "Check 457 (配線 ⟹ 配信面の照合): freshness tool の照合対象を index.html 由来の "
            "導出からハードコード 3 件へ戻す —— **aio-guard.js / theme-init.js / karte-init.js / "
            "error-suppressor.js が配信面で一度も検証されない**状態へ回帰する。Check 133/134/135 は "
            "リポジトリ内の配線しか見ないので、公開されているのが古い/壊れた版という失敗モードは "
            "原理的に見えない (帰属実測済: 発火するのは 457 のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "    return sorted(set(root_js) | set(root_css) | {\"sw.js\", \"index.html\"}) + sorted(",
    "replace": "    return [\"style.css\", \"main.js\", \"sw.js\"] + sorted(",
})


_MUTATIONS_TAIL.append({
    "name": "Check 457b (導出の起点の検証): 照合対象から index.html だけを外す —— "
            "版数 (ai:version / ai:last-modified) は**中身が変わっても動かない** "
            "(実測: 直近 30 日で index.html は 7 commit 変更・版数 bump は 0 件) ので、"
            "外した瞬間に **JSON-LD / CSP / meta / script 配線 / sr-only entity anchor を載せる "
            "最も影響の大きい file** が配信面で silent に古いままになりうる状態へ戻る "
            "(帰属実測済: 発火するのは 457b のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "{\"sw.js\", \"index.html\"}",
    "replace": "{\"sw.js\"}",
})


_MUTATIONS_TAIL.append({
    "name": "Check 457c (機械向け宣言面の配信検証): discovery 照合対象から .well-known/** の "
            "導出を外す —— **200 が返ることと中身が最新であることは別**で、古い robots.txt は "
            "クローラの到達範囲を変え、古い .well-known/* は agent が読む契約そのものを変え、"
            "古い aio-manifest.json は agent へ誤った digest を宣言する。しかも人間には"
            "何も見えない。実測 (2026-08-26): 導入前は discovery 層 13 件中 10 件が"
            "存在確認どまりだった (帰属実測済: 発火するのは 457c のみ)",
    "file": ROOT / ".github" / "scripts" / "check_deployed_freshness.py",
    "find": "    out = set(_wellknown_paths())",
    "replace": "    out = set()",
})


_MUTATIONS_TAIL.append({
    "name": "Check 458b (venue の誤主張): CLAUDE.md §7 の投稿先を `license-review` へ投稿済みと"
            "書き換える —— **取り違えには実害がある**。`license-discuss` は OSI の一般的な議論"
            "リストで承認申請の窓口ではないので、「申請済み」と記録すると **まだ何も申請して"
            "いない**ことに誰も気付けなくなる。2026-08-26 の 1 日で 2 度 drift した class "
            "(帰属実測済: 発火するのは 458b のみ)",
    "file": ROOT / "CLAUDE.md",
    "find": "OSI `license-discuss` へ投稿済み・結果待ち",
    "replace": "OSI `license-review` へ投稿済み・結果待ち",
})


_MUTATIONS_TAIL.append({
    "name": "Check 461: 予算ラチェットの累積記録を stale に戻す —— 個々のラチェットに理由を書いても、"
            "累積が更新されなければ「今日で合計いくら増えたか」が視界に入らない。予算は自分で上げられる"
            "ので、歯止めは累積を見ることにしかない (2026-08-27 に実際 5 回分 stale 化していた)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    # [FIX] anchor をラチェットのたび動く値から不変部分へ移す。旧 anchor は `current=726300` を
    #   直接掴んでおり、**次のラチェットで必ず orphan 化**した (実際に 2026-09-06 に Check 362 が検出)。
    #   末尾に数字を足すだけで current が別値になり Check 461 が RED になる。
    "find": "session-start=716800 current=",
    "replace": "session-start=716800 current=9",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 462: Zenn 記事数の自己申告だけを動かす —— 記事の増減で文言が取り残されると、"
            "公開面が silent に嘘の本数を名乗る。機械可読な権威シグナルを正しく保つことが主眼の"
            "リポジトリで、公開文言の事実誤りは中核の毀損にあたる",
    "file": ROOT / "js" / "components.js",
    "find": "全11本の記事",
    "replace": "全12本の記事",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 460 (g): 入口ページから規模の申告そのものを消す —— REVIEWERS.md は "
            "reviewer が最初に読む英語ページで、そこが 'All N adverse facts' と完全性を主張する。"
            "2026-09-05 に実測すると 118/14/Five と書いてあり実体は 144/57/9 で、3 つとも過少だった。"
            "「全部開示する」と述べるドシエが開示量を小さく言うのは、間違える向きとして最悪である",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    # anchor は **数字を含めない** —— 件数は増分ごとに動くので、数字を釘にすると
    # 次の増分で Check 362 が orphan として RED にする (本 mutation で実際に踏んだ)。
    # "All " を落として申告そのものを消す形にすると、face (g) の「申告が見つからない」
    # 枝を突ける —— 維持が面倒になった誰かが文ごと消す、という現実的な退行でもある。
    # 2026-09-09 再アンカー (2 度目)。前の釘は "**Read this first.** All " で、#120 が
    # その一文を書き換えた瞬間 orphan になった。**教訓は「数字を釘にするな」だけでは
    # 足りない —— 説明文そのものが動く。** そこで今度は **Check 460 (g) が探す正規表現の
    # 文字列そのもの**を釘にする: face (g) は `(\d+) worked entries, indexed by the question`
    # を探すので、その語順を壊せば「申告が見つからない」枝が必ず発火する。
    # **釘と検査対象が同一なので、検査が在る限り釘も在る。**
    "find": "worked entries, indexed by the question",
    "replace": "worked entries, listed by the question",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 464: 次版の変更リストから errata を 1 件落とす —— 1.0 は凍結中で「欠陥は直さず"
            "記録する」運用なので、記録が集約点に載らなければそのまま忘れられる。1.1 の入力は "
            "errata / review-responses-meta / review-responses-clauses / discussion-log の 4 か所に"
            "散っており、議論後に回って集める手順は必ず落とす",
    "file": ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md",
    "find": "| E9 | §10.4 |",
    "replace": "| E99 | §10.4 |",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 465: rounds/ の在庫申告を実測より小さくする —— 記録が drift しないためだけに"
            "在るディレクトリの入口が、中身の量について偽を述べる形。2026-09-06 まで実際に"
            "「いまの状態: 空である」と書かれ続けており (against.md #89)、審査者は証拠の量を"
            "その入口から受け取るので、小さく言うのは開示の主張を嘘にする",
    "file": ROOT / "LICENSES" / "rounds" / "README.md",
    # [FIX] 初版は find を「…7 ファイル」に釘付けしていた。**件数は増分のたびに動く値**なので、
    #   翌日 8 件目を置いた時点で anchor が消え Check 362 が orphan として RED にした
    #   (CLAUDE.md §7「安全網の anchor は『たまたま近くにある文字列』を掴みやすい」の 6 度目)。
    #   在庫表の先頭行 —— **最初の送信であり、以後動かない** —— の行頭 `|` を落として
    #   「行として数えられない」状態を作る形へ移した。件数見出しではなく行数の面を打つ。
    "find": "\n| 2026-08-26 | ",
    "replace": "\n2026-08-26 | ",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 466: 表紙から審査者への案内を消す —— 送った文面は GitHub リポジトリを指すので "
            "README.md は審査者の入口である。案内が無ければ、`LICENSES/` の 24 文書は在っても"
            "到達されない。2026-09-07 まで実際にこの案内は 214 行下にあり、手前は AI 向けブロックと"
            "日本語の節だった (against.md #94)",
    "file": ROOT / "README.md",
    "find": "> **[`LICENSES/REVIEWERS.md`](LICENSES/REVIEWERS.md)** \u2014 it is in English and states the",
    "replace": "> **the reviewer guide in this repository** \u2014 it is in English and states the",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 463: 送る文面から OSD 3/5/6/9 の名指しを落とす —— OSI の review-process は"
            "「OSD に準拠する」ではなく「**3, 5, 6, 9 を満たすと specifically 明言する**」を求める。"
            "2026-09-07 に Carlo Piana 氏が別の提出へ『required information が無いので解決するまで"
            "コメントしない』と述べた (against.md #97) ため、欠落は議論の遅れではなく不成立を招く",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "**OSD 5 and OSD 6**",
    "replace": "**OSD 5/6**",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 467: 単一ソースだけ `paused` へ戻す —— 状態は面に散らばっており、**両方向に危険である**。"
            "止めたのに面が残っていなければ次のセッションが送りかねず、再開したのにバナーが残れば"
            "送れるのに送らない。marker と面が食い違ったら必ず RED になること。"
            "**2026-09-17 に発信が再開したので、mutation の向きを逆にした** ——"
            "**anchor が解決することは、正しい向きを打っている証拠ではない**",
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": "<!-- POSTING-STATUS: active -->",
    "replace": "<!-- POSTING-STATUS: paused 2026-09-09 -->",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 460 (m): register の集計行を古い値に戻す —— 項目を足すたび列は増えるのに集計行は"
            "動かない。**しかも過少申告は #58 と同じ向きの誤りで、読み手は残作業を少なく見積もる**",
    "file": ROOT / "LICENSES" / "ACD-OSI-BOTTLENECKS.md",
    # **anchor は可変値に釘付けにしない。** 初版は宣言側の数 ("… 要る 6") を find にしていたが、
    # **その数は項目を足すたび動く**ので、2026-09-13 に B2 へ OSI の ○ を足した瞬間 orphan 化した
    # (Check 362 が捕捉)。**表の側の不変なラベルを打ち、○ を落として導出値を 1 減らす** ——
    # 宣言と導出がずれるので Check 460 (m) は同じように RED になり、**anchor は数から独立する。**
    # **⚠ 最初の書き直しは、解決するのに発火しなかった。** 行の途中に列を挿し込んだため、
    # face (m) が見る「末尾 3 列」がずれず導出値が動かなかった ——**anchor が解決することは、
    # 正しい対象を打っていることを意味しない** (Check 362 / 420 はどちらも前者しか見ない)。
    # **○ そのものを落とす形にして RED を実測した。**
    "find": "**外部回答待ち**（E11・steward が自ら出した唯一の問い）| — | — | ○ |",
    "replace": "**外部回答待ち**（E11・steward が自ら出した唯一の問い）| — | — | — |",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 460 (n): §4c の「機械的に確かめた」数字を 1 つずらす —— この表は審査者に"
            "「弁護士がいなくても機械で確かめられること」を示す面で、**表自身が『nothing enforces it』と"
            "書いていた**（2026-09-06 の再導出では実際に 3 行が誤っていた）",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-reference.md",
    "find": "| 10 terms, all in §1.1",
    "replace": "| 11 terms, all in §1.1",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 470: 条項に帰属させた逐語引用を、別の条へ付け替える —— 法への参照規則は §15.2 に"
            "在るのに §15.6 に帰属していた（実欠陥・2026-09-15）。**§15.6 は代理・組合の否認で、"
            "法への参照を 1 つも持たない** ——審査者が pointer を辿ると空振りする",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "\u00a715.2's interpretation rule",
    "replace": "\u00a715.6's interpretation rule",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 471 (a): `rounds/` の一次資料への参照を、実在しない file 名へ変える —— "
            "**`rounds/` は「一次資料はここに在る」という証拠の主張そのもの**で、"
            "指した先が無ければ審査者は存在しない原文を探しに行く",
    "file": ROOT / "LICENSES" / "AUDIT-LEDGER.md",
    "find": "rounds/2026-09-14-osi-normative-pages-snapshot.txt",
    "replace": "rounds/2026-09-14-osi-normative-pages-missing.txt",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 471 (f): \u00a71.xx の共有採番を衝突させる —— この採番は 5 file に分かれており、"
            "**同じ番号を 2 つの file が使うと参照は「解決する」のに別の節へ着く。(d)(e) は解決性しか"
            "見ないので原理的に捕捉できない** (2026-09-15 に実際に重複を作った)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-precedents.md",
    "find": "## 1.88 \u627f\u8a8d\u306f\u53d6\u308a\u6d88\u305b\u306a\u3044",
    "replace": "## 1.87 \u627f\u8a8d\u306f\u53d6\u308a\u6d88\u305b\u306a\u3044",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 472b (提出側の逐語引用の版): 1.1 の語句を 1.0 の条文として引かせる —— §16.4 は両方の版に"
            "在るので番号の存在しか見ない Check 472 は通すが、*\"except by the Steward\"* は 1.0 に無く、"
            "審査者は存在しない条文を読まされる (against.md #160 の実例)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-osd.md",
    "find": "**Applies identically to every distributor of the text, the steward included.**",
    "replace": "**Applies identically; §16.4 reads *\"except by the Steward\"*.**",
})

_MUTATIONS_TAIL.append({
    "name": "Check 467c (発信停止の現在形): 再開後の入口 README に「停止している」を戻す —— 467 の状態の面は"
            " REVIEWERS.md だけなので、列挙外の面が再開後も停止を述べ続けても通っていた",
    "file": ROOT / "LICENSES" / "README.md",
    "find": "> **発信は 2026-09-17 に再開した**（",
    "replace": "> **発信は 2026-09-09 から停止している**（",
})

_MUTATIONS_TAIL.append({
    "name": "Check 472c (入口ページの検証コマンド): 期待値を実行結果と違う値にする —— 審査者は貼って比べるので、"
            "正しいテキストを前に改変を疑わせる (#190)",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "editing            → expect 1",
    "replace": "editing            → expect 0",
})

_MUTATIONS_TAIL.append({
    "name": "Check 472d (入口の到達距離): \"In one screen\" を見出しごと消す —— B13 の唯一の実効的な緩和が黙って失われる",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "## In one screen\n",
    "replace": "## At a glance\n",
})

_MUTATIONS_TAIL.append({
    "name": "Check 472e (placeholder 0 の限定): 限定を外して無限定の 0 に戻す —— §16.1 の雛形 1 欄があるので偽",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-rules.md",
    "find": "固有名詞 0・条項の置換テキスト 0（§16.1 の推奨 notice の雛形 1 欄を除く）・採用に本文編集は不要（§4b）",
    "replace": "固有名詞 0・置換テキスト 0・採用に本文編集は不要（§4b）",
})

_MUTATIONS_TAIL.append({
    "name": "Check 434c (git の -z): Check 454 の git ls-files から -z を外す —— 日本語名のパスが引用符付きで返り、"
            "is_file() が偽になって黙って飛ばされる (2026-09-21 の週次配信検査の赤と同じ根)",
    "file": ROOT / ".github" / "scripts" / "checks_size_budget.py",
    "find": '_ls454 = _sp454.run(["git", "ls-files", "-z"], cwd=str(ROOT),',
    "replace": '_ls454 = _sp454.run(["git", "ls-files"], cwd=str(ROOT),',
})

_MUTATIONS_TAIL.append({
    "name": "Check 476 (承認済みライセンスの本数): 別の量の一括更新に巻き込まれた本数 —— 2026-09-19 に "
            "不利な事実の件数を 149 → 150 と上げた更新が、偶然同じ値だった承認済みの本数まで押し上げた実例の再現",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-reference.md",
    "find": "against all 149 OSI-approved licence texts",
    "replace": "against all 150 OSI-approved licence texts",
})
_MUTATIONS_TAIL.append({
    "name": "Check 471 (i): 英語で書いた英字節参照 `section E.1` を存在しない節へ向ける —— "
            "face (e) は `\u00a7` 付きしか見ておらず、SPDX 提出文の「section B.2 above」"
            "（分割で消えた節）を素通りした (2026-09-25)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-reference.md",
    "find": "A fuller statement is in section E.1.",
    "replace": "A fuller statement is in section E.9.",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468 (else): 次版草案の path を存在しない名前にずらす —— 以前は草案が無いと "
            "468 は OK も ERROR も出さずに消えた。版を確定して DRAFT を改名した日に、次版の検査が"
            "黙って止まる形だった (2026-09-26 に else を追加)",
    "file": ROOT / ".github" / "scripts" / "checks_license_draft.py",
    "find": '_dr468 = ROOT / "LICENSES" / "ACD-1.2-DRAFT.txt"',
    "replace": '_dr468 = ROOT / "LICENSES" / "ACD-1.2-DRAFT-MISSING.txt"',
    "check": CHECK,
})

MUTATIONS = MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。
















































_E2E_TAIL.append({
    "name": "settings の aria-labelledby が dangling になる —— 支援技術がその参照を辿ると存在しない要素へ着地し、グループ名が失われる。視覚には一切出ないので screenshot でも目視でも気付けない",
    "file": ROOT / "js" / "settings-page.js",
    "find": "'aria-labelledby': 'settingsIncludeGroupLabel'",
    "replace": "'aria-labelledby': 'settingsIncludeGroupLabelZZ'",
    "test": "全ルートの aria-* id 参照が実在要素へ解決する",
})

_E2E_TAIL.append({
    "name": "data-ai-state を JSON.stringify でなく文字列連結で組む —— filter は URL の query をそのまま echo するので、引用符を含む query 1 つで属性全体が壊れた JSON になり agent は route も loading も読めなくなる。視覚に一切出ない機械可読面の silent failure",
    "file": ROOT / "main.js",
    "find": """                document.body.setAttribute('data-ai-state', JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] 従来は `''` 決め打ちで絞り込みを宣言できなかった (router の単一ソースへ)。""",
    "replace": """                document.body.setAttribute('data-ai-state', '{"route":"' + (route.name || 'home') + '","filter":"' + Router.getFilterString() + '","loading":false}'); void JSON.stringify({
                    route: route.name || 'home',
                    // [FIX] 従来は `''` 決め打ちで絞り込みを宣言できなかった (router の単一ソースへ)。""",
    "test": "data-ai-state は敵対的な query でも valid JSON であり続ける",
})

_E2E_TAIL.append({
    "name": "quiz の動的 import に cache-buster が付く —— ESM のモジュールキャッシュが効かなくなり、開くたびに 83KB を再ダウンロードする。体感は速いままなので気付きにくいが通信量とバッテリーには効く",
    "file": ROOT / "main.js",
    "find": "import('./js/quiz/aws-quiz-data.js').then(m => m.awsQuizData)",
    "replace": "import('./js/quiz/aws-quiz-data.js?v=' + Date.now()).then(m => m.awsQuizData)",
    "test": "Revisiting the quiz does not re-download the question set",
})

_E2E_TAIL.append({
    "name": "「全リセット」が appsData を戻さなくなる —— 稼働中タイマー / quiz 検索語 / 未送信ノートが取り残され、「初期化したのに前の状態が残っている」一貫性の破れになる",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            State.set(Store.createDefaultStore());",
    "replace": "            State.update(s => { s.projects = Store.createDefaultStore().projects; });",
    "test": "Full reset clears pomodoro / quiz search / notes together",
})

_E2E_TAIL.append({
    "name": "ダークテーマの前景トークン (--on-tint-success) が暗背景に暗い色になる —— 全ブランド x ダークの全ページでコントラストが落ちるが、既定のライトでは何も起きないので気付きにくい",
    "file": ROOT / "style.css",
    "find": """                --on-tint-success: #4ade80;""",
    "replace": """                --on-tint-success: #1f3d2a;""",
    "test": "indigo ダークの全ページで color-contrast",
})

_E2E_TAIL.append({
    "name": "nav リンクの aria-current が付かなくなる —— SR 利用者は「今どこにいるか」を失う。視覚は active スタイルが残るので目視でも screenshot でも気付けない (sidebar と drawer が同じ navLink を共有するため両方が同時に壊れる)",
    "file": ROOT / "js" / "components.js",
    "find": "'aria-current': item.active ? 'page' : undefined",
    "replace": "'aria-current': undefined",
    "test": "aria-current marks exactly the active nav item",
})

_E2E_TAIL.append({
    "name": "Lab トグルの開閉状態が永続化されなくなる —— 開いておいた利用者はルート遷移やリロードのたびに畳まれた状態へ戻る。1 回の操作では気付けず「たまに閉じている」としか見えない",
    "file": ROOT / "js" / "components.js",
    "find": "            try { localStorage.setItem(labKey, String(next)); } catch { /* ignore */ }",
    "replace": "            /* persistence removed */",
    "test": "toggle flips aria-expanded",
})

_E2E_TAIL.append({
    "name": "ダーク実効の --text-muted が暗背景に暗い色になる —— drawer / palette / toast など**開いた状態でしか見えない面**のコントラストが落ちる。既定の閉じた状態では何も起きないので通常の a11y 走査では踏まれない",
    "file": ROOT / "style.css",
    "find": """                --text-muted: #9aa4b5;""",
    "replace": """                --text-muted: #2b3444;""",
    "test": "ダークの drawer / palette / toast",
})

_E2E_TAIL.append({
    "name": "nav リンクから href が外れる —— マウスの click ハンドラは残るので**見た目も挙動も変わらず**、キーボード利用者だけがナビゲーションへ到達できなくなる (WCAG 2.1.1)。Googlebot のリンク発見も同時に失われる",
    "file": ROOT / "js" / "components.js",
    "find": "                href: '#/' + item.path,",
    "replace": "                'data-href': '#/' + item.path,",
    "test": "Sidebar nav link is keyboard-operable",
})

_E2E_TAIL.append({
    "name": "上限で断られたときに打った文字が消える —— 追加できたときだけクリアする復元を外すと、"
            "「不要なタスクを削除してください」と言われた時点で入力欄が既に空になっており、"
            "削除して戻っても打ち直しになる (クリア自体は #1061 の二重登録ガードとして必要)",
    "file": ROOT / "js" / "apps.js",
    "find": "if (!addTask(_v)) { e.target.value = _v; }",
    "replace": "addTask(_v);",
    "test": "keeps the typed text when the add is refused by the cap",
})

_E2E_TAIL.append({
    "name": "一時的な通信断から quiz が回復しなくなる —— 失敗した動的 import は module map に "
            "キャッシュされ、以降の import はネットワークへ行かず即 reject する。別 URL での "
            "再取得を外すと、開き直しても永久に失敗表示のまま (完全リロードしか直らない)",
    "file": ROOT / "main.js",
    "find": ").catch(() => _retryQuizData(type))",
    "replace": ")",
    "test": "recovers from a transient load failure by refetching under a new URL",
})

_E2E_TAIL.append({
    "name": "JSON-LD の CreativeWork ノードから license が落ちる —— schema.org で license は "
            "CreativeWork に定義される。1 ノードでも欠けると、その経路から来た agent は "
            "「学習してよいか」を判定できない (ACD-1.0 §6.5)。**視覚には一切出ない**",
    "file": ROOT / "js" / "meta-management.js",
    "find": "'license': SITE_CONFIG.LICENSE_URL,\n                'dateModified'",
    "replace": "'dateModified'",
    "test": "レンダリング後の全 CreativeWork ノードが同一のライセンスを宣言する",
})

_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.0.txt" />',
    "replace": '<!-- removed by mutation probe -->',
    "test": "HTML 標準の license リンクが全ルートで解決可能な形で存在する",
})

_E2E_TAIL.append({
    "name": "runtime の speakable ノードが canonical と同じ @id にルート固有の name を載せる —— "
            "JSON-LD では同一 @id = 同一エンティティなので property が merge され、"
            "**1 つのエンティティが 2 つの名前を主張**する。「このクエリはこのエンティティにのみ "
            "解決すべき」という中核宣言と真っ向から矛盾する (2026-08-23 の実バグ)",
    "file": ROOT / "js" / "meta-management.js",
    "find": "            'license': SITE_CONFIG.LICENSE_URL,\n            'speakable': {",
    "replace": "            'license': SITE_CONFIG.LICENSE_URL,\n            'name': fullTitle,\n            'speakable': {",
    "test": "同一 @id が矛盾する property 値を宣言しない",
})

_E2E_TAIL.append({
    "name": "取り込みモード「全置換」が appsData に効かなくなる —— #1183 の実バグそのもの。"
            "モードは projects にしか効いておらず、appsData はどのモードでも丸ごと置き換えていた "
            "(既定の「追加のみ」で AppsData を含むファイルを取り込むと**既存のタスク・やること・"
            "ノート・履歴が全部消えた**)。**最も安全なつもりの選択が最も破壊的**で、しかもそれが既定値",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (settingsImportMode === 'strict') {\n                        merged.appsData = inc;",
    "replace": "                    if (false) {\n                        merged.appsData = inc;",
    "test": "「全置換」の import は宣言どおり丸ごと置き換える",
})

_E2E_TAIL.append({
    "name": "取り込みモード「更新+追加」が既存 id を更新しなくなる —— append との差が消え、"
            "3 モードのうち 2 つが同じ挙動になる。**利用者は宣言どおりに動いたと信じて元データを"
            "捨てうる**ので、モード間の意味論の差は e2e で固定しておく必要がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "if (!map.has(x.id) || settingsImportMode === 'upsert') { map.set(x.id, x); }",
    "replace": "if (!map.has(x.id)) { map.set(x.id, x); }",
    "test": "「更新+追加」の import は既存を残しつつ取り込む",
})

_E2E_TAIL.append({
    "name": "slug 一意化を無効化する —— #154 の実バグ。同名プロジェクトを追加すると slug が衝突し、"
            "ProjectDetailPage の find(p.slug===slug) が先頭のみ返すため**片方の詳細ページへ"
            "到達不能**になる。一覧には両方出るので気付く手掛かりが薄い",
    "file": ROOT / "js" / "store.js",
    "find": "            if (_seenSlugs.has(s)) {\n                let n = 2;",
    "replace": "            if (false) {\n                let n = 2;",
    "test": "Adding two projects with the same name yields unique slugs",
})

_E2E_TAIL.append({
    "name": "sidebar の nav リンクが指すルートを 1 つ router から落とす —— 利用者にはナビを押すと "
            "NotFound が出るだけに見える。この gate は 2026-08-24 まで **前ルートの DOM に対して "
            "不在アサーションを評価**しており、自分が名乗っている「壊れた nav リンク」を一度も "
            "検出できなかった (遷移直後の NotFound 見出し 0 件で PASS・settle 後は 1 件)",
    "file": ROOT / "js" / "router.js",
    "find": "            case 'role-split':\n                route.name = 'role-split';",
    "replace": "            case 'role-split-DISABLED':\n                route.name = 'role-split';",
    "test": "All sidebar nav links resolve to valid",
})

_E2E_TAIL.append({
    "name": "quiz の章見出しを h2 -> h4 にして heading-order を壊す —— 長い読み物の見出し階層が"
            "飛ぶと、スクリーンリーダーの主要移動手段である見出しジャンプで本文を辿れなくなる。"
            "この違反は 2026-08-24 まで **ダーク走査から構造的に見えなかった**: ループの待ちが汎用で"
            "前ルートの DOM で成立していたため、axe はちょうど 1 つ前のルートを走査しており "
            "`#/quiz` (最大のコンテンツページ) は一度も走査されていなかった (実測: 同じ違反を"
            "注入して旧待ちでは PASS・新待ちでは `#/quiz: heading-order(1)` で FAIL)",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h2\", { class: \"quiz-section-title\" }, section));",
    "replace": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h4\", { class: \"quiz-section-title\" }, section));",
    "test": "ダークテーマの全ルート",
})

_E2E_TAIL.append({
    "name": "quiz の章カードに min-width を与えて 320px であふれさせる (WCAG 1.4.10)。この違反は "
            "2026-08-24 まで **reflow の走査から構造的に見えなかった**: ループの待ちが汎用で前ルートの "
            "DOM で成立していたため、6 ルート全てが `#/role-split` を測っており、#962 で直した実バグの "
            "対象 (quiz / hiring-risk / pomodoro) は一度も測られていなかった",
    "file": ROOT / "style.css",
    "find": ".quiz-section-card {",
    "replace": ".quiz-section-card { min-width: 420px;",
    "test": "320px 幅でどのルートも横スクロールしない",
})

_E2E_TAIL.append({
    "name": "AI 応答到着時のルート判定を潰す —— 応答は submit の 300ms 後に非同期で届くので、"
            "その間に別アプリへ移っているのは普通にある。ルートを見ずに State.update すると "
            "notify → #content の全再描画が起き、**操作していない画面の未送信入力が消える** "
            "(実測: AI-INTERRUPT-DRAFT → \"\")。#994 の focus 復元が id で働くぶん "
            "**activeElement は残って値だけ消える**ので、利用者は原因に見当がつかない。"
            "#982 / #1055 / #1056 と同じ class",
    "file": ROOT / "js" / "ai-page.js",
    "find": "if (onAiRoute) { State.update(applyResponse); }",
    "replace": "if (true) { State.update(applyResponse); }",
    "test": "別アプリで入力中のテキストを消さない",
})

_E2E_TAIL.append({
    "name": "「全リセット」を appsData だけ戻す部分リセットへ退行させる —— projects / profile / "
            "theme / projectPrefs が残る。**「全」と名乗る操作が一部しか戻さない**のは、利用者が"
            "「初期化した」と信じて元データを捨てうる silent failure。実測 (2026-08-26): "
            "pomodoro/quiz/notes を見る multi-app リセット test も、AI 応答待ち中のリセット test も"
            "**appsData しか見ないので素通り**する。捕捉層は apps-settings-io の 2 件だけだった",
    "file": ROOT / "js" / "settings-page.js",
    "find": "State.set(Store.createDefaultStore());",
    "replace": "State.set({ ...State.get(), appsData: Store.createDefaultStore().appsData });",
    "test": "表示テーマが export → import で復元され",
})

_E2E_TAIL.append({
    "name": "theme を「値が変わらなくても applied に数える」形へ戻す —— フルバックアップには "
            "**必ず theme が入る**ので、この 1 行だけで #1040 の「0 セクションなら成功と言わない」"
            "ガードが最も一般的なファイル形式に対して丸ごと無効化される。実測 (2026-08-26): "
            "対象 3 つを全て外して読み込むと state は前後で完全に同一なのに「完了しました」と出る。"
            "既存の #1040 test は theme を含まない `AppsDataのみ` を使うためこの枝を踏めない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (parsed.theme !== base.theme) { applied = true; }",
    "replace": "                    applied = true;",
    "test": "フルバックアップでも、対象を全部外したら成功と report しない",
})


_E2E_TAIL.append({
    "name": "`Projectsのみ` の書き出しを projects の素の配列へ戻す —— 既定プロジェクトは削除できず "
            "**「非表示」が唯一の非公開手段** (#886) なのに、このファイルから復元すると "
            "隠したプロジェクトが黙って再公開される。フルバックアップは #1037 で projectPrefs を "
            "含むよう直したのに、部分 export だけ取り残されていた形 (実測 2026-08-26)",
    "file": ROOT / "js" / "settings-io.js",
    "find": "downloadJSON({ projects: s.projects, projectPrefs: s.projectPrefs },",
    "replace": "downloadJSON(s.projects,",
    "test": "Projectsのみ の往復で非表示設定が戻る",
})


_E2E_TAIL.append({
    "name": "貼り付けが maxlength で切られたことを黙らせる (通知条件を殺す) —— **打鍵は「入らなく"
            "なる」のが見えるが貼り付けは無反応**。実測 (2026-08-26): タスク入力へ 500 文字を貼ると "
            "200 文字だけ残り 300 文字が通知ゼロで消えた。既定動作は妨げず報告だけを足す設計なので、"
            "この条件を殺すと**元の silent な消失に戻る**",
    "file": ROOT / "js" / "ui-components.js",
    "find": "        if (dropped > 0) {",
    "replace": "        if (false) {",
    "test": "上限を超える貼り付けは、消えた文字数を通知する",
})


_E2E_TAIL.append({
    "name": "スナップショットの上書き確認を無効化する —— スロットは**単一**なので 2 度目の「保存」は "
            "前の内容を消して現在の状態で置き換える = **削除と同じく不可逆**。clearSnapshot は "
            "#1185 で confirm を得たのに**上書きだけ取り残されていた** (実測 2026-08-26: 2 回目の "
            "クリックで dialog ゼロのまま保存日時が置き換わった)。壊れた状態を実験したあと反射的に "
            "「保存」を押すと、**戻るはずだった良い状態を自分で消す**",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (_prev) {",
    "replace": "            if (false) {",
    "test": "スナップショットの上書きは確認を求め、キャンセルすると元が残る",
})


_E2E_TAIL.append({
    "name": "全置換 (strict) モードの取り込み確認を無効化する —— **最も破壊的な経路**なのに、"
            "プロジェクト 1 件の削除も全リセットもスナップショットの削除・上書きも confirm を通すのに"
            "ここだけ素通りしていた (実測 2026-08-26: dialog ゼロで既存タスクが消えた)。"
            "**モードは遷移を跨いで残る**ので、一度 strict にした利用者が後で別のファイルを"
            "取り込むときに選択を覚えていない、という現実的な経路がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (settingsImportMode === 'strict') {\n                    if (!confirm(",
    "replace": "                if (false) {\n                    if (!confirm(",
    "test": "全置換モードの取り込みは確認を求め、キャンセルすると既存データが残る",
})


_E2E_TAIL.append({
    "name": "プロジェクト削除の確認文から**対象の名前**を落とす —— 成功 Toast は名前を出すのに "
            "確認が「本当に削除しますか？」だけだと、**一覧で行を押し間違えても気付けない** "
            "(名前が出るのは消えた後)。#1185 が「文言は何を失うかを明示する」と原則を書いたのに、"
            "その比較対象だった当の削除が取り残されていた",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (!confirm(_target && _target.name",
    "replace": "            if (!confirm(false && _target && _target.name",
    "test": "Deleting a user project (confirm accepted) removes it everywhere",
})


_E2E_TAIL.append({
    "name": "全リセットの確認文から「元に戻せません／スナップショットは残ります」を落とす —— "
            "**何を失い何が残るかを言わない確認は判断材料にならない**。残るものを伝えるほうが"
            "利用者は判断できる (消える恐れで踏みとどまる必要が無くなる)。#1185 が書いた"
            "「文言は何を失うかを明示する」原則の、全リセット面",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                + '元に戻せません。スナップショットは残ります。')) {return;}",
    "replace": "                + '')) {return;}",
    "test": "全リセットの確認文は、元に戻せないことと残るものを伝える",
})


_E2E_TAIL.append({
    "name": "取り込み失敗の文言から**受け付ける形式の案内**を落とす —— 利用者はこのアプリ自身が"
            "書き出したファイルを読み込もうとして失敗しており、「失敗した」だけでは**次の一手が"
            "無い行き止まり**になる。受け付ける 4 形式はアプリ自身が知っているのだから伝える",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    Toast.show('認識できない形式のファイルです。'",
    "replace": "                    Toast.show('認識できない形式のファイルです', 'error'); if (0) Toast.show('x'",
    "test": "認識できない形式の JSON は成功と report しない",
})

_E2E_TAIL.append({
    "name": "スキーマ移行の通知を落とす —— 版数が変わったデプロイで**全データが既定へ戻る**のに、"
            "消えたことも復元できることも伝えない状態に戻す。退避先は作られているので救えるのに、"
            "利用者からは「開いたら全部消えていた」としか見えず復元導線へ辿り着けない",
    "file": ROOT / "js" / "state.js",
    "find": "const _migration = Store.takeMigrationNotice ? Store.takeMigrationNotice() : null;",
    "replace": "const _migration = null;",
    "test": "Schema migration tells the user what was reset",
})

_E2E_TAIL.append({
    "name": "スナップショットの由来判定を潰す —— 移行時の自動退避を「手動で保存」と表示させる。"
            "自動退避は load 時に走るため確認を挟めず手動保存を黙って上書きするので、由来を"
            "誤って表示すると利用者は自分の復元点が残っていると誤解したまま別物を復元する",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (snap.reason === 'schema-mismatch') {",
    "replace": "            if (false) {",
    "test": "自動退避されたスナップショットは移行元と移行先を示す",
})

_E2E_TAIL.append({
    "name": "brand の取り込みを落とす —— 「フルバックアップ」に配色が入っていても復元されない"
            "状態に戻す。brand は store の外なので merged に載せても normalize が落とす。theme が"
            "戻るのに brand だけ戻らない非対称は利用者から見て「フル」の約束破り",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (typeof parsed.brand === 'string' && Brand && Brand.set) {",
    "replace": "                if (false) {",
    "test": "配色 (brand) が export → import で復元される",
})

_E2E_TAIL.append({
    "name": "書き出しの成功通知を落とす —— ファイルは落ちるのに何も報告しない状態に戻す。"
            "他の操作は全て報告するのに書き出しだけ黙る非対称で、SR 利用者は成否を知る手段が"
            "無い (WCAG 4.1.3)。バックアップは「取れたつもり」が最も危ない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show(`${filename} を書き出しました`);",
    "replace": "            void filename;",
    "test": "書き出しは成功を報告する",
})
_E2E_TAIL.append({
    "name": "書き出しの失敗を握り潰さず再送出する —— 修正前の挙動に戻す。例外がそのまま致命"
            "エラーへ昇格し FatalPage と全画面オーバーレイで Settings が消える＝**バックアップを"
            "取ろうとして画面を失う**。失敗の伝え方として最悪の形",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show('書き出しに失敗しました。ブラウザのダウンロード設定を確認してください。', 'error', 5000);",
    "replace": "            throw e;",
    "test": "書き出しが失敗しても致命エラーにせず理由を伝える",
})

_E2E_TAIL.append({
    "name": "リセットの通知を落とす —— 押してもボタン名は変わらず、タイマーは意図的に非 live"
            "なので、結果だけ変わって無音になる。見えない利用者にはリセットできたのかどうかが"
            "分からない (開始/一時停止はラベル、モード切替は aria-pressed が変化を伝える)",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "            announce(`${label}のタイマーをリセットしました。残り ${formatTime(duration)}`);",
    "replace": "            void label;",
    "test": "リセットは結果を支援技術へ伝える",
})



_E2E_TAIL.append({
    "name": "nav リンク自身の closeDrawer を落とす —— 別ルートへの遷移は hashchange の配線 (#998) が"
            "閉じるので気付けないが、**今いるページのリンクを押したとき**は hash が変わらず hashchange が"
            "発火しないため drawer が開いたまま残る。モバイルでは画面を覆うので、メニューを閉じるつもりの"
            "普通の操作で閉じなくなる",
    "file": ROOT / "js" / "components.js",
    "find": "                    if (isDrawer) { closeDrawer(); }",
    "replace": "                    if (false) { closeDrawer(); }",
    "test": "今いるページの nav リンクを押しても drawer は閉じる",
})
_E2E_TAIL.append({
    "name": "詳細ページの「一覧に戻る」が絞り込みを捨てる —— router が戻り先を query 込みで保持する"
            "単一ソース (#951) を潰す。1 件に絞り込んだ状態から戻ると全件に戻り、利用者は同じ意味の"
            "操作 (ブラウザの戻る) との食い違いに気付けない",
    "file": ROOT / "js" / "router.js",
    "find": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = raw; }",
    "replace": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = 'projects'; }",
    "test": "In-page \"back to list\" preserves the active filter",
})

_E2E_TAIL.append({
    "name": "カテゴリ絞り込みの URL 同期を落とす —— 画面上は絞り込まれるのに URL に残らないので、"
            "共有したリンクや再読み込みで全件へ戻る。絞り込みは「今見ている範囲」そのものなので、"
            "URL に出ないと共有も復元もできない",
    "file": ROOT / "js" / "projects-page.js",
    "find": "                if (cat !== 'All') {params.set('cat', cat);}",
    "replace": "                if (false) {params.set('cat', cat);}",
    "test": "Projects category filter narrows the list and syncs to the URL",
})
_E2E_TAIL.append({
    "name": "nav リンクの aria-current を落とす —— 支援技術に「今どのページにいるか」が伝わらなくなる"
            "(WCAG 2.4.8)。視覚的な強調は class で別に付くので**目では気付けない**。sidebar と drawer は"
            "同じ実装を共有するが、mobile では drawer が唯一のナビなので両方が守られる必要がある",
    "file": ROOT / "js" / "components.js",
    "find": "                'aria-current': item.active ? 'page' : undefined",
    "replace": "                'aria-current': undefined",
    "test": "モバイルの drawer が現在ルートに aria-current を付け、遷移に追従する",
})

E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
