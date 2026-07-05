---
file: .github/scripts/checks_shipped_static.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_shipped_static.py

## What

`check_repository_consistency.py` 分割トラックの 27 個目の split module。shipped JS/assets を静的走査する **tightly-coupled full-set** クラスタ Check **237/239/240/241/262/263/264/265/269/270/271/272/310**（13 checks・非連続）を内包し、`run(ctx)` で monolith から呼ばれる。

- 237(zero-ESM-import leaves) / 239(no eval/Function) / 240(no setTimeout-string) / 241(no document.write) / 262(no console.log) / 263(no debugger/alert) / 264(no TODO/FIXME comments) / 265(strict equality only) / 269(binary asset byte budget) / 270(text asset byte budget) / 271(root JS byte budget) / 272(leaf JS byte budget) / 310(total shipped weight budget)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 33**）。このクラスタは 3 重の内部共有で結ばれた unit: (1) `import glob as _glob237`（237 内・239/271/272 が使用）、(2) `_eval_targets239`（shipped-JS file+content list・239 内・240/241/262-265 が共有）、(3) `_HERO_WEBP269`/`_BGM_MP3_269`（binary asset path・269 内・Check 310 が消費 = **逆結合**）。**単純な部分抽出（237-272 のみ）は 271/272 の `_glob237` 参照 → 269 の `_HERO_WEBP269` を Check 310 が参照、で 2 度 crash した（安全網が検知）。解決 = 消費者 310 も含めた full-set を一括抽出し全共有 var を module-local 化。** annotation+def-aware free-var 分析でも「クラスタ内定義・外部使用」の逆結合は検出できず、`grep -nw` の外部消費者確認 + extract→NameError の安全網で確定した。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**Check 237 の元位置**で `checks_shipped_static.run(_ctx)` を呼ぶ。13 checks は list 順（237→239→…→272→310）で連続実行され、共有 var（glob import / `_eval_targets239` / hero+bgm path）が消費者より前に bind される（310 が最後）。順序非依存（各 Check は共有 errors/warnings に append するだけ・全出力 diff で byte-identical 実証）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json` + **`from pathlib import Path`**（Check 239 が Path 使用・初回抽出で NameError → 追加）。
- **mutation-anchor 追従**: 269/270/271/272/310 の 5 mutation（`mutation_samples.py`・budget-value を 1 byte に tighten する `"file": CHECK` 型）の target file を本 module へ更新（Check 362 が抽出時に orphan を BLOCKING 検知 → 追従）。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json`/`Path` のみ module import。`exec` 不使用。
- **full-set の完全性**: 237/239/271/272/310 が共有する glob・list・binary-path の定義元（237/239/269）と全消費者（310 含む）が本 module 内に閉じる。新たに shipped-static 系 Check を足す場合も本 module へ。
- **自己整合（Check 45/70/105）**: docstring inventory と section は 1 対 1、monolith と合わせて bijection。
- **mutation anchor 追従（Check 362）**: budget-value を mutate する 5 mutation の `"file"` は本 module。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 6,590 → 6,100（−490・Phase 33）。track 元 15,913 から **約 62%減**。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `shipped-static`, `lint`, `byte-budget`, `reverse-coupling`, `phase33`
- **最重要教訓（逆結合）: free-var analyzer は「クラスタ内で定義され外部で使われる var」（逆結合）を検出しない。抽出前に `grep -nw '<cluster内定義 var>' check.py` で外部消費者を確認し、消費者（非隣接でも）を cluster に含めよ。** また stdlib（Path 等）の import 漏れ・mutation-anchor orphan は安全網（extract→NameError / Check 362）が確実に捕捉する。
- 残ターゲット: ctx-enrich（style/html glob=174/187/220/250/255/344/356/360）/ helper 同梱（`_lib_csp_sri_hash`=350 / `_walkNNN`=190/201）/ 単発 clean（189/349）。以降は `_ctx` enrich が主軸。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 27 個目。公開 JS の静的検査(危険関数なし/ログなし等)とファイルサイズ予算の 13 検査をまとめて移した。これらは互いに変数を共有し、さらにサイズ合計の検査(310)が個別サイズの検査の変数を使うため、13 個を一緒に動かす必要があった（部分的に動かすと壊れる）。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 + Check 362 が monolith + 27 split module 横断で緑（Phase 33 で 6,590→6,100）。抽出前後の全 check 出力 diff で byte-equivalence を実証。部分抽出の 2 度の crash → full-set 解決という透明な試行錯誤の記録。
