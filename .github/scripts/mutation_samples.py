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
    "name": "Check 143: paths の最後に \"!docs/evidence/**\" を足して digest 付きの evidence 3 file を外す —— 否定の形を読まず、literal と prefix/** だけを被覆と数えていた",
    "file": ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml",
    "find": "      - \"docs/incident-artifacts/**\"\n",
    "replace": "      - \"docs/incident-artifacts/**\"\n      - \"!docs/evidence/**\"\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 143: push の branches を main 以外 (release) にする —— paths だけを見て、main への push で発火するかは見ていなかった",
    "file": ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml",
    "find": "    branches: [\"main\"]\n    paths:\n",
    "replace": "    branches: [\"release\"]\n    paths:\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 374: importJSON から validateAndNormalize の呼び出しを消し、マージ結果をそのまま State.set する —— 本体の部分文字列で読み、コメントの「validateAndNormalize していた」で満たされていた",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                const normalized = Store.validateAndNormalize(merged);\n                State.set(normalized);",
    "replace": "                State.set(merged);",
})
_MUTATIONS_TAIL.append({
    "name": "Check 374: importJSON で validateAndNormalize を呼んで結果を捨て、マージ結果を State.set する —— 呼び出しの在否しか見ず、戻り値が State.set に渡るかを見ていなかった",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                const normalized = Store.validateAndNormalize(merged);\n                State.set(normalized);",
    "replace": "                Store.validateAndNormalize(merged);\n                State.set(merged);",
})
_MUTATIONS_TAIL.append({
    "name": "Check 367: インポートモードの select を二重引用符の h(\"select\" で書き、引用符つきの 'value': キーを付ける —— 一重引用符の h('select' しか読まず、二重引用符の形と引用符つきのキーは素通りしていた",
    "file": ROOT / "js" / "settings-page.js",
    "find": "h('select', { class: 'input', id: 'settingsImportMode', 'aria-label': 'インポートモード', onchange:",
    "replace": "h(\"select\", { class: 'input', 'value': settingsImportMode, id: 'settingsImportMode', 'aria-label': 'インポートモード', onchange:",
})
_MUTATIONS_TAIL.append({
    "name": "Check 394: UI の work の上限を 240 にし、行の後ろのコメントに古い式 (settings.work = clamp(x, 1, 180)) を残す —— 生のソースの最後の一致を層の値にしたので、コメントが本物の行を上書きしていた",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work, 1, 180);",
    "replace": "s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work, 1, 240); // was: settings.work = clamp(x, 1, 180)",
})
_MUTATIONS_TAIL.append({
    "name": "Check 410: TODO の入力の maxlength をコメントにする —— 生のソースを読み、コメントにした maxlength が保存側の上限と一致と数えていた",
    "file": ROOT / "js" / "apps.js",
    "find": "                        maxlength: CONSTANTS.LIMITS.TODO_TEXT,\n",
    "replace": "                        // maxlength: CONSTANTS.LIMITS.TODO_TEXT,\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 374: importJSON の State.set の前に、括弧の前に空白のある State.update (…) を足す —— 部分文字列 'State.update(' しか探さず、空白のある有効な呼び出しを見逃していた",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                State.set(normalized);",
    "replace": "                State.update (() => merged);\n                State.set(normalized);",
})
_MUTATIONS_TAIL.append({
    "name": "Check 370: UI の long の入力の fallback を 15 の直書きに戻す —— state.js / store.js しか見ず、pomodoro-page.js の || 25 / || 5 / || 15 は定数を変えても取り残された",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "|| CONSTANTS.POMODORO_DEFAULT_SETTINGS.long, 1, 120);",
    "replace": "|| 15, 1, 120);",
})
_MUTATIONS_TAIL.append({
    "name": "Check 370: store の既定の settings を別の値の直書き (work: 30) にする —— 今の値 (work: 25) の完全一致しか探さず、別の値の二重持ちは素通りしていた",
    "file": ROOT / "js" / "store.js",
    "find": "            settings: { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS },\n",
    "replace": "            settings: { work: 30, short: 5, long: 15 },\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 10: checks_tooling.py の docstring の r 接頭辞を外し、\\\\s を無効なエスケープに戻す —— ast.parse は通り、3.12 の SyntaxWarning (将来の SyntaxError) を見ていなかった",
    "file": ROOT / ".github" / "scripts" / "checks_tooling.py",
    "find": "        r\"\"\"frontmatter の 1 行の値 (行の中だけを読み、引用符を外す)。",
    "replace": "        \"\"\"frontmatter の 1 行の値 (行の中だけを読み、引用符を外す)。",
})
_MUTATIONS_TAIL.append({
    "name": "Check 162: .gitignore の node_modules/ の規則をコメントにする —— file 全体の部分文字列で探し、コメントにした規則も在ると数えていた",
    "file": ROOT / ".gitignore",
    "find": "\nnode_modules/\n",
    "replace": "\n# node_modules/\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 162: .gitignore で node_modules/ の直後に否定の !node_modules/ を足す —— 後の行の否定で打ち消された規則も在ると数えていた",
    "file": ROOT / ".gitignore",
    "find": "\nnode_modules/\n",
    "replace": "\nnode_modules/\n!node_modules/\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 468y: 逐条の §16.1 の行から試作の節 (§14.25・変えない) への言及を消す —— 試作の結論が逐条の行から辿れるかを手で揃えていた",
    "file": ROOT / "LICENSES" / "ACD-1.4-CLAUSE-REFERENCE-DRAFT.md",
    "find": "運ばない語として読んだうえで変えないとした（試作 §14.25",
    "replace": "運ばない語として読んだうえで変えないとした（試作 §14.2x",
})
_MUTATIONS_TAIL.append({
    "name": "Check 468z: 記述子の下書きの outOfScope[1] の note を草案に無い Section 11.9 にする —— 凍結した記述子は 451f が照合するが、確定の日までの下書きの表は照合の外だった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "No permission is granted under these rights (Section 11.4).",
    "replace": "No permission is granted under these rights (Section 11.9).",
})
_MUTATIONS_TAIL.append({
    "name": "Check 248: utf-8 の宣言の後に、属性が前に在る 2 つ目の宣言 <meta data-x=\"1\" charset=\"shift_jis\"> を足す —— <meta charset の直後しか読まず、最初の 1 つで満たされていた",
    "file": ROOT / "index.html",
    "find": "    <meta charset=\"utf-8\" />\n",
    "replace": "    <meta charset=\"utf-8\" />\n    <meta data-x=\"1\" charset=\"shift_jis\" />\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 248: http-equiv の Content-Type で shift_jis を宣言する —— <meta charset の形しか読まず、http-equiv の宣言は見えなかった",
    "file": ROOT / "index.html",
    "find": "    <meta charset=\"utf-8\" />\n",
    "replace": "    <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\" />\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 144: digest の道具の対応表で real-work-claims.md の値を別の file (ai-pioneer-identity-review.md) にする —— key だけを比べ、道具が別の file の digest を書く形を見ていなかった",
    "file": ROOT / ".github" / "scripts" / "update_aio_digests.py",
    "find": "    \"docs/evidence/real-work-claims.md\": ROOT / \"docs\" / \"evidence\" / \"real-work-claims.md\",",
    "replace": "    \"docs/evidence/real-work-claims.md\": ROOT / \"docs\" / \"evidence\" / \"ai-pioneer-identity-review.md\",",
})
_MUTATIONS_TAIL.append({
    "name": "Check 242: </main> の後に <svg/onload=\"alert(1)\"></svg> を足す —— 開始タグの文法が属性の前に空白を要求し、/ で区切った属性 (HTML の tokenizer は区切りとして読む) を列挙から落としていた",
    "file": ROOT / "index.html",
    "find": "        </main>\n",
    "replace": "        </main><svg/onload=\"alert(1)\"></svg>\n",
})
_MUTATIONS_TAIL.append({
    "name": "Check 151: a11y-axe の題名を、別の spec の題名と連結で同じになる形 ('…' + '…') にする —— 最初の閉じ引用符までを題名にし、連結の題名は前半だけで比べていた",
    "file": ROOT / "e2e" / "a11y-axe.spec.js",
    "find": "test('a11y axe: open command palette has no render-neutral critical violations', async",
    "replace": "test('WCAG 1.4.3: ライトの drawer / palette / ' + 'toast に color-contrast 違反がゼロ', async",
})
_MUTATIONS_TAIL.append({
    "name": "Check 481: checks_behavioral.py の helper の呼び出しを re.compile(r\"//[^\\n]*\").sub(…) に戻す —— re.sub( と // が 1 行に並ぶ形しか知らず、compile してから sub する形を見逃していた",
    "file": ROOT / ".github" / "scripts" / "checks_behavioral.py",
    "find": "_src406 = strip_js_comments(_uic406.read_text(encoding=\"utf-8\"))",
    "replace": "_src406 = re.compile(r\"//[^\\n]*\").sub(\"\", _uic406.read_text(encoding=\"utf-8\"))",
})
_MUTATIONS_TAIL.append({
    "name": "Check 481: checks_behavioral.py の helper の呼び出しを inline flag の re.sub(r\"(?m)//.*$\", …) に戻す —— (?m) の flag が前に付く形を見逃していた",
    "file": ROOT / ".github" / "scripts" / "checks_behavioral.py",
    "find": "_src406 = strip_js_comments(_uic406.read_text(encoding=\"utf-8\"))",
    "replace": "_src406 = re.sub(r\"(?m)//.*$\", \"\", _uic406.read_text(encoding=\"utf-8\"))",
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (a): face (w) の唯一の _bad460.append を pass にする —— コメント `# (w)` は残るので、旧版 (コメントで実装を数える) は"
            "検査が消えても緑だった (2026-11-12・監査 #145)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "                    _bad460.append(f\"(w) {_p460w.name}:{_n460w} が質問集を {_g.group(0)!r} と述べる / 実数 {_nq460w}\")",
    "replace": "                    pass",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (a): face (r) の entry を docstring から消す —— 別の face の説明の中の「(r) の §B.0 語数」が残るので、旧版 (区間のどこかの (x) を"
            "宣言と数える) は宣言が満たされたまま緑だった (2026-11-12・監査 #146)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "(r) **`submission.md` の外に書かれた §B.0 の語数 ↔",
    "replace": "**`submission.md` の外に書かれた §B.0 の語数 ↔",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 469 (b): E10 の errata の表の行を「未着手」にする —— E10 は別の行で both を受けているので {settled, pending, both} になり、"
            "旧版 (等号で比べる) は矛盾を見逃した (2026-11-12・監査 #147)",
    "file": ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md",
    "find": "| **1.1 で閉じた**（`ACD-1.1.machine.json` の `textRedistribution`",
    "replace": "| **未着手**（`ACD-1.1.machine.json` の `textRedistribution`",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 463b: 申請日の 1 枚の「利益相反」の事実を「—」にする —— 旧版は空文字列だけを空と数え、字の無い事実を事実ありとして通した"
            " (2026-11-12・監査 #37)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "| 利益相反 | 他者のライセンスの審査に意見したことがあるなら 1 行で開示（`REVISION-PROTOCOL.md` 規則 7）",
    "replace": "| 利益相反 | —",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 463b: 申請日の 1 枚の要件表の見出しを変える —— 旧版は file の全表の行を読むので、要件表を見失っても黙っていた (2026-11-12)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "| 項目 | 事実（`<版>` は確定した版） |",
    "replace": "| 要件 | 事実（`<版>` は確定した版） |",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 473b: docs/files/LICENSES/rounds/ の mirror (AI が書く散文) に否定済みの句を訂正の印なしで置く —— 旧版は path に"
            " rounds が在れば射程から外していた (2026-11-12・監査 #47)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "1999-2024-license-review-w3c-software-license-observed-1of7.txt.md",
    "find": "\n## What\n",
    "replace": "\n## What\n\nThe steward did not ask for it.\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 473c: REVISION-PROTOCOL.md の off-list correspondence の例外を「例外ではない」に逆転する —— 旧版は 2 語が在れば"
            "例外を述べたと数え、stub 5 件と逆の規則が並んでも緑だった (2026-11-12・監査 #43)",
    "file": ROOT / "LICENSES" / "REVISION-PROTOCOL.md",
    "find": "1. 受領全文が `rounds/` に無改変で入っている（**⚠ 第三者との private off-list correspondence は例外**",
    "replace": "1. 受領全文が `rounds/` に無改変で入っている（**⚠ 第三者との private off-list correspondence も例外ではない**",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 452: READY-TO-SUBMIT.md の接頭辞なしの参照を存在しない名前へ替える —— 旧版は LICENSES/ 等の接頭辞つきだけを導出し、"
            "本文の参照の大半 (接頭辞なし) を見なかった (2026-11-12・監査 #177)",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "`ACD-OSI-BOTTLENECKS.md` **B14**",
    "replace": "`ACD-OSI-BOTTLENECK.md` **B14**",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (h): docs/files/LICENSES/rounds/ の mirror にドシエの規模の数字を置く —— 旧版は mirror の最上段 (glob) だけを"
            "読み、rounds/ の mirror を見なかった (2026-11-12・監査 #133)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "1999-2024-license-review-w3c-software-license-observed-2of7.txt.md",
    "find": "\n## What\n",
    "replace": "\n## What\n\n不利な事実 144 件を数えた。\n",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (r): mirror の §B.0 と並ぶ語数から日付を外す —— 旧版は docs/files/LICENSES/ の mirror を読まなかった"
            " (2026-11-12・監査 #138)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "2026-08-26-license-discuss-sent.txt.md",
    "find": "だが 2026-08-26 に送ったのは 5,778 語で、",
    "replace": "だが送ったのは 5,778 語で、",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (s): file-size-budget.md に Check 463 の項目数を古い値で書く —— 旧版は LICENSES/ だけを読み、"
            "docs/architecture/ の「10 項目」(実装 16) を見なかった (2026-11-12・監査 #136)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "Check 463（送る文面が OSI の要求項目を含む・項目数は Check 463 の OK 行）",
    "replace": "Check 463（送る文面が OSI の要求 10 項目を含む）",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (w): 質問集の mirror が名前を書かずに述べる問数を変える —— 旧版は QUESTIONS-FOR-COUNSEL の語を持つ行だけを"
            "読み、mirror 自身の「尋ねたい 9 問」を読まなかった (2026-11-12・監査 #135)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "QUESTIONS-FOR-COUNSEL.md.md",
    "find": "尋ねたい 9 問を、",
    "replace": "尋ねたい 8 問を、",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 460 (w): 質問集を名指す行に「全8問」と書く —— 旧版は数の前に \\b を要求し、全 と 8 がどちらも語の文字なので"
            "数えなかった (2026-11-12・監査 #135)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "QUESTIONS-FOR-COUNSEL.md.md",
    "find": "**ACD を読む弁護士に尋ねたい 9 問を、",
    "replace": "**ACD を読む弁護士に尋ねたい `QUESTIONS-FOR-COUNSEL`（全8問）を、",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468r: §10.1 に「いまの状態」の語を足す (currently) —— 後で偽になる文を作用の条に書く T54 の型 (2026-11-12)",
    "file": CURRENT_DRAFT,
    "find": "       requirement upon You in respect of the Work.",
    "replace": "       requirement upon You in respect of the Work as currently drafted.",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 468r: §6.5 の除外の句を書き換える —— 句で持つ除外が条から消えたら、読み直しの合図として RED (2026-11-12)",
    "file": CURRENT_DRAFT,
    "find": "       proved ambiguous in practice, and because a permission that an automated",
    "replace": "       proved unclear in practice, and because a permission that an automated",
    "check": CHECK,
})
_MUTATIONS_TAIL.append({
    "name": "Check 472n: 申請日の 1 枚が引く草案の句 (§5.2 の \"that the Dedicator itself makes or makes available\") を草案から消す —— "
            "旧版の manifest は本文で確かめた引用の hash も残すので、草案が句を失っても引用を解決し続けた (2026-11-12)",
    "file": CURRENT_DRAFT,
    "find": "       the Work, that the Dedicator itself makes or makes available, or the",
    "replace": "       the Work, that the Dedicator itself makes or distributes, or the",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 453: ドシエの .md (ACD-1.0.comparison.md) を、いまの sha256 のまま FREEZE-DATA に足す —— 旧版は ACD-<版>.<英字> の形を"
            "全部通し、正しい手順で直せない file を増やせた (2026-11-12・監査 #182。その file が後で変わると旧版も sha の不一致で赤くなる)",
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": "b90a388803a628bf382455ac6350adf8d9e58fe7f381ae10155bd42c0b129e25  LICENSES/ACD-1.3.machine.json\n",
    "replace": "b90a388803a628bf382455ac6350adf8d9e58fe7f381ae10155bd42c0b129e25  LICENSES/ACD-1.3.machine.json\n581b22e37add8a3c7138bca22c534f38e1bb218aa4c4a322df09fb3d3c295e5d  LICENSES/ACD-1.0.comparison.md\n",
    "check": CHECK,
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
