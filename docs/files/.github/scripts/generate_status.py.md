---
file: .github/scripts/generate_status.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-10
canonical-ref: STATUS.md (output) / Check 121 (freshness enforcement)
---

# .github/scripts/generate_status.py

## What

オーナー向け `STATUS.md`（root の機械生成 BLUF）を authoritative ソースから決定論的に生成する Python スクリプト。`npm run status` から呼ばれる。`build_status()` が本文を組み立て、`main()` が `STATUS.md` へ書き出す。

## Why

AI-only 自走リポジトリで、オーナーがコードを読まずに現況を一目把握する手段（STATUS.md）を drift なく維持するため。**オーナーの runtime 役割は「制御（goal/priority 提示）と監査（CI オールグリーン確認）」だが、STATUS.md には当初 URL が 1 つも無く、スマホでその監査を実行する手段が無かった**（2026-08-10 に監査導線を追加）。hand-maintain な dashboard は stale 化し誤情報になる。生成を 1 つのスクリプトに集約し、`build_status()` を Check 121 が import して regenerate-compare することで鮮度を機械強制する。

## How (usage)

```
npm run status   →  python3 .github/scripts/generate_status.py  →  main() → STATUS.md 書き出し
build_status()   →  AI2AI.md から Pipeline-Version / 最新 Session Record # を正規表現で抽出し
                    エンティティ/運用モデル/ポインタを含む BLUF テキストを返す (決定論的・volatile 値なし)
                 →  監査導線も **導出** する: CLAUDE.md の canonical URL から owner/repo を割り出し、
                    `.github/workflows/*.yml` を 2 群に分けて live badge + 実行履歴リンクにする。
                      (a) `pull_request:` で起動 = merge を守るゲート
                      (b) `schedule:` で起動 = 定期実行。**PR を止めないので赤くても誰にも届かない**
                          ため別枠 + 但し書きを付ける (安全網の自己検証 = mutation-probe / 週次 AIO
                          監視 = aio-monitoring がここに属する)
                    全ワークフロー履歴 / 未マージ PR / 公開サイトへのリンクも出す。
                    **トリガ判定は全文からコメント行を除いた上で `on:` ブロックだけを走査する**
                    (2026-08-10 修正: 以前は先頭 800 文字しか見ておらず、33 行の WHY コメントヘッダを
                    持つ mutation-probe.yml は `on:` が窓の外に落ちて **導出から silent に消えていた**。
                    「ハードコードしないので追従する」と謳う導出そのものが実態を覆っていなかった)
Check 121        →  generate_status を import し build_status() == committed STATUS.md を検証
Check 415        →  **生成器と独立に** workflow を直接 parse し、PR ゲート ∪ 定期実行の全 workflow が
                    STATUS.md にバッジを持つことを検証 (121 は「STATUS.md が生成器の出力と一致するか」
                    しか見ないため、生成器の導出バグ自体はこの層でしか捕まらない)
```

## Change impact

- 出力フォーマット変更 → `npm run status` で STATUS.md 再生成し同コミットで同期（Check 121）
- 埋め込みソース追加時は volatile（per-commit で変わる）値を避ける（低 churn 維持）

## Constraints

- **Python 3.10+ guard** 必須（Check 104。npm から呼ばれる .github/scripts/*.py の規律）
- **決定論的**であること（timestamp 等の volatile 値を出力に含めない＝Check 121 が安定）
- **Check 10**: py 構文妥当 / **Check 108**: docs/files mirror bijection（本ファイルがその mirror）

## Audience-specific notes

### For AI agents
- 役割タグ: `generator`, `owner-dashboard`, `deterministic`
- build_status() は副作用なし（純生成）。main() のみ書き込み。Check から安全に import 可

### For human engineers (新卒レベル)
- 「現況サマリを作る小さな生成器」。出力は STATUS.md、起動は `npm run status`

### For third parties
- machine-generated dashboard を regenerate-compare で drift-free に保つ generator 実装例
