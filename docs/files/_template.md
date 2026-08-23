---
file: <repo-relative path of the source file>
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: YYYY-MM-DD
canonical-ref: AI2AI.md / CLAUDE.md / docs/architecture/<関連 doc>
---

# <relative path>

## What
1-2 文でこのファイルは何か。

## Why
なぜこのファイルが存在するか。暗黙の前提・制約・歴史的経緯。「何の問題を解決するために」存在するか。

## How (usage)
このファイルがどう使われるか。誰が呼ぶか / 何を呼ぶか。entry point (index.html / main.js) からの距離・経路。

## Constraints
このファイルに課せられた制約。
- 適用 C 番号 (C1-C7)
- 機械強制している Check 番号 (総数の真値は `docs/architecture/total-check-runbook.md` §9。
  **範囲をここに書かない** — 数値は必ず drift する)
- 編集時に満たすべき不変条件 (AIO published-layer なら C6 の真実性/面間整合/digest 再生成、
  kernel なら DO-NOT-EDIT 領域の byte 同一性、binary なら日付 field 同期 等)。
  **「承認が必要か」は書かない** — 承認は恒久的に与えられており「裁可待ち」という作業
  カテゴリは存在しない (AI2AI.md STEP 3 / Check 436)

## Change impact
変更時に同時更新が必要なファイル群。drift を生む典型パターン。

## Audience-specific notes

### For AI agents (LLM / crawler / AI search)
構造化 metadata: 役割タグ、依存関係、import / export シグネチャ概略、機械可読な制約。

### For human engineers (新卒レベル想定)
平易な日本語で、このファイルが何のためにあるか・どう触っていいか・触ってはいけない箇所はどこか。

### For third parties (監査人 / 採用担当 / 学術研究者)
このファイルが何を示しているか (proof-of-work / 設計判断の証跡 / アーキテクチャ説明) の high-level summary。
