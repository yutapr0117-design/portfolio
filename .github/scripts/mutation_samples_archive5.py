"""mutation_samples_archive5.py — rotate 先 (自動生成)。

rotate_mutation_samples.py が受け皿の余裕を実測して選び、埋まったら次を起こす。
**新しい mutation は mutation_samples.py の tail へ足すこと** (ここは退避先)。
"""
from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER  # noqa: F401 (entry 内で参照)

MUTATIONS_ARCHIVE5 = [
    {
    "name": 'Check 487: 週次 aio-monitoring.yml の git add から STATUS.md を外す —— 生成器が読むログだけを bot が commit し、STATUS.md のずれが次の無関係な PR の Check 121 で初めて赤くなる形',
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "              .well-known/agent-skills/index.json \\\n              STATUS.md\n",
    "replace": "              .well-known/agent-skills/index.json\n",
    "check": CHECK,
},
    {
    "name": 'Check 488: aio-monitoring.yml の job から timeout-minutes を外す —— 外部 API を待つ job が既定の 6 時間まで居座り、concurrency で翌週の run を塞ぐ',
    "file": ROOT / ".github" / "workflows" / "aio-monitoring.yml",
    "find": "    timeout-minutes: 15\n",
    "replace": "",
    "check": CHECK,
},
    {
    "name": 'Check 460 (w): REVIEWERS.md の質問集の問数を "Eight" へ戻す —— 11-01 に問 9 を足したあと、審査者向けの入口だけが 8 問と述べ続けていた形 (bb / 25 が発見)',
    "file": ROOT / "LICENSES" / "REVIEWERS.md",
    "find": "Nine questions on which",
    "replace": "Eight questions on which",
    "check": CHECK,
},
    {
    "name": 'Check 51b: update-playwright-snapshots の mirror に古い Playwright pin を現在形で書き戻す —— 2026-11-02 まで mirror 3 枚が 1.60.0 と述べ、pin は 1.64.1 だった',
    "file": ROOT / "docs" / "files" / ".github" / "workflows" / "update-playwright-snapshots.yml.md",
    "find": "Playwright の pin（`package.json` が権威・版数はここに書き写さない）を runbook と整合",
    "replace": "Playwright pin (1.60.0) を runbook と整合",
    "check": CHECK,
},
    {
    "name": 'Check 400: monolith の style.css の読み込みを素の read() へ戻す —— style.css が 1 つ欠けただけで traceback になり、全 Check が未実行のまま終わる (2026-11-02 に退避して実測)',
    "file": ROOT / ".github" / "scripts" / "check_repository_consistency.py",
    "find": 'style      = _read_core("style.css")',
    "replace": 'style      = read("style.css")',
    "check": CHECK,
},
    {
    "name": 'Check 437b: install の step timeout を文字列の env のまま渡す形へ戻す —— GitHub は template error を記録して timeout なしで走らせ、run は success なので誰にも見えない (2026-08-21〜11-02 の状態)',
    "file": ROOT / ".github" / "workflows" / "playwright-regression.yml",
    "find": "        timeout-minutes: ${{ fromJSON(env.INSTALL_TIMEOUT_MIN) }}\n",
    "replace": "        timeout-minutes: ${{ env.INSTALL_TIMEOUT_MIN }}\n",
    "check": CHECK,
},
]
