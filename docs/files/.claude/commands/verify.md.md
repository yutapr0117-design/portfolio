---
file: .claude/commands/verify.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: package.json scripts / Check 77
---

# .claude/commands/verify.md

## What

`/verify` slash command。`npm run verify` を実行して check / lint:css / lint / lint:js の 4 層 + Check 1-99 を順次検証し、結果を BLUF で報告。

## Why

「念のため verify」を手早く実行できる定型コマンド。CI 待ち前にローカルで pre-check したいときに使う。

## How (usage)

```
/verify
└─ npm run verify
└─ exit code / layer 別 pass/fail / 失敗時の minimal fix 提案
```

## Constraints

- **Check 77**: frontmatter + description

## Change impact

- 出力フォーマット変更 → 後続 session の status 報告品質

## Audience-specific notes

### For AI agents
- 役割タグ: `slash-command`, `verify-runner`

### For human engineers (新卒レベル)
- 「commit する前にチェック」と思ったら `/verify`

### For third parties
- pre-commit verification の slash 化
