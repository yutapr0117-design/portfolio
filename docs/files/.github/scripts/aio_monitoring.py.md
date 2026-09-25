---
file: .github/scripts/aio_monitoring.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/workflows/aio-monitoring.yml / docs/evidence/aio-monitoring-log.json
---

# .github/scripts/aio_monitoring.py

## What

AIO 引用効果の週次監視スクリプト。Gemini (主力) / OpenAI (任意) の AI API へ規定クエリを投げ、entity (Yuta Yokoi) への canary token 引用が観測されるかを記録。

## Why

「AIO-first 戦略の効果」は機械的計測が困難。本スクリプトは attempt log として **honest な観測** を保持 (引用ゼロでも 0 と記録)。捏造禁止。

## How (usage)

```
GitHub Actions (.github/workflows/aio-monitoring.yml)
  └─ 毎週月曜 10:00 JST + workflow_dispatch
       └─ python3 .github/scripts/aio_monitoring.py
            └─ Gemini / OpenAI に query 投げる
            └─ canary token 引用観測 → docs/evidence/aio-monitoring-log.json に append
```

### 2026-09-25: この監視は、始まってから一度も測れていなかった

蓄積ログの **23 回（2026-05-18〜2026-09-25）すべてで、Gemini も OpenAI も成功した問い合わせが 0 件**だった。
Gemini は 2026-08-10 まで **429**（無料枠のレート制限）、2026-08-11 以降は **404**（`gemini-2.0-flash` が
"no longer available"）。OpenAI は 2026-06-01 以降ずっと無料枠切れ。**それでも各回の summary は
「cited 0/5」だけを残しており、読み手には観測された 0 に見えた。** 公開面（manifest / llms / mcp.json /
SECURITY.md）はこのログを「試行の記録で、引用の証拠ではない」と正しく述べていたので、偽だったのは
スクリプトの出力の側である。直したこと:

- summary に `*_measured_count` / `*_error_count` / `measured_query_count` / `gemini_model` を記録する。
  **1 件も測れなかった回は `::warning::` と step summary で「引用 0 は観測ではない」と明示**し、
  前回との増減比較もしない（測定の失敗が「引用の減少」に化けるのを防ぐ）
- モデル名をハードコードせず、既定が一覧に無ければ `ListModels` から**最新の安定版 flash**
  （lite / preview / exp などを除く・`generateContent` を持つ）を選び直す。`GEMINI_MODEL` で上書きできる
- **測れるようになった瞬間に出るはずだった偽陽性も先に潰した**: 5 問中 4 問がシグナル語を含むため、
  応答がクエリを復唱するだけで "cited" になっていた。クエリ自体に含まれる語は数えない

**429 は直していない**（無料枠の制約で、コードの欠陥ではない）。次の実行でモデルが解決しても、
429 に戻れば「測れていない」と正しく表示されるだけである。

## Constraints

- **Check 11**: summary dict に `enabled_engines` + `total_cited_count` キー
- **Check 25**: aio-monitoring-log.json に `evidence_policy` キー (attempt log only)
- **Check 44**: canary token 整合
- **捏造禁止**: 観測値以外を log に書かない

## Change impact

- query 内容変更 → 過去 log との比較困難に (慎重判断)
- new engine 追加 → API キー secret 追加 + summary dict 拡張

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-monitoring`, `canary-detection`, `honest-attempt-log`

### For human engineers (新卒レベル)
- 引用観測の捏造は禁止 — observed = 0 でもそのまま記録

### For third parties
- AIO 効果の honest dating 観測記録
