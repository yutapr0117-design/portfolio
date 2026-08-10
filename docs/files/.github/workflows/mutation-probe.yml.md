---
file: .github/workflows/mutation-probe.yml
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-10
canonical-ref: .github/scripts/mutation_probe.py (runner) / .github/scripts/mutation_samples.py (データ) / .github/scripts/checks_mutation_integrity.py (Check 362/379/380/397/399/409)
---

# .github/workflows/mutation-probe.yml

## What

**安全網そのものの自己検証**を週次で走らせる GitHub Actions ワークフロー。

> **2026-08-10: consistency と behavior を並列の別ジョブへ分割した。** 実測（run 31397732391）は
> **全体 38m48s / consistency 約 10 分（306 mutations）/ behavior 約 29 分（143 mutations）** で、
> 直列だったため wall-clock は両者の和になっていた。並列化で **約 29 分（= 遅い方）** になり 26% 短縮する見込みだった。**分割後の実測（run 31405115213・2026-08-10）は 30m14s**（consistency 9m03s / behavior 30m08s）で、予測どおり。**22% 短縮**（38m48s → 30m14s）。
> 下の「45 分を超えたら rotate か分割を検討」の閾値には**まだ達していない**が、mutation は増分ごとに
> 増える一方で、超えてから動くと「安全網の検証が止まっている」ことに気付きにくい（この workflow は
> PR を止めないため、赤に気付けるのは STATUS.md のバッジだけ）。**閾値に当たる前に構造を直す。**
> 分割のもう一つの利点は **どちらの層が壊れたのかがジョブ単位で分かる**こと（従来は 1 つの赤としか
> 見えなかった）。consistency 側は playwright を使わないので `npm ci` / browser install も不要になる。

| ジョブ / ステップ | 内容 |
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

- **2 ジョブは互いに独立**（別の安全網を検証する）ため直列である必然性が無い。片方が落ちても
  もう片方の結果は知りたいので、`needs` で連結しない。
- **`pull_request` トリガを持たせない。** 20〜30 分かかるため merge ゲートにすると自走のリズムが壊れる。`STATUS.md` の監査バッジは `pull_request:` を持つ workflow だけを「ゲート」として導出するため、この workflow はバッジ対象外になる（意図どおり）。
- `permissions: contents: read` のみ（コミットも Issue 作成もしない・Check 68 の明示 permissions 要件）。
- `concurrency` で多重実行を抑止する。
- Check 107（runbook §11 の workflow 一覧 ↔ ディスク上の workflow）と Check 108（`docs/files` mirror bijection）の対象。

## 実 CI での検証済み実績（2026-08-10）

新設した workflow を `workflow_dispatch` で実際に走らせ、**実 CI 上で全 step が緑になること**を確認済み（run `31331210733`）。本セッションで「宣言はあるが実際には動かない」class を 2 件（WebMCP の DOM 抽出 / ルート追従 JSON-LD の無 gate）見つけた直後だったため、**自分が同じものを増やしていないことを実測で確かめた**。

| 項目 | 実測値 |
| :-- | :-- |
| 全体所要 | **34m18s**（425 mutations 時点）→ 38m48s（直列・449 mutations）→ **30m14s**（分割後・実測 run 31405115213） |
| consistency probe | ✓（当時 300 mutations） |
| behavior probe | ✓（当時 125 mutations） |
| working tree assert | ✓（復元漏れなし） |

**この数値の使いどころ**: `timeout-minutes: 60` に対し headroom は約 26 分（44%）。mutation は増分ごとに増える一方なので、**将来この timeout に静かに当たる**。当たってからでは「安全網の検証が止まっている」ことに気付きにくいので、目安として:

- 所要が **45 分**を超えたら rotate（最古の mutation を `mutation_samples_archive*.py` へ）か job 分割を検討する。
- 上の 34m18s は「300 + 125 = 425 mutations」時点の基準値。おおよそ **1 mutation ≒ 5 秒**として外挿できる。

## この workflow が実際に穴を見つけた記録（2026-08-10）

STATUS.md にバッジを出した直後（#964）、週次 run が **failure** で **4 件の behavior mutation が
SURVIVED** していた。PR CI では走らないため、**バッジが無ければ気付かないまま**だった。

| 段階 | 判明したこと |
| :-- | :-- |
| 1 回目（失敗） | 4 SURVIVED。うち 2 件は **mutation の find が非一意**で `replace(..., 1)` が別の場所を壊していた（probe が的を外していた）。1 件は **inert により観測不能**な mutation（原理的に捕捉不可）。 |
| #980 修正後 | **4 → 2**。anchor 一意化・実ガード（`setAppInert`）への付け替えが実 CI で効いた。**Check 420** で非一意 anchor を構造禁止（導入直後に 3 件目を検出）。 |
| #984 修正後 | **2 → 0**。残りは snapshot restore テストが click 直後に `__fatalError` を**待ちなしで単発読み**していた race（ローカルでは再現せず CI 負荷でのみ露見）。 |

**教訓**: この層は「安全網が本当に機能しているか」を検証する唯一の手段だが、**PR を止めないので
赤が届かない**。バッジ（#964）→ 発見（#980）→ 根治（#984）→ 分割で高速化（#983）という連鎖は、
**観測できるようにしたことが起点**だった。

## Change impact

- mutation を追加/変更したら、この workflow が週次で検証する。ローカルでの非 vacuity 実測（CLEAN=pass / MUTATED=fail）は依然として増分ごとの義務であり、本 workflow はその**取りこぼしを拾う網**であって代替ではない。
- 実行時間が伸びて `timeout-minutes: 60` に迫ったら、mutation の rotate（`mutation_samples_archive*.py` へ）か分割実行を検討する（判断の基準値は上の実測実績を参照）。

## Audience-specific notes

- **AI（後任）**: 挙動を変える修正をしたら、**関連する既存テストの非 vacuity を測り直せ**。テストは「壊れた」ではなく「鈍った」形で失われる（前提が崩れて緑のまま無力化する）。週次 run はその保険であって、増分ごとの実測の免除ではない。
- **監査人**: この workflow の run 履歴が「安全網が実際に機能していること」の時系列の証拠になる。
