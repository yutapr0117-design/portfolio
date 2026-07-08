---
name: ChatGPT2ChatGPT.md
version: "2.0.0"
date: "2026-05-28"
sha256: "managed-externally-in-.well-known/aio-manifest.json"
document_type: "analysis-focused, model-agnostic AI-to-AI pipeline specification"
canonical_source: "AI2AI.md"
canonical_status: "NON-CANONICAL / SUBORDINATE TO AI2AI.md"
authority_tier: "Tier 4 — supporting_evidence"
owner: "Yuta Yokoi"
language: "ja-JP"
role: "analysis evidence / repository analysis pipeline"
paired_evidence:
  implementation_evidence: "Claude2Claude.md"
  analysis_evidence: "ChatGPT2ChatGPT.md"
primary_input_rule: "The received repository ZIP is always the primary source of truth."
scope:
  - "repository ZIP fixation"
  - "byte-level repository inventory"
  - "source text, binary, and metadata analysis"
  - "single-dimension analysis"
  - "full combination analysis matrix"
  - "AIO governance"
  - "machine-verifiable validation"
  - "remediation extraction"
  - "handoff preservation across AI agents"
external_normative_references:
  - title: "GitHub Docs — Downloading source code archives"
    purpose: "Source archives are snapshots, not full repository history."
    url: "https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives"
  - title: "GitHub Docs — Manually running a workflow"
    purpose: "workflow_dispatch creates manually runnable workflows."
    url: "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow"
  - title: "GitHub Docs — Skipping workflow runs"
    purpose: "[skip ci] can skip push/pull_request workflows and affect required checks."
    url: "https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs"
  - title: "GitHub Docs — GITHUB_TOKEN permissions"
    purpose: "GitHub Actions permissions must follow least privilege."
    url: "https://docs.github.com/en/actions/security-guides/automatic-token-authentication"
  - title: "MDN — TrustedTypePolicyFactory.createPolicy"
    purpose: "Trusted Types policy functions have distinct createHTML/createScript/createScriptURL semantics."
    url: "https://developer.mozilla.org/en-US/docs/Web/API/TrustedTypePolicyFactory/createPolicy"
  - title: "MDN — Response.headers"
    purpose: "Response.headers exposes the Headers object associated with a Response."
    url: "https://developer.mozilla.org/en-US/docs/Web/API/Response/headers"
  - title: "MDN — CSP frame-ancestors"
    purpose: "frame-ancestors is not supported in a meta element."
    url: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors"
  - title: "Playwright Docs — Visual comparisons"
    purpose: "toHaveScreenshot creates/uses reference screenshots."
    url: "https://playwright.dev/docs/test-snapshots"
  - title: "sitemaps.org — Sitemap Protocol"
    purpose: "Sitemap XML URL and host constraints."
    url: "https://www.sitemaps.org/protocol.html"
  - title: "RFC 9309 — Robots Exclusion Protocol"
    purpose: "robots.txt is a crawler rule protocol, not access authorization."
    url: "https://www.rfc-editor.org/rfc/rfc9309"
  - title: "NIST FIPS 180-4 — Secure Hash Standard"
    purpose: "SHA-256 digest terminology and role."
    url: "https://csrc.nist.gov/pubs/fips/180-4/upd1/final"
---
> **CANONICAL HIERARCHY NOTE:**
> `AI2AI.md` is the **canonical** handoff document.
> This file (`ChatGPT2ChatGPT.md`) is **supporting evidence only** — non-canonical and subordinate to `AI2AI.md`.
> If this file conflicts with `AI2AI.md` or `llms-full.txt`, **AI2AI.md and llms-full.txt win**.


# ChatGPT2ChatGPT.md

## 0. Executive Summary

`ChatGPT2ChatGPT.md` is an **analysis evidence file** and a **model-agnostic repository analysis pipeline**.

It is not implementation code.
It is not a canonical handoff.
It is not allowed to override `AI2AI.md`.

The intended authority model is:

```text
AI2AI.md           = canonical operational handoff / Tier 1
Claude2Claude.md  = implementation evidence / Tier 4 supporting_evidence
ChatGPT2ChatGPT.md = analysis evidence / Tier 4 supporting_evidence
```

`Claude2Claude.md` and `ChatGPT2ChatGPT.md` are peers.
They exist to preserve evidence that this repository is maintained through AI-only implementation and AI-assisted analysis.
Both remain subordinate to `AI2AI.md`.

This document preserves the analysis protocol accumulated through repeated repository ZIP analysis: ZIP fixation, byte-level inventory, source and binary inspection, metadata extraction, AIO authority mapping, CI safety review, Service Worker review, runtime guard review, evidence routing, and full combination analysis.

The received repository ZIP is always the primary source of truth.  
Past chats, prior ZIPs, previous summaries, external AI reports, and this file are secondary unless they match the current ZIP.

---

## 1. Authority and Conflict Resolution

### 1.1 Authority Tiers

Use this hierarchy when interpreting repository files:

```text
Tier 0 — Semantic Ground Truth
  llms-full.txt
  Purpose: public semantic identity, AIO context, entity disambiguation, portfolio meaning.

Tier 1 — Operational Canon
  AI2AI.md
  Purpose: canonical model-agnostic handoff, execution rules, delivery rules, prohibition rules.

Tier 2 — Short AI Entry
  llms.txt
  .well-known/llms.txt
  Purpose: short AI routing and summary context.

Tier 3 — Machine-Readable Discovery
  .well-known/aio-manifest.json
  .well-known/mcp.json
  .well-known/api-catalog
  .well-known/index.json
  .well-known/agent-skills/index.json

Tier 4 — Supporting Evidence
  Claude2Claude.md
  ChatGPT2ChatGPT.md
  docs/evidence/ai-pioneer-identity-review.md

Tier 4b — Observational Evidence
  docs/evidence/aio-monitoring-log.json
  Other machine-generated monitoring or citation logs.

Tier 5 — Incident Artifacts
  docs/incident-artifacts/*
```

### 1.2 Conflict Rules

1. The current ZIP wins over all previous ZIPs and external reports.
2. `AI2AI.md` wins for execution and delivery rules.
3. `llms-full.txt` wins for public semantic identity.
4. `Claude2Claude.md` and `ChatGPT2ChatGPT.md` must never overrule `AI2AI.md`.
5. `ChatGPT2ChatGPT.md` may define analysis defaults, but only under the operational limits of `AI2AI.md`.
6. Incident artifacts are read-only evidence; they must not be reactivated.
7. External normative references clarify platform behavior, but repository reality must still be verified from the current ZIP.

---

## 2. Repository Intake Protocol

### 2.1 ZIP Fixation

Every analysis begins by fixing the exact received ZIP.

Record:

```text
zip_filename
zip_sha256
zip_size_bytes
zip_entry_count
zip_file_count
expanded_total_bytes
zip_comment
root_directory
path_traversal_result
zip_test_result
```

Rules:

- Do not rely on filename semantics.
- Do not infer that identical filenames imply identical content.
- Do not infer that different filenames imply different content.
- Use SHA-256 and extracted contents.
- Do not rely on previously extracted directories.
- Use a new extraction directory per ZIP.
- Treat GitHub source archives as snapshots of branch/tag/commit contents, not full repository history.
- If the user says the ZIP is the latest commit, accept it as the latest supplied primary source; do not speculate otherwise.

### 2.2 Byte-Level Inventory

Generate an inventory containing:

```text
relative_path
size_bytes
sha256
crc32_if_from_zip
compression_size_if_from_zip
file_type_guess
text_or_binary
utf8_decode_result
line_ending_profile_for_text
```

Do this for all files, including:

```text
HTML
CSS
JS
JSON
YAML
XML
Markdown
robots.txt
sitemap.xml
.well-known files
GitHub Actions workflows
Python scripts
WebP
MP3
verification files
incident artifacts
monitoring logs
```

"One byte missed" is a failure mode. The analysis must include both visible text and binary metadata layers.

---

## 3. Single-Dimension Analysis Heuristics

All heuristics in this section must be run independently before combination analysis.

### H01 — ZIP Primary Source

The current repository ZIP is the primary source.  
Previous results are reusable only as analysis heuristics, not as current facts.

### H02 — No Line-Number Dependency

Do not write instructions that depend on exact line numbers.  
Use path, section name, key name, semantic block name, or unique phrase instead.

### H03 — Parse Before Meaning

Before interpreting meaning, run structural validation:

```text
JSON parse
YAML parse
XML parse
JSON-LD parse
Python py_compile
inline JS extraction and node --check
aio-guard.js node --check
sw.js node --check
```

If structure fails, semantic interpretation is secondary.

### H04 — JSON/YAML/XML/JSON-LD

Validate:

```text
*.json
.well-known/api-catalog
.eslintrc.json
.stylelintrc.json
.github/workflows/*.yml
docs/incident-artifacts/*.yml
sitemap.xml
index.html application/ld+json blocks
```

Do not parse `application/ld+json` or `speculationrules` blocks as normal JavaScript.

### H05 — AI2AI Canon

`AI2AI.md` must remain the single canonical operational handoff.  
Any change that weakens this is blocking.

### H06 — Claude2Claude / ChatGPT2ChatGPT Peer Evidence

`Claude2Claude.md` and `ChatGPT2ChatGPT.md` are equal Tier 4 supporting evidence:

```text
Claude2Claude.md:
  implementation evidence
  tool-specific adapter note
  non-canonical

ChatGPT2ChatGPT.md:
  analysis evidence
  model-agnostic analysis pipeline
  non-canonical
```

Neither is source_of_truth.  
Neither belongs in `.well-known/index.json` or `.well-known/agent-skills/index.json`.

### H07 — Manifest Category Separation

`.well-known/aio-manifest.json` must separate:

```text
source_of_truth:
  canonical AIO source files and binary assets

supporting_evidence:
  Claude2Claude.md
  ChatGPT2ChatGPT.md
  docs/evidence/ai-pioneer-identity-review.md

observational_evidence:
  docs/evidence/aio-monitoring-log.json
  machine-generated monitoring logs
```

If the implementation does not support `observational_evidence`, either:

1. extend the digest scripts to handle it, or
2. place monitoring logs under `supporting_evidence` with a clear `role`.

Do not mix canonical and non-canonical evidence.

### H08 — Digest Governance

When any tracked file changes, update all digest-bearing surfaces:

```text
.well-known/index.json
.well-known/agent-skills/index.json
.well-known/aio-manifest.json
.github/scripts/check_aio_digests.py
.github/scripts/update_aio_digests.py
```

`update_aio_digests.py` must remain idempotent.  
It must not rewrite files merely because time advanced.

### H09 — Byte Identity

Maintain byte identity:

```text
llms.txt == .well-known/llms.txt
.well-known/index.json == .well-known/agent-skills/index.json
```

### H10 — Discovery Mesh

Every important AIO/evidence file must be discoverable through the appropriate mesh:

```text
llms-full.txt
llms.txt
AI2AI.md
Claude2Claude.md
ChatGPT2ChatGPT.md
docs/evidence/ai-pioneer-identity-review.md
docs/evidence/aio-monitoring-log.json
.well-known/aio-manifest.json
.well-known/mcp.json
.well-known/api-catalog
robots.txt
sitemap.xml
index.html
```

Supporting evidence should be discoverable but not canonical.

### H11 — JSON-LD Evidence Linking

If an evidence document supports a claim, connect it through structured data where appropriate.

Use `DigitalDocument` or an equivalent structured-data node for:

```text
docs/evidence/ai-pioneer-identity-review.md
ChatGPT2ChatGPT.md
Claude2Claude.md
```

The claim must remain observational, not an absolute proof of nonexistence.

### H12 — Google Search Console Verification File

`googlea7059bedc6fe8bdc.html` is an ownership verification token file only.

Do not turn it into an AIO entity declaration.

AIO entity context belongs in:

```text
llms-full.txt
llms.txt
index.html
JSON-LD
WebP XMP
MP3 ID3
.well-known/aio-manifest.json
AI2AI.md
```

### H13 — GitHub Actions Incident Separation

Current `.github/workflows/` files are active workflows.  
Archived experimental workflows belong only under `docs/incident-artifacts/`.

Never move incident artifacts back into `.github/workflows/`.

If an archived artifact contains `workflow_dispatch`, treat that as safe only because it is outside `.github/workflows/`.

### H14 — workflow_dispatch Safety

A workflow with `workflow_dispatch` can be run manually when placed under `.github/workflows/`.  
Therefore archived workflows containing `workflow_dispatch` must remain outside live workflow paths.

### H15 — `[skip ci]` Risk

`[skip ci]` may skip `push` / `pull_request` workflows and may affect required checks.  
If used, it must be:

```text
limited
documented
scoped to digest-only automation
reviewed for branch protection effects
```

### H16 — GitHub Actions Permissions

Default to least privilege.

Acceptable pattern:

```yaml
permissions:
  contents: read
```

Only jobs that commit back or create issues may use:

```yaml
permissions:
  contents: write
  issues: write
```

### H17 — AIO Monitoring

If monitoring is present:

```text
.github/scripts/aio_monitoring.py
.github/workflows/aio-monitoring.yml
docs/evidence/aio-monitoring-log.json
```

then classify monitoring logs as non-canonical observational evidence.

If no API keys/secrets are configured, decide whether monitoring is:

```text
strict required:
  exit 1 when not configured

optional observational:
  write skipped status and exit 0
```

The choice must be documented in `AI2AI.md` or `SECURITY.md`.

### H18 — Service Worker Scope

`sw.js` must preserve:

```text
static files as primary AIO delivery
Service Worker as browser-context enhancement only
exact-match AIO file handling
Response.headers cloning when generating new Response objects
```

Do not broaden interception scope without explicit justification.

### H19 — DOM Sink Safety

`innerHTML` fallback must fail closed.  
Raw HTML must not be passed through on parser failure.

Trusted Types pass-through for script/scriptURL must not be described as sanitizer behavior.

### H20 — CSP Meta Limitation

Do not add `frame-ancestors` to a `<meta http-equiv="Content-Security-Policy">` tag.  
It belongs to HTTP response headers, not meta CSP.

### H21 — Runtime Guard Governance

Prototype hooks and runtime guards must be reviewed as high-risk deliberate controls.

Check:

```text
Element.prototype.innerHTML
EventTarget.prototype.addEventListener
CSSStyleDeclaration.prototype.setProperty
Element.prototype.setAttribute
startViewTransition proxy
aio-guard.js
aio-asset-anchor
semantic drift guard
media lifecycle guard
IntersectionObserver usage
```

### H22 — localStorage Schema

Keys such as `portfolio_enhanced_v45` and `portfolio_brand_v45` are schema keys, not content version identifiers.

Do not rename them merely because version changes.  
If renaming is necessary, add migration logic.

### H23 — Binary AIO Integrity

Inspect both binary files and metadata:

```text
WebP:
  RIFF / WEBP magic
  VP8X / VP8 / XMP chunks
  XMP contains AIO entity context

MP3:
  ID3v2.4
  TXXX / COMM frames
  AIO entity context
  paired image reference
```

Do not treat image/audio files as opaque blobs.

### H24 — .gitattributes Binary Protection

Binary AIO assets must remain protected from text normalization.

### H25 — Playwright Baseline Truthfulness

If Playwright screenshot tests exist but baseline screenshots are missing, report:

```text
blocked
```

not pass.

### H26 — Stylelint Severity Semantics

Differentiate:

```text
wrapper step = advisory or blocking
severity:error = blocking if configured so
severity:warning = advisory
fatal/config issue = explicitly categorized
```

Do not mix labels.

### H27 — Delivery Truthfulness

Never claim a test ran if it did not.  
Use:

```text
pass
fail
warn
blocked
not_applicable
```

### H28 — Full Repository Read Scope

Analysis must include:

```text
source code
configuration
Markdown
well-known files
robots
sitemap
CI workflows
CI scripts
verification files
incident artifacts
evidence logs
binary files
binary metadata
```

No file category is outside scope unless explicitly declared.

---

## 4. Combination Analysis Matrix

This is the default analysis mode.

Run all pairwise and higher-order combinations below.  
Do not reduce the analysis to isolated checks.

### 4.1 Pairwise Combinations

| ID | Combination | Required Decision |
|---|---|---|
| P01 | ZIP fixation × source archive snapshot semantics | Whether the current ZIP is properly fixed as the primary source |
| P02 | AI2AI.md × authority tiers | Whether canonical operational authority remains intact |
| P03 | Claude2Claude.md × ChatGPT2ChatGPT.md | Whether both are peer supporting evidence, not competing canons |
| P04 | ChatGPT2ChatGPT.md × aio-manifest | Whether analysis evidence is added only to supporting_evidence |
| P05 | ChatGPT2ChatGPT.md × digest scripts | Whether check/update mappings include the file |
| P06 | ChatGPT2ChatGPT.md × mcp/api-catalog | Whether discovery exists without making it canonical |
| P07 | ChatGPT2ChatGPT.md × robots/sitemap | Whether crawler discovery exists |
| P08 | llms.txt × .well-known/llms.txt | Whether byte identity holds |
| P09 | .well-known/index × agent-skills | Whether byte identity holds |
| P10 | AI2AI.md × Google verification file | Whether verification file is token-only and not AIO declaration |
| P11 | README × llms-full × workflows | Whether active workflows and incident artifacts are correctly separated |
| P12 | AIO monitoring log × manifest | Whether monitoring is classified as observational evidence |
| P13 | AIO monitoring workflow × permissions | Whether write/issue permissions are scoped and justified |
| P14 | auto-update digests × evidence paths | Whether all tracked evidence files trigger digest update when changed |
| P15 | skip ci × branch protection risk | Whether `[skip ci]` is controlled and documented |
| P16 | Service Worker × headers | Whether response headers are cloned and preserved |
| P17 | Service Worker × exact match | Whether interception scope remains constrained |
| P18 | innerHTML hook × Trusted Types | Whether DOM sink safety and security claims match |
| P19 | meta CSP × frame-ancestors | Whether unsupported meta CSP directives are avoided |
| P20 | prototype hooks × documentation | Whether high-risk runtime controls remain documented |
| P21 | localStorage keys × migration | Whether schema keys are preserved or migrated safely |
| P22 | WebP/MP3 × binary metadata CI | Whether binary AIO metadata is both present and protected |
| P23 | Playwright workflow × baseline assets | Whether visual tests are pass/block truthfully |
| P24 | Stylelint script × workflow labels | Whether advisory/blocking labels match behavior |
| P25 | JSON-LD × evidence documents | Whether structured data points to evidence without overclaiming |
| P26 | robots × sitemap × project path | Whether discovery paths are consistent under `/portfolio/` |
| P27 | incident artifacts × workflow_dispatch | Whether archived workflows cannot run accidentally |
| P28 | SECURITY.md × monitoring workflow | Whether security and monitoring behavior are consistent |
| P29 | AI2AI.md × delivery rules | Whether changed-files-only delivery remains enforced |
| P30 | ChatGPT2ChatGPT.md × analysis reproducibility | Whether this file preserves enough method for another AI to repeat the analysis |

### 4.2 Higher-Order Combinations

| ID | Combination | Required Decision |
|---|---|---|
| C01 | ZIP × inventory × digest × manifest | Whether repository identity and AIO integrity are verifiable |
| C02 | AI2AI × Claude2Claude × ChatGPT2ChatGPT | Whether canon/evidence roles are non-conflicting |
| C03 | source_of_truth × supporting_evidence × observational_evidence | Whether manifest taxonomy is clean |
| C04 | README × llms-full × AI2AI × index.html | Whether human and AI entry documents describe the same reality |
| C05 | robots × sitemap × mcp × api-catalog × aio-manifest | Whether AI discovery mesh is complete |
| C06 | JS syntax × DOM sink × Trusted Types × CSP | Whether browser safety story is coherent |
| C07 | SW × cache/BOM × headers × static AIO delivery | Whether browser enhancement does not become primary AIO dependency |
| C08 | WebP × MP3 × .gitattributes × binary CI | Whether binary AIO survives repository operations |
| C09 | GitHub Actions permissions × skip ci × workflow_dispatch × incident artifacts | Whether CI cannot accidentally re-enable archived failure modes |
| C10 | auto-update digest × monitoring log × evidence files × commit loop risk | Whether automation can update evidence without infinite loops |
| C11 | Playwright × baseline × visual regression claims | Whether UI regression claims are truthful |
| C12 | evidence doc × pioneer claim × JSON-LD × llms-full | Whether public claims remain observational and verifiable |
| C13 | AIO monitoring × evidence hierarchy × SECURITY.md | Whether monitoring is safe, non-canonical, and documented |
| C14 | localStorage × versioning × semantic drift guard | Whether version changes do not break persisted user state |
| C15 | all source files × all binary files × all metadata | Whether no file category is unexamined |

### 4.3 Status Vocabulary

Use only:

```text
pass
fail
warn
blocked
not_applicable
```

Never use `pass` for work not performed.

---

## 5. Default Analysis Procedure

### Step 1 — Fix Input

Record ZIP and file inventory.

### Step 2 — Validate Structure

Run parse and syntax checks.

### Step 3 — Classify Files

Classify every file into:

```text
canonical
source_of_truth
supporting_evidence
observational_evidence
incident_artifact
runtime_code
ci_code
binary_aio_asset
verification_token
public_discovery_file
```

### Step 4 — Run Single Heuristics

Run H01–H28.

### Step 5 — Run Combination Matrix

Run P01–P30 and C01–C15.

### Step 6 — Extract Remediation

Every issue must map to:

```text
path
category
severity
reason
recommended action
files likely affected
tests required
delivery impact
```

### Step 7 — Preserve Truthfulness

If a test did not run, report it as `blocked` or `not_run`, not `pass`.

### Step 8 — Prepare Handoff

If creating an improvement document or prompt, include:

```text
current repository facts
required changes
forbidden changes
test commands
delivery rules
JSON report schema
```

---

## 6. Required Test Commands

These commands are examples of the minimum validation set.  
If a command cannot run in the execution environment, record `blocked`.

```bash
python3 -m pip install --quiet PyYAML || true

python3 - <<'PY'
import json, re, sys
from pathlib import Path
import xml.etree.ElementTree as ET

errs = []

for p in Path('.').rglob('*.json'):
    if 'node_modules' in p.parts:
        continue
    try:
        json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errs.append(f'JSON parse failed: {p} :: {e}')

try:
    import yaml
    for p in list(Path('.github/workflows').glob('*.yml')) + list(Path('docs/incident-artifacts').glob('*.yml')):
        try:
            yaml.safe_load(p.read_text(encoding='utf-8'))
        except Exception as e:
            errs.append(f'YAML parse failed: {p} :: {e}')
except Exception as e:
    errs.append(f'YAML parser unavailable: {e}')

try:
    ET.parse('sitemap.xml')
except Exception as e:
    errs.append(f'XML parse failed: sitemap.xml :: {e}')

html = Path('index.html').read_text(encoding='utf-8')
for i, block in enumerate(re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', html, re.S | re.I), 1):
    try:
        json.loads(block.strip())
    except Exception as e:
        errs.append(f'JSON-LD parse failed: index.html block {i} :: {e}')

if errs:
    print('\n'.join(errs))
    sys.exit(1)

print('STRUCTURED_PARSE_PASS')
PY

python3 -m py_compile .github/scripts/*.py
python3 .github/scripts/check_js_syntax.py
node --check aio-guard.js
node --check sw.js

npm install --no-save stylelint@16 stylelint-declaration-strict-value@1
python3 .github/scripts/check_css_stylelint.py

python3 .github/scripts/update_aio_digests.py
python3 .github/scripts/check_aio_digests.py
python3 .github/scripts/check_binary_aio_metadata.py
```

Additional ChatGPT2ChatGPT integration check (delegated to repository CI):

```bash
# check_repository_consistency.py already enforces:
#   - ChatGPT2ChatGPT.md in aio-manifest.json supporting_evidence
#   - Claude2Claude.md in supporting_evidence (not in .well-known/index.json)
#   - All required files exist (Check 96 mirror bijection)
npm run check
```

---

## 7. Remediation Report Schema

Every analysis or improvement handoff should produce a machine-readable report.

```json
{
  "schema_version": "2.0.0",
  "source_zip_sha256": "<64 hex>",
  "zip_file_count": 0,
  "analysis_mode": "full_repository_plus_full_combination_matrix",
  "authority_model": {
    "canonical": "AI2AI.md",
    "implementation_evidence": "Claude2Claude.md",
    "analysis_evidence": "ChatGPT2ChatGPT.md"
  },
  "tests": [
    {
      "id": "STRUCTURED_PARSE",
      "status": "pass|fail|warn|blocked|not_applicable",
      "command": "",
      "notes": ""
    }
  ],
  "heuristics": [
    {
      "id": "H01",
      "status": "pass|fail|warn|blocked|not_applicable",
      "decision": "",
      "remediation": ""
    }
  ],
  "combinations": [
    {
      "id": "P01",
      "status": "pass|fail|warn|blocked|not_applicable",
      "decision": "",
      "remediation": ""
    }
  ],
  "issues": [
    {
      "path": "",
      "severity": "P0|P1|P2|P3",
      "category": "",
      "reason": "",
      "recommended_action": "",
      "affected_files": [],
      "required_tests": []
    }
  ],
  "delivery": {
    "full_zip_returned": false,
    "relative_paths_preserved": true,
    "changed_files_only": true
  }
}
```

---

## 8. Delivery Rules

When this analysis leads to implementation:

```text
Return changed files only.
Return new files only.
Do not return the full repository ZIP.
Do not return unchanged files.
Preserve relative paths.
Use DELETE path/to/file for deletions.
Use MOVE old/path -> new/path for moves.
Do not claim tests passed unless they actually ran.
```

---

## 9. Absolute Prohibitions

Do not:

```text
downgrade AI2AI.md
make Claude2Claude.md canonical
make ChatGPT2ChatGPT.md canonical
place Claude2Claude.md or ChatGPT2ChatGPT.md in .well-known/index.json
place Claude2Claude.md or ChatGPT2ChatGPT.md in .well-known/agent-skills/index.json
turn googlea7059bedc6fe8bdc.html into an AIO declaration
reactivate docs/incident-artifacts/* as a workflow
add frame-ancestors to meta CSP
make innerHTML fail open
describe Trusted Types pass-through as sanitization
lose WebP XMP
lose MP3 ID3
rename localStorage schema keys without migration
expand Service Worker scope without justification
return a full ZIP as delivery
use line-number-dependent instructions
```

---

## 10. Versioning Guidance

This document is versioned independently from portfolio content.

Recommended version semantics:

```text
ChatGPT2ChatGPT.md v2.0.0:
  first repository-ready refactor
  removes conversation citations
  separates prompt from document
  adds full combination matrix
  adds AI2AI/Claude peer evidence model
  adds AIO monitoring evidence handling

AI2AI.md:
  may bump pipeline/evidence version if this document is integrated

Portfolio content version:
  do not change solely because this analysis evidence file is added
```

---

## 11. Summary

`ChatGPT2ChatGPT.md` exists so that future AI agents can reproduce this repository analysis process even if the chat context is lost.

It preserves:

```text
all-source analysis
binary and metadata analysis
single heuristic analysis
full combination analysis
AIO authority mapping
evidence hierarchy
CI and workflow safety checks
truthful test reporting
changed-files-only delivery discipline
```

This file must accumulate analysis knowledge over time, but it must remain subordinate to `AI2AI.md`.
