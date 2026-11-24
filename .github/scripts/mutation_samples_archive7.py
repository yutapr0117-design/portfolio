"""mutation_samples_archive7.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_CHANGES, CURRENT_DRAFT_VER, PREVIOUS_VER, FROZEN_PREVIOUS, APPLIED_ID, APPLIED_DATE, SUBMISSION_TARGET, NEXT_CHECK  # noqa: F401 (entry 内で参照)

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
    "find": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/" + APPLIED_ID + ".txt\"\n",
    "replace": "\"name\": \"Authoritative AI full context — Yuta Yokoi (横井雄太) canonical ground truth\"\n",
},
    {
    "name": "Check 444: Person.subjectOf の docs/evidence の DigitalDocument から license を外す —— DigitalDocument は _CW444 に無く、入れ子でもあったので見ていなかった",
    "file": ROOT / "index.html",
    "find": "\"url\": \"https://yutapr0117-design.github.io/portfolio/docs/evidence/ai-pioneer-identity-review.md\",\n                              \"license\": \"https://yutapr0117-design.github.io/portfolio/LICENSES/" + APPLIED_ID + ".txt\",\n",
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
    "name": "Check 70: runbook §9 の Check 総数の行の「最大番号」だけを別の数にする —— 行の最初の **N** しか読まず、同じ行が比べている性質を 2 度目に述べる数には読む者が無かった",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": "（最大番号 ",
    "replace": "（最大番号 1",
},
    {
    "name": "Check 468x: 1.5 の主表の T135 の行から「後の行で再改」の印を外す —— After の文は T146 の述べ直しで草案に無く、印が無ければ主表がいまの草案と違うことを言う",
    "file": CURRENT_CHANGES.with_name(f"ACD-{CURRENT_DRAFT_VER}-CHANGELIST.md"),
    # 2026-11-24: T146 で草案の文が変わったので、草案の側でなく主表の印を打つ (旧い形は After の文を草案から消していた)
    "find": "（後の行で再改 —— T146",
    "replace": "（T146",
},
    {
    "name": "Check 498: 「1.0 から何が変わったか」の下書きの版ごとの閉鎖数の 1.3 を 5 にする —— 使い捨ての計数で版の語の最初の一致を数え、閉鎖の印 (19 / 13 / 4) と違う数を書いた",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST-VERIFICATION.md",
    "find": "(19, 13 and 4)",
    "replace": "(19, 13 and 5)",
},
    {
    "name": "Check 498: 「1.0 から何が変わったか」の下書きの §2 の件数を 12 にする —— 節ごとの件数は errata の表の 2 列目から導けるのに、照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST-VERIFICATION.md",
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
    {
    "name": "Check 481: checks_behavioral.py の helper の呼び出しを re.compile(r\"//[^\\n]*\").sub(…) に戻す —— re.sub( と // が 1 行に並ぶ形しか知らず、compile してから sub する形を見逃していた",
    "file": ROOT / ".github" / "scripts" / "checks_behavioral.py",
    "find": "_src406 = strip_js_comments(_uic406.read_text(encoding=\"utf-8\"))",
    "replace": "_src406 = re.compile(r\"//[^\\n]*\").sub(\"\", _uic406.read_text(encoding=\"utf-8\"))",
},
    {
    "name": "Check 481: checks_behavioral.py の helper の呼び出しを inline flag の re.sub(r\"(?m)//.*$\", …) に戻す —— (?m) の flag が前に付く形を見逃していた",
    "file": ROOT / ".github" / "scripts" / "checks_behavioral.py",
    "find": "_src406 = strip_js_comments(_uic406.read_text(encoding=\"utf-8\"))",
    "replace": "_src406 = re.sub(r\"(?m)//.*$\", \"\", _uic406.read_text(encoding=\"utf-8\"))",
},
    {
    "name": "Check 469 (a): face (w) の唯一の _bad460.append を pass にする —— コメント `# (w)` は残るので、旧版 (コメントで実装を数える) は"
            "検査が消えても緑だった (2026-11-12・監査 #145)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "            _bad460.append(_msg460w)",
    "replace": "            pass",
    "check": CHECK,
},
    {
    "name": "Check 469 (a): face (r) の entry を docstring から消す —— 別の face の説明の中の「(r) の §B.0 語数」が残るので、旧版 (区間のどこかの (x) を"
            "宣言と数える) は宣言が満たされたまま緑だった (2026-11-12・監査 #146)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "(r) **`submission.md` の外に書かれた §B.0 の語数 ↔",
    "replace": "**`submission.md` の外に書かれた §B.0 の語数 ↔",
    "check": CHECK,
},
    {
    "name": "Check 469 (b): E10 の errata の表の行を「未着手」にする —— E10 は別の行で both を受けているので {settled, pending, both} になり、"
            "旧版 (等号で比べる) は矛盾を見逃した (2026-11-12・監査 #147)",
    "file": ROOT / "LICENSES" / "ACD-1.1-CHANGELIST.md",
    "find": "| **1.1 で閉じた**（`ACD-1.1.machine.json` の `textRedistribution`",
    "replace": "| **未着手**（`ACD-1.1.machine.json` の `textRedistribution`",
    "check": CHECK,
},
    {
    "name": "Check 463b: 申請日の 1 枚の「利益相反」の事実を「—」にする —— 旧版は空文字列だけを空と数え、字の無い事実を事実ありとして通した"
            " (2026-11-12・監査 #37)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "| 利益相反 | 他者のライセンスの審査に意見したことがあるなら 1 行で開示（`REVISION-PROTOCOL.md` 規則 7）",
    "replace": "| 利益相反 | —",
    "check": CHECK,
},
    {
    "name": "Check 463b: 申請日の 1 枚の要件表の見出しを変える —— 旧版は file の全表の行を読むので、要件表を見失っても黙っていた (2026-11-12)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "| 項目 | 事実（`<版>` は確定した版） |",
    "replace": "| 要件 | 事実（`<版>` は確定した版） |",
    "check": CHECK,
},
    {
    "name": "Check 473b: docs/files/LICENSES/rounds/ の mirror (AI が書く散文) に否定済みの句を訂正の印なしで置く —— 旧版は path に"
            " rounds が在れば射程から外していた (2026-11-12・監査 #47)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "1999-2024-license-review-w3c-software-license-observed-1of7.txt.md",
    "find": "\n## What\n",
    "replace": "\n## What\n\nThe steward did not ask for it.\n",
    "check": CHECK,
},
    {
    "name": "Check 473c: REVISION-PROTOCOL.md の off-list correspondence の例外を「例外ではない」に逆転する —— 旧版は 2 語が在れば"
            "例外を述べたと数え、stub 5 件と逆の規則が並んでも緑だった (2026-11-12・監査 #43)",
    "file": ROOT / "LICENSES" / "REVISION-PROTOCOL.md",
    "find": "1. 受領全文が `rounds/` に無改変で入っている（**⚠ 第三者との private off-list correspondence は例外**",
    "replace": "1. 受領全文が `rounds/` に無改変で入っている（**⚠ 第三者との private off-list correspondence も例外ではない**",
    "check": CHECK,
},
    {
    "name": "Check 452: READY-TO-SUBMIT.md の接頭辞なしの参照を存在しない名前へ替える —— 旧版は LICENSES/ 等の接頭辞つきだけを導出し、"
            "本文の参照の大半 (接頭辞なし) を見なかった (2026-11-12・監査 #177)",
    "file": ROOT / "LICENSES" / "READY-TO-SUBMIT.md",
    "find": "`ACD-OSI-BOTTLENECKS.md` **B14**",
    "replace": "`ACD-OSI-BOTTLENECK.md` **B14**",
    "check": CHECK,
},
    {
    "name": "Check 460 (h): docs/files/LICENSES/rounds/ の mirror にドシエの規模の数字を置く —— 旧版は mirror の最上段 (glob) だけを"
            "読み、rounds/ の mirror を見なかった (2026-11-12・監査 #133)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "1999-2024-license-review-w3c-software-license-observed-2of7.txt.md",
    "find": "\n## What\n",
    "replace": "\n## What\n\n不利な事実 144 件を数えた。\n",
    "check": CHECK,
},
    {
    "name": "Check 460 (r): mirror の §B.0 と並ぶ語数から日付を外す —— 旧版は docs/files/LICENSES/ の mirror を読まなかった"
            " (2026-11-12・監査 #138)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "rounds" / "2026-08-26-license-discuss-sent.txt.md",
    "find": "だが 2026-08-26 に送ったのは 5,778 語で、",
    "replace": "だが送ったのは 5,778 語で、",
    "check": CHECK,
},
    {
    "name": "Check 460 (s): file-size-budget.md に Check 463 の項目数を古い値で書く —— 旧版は LICENSES/ だけを読み、"
            "docs/architecture/ の「10 項目」(実装 16) を見なかった (2026-11-12・監査 #136)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "Check 463（送る文面が OSI の要求項目を含む・項目数は Check 463 の OK 行）",
    "replace": "Check 463（送る文面が OSI の要求 10 項目を含む）",
    "check": CHECK,
},
    {
    "name": "Check 460 (w): 質問集の mirror が名前を書かずに述べる問数を変える —— 旧版は QUESTIONS-FOR-COUNSEL の語を持つ行だけを"
            "読み、mirror 自身の「尋ねたい 9 問」を読まなかった (2026-11-12・監査 #135)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "QUESTIONS-FOR-COUNSEL.md.md",
    "find": "尋ねたい 10 問を、",
    "replace": "尋ねたい 9 問を、",
    "check": CHECK,
},
    {
    "name": "Check 460 (w): 質問集を名指す行に「全8問」と書く —— 旧版は数の前に \\b を要求し、全 と 8 がどちらも語の文字なので"
            "数えなかった (2026-11-12・監査 #135)",
    "file": ROOT / "docs" / "files" / "LICENSES" / "QUESTIONS-FOR-COUNSEL.md.md",
    "find": "**ACD を読む弁護士に尋ねたい 10 問を、",
    "replace": "**ACD を読む弁護士に尋ねたい `QUESTIONS-FOR-COUNSEL`（全8問）を、",
    "check": CHECK,
},
    {
    "name": "Check 468r: §4.1 に「いまの状態」の語を足す (today) —— 後で偽になる文を作用の条に書く T54 の型 (2026-11-12・1.5 の書き直しで §10.1 → §4.1)",
    "file": CURRENT_DRAFT,
    "find": "terminates or narrows, under this Dedication, for any reason",
    "replace": "terminates or narrows, under this Dedication today, for any reason",
    "check": CHECK,
},
    {
    "name": "Check 468r: §5.3 の除外の句を書き換える —— 句で持つ除外が条から消えたら、読み直しの合図として RED (2026-11-12・1.5 の書き直しで §6.4 → §5.3)",
    "file": CURRENT_DRAFT,
    "find": "formality, this Dedication is revocable or ineffective and, so far as the",
    "replace": "formality, this Dedication is revocable or ineffective and, as far as the",
    "check": CHECK,
},
    {
    "name": "Check 472n: 申請日の 1 枚が引く草案の句 (§5.2 の \"that the Dedicator itself makes or makes available\") を草案から消す —— "
    # 2026-11-24 (fc・ライセンスの mutation 256 件の全数の当て直しで MISSED): 1.4 の確定と提出対象の切り替えで前提が外れたので付け替えた
            "旧版の manifest は本文で確かめた引用の hash も残すので、草案が句を失っても引用を解決し続けた (2026-11-12)",
    "file": ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md",
    "find": "*\"that the Dedicator itself makes or makes available\"*",
    "replace": "*\"that the Dedicator itself makes or distributes\"*",
    "check": CHECK,
},
    {
    "name": "Check 453: ドシエの .md (ACD-1.0.comparison.md) を、いまの sha256 のまま FREEZE-DATA に足す —— 旧版は ACD-<版>.<英字> の形を"
            "全部通し、正しい手順で直せない file を増やせた (2026-11-12・監査 #182。その file が後で変わると旧版も sha の不一致で赤くなる)",
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": "b90a388803a628bf382455ac6350adf8d9e58fe7f381ae10155bd42c0b129e25  LICENSES/ACD-1.3.machine.json\n",
    "replace": "b90a388803a628bf382455ac6350adf8d9e58fe7f381ae10155bd42c0b129e25  LICENSES/ACD-1.3.machine.json\n581b22e37add8a3c7138bca22c534f38e1bb218aa4c4a322df09fb3d3c295e5d  LICENSES/ACD-1.0.comparison.md\n",
    "check": CHECK,
},
    {
    "name": "Check 450: 規範層の「権威テキスト」の「テ」を Cyrillic Supplement の字 (U+0501) へ —— 旧版は 1 スクリプト 1 ブロックで、"
            "主ブロックの外の字 (U+0501 / U+FE8D / U+FFA1) は日本語の語の中でも通った (2026-11-12・監査 #198)",
    "file": ROOT / "docs" / "architecture" / "repository-maintainability-map.md",
    "find": "\u6a29\u5a01\u30c6\u30ad\u30b9\u30c8",
    "replace": "\u6a29\u5a01\u0501\u30ad\u30b9\u30c8",
    "check": CHECK,
},
    {
    "name": "Check 468b: 変更の一覧の「A Result may result from the Work indirectly」を引用符の付いた本文に無い文へ —— 一覧が引く新しい文が本文に無くても、旧版は黙っていた (2026-11-12・portfolio-aa の提案)",
    # 2026-11-24 (T146): 一覧は本文を引かなくなった (効果の差を述べる) ので、草案の側でなく一覧の側に、本文に無い引用を入れる
    "file": CURRENT_CHANGES,
    "find": "A Result may result from the Work indirectly",
    "replace": "\"A Result may arise from the Work indirectly\"",
    "check": CHECK,
},
    {
    "name": "Check 468g: §4.2 の \"You need not\" を \"You will not\" にする —— You を主語にした will は義務に読まれうるが、旧版の型 (shall / must / You agree …) には無かった (1.5 の書き直しで §10.2 → §4.2)",
    "file": CURRENT_DRAFT,
    "find": "  4.2  In particular, You need not know of or accept this Dedication, give",
    "replace": "  4.2  In particular, You will not know of or accept this Dedication, give",
    "check": CHECK,
},
    {
    "name": "Check 471 (d): CHANGELIST の SELF-AUDIT の節の参照を存在しない §3zz にする —— 旧版は節番号の末尾の英字を 1 文字まで"
            "しか読まず、§3zz を参照として拾わずに黙って通した (2026-11-12・SELF-AUDIT が 3a〜3z を使い切った)",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "errata ではなく `ACD-1.1-SELF-AUDIT.md` §3z に記録した | −2",
    "replace": "errata ではなく `ACD-1.1-SELF-AUDIT.md` §3zz に記録した | −2",
    "check": CHECK,
},
    {
    "name": "Check 105: map から Check 7 の行を消す (7b / 7c の枝番の行は残る) —— 旧版は枝番を整数に丸めて集合を作り、7 の行が"
            "消えても集合が変わらず緑だった (2026-11-12・監査 #12)",
    "file": ROOT / "docs" / "architecture" / "check-repository-consistency-map.md",
    "find": "| 7 | index.html の CSP メタが inline suppressor スクリプトより前にある | BLOCKING |\n",
    "replace": "",
    "check": CHECK,
},
    {
    "name": "Check 105: Check 99 の check 呼び出しを消して見出しのコメントだけの区間にする —— 旧版は `# ── N.` の見出しがあれば"
            "実装と数え、Check 99 が何も検査しなくなっても 45 / 70 / 105 は 499 のまま緑だった (2026-11-12・監査 #13)",
    "file": ROOT / ".github" / "scripts" / "checks_docs_mirror.py",
    "find": "    check(\n        _inventory99.exists() and _template99.exists(),\n        \"Check 99: docs/files/README.md (inventory) と _template.md (5-軸 template) が両方存在\",\n        f\"Check 99: missing — README.md={_inventory99.exists()}, _template.md={_template99.exists()}\",\n    )\n",
    "replace": "    pass\n",
    "check": CHECK,
},
    {
    "name": "Check 22: Session Record #34 の見出しを #33 に打ち直す —— 旧版は <= で比べ、#33 が 2 つ・#34 が無いまま昇順として"
            "通った (2026-11-12・監査 #188)",
    "file": ROOT / "AI2AI.md",
    "find": "## [HANDOFF] Session Record #34",
    "replace": "## [HANDOFF] Session Record #33",
    "check": CHECK,
},
    {
    "name": "Check 468a: FAQ が「1.4 草案」として引く逐語を草案に無い語へ変える (agreed to make → agreed to remit) —— 旧版は errata の"
            "「N.M draft」しか見ず、ドシエの他の面の注記が後の試作で古くなっても黙っていた (2026-11-12・portfolio-00 の提案)",
    "file": ROOT / "LICENSES" / "ACD-1.0.faq.md",
    "find": "*\"a payment You agreed to make\"*",
    "replace": "*\"a payment You agreed to remit\"*",
    "check": CHECK,
},
    {
    "name": "Check 460 (x): B3 の見出しが述べる「いまの草案の題名からの語数」の先頭に 1 を足す —— 草案の長さを述べる外向きの行は、"
            "SUBMISSION-MATERIALS が「Check 468 が照合する」と書いていたのに誰も見ていなかった (2026-11-15)。anchor に数を含めないのは、"
            "草案を動かすたびに anchor が外れないため",
    "file": ROOT / "LICENSES" / "ACD-OSI-BOTTLENECKS.md",
    "find": f"（**確定した ACD-{PREVIOUS_VER} は題名から ",
    "replace": f"（**確定した ACD-{PREVIOUS_VER} は題名から 1",
    "check": CHECK,
},
    {
    "name": "Check 498 (h): READ-THREADS.txt から読了の行を 1 つ消す —— AS-OF の 3 つの数は和が合ったまま残り、旧版 (同じ文の中の"
            "算術だけ) は読了の一覧と AS-OF の食い違いを見なかった (2026-11-15・2f が気付き 50 が提案)",
    "file": ROOT / "LICENSES" / "READ-THREADS.txt",
    "find": "1999-04-24\tAPSL 1.1 certification...\n",
    "replace": "",
    "check": CHECK,
},
    {
    "name": "Check 498 (h): 2010 年以後に始まった会話の行を READ-THREADS.txt (2009 年まで) にも置く —— 読了の集合も件数も変わらない"
            "ので、年の照合が無ければ通り、record_read の重複の照合 (書く file の中だけ) もすり抜ける (2026-11-16・年で 2 つに分けたとき)",
    "file": ROOT / "LICENSES" / "READ-THREADS.txt",
    "find": "2009-12-08\tOKL4 license\n",
    "replace": "2009-12-08\tOKL4 license\n2010-01-19\tmove licenses to voluntarily retired list?\n",
    "check": CHECK,
},
    {
    "name": "Check 498 (h): 2010 年以後に始まった候補の会話の行を THREAD-CANDIDATES.txt (2009 年まで) にも置く —— 候補の集合も件数も"
            "変わらないので、年の照合が無ければ通る (2026-11-16・候補の一覧も年で分けたとき・50 の勧め)",
    "file": ROOT / "LICENSES" / "THREAD-CANDIDATES.txt",
    "find": "2009-12-08\tOKL4 license\n",
    "replace": "2009-12-08\tOKL4 license\n2010-01-19\tmove licenses to voluntarily retired list?\n",
    "check": CHECK,
},
    {
    "name": "Check 468d: 草案の §6 の \"makes no Reservation\" を \"makes a Reservation\" へ —— gap を担う条の中身が消える。468d に"
            "登録の mutation が 1 つも無かった (2026-11-16・目印を _lib_draft_markers へ移したときに気付いた)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "makes no Reservation",
    "replace": "makes a Reservation",
    "check": CHECK,
},
    {
    "name": "Check 468ab: 草案の §4.3 の \"Section 4.3 does not permit\" を \"This Section does not permit\" へ戻す —— 小項の中の \"this Section\" は §4 か §4.3 かで割れる (T84〜T88 で 5 → 0 にした型・2026-11-16・1.5 の書き直しで §8.4 → §4.3)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "Section 4.3 does not permit a person to impose what",
    "replace": "This Section does not permit a person to impose what",
    "check": CHECK,
},
    {
    "name": "Check 468ab: 草案の §8.2 の例外の列から 2.5 を外す —— §2.5 の約束 (権利を主張しない) の違反まで §8.2 が免責する形に戻る (T88 で閉じた問い 9 (a) の型・2026-11-16・1.5 の書き直しで §14.2 → §8.2)",
    "file": ROOT / "LICENSES" / f"ACD-{CURRENT_DRAFT_VER}-DRAFT.txt",
    "find": "            Section 2.5, 5.1, 5.2, or 5.3.",
    "replace": "            Section 5.1, 5.2, or 5.3.",
    "check": CHECK,
},
]
