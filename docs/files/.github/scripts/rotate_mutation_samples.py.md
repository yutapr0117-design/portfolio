---
file: .github/scripts/rotate_mutation_samples.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-26
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

## 2026-08-26 の是正 —— 「道具が宣言どおりに仕事をしていなかった」5 件

この道具は「無限に伸びる append-log を止める」ために在るのに、実測すると次の 5 つが壊れていた。いずれも**普段は動くが、いちばん助けが要る局面でだけ**壊れる形だった。

| # | 何が壊れていたか | どう分かったか |
|---|---|---|
| 1 | `_wire_new_archive` が **`if __name__` ガードより後ろ**で定義され、**CLI 実行時は未定義**だった。docstring が宣伝する「受け皿が埋まったら次を起こす」機能は `npm run rotate-mutations` から**一度も動いたことがない** | サンドボックスで CLI 実行し `NameError` を実測。**Check 456** で構造封じ |
| 2 | 同関数が **E2E 側の名前をハードコード**。consistency 側から呼ばれると (a) 同番号の E2E 変数がある場合は早期 return して**何も書かない**（受け皿は作られるが参照されず entry が消える）、(b) 無い場合は `from mutation_samples_archive4 import E2E_MUTATIONS_ARCHIVE4` を書き **ImportError** で `mutation_samples.py` が import 不能 = consistency ゲート自体が動かなくなる | 両分岐を実測。名前を chain から導出する形へ |
| 3 | `CHAINS` が **file 名のハードコード list**。`_pick_archive` が新しい受け皿を起こしても追加されず、その archive は rebalance の対象外になる ——「溢れた archive に自動の逃げ道が無い」という rebalance 導入の動機がそのまま再発する | disk から導出。導出結果が旧 list と完全一致することを control として確認 |
| 4 | 受け皿選びが **BLOCKING 基準**（`1000 - 60`）だったので、選んだ先が **advisory (950) を跨ぐ**。**advisory を意味あるものに保つ道具が、鳴りっぱなしの advisory を作っていた** | 実測: 1 回の rotate で e2e_archive が 957 行。基準を `ARCHIVE_TARGET` へ |
| 5 | `_rebalance()` が rotate の**前だけ**で走るので、溢れさせた受け皿を**同じ実行では直せない** | rotate 後にも実行。加えて §2 の実測行数を道具自身が同期する（Check 424 が BLOCKING で要求するため、手作業に頼ると必ず忘れる） |

**設計上の合意**: 1 回の実行で tree が緑になるところまでを道具の責任にする。「同期すること」と print で人に頼むのは、この道具が生まれた動機（毎回その場で分割スクリプトを書き起こしていた）と同じ誤り。

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
