---
file: .github/scripts/checks_canonical_https.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / docs/incident-artifacts/decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first split protocol) / docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
---

# .github/scripts/checks_canonical_https.py

## What

`check_repository_consistency.py` 分割トラックの 21 個目の split module。canonical URL・HTTPS-only・manifest/icon path の coherence を守る連続クラスタ Check **202-214** を内包し、`run(ctx)` で monolith から呼ばれる。

- 202(canonical trailing slash) / 203(Person given/family name) / 204(WebSite brand markers) / 205(JSON-LD url HTTPS) / 206(JSON-LD @id HTTPS) / 207(HTML src/href HTTPS) / 208(JSON-LD date ISO-8601) / 209(potentialAction target prefix) / 210(manifest start_url/scope) / 211(contentUrl/thumbnailUrl prefix) / 212(manifest icons src) / 213(link icon href) / 214(JSON-LD sameAs HTTPS)。

## Why

owner 合意 C-first の check.py 段階分割（**Phase 24**）。202-214 は「canonical URL / HTTPS-only / manifest-icon path coherence」という単一テーマの **連続 self-contained クラスタ**。各 Check は対象ファイル（index.html / manifest.webmanifest）を自前で読み global content 依存なし。**208 は freevars4 が tuple-unpack（`_y, _mo, _d = _v.split("-")`）で誤 gap 化していたが、extract→全出力 diff で実は self-contained と実証**（tuple-unpack false-positive の典型）。global→nonlocal 変換 0 箇所。202-214 の mutation は shipped file を mutate ゆえ Check 362 anchor 追従不要。READ-ONLY ゆえ C6 対象外。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**元の実行位置（Check 201 の後・215 の前）**で `checks_canonical_https.run(_ctx)` を呼ぶ（順序保存・連続ブロックゆえ reorder なし）。
- `run()` は `ROOT`/`check` を ctx から unpack し `import re, json`。
- `ctx.check`/`ctx.errors` は monolith と同一オブジェクト参照 → byte-equivalent。
- `_aggregate_check_numbers()` が `CHECK_SOURCE_FILES`（本ファイル含む）を横断集約。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re`/`json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  202.`〜`  214.`）と section は 1 対 1、monolith と合わせて bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- 新規 split module ゆえ Check 108 が本 doc を BLOCKING で要求。
- monolith 行数: 9,047 → 8,444（−603・Phase 24）。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `check-split`, `canonical-url`, `https`, `manifest-icon`, `phase24`
- **教訓（Phase 24）: freevars4 の tuple-unpack false-positive（`_y, _mo, _d = ...` を defined 認識しない）で誤 gap 化した section も、extract→全出力 diff + exit code の安全網が最終判定なので、疑わしければ含めて試し diff で確認せよ（208 が実例）。**
- 残ターゲット（freevars4-clean）: 216-219(4・218 global) / 242-249(8・245-247 global) / 251-254(4) / 256-261(6・global)。gap の多くは html/style glob（ctx-enrich 要）か `_walkNNN` 共有 nested-fn（helper 統合要）。

### For human engineers（新卒レベル）
- 巨大 1 ファイルを役割別に切り出す 21 個目。今回は「公開 URL が正規形か・HTTPS か・アプリ manifest のアイコンパスが正しいか確かめる 13 の検査」をまとめて移した。

### For third parties / auditors
- 各 PR で `npm run verify` exit 0・自己整合 Check 45/70/105 が monolith + 21 split module 横断で緑（Phase 24 で 9,047→8,444）。抽出前後の全 check 出力 diff で byte-equivalence を実証。
