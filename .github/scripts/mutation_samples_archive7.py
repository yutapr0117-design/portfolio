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
    "name": "Check 498: 「1.0 から何が変わったか」の下書きの §2 の件数を 11 にする —— 節ごとの件数は errata の表の 2 列目から導けるのに、照合していなかった",
    "file": ROOT / "LICENSES" / "ACD-1.4-CHANGELIST.md",
    "find": "§2 (scope and effect, 10)",
    "replace": "§2 (scope and effect, 11)",
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
]
