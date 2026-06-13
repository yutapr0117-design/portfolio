---
file: js/aidk-rails.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: docs/architecture/main-js-extraction-map.md (Stage 5-l) / docs/architecture/repository-maintainability-map.md
---

# js/aidk-rails.js

## What

AIDK (AI Development Kernel) Rail 5 IIFE の合体 factory module (425 行)。`createAIDKRails({deps})` を export。RouteState / EffectRails / BindingRegistry / ActionDelegator / DiagnosticsRail の 5 つの内部 IIFE を合成する factory pattern モジュール。

## Why

main.js 内に分散していた AIDK Rail 系 5 IIFE を Stage 5-l で物理分割。closure-deps = none (引数注入) を維持しつつ、route state / effect / binding / action delegation / diagnostics の 5 軸を 1 モジュールに集約。

歴史: PR #37 で「Stage 5-l」として実装。同じ「Stage 5-l」命名は PR #33 (Meta Management) でも先に使われており、changelog 上は PR #33 を 5-k' とリネームして衝突回避 (Check 64 で番号衝突防止を機械強制)。

## How (usage)

```
main.js
  └─ import { createAIDKRails } from './js/aidk-rails.js'
  └─ const { RouteState, EffectRails, BindingRegistry, ActionDelegator, DiagnosticsRail }
        = createAIDKRails({ secureExternalLinks, openDrawer, closeDrawer, Theme, BGM })
```

葉モジュール契約: 自身は import 0 件 (`closure-deps = none`)。Check 47 で機械強制。

## Constraints

- **C2 IIFE**: 内部 5 個の IIFE 構造を保つ
- **factory pattern** (Check 56, 61): `export function createAIDKRails({...})` の object 引数形 + docstring に "factory pattern" マーカー
- **Check 47**: main.js との import/export bijection
- **Check 52**: 425 行 ≤ 550 (行数予算)

## Change impact

- factory signature 変更 → main.js の合成呼び出し + 注入される deps (Theme/BGM/openDrawer 等) と整合
- 5 IIFE の役割境界変更 → AIDK 全体の動作影響大

## Audience-specific notes

### For AI agents
- 役割タグ: `factory`, `aidk-rail`, `closure-deps-none`
- Export: `createAIDKRails` (factory)

### For human engineers (新卒レベル)
- factory pattern: `createXxx({deps})` で deps を引数注入する。globals を使わない (ReferenceError 防止 — Stage 5-j 教訓)
- 「AIDK Rail」は AI Development Kernel の補助システム群

### For third parties
- Stage 5 物理分割の代表例。factory pattern の確立と適用の証跡 (PR #37)
