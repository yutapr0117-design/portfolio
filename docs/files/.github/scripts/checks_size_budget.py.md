---
file: .github/scripts/checks_size_budget.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-26
canonical-ref: docs/architecture/file-size-budget.md (予算の単一ソース) / .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_maintainability.py (分離元)
---

# .github/scripts/checks_size_budget.py

## What

ファイルサイズ予算の**統治クラスタ** 9 Check を内包する split module。`run(ctx)` で monolith から呼ばれる。

| Check | 守る性質 |
|---|---|
| 52 | per-file の loose な予算超過を **ADVISORY** で警告する（早期警告層）|
| 365 | 全非 A 追跡テキストファイルを **1,000 行**で止める（ハードゲート層）|
| 363 | shipped JS logic-leaf の独立した hard ceiling |
| 71 | 予算に書かれた path が実在する（registered ⟹ exists）|
| 361 | shipped JS leaf が予算に登録済み（exists ⟹ registered・71 の対称）|
| 408 | e2e spec が予算に登録済み（同じ対称を spec 面で）|
| 424 | §2 表の「実測行数」が実際に `wc -l` と一致する |
| 443 | 予算値が hard ceiling より**厳密に小さい**（でないと早期警告が構造的に出ない）|
| 454 | 危険域（>800 行）の file が予算を**持っている**（無登録は 443 の検査対象にすら入らない）|

module-level に単一ソース定数（`HARD_CEILING` / `CEILING_EXEMPT_*` / `EARLY_WARNING_FLOOR`）を持ち、365 / 443 / 454 が共有する。

## Why

肥大化の抑制は**二層**で設計されている —— 「advisory で早めに気付き、BLOCKING で最終的に止める」。この二層が実際に機能するには、予算について 4 つの前提が同時に成り立っていなければならない。

1. **予算がある**（Check 454）
2. **値が妥当**＝ hard ceiling 未満（Check 443）
3. **対象が漏れていない**（Check 71 / 361 / 408）
4. **実測と一致する**（Check 424）

どれか 1 つでも欠けると、その file は **OK からいきなり BLOCKING へ飛ぶ**。実際にこの事故は 3 度起きている（#1067 / #1135、そして本 module を切り出した増分自身）。9 Check は独立した検査ではなく、**互いの前提条件を守り合う 1 つの機構**なので、同じ module に置く。

分離のきっかけも同じ現象だった。分離元 `checks_maintainability.py` は Check 454 を足した時点で **985 行 = hard ceiling まで残り 15 行**になった。**454 が塞ごうとしている当の現象を、454 を足した増分自身が踏んだ**。圧縮で誤魔化さず「いま触っているクラスタ」を切り出すのが本リポジトリの定型手である。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**`checks_maintainability.run(_ctx)` の直後**という元の実行位置で `checks_size_budget.run(_ctx)` を呼ぶ。
- `ROOT` / `check` / `warnings` を ctx から unpack。`ctx.check` / `ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播・exit code が byte-equivalent。
- 移した section は 1 行も書き換えていない。残留側が module-level 定数を参照しないことは抽出前に実測で確認した。

## Constraints

- **単一ソースを分けない**: `HARD_CEILING` と除外集合は Check 365 / 443 / 454 が共有する。片方に file を足してもう片方を忘れると「hard ceiling の対象なのに早期警告が要らないと判定される」逆の穴が開く。
- **advisory は上げて黙らせない**。超えたら「削れないか」を先に実測し、削れないなら**クラスタを切り出す**。ラチェットする場合は内訳を `file-size-budget.md` に書く。
- **自己整合（Check 45/70/105）**: docstring inventory と `# ── N.` section が 1 対 1 で、monolith と合わせて map / runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。

## Change impact

- Check を足すと自分自身の行数が増える。この module は**自分が守っている規律の対象でもある**ので、`EARLY_WARNING_FLOOR` を超えたら自分を BUDGET-DATA に登録すること。
- 予算値を変えるときは §2 表と §4 BUDGET-DATA の両方（Check 59 が集合一致を強制する）と、実測行数（Check 424）を同じ commit で同期する。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `size-budget`, `two-layer-gate`, `ctx-injection`
- **`EARLY_WARNING_FLOOR = 800` は根拠のある値ではなく、実測に基づく運用値**。導入時点で「hard ceiling 対象かつ 800 行超」は 24 file（うち未登録 7）で、閾値を 700 に下げると 29 file・900 に上げると 9 file だった。登録を要求する数が actionable に収まる範囲として 800 を選んだ。**下げるなら未登録の増加数を実測してから**。
- advisory を踏んだときの正しい順序: ①コメントを全部削っても収まらないかを**実測** → ②収まらないならクラスタを切り出す → ③それでも駄目ならラチェットし、内訳を doc に書く。

### For human engineers（新卒レベル）

ファイルが際限なく大きくなるのを防ぐ仕組み。「そろそろ大きいですよ」という**黄色信号**（advisory）と、「これ以上は通しません」という**赤信号**（1,000 行で CI を止める）の 2 段構えになっている。この module は赤信号だけでなく、**黄色信号がちゃんと点く状態か**まで検査するのが特徴で、実際「黄色信号の配線が繋がっていないまま赤信号の 13 行手前まで来ていた」ファイルが見つかっている。

### For third parties / auditors

「上限を設けた」と主張するだけでなく、**その上限の手前で警告が実際に出る状態か**を機械が検証している点が監査上の要点。Check 443（値の妥当性）と Check 454（登録の存在）は、どちらも「宣言はあるが実態が伴わない」class を塞ぐために、実測で欠陥を確認してから追加された。
