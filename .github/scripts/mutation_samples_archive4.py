"""mutation_samples_archive4.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE4 = [
    {
    "name": "Check 413c: runbook §9 が引用する Check 108 の件数だけを古い値へ戻す —— 4 つの数 "
            "(総数 / source / mirror / 行末の合計) は 413/413b が守るが、同じ行の 5 つ目の数である"
            "**引用の中の数**は誰も見ていなかった (実測 2026-09-28: 284 と 636 を同時に主張していた)",
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    # anchor は件数そのものを含めない（件数は file 追加のたび動き anchor が orphan 化する）。
    # 数字の直前に "9" を差し込んで値を変える＝実測と必ず食い違う。
    "find": "OK メッセージ `all ",
    "replace": "OK メッセージ `all 9",
    "check": CHECK,
},
    {
    "name": "Check 469 (a): Check 460 の face 列挙から (d) を落とす —— 実装は 19 面のまま宣言だけ 18 面になる。"
            "列挙は減る側へ drift するので「増えたか」では検出できない (479 の凍結リストに残っていた)",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": "(d) FAQ mirror の件数、",
    "replace": "FAQ mirror の件数、",
    "check": CHECK,
},
    {
    "name": "Check 460: 読み先の FAQ を改名後の名前へずらす —— 改名を mirror と参照まで正しく直すと他の Check は"
            "全部緑になり、2026-11-01 まで本 Check だけが 19 面まるごと warning で skip していた",
    "file": ROOT / ".github" / "scripts" / "checks_license_self_reporting.py",
    "find": '_fq460 = _read460("ACD-1.0.faq.md")',
    "replace": '_fq460 = _read460("ACD-1.0.faq-renamed.md")',
    "check": CHECK,
},
    {
    "name": "Check 363: JS-LEAF-CEILING marker を消す —— 2026-11-01 まで BLOCKING の 1,000 行上限が"
            "warning 1 行を残して exit 0 のまま外れていた (兄弟の ESLINT / PERF marker は既に BLOCKING)",
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": "<!-- JS-LEAF-CEILING 1000 -->",
    "replace": "<!-- JS LEAF CEILING (removed) -->",
    "check": CHECK,
},
    {
    "name": "Check 468k (mirror / 「いまは」の言い回し): 1.1 の mirror に「いまは `ACD-1.3-DRAFT.txt`」を戻す —— "
            "2026-11-01 まで 468k は LICENSES/*.md の「いまの作業場は」しか見ておらず、同じ古さが 3 箇所残っていた",
    "file": ROOT / "docs" / "files" / "LICENSES" / "ACD-1.1.txt.md",
    "find": "以後の作業場は `FROZEN.md` 冒頭が権威。",
    "replace": "いまは `ACD-1.3-DRAFT.txt`。",
    "check": CHECK,
},
    {
    "name": "Check 468l: 草案の 2 行を語を変えずに 1 行へ繋いで 80 桁超にする —— 1.1〜1.3 はこの形で確定し、"
            "凍結で直せなくなった (2026-11-01 実測)",
    "file": CURRENT_DRAFT,
    # 語を足すと 468 の語数申告の face が先に拾い帰属が曖昧になる (初版で実測)。語を変えずに 2 行を
    # 1 行へ繋いで 80 桁を超えさせ、468l だけを狙う。
    "find": "in any medium and in any form,\n       including source code",
    "replace": "in any medium and in any form, including source code",
    "check": CHECK,
},
    {
    "name": "Check 468: 次版草案の題名行を前の版へ戻す (468j) —— 1.2 を複製した 1.3 草案で題名だけが "
            "7 日間 \"Version 1.2\" のまま残った実例 (2026-10-24)。語数は版数で変わらないので他の face は気付かない",
    "file": CURRENT_DRAFT,
    "find": f"                              Version {CURRENT_DRAFT_VER}\n",
    "replace": f"                              Version {PREVIOUS_VER}\n",
    "check": CHECK,
},
    {
    "name": "Check 468: 英語の入口が作業場を前の版の草案のまま名指す (468k) —— 2026-10-29 に 7 箇所が "
            "1.3 草案を指したままだった実例。語数・条数・題名は草案側の性質なので他の face は気付かない",
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": f"happens in [`{CURRENT_DRAFT.name}`]({CURRENT_DRAFT.name})",
    "replace": f"happens in [`ACD-{PREVIOUS_VER}-DRAFT.txt`](ACD-{PREVIOUS_VER}-DRAFT.txt)",
    "check": CHECK,
},
]
