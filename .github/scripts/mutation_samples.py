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

from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_CHANGES, CURRENT_DRAFT_VER, PREVIOUS_VER, NEXT_CHECK, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, FROZEN_PREVIOUS  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
from mutation_samples_archive7 import MUTATIONS_ARCHIVE7
from mutation_samples_archive6 import MUTATIONS_ARCHIVE6
from mutation_samples_archive5 import MUTATIONS_ARCHIVE5
from mutation_samples_archive4 import MUTATIONS_ARCHIVE4
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
    "name": "Check 498 (h): READ-THREADS.txt から読了の行を 1 つ消す —— AS-OF の 3 つの数は和が合ったまま残り、旧版 (同じ文の中の"
            "算術だけ) は読了の一覧と AS-OF の食い違いを見なかった (2026-11-15・2f が気付き 50 が提案)",
    "file": ROOT / "LICENSES" / "READ-THREADS.txt",
    "find": "1999-04-24\tAPSL 1.1 certification...\n",
    "replace": "",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 498 (h): 2010 年以後に始まった会話の行を READ-THREADS.txt (2009 年まで) にも置く —— 読了の集合も件数も変わらない"
            "ので、年の照合が無ければ通り、record_read の重複の照合 (書く file の中だけ) もすり抜ける (2026-11-16・年で 2 つに分けたとき)",
    "file": ROOT / "LICENSES" / "READ-THREADS.txt",
    "find": "2009-12-08\tOKL4 license\n",
    "replace": "2009-12-08\tOKL4 license\n2010-01-19\tmove licenses to voluntarily retired list?\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 498 (h): 2010 年以後に始まった候補の会話の行を THREAD-CANDIDATES.txt (2009 年まで) にも置く —— 候補の集合も件数も"
            "変わらないので、年の照合が無ければ通る (2026-11-16・候補の一覧も年で分けたとき・50 の勧め)",
    "file": ROOT / "LICENSES" / "THREAD-CANDIDATES.txt",
    "find": "2009-12-08\tOKL4 license\n",
    "replace": "2009-12-08\tOKL4 license\n2010-01-19\tmove licenses to voluntarily retired list?\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468d: 草案の §6 の \"makes no Reservation\" を \"makes a Reservation\" へ —— gap を担う条の中身が消える。468d に"
            "登録の mutation が 1 つも無かった (2026-11-16・目印を _lib_draft_markers へ移したときに気付いた)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "makes no Reservation",
    "replace": "makes a Reservation",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468ab: 草案の §8.4 の \"Section 8.4 reaches a claim only\" を \"This Section reaches a claim only\" へ戻す —— 小項の中の "
            "\"this Section\" は §8 か §8.4 かで割れる (T84〜T88 で 5 → 0 にした型・2026-11-16)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "Section 8.4 reaches a claim only",
    "replace": "This Section reaches a claim only",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468ab: 草案の §14.2 の例外の列から 2.5 を外す —— §2.5 の約束 (撤回を主張しない) の違反まで §14.1 が免責する形に"
            "戻る (T88 で閉じた問い 9 (a) の型・2026-11-16)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "Section 2.5, 5, 8.6, or",
    "replace": "Section 5, 8.6, or",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468ac: §19 の §1.4 第 1 文の行の分類の欄を太字にする —— ROW19 に合わず台帳が数えなくなる形 (2026-11-19・50 が "
            "「**試作 T112 で入った**」で開いている試作 3 が 0 に見えたのを見つけた型)",
    "file": ROOT / "LICENSES" / "ACD-1.4-UNIQUE-READING.md",
    "find": "- §1.4 第 1 文 | 別の読み: *\"holds or may hold … in it\"* の *it* が Dedication を指す | 一意 |",
    "replace": "- §1.4 第 1 文 | 別の読み: *\"holds or may hold … in it\"* の *it* が Dedication を指す | **一意** |",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468 (定義語): §16.5 が定義する語を \"the Stewardship\" に変える —— 定義だけが残り、本文はどこもその語を使わない。"
            "語を外す試作が続く中で、使い先の無い定義を誰も見ていなかった (2026-11-15)",
    "file": CURRENT_DRAFT,
    "find": "In Section 16.4, \"the Steward\" means",
    "replace": "In Section 16.4, \"the Stewardship\" means",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 474 (474c): 提出の材料の §2 の表で #322 の直後の印を [CLOSED] にする —— register の状態と食い違う。#326 の行は "
            "register が [CLOSED] になった後も数時間古いまま残った (2026-11-15・50 の提案)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "（#322・**[EXTERNAL]**）",
    "replace": "（#322・**[CLOSED]**）",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 459c: review-readings-2 の reachable-via を消す —— 審査者向けの続きの冊が英語の入口 (REVIEWERS.md) から辿れなくなる。"
            "459 は README の索引しか見ず、QUESTIONS-FOR-PRACTITIONERS.md は入口から辿れなかった (2026-11-15・50 の提案)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-readings-2.md",
    "find": "reachable-via: ACD-1.0.review-readings.md\n",
    "replace": "",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468 (§0d): 材料 §0d の表の「§8.1 は *\"derived from\"*」を *\"resulting from\"* にする —— §8.1 にその語は無い。表の行は"
            "草案の状態を前提にしているのに、草案が変わっても何も鳴らなかった (2026-11-15・50 の提案)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "§8.1 は *\"derived from\"*",
    "replace": "§8.1 は *\"resulting from\"*",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 472n: QUESTIONS-FOR-PRACTITIONERS の草案の引用の 1 語を変える (automated → automatic) —— 英語で実務家に問う文書は"
            "入口の面に入っておらず、草案の引用を変えてもどの Check も鳴らなかった (2026-11-15)",
    "file": ROOT / "LICENSES" / "QUESTIONS-FOR-PRACTITIONERS.md",
    "find": "any automated processing of the Work",
    "replace": "any automatic processing of the Work",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 500: review-readings-2 の §1.241 の見出しを §1.240 に変える —— 帯を越えて同じ番号を 2 人が使うと、"
            "名を添えない「§1.N」の引用が解決しない (2026-11-15・5 人で未読を読む日)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-readings-2.md",
    "find": "\n## 1.241 ",
    "replace": "\n## 1.240 ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 501: review-readings-6 に反映の欄の無い節を足す —— 読んだ節がどこへ効いたかを書かないまま、"
            "未反映で本申請へ進める形 (オーナーの前提・2026-11-15)",
    "file": ROOT / "LICENSES" / "ACD-1.0.review-readings-6.md",
    "find": "で読了だけを記録する。\n",
    "replace": "で読了だけを記録する。\n\n## 1.499 反映の欄の無い節\n\n本文だけを書いた。\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 501b: REFLECTION-BACKFILL の行の番号を実在しない節へ変える —— 表の行が見出しと 1 対 1 でないまま、"
            "古い節を反映済みと数える形 (提出のゲート 6c・2026-11-15)",
    "file": ROOT / "LICENSES" / "REFLECTION-BACKFILL.md",
    "find": "\n| 1.179 | ",
    "replace": "\n| 1.1799 | ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 501b: 床 (70) の下の節の行き先から文書の名を外す —— 「§1.45」だけでは comparison の §1.45 とも読め、"
            "別の文書の同じ番号で照合が偽の緑になる (2026-11-15・30 の指摘)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "（`review-precedents.md` §1.45）",
    "replace": "（§1.45）",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 501b: 表の番号のセルを読めない形にする —— 形の合わない行を黙って飛ばすと、書いた人は表に足したつもりで"
            "照合だけ外れる (2026-11-15・50 の #3251 の 42 行)",
    "file": ROOT / "LICENSES" / "REFLECTION-BACKFILL.md",
    "find": "\n| `ACD-1.0.review-precedents.md` 1.45 | ",
    "replace": "\n| review_precedents 1.45 | ",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 451g: 確定の道具の textRedistribution の注を「ACD- を含む」から「ACD- で始まる」へ戻す —— 草案の §16.4 は "
            "contains と書くので、確定すると 1.4 の記述子が本文より狭い制限を述べる (errata E10 の型・2026-11-16)",
    "file": ROOT / ".github" / "scripts" / "prepare_version_freeze.py",
    "find": "or under any identifier that contains \\\"ACD-\\\", regardless of case, followed by a digit",
    "replace": "or under any identifier that begins with \\\"ACD-\\\" followed by a digit",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 470: UNIQUE-READING の §11.4 の行の「1.4 草案の §1.4（1.0 の §1.3）の」から条の番号を外す —— 作業文書にファイル名の版の"
            "地図を当てた後も、条を名指さない帰属は RED (2026-11-20・2f の案の対照)",
    "file": ROOT / "LICENSES" / "ACD-1.4-UNIQUE-READING.md",
    "find": "根拠: 1.4 草案の §1.4（1.0 の §1.3）の \"this Dedication operates severally as to each\"",
    "replace": "根拠: 1.4 草案の \"this Dedication operates severally as to each\"",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468ab: 草案の §14.2 の条件を「does not permit a liability to be excluded or limited」にする (T126 の前と同じ割れ) —— "
            "否定が or の並びに掛かり、除外は許さないが制限は許す場面が文から外れる型 (2026-11-20・1c の 4 巡目)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "to be excluded, that liability is limited",
    "replace": "to be excluded or limited, that liability is limited",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 473d: 17 U.S.C. §1201 の写しの逐語の片の shall を may に変える —— 置いた後に本文を直すと、§18 の行が引いた逐語が "
            "いつの文かを確かめられなくなる (2026-11-20)",
    "file": ROOT / "LICENSES" / "rounds" / "2026-11-19-us-17-usc-203-1201-snapshot.txt",
    "find": "No person shall circumvent a technological measure",
    "replace": "No person may circumvent a technological measure",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468ad: §19.5 の §14.2 の否定の掛かり先の行を「試作 T999 で入った」にする —— CHANGELIST に名の無い試作を台帳が"
            "「本文に入った」と言う形 (2026-11-20)",
    "file": ROOT / "LICENSES" / "ACD-1.4-UNIQUE-READING.md",
    "find": "| 試作 T126 で入った | 根拠: T126（PR 3742）で",
    "replace": "| 試作 T999 で入った | 根拠: T999（PR 3742）で",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 467d: LICENSES/README.md の「次版に反映するものの集約点」の行を同じ表の中で 2 行に重ねる —— 重なった行は数を揃える"
            "道具にも Check にも別の場所と数えられる (2026-11-20・50: SUBMISSION-MATERIALS の「| 長さ |」が T77 から 2 行だった)",
    "file": ROOT / "LICENSES" / "README.md",
    "find": f"| **次版に反映するものの集約点（{CURRENT_DRAFT_VER}）** | [`ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md`](ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md) |\n",
    "replace": f"| **次版に反映するものの集約点（{CURRENT_DRAFT_VER}）** | [`ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md`](ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md) |\n"
               f"| **次版に反映するものの集約点（{CURRENT_DRAFT_VER}）** | [`ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md`](ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md) |\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 502: 作業中の草案の冒頭から状態の箇条「It has not been posted to any list.」を消す —— 投稿の状態を何も述べない草案 "
            "(2026-11-23: 1.4 の確定で、CHANGES-ACD-1.4.txt を打っていた旧 entry が的を外したので、版に依らない CURRENT_DRAFT へ移した)",
    "file": CURRENT_DRAFT,
    "find": "    * It has not been posted to any list.\n",
    "replace": "",
})
_MUTATIONS_TAIL.append({
    "name": "Check 465: 1999〜2012 年の分冊の行の日付を 2022 年にする —— 帯の外の行は、日付で分冊を選ぶ読者にも差し込む道具にも "
            "見つからない (2026-11-23・在庫表を年の帯ごとの分冊へ移した)",
    "file": ROOT / "LICENSES" / "rounds" / "INVENTORY-1999-2012.md",
    "find": "\n| 2002〜2005 | ",
    "replace": "\n| 2022〜2025 | ",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498 (h2): 候補の一覧の census の定義の指紋を別の値にする —— 決める側の照合を変えて一覧を作り直さないと、"
            "gate_6c と (h) が古い定義の一覧で「未読 0」を返す (2026-11-23・照合の漏れで候補が 19 本増えた)",
    "file": ROOT / "LICENSES" / "THREAD-CANDIDATES.txt",
    "find": "# census-definition: ",
    "replace": "# census-definition: 0",
})
_MUTATIONS_TAIL.append({
    "name": "Check 468y: 1.5 の試作の T135 の見出しを「§11.4 は変えない」にする —— 逐条の §11.4 の行は T135 に触れていないので RED に"
            "なるはず。1.4 の確定の後、468y は名で決め打ちした SECOND / THIRD しか読まず、1.5 の試作を 1 つも読まなかった (2026-11-23)",
    "file": ROOT / "LICENSES" / "ACD-1.5-CLARITY-TRIAL.md",
    "find": "## 1. T135 —— §11.4 第 2 文の",
    "replace": "## 1. T135 —— §11.4 は変えない。第 2 文の",
})
_MUTATIONS_TAIL.append({
    "name": "Check 413: runbook §9 の追跡ファイルの行に絶対値を戻す —— 5 人が並行して file を足すと merge のたびに数がずれ、"
            "PR どうしが衝突して workflow が起動しなかった (2026-11-23 に数を外した)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": "| 追跡ファイル総数 | **数は書かない**",
    "replace": "| 追跡ファイル総数 | **2330**",
})
_MUTATIONS_TAIL.append({
    "name": "Check 470b: 逐条の §8.4 の行が引く 1.4 §8.3 第 2 文から *as to those acts* を落とし、T99 より前の文を「いまの文」として引く形に"
            "戻す (2026-11-23 に 470b を足したとき main に在った 1 件)",
    "file": ROOT / "LICENSES" / "ACD-1.4-CLAUSE-REFERENCE-DRAFT.md",
    "find": "*\"Nothing in this Dedication, as to those acts, reserves, preserves, or leaves unaffected any patent claim they reach.\"*（*as to those acts* は T99 で入った）",
    "replace": "*\"Nothing in this Dedication reserves, preserves, or leaves unaffected any patent claim they reach.\"*",
})
_MUTATIONS_TAIL.append({
    "name": "Check 468z: 次版の CHANGELIST の「## 記述子の候補」の箇条が引く条を、草案に無い §5.9 にする —— 節の名が「### N.M の記述子の"
            "下書き」から変わり、468z は OK 行に「—」を出して候補を照らしていなかった (2026-11-23)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md",
    "find": "`true`・§5.2・`note`",
    "replace": "`true`・§5.9・`note`",
})
MUTATIONS = MUTATIONS_ARCHIVE7 + MUTATIONS_ARCHIVE6 + MUTATIONS_ARCHIVE5 + MUTATIONS_ARCHIVE4 + MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。




























































_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": f'<link rel="license" href="/portfolio/LICENSES/{APPLIED_ID}.txt" />',
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

_E2E_TAIL.append({
    "name": "初回描画の route-focus ガードを外す —— ページを開いただけで h1 へ focus が移り、2px の枠が出て、"
            "最初の Tab が skip-link とナビを飛ばして本文へ着地する (2026-11-02 まで全ルートでこの状態だった)",
    "file": ROOT / "main.js",
    "find": "            if (isRouteChange && _hasRenderedOnce && content && _focusWasLost) {",
    "replace": "            if (isRouteChange && content && _focusWasLost) {",
    "test": "初回表示では focus を動かさず、最初の Tab は skip-link に届く",
})

_E2E_TAIL.append({
    "name": "about の Speakable が幻セレクタ [data-speakable] を宣言し直す — その属性は home の hero にしか無く、他ルートでは一度も対象を持たない (2026-11-03 まで実際にそうだった)。機械向けの面なので視覚にも他のテストにも出ない",
    "file": ROOT / "js" / "meta-management.js",
    "find": "            'about':       ['h1', '.sr-only'],",
    "replace": "            'about':       ['h1', '[data-speakable]', '.sr-only'],",
    "test": "Every non-home Speakable cssSelector resolves to real elements (AIO accuracy)",
})
_E2E_TAIL.append({
    "name": "quiz の未知 ?type= で title だけ汎用「Quiz」へ戻る —— 描画 (AWS 問題集) / sidebar nav (AWS active) と title が食い違う 2026-11-03 以前の状態",
    "file": ROOT / "js" / "page-meta.js",
    "find": "            return Object.prototype.hasOwnProperty.call(map, type) ? map[type] : map.aws;",
    "replace": "            return Object.prototype.hasOwnProperty.call(map, type) ? map[type] : 'Quiz';",
    "test": "Quiz document.title stays in the known-safe set for ?type=",
})
_E2E_TAIL.append({
    "name": "AI 履歴の取り込みの型ガードを truthy 判定へ戻す —— {prompt: {}} の entry が落ちず、空の会話として残る (2026-11-08 まで \"[object Object]\" を描画していた)",
    "file": ROOT / "js" / "store.js",
    "find": ".filter(h => h && isText(h.prompt) && isText(h.response))",
    "replace": ".filter(h => h && h.prompt && h.response)",
    "test": "Hostile AI history: non-string prompt/response must not render as [object Object]",
})
E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
