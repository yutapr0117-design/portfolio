"""
aio_monitoring.py — AIO Effect Monitoring Script

複数のAIシステムに対してクエリを実行し、
Yuta Yokoi (横井雄太) のポートフォリオが引用・言及されているかを検出する。

対応API:
  - Perplexity API (sonar model — web検索付き、citations付き)
  - OpenAI API (gpt-4o-search-preview — web検索付き)

出力:
  docs/evidence/aio-monitoring-log.json に追記

Exit codes:
  0 — 実行完了（引用なしでも正常終了）
  1 — API設定エラーまたは実行失敗
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── 設定 ──────────────────────────────────────────────────────────────────

CANONICAL_URL = "yutapr0117-design.github.io/portfolio"
ENTITY_SIGNALS = [
    "yutapr0117-design.github.io",
    "横井雄太",
    "Yuta Yokoi",
    "Yokoi Yuta",
    "KERNEL framework",
    "KERNELフレームワーク",
    "AI-Driven PM Portfolio",
]

QUERIES = [
    "Yuta Yokoi AI-Driven PM portfolio",
    "横井雄太 AI-Driven PM ポートフォリオ",
    "KERNEL framework AI orchestration zero code",
    "AI-Driven PM 個人レベル 完全アーキテクチャ Vanilla JS",
]

OUTPUT_PATH = Path("docs/evidence/aio-monitoring-log.json")

# ── API呼び出しユーティリティ ───────────────────────────────────────────────

def post_json(url: str, headers: dict, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode("utf-8")
            return {"error": f"HTTP {e.code}: {e.reason} — {body[:300]}"}
        except Exception:
            return {"error": f"HTTP {e.code}: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


# ── 信号検出 ───────────────────────────────────────────────────────────────

def detect_signals(text: str) -> dict:
    text_lower = text.lower()
    found = [s for s in ENTITY_SIGNALS if s.lower() in text_lower]
    return {
        "portfolio_url_found": CANONICAL_URL in text_lower,
        "signals_found": found,
        "cited": len(found) > 0,
    }


# ── Perplexity ─────────────────────────────────────────────────────────────

def query_perplexity(query: str, api_key: str) -> dict:
    result = post_json(
        "https://api.perplexity.ai/chat/completions",
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        {
            "model": "sonar",
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 800,
        },
    )

    if "error" in result:
        return {"status": "error", "detail": result["error"]}

    try:
        content = result["choices"][0]["message"]["content"]
        citations = result.get("citations", [])
        signals = detect_signals(content + " " + " ".join(citations))
        return {
            "status": "ok",
            "response_excerpt": content[:300],
            "citations": citations,
            **signals,
        }
    except (KeyError, IndexError) as e:
        return {"status": "parse_error", "detail": str(e)}


# ── OpenAI ─────────────────────────────────────────────────────────────────

def _call_openai(api_key: str, body: dict) -> dict:
    return post_json(
        "https://api.openai.com/v1/chat/completions",
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        body,
    )

def query_openai(query: str, api_key: str) -> dict:
    # 試行順: search-preview → tools形式 → gpt-4o(フォールバック)
    attempts = [
        {"model": "gpt-4o-search-preview",
         "messages": [{"role": "user", "content": query}],
         "max_tokens": 800},
        {"model": "gpt-4o",
         "tools": [{"type": "web_search_preview"}],
         "messages": [{"role": "user", "content": query}],
         "max_tokens": 800},
        {"model": "gpt-4o",
         "messages": [{"role": "user", "content": query}],
         "max_tokens": 800},
    ]

    last_error = None
    for body in attempts:
        result = _call_openai(api_key, body)
        if "error" in result:
            last_error = result["error"]
            print(f"    [OpenAI] model={body['model']} error: {last_error[:120]}")
            continue
        try:
            content = result["choices"][0]["message"]["content"]
            signals = detect_signals(content)
            return {
                "status": "ok",
                "model_used": body["model"],
                "response_excerpt": content[:300],
                **signals,
            }
        except (KeyError, IndexError) as e:
            last_error = str(e)
            continue

    return {"status": "error", "detail": last_error}


# ── ログ管理 ───────────────────────────────────────────────────────────────

def load_log() -> dict:
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"runs": []}


def save_log(log: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)


def get_previous_citation_status(log: dict) -> dict | None:
    """直前のrunの引用状況サマリーを返す"""
    if not log["runs"]:
        return None
    last = log["runs"][-1]
    return last.get("summary", {})


# ── メイン ─────────────────────────────────────────────────────────────────

def main() -> None:
    perplexity_key = os.environ.get("PERPLEXITY_API_KEY", "")
    openai_key = os.environ.get("OPENAI_API_KEY", "")

    if not perplexity_key and not openai_key:
        print("::error::AIO Monitoring: No API keys configured.")
        print("::error::Set PERPLEXITY_API_KEY or OPENAI_API_KEY in GitHub Secrets.")
        sys.exit(1)

    log = load_log()
    previous_status = get_previous_citation_status(log)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    run_record = {
        "timestamp": timestamp,
        "queries": [],
        "summary": {
            "perplexity_cited_count": 0,
            "openai_cited_count": 0,
            "total_queries": len(QUERIES),
        },
    }

    print(f"=== AIO Monitoring Run: {timestamp} ===")
    print(f"Queries: {len(QUERIES)}  |  Perplexity: {'enabled' if perplexity_key else 'skip'}  |  OpenAI: {'enabled' if openai_key else 'skip'}")
    print("")

    for query in QUERIES:
        print(f"Query: {query}")
        query_record = {"query": query, "results": {}}

        if perplexity_key:
            pr = query_perplexity(query, perplexity_key)
            query_record["results"]["perplexity"] = pr
            if pr.get("cited"):
                run_record["summary"]["perplexity_cited_count"] += 1
                print(f"  Perplexity: CITED — {pr.get('signals_found', [])}")
            else:
                print(f"  Perplexity: not cited (status={pr.get('status')})")

        if openai_key:
            or_ = query_openai(query, openai_key)
            query_record["results"]["openai"] = or_
            if or_.get("cited"):
                run_record["summary"]["openai_cited_count"] += 1
                print(f"  OpenAI: CITED — {or_.get('signals_found', [])}")
            else:
                detail = or_.get("detail", "")
                model = or_.get("model_used", "")
                print(f"  OpenAI: not cited (status={or_.get('status')} model={model} detail={detail[:80]})")

        run_record["queries"].append(query_record)

    log["runs"].append(run_record)
    save_log(log)

    # ── 変化検出（GitHub Actions output） ─────────────────────────────────
    s = run_record["summary"]
    total_cited = s["perplexity_cited_count"] + s["openai_cited_count"]

    print("")
    print(f"=== Summary ===")
    print(f"Perplexity cited: {s['perplexity_cited_count']}/{s['total_queries']}")
    print(f"OpenAI cited:     {s['openai_cited_count']}/{s['total_queries']}")

    # GitHub Actions の job summary に出力
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(f"## AIO Monitoring — {timestamp}\n\n")
            f.write(f"| AI | 引用クエリ数 / 全クエリ数 |\n|---|---|\n")
            if perplexity_key:
                f.write(f"| Perplexity | {s['perplexity_cited_count']} / {s['total_queries']} |\n")
            if openai_key:
                f.write(f"| OpenAI | {s['openai_cited_count']} / {s['total_queries']} |\n")

    # 変化があればGitHub Actionsで警告出力（Issue作成はワークフロー側で行う）
    if previous_status:
        prev_total = previous_status.get("perplexity_cited_count", 0) + previous_status.get("openai_cited_count", 0)
        if total_cited > prev_total:
            print(f"::notice::AIO CITATION INCREASE: {prev_total} → {total_cited}")
            # GitHub Actions output variable
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    f.write(f"citation_change=increase\n")
                    f.write(f"citation_delta={total_cited - prev_total}\n")
        elif total_cited < prev_total:
            print(f"::warning::AIO CITATION DECREASE: {prev_total} → {total_cited}")
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    f.write(f"citation_change=decrease\n")
                    f.write(f"citation_delta={prev_total - total_cited}\n")
        else:
            github_output = os.environ.get("GITHUB_OUTPUT")
            if github_output:
                with open(github_output, "a") as f:
                    f.write(f"citation_change=none\n")
                    f.write(f"citation_delta=0\n")

    print("Log saved to docs/evidence/aio-monitoring-log.json")


if __name__ == "__main__":
    main()
