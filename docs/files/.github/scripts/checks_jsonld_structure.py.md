---
file: .github/scripts/checks_jsonld_structure.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: .github/scripts/check_repository_consistency.py (CHECK_SOURCE_FILES) / .github/scripts/checks_shipped_hygiene.py (切り出し元) / docs/architecture/file-size-budget.md
---

# .github/scripts/checks_jsonld_structure.py

## What

index.html の JSON-LD の Schema.org 構造を守る Check **244〜247** を持つ split module。`run(ctx)` で `check_repository_consistency.py` から、`checks_shipped_hygiene.py` の直後に呼ばれる。

- 244: `@graph` の全 top-level node が非空の `@type` を持つ。
- 245: FAQPage の `mainEntity` が Question + name + acceptedAnswer（Answer + text）の形である。
- 246: BreadcrumbList の `itemListElement` が ListItem + position（整数）+ name + item の形である。
- 247: ImageObject / AudioObject / VideoObject が name と contentUrl（または url）を持つ。

## Why

2026-11-15 に `checks_shipped_hygiene.py` が 958 行で advisory（950）を越えた。予算は上げず（CLAUDE.md §7 の教訓 (8)）、互いに独立した連続の区間を移した。4 つの区間はどれも index.html を自分で読み、他の区間の変数に依らない。照合の中身と実行の順は変えていない（切り出しの前後で 244〜247 の OK 行が同じ）。

## How (usage)

単独では走らせない。`npm run verify`（`check_repository_consistency.py`）の中で走る。

## Constraints

- READ-ONLY。index.html を読むだけで、AIO の公開層は書き換えない（C6 の対象外）。
- 区間とラベルは `# ── N.` の形を保つ（Check 45 / 70 / 105 が CHECK_SOURCE_FILES を横断して数える）。

## Change impact

- 244〜247 の照合を変えるときは、この module を直す。`checks_shipped_hygiene.py` には残っていない。

## Audience-specific notes

### For AI agents（次担当）

- JSON-LD の構造の Check を足すときはこの module に足す。

### For human engineers（新卒レベル）

検索エンジンや AI が読む構造化データ（JSON-LD）の形が正しいかを確かめる検査の置き場。

### For third parties / auditors

検査の中身は切り出しの前と同じで、置き場所だけが変わった。
