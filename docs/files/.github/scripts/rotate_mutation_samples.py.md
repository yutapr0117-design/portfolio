---
file: .github/scripts/rotate_mutation_samples.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-18
canonical-ref: .github/scripts/mutation_samples.py / .github/scripts/mutation_probe.py / docs/architecture/file-size-budget.md
---

# .github/scripts/rotate_mutation_samples.py

## What

`mutation_samples.py`（mutation の hot log）が行数閾値を超えたとき、最古の entry を
archive chain へ移す 1 コマンド（`npm run rotate-mutations`）。移動元は **`_E2E_TAIL` と
`_MUTATIONS_TAIL` のうち rotate 単位が多い方**を選び、移動先は **余裕を実測して**
対応する chain（`mutation_samples_e2e_archive*.py` / `mutation_samples_archive*.py`）
から選ぶ。埋まっていれば次の番号を起こし、import と連結式まで配線する。

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
- **rotate 単位は「literal entry ∪ `.append({...})` ブロック」**: 新しい mutation は必ず
  `NAME.append({...})` で足す規約なので、**成長は append 経由**。旧実装は `NAME = [ ... ]` の
  literal だけを排出対象にしており、**排出できる場所と増える場所が別**だった。literal が枯れると
  「rotate すると空になる」で止まり、append で溜まった entry には逃げ道が一つも無い
  （2026-08-23 に literal 6 件 / append 87 件で実際に詰んだ）。両方を同じ単位として扱い、
  **ファイル上の出現順（= 時系列順）**で古いものから排出する
- **entry 直前のコメントは運ばない**: `_split_entries` は entry の直前にあるコメント行を
  巻き込むが、それは hot log 固有の注記なので archive へ移すと文脈が壊れる。単位は `{` から始める

## Change impact

- 閾値（`ADVISORY` / `BLOCKING`）を変えるときは Check 52 / Check 365 の値と揃える
- archive の追記先を変えるときは `mutation_samples.py` の連結式
  （`E2E_MUTATIONS = …` / `MUTATIONS = …`）の順と整合させる（Check 430 が導出して検証する）

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
