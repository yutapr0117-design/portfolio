# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 5.1.x   | :white_check_mark: |
| 5.0.x   | :x:                |
| 4.0.x   | :white_check_mark: |
| < 4.0   | :x:                |

## Reporting a Vulnerability

Use this section to tell people how to report a vulnerability.

Tell them where to go, how often they can expect to get an update on a
reported vulnerability, what to expect if the vulnerability is accepted or
declined, etc.


## AIO Monitoring Policy

This repository includes an optional AIO citation monitoring workflow:

- `.github/workflows/aio-monitoring.yml`
- `.github/scripts/aio_monitoring.py`
- `docs/evidence/aio-monitoring-log.json`

### Secrets Configuration

When API keys / secrets are not configured:

- **AIO monitoring is optional observational.**
- If required secrets are not set, the monitoring script exits with `exit 0` (warning only).
- Missing secrets do NOT cause CI to block.
- Monitoring output is non-canonical and must not override `AI2AI.md` or `llms-full.txt`.

### Evidence Classification

`docs/evidence/aio-monitoring-log.json` is classified as:

```
observational_evidence
machine-generated AIO monitoring log
non-canonical
must not override llms-full.txt or AI2AI.md
```

It appears in `.well-known/aio-manifest.json` under `observational_evidence`, not `source_of_truth`.

### Workflow Permissions

`aio-monitoring.yml` follows least-privilege permissions. No repository write access is needed for monitoring-only runs.
