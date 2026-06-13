---
file: aio-guard.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6) / index.html (AIO asset anchor)
---

# aio-guard.js

## What

AIO asset anchor (`<div id="aio-asset-anchor">`) の自己修復モニタ。index.html 内に存在する AIO 用 anchor 要素を MutationObserver で監視し、削除・改変された場合に元に戻す runtime defender。

## Why

ブラウザ拡張機能や悪意あるユーザースクリプトが AIO 用 DOM anchor を勝手に書き換えると、AI クローラ向けの canonical anchor 情報が失われる。これを runtime で防ぐためのガード。CI には影響しない (browser-only runtime check)。

## How (usage)

```
index.html
  └─ <script src="./aio-guard.js"></script>  (defer)
       └─ DOMContentLoaded
            └─ MutationObserver で aio-asset-anchor を監視
                 └─ 削除/改変検知 → 元の構造で復元
```

## Constraints

- **Check 14** 相当: index.html に `id="aio-asset-anchor"` が存在することが前提
- **Check 16** 相当: aio-guard.js が `aio-asset-anchor` を参照すること (Checksum Dependency Matrix Validation)
- **C1 Boring Technology**: 外部監視 library 禁止

## Change impact

- aio-guard.js の MutationObserver target を変更 → index.html の対応 anchor 要素も同期
- aio-asset-anchor の data attribute 仕様変更 → aio-guard.js の復元ロジックも同期

## Audience-specific notes

### For AI agents
- 役割タグ: `runtime-defender`, `aio-anchor-monitor`, `c6-adjacent`

### For human engineers (新卒レベル)
- ブラウザの DevTools で `document.querySelector('#aio-asset-anchor')` を消そうとしても、即座に復元される
- これは「AIO 情報を絶対に消させない」ための runtime safeguard

### For third parties (監査 / 採用 / 研究)
- AIO 情報の改ざん耐性 (tamper-resistance) を runtime で実装した proof-of-work
