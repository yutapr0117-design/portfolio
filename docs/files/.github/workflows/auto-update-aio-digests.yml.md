---
file: .github/workflows/auto-update-aio-digests.yml
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: .github/scripts/update_aio_digests.py
---

# .github/workflows/auto-update-aio-digests.yml

## What

AIO 関連ファイル変更時の digest 自動再計算 workflow。AIO trigger paths (llms*.txt / aio-manifest.json / WebP / MP3 等) が push されると `update_aio_digests.py` を実行して digest 連鎖を同期、`[skip ci]` 付きで commit + push。

## Why

人間が AIO surface を編集して digest を忘れる drift を構造防止。冪等なので「digest 変わらない場合は no-op」。

## How (usage)

```
on:
  push to main
  paths: [llms.txt, llms-full.txt, AI2AI.md, aio-manifest.json, WebP, MP3, ...]
└─ checkout + setup-python
└─ update_aio_digests.py 実行
└─ git diff があれば commit "[skip ci]" + push
```

## Constraints

- **Check 23**: YAML 構文 valid
- **Check 67**: top-level permissions: contents:write
- **concurrency**: group per ref + cancel-in-progress: false

## Change impact

- trigger paths 拡張 → update_aio_digests.py の MANIFEST_PATH_TO_LOCAL と整合

## Audience-specific notes

### For AI agents
- 役割タグ: `auto-digest-sync`, `skip-ci-tag`

### For human engineers (新卒レベル)
- 編集して push するだけで digest が自動同期される
- `[skip ci]` 付きなので無限ループしない

### For third parties
- semantic 編集と derived value の auto-sync 実装例
