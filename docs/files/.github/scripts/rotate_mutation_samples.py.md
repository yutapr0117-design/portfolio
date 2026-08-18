---
file: .github/scripts/rotate_mutation_samples.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-18
canonical-ref: .github/scripts/mutation_samples.py / .github/scripts/mutation_probe.py / docs/architecture/file-size-budget.md
---

# .github/scripts/rotate_mutation_samples.py

## What

`mutation_samples.py`（mutation の hot log）が行数閾値を超えたとき、最古の entry を
`mutation_samples_e2e_archive2.py` へ移す 1 コマンド（`npm run rotate-mutations`）。

## Why

mutation は増え続ける append-log で、hot log には **Check 52 の advisory（975 行）**と
**Check 365 の BLOCKING（1,000 行）**がある。実運用では **advisory を素通りして BLOCKING に
当たる**事故が繰り返し起きた（#1067 / #1135 の 2 回）。

原因は「毎回その場で brace-aware な分割スクリプトを書き起こしていた」こと ——
**手順が人の注意力に依存していた**。同じ失敗を 2 回したなら、それは規律ではなく仕組みの問題。

## How (usage)

```
npm run rotate-mutations                                   # 必要なら rotate（既定 6 件）
python3 .github/scripts/rotate_mutation_samples.py --count 8
python3 .github/scripts/rotate_mutation_samples.py --check  # 判定のみ（超過なら exit 1）
```

rotate 後は **`file-size-budget.md` §2 の実測行数を同期する**（Check 424 が BLOCKING で強制。
スクリプト自身も最後にその旨を出力する）。

## Constraints

- **brace-aware でなければならない**: 素朴に `s.index('\n]')` で配列末尾を探すと、
  **entry の文字列リテラル内の `]`** に当たってファイルを壊す（実際に 982 → 197 行まで
  削った事故がある）。文字列の内外を追いながら bracket depth を数えるのが唯一安全
- **総数が変わらないこと**を rotate 後に `importlib` で自己検証する（移動であって削除ではない）
- **Check 104**: npm から呼ぶ Python は `sys.version_info < (3, 10)` guard が必須

## Change impact

- 閾値（`ADVISORY` / `BLOCKING`）を変えるときは Check 52 / Check 365 の値と揃える
- archive の追記先を変えるときは `mutation_samples.py` の
  `E2E_MUTATIONS = ARCHIVE2 + ARCHIVE + _E2E_TAIL` の連結順と整合させる

## Audience-specific notes

### For AI agents
- 役割タグ: `dev-tooling`, `log-rotation`, `safety-net`
- **`importlib` で件数を数えるときは `sys.modules` を必ず purge する** —— `mutation_samples.py` は
  archive 群を import するので、2 回目の呼び出しで**古い archive** が再利用され、rotate 直後の
  件数が更新前のまま返る（実測: archive へ 1 件足しても purge 無しでは 297 のまま / purge すると 298）。
  この状態で不変条件を検査すると **正しい rotate を「総数が変わった」と誤検出して落ちる**
  （実際に踏んだ。ヘルパー自身の安全弁が、自分の計測ミスで誤発火した例）

### For human engineers (新卒レベル)
- 「毎回手で同じ手順を踏む」ものは、2 回間違えたら自動化する合図

### For third parties
- 無限に伸びる append-log を、閾値と自動 rotation で運用可能に保つ実装例
