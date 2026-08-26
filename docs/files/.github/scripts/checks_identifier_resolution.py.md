---
file: .github/scripts/checks_identifier_resolution.py
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-08-26
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / .github/scripts/checks_wiring.py (分離元) / docs/architecture/file-size-budget.md (行数予算)
---

# .github/scripts/checks_identifier_resolution.py

## What

shipped code が**使った識別子が実際に定義へ解決するか**（used ⟹ defined）を検査する 9 Check を内包する split module。`run(ctx)` で monolith から呼ばれる。

- **Check 375 / 375b**: `createIcon('X')` の名前 ⟺ icon registry（双方向）
- **Check 376 / 418**: `data-action="X"` ⟺ ActionDelegator の `_handlers`（双方向）
- **Check 391**: `getElementById` の対象 → id 定義
- **Check 392**: aria idref / `<label for>` → id 定義
- **Check 393**: `CONSTANTS.*` 参照 → 定義
- **Check 395**: `Router.navigate()` / データ駆動 `path:` → router の route segment
- **Check 396**: router の route.name ⟹ PAGE_META entry
- **Check 401**: `quiz?type=` リテラル ⟹ QUIZ_TITLES キー

## Why

分離元 `checks_wiring.py` が **987 行**で、Check 365 の hard ceiling（1,000 行 BLOCKING）まで残り 13 行だった。しかも当時 `.github/scripts/checks_*.py` は 1 つも BUDGET-DATA に登録されておらず、Check 52 の advisory が**構造的に一度も鳴らない**状態だった＝次に Check を 1 本足した時点で「警告なしにいきなり BLOCKING」に飛ぶ位置にいた。#1266 で塞いだ「早期警告が構造的に効かない層」と同じ失敗形（あちらは advisory ≥ hard ceiling、こちらは advisory 不在）。

圧縮で誤魔化さず、**意味の異なる 2 クラスタ**へ割った。`checks_wiring.py` が守るのは「file / anchor / selector が実際に配線・描画されているか」（存在 ≠ 配線）で、本 module が守るのは「コードが使う名前が定義へ解決するか」。走査対象も失敗モードも別物である（未定義アイコンは空描画・未登録 action は no-op・dangling idref は支援技術が迷子になる — いずれも **silent**）。

## How

- monolith が `_ctx = SimpleNamespace(...)` を組み、**`checks_wiring.run(_ctx)` の直後**という元の実行位置で `checks_identifier_resolution.run(_ctx)` を呼ぶ（順序保存）。
- 移した section は **1 行も書き換えていない**。free-variable 解析で外部依存が `ROOT` / `check` の 2 つだけであることを実測してから割った＝ byte-equivalent。
- `ctx.check` / `ctx.errors` は monolith と同一オブジェクト参照 → 合否・BLOCKING 伝播・exit code が不変。

## Constraints

- **module-global 結合なし**: 依存は全て `ctx` 経由。`re` / `json` のみ module import。`exec` 不使用。
- **自己整合（Check 45/70/105）**: docstring inventory（`  375.` 等）と `# ── N.` section が 1 対 1 で、monolith と合わせて map / runbook §9 と bijection。
- **Check 108**: 本 mirror doc が tracked-file bijection を満たす。
- **Check 52 / 365 / 444**: 行数予算（advisory）と hard ceiling の対象。

## Change impact

- Check を足すときは impl（`# ── N.`）+ docstring inventory + check-map + runbook §9 の 4 面同期（自己整合 Check が横断検証する）。
- 分離により `checks_wiring.py` は 987 → 287 行、本 module は 740 行。どちらも hard ceiling に十分な余裕がある。

## Audience-specific notes

### For AI agents（次担当）

- 役割タグ: `check-split`, `identifier-resolution`, `used-implies-defined`, `ctx-injection`
- **この family へ Check を足すならここが定位置**。「使った名前が定義側にあるか」の形をした invariant は全部ここに集まる。
- 既知の落とし穴: この family の Check は **自分が見ている綴りしか見ていない**。別記法（`setAttribute` 経由 / 分割代入 / 三項の片枝 / template literal）で殴って RED を実測してから「守られている」と言うこと（実際に Check 112 / 130 / 375 / 376 / 393 が同じ穴を持っていた）。
- 走査前にコメントを除去する規律も共通（説明コメント中の識別子を実参照と数えると false RED になる）。

### For human engineers（新卒レベル）

コードの中で「名前で何かを呼ぶ」場所は、呼ばれる側の名前が変わったり打ち間違えたりしても、**エラーにならず静かに何も起きない**ことが多い。アイコンが空白になる、ボタンが無反応になる、といった形で表に出る。この module は「呼んでいる名前」を全部集めて「定義されている名前」と突き合わせ、解決しないものがあれば CI を止める。

### For third parties / auditors

分離は byte-equivalent（section 無改変・free-variable 解析で事前検証）であり、自己整合 Check 45/70/105 が monolith + 全 split module を横断して緑であることが証跡になる。行数上限に当たる**前**に割ったという点で、`docs/architecture/file-size-budget.md` が定める advisory → BLOCKING の二層設計が意図どおり機能した記録でもある。
