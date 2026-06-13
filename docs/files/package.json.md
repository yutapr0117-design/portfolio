---
file: package.json
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: package-lock.json / Check 38/46/50/54/69
---

# package.json

## What

npm manifest。`private: true`、`type: "module"`、`scripts` (check / lint / lint:css / lint:js / test:e2e / verify)、`devDependencies` (eslint / @eslint/js / stylelint / @playwright/test / http-server / globals)、`engines.node` (`^20.19.0 || ^22.13.0 || >=24`) を定義。

## Why

dev-tooling-only manifest。public site はランタイム依存ゼロ (C1 Boring Technology)。npm scripts を単一真値として CI workflow と一致させる。

## How (usage)

```
npm ci → devDependencies install
npm run check / lint / lint:css / lint:js / test:e2e
npm run verify (= check + lint:css + lint + lint:js)
```

## Constraints

- **Check 23**: JSON 構文 valid
- **Check 38**: package-lock.json と sync + private + no runtime dependencies
- **Check 46**: lint scripts が同じ JS file set をカバー
- **Check 50**: lint script に legacy eslintrc 系 flag なし
- **Check 54**: eslint と @eslint/js が同じメジャー
- **Check 69**: engines.node が CI node-version pin (24) を許容

## Change impact

- script 名変更 → CI workflow 全部同期
- dependency 追加 → 必ず package-lock.json も更新

## Audience-specific notes

### For AI agents
- 役割タグ: `npm-manifest`, `dev-tooling-only`, `private-package`

### For human engineers (新卒レベル)
- `npm run <script>` で実行できるものはここに定義
- 「public site にランタイム依存追加するか」は C1 違反になるので要 orchestrator OK

### For third parties
- C1 Boring Technology の dev-tooling-only manifest 実装例
