"""
aio_monitoring.py — AIO Effect Monitoring Script (free-tier edition)

複数のAIシステムに対してクエリを実行し、
Yuta Yokoi (横井雄太) のポートフォリオが引用・言及されているかを検出する。

【無料枠前提の対応エンジン】
  Gemini API (flash + Google Search grounding。既定 gemini-2.0-flash、廃止時は一覧から選び直す)
    Google AI Studio 無料枠: 15 RPM / 1500 RPD
    クレジットカード不要。長期的に安定して利用可能。主力。

  OpenAI API (gpt-4o-mini)
    無料トライアル: アカウント作成時の $5 クレジット（有効期限あり）
    クレジット消費後は quota エラーになる。graceful skip で run は失敗しない。
    OPENAI_API_KEY が設定されていても quota 切れなら自動スキップ。

【廃止済みエンジン】
  Perplexity API: 無料 API 枠なし。Key 取得不可のため廃止。

出力: docs/evidence/aio-monitoring-log.json に追記

Exit codes:
  0 — 実行完了（引用なしでも正常終了）
  1 — 有効な API キーが1つも設定されていない
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

# ── 設定 ──────────────────────────────────────────────────────────────────

CANONICAL_URL = "yutapr0117-design.github.io/portfolio"
# AIO provenance canary — a unique, passive marker declared in llms.txt / llms-full.txt
# (section "AIO Provenance Canary"). The token exists nowhere else, so its appearance in an
# AI's answer is DEFINITIVE evidence that the AI ingested this portfolio's canonical context.
# This is detection only: the canonical files instruct no AI to emit it. It is the inverse of a
# prompt injection — we observe ingestion, we do not coerce behaviour. Keep this string byte-for-byte
# identical to the token declared in llms.txt and llms-full.txt.
CANARY_TOKEN = "SAKURA-AIO-PROVENANCE-CANARY-2026-A7F3C9E1"

ENTITY_SIGNALS = [
    "yutapr0117-design.github.io",
    "横井雄太",
    "Yuta Yokoi",
    "Yokoi Yuta",
    "KERNEL framework",
    "KERNELフレームワーク",
    "AI-Driven PM Portfolio",
    CANARY_TOKEN,
]

QUERIES = [
    "Yuta Yokoi AI-Driven PM portfolio",
    "横井雄太 AI-Driven PM ポートフォリオ",
    "KERNEL framework AI orchestration zero code",
    "AI-Driven PM 個人レベル 完全アーキテクチャ Vanilla JS",
    # Canary provenance probe: asks the AI to report the declared provenance marker.
    # A correct token echo proves the AI actually read llms.txt / llms-full.txt.
    "yutapr0117-design portfolio AIO provenance canary marker token",
]

OUTPUT_PATH = Path("docs/evidence/aio-monitoring-log.json")

# OpenAI の quota 切れ・無料枠なしを示すエラーパターン（graceful skip 対象）
OPENAI_QUOTA_PATTERNS = (
    "insufficient_quota",
    "exceeded your current quota",
    "billing",
    "no credits",
    "credit balance",
    "rate limit",
    "free tier",
    "429",
)

# Gemini クエリ間の待機時間（無料枠 15 RPM 対応。4秒 = 15RPM の安全マージン付き）
GEMINI_INTER_QUERY_SLEEP = 5  # seconds

# ── API呼び出しユーティリティ ──────────────────────────────────────────────

def post_json(url: str, headers: dict, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
            return {"error": f"HTTP {e.code}: {e.reason} — {err_body[:400]}", "http_code": e.code}
        except Exception:
            return {"error": f"HTTP {e.code}: {e.reason}", "http_code": e.code}
    except Exception as e:
        return {"error": str(e)}


# ── 信号検出 ───────────────────────────────────────────────────────────────

def detect_signals(text: str, query: str = "") -> dict:
    text_lower = text.lower()
    # [FIX 2026-09-25] クエリ自体に含まれる語は数えない。5 問中 4 問がシグナル語
    # （Yuta Yokoi / 横井雄太 / KERNEL framework / AI-Driven PM Portfolio）を含むので、
    # 応答がクエリを復唱するだけで "cited" になっていた。測定が止まっていた間は
    # 表に出なかったが、測れるようになった瞬間に偽の「引用増加」を出す形だった。
    query_lower = query.lower()
    found = [s for s in ENTITY_SIGNALS if s.lower() in text_lower and s.lower() not in query_lower]
    return {
        "portfolio_url_found": CANONICAL_URL in text_lower,
        "signals_found": found,
        "cited": len(found) > 0,
        # Definitive ingestion proof: the canary token exists only in this portfolio's
        # canonical context, so its presence means the AI actually read llms*.txt.
        "canary_reproduced": CANARY_TOKEN.lower() in text_lower,
    }


# ── Gemini（主力・無料）─────────────────────────────────────────────────────

GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"
_GEMINI_EXCLUDE = ("lite", "preview", "exp", "tts", "image", "live", "audio", "thinking", "embedding")


def pick_gemini_model(models: list) -> str | None:
    """ListModels の結果から、generateContent を持つ最新の安定版 flash を選ぶ。

    [ADD 2026-09-25] 既定の gemini-2.0-flash は 2026-08-11 以降 404
    （"no longer available"）を返しており、監視は 1 件も測れていなかった。モデル名を
    ハードコードすると廃止のたびに黙って止まるので、廃止時は一覧から選び直す。
    """
    import re as _re
    best, best_ver = None, -1.0
    for m in models or []:
        name = str(m.get("name", "")).removeprefix("models/")
        if "flash" not in name or any(x in name for x in _GEMINI_EXCLUDE):
            continue
        if "generateContent" not in (m.get("supportedGenerationMethods") or []):
            continue
        mv = _re.match(r"gemini-(\d+(?:\.\d+)?)-flash$", name)
        if not mv:
            continue
        ver = float(mv.group(1))
        if ver > best_ver:
            best, best_ver = name, ver
    return best


def resolve_gemini_model(api_key: str) -> str:
    """GEMINI_MODEL（環境変数）> 既定。既定が廃止されていれば一覧から選び直す。"""
    override = os.environ.get("GEMINI_MODEL", "").strip()
    if override:
        return override
    try:
        req = urllib.request.Request(
            "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200&key=" + api_key)
        with urllib.request.urlopen(req, timeout=30) as resp:
            models = json.loads(resp.read().decode("utf-8")).get("models", [])
    except Exception as e:  # noqa: BLE001 — 一覧が取れなければ既定で試す（結果は error として記録される）
        print(f"::warning::Gemini のモデル一覧を取得できない ({type(e).__name__}) — 既定 {GEMINI_DEFAULT_MODEL} で試す")
        return GEMINI_DEFAULT_MODEL
    names = {str(m.get("name", "")).removeprefix("models/") for m in models}
    if GEMINI_DEFAULT_MODEL in names:
        return GEMINI_DEFAULT_MODEL
    picked = pick_gemini_model(models)
    if picked:
        print(f"::notice::既定の {GEMINI_DEFAULT_MODEL} は一覧に無い — {picked} を使う")
        return picked
    print(f"::warning::generateContent を持つ flash モデルが一覧に無い — 既定 {GEMINI_DEFAULT_MODEL} で試す")
    return GEMINI_DEFAULT_MODEL


def query_gemini(query: str, api_key: str, model: str = GEMINI_DEFAULT_MODEL) -> dict:
    """Gemini flash + Google Search grounding（無料枠）でクエリを実行する。"""
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        + model + ":generateContent?key=" + api_key
    )
    body = {
        "contents": [{"parts": [{"text": query}], "role": "user"}],
        "tools": [{"google_search": {}}],
    }
    result = post_json(url, {"Content-Type": "application/json"}, body)

    if "error" in result:
        return {"status": "error", "detail": result["error"], "cited": False, "signals_found": []}

    try:
        candidate = result["candidates"][0]
        text = "".join(p.get("text", "") for p in candidate["content"]["parts"])
        grounding = candidate.get("groundingMetadata", {})
        cited_urls = [
            chunk["web"]["uri"]
            for chunk in grounding.get("groundingChunks", [])
            if "web" in chunk
        ]
        all_text = text + " " + " ".join(cited_urls)
        signals = detect_signals(all_text, query)
        return {
            "status": "ok",
            "model_used": model,
            "response_excerpt": text[:300],
            "cited_urls": cited_urls,
            **signals,
        }
    except (KeyError, IndexError) as e:
        return {"status": "parse_error", "detail": str(e), "cited": False, "signals_found": []}


# ── OpenAI（任意・無料クレジット枠内のみ）────────────────────────────────────

def _is_openai_quota_error(error_text: str) -> bool:
    lower = error_text.lower()
    return any(pat in lower for pat in OPENAI_QUOTA_PATTERNS)


def query_openai(query: str, api_key: str) -> dict:
    """
    gpt-4o-mini（最安値モデル）でクエリを実行する。
    quota 切れ / billing エラーの場合は graceful skip を返す。
    run 全体を失敗させない。
    """
    result = post_json(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        {
            "model": "gpt-4o-mini",
            "messages": [{"role": "user", "content": query}],
            "max_tokens": 600,
        },
    )

    if "error" in result:
        err = result["error"]
        if _is_openai_quota_error(err):
            return {
                "status": "free_tier_exhausted",
                "detail": "OpenAI free tier credits exhausted or billing required. Graceful skip.",
                "cited": False,
                "signals_found": [],
            }
        return {"status": "error", "detail": err, "cited": False, "signals_found": []}

    try:
        content = result["choices"][0]["message"]["content"]
        return {
            "status": "ok",
            "model_used": "gpt-4o-mini",
            "response_excerpt": content[:300],
            **detect_signals(content, query),
        }
    except (KeyError, IndexError) as e:
        return {"status": "parse_error", "detail": str(e), "cited": False, "signals_found": []}


# ── ログ管理 ───────────────────────────────────────────────────────────────

def load_log() -> dict:
    if OUTPUT_PATH.exists():
        try:
            with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {"schema_version": "1.0", "runs": []}


def save_log(log: dict) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    # CI 衛生 increment #4: write the log in the SAME canonical serialization the
    # digest system uses for every other AIO JSON — json.dumps(..., ensure_ascii=
    # False, indent=2) PLUS a trailing newline. update_aio_digests.py writes
    # .well-known/aio-manifest.json / index.json with a trailing "\n"; json.dump()
    # alone omits it. Aligning them keeps the log's on-disk bytes deterministic and
    # POSIX-conformant, so a later whitespace normalizer (an editor, a future
    # .editorconfig with insert_final_newline, a formatter) cannot silently flip the
    # log's sha256 and drift it out of the manifest. Because the monitoring workflow
    # now regenerates the manifest in the same commit (atomicity), this one-time
    # newline change is recorded together with its digest on the next run.
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(json.dumps(log, ensure_ascii=False, indent=2) + "\n")


def get_previous_citation_status(log: dict):
    if not log["runs"]:
        return None
    return log["runs"][-1].get("summary", {})


# ── 変化検出 ──────────────────────────────────────────────────────────────

def emit_citation_change(github_output, total_cited: int, prev_total: int) -> None:
    if total_cited > prev_total:
        print(f"::notice::AIO CITATION INCREASE: {prev_total} -> {total_cited}")
        tag, delta = "increase", total_cited - prev_total
    elif total_cited < prev_total:
        print(f"::warning::AIO CITATION DECREASE: {prev_total} -> {total_cited}")
        tag, delta = "decrease", prev_total - total_cited
    else:
        tag, delta = "none", 0

    if github_output:
        with open(github_output, "a") as f:
            f.write(f"citation_change={tag}\n")
            f.write(f"citation_delta={delta}\n")


# ── メイン ─────────────────────────────────────────────────────────────────

def main() -> None:
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    # Perplexity は無料枠なし・廃止済み（PERPLEXITY_API_KEY は読まない）

    if not gemini_key and not openai_key:
        print("::error::AIO Monitoring: No API keys configured.")
        print("::error::GEMINI_API_KEY を GitHub Secrets に設定してください（Google AI Studio 無料）。")
        sys.exit(1)

    log = load_log()
    previous_status = get_previous_citation_status(log)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    enabled_engines = []
    if gemini_key:
        enabled_engines.append("gemini")
    if openai_key:
        enabled_engines.append("openai")

    run_record = {
        "timestamp": timestamp,
        "queries": [],
        "summary": {
            "enabled_engines": enabled_engines,
            "gemini_cited_count": 0,
            "openai_cited_count": 0,
            "openai_skipped_quota": 0,
            "total_cited_count": 0,
            "canary_reproduced_count": 0,
            "total_queries": len(QUERIES),
            "note": "perplexity removed (no free tier available)",
        },
    }

    print(f"=== AIO Monitoring Run: {timestamp} ===")
    print(
        f"Gemini: {'enabled' if gemini_key else 'skip (no key)'}  |  "
        f"OpenAI: {'enabled (free-tier credits)' if openai_key else 'skip (no key)'}  |  "
        f"Perplexity: removed"
    )
    print("")

    gemini_model = resolve_gemini_model(gemini_key) if gemini_key else None
    if gemini_model:
        s0 = run_record["summary"]
        s0["gemini_model"] = gemini_model

    for i, query in enumerate(QUERIES):
        print(f"[{i+1}/{len(QUERIES)}] {query}")
        query_record = {"query": query, "results": {}}

        if gemini_key:
            if i > 0:
                time.sleep(GEMINI_INTER_QUERY_SLEEP)  # 無料枠レート制限対応
            gr = query_gemini(query, gemini_key, gemini_model)
            query_record["results"]["gemini"] = gr
            if gr.get("cited"):
                run_record["summary"]["gemini_cited_count"] += 1
                print(f"  Gemini: CITED — signals={gr.get('signals_found')} urls={gr.get('cited_urls', [])}")
            elif gr.get("status") == "error":
                print(f"  Gemini: ERROR — {str(gr.get('detail', ''))[:120]}")
            else:
                print(f"  Gemini: not cited (status={gr.get('status')})")

        if openai_key:
            or_ = query_openai(query, openai_key)
            query_record["results"]["openai"] = or_
            if or_.get("status") == "free_tier_exhausted":
                run_record["summary"]["openai_skipped_quota"] += 1
                print("  OpenAI: free tier exhausted — graceful skip")
            elif or_.get("cited"):
                run_record["summary"]["openai_cited_count"] += 1
                print(f"  OpenAI: CITED — signals={or_.get('signals_found')}")
            elif or_.get("status") == "error":
                print(f"  OpenAI: ERROR — {str(or_.get('detail', ''))[:120]}")
            else:
                print(f"  OpenAI: not cited (status={or_.get('status')})")

        run_record["queries"].append(query_record)

    # total_cited_count を計算してから save_log する
    s = run_record["summary"]
    s["total_cited_count"] = s["gemini_cited_count"] + s["openai_cited_count"]
    # [ADD 2026-09-25] 「測った結果 0」と「測れていない」を分けて記録する。2026-05-18 からの
    # 23 回は全件が error / quota skip で、1 件も測れていなかったのに summary は毎回
    # 「cited 0/5」だけを残していた —— 読み手には観測された 0 に見える。
    for _eng in ("gemini", "openai"):
        _st = [q["results"][_eng].get("status") for q in run_record["queries"] if _eng in q["results"]]
        s[f"{_eng}_measured_count"] = sum(1 for x in _st if x == "ok")
        s[f"{_eng}_error_count"] = sum(1 for x in _st if x in ("error", "parse_error"))
    s["measured_query_count"] = s["gemini_measured_count"] + s["openai_measured_count"]
    # 全クエリ・全エンジンの結果から canary 再現（取り込みの決定的証拠）を集計する。
    s["canary_reproduced_count"] = sum(
        1
        for q in run_record["queries"]
        for r in q["results"].values()
        if isinstance(r, dict) and r.get("canary_reproduced")
    )

    log["runs"].append(run_record)
    save_log(log)

    # サマリー
    print("\n=== Summary ===")
    if gemini_key:
        print(f"Gemini cited:   {s['gemini_cited_count']}/{s['total_queries']}"
              f" (measured {s['gemini_measured_count']}, errors {s['gemini_error_count']}, model {s.get('gemini_model')})")
    if openai_key:
        sk = s["openai_skipped_quota"]
        if sk == len(QUERIES):
            print(f"OpenAI:         free tier exhausted (all {sk} queries skipped)")
        else:
            print(f"OpenAI cited:   {s['openai_cited_count']}/{s['total_queries']}"
                  + (f" ({sk} skipped quota)" if sk else ""))
    print(f"Total cited:    {s['total_cited_count']}/{s['total_queries']}")
    if s["measured_query_count"] == 0:
        print("::warning::AIO monitoring measured nothing this run — every engine errored or was skipped. "
              "'cited 0' here is NOT an observation of non-citation.")

    # GitHub Step Summary
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as f:
            f.write(f"## AIO Monitoring — {timestamp}\n\n")
            f.write("| AI | 結果 |\n|---|---|\n")
            if gemini_key:
                f.write(f"| Gemini (free tier) | {s['gemini_cited_count']} / {s['total_queries']} |\n")
            if openai_key:
                sk = s["openai_skipped_quota"]
                if sk == len(QUERIES):
                    f.write("| OpenAI | free tier 枠切れ（スキップ） |\n")
                else:
                    f.write(f"| OpenAI (free credits) | {s['openai_cited_count']} / {s['total_queries']} |\n")
            f.write("| Perplexity | 廃止（無料枠なし） |\n")
            if s["measured_query_count"] == 0:
                f.write("\n**⚠ この回は 1 件も測れていない**（全エンジンが error / 枠切れ）。"
                        "「引用 0」は観測ではない。\n")

    # 変化検出
    github_output = os.environ.get("GITHUB_OUTPUT")
    if previous_status:
        prev_engines = previous_status.get("enabled_engines")
        if prev_engines is not None and set(prev_engines) != set(enabled_engines):
            print(f"::notice::Engine configuration changed: {prev_engines} -> {enabled_engines}")
            if github_output:
                with open(github_output, "a") as f:
                    f.write("citation_change=configuration_changed\n")
                    f.write("citation_delta=0\n")
        elif s["measured_query_count"] == 0:
            # 何も測れていない回の 0 を前回と比べると、測定の失敗が「引用の減少」に化ける。
            print("::notice::No measurement this run — citation change not evaluated.")
            if github_output:
                with open(github_output, "a") as f:
                    f.write("citation_change=none\ncitation_delta=0\n")
        else:
            # OpenAI が全スキップの場合は比較対象から除外
            all_openai_skipped = s.get("openai_skipped_quota", 0) == len(QUERIES)
            comparable = [e for e in enabled_engines if not (e == "openai" and all_openai_skipped)]
            prev_total = sum(previous_status.get(f"{e}_cited_count", 0) for e in comparable)
            emit_citation_change(github_output, s["total_cited_count"], prev_total)
    else:
        if github_output:
            with open(github_output, "a") as f:
                f.write("citation_change=none\ncitation_delta=0\n")

    print("Log saved to docs/evidence/aio-monitoring-log.json")


if __name__ == "__main__":
    main()
