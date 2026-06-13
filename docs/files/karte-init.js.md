---
file: karte-init.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C7) / CLAUDE.md §2
---

# karte-init.js

## What

KARTE (https://karte.io/) タグの初期化スニペット。外部 CDN (`cdn-edge.karte.io` 等) を CSP `connect-src` / `script-src` で許可した上で読み込む analytics / customer experience tag。vendor snippet なので構造は KARTE 公式仕様に従う。

## Why

ユーザー行動の観測 (page-view / event / session) のため。GA4 を使わなかった理由は `docs/architecture/decision-*.md` 系の判断ログに記録 (KARTE は SPA 対応がより明確で、CSP / CSRF も明示しやすい)。

## How (usage)

```
index.html
  └─ <script src="./karte-init.js"></script>  (defer)
       └─ KARTE tracker init
            └─ external CDN: cdn-edge.karte.io / static.karte.io / b.karte.io etc.
                 (CSP connect-src で許可)
```

## Constraints

- **C7 KARTE CDN SRI Non-Application**: SRI 提案禁止 (external 更新があるため SRI を入れると prod load が壊れる)
- **CSP connect-src**: 6 KARTE host を `connect-src` で明示許可済
- **vendor snippet 保護**: 構造を勝手に変えない (KARTE 公式更新時のみ追従)

## Change impact

- KARTE host 追加/変更 → index.html CSP `connect-src` 同期 + AI2AI.md C7 Architecture Note 更新

## Audience-specific notes

### For AI agents
- 役割タグ: `vendor-snippet`, `analytics`, `c7-protected`, `csp-connect-src`

### For human engineers (新卒レベル)
- ここは KARTE 公式の vendor snippet なので、自分で書き換えない
- 「SRI を入れたい」と思っても禁止 (C7) — KARTE が edge.js を更新するたびに hash が変わって prod load が落ちるから

### For third parties (監査 / 採用 / 研究)
- 外部 SaaS analytics の組み込み + CSP / SRI 設計判断の証跡
