"""mutation_samples_archive7.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER, FROZEN_PREVIOUS, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, NEXT_CHECK  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE7 = [
    {
    "name": "Check 460: READY-TO-SUBMIT の散文に §B.0 の語数を裸で書き、日付は次の行の別の文にだけ在る —— 表の外は ±3 行の窓で日付を探し、隣の行の「2026-09-07 に同じ理由で書き換えた」を語数の日付と読んでいた",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "提出文（`submission.md` §B.0）も",
    "replace": "提出文（`submission.md` §B.0・900 語）も",
},
    {
    "name": "Check 444: TechArticle の encoding の llms-full.txt の MediaObject から license を外す —— 444b は @graph の直下しか歩かず、_CW444 が挙げる MediaObject は入れ子にしか無いので対象が 0 件だった",
    "file": ROOT / "index.html",
    "find": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.3.txt\"\n",
    "replace": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\"\n",
},
    {
    "name": "Check 444: Person.subjectOf の docs/evidence の DigitalDocument から license を外す —— DigitalDocument は _CW444 に無く、入れ子でもあったので見ていなかった",
    "file": ROOT / "index.html",
    "find": "\"url\": \"https://yutapr0117-design.github.io/portfolio/docs/evidence/ai-pioneer-identity-review.md\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.3.txt\",\n",
    "replace": "\"url\": \"https://yutapr0117-design.github.io/portfolio/docs/evidence/ai-pioneer-identity-review.md\",\n",
},
    {
    "name": "Check 145: step の先頭の `- uses:` の形で可変の tag (actions/checkout@v4) を足す —— 行の先頭の語が uses: のときしか読まず、`- uses:` は素通りしていた",
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "    steps:\n",
    "replace": "    steps:\n      - uses: actions/checkout@v4\n",
},
    {
    "name": "Check 145: docker:// の image を可変の tag (alpine:latest) で足す —— docker:// は理由の記述なく丸ごと除外され、digest で pin していない image も通した",
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "    steps:\n",
    "replace": "    steps:\n      - uses: docker://alpine:latest\n",
},
    {
    "name": "Check 366: GitHub のリンクの target を二重引用符で書き、rel を noopener だけにする —— `target: '_blank'` の完全一致しか数えず、\"_blank\" の行は走査から落ちていた",
    "file": ROOT / "js" / "components.js",
    "find": "h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }",
    "replace": "h('a', { href: profile.github, target: \"_blank\", rel: 'noopener' }",
},
    {
    "name": "Check 366: GitHub のリンクの rel を noopener だけにし、同じ行のコメントに noreferrer を書く —— 窓の中の noreferrer の綴りを探したので、コメントが rel の欠けを満たしていた",
    "file": ROOT / "js" / "components.js",
    "find": "h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }",
    "replace": "h('a', { href: profile.github, target: '_blank', rel: 'noopener' /* noreferrer */ }",
},
    {
    "name": "Check 468x: 主表の §5.2(d) の行から「後の行で再改」の印を外す —— 草案の文が後で変わったのに、主表の After がいまの草案に在るか・後の記録が在るかを照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "（**後の行で再改**: 「§5.2(d)（語順・T39）」の行で除外を (d) の冒頭へ移した）",
    "replace": "",
},
    {
    "name": "Check 70: runbook §9 の Check 総数の行の「最大番号」だけを別の数にする —— 行の最初の **N** しか読まず、同じ行が比べている性質を 2 度目に述べる数には読む者が無かった",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": "（最大番号 ",
    "replace": "（最大番号 1",
},
    {
    "name": "Check 468x: 主表が「足す」と述べた語句 (or for a payment You agreed to make) を草案から消す —— After は「へ」の引用しか読まず、「*\"…\"* を足す」の引用は照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-DRAFT.txt",
    "find": "       11.3), or for a payment You agreed to make.\n",
    "replace": "       11.3).\n",
},
    {
    "name": "Check 468x: 主表が §1.3 から「外す」と述べた語句 (in whole or in part) を §1.3 に戻す —— 「外す」の引用は照合しておらず、外したはずの語が条に残っても通った",
    "file": ROOT / "LICENSES" / "ACD-1.4-DRAFT.txt",
    "find": "  1.3  \"Work\" means the material to which the Dedicator has applied this\n",
    "replace": "  1.3  \"Work\" means the material, in whole or in part, to which the Dedicator has applied this\n",
},
    {
    "name": "Check 498: 「1.0 から何が変わったか」の下書きの版ごとの閉鎖数の 1.3 を 5 にする —— 使い捨ての計数で版の語の最初の一致を数え、閉鎖の印 (19 / 13 / 4) と違う数を書いた",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "(19, 13 and 4)",
    "replace": "(19, 13 and 5)",
},
    {
    "name": "Check 498: 「1.0 から何が変わったか」の下書きの §2 の件数を 12 にする —— 節ごとの件数は errata の表の 2 列目から導けるのに、照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "§2 (scope and effect, 11)",
    "replace": "§2 (scope and effect, 12)",
},
    {
    "name": "Check 478: 地図の 476 の行の「実装:」を分割前の module (checks_license_submission.py) にする —— 所在列しか読まず、説明の欄の「実装:」の形は照合していなかった (473 の行が実際にそうなっていた)",
    "file": ROOT / "docs" / "architecture" / "check-repository-consistency-map.md",
    "find": "\u3002\u5b9f\u88c5: `.github/scripts/checks_license_dossier.py`",
    "replace": "\u3002\u5b9f\u88c5: `.github/scripts/checks_license_submission.py`",
},
    {
    "name": "Check 78: aio-guardian の name を 2 語 (aio-guardian v2) にする —— 最初の語だけを取り、stem と一致と読んでいた",
    "file": ROOT / ".claude" / "agents" / "aio-guardian.md",
    "find": "\nname: aio-guardian\n",
    "replace": "\nname: aio-guardian v2\n",
},
    {
    "name": "Check 78: check-author の description を空にし、本文を別のキーへ移す —— \\s* が改行をまたぎ、空の description: が次の行のキーの字で満たされていた",
    "file": ROOT / ".claude" / "agents" / "check-author.md",
    "find": "\ndescription: Use this agent when the user (or another agent)",
    "replace": "\ndescription:\nnote: Use this agent when the user (or another agent)",
},
    {
    "name": "Check 143: paths の最後に \"!docs/evidence/**\" を足して digest 付きの evidence 3 file を外す —— 否定の形を読まず、literal と prefix/** だけを被覆と数えていた",
    "file": ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml",
    "find": "      - \"docs/incident-artifacts/**\"\n",
    "replace": "      - \"docs/incident-artifacts/**\"\n      - \"!docs/evidence/**\"\n",
},
    {
    "name": "Check 143: push の branches を main 以外 (release) にする —— paths だけを見て、main への push で発火するかは見ていなかった",
    "file": ROOT / ".github" / "workflows" / "auto-update-aio-digests.yml",
    "find": "    branches: [\"main\"]\n    paths:\n",
    "replace": "    branches: [\"release\"]\n    paths:\n",
},
    {
    "name": "Check 374: importJSON から validateAndNormalize の呼び出しを消し、マージ結果をそのまま State.set する —— 本体の部分文字列で読み、コメントの「validateAndNormalize していた」で満たされていた",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                const normalized = Store.validateAndNormalize(merged);\n                State.set(normalized);",
    "replace": "                State.set(merged);",
},
    {
    "name": "Check 374: importJSON で validateAndNormalize を呼んで結果を捨て、マージ結果を State.set する —— 呼び出しの在否しか見ず、戻り値が State.set に渡るかを見ていなかった",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                const normalized = Store.validateAndNormalize(merged);\n                State.set(normalized);",
    "replace": "                Store.validateAndNormalize(merged);\n                State.set(merged);",
},
    {
    "name": "Check 367: インポートモードの select を二重引用符の h(\"select\" で書き、引用符つきの 'value': キーを付ける —— 一重引用符の h('select' しか読まず、二重引用符の形と引用符つきのキーは素通りしていた",
    "file": ROOT / "js" / "settings-page.js",
    "find": "h('select', { class: 'input', id: 'settingsImportMode', 'aria-label': 'インポートモード', onchange:",
    "replace": "h(\"select\", { class: 'input', 'value': settingsImportMode, id: 'settingsImportMode', 'aria-label': 'インポートモード', onchange:",
},
    {
    "name": "Check 394: UI の work の上限を 240 にし、行の後ろのコメントに古い式 (settings.work = clamp(x, 1, 180)) を残す —— 生のソースの最後の一致を層の値にしたので、コメントが本物の行を上書きしていた",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work, 1, 180);",
    "replace": "s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || CONSTANTS.POMODORO_DEFAULT_SETTINGS.work, 1, 240); // was: settings.work = clamp(x, 1, 180)",
},
    {
    "name": "Check 410: TODO の入力の maxlength をコメントにする —— 生のソースを読み、コメントにした maxlength が保存側の上限と一致と数えていた",
    "file": ROOT / "js" / "apps.js",
    "find": "                        maxlength: CONSTANTS.LIMITS.TODO_TEXT,\n",
    "replace": "                        // maxlength: CONSTANTS.LIMITS.TODO_TEXT,\n",
},
    {
    "name": "Check 374: importJSON の State.set の前に、括弧の前に空白のある State.update (…) を足す —— 部分文字列 'State.update(' しか探さず、空白のある有効な呼び出しを見逃していた",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                State.set(normalized);",
    "replace": "                State.update (() => merged);\n                State.set(normalized);",
},
    {
    "name": "Check 370: UI の long の入力の fallback を 15 の直書きに戻す —— state.js / store.js しか見ず、pomodoro-page.js の || 25 / || 5 / || 15 は定数を変えても取り残された",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "|| CONSTANTS.POMODORO_DEFAULT_SETTINGS.long, 1, 120);",
    "replace": "|| 15, 1, 120);",
},
    {
    "name": "Check 370: store の既定の settings を別の値の直書き (work: 30) にする —— 今の値 (work: 25) の完全一致しか探さず、別の値の二重持ちは素通りしていた",
    "file": ROOT / "js" / "store.js",
    "find": "            settings: { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS },\n",
    "replace": "            settings: { work: 30, short: 5, long: 15 },\n",
},
    {
    "name": "Check 10: checks_tooling.py の docstring の r 接頭辞を外し、\\\\s を無効なエスケープに戻す —— ast.parse は通り、3.12 の SyntaxWarning (将来の SyntaxError) を見ていなかった",
    "file": ROOT / ".github" / "scripts" / "checks_tooling.py",
    "find": "        r\"\"\"frontmatter の 1 行の値 (行の中だけを読み、引用符を外す)。",
    "replace": "        \"\"\"frontmatter の 1 行の値 (行の中だけを読み、引用符を外す)。",
},
    {
    "name": "Check 162: .gitignore の node_modules/ の規則をコメントにする —— file 全体の部分文字列で探し、コメントにした規則も在ると数えていた",
    "file": ROOT / ".gitignore",
    "find": "\nnode_modules/\n",
    "replace": "\n# node_modules/\n",
},
    {
    "name": "Check 162: .gitignore で node_modules/ の直後に否定の !node_modules/ を足す —— 後の行の否定で打ち消された規則も在ると数えていた",
    "file": ROOT / ".gitignore",
    "find": "\nnode_modules/\n",
    "replace": "\nnode_modules/\n!node_modules/\n",
},
    {
    "name": "Check 468y: 逐条の §16.1 の行から試作の節 (§14.25・変えない) への言及を消す —— 試作の結論が逐条の行から辿れるかを手で揃えていた",
    "file": ROOT / "LICENSES" / "ACD-1.4-CLAUSE-REFERENCE-DRAFT.md",
    "find": "運ばない語として読んだうえで変えないとした（試作 §14.25",
    "replace": "運ばない語として読んだうえで変えないとした（試作 §14.2x",
},
    {
    "name": "Check 468z: 記述子の下書きの outOfScope[1] の note を草案に無い Section 11.9 にする —— 凍結した記述子は 451f が照合するが、確定の日までの下書きの表は照合の外だった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "No permission is granted under these rights (Section 11.4).",
    "replace": "No permission is granted under these rights (Section 11.9).",
},
    {
    "name": "Check 248: utf-8 の宣言の後に、属性が前に在る 2 つ目の宣言 <meta data-x=\"1\" charset=\"shift_jis\"> を足す —— <meta charset の直後しか読まず、最初の 1 つで満たされていた",
    "file": ROOT / "index.html",
    "find": "    <meta charset=\"utf-8\" />\n",
    "replace": "    <meta charset=\"utf-8\" />\n    <meta data-x=\"1\" charset=\"shift_jis\" />\n",
},
    {
    "name": "Check 248: http-equiv の Content-Type で shift_jis を宣言する —— <meta charset の形しか読まず、http-equiv の宣言は見えなかった",
    "file": ROOT / "index.html",
    "find": "    <meta charset=\"utf-8\" />\n",
    "replace": "    <meta charset=\"utf-8\" />\n    <meta http-equiv=\"Content-Type\" content=\"text/html; charset=shift_jis\" />\n",
},
    {
    "name": "Check 144: digest の道具の対応表で real-work-claims.md の値を別の file (ai-pioneer-identity-review.md) にする —— key だけを比べ、道具が別の file の digest を書く形を見ていなかった",
    "file": ROOT / ".github" / "scripts" / "update_aio_digests.py",
    "find": "    \"docs/evidence/real-work-claims.md\": ROOT / \"docs\" / \"evidence\" / \"real-work-claims.md\",",
    "replace": "    \"docs/evidence/real-work-claims.md\": ROOT / \"docs\" / \"evidence\" / \"ai-pioneer-identity-review.md\",",
},
    {
    "name": "Check 242: </main> の後に <svg/onload=\"alert(1)\"></svg> を足す —— 開始タグの文法が属性の前に空白を要求し、/ で区切った属性 (HTML の tokenizer は区切りとして読む) を列挙から落としていた",
    "file": ROOT / "index.html",
    "find": "        </main>\n",
    "replace": "        </main><svg/onload=\"alert(1)\"></svg>\n",
},
    {
    "name": "Check 151: a11y-axe の題名を、別の spec の題名と連結で同じになる形 ('…' + '…') にする —— 最初の閉じ引用符までを題名にし、連結の題名は前半だけで比べていた",
    "file": ROOT / "e2e" / "a11y-axe.spec.js",
    "find": "test('a11y axe: open command palette has no render-neutral critical violations', async",
    "replace": "test('WCAG 1.4.3: ライトの drawer / palette / ' + 'toast に color-contrast 違反がゼロ', async",
},
]
