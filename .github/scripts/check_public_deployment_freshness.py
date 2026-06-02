#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_public_deployment_freshness.py — public deployment freshness OBSERVER (NON-BLOCKING)

WHY THIS SCRIPT EXISTS
----------------------
The repository working copy (a local clone, or the ZIP handed to an AI agent) is the
single source of truth. The GitHub Pages deployment, AI crawlers, and search/extraction
caches are *downstream observers* of that truth, and they can legitimately lag: a path
can return an older version (e.g. a v68-era llms.txt) because of Pages build/deploy delay,
CDN/HTTP caching, the fetch tool's own cache, or a stale search index — none of which mean
the repository is wrong.

This observer fetches the PUBLIC llms.txt and compares it against expectations derived from
the working-copy source of truth, so a human or AI can SEE whether the public surface has
caught up — WITHOUT ever being tempted to "fix" the repository by rolling it back to the
older public content. Rolling the repository back to stale public output is explicitly
forbidden (see docs/evidence/public-deployment-freshness-review.md).

DESIGN CONTRACT (deliberate, do not "harden" into a gate)
---------------------------------------------------------
- This script is OBSERVATIONAL EVIDENCE, never a BLOCKING gate. It depends on an external
  HTTP endpoint, which is inherently flaky; making it block CI would couple correctness to
  network weather. It therefore ALWAYS exits 0, even on network failure or mismatch.
- It is intentionally NOT part of `npm run check` and NOT a check in
  check_repository_consistency.py. Run it manually, or on a schedule, as a warning-only probe.
- It reads the local llms.txt to derive expectations, so the expected values stay honest as
  the source of truth evolves (no hard-coded version that drifts).

USAGE
-----
    python3 .github/scripts/check_public_deployment_freshness.py
    python3 .github/scripts/check_public_deployment_freshness.py --url <public-llms.txt URL>
    python3 .github/scripts/check_public_deployment_freshness.py --json   # machine-readable

EXIT CODE
---------
    0 — always (observational; absence of a match is NOT a failure, only an observation).
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Default public entry point. The repository is a GitHub Pages *project* site, so the
# canonical public path is project-scoped (/portfolio/...), not origin-root.
DEFAULT_PUBLIC_URL = "https://yutapr0117-design.github.io/portfolio/llms.txt"

# The passive provenance canary. Its presence in BOTH the source of truth and a fetched
# response is decisive positive evidence that the response derives from current canonical
# content. (This token is descriptive provenance, not an instruction — the opposite of a
# prompt injection.)
CANARY_TOKEN = "SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1"

# How long to wait on the network before treating the fetch as "unobservable".
HTTP_TIMEOUT_SECONDS = 15


def _read_local_llms() -> str:
    """Return the working-copy llms.txt (the source of truth for expectations)."""
    return (ROOT / "llms.txt").read_text(encoding="utf-8")


def _extract_last_updated(text: str) -> str | None:
    """Pull the declared 'Last-Updated: YYYY-MM-DD' date out of an llms.txt body."""
    m = re.search(r"Last-Updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})", text)
    return m.group(1) if m else None


def _fetch(url: str) -> tuple[str | None, str | None]:
    """
    Fetch `url`. Returns (body, error). Either body is set (success) or error is set
    (the endpoint was unobservable). Never raises — network failure is an observation,
    not a crash.
    """
    req = urllib.request.Request(
        url,
        headers={
            # Ask intermediaries not to serve a cached copy, so we observe the freshest
            # public state we can. (Caches may still ignore this; that itself is signal.)
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "User-Agent": "portfolio-aio-freshness-observer/1.0 (+non-blocking observational probe)",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT_SECONDS) as resp:
            raw = resp.read()
        return raw.decode("utf-8", errors="replace"), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return None, f"network error: {e.reason}"
    except Exception as e:  # noqa: BLE001 — observational probe must never crash the caller
        return None, f"unexpected error: {e!r}"


def observe(url: str) -> dict:
    """
    Compare the public llms.txt against working-copy expectations and return a structured
    observation. This function makes NO judgement about which side is 'correct' — it only
    records what was observed and classifies any divergence.
    """
    local = _read_local_llms()
    expected_date = _extract_last_updated(local)
    expected_canary_present = CANARY_TOKEN in local

    result: dict = {
        "observed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "public_url": url,
        "source_of_truth": "working-copy llms.txt",
        "expected_last_updated": expected_date,
        "expected_canary_present": expected_canary_present,
        "fetch_ok": False,
        "public_last_updated": None,
        "public_canary_present": None,
        "classification": None,
        "notes": [],
    }

    body, err = _fetch(url)
    if body is None:
        result["classification"] = "unobservable"
        result["notes"].append(
            f"Could not fetch the public endpoint ({err}). This is an observation, not a "
            "repository defect; the working copy remains the source of truth."
        )
        return result

    result["fetch_ok"] = True
    public_date = _extract_last_updated(body)
    public_canary = CANARY_TOKEN in body
    result["public_last_updated"] = public_date
    result["public_canary_present"] = public_canary

    date_matches = (expected_date is not None) and (public_date == expected_date)
    canary_matches = (expected_canary_present == public_canary)

    if date_matches and canary_matches:
        result["classification"] = "fresh"
        result["notes"].append(
            "The public surface matches the source of truth (Last-Updated and canary aligned)."
        )
    else:
        # Diverged. Classify WHY, but never recommend rolling the repo back.
        result["classification"] = "stale-or-divergent"
        if expected_date and public_date and public_date < expected_date:
            result["notes"].append(
                f"Public Last-Updated ({public_date}) is OLDER than the source of truth "
                f"({expected_date}). Likely Pages deploy lag, CDN/HTTP cache, fetch-tool "
                f"cache, or a stale search index. DO NOT roll the repository back."
            )
        elif expected_date and public_date and public_date > expected_date:
            result["notes"].append(
                f"Public Last-Updated ({public_date}) is NEWER than this working copy "
                f"({expected_date}). This working copy may predate the latest commit; "
                f"reconcile against the repository before assuming a defect."
            )
        if expected_canary_present and not public_canary:
            result["notes"].append(
                "Provenance canary is present in the source of truth but ABSENT from the "
                "public response — strong sign the public surface has not yet caught up."
            )
        if not result["notes"]:
            result["notes"].append(
                "Public content diverges from the source of truth; classify as a "
                "propagation/cache/retrieval-path difference, not a repository defect."
            )

    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Observe public-deployment freshness (NON-BLOCKING; always exits 0)."
    )
    parser.add_argument("--url", default=DEFAULT_PUBLIC_URL, help="Public llms.txt URL to probe.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON.")
    args = parser.parse_args()

    obs = observe(args.url)

    if args.json:
        print(json.dumps(obs, ensure_ascii=False, indent=2))
    else:
        print("Public deployment freshness — OBSERVATION (non-blocking, always exit 0)")
        print(f"  observed_at           : {obs['observed_at']}")
        print(f"  public_url            : {obs['public_url']}")
        print(f"  expected Last-Updated : {obs['expected_last_updated']}  (from working-copy llms.txt)")
        print(f"  fetch_ok              : {obs['fetch_ok']}")
        print(f"  public Last-Updated   : {obs['public_last_updated']}")
        print(f"  canary expected/public: {obs['expected_canary_present']} / {obs['public_canary_present']}")
        print(f"  classification        : {obs['classification']}")
        for note in obs["notes"]:
            print(f"  note: {note}")
        print()
        print("Reminder: the working copy is the source of truth. A stale or unobservable "
              "public surface is an observation to record, never a reason to roll the repository back.")

    # OBSERVATIONAL by contract: always succeed, regardless of what was observed.
    return 0


if __name__ == "__main__":
    sys.exit(main())
