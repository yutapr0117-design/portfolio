# Decision Record v75 — CodeQL Custom Workflow Introduction

Date: 2026-05-28
Status: Superseded by decision-v78-codeql-default-setup-compatible-ci-recovery.md
Context:
  CodeQL code scanning was not present in the repository workflow.
  A custom CodeQL advanced configuration workflow (.github/workflows/codeql.yml) was added
  to enable SAST scanning of JavaScript files in the portfolio.

Decision:
  Add .github/workflows/codeql.yml with CodeQL advanced setup for JavaScript analysis.

Rejected:
  Relying solely on GitHub's Default Setup — wanted full control over analysis configuration.

Rationale:
  CodeQL advanced setup allows customization of queries and analysis scope.
  The workflow was added in good faith without confirming whether GitHub Default Setup
  was already enabled on the repository.

Operational Impact:
  The custom workflow and GitHub Default Setup both attempted to upload SARIF to GitHub's
  code scanning API. GitHub rejects SARIF from advanced configurations when Default Setup
  is active, causing CI failures starting from this version.
  See decision-v76-v77-codeql-default-setup-conflict.md and
  decision-v78-codeql-default-setup-compatible-ci-recovery.md for resolution.

Lessons Learned for AI Agents:
  Before adding a custom CodeQL workflow, verify whether GitHub Default Setup is enabled
  on the repository (Settings → Security → Code scanning). If Default Setup is active,
  do NOT add .github/workflows/codeql.yml without first disabling Default Setup in the UI.
  Adding both will cause persistent CI failure regardless of workflow correctness.
