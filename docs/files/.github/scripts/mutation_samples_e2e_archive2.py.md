---
file: .github/scripts/mutation_samples_e2e_archive2.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-17
canonical-ref: .github/scripts/mutation_samples.py (hot log / 公開 API 合成) / .github/scripts/mutation_probe.py (runner) / .github/scripts/checks_mutation_integrity.py (Check 362/379/380/397)
---

# .github/scripts/mutation_samples_e2e_archive2.py

## What

**behavior (e2e) mutation の rotated アーカイブ (part 2)**。`E2E_MUTATIONS_ARCHIVE2` を 1 つだけ export し、`mutation_samples.py` が

```
E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE2 + _E2E_TAIL      # 順序 = 時系列 (古 → 新)
```

として公開 API を合成する。consistency 側の `mutation_samples_archive*.py` (`MUTATIONS_ARCHIVE` / `MUTATIONS_ARCHIVE2`) と同じ log-rotation 方式の e2e 版。

## Why

curated mutation は増分ごとに時系列で追記され**無限に成長する**。`Check 365`（全非 A テキストファイル ≤1,000 行 BLOCKING）に当たると「安全網にこれ以上 mutation を足せない」状態になるため、hot log を一定サイズに保つ必要がある。

**なぜ e2e 版が後から必要になったか**: consistency 側にだけ rotation 機構があり、`E2E_MUTATIONS` は単一リテラルのまま増え続けていた。2026-08-10 に hot log が **996 行**（Check 52 の advisory budget 975 超過・BLOCKING の 1,000 まで残り 4 行）へ到達し、**BLOCKING に当たる前に**先回りで機構を用意した（advisory → blocking の二層設計を、当たってから対処ではなく警告段階で使い切る運用）。


**なぜ 2 段目が必要になったか** (2026-08-17): part 1 自体が Check 365 の 1,000 行 cap に達した。
archive は「新規を hot log から押し出す先」なので、**archive も無限には伸ばせない**。consistency 側が
`mutation_samples_archive.py` / `archive2.py` の 2 段構成になっているのと同じ形へ揃えた。
rotation の向きは 新規 → hot log の tail → part 1 → part 2 で、どの段にあっても `E2E_MUTATIONS` へ
連結されるため mutation の総数と有効性は変わらない (Check 362/379/397/420 は連結後の全件に働く)。

## How (usage)

```
新規 mutation は常に mutation_samples.py の _E2E_TAIL 末尾へ追記する（本ファイルへ直接足さない）
hot log が advisory (975 行) を超えたら、_E2E_TAIL の最古ブロックを本ファイル末尾へ移す
さらに溢れたら mutation_samples_e2e_archive2.py を新設する（consistency 側 part2 と同じ）
```

移動しても `E2E_MUTATIONS` の**件数と順序は不変**であること（合成後に import して件数を確認する）が rotate の受け入れ条件。

## Constraints

- **entry の中身を編集しない**。ここは「過去に実在した回帰」の記録であり、対象コードが変わって find-anchor が解決しなくなったら `Check 362` が RED になるので、その時点で anchor を実態へ追従させる（＝アーカイブでも死んだデータではない）。
- `Check 379 / 397`（`test` フィールドが実在の e2e title へ一意解決）、`Check 380`（`replace != find`）、`Check 409/409b`（登録先と命名の分離）は archive の entry にも等しく適用される。
- `Check 365`（1,000 行）と `Check 108`（`docs/files` mirror bijection）の対象。

## Change impact

- 本ファイルを新設した際、`mutation_samples.py` 側は `from mutation_samples_e2e_archive import E2E_MUTATIONS_ARCHIVE2` と `E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE2 + _E2E_TAIL` の 2 行だけが変更点。**リストの実体は移動のみで、内容は 1 文字も変えていない**（rotate は非破壊であることが前提）。
- rotate 後は必ず `npm run mutation-probe-e2e` か、少なくとも `mutation_samples` の import で件数を確認する。順序が壊れると probe の実行順が変わるだけだが、件数が減っていれば安全網が痩せている。

## Audience-specific notes

- **AI（後任）**: 「hot log が大きくなったから古いものを消す」ではない。**移す**のであって捨てない — 過去の回帰を再現できることが安全網の価値そのもの。
- **監査人**: 安全網の総量は `MUTATIONS`（consistency）+ `E2E_MUTATIONS`（behavior）の合計で、archive を含めた数がその時点の総量。
