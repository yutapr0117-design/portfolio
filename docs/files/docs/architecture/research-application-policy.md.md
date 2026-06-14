---
file: docs/architecture/research-application-policy.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: CLAUDE.md §5 / Deferred backlog
---

# docs/architecture/research-application-policy.md

## What

research 規律 ポリシー。「research は適用されて初めて完了」原則 + apply / defer-with-reason / verify-currency の 3 分岐 + Defer 理由のカタログ (safety gate / standard-not-final / strategy-mismatch)。

## Why

research を「読んで終わり」にせず必ず apply / defer / verify のいずれかに着地させる規律。CLAUDE.md §5 で定義された Loop の Research discipline 部分の根拠。

## How (usage)

新規 research を行ったとき本 policy に従って着地先を決める。Deferred backlog (WCAG 2.2 / CWV / IETF AIPREF 等) の rationale はここに記録。

## Change impact

- 新 deferred 項目 → 本ファイルに rationale 追記 + CLAUDE.md §7 に backlog 反映

## Audience-specific notes

### For AI agents
- 役割タグ: `policy`, `research-discipline`, `deferred-backlog-rationale`

### For human engineers (新卒レベル)
- research は読んだら必ず apply / defer / verify-currency のどれかに着地

### For third parties
- research-driven 改善の規律実装
