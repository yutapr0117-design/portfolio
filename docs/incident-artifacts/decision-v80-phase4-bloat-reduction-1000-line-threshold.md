# Decision — v80+ phase4: 肥大化解消 1,000 行しきい値と残存ファイルの disposition

```
Date        : 2026-07-04
Owner        : 横井雄太 (Yuta Yokoi) — 提案・裁可
Implementer  : Claude Code (AI 自走)
Status       : ADOPTED（shipped code 完遂 + 機械強制済 / 残存は defer-with-reason・設計制約）
Canonical-Ref: docs/architecture/file-size-budget.md（BUDGET-DATA 真値）/ CLAUDE.md §7 handoff
```

## 背景 / 決定

オーナーの提案（指示でなく提案・受諾済）: リポジトリの肝は「AI への全委任で生じる無限改善自走そのもの」であり、**肥大化を残すことがその自走への最大リスク**（context 圧迫・保守/拡張負荷・変更の非破壊証明コスト）。よって **1,000 行を肥大化の目安**とし、着実に一つずつ解消し、かつ「生じないように」進める。過去の main.js 7,785→1,086 行がその example。

## 実施したこと（2026-07-04 セッション）

葉モジュール factory パターン（`export function createX({deps})` + main.js 依存注入 + byte-equivalent）で shipped JS を分割:

| 対象 | 変更 | PR |
| :-- | :-- | :-- |
| js/pages.js | 642→267（HiringRiskPage + 専用 helper を js/hiring-risk-page.js へ） | #556 |
| js/apps.js | 1,179→1,040（AIPage → js/ai-page.js） | #557 |
| js/apps.js | 1,040→824（PomodoroPage → js/pomodoro-page.js） | #558 |
| .github/scripts/mutation_samples.py | 1,597→870 + archive 742 + common 12（log-rotation 分割） | (main 直) |
| docs/architecture/file-size-budget.md | BUDGET-DATA 実態同期 + 8 葉モジュール登録 + 1,000 しきい値 tighten | #559 |
| Check 361（新設・BLOCKING） | shipped js/*.js ∪ js/quiz/*.js が BUDGET-DATA 登録済みを強制（Check 71 の対称） | #559 |

**結果**: shipped JS は全て ≤824 行。**Check 361 + Check 52（advisory 行数予算）+ Check 71（BUDGET-DATA path 実在）で「新 leaf が silent に未予算化して無制限成長する」class を機械強制で封じた**（memory/convention → BLOCKING Check へ昇華 = 「生じないように」の実体化）。mutation_samples は log-rotation 規約（新規は tail へ、~900 行超で archive へ rotate）で無限成長を止めた。

## 残存 >1,000 行ファイルの disposition（将来セッションはこれを再検討/衝動的着手しないこと）

| ファイル | 行数 | disposition | 理由 |
| :-- | --: | :-- | :-- |
| `.github/scripts/check_repository_consistency.py` | ~15,700 | **defer-with-reason** | #253 で body split は net-negative と評価済。360+ の atomic check が共有 module グローバル（check/html/errors）と `# ── N.` column-0 section header 規約に依存し、`exec()` 間接化は自由変数の静的解決不能・未定義グローバル参照の脆さを生む。抽出可能な大データ塊も無い（平均 ~43 行/check の logic）。Check 52 advisory が surface し続ける（budget 4,750）が「抑制すべき bloat」でなく「機械強制の richness 増加」。 |
| `e2e/portfolio.spec.js` | ~3,332 | **defer-with-reason** | Check 16/28/29/58/110/111/114/118/151 の **9 個**が本ファイルを名前で参照し、うち数個は特定 const（ALL_ROUTES/A11Y_ROUTES/PAGE_META）に semantic 結合。単純分割は「新 spec が 9 guard を silent に escape する」vacuous 化を招く。安全な分割には先に 9 check を `e2e/*.spec.js` glob へ一般化する必要があり（= verify gate 自体への高 blast-radius 改修）、かつ snapshot dir 名（`portfolio.spec.js-snapshots`）が本ファイル名に固定。**de-risk 経路（将来やるなら）**: ①9 check を glob 化（テスト移動なし=非破壊・latent vacuous gap も同時に閉じる）→ ②テーマ群を 1 つずつ別 spec へ移動。test ファイルゆえ shipped code より優先度低。 |
| `style.css` | ~2,178 | **設計制約** | 単一 stylesheet（Check 135 が単一 `<link>` 配線を強制・Check 108/52/120）。複数 `<link>`/@import は追加 request で C1「Boring Technology」/perf と衝突。baseline 取得後の section 分割は cascade 破壊リスクゆえ human-gated。 |
| `index.html` | ~1,308 | **設計制約** | 単一 SPA entry（CSP/JSON-LD/AI meta/AIO anchor/app-shell）。分割不能。`protected`（AIO 承認なしに整理しない・C6）。 |
| `main.js` | ~1,183 | **設計制約（保護 kernel）** | AIDK Kernel proper + view-transition/render core + Trusted Types + IIFE + SITE_CONFIG + protected blocks（Check 43 が BLOCKING 保護）。抽出済み 24 葉モジュールの合成呼び出し（import + `const {X}=createX()`）は wiring ゆえ抽出不能で、むしろ leaf 抽出のたび微増する。物理分割は Stage 5 で完遂済（7,785→1,086）。 |

## なぜこの判断か（原則）

- **最大のリスクは肥大化したまま進めること**。ただし解消にもリスクがあり、**着実に一つずつ・非破壊証明（verify=0 + behavior e2e 非回帰 + byte-equivalent）しながら**進めればリスクを抑えられる。
- shipped code（サイト挙動 + 最頻編集面）を最優先で完遂した。残存は tooling/generated/設計制約で、shipped より context 負荷が低いか、分割が net-negative/high-risk。
- 「生じないように」は doc/memory の規約でなく **Check 361（BLOCKING）で機械強制**した。これが本セッションの最重要成果（recurrence を人手でなく CI が防ぐ）。

## 関連

- `docs/architecture/file-size-budget.md`（§4 BUDGET-DATA = Check 52/71/361 の真値）
- Check 52（advisory 行数予算）/ 71（registered⟹exists）/ 361（exists⟹registered）
- memory: `feedback_bloat_1000_line_threshold` / `feedback_sed_ampersand_lint_edit`（葉抽出チェックリスト）
