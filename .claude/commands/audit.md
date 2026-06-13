---
description: Repository-wide drift audit — invokes the repo-auditor sub-agent and reports back drift candidates without editing anything.
allowed-tools: Read, Glob, Grep, Bash(npm run check), Bash(python3 .github/scripts/*), Bash(sha256sum*), Bash(git log*), Bash(git status*)
---

リポジトリ全体の drift 監査を実行する。`repo-auditor` sub-agent を呼び、以下の dimension を読み取り専用で確認:

1. **C1〜C7 制約整合性** — `AI2AI.md` の canon と shipped 実装が一致するか
2. **Check 45 self-integrity** — `check_repository_consistency.py` の docstring inventory ↔ `# ── N.` section header ↔ map.md table の 3 者一致
3. **AIO published-layer drift (C6)** — `llms*` / `.well-known/*` / `aio-manifest.json` の digest 連鎖
4. **Stage 5 invariance** — `main.js` 1,086 行 ± 10 を逸脱していないか
5. **Last-Updated freshness** — `docs/architecture/*.md` の `Last-Updated:` が active increment window 内か
6. **CI workflow hygiene** — `.github/workflows/*.yml` 全ファイルに top-level `permissions:` (Check 67)

出力は Japanese・BLUF first・最大 30 行。drift 候補を 🟢 / 🟡 / 🔴 で分類して報告。

**編集はしない**。fix の判断はオーケストレーターに委ねる。
