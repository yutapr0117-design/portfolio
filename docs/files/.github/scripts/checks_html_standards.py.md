---
file: .github/scripts/checks_html_standards.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_html_standards.py

## What

`check_repository_consistency.py` 分割トラックの 17 個目の split module。index.html の標準準拠・安全 hygiene と webmanifest / binary asset の integrity を守る連続クラスタ Check **324-337** を内包し、`run(ctx)` で monolith から呼ばれる。

- 324(affiliation.start_date 未来なし) / 325(referrer enum) / 326(preload as enum) / 327(no meta refresh) / 328(no base) / 329(no HTML4 deprecated) / 330(no iframe/object/embed) / 331(no javascript: URL) / 332(root classic-script no import/export) / 333(webmanifest anonymity) / 334(webmanifest orientation enum) / 335(manifest link resolve) / 336(og:image==twitter:image) / 337(binary magic-byte integrity)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 20**）。324-337 は「index.html standards/safety hygiene + webmanifest + asset integrity」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（index.html / manifest.webmanifest / root scripts / binary assets）を自前で読み global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。READ-ONLY hygiene 検査ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 323 の後・338 の前）**で `checks_html_standards.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- **mutation_samples 追従**: Check 337 の mutation（`_wh337[8:12] == b"WEBP"` を XXXX に mutate）の target file を `CHECK`（check.py）から本 module へ更新した（Check 362 = mutation anchor 整合が抽出時に orphan を検知 → 追従修正）。抽出時に対象 Check の mutation-anchor file を追従させる規律の実例。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  324.`〜`  337.`）と section は 1 対 1、monolith と合わせて bijection。
- **mutation anchor 追従（Check 362）**: 抽出した Check に mutation_samples の entry があれば、その `file` を本 module に追従させる（さもなくば Check 362 が orphan で BLOCKING）。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 11,070 → 10,505（−565・Phase 20）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `html-standards`, `hygiene`, `asset-integrity`, `phase20`
- **重要教訓（Phase 20）: 抽出する Check に mutation_samples.py の entry があると、その `find` anchor が check.py から移動して Check 362 が orphan を BLOCKING で検知する。抽出時に該当 mutation の `"file"` を新 module へ追従させよ（`grep -n "Check NNN" mutation_samples*.py` で確認）。** また mutation-probe を単独実行すると SIGTERM で shipped file（manifest.webmanifest 等）が mutated 残留しうる → `git checkout <file>` で復元（memory `feedback_mutation_probe_verify_race`）。
- 残ターゲット（clean・大型連続 run）: 191-200(10) / 221-235(15・global 235) / 242-249(8・global 245-247) / 256-261(6・global) / 202-207 / 209-214 / 351-359。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 17 個目。今回は「公開 HTML が古い/危険な要素を使っていないか・アプリ manifest とバイナリ資産が正しいか確かめる 14 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 17 split module 横断で緑（Phase 20 で 11,070→10,505）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
