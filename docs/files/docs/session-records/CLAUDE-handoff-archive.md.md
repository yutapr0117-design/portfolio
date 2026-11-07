---
file: docs/session-records/CLAUDE-handoff-archive.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-11-07
canonical-ref: CLAUDE.md §7 / docs/architecture/total-check-runbook.md §9
---

# docs/session-records/CLAUDE-handoff-archive.md

## What

`CLAUDE.md` §7 から移した run ごとの記録の読み取り専用アーカイブ。2026-06-15〜2026-09-09 の「終わりなき改善」の run 58 項目で、各 run の実バグ、新しい Check、教訓、「実測して clean と確認済み（再監査不要）」の一覧を持つ。

## Why

`CLAUDE.md` は全 session と全 subagent に毎回読み込まれる。移す前は 443,549 バイトのうち 96% が §7 で、workflow の agent は開始時点で約 1.65 MB の transcript を持っていた。2026-11-07 に 13 体の agent が 555 万トークンを使って利用上限に当たり、この固定費が主因と分かった。Check 365 は行数を見るので、1 項目が 1 行の §7 の肥大は見えていなかった。

## How (usage)

監査や増分に着手する前に、その面が既に見られていないかをここで grep する。

```
grep -n '再監査不要' docs/session-records/CLAUDE-handoff-archive.md | cut -c1-200
grep -n 'PR #1224' docs/session-records/CLAUDE-handoff-archive.md | cut -c1-200
```

## Constraints

- **本文は移した時点のまま**: 歴史記録なので書き換えない。古い数字も、書かれた時点の値として残す
- **規則と現在の状態はここに無い**: それらの権威は `CLAUDE.md` §7 と `AI2AI.md`
- **NOT in AIO discovery layer**: `CLAUDE.md` と同じく dev-tooling 専用。sitemap / robots / aio-manifest に登録しない

## Change impact

- 文中の「§7」「本 §7」「§9」は書かれた時点の節を指すので、節番号が変わっても直さない
- `CLAUDE.md` §7 が再び伸びたら、古い run をここへ追記して移す。Check 365 の 1,000 行に近づいたら 2 つ目のファイルを起こす

## Audience-specific notes

### For AI agents
- 役割タグ: `archive`, `read-only`, `dev-tooling`
- 全文を読まない。grep して該当の項目だけを読む

### For human engineers (新卒レベル)
- どの実バグをどう見つけて直したかの実例集として読める

### For third parties (監査 / 採用 / 研究)
- AI 自走の run ごとの成果と自己訂正の記録
