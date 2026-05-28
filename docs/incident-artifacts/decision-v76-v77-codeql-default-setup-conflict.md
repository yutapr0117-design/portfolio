# Decision Record v76–v77 — CodeQL Default Setup Conflict Diagnosed

Date: 2026-05-28
Status: Resolved by decision-v78-codeql-default-setup-compatible-ci-recovery.md
Context:
  After adding the custom CodeQL workflow (v75), CI continued to fail with:
    "Code Scanning could not process the submitted SARIF file:
     CodeQL analyses from advanced configurations cannot be processed
     when the default setup is enabled"

  Initial attempts (v76, v77) attempted to fix the workflow by adjusting permissions,
  action versions (@v4), and analysis parameters. None resolved the root cause.

Decision:
  Continue investigation. Do not yet remove the custom workflow.

Rejected:
  Removing the workflow immediately — more information was gathered first.
  Disabling Default Setup via GitHub UI — this requires human operator action.

Rationale:
  The error message makes clear that CodeQL analysis itself SUCCEEDED.
  The failure is not a code scanning failure — it is a SARIF upload rejection.
  GitHub enforces mutual exclusivity: Default Setup and advanced configuration SARIF
  cannot coexist in the same repository at the same time.
  No changes to the YAML content can resolve this; it is a GitHub platform constraint.

Operational Impact:
  CI remained failing for v76 and v77. All other checks passed.

Root Cause Summary:
  GitHub CodeQL Default Setup was already enabled when the custom workflow was added (v75).
  The platform rejects SARIF uploads from advanced configurations when Default Setup is active.
  This is documented GitHub behavior, not a bug in the workflow file.

Lessons Learned for AI Agents:
  Do not attempt to fix CodeQL SARIF rejection by modifying the workflow YAML.
  The fix requires either:
  (A) Human operator disables Default Setup in GitHub UI → advanced workflow restored (preferred long-term).
  (B) Remove .github/workflows/codeql.yml → Default Setup continues scanning (implementation-only fix).
  Modifying action versions, permissions, or analysis parameters will NOT resolve SARIF upload rejection.
