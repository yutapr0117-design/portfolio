---
file: .github/scripts/rehearse_version_freeze.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
canonical-ref: .github/scripts/prepare_version_freeze.py (予行する道具) / .github/workflows/mutation-probe.yml (週次の実行)
---

# .github/scripts/rehearse_version_freeze.py

## What

確定の道具が今の tree で確定まで届くことを、使い捨ての worktree で確かめる。作業ツリーは触らない。

## Why

`prepare_version_freeze.py` は確定の日にしか走らない。本文やドシエの形が変わって壊れても、確定の日まで分からない。Check 489 の道具と同じ問題だが、これはファイルを書き換えるので consistency の中では走らせられない。

## How

```sh
python3 .github/scripts/rehearse_version_freeze.py
```

HEAD を別の worktree に取り出して確定の道具を走らせ、新しい file を明示パスで add し、consistency を回す。RED が `EXPECTED` の中に収まれば成功である。週次の `mutation-probe.yml` の `freeze-rehearsal` job が回す。

## Constraints

- HEAD を見る。commit していない変更は予行に入らない。
- `EXPECTED` は確定の直後に残って正しい RED の一覧である。一覧の外の RED は、確定の日に止まる場所が増えたことを意味する。
- 道具を壊して試した。`FROZEN TEXT` を別の語にすると Check 490 が一覧の外に出て失敗した（2026-11-07）。

## Change impact

確定の手順を変えて残る RED が変わったら、`EXPECTED` と `prepare_version_freeze.py` の mirror doc の表を合わせる。

## Audience-specific notes

- **AI**: 週次の失敗は Issue に押し出される。一覧の外の RED が出たら、確定の日より前に直す。
- **監査人**: 確定後の verify と behavior e2e は 2026-11-06〜07 に手で 1 回測った（verify exit 0、495 件通過）。週次の job が見るのは consistency までである。
