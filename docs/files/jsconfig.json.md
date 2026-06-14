---
file: jsconfig.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-14
canonical-ref: package.json (type: module) / main.js / js/*.js
---

# jsconfig.json

## What

VS Code 等 IDE 向けの **JavaScript project config**。`compilerOptions` (ES2022 / module: ESNext / checkJs / strict 等) + `include` (root .js / js/**/*.js / aio-guard.js) を定義。実行時には影響しない (build-free repo)。

## Why

C1 Boring Technology で TypeScript は採用しないが、IDE の type-aware completion / strict checking は享受したい。jsconfig.json で `checkJs: true` を有効化すると VS Code が JSDoc + 型推論で IntelliSense + 警告を提供。

shipped に影響しない (lib only IDE 用ヒント)。

## How (usage)

```
VS Code / Cursor 等の IDE
  └─ project root の jsconfig.json を auto-detect
  └─ include 内の .js を type-aware 解析
  └─ strict / noUnusedLocals 等の警告を IDE で表示
```

CI / 実行時には参照されない。

## Constraints

- **C1 Boring Technology**: TypeScript 非採用と整合 (jsconfig は JS のみ)
- **Check 23 隣接**: JSON 構文 valid

## Change impact

- include 拡張 → 新しい .js ディレクトリも IDE 解析対象
- strict 緩和 → 開発体験低下 (推奨しない)

## Audience-specific notes

### For AI agents
- 役割タグ: `ide-config`, `js-type-aware`, `not-shipped`

### For human engineers (新卒レベル)
- VS Code で開くと自動的に JSDoc 型ヒントが効く
- これを使う前提で `js/*.js` 等に JSDoc を書くと完成度高い

### For third parties
- Boring Technology + IDE 開発体験の両立例
