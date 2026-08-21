---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-critical-path-and-self-correction.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-21
canonical-ref: AI2AI.md / CLAUDE.md / docs/incident-artifacts/improvement-notes-claude-v80-phase4-gate-truth-audit.md / docs/architecture/file-size-budget.md
---

# docs/incident-artifacts/improvement-notes-claude-v80-phase4-critical-path-and-self-correction.md

## What

2026-08-21 の run（PR #1236〜#1243）の改善文書。前 run の「その gate は実際に何を見ているのか」を
**perf 面へ広げた**結果と、**自分が入れた変更の欠陥を自分で見つけて直した連鎖**の記録。

`AI2AI.md` の Session Record #28 は**要点のみ**を持ち、本ファイルが詳細層。

## Why

この run には、後から読む人が最も必要とする 2 種類の情報がある。

1. **アーキテクチャ上の判断**: quiz データを動的 import へ移した設計（なぜ render core を
   触らずに済んだのか）と、**Check 120 が測る対象を変えた理由**。後者は「正しい改善で
   数字が悪化する gate は改善の方向を誤らせる」という、次に perf を触る人が必ず要る前提。
2. **繰り返し踏んだ失敗の型**: 同じ assertion で 3 回 vacuous、条件が意図せず先に成立する
   class で 5 回。これは個別の bug より再利用価値が高い。

## How (usage)

- **cold-start の読み順**: `CLAUDE.md` §7 → `AI2AI.md` の最新 Session Record →
  （その run の詳細が要るとき）本ファイル。
- **perf を触る前**に「未着手の vein」節を読むこと。他のルート専用モジュールを遅延化する案は
  **render core (§3 の高リスク面) に触れる**ので、quiz と同じ手が使えるとは限らない。

## Constraints

- **Check 42a**: `improvement-notes-<author>-v<version>-<slug>.md` の命名に従う（準拠）。
- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること。
- **Check 108**: 本 mirror doc が存在すること。
- **Check 365**: 1,000 行以内。
- 歴史記録なので **Check 436 の規範層スコープ外**。過去の判断理由を後から書き換えないこと。

## Change impact

- 追記は「実測値を伴う事実」に限る。推測を足すと、次の AI がそれを根拠にコードを足す。
- 「未着手の vein」を消化したら、次の improvement-notes 側で状態を更新すること。

## Audience-specific notes

### For AI agents
- 役割タグ: `handoff`, `improvement-notes`, `performance`, `critical-path`, `self-correction`
- 最も再利用価値が高いのは **「その gate は実際に何を測っているのか」** と
  **「条件が意図せず先に成立する」5 例**。

### For human engineers (新卒レベル)
- 「ファイルがある」と「毎回ダウンロードされる」は別。遅延読み込みは**新しい状態**
  （データが来るまでの窓）を作り、そこに欠陥が生まれる。

### For auditors / third parties
- AI 自走下で、**自分が入れた変更の欠陥を自分で連続して見つけ、正直に記録した**実例。
