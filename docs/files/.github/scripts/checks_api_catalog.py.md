---
file: .github/scripts/checks_api_catalog.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .well-known/api-catalog (検証対象) / docs/files/.well-known/api-catalog.md
---

# .github/scripts/checks_api_catalog.py

## What

`.well-known/api-catalog`（RFC 9727 の API Catalog）の適合性を守る Check 群（**165 / 449**・どちらも BLOCKING）を所有する split module。`checks_seo_meta.py` から「api catalog」カテゴリとして切り出した。

- **Check 165** — valid JSON + `linkset` が非空 array + `linkset[0].anchor` が canonical URL prefix を持つ（**構造**の層）
- **Check 449** — RFC 9727 / 9264 / 6573 の**関係型セマンティクス**（**意味**の層）
  - **449a** `api-catalog` 関係は「別の API カタログへの入れ子」のみ（メンバー列挙に使わない）
  - **449b** `service-desc` / `service-meta` / `service-doc` / `status` を link object の attribute に混ぜない
  - **449c** 全 link object が文字列 `href` を持つ

## Why

`/.well-known/api-catalog` は「このサイトの API / AIO 入口は何か」への機械可読な真値で、**視覚に一切出ない**。screenshot にも behavior e2e にも現れないため、**仕様適合だけが唯一の検証手段**になる。

構造と意味を別 Check に分けているのは、**構造が正しいまま意味だけが壊れうる**から。実際 2026-08-23 に、メンバー 7 件すべてが `api-catalog` 関係で列挙されている状態（= それら全てを「別のカタログ」だと偽って宣言している状態）が発見された。JSON は妥当で anchor も正しいので Check 165 は緑のままで、仕様に従う agent だけが `llms-full.txt` を linkset として parse しようとして失敗する。

## How

`.well-known/api-catalog` と `index.html` を直接読む。monolith の共有 global（html / style / mainjs 等）には依存しないため ctx enrichment は不要。`run(ctx)` は monolith と同じ `check` / `ROOT` オブジェクトを参照で受け取る（`exec` 不使用）ので、append の意味論・BLOCKING の伝播・exit code は monolith と byte-equivalent。

449 は linkset の全 context / 全関係 / 全 link object を走査する。`api-catalog` 関係の href は「`/.well-known/api-catalog` で終わる」ことを条件にしており、**正当な入れ子（別サイトのカタログを指す）は通す**。

## Constraints

- **外部仕様がリテラル**: `item` / `service-*` / `api-catalog` という関係名は **RFC 由来でリポジトリから導出できない**ため本 module にリテラルで持つ。**RFC が更新されたら同一 commit で本 module も更新する**契約。
- **Check 45 / 70 / 105**: docstring inventory ↔ `# ── N.` section ↔ check-map 行 ↔ runbook §9 総数の 4 面が同期していること。
- **Check 431**: 実在 ⟺ `CHECK_SOURCE_FILES` 登録 ⟺ `run(_ctx)` 呼び出し。

## Change impact

- Check 追加 → docstring inventory + `# ── N.` section + check-map 行 + runbook §9 総数を同一 commit で同期
- `.well-known/api-catalog` にエントリ追加 → `linkset[0].item` へ（`api-catalog` ではない）
- 本 module のファイル名変更 → `CHECK_SOURCE_FILES` / dispatch / mirror doc の 3 箇所

## Audience-specific notes

### For AI agents

- 本 module は「**宣言と実態の乖離**」を守る層のひとつ。機械可読面の宣言は視覚に出ないため、**実際に何件マッチするか / 仕様原文に照らして何を意味するか**を実測してから結論を出すこと。
- 仕様は要約でなく**原文**で読む（本 Check は RFC 9727 原文の「the 'item' [RFC6573] link relation identifies a target resource that represents an API that is a member of the API catalog」に基づく）。

### For 監査人

- 165 = 構造層 / 449 = 意味層、という二層設計。片方が緑でももう片方が壊れうる。
- 449 の非 vacuity は 3 部それぞれを単独で壊して RED を実測済（check-map の 449 行に記録）。

### For 学術研究者 / 第三者

- RFC 9727（API Catalog）/ RFC 9264（Linkset）/ RFC 6573（`item` 関係）の 3 仕様に同時に従う面を、CI で機械強制している実例。
