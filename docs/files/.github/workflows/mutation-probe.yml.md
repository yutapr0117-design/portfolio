---
file: .github/workflows/mutation-probe.yml
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-10
canonical-ref: .github/scripts/mutation_probe.py (runner) / .github/scripts/mutation_samples.py (データ) / .github/scripts/checks_mutation_integrity.py (Check 362/379/380/397/399/409)
---

# .github/workflows/mutation-probe.yml

## What

**安全網そのものの自己検証**を週次で走らせる GitHub Actions ワークフロー。

| ステップ | 内容 |
| :-- | :-- |
| consistency probe | `MUTATIONS` を 1 件ずつ当て、`check_repository_consistency.py` が Check 362（anchor orphan）**以外**の error を出すことを確認 |
| behavior probe | `E2E_MUTATIONS` を 1 件ずつ当て、`test` フィールドが指す playwright テストが実際に fail することを確認 |
| working tree assert | probe が全 mutation を復元したか（復元ロジックの回帰検出） |

SURVIVED（どの Check / e2e も捕捉しない mutation）が 1 件でもあれば run が落ちる。

## Why

consistency Check 群と behavior e2e は「**実装の**回帰」を守る。だが「**その安全網自体が回帰していないか**」は誰も守っていなかった。mutation probe が唯一の検出手段でありながら、**PR の CI では走らない**（behavior 側は mutation ごとに playwright を起動するため 20〜30 分かかり、全 PR に載せると merge 待ちが破綻する）。

結果としてこの層は「気付いた人が手で走らせる」だけの状態だった。実際 2026-08-10 の cross-tab 修正では、挙動を変えたことで**既存テストが新しい延期パスを踏み、何を壊しても緑になる**（＝安全網が黙って鈍る）事故が起きている。手動 probe で気付けたが、気付かなければ検出手段はゼロだった。週次実行はこの「気付けるかどうか」を運任せにしない。

## How (usage)

```
週次    : 毎週月曜 UTC 02:00（JST 11:00）。aio-monitoring.yml の 1 時間後にずらして負荷を分散
手動    : Actions タブから workflow_dispatch
ローカル: npm run mutation-probe / npm run mutation-probe-e2e（verify と連結しないこと）
```

失敗時の読み方:

- **SURVIVED** — その mutation を誰も捕捉していない。安全網の穴か、対応するテストが鈍った（前提が崩れた）かのどちらか。
- **CRASHED** — gate が traceback で停止した。「Check が働いた」ではなく「その Check は走らず、以降の Check も masking された」状態（Check 400 が構造的に封じている class）。

## Constraints

- **`pull_request` トリガを持たせない。** 20〜30 分かかるため merge ゲートにすると自走のリズムが壊れる。`STATUS.md` の監査バッジは `pull_request:` を持つ workflow だけを「ゲート」として導出するため、この workflow はバッジ対象外になる（意図どおり）。
- `permissions: contents: read` のみ（コミットも Issue 作成もしない・Check 68 の明示 permissions 要件）。
- `concurrency` で多重実行を抑止する。
- Check 107（runbook §11 の workflow 一覧 ↔ ディスク上の workflow）と Check 108（`docs/files` mirror bijection）の対象。

## Change impact

- mutation を追加/変更したら、この workflow が週次で検証する。ローカルでの非 vacuity 実測（CLEAN=pass / MUTATED=fail）は依然として増分ごとの義務であり、本 workflow はその**取りこぼしを拾う網**であって代替ではない。
- 実行時間が伸びて `timeout-minutes: 60` に迫ったら、mutation の rotate（`mutation_samples_archive*.py` へ）か分割実行を検討する。

## Audience-specific notes

- **AI（後任）**: 挙動を変える修正をしたら、**関連する既存テストの非 vacuity を測り直せ**。テストは「壊れた」ではなく「鈍った」形で失われる（前提が崩れて緑のまま無力化する）。週次 run はその保険であって、増分ごとの実測の免除ではない。
- **監査人**: この workflow の run 履歴が「安全網が実際に機能していること」の時系列の証拠になる。
