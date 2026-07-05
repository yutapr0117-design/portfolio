---
file: .github/scripts/checks_jsonld_entity.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_jsonld_entity.py

## What

`check_repository_consistency.py` 分割トラックの 18 個目の split module。index.html JSON-LD の Person / WebSite / WebPage / Organization ノードが canonical URL・entity 事実と一致することを守る連続クラスタ Check **191-200** を内包し、`run(ctx)` で monolith から呼ばれる。

- 191(CNAME absence) / 192(Person.url) / 193(WebSite.url) / 194(WebPage.url) / 195(Person.alternateName variants) / 196(Organization.name=株式会社日本経営) / 197(Organization.url=nkgr.co.jp) / 198(Person.jobTitle role markers) / 199(Person.knowsAbout anchors) / 200(Person.@id canonical derivation)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 21**）。191-200 は「JSON-LD Person/WebSite/WebPage/Organization canonical entity coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は index.html を自前で `read_text()` し global content 依存なし。annotation+def-aware free-var 分析で外部依存ゼロ確認。global→nonlocal 変換 0 箇所。READ-ONLY coherence 検査ゆえ C6 対象外。**mutation-anchor: 192-200 の mutation（`mutation_samples_archive.py`）は index.html(JSON-LD content) を mutate する（check.py コードでない）ため anchor 追従は不要 — Check 362 は index.html の find-anchor を検証し、それは移動していない。**

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 190 の後・201 の前）**で `checks_jsonld_entity.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  191.`〜`  200.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 10,505 → 10,025（−480・Phase 21）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `jsonld`, `entity-coherence`, `phase21`
- **mutation-anchor 追従の判断**: 抽出 Check の mutation が **shipped file**(index.html 等) を mutate する場合は anchor 追従不要（find-anchor が移動しない）。**check.py の *check コード自体* を mutate する場合のみ**（Phase 20 の Check 337 型）新 module へ `"file"` 追従。`grep -n "Check NNN" mutation_samples*.py` で entry を見て `"file": CHECK` かどうかを判別せよ。
- 残ターゲット（clean・def-aware 確認済）: 175-180(6) / 202-207(6) / 209-214(6) / 216-219(4) / 221-235(15) / 242-249(8) / 251-254(4) / 256-261(6) / 341-347 / 351-359。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 18 個目。今回は「検索エンジン向け構造化データ(JSON-LD)の本人・会社・サイト情報が正しい URL/名前になっているか確かめる 10 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 18 split module 横断で緑（Phase 21 で 10,505→10,025）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
