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
    # 2026-09-27: §1.88 は `ACD-1.0.review-outcomes.md` へ主題で分離した (Check 365 の 1,000 行上限)。
    # **anchor は移動先を追う** —— 「解決する」だけでは正しい対象を打っている証拠にならない (#227 の class)。
    "file": ROOT / "LICENSES" / "ACD-1.0.review-outcomes.md",
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

_MUTATIONS_TAIL.append({
    "name": "Check 472f: 提出パケット §A.0 header の License URL 欄だけを別の版へずらす —— 版を切り替えた日に"
            "欄が 1 つ残ると、審査者には旧版の欄と新版の本文が届く (2026-09-26)",
    "file": ROOT / "LICENSES" / "ACD-1.0.submission.md",
    "find": "License URL:                    https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.0.txt",
    "replace": "License URL:                    https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.2.txt",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 471 (d): 短い名前の節参照を、分割で節が移る前の file 名へ戻す —— 旧実装は見出し辞書の"
            "フル名としか照合せず、短い名前の参照 (ドシエで普通の書き方) を全部読み飛ばしていた。"
            "移転漏れが 43 件たまっていた (2026-09-28)",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "`review-precedents.md` §1.46",
    "replace": "`comparison.md` §1.46",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 471 (d): リンク形式の節参照を、提出参考資料に無い §9 へ向ける —— 条番号への言及の例外を"
            "「の」でつないだ形に限らないと、ライセンスの節番号と同じ数字を持つ文書ではこの誤りを素通しする (2026-09-28)",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "(ACD-1.0.submission-reference.md) §1–§4",
    "replace": "(ACD-1.0.submission-reference.md) §9–§4",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468i: 草案の変更一覧から、errata が「1.2 草案で閉じた」とする E34 を外す —— 冒頭は一覧が"
            "差分のすべてだと宣言しているので、閉じた errata の記録漏れは草案の自己記述を偽にする (2026-09-28)",
    "file": ROOT / "LICENSES" / "ACD-1.2-DRAFT.txt",
    "find": "compression dropped (errata E34):",
    "replace": "compression dropped (errata):",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 473b: 否定済みの起草主体の句を、訂正の印なしで審査者向けの面へ戻す —— 2026-09-23 に steward 本人の"
            "手紙で覆った「ライセンスは頼まれていない」型の記述が、現在形の面に再び現れる形。2026-09-29 まで"
            "この Check を狙う mutation は 0 件だった (全件帰属掃引で判明)",
    "file": ROOT / "LICENSES" / "QUESTION-INDEX.md",
    "find": "`review-responses-meta.md` Q32d; `against.md` #62 |",
    "replace": "`review-responses-meta.md` Q32d; `against.md` #62 |\n\nThe owner did not commission it.",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 478: check-map の所在列を分割前の module へ戻す —— 468 の行が checks_license_dossier.py を"
            "指していた 2026-09-28 の実例そのもの。Check 105 は番号しか見ないので、所在の誤りは 478 だけが捕まえる",
    "file": ROOT / "docs" / "architecture" / "check-repository-consistency-map.md",
    "find": "| BLOCKING | `checks_license_draft.py` |",
    "replace": "| BLOCKING | `checks_license_dossier.py` |",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 479: 未検証 Check の既存リストから 1 件消す —— そのまま名指し 0 件の Check が「新規」として"
            "現れる形。ratchet が効いていることの非 vacuity (対象は checks_mutation_integrity.py なので"
            " mutation_samples.py の自己参照 trap に当たらない)",
    "file": ROOT / ".github" / "scripts" / "checks_mutation_integrity.py",
    "find": '_BASE479 = ("1,4-8,',
    "replace": '_BASE479 = ("4-8,',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 453: 凍結対象の pin を書き換える —— FROZEN.md の FREEZE-DATA の sha256 を 1 桁変える。凍結は「触らない」を記憶に委ねないための機械強制なので、pin と実体の食い違いは必ず止まらなければならない (2026-09-29 まで名指し 0 件)',
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": 'a9cdf425929af1afbf6b854204eea9df3199c8759bc05b411ab327c90932d00e  LICENSES/ACD-1.0.spdx.xml',
    "replace": 'b9cdf425929af1afbf6b854204eea9df3199c8759bc05b411ab327c90932d00e  LICENSES/ACD-1.0.spdx.xml',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 459: 索引から 1 file へのリンクを消す —— 到達できない文書は無いのと同じ。入口の README から落ちると、審査者も次のセッションもその file に辿り着かない (2026-09-29 まで名指し 0 件)',
    "file": ROOT / "LICENSES" / "README.md",
    "find": '[`ACD-1.0.dig-2026-09.md`](ACD-1.0.dig-2026-09.md)',
    "replace": 'dig',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 474: 不利な事実 register の状態トークンを語彙に無い値へ変える —— register は「潰すための backlog」として機械可読でなければならず、未知のトークンは集計から黙って落ちる (2026-09-29 まで名指し 0 件)',
    "file": ROOT / "LICENSES" / "ACD-1.0.against.md",
    "find": '| **[CLOSED]** **Corrected in place and mechanised.**',
    "replace": '| **[FIXED]** **Corrected in place and mechanised.**',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 475: AS-OF の反証表の行から状態の印を消す —— 反証表は「観測が来たら、まずここを見る」表で、状態と日付の無い行は、いつの読みかが分からなくなる (2026-09-29 まで名指し 0 件)',
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": '🟡 未充足（2026-09-25 確認・全数で再測定済み）',
    "replace": '未充足（2026-09-25 確認・全数で再測定済み）',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 409: consistency 側の mutation に e2e の `test` キーを混ぜる —— e2e probe では走らず "
            "consistency probe では恒久 SURVIVED になる登録ミスの形 (対象は archive なので自己参照 trap に当たらない)",
    "file": ROOT / ".github" / "scripts" / "mutation_samples_archive.py",
    "find": '        "name": "Check 45 (docstring↔section bijection): break a section-header number",',
    "replace": '        "test": "x",\n        "name": "Check 45 (docstring↔section bijection): break a section-header number",',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 410: notes editor の maxlength を外す —— 入力できる文字数と保存される文字数がずれ、"
            "超過分がリロードで黙って消える形 (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "js" / "apps.js",
    "find": "            maxlength: CONSTANTS.LIMITS.NOTES_TEXT,\n",
    "replace": "",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 420: e2e mutation の find が対象 file 内で 2 箇所になる —— probe は先頭 1 件しか置換しないので"
            "別の箇所を壊して silent SURVIVED になる形",
    "file": ROOT / "js" / "ai-page.js",
    "find": "                                'aria-label': 'AI アシスタントへの依頼を入力',\n",
    "replace": "                                'aria-label': 'AI アシスタントへの依頼を入力',\n"
               "                                'aria-label': 'AI アシスタントへの依頼を入力',\n",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 451c: 公開 manifest の ai_training_permitted を反転 —— 機械可読記述子と公開面が食い違い、"
            "agent が 1 回の fetch で受け取る許諾判定が偽になる形 (451a は凍結 file を触るので 453 と帰属が重なる・"
            "こちらを選んだ)",
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '    "ai_training_permitted": true,',
    "replace": '    "ai_training_permitted": false,',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 452: 提出準備マーカーの項数を 1 つずらす —— 「達した」という判断を別のテキストについて読ませる形",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "(16 節 / 82 項 / 597 行",
    "replace": "(16 節 / 81 項 / 597 行",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 479b: 失敗文言から番号を落とす —— probe がその Check を帰属できなくなる形 (2026-09-29 まで名指し 0 件)",
    "file": ROOT / ".github" / "scripts" / "checks_html.py",
    "find": "\"Check 8: index.html: X-Content-Type-Options meta present",
    "replace": "\"index.html: X-Content-Type-Options meta present",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 2: main.js の VERSION を 1 版ずらす (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "main.js",
    "find": "            VERSION:       'v74',",
    "replace": "            VERSION:       'v73',",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 3: mcp.json の server.version の major をずらす (2026-09-29 まで名指し 0 件)",
    "file": ROOT / ".well-known" / "mcp.json",
    "find": "    \"version\": \"74.0.0\",",
    "replace": "    \"version\": \"73.0.0\",",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 9: sitemap.xml を XML として壊す (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "sitemap.xml",
    "find": "<urlset xmlns=",
    "replace": "<urlset<< xmlns=",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 11: 要約 dict から enabled_engines キーを外す (同名変数は残る = 旧判定では緑だった形) (2026-09-29 まで名指し 0 件)",
    "file": ROOT / ".github" / "scripts" / "aio_monitoring.py",
    "find": "\"enabled_engines\": enabled_engines,",
    "replace": "\"enabled_enginesx\": enabled_engines,",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 19: sw.js の CACHE_NAME を旧版へ (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "sw.js",
    "find": "const CACHE_NAME = 'portfolio-aio-v74';",
    "replace": "const CACHE_NAME = 'portfolio-aio-v73';",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 20: og:image:alt を消す (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "index.html",
    "find": "<meta property=\"og:image:alt\" content=",
    "replace": "<meta property=\"og:image:altx\" content=",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 23: workflow YAML を parse 不能にする (2026-09-29 まで名指し 0 件)",
    "file": ROOT / ".github" / "workflows" / "mutation-probe.yml",
    "find": "name: Mutation Probe (safety-net self-check)",
    "replace": "name: [Mutation Probe (safety-net self-check)",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 25: 監視ログから evidence_policy キーを外す (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "docs" / "evidence" / "aio-monitoring-log.json",
    "find": "  \"evidence_policy\": {",
    "replace": "  \"evidence_policyx\": {",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 29: baseline 生成 workflow から PLAYWRIGHT_UPDATE_SNAPSHOTS を落とす (2026-09-29 まで名指し 0 件)",
    "file": ROOT / ".github" / "workflows" / "update-playwright-snapshots.yml",
    "find": "PLAYWRIGHT_UPDATE_SNAPSHOTS: \"1\"",
    "replace": "PLAYWRIGHT_UPDATE_SNAPSHOTX: \"1\"",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 35: robots.txt の Sitemap: を存在しない file へ (2026-09-29 まで名指し 0 件)",
    "file": ROOT / "robots.txt",
    "find": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml",
    "replace": "Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.txt",
    "check": CHECK,
})

MUTATIONS = MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。






















































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
