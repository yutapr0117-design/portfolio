---
file: .github/scripts/submission_gate.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-23
canonical-ref: LICENSES/REVISION-PROTOCOL.md (§3.6 の 6b・6c) / LICENSES/FROZEN.md (POSTED-VERSION marker) / .github/scripts/prepare_version_freeze.py (gate_6b・gate_6c)
---

# .github/scripts/submission_gate.py

## What

凍結済みの版 (`ACD-1.4` など) を license-review へ出す日に、段 6b (license-discuss に届いてから 30 日) と 6c (未読 0・反映・写しの鮮度) を確かめる。6b は `FROZEN.md` の `<!-- POSTED-VERSION: ACD-x.y <届いた日> <公開アーカイブの URL> -->` から数え、拒否の道 (`POSTING-REJECTED` と `STAGE-6B-DECISION proceed`) も読む。6c は `prepare_version_freeze.gate_6c` をそのまま使う。何も書き換えない。`posted_problems` は Check 453c が毎回使う。

## Why

1.4 は list に出す前に `--not-for-submission` で確定したので、1.4 そのものを出す日には確定の道具 (gate_6b) が回らず、6b を見る機械が無かった (2026-11-23・6d の指摘)。

## How (usage)

```sh
python3 .github/scripts/submission_gate.py ACD-1.4
```

## Constraints

届いたことは公開アーカイブで確かめてから marker を書く (送信控えでなく・ゲート 10)。投稿の文はオーナーが書く (B14)。30 日は助言 (Chestek 氏 2026-01-23) であって規則ではない。

## Change impact

marker の形を変えたら `POSTED` / `REJECTED` の正規表現と Check 453c を同じ commit で直す。

## Audience-specific notes

- **統合**: 提出の日はこの道具が OK を出してから、オーナーへ文面の材料を渡す。
