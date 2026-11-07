---
file: docs/session-records/runbook-check-history.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-07
canonical-ref: docs/architecture/total-check-runbook.md §9 / docs/architecture/check-repository-consistency-map.md
---

# docs/session-records/runbook-check-history.md

## What

`total-check-runbook.md` §9 の「consistency Check 総数」の行に積まれていた、Check ごとの追加の経緯の読み取り専用アーカイブ。文の区切りで行に分けたほかは、移した時点のまま。

## Why

`.claude/CLAUDE.md` は session の開始時に runbook §9 を読むよう案内している。その行だけで 222,303 バイトあり、1 行のまま伸びるので Check 365 の行数の上限では気付けなかった。`CLAUDE.md` の §7 と同じ形の肥大なので、同じ日に移した。

## How (usage)

ある Check がいつ、なぜ足されたかを調べるときに grep する。

```
grep -n 'Check 361' docs/session-records/runbook-check-history.md | cut -c1-200
```

## Constraints

- **本文は移した時点のまま**: 歴史記録なので書き換えない。古い数字も、書かれた時点の値として残す
- **新しい Check はここへ足さない**: Check の内容の権威は `docs/architecture/check-repository-consistency-map.md`
- **NOT in AIO discovery layer**: dev-tooling 専用。sitemap / robots / aio-manifest に登録しない

## Change impact

- Check の番号が変わっても直さない。書かれた時点の番号を残す

## Audience-specific notes

### For AI agents
- 役割タグ: `archive`, `read-only`, `dev-tooling`
- 全文を読まない。grep して該当の項目だけを読む

### For human engineers (新卒レベル)
- 機械強制がどう増えてきたかの時系列として読める

### For third parties (監査 / 採用 / 研究)
- Check ごとの追加の理由の記録
