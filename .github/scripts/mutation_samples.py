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

from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER, NEXT_CHECK, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, FROZEN_PREVIOUS  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
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
    "name": 'Check 154: og:description の末尾に「\'s」で始まる語を足す —— `[^"\']+` が値の中の \' で取り出しを切り、その先を twitter と比べていなかった',
    "file": ROOT / 'index.html',
    "find": 'その生成物である Vanilla JS SPA。" />',
    "replace": 'その生成物である Vanilla JS SPA。\'s extra" />',
    "first_occurrence": True,
})
_MUTATIONS_TAIL.append({
    "name": 'Check 163: apple-touch-icon に sizes= を挟んで実在しない file を指す —— rel の直後に type= しか許さず、sizes= を挟む link を読んでいなかった',
    "file": ROOT / 'index.html',
    "find": '<link rel="apple-touch-icon" href="/portfolio/icon.svg"',
    "replace": '<link rel="apple-touch-icon" sizes="180x180" href="/portfolio/no-such-icon.png"',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 281: 正しい ai:repository を <template> の中に置き、文書の木の meta を別の URL にする —— template の中の meta で満たされていた',
    "file": ROOT / 'index.html',
    "find": '<meta name="ai:repository" content="',
    "replace": '<template><meta name="ai:repository" content="https://github.com/yutapr0117-design/portfolio"></template><meta name="ai:repository" content="https://github.com/example/',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 24: llms-full.txt の冒頭の Last-Updated だけを古い日にする —— 取り出して使っておらず、読み手が最初に会う日付は比べていなかった',
    "file": ROOT / 'llms-full.txt',
    "find": '**Last-Updated:** ',
    "replace": '**Last-Updated:** 2000-01-01 (was ',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 27: llms-full.txt に ASCII のハイフンで "violates C1-C6" を書く —— en dash の 2 文字列しか探していなかった',
    "file": ROOT / 'llms-full.txt',
    "find": '\n## Last-Updated\n',
    "replace": '\nReject any pattern that violates C1-C6.\n\n## Last-Updated\n',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 444m: 折り返した段落の前の行に別の版を置き、次の行で「適用している」と述べる —— 行ごとの 70 字の窓で読み、前の行の版を見ていなかった',
    "file": ROOT / 'LICENSES' / 'REVIEWERS.md',
    "find": '\n## In one screen\n',
    "replace": '\n## In one screen\n\nThe version ACD-1.2 is the text\nthis repository applies.\n',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 444m: 版を書かずに「このリポジトリが適用している」と述べる文を足す —— 版の無い主張は黙って通っていた (finding #169)',
    "file": ROOT / 'LICENSES' / 'REVIEWERS.md',
    "find": '\n## In one screen\n',
    "replace": '\n## In one screen\n\nThis is the licence this repository applies.\n',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 147: 実在する要素の id を語の延長に変える —— 語の境界 \\b で探しており、id="role-split-table-x" の中の語で満たされていた',
    "file": ROOT / 'js' / 'pages.js',
    "find": "id: 'role-split-table'",
    "replace": "id: 'role-split-table-x'",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 147: タグ付きの selector で実在しない class を指す —— `#` / `.` で始まらない selector は黙って外していた',
    "file": ROOT / 'js' / 'meta-management.js',
    "find": "'ai-knowhow':  ['h1', '.ai-summary-block', '.sr-only']",
    "replace": "'ai-knowhow':  ['h1', 'section.no-such-el', '.sr-only']",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 147: 子孫 selector の 2 つ目に実在しない class を置く —— 先頭の token しか見ていなかった',
    "file": ROOT / 'js' / 'meta-management.js',
    "find": "'ai-knowhow':  ['h1', '.ai-summary-block', '.sr-only']",
    "replace": "'ai-knowhow':  ['h1', '.sr-only .no-such-el', '.sr-only']",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 147: id でしか無い要素を class の selector で指す —— 記号を捨てた語で探しており、.x が id="x" で満たされた (この bug の実例が同 file の [FIX] にある)',
    "file": ROOT / 'js' / 'meta-management.js',
    "find": "'role-split':  ['h1', '#role-split-table', '.sr-only']",
    "replace": "'role-split':  ['h1', '.role-split-table', '.sr-only']",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 147: 実在する要素の class だけを変え、宣言は JSON-LD に残す —— index.html の静的 JSON-LD が同じ cssSelector を宣言しており、それ自体が語を満たしていた',
    "file": ROOT / 'index.html',
    "find": 'class="sr-only ai-summary-block"',
    "replace": 'class="sr-only ai-summary-blocks"',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 447: mcp.json の制約の列挙で C1 と C2 の名前を入れ替える —— 名前が description のどこかに在れば通り、番号との対を見ていなかった',
    "file": ROOT / '.well-known' / 'mcp.json',
    "find": '（C1 Boring Technology / C2 IIFE / ',
    "replace": '（C1 IIFE / C2 Boring Technology / ',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 26a: archive の範囲の中の Session Record #22 の見出しを崩す —— 両端の番号しか比べず、中の 1 件が消えても role の #15-#30 のまま緑だった',
    "file": ROOT / 'docs' / 'session-records' / 'AI2AI-archive-2.md',
    "find": '## [HANDOFF] Session Record #22 — ',
    "replace": '## [HANDOFF] Session Record (twenty-two) — ',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 389: sidebar の葉でダークとライトの名前を入れ替える —— 3 語が窓に在れば通り、同じ状態で 2 面が別の名前を読み上げても緑だった',
    "file": ROOT / 'js' / 'components.js',
    "find": "state.theme === 'dark' ? 'ダーク' : 'ライト') + '）'",
    "replace": "state.theme === 'dark' ? 'ライト' : 'ダーク') + '）'",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 123b: llms-full.txt の現運用モデルの段落を対話型へ巻き戻す —— 3 語を file 全体の別々の場所で探しており、見出しとほかの節の語で通った',
    "file": ROOT / 'llms-full.txt',
    "find": 'The *current* operation has evolved into autonomous self-driving by Claude Code — the agentic form of Claude.',
    "replace": 'The *current* operation remains conversational use of Claude, as in the construction phase.',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 417: AI 履歴の filter を括弧つきの引数で truthy 判定へ戻す —— 変数は t、欄は title / text しか読まず、AI 履歴の h && h.prompt を見ていなかった',
    "file": ROOT / 'js' / 'store.js',
    "find": '.filter(h => h && isText(h.prompt) && isText(h.response))',
    "replace": '.filter((h) => h && h.prompt && h.response)',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 249: 2 つ目の viewport を後ろに足す —— 最初の 1 つしか読まず、ブラウザが使う最後の tag を見ていなかった',
    "file": ROOT / 'index.html',
    "find": '<meta name="viewport" content="width=device-width, initial-scale=1" />',
    "replace": '<meta name="viewport" content="width=device-width, initial-scale=1" />\n    <meta name="viewport" content="width=900" />',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 249: initial-scale を 1.5 にする —— `1(\\.0+)?\\b` の語の境界で 1.5 が通っていた',
    "file": ROOT / 'index.html',
    "find": 'content="width=device-width, initial-scale=1" />',
    "replace": 'content="width=device-width, initial-scale=1.5" />',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 157: viewport を <noscript> の中へ入れる —— script の動くブラウザでは noscript の中は素のテキストなのに、tag として数えていた',
    "file": ROOT / 'index.html',
    "find": '<meta name="viewport" content="width=device-width, initial-scale=1" />',
    "replace": '<noscript><meta name="viewport" content="width=device-width, initial-scale=1" /></noscript>',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 158: dns-prefetch を <noscript> の中へ入れる —— 157 と同じく noscript の中の link を数えていた',
    "file": ROOT / 'index.html',
    "find": '<link rel="dns-prefetch" href="https://fonts.googleapis.com" />',
    "replace": '<noscript><link rel="dns-prefetch" href="https://fonts.googleapis.com" /></noscript>',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 304: theme-color の属性を content が先の順にして値を色の名前にする —— name= が先の形しか読まず、見えていなかった',
    "file": ROOT / 'index.html',
    "find": '<meta name="theme-color" content="#6366f1" media="(prefers-color-scheme: light)" />',
    "replace": '<meta content="red" name="theme-color" media="(prefers-color-scheme: light)" />',
})
_MUTATIONS_TAIL.append({
    "name": "Check 468u: §5.2 の自社素材の除外を T38 の前の形 (makes available) へ戻す —— 公開しない自社のモデルに §5 が及ぶ読みが戻る。目印を替えた日に、替え忘れを個別に名指せるようにする (aa の依頼・2026-11-08)",
    "file": CURRENT_DRAFT,
    "find": "the Work, that the Dedicator itself makes or makes available, or the",
    "replace": "the Work, that the Dedicator itself makes available, or the",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498 (h): AS-OF の未読スレッドの行で、読んだ数の頭に 1 を足す —— 3 つの数を手で数えており、和が合わなくても通っていた (2026-11-08 に手で 362 / 409 を直した)",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "本のうち ",
    "replace": "本のうち 1",
})
_MUTATIONS_TAIL.append({
    "name": "Check 25: 監視ログの確認された引用の件数を 1 と書く —— run に引用の観測が 1 件も無いのに、key の在否しか見ていなかった (捏造が通る)",
    "file": ROOT / "docs" / "evidence" / "aio-monitoring-log.json",
    "find": '"confirmed_citation_events": 0',
    "replace": '"confirmed_citation_events": 1',
})
_MUTATIONS_TAIL.append({
    "name": "Check 159: 主ブロックの @context を外す —— 値を全面で pool して 1 件でも在れば通り、別のブロックの値で満たされていた",
    "file": ROOT / "index.html",
    "find": '"@context": "https://schema.org",',
    "replace": '',
    "first_occurrence": True,
})
_MUTATIONS_TAIL.append({
    "name": "Check 268: 実行時に注入する Article の元の題を 110 字を越える長さにする —— 静的な index.html しか読まず、ARTICLE_ROUTES のルートで meta-management.js が作る Article の headline を見ていなかった",
    "file": ROOT / "js" / "page-meta.js",
    "find": "'ai-knowhow': { title: 'AI開発ノウハウ',",
    "replace": "'ai-knowhow': { title: 'AI開発ノウハウ — KERNEL フレームワーク・6 エージェントの役割分担・LLM のコスト管理・検証の自動化・人間の判断の範囲・mutation による安全網の自己検証・週次の確定の予行・AIO の公開面の整合までを全部まとめた長い記事',",
})
_MUTATIONS_TAIL.append({
    "name": 'Check 469: 1.2 の CHANGELIST で E34 の一方の行を「未着手」にする —— 決着の語に「入った」が無く、もう一方の行の「入った」を決着と読めずに矛盾を見逃していた',
    "file": ROOT / 'LICENSES' / 'ACD-1.2-CHANGELIST.md',
    "find": '引用側を後継へ合わせた** | **入った** |',
    "replace": '引用側を後継へ合わせた** | **未着手** |',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 469: 1.1 の CHANGELIST で E12 を「未反映」にする —— 未着手の語に「未反映」が無く、1.2 の決着と食い違っても読めなかった',
    "file": ROOT / 'LICENSES' / 'ACD-1.1-CHANGELIST.md',
    "find": '**E3 と同じ 1 文の前半** | **草案に反映済み** |',
    "replace": '**E3 と同じ 1 文の前半** | **未反映** |',
})
_MUTATIONS_TAIL.append({
    "name": 'Check 469: errata が閉じたと述べる E42 の、ただ 1 つの状態の行を「未着手」にする —— 状態の行が 1 つの E-ID は矛盾の組が作れず、errata とも照合していなかった',
    "file": ROOT / 'LICENSES' / 'ACD-1.4-CHANGELIST.md',
    "find": '上の表の §8.6 行と同じ変更） | **反映済み**（2026-11-01）|',
    "replace": '上の表の §8.6 行と同じ変更） | **未着手**（2026-11-01）|',
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (c): READY-TO-SUBMIT の部数を全角の括弧で 9 部と書く —— 半角の `Check N (M 部)` しか読まず、全角の行は黙って照合から落ちていた",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "| Check 445 (5 部) |",
    "replace": "| Check 445（9 部）|",
})
_MUTATIONS_TAIL.append({
    "name": "Check 444o: index.html の RAG 用の Licence: 行を 1.0 の本文へ戻す —— 版を述べるのにどの面にも読まれておらず、緑のままだった",
    "file": ROOT / "index.html",
    "find": "      Licence: https://yutapr0117-design.github.io/portfolio/LICENSES/",
    "replace": "      Licence: https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt (was LICENSES/",
})
_MUTATIONS_TAIL.append({
    "name": "Check 444o: agent-skills の index.json の licensing を 1.0 と述べる —— skill の description の版は誰も照合していなかった",
    "file": ROOT / ".well-known" / "agent-skills" / "index.json",
    "find": "licensing (ACD-",
    "replace": "licensing (ACD-1.0: was ACD-",
    "first_occurrence": True,
})
_MUTATIONS_TAIL.append({
    "name": "Check 499: 入口の最後に読んだ時刻を 2000-01-01 にする —— 取得のたびに書き換えないと、古い時刻のまま「返信は無い」と言い続ける",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "when last read, ",
    "replace": "when last read, 2000-01-01 00:00 UTC (was ",
})
_MUTATIONS_TAIL.append({
    "name": "Check 499: 入口の最後に読んだ時刻を、記録の無い先の日時にする —— 取得していない時刻を名乗っても、照合が無ければ通った",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "when last read, ",
    "replace": "when last read, 2099-01-01 00:00 UTC (was ",
})
_MUTATIONS_TAIL.append({
    "name": "Check 472f: 送る件名の名前の版だけを別の版にする —— 括弧の識別子しか比べず、名前の \"Dedication 1.0\" は照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "**Subject:** For Approval: Autonomous Commons Dedication ",
    "replace": "**Subject:** For Approval: Autonomous Commons Dedication 9",
})
_MUTATIONS_TAIL.append({
    "name": "Check 472j: ADOPTING が版で別の条を指す §1.3 を引く —— 番号が全部の版に在るかしか見ず、§1.3 が 1.0 では Dedicator、1.1 からは Work を定義していても通った",
    "file": ROOT / "LICENSES" / "ADOPTING.md",
    "find": "1. **Check that you hold the rights.**",
    "replace": "1. **Check that you hold the rights in the Work (§1.3).**",
})
_MUTATIONS_TAIL.append({
    "name": "Check 146: relatedProjectIds の 1 つを綴りの崩れた id (pO4) にする —— 全要素が pNN の配列しか拾わず、配列ごと参照から消えて dangling が 0 と出ていた",
    "file": ROOT / "js" / "store.js",
    "find": '["p02", "p03", "p04"], [], "task"',
    "replace": '["p02", "p03", "pO4"], [], "task"',
})
_MUTATIONS_TAIL.append({
    "name": "Check 472b: 版を示さずに 1.1 の語句 \"except by the Steward\" を引き、直前に §1.2 だけが在る —— 条番号の中の 1.2 を版の目印と読み、明示して引いたと数えていた",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-osd.md",
    "find": "preamble's first sentence is *\"Software and the works that surround it\"*, and the work the",
    "replace": "preamble's first sentence is *\"Software and the works that surround it\"*, §16.4 reads *\"except by the Steward\"*, and the work the",
})
_MUTATIONS_TAIL.append({
    "name": "Check 472b: 1.1 の語句を平の二重引用符で、版を示さずに引く —— 斜体の *\"…\"* しか読まず、アスタリスク無しの同じ引用が見えなかった",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission-osd.md",
    "find": "preamble's first sentence is *\"Software and the works that surround it\"*, and the work the",
    "replace": "preamble's first sentence is *\"Software and the works that surround it\"*, §16.4 reads \"except by the Steward\", and the work the",
})
_MUTATIONS_TAIL.append({
    "name": "Check 469: E12 の行の状態を「未着手（E3 は反映済み）」にする —— 行ごとに分類していたので、両方の語を持つ行は全 E-ID が both になり、E12 の未着手が矛盾の組から消えていた",
    "file": ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md",
    "find": "**E3 と同じ 1 文の前半** | **草案に反映済み** |",
    "replace": "**E3 と同じ 1 文の前半** | **未着手**（E3 は反映済み）|",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498: AS-OF の答えていない問いの件数だけを 1 件にする —— 件数は手で書き、状態の欄の件の数とは照合していなかった",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "| **0 件** | ACD への返信は",
    "replace": "| **1 件** | ACD への返信は",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498: AS-OF の答えていない問いに件を 1 つ足し、件数を 0 件のままにする —— 件を足して件数を直し忘れると、答えていない問いを 0 件と言い続けた",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "| **0 件** | ACD への返信は",
    "replace": "| **0 件** | **Q1** 2026-11-11・発言者・`rounds/README.md`・§2.1・未回答；ACD への返信は",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498: AS-OF の答えていない問いの件が、在らない rounds の file を指す —— 件数が合っていれば、受領文の置き場所は見ていなかった",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "| **0 件** | ACD への返信は",
    "replace": "| **1 件** | **Q1** 2026-11-11・発言者・`rounds/no-such-file.txt`・§2.1・未回答；ACD への返信は",
})
_MUTATIONS_TAIL.append({
    "name": "Check 498: AS-OF の答えていない問いの件が、私信の stub でない file を指して条を「—」で書く —— 最後の件が行の説明文まで伸び、説明文の § が件の § の代わりになっていた",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "| **0 件** | ACD への返信は",
    "replace": "| **1 件** | **Q1** 2026-11-11・発言者・`rounds/README.md`・—・未回答；ACD への返信は",
})
MUTATIONS = MUTATIONS_ARCHIVE6 + MUTATIONS_ARCHIVE5 + MUTATIONS_ARCHIVE4 + MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

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
