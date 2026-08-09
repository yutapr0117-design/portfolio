---
file: .github/scripts/checks_mutation_integrity.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-10
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/mutation_probe.py (runner) / .github/scripts/mutation_samples.py (データ)
---

# .github/scripts/checks_mutation_integrity.py

## What

**mutation 安全網そのものの完全性**を守る Check 群（362 / 379 / 380 / 397 / 399 / 409・すべて BLOCKING）を所有する split module。`checks_maintainability.py` から「meta-QA」カテゴリとして切り出した。

| Check | 守る面 |
| :-- | :-- |
| 362 | mutation の `find` anchor が対象ファイルに実在する |
| 379 | E2E_MUTATIONS の `test` フィールドが実在の e2e title に解決する（≥1） |
| 380 | `replace` ≠ `find`（no-op mutation は必ず SURVIVED する偽陰性） |
| 397 | `test` フィールドが**ただ一つ**の test に解決する（帰属の曖昧化防止） |
| 399 | mutation-probe の catch 判定が Check 362 の副作用で自動成立しない |
| 409 / 409b | consistency / behavior の登録先分離（`test` キーの有無 + 命名規約） |

## Why

mutation testing は「安全網（consistency Check 群 / behavior e2e）が実際に回帰を捕捉できるか」を検証する唯一の手段であり、**mutation 定義自体が腐ると、CI の緑は「守られている」ではなく「検証されていない」を意味する**。これは仮定ではなく実測された事故である:

- **#885**: mutation を当てるとその mutation 自身の find-anchor が対象ファイルから消えるため Check 362 が必ず RED になり、**意図した Check が 1 つも発火しなくても全 mutation が caught と報告**されていた（Check 362 導入以降ずっと）。帰属を正した瞬間に、`.well-known/mcp.json` を壊すと monolith が traceback で停止し **Check 343 が一度も走っていなかった** latent crash が露出した。
- **登録先の混線**: behavior mutation が consistency 側に登録されていた 6 件は e2e probe で一度も走らず、consistency probe では対応 Check が無いため恒久的に SURVIVED だった。

ゆえに find-anchor / test 題名 / no-op / 帰属 / 登録先の 5 面をすべて BLOCKING で機械強制する。

## How

- monolith が `_ctx = SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)` を組み、`checks_mutation_integrity.run(_ctx)` を呼ぶ（`exec` は使わない）。`ctx.check` / `ctx.errors` / `ctx.warnings` は **monolith と同一オブジェクトの参照**であり、合否・BLOCKING 伝播・exit code は分割前と byte-equivalent。
- 各 Check は `mutation_samples` を importlib で読み、`e2e/*.spec.js` と対象 shipped file を直接読む。monolith の共有 global（html / style / mainjs 等）に依存しないため ctx enrichment は不要。
- `_e2e_titles(src)` が e2e の test 題名を **引用符リテラルと backtick テンプレートの両記法**で抽出する。テンプレートは `${…}` 境界で静的セグメントへ分解し、フィールドがいずれかのセグメントの部分文字列なら解決とみなす（実行時 title は必ず全静的セグメントを含むため保守的かつ健全）。Check 379 と 397 が共用する。
- `_aggregate_check_numbers()`（monolith）が `CHECK_SOURCE_FILES`（本ファイルを含む）を横断し、docstring inventory（`  N.`）と section header（`# ── N.`）の bijection を Check 45 / 70 / 105 で強制する。

## Constraints

- **本ファイル自身を対象にする consistency mutation は登録できない**（mutation self-reference trap）。`mutation_probe` の `replace(find, replace, 1)` は first-only 置換であり、自己参照 find はファイル前方の自 entry を先に打つため実 target が無傷のまま「機能しない偽 SURVIVED」になる。非 vacuity は手動（replace-all → RED → 保存コピーから復元）で担保し、非登録理由を NOTE に明記する運用。
- Check の追加・変更時は docstring inventory・`# ── N.` section header・`check-repository-consistency-map.md`・`total-check-runbook.md` §9 を同一 commit で同期する（Check 45 / 70 / 105 が bijection を BLOCKING 強制）。
- 1,000 行上限（Check 365）と `docs/files` mirror bijection（Check 108）の対象。

## Change impact

- Check を足す/移す際は `CHECK_SOURCE_FILES` の登録と monolith からの `run(_ctx)` 呼び出しの両方が必要（片方だけでは silent に無効化される）。
- `_e2e_titles` の記法対応を狭めると、パラメタライズド e2e（security-proxy の ALL_ROUTES route-render loop / a11y-axe の route loop）に mutation を登録できなくなる（解決不能で false RED）。**安全網の最重要部分が mutation 未検証のまま残る**ため、記法の追加はあっても削除はしない。

## Audience-specific notes

- **AI（後任）**: 「gate が RED になった」と「意図した Check が捕捉した」は別物。非 vacuity の実証では *どの* Check / assertion が落ちたかまで帰属せよ。対照 mutation（どの Check も見ない inert な変更）が帰属の検査に効く。
- **人間（新卒）**: このファイルは「テストのテスト」を機械化したもの。テストが通っているという事実と、テストが意味のある検査をしているという事実は別、という原則の実装。
- **監査人**: 安全網の健全性は `npm run mutation-probe`（consistency）と `npm run mutation-probe-e2e`（behavior）の出力で確認できる。CI は前者を回さないため、本 Check 群が静的な代替ゲートとして機能する。
