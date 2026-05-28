# Decision Record v78 — CodeQL Default Setup Compatible CI Recovery

Date: 2026-05-28
Status: Accepted
Context:
  CI had been failing since v75 due to GitHub Default Setup rejecting SARIF uploads
  from the custom CodeQL advanced workflow (.github/workflows/codeql.yml).
  The root cause and fix options were identified in v76–v77 (see
  decision-v76-v77-codeql-default-setup-conflict.md).

  Two resolution paths were available:
  (A) Human operator disables GitHub Default Setup in the UI → advanced workflow can SARIF-upload.
  (B) Remove .github/workflows/codeql.yml → Default Setup continues scanning autonomously.

Decision:
  Implement path (B): Delete .github/workflows/codeql.yml from the repository.
  This is the implementation-only path that does not require human UI interaction.

Rejected:
  Path (A) — Disabling Default Setup via GitHub UI is a human operator action outside
  repository file scope. Not implementable by an AI agent editing repository files only.

  Restoring codeql.yml with modified parameters — will not resolve SARIF rejection (v76/v77 confirmed).

Rationale:
  Path (B) restores CI green without requiring UI access.
  GitHub Default Setup continues to provide code scanning independently and automatically.
  Code coverage is maintained; only the custom configuration is removed.
  The CI failure is fully resolved by removing the conflicting workflow file.

Implementation:
  Deleted: .github/workflows/codeql.yml
  Added: this decision record to docs/incident-artifacts/

Operational Impact:
  CI should pass from this version onward (custom CodeQL workflow no longer runs).
  GitHub Default Setup continues scanning the repository on push/PR.
  SARIF upload conflict is eliminated.

Future Guidance for AI Agents:
  DO NOT re-add .github/workflows/codeql.yml while GitHub Default Setup is enabled.
  If advanced CodeQL configuration is desired in the future:
    1. Human operator disables Default Setup (GitHub UI: Settings → Security → Code scanning).
    2. AI agent may then restore or create a new codeql.yml.
  Attempting to add the workflow without step 1 will reproduce the same CI failure.

Not Possible (human action required if path A is desired):
  Disabling GitHub Default Setup via repository file editing is not supported.
  The UI toggle at Settings → Security → Code scanning requires authenticated human access.
