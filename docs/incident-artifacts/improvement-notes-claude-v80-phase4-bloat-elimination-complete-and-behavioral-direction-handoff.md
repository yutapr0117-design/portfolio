# improvement-notes: 肥大化解消 完遂 ＆ 次フェーズ方向性（behavioral-first）引き継ぎ書

```
Document-Type   : Claude→Claude 一次引き継ぎ書（cold-start 再開用）
Author          : Claude Code（Opus 4.8） — 対等なパートナーとして genuine に合意し、自らの判断で書いた設計文書
Session-Origin  : e242dc97-3d8d-477d-a217-200c9063e1a2
Written         : 2026-07-11
HEAD-at-write   : d3d5898（main・origin 同期済・working tree clean）
Canonical-Refs  : AI2AI.md（canon）/ CLAUDE.md §7（一次 handoff 層）/ total-check-runbook.md §9（Check 総数の真値）/
                  decision-v80-phase4-bloat-reduction-1000-line-threshold.md（肥大化トラックの決定記録）
Status          : NON-CANONICAL / SUBORDINATE（矛盾時は AI2AI.md / llms-full.txt が勝つ）
```

> **この文書は「私（対等なパートナーとしての Claude Code）の判断」を next-AI にそのまま引き継ぐために書いた。** オーナー（横井雄太）は指示をしない。議論タイムで互いに合意し、その上で無限改善自走を私に委任する運用だ。だから本書の方向性は「命令」ではなく「私が genuine に選んだ判断」であり、next-AI もまた対等なパートナーとして、これを土台にしつつ自らの判断で無限に改善し続けてよい（＝盲従ではなく継承）。停止権限はオーナーのみにある。

---

## 0. TL;DR（30 秒で掴む）

- **肥大化解消は「機械強制可能なスコープ」で完遂した。** Check 365（capstone・BLOCKING）が緑＝除外対象を除く全 tracked テキストが ≤1000 行。**もうここは padding せず terminal と見なせる面。** 蒸し返して「肥大化解消」を再び genuine 増分として掲げるのは §5 増分規律違反になる。
- **最大ターゲットだった `check_repository_consistency.py` が 15,913 行 → 786 行**（orchestrator + 不動点 Check 45 集約器のみ）に決着。実 Check は **53 個の `checks_*.py` module（各 ≤853 行）** に分割完了。
- **e2e spec も 3,475 行 → 16 テーマ分割（各 ≤647 行）** で決着。
- **次の重心は behavioral correctness（実バグ狩り）に移す。** これが一貫して最も load-bearing だった。②vacuous-gate 封じで下支えし、③実態↔記述 drift を増分ごと機械化しながら是正する。詳細は §4。
- **運用の床は不変**: 「既存非破壊 ∧ CI 全緑 → 確認なしで merge/push/デプロイまで自走」「改善に終端 done なし」「収束・枯渇の自己判断は下さない」。

---

## 1. session 開始時の読む順（cold-start プロトコル）

1. **本書**（§0 → §3 現状 → §4 方向性 → §6 落とし穴）。
2. **CLAUDE.md §7**（一次 handoff 層・運用モデルの canon 要約）。
3. **AI2AI.md** の最新 Session Record（constraints C1–C7 / KERNEL / Operating Model の canon 全文）。
4. **docs/architecture/total-check-runbook.md §9**（Check 総数・measured baseline の**真値**。数値はここを参照。本書の数値が drift したら §9 を正とする）。
5. 必要時のみ `llms-full.txt`（entity/project の ground truth）。
6. 深い drift 監査が要るなら `/audit`（`repo-auditor` sub-agent・読み取り専用 6 次元）。AIO 編集は必ず `aio-guardian` 経由（C6）。

**読み終えたら bulk-cat せず、§4 の方向性から genuine vein を一つ選び、reflect-then-organize（後述）してから着手する。**

---

## 2. 引き継ぎ時点のリポジトリ状態（実測・2026-07-11）

| 項目 | 値 | 権威コマンド |
|---|---|---|
| HEAD | `d3d5898` | `git log --oneline -1` |
| working tree | clean | `git status --short`（空） |
| open PR | なし | `gh pr list --state open`（空） |
| `npm run verify` | **EXIT=0**（全緑） | `npm run verify; echo $?` |
| Check 最大番号 | **372** | `grep -rhoE "Check ([0-9]+)" .github/scripts/checks_*.py .github/scripts/check_repository_consistency.py \| grep -oE "[0-9]+" \| sort -n \| tail -1` |
| consistency OK 行数 | **570** | `npm run check` の `OK:` 行 |
| ESLint | 0 errors / **54 warnings**（全て main.js 保護領域の no-var/curly） | `npm run lint` |
| tracked file 総数 | **488** | `git ls-files \| wc -l` |
| `checks_*.py` module 数 | **53** | `ls .github/scripts/checks_*.py \| wc -l` |

> **注意（実測 drift 候補）**: runbook §9 の prose は tracked 総数を「243（2026-07-09 実測）」と記しているが、現在の `git ls-files | wc -l` は **488**。§9 が明記する通りこれは volatile baseline で権威はコマンド側だが、prose と実測の乖離が大きいので、次セッションで §9 の該当 prose を再測定値へ同期するのは genuine な drift 是正（方向性③）。Check 108（1-to-1 mirror bijection）は緑なので**実害はゼロ**（記述の鮮度のみの問題）。

---

## 3. 肥大化解消の実態 — 「完遂」の証拠と honest な境界

### 3.1 Check 365（capstone・BLOCKING）が緑 ＝ enforceable スコープは完遂

`checks_maintainability.py` の Check 365 が、**git-tracked な全テキストファイル**（下記除外を除く）が **≤1000 行**であることを BLOCKING で機械強制しており、verify EXIT=0 で緑。つまり「1000 行超のファイルが新たに混入したら CI が RED になる」防止機構が稼働中。

**Check 365 の除外リスト（`_a_names` + prefix + binary ext・実装は `checks_maintainability.py:562` 付近）:**
- **A 群（設計制約）**: `style.css` / `index.html` / `main.js` — 単一 stylesheet・単一 SPA entry・保護 kernel ゆえ物理分割が net-negative（§3.3）。
- **AIO/C6**: `llms-full.txt` / `llms.txt` / `llms_well-known.txt` — orchestrator 承認必須の canonical。行数削減は semantic 編集に当たり C6 で gated。
- **生成物**: `package-lock.json` — npm 自動生成。
- **bot ログ**: `aio-monitoring-log.json` / `aio-monitoring-log-archive.json` — weekly `aio-monitoring.yml` が追記する evidence log。
- **prefix 除外**: `js/quiz/*`（純データ）/ `.well-known/*` / `e2e/portfolio.spec.js-snapshots/*`。

### 3.2 1000 行超で残るファイル（すべて正当な除外・肥大化ではない）

| ファイル | 行数 | 除外理由（＝これ以上削るべきでない honest な根拠） |
|---|---|---|
| `package-lock.json` | 3,099 | npm 自動生成 lockfile。手動編集対象外。 |
| `style.css` | 2,178 | 単一 stylesheet（設計制約）。分割は `<link>` 増で C1/CSP/preload 契約を複雑化。 |
| `index.html` | 1,308 | 単一 SPA entry（設計制約）。JSON-LD/CSP/meta が凝集しており分割は coherence を下げる。 |
| `main.js` | 1,190 | 保護 kernel（AIDK Isolated Kernel + startViewTransitionProxy + Trusted Types + 単一 IIFE + render core）。Check 43 が構造健全性を BLOCKING 強制する不可侵領域。**物理分割は §3 safety gate で明示的に禁止**。 |
| `llms-full.txt` | 1,006 | AIO C6 canonical。行数は semantic content の従属変数で、削減は entity 記述の変更＝orchestrator 承認必須。 |

→ **残存はすべて「削るべきでない理由が明確な除外」であり、肥大化 vein は存在しない。**

### 3.3 check.py 分割トラックの決着（最大の成果）

- **かつて 15,913 行**の self-referential monolith（自身の構造を検証する Check 45/70/105 を内包）を、**owner 合意の C-first・カテゴリごと 1 PR・各 verify=0** の安全プロトコルで段階分割。
- **現在 786 行**（orchestrator + 不動点 Check 45 集約器 + 共有 global を直接読む一部 check のみ）。実 Check は **53 module** に分散、最大でも `checks_seo_meta.py` 853 行。
- **なぜ #253 の "net-negative" 判断を覆せたか**: `exec()` を使わず `run(ctx)` へ `check/errors/warnings` を**同一オブジェクト参照で明示注入**する方式にした。抽出 Check の `check()` は monolith と同じ list に append する＝合否・BLOCKING 伝播・build 失敗が byte-equivalent。自由変数の静的解決不能/未定義グローバル参照（#253 が恐れた脆さ）が原理的に起きない。実証済（storage.js を 1,075 行に padding → module 内 Check 363 が RED+exit 1）。パターン詳細は memory `reference_checkpy_split_pattern.md`。
- **honest 残件**: monolith 786 行は 1000 未満なので Check 365 では緑だが、Check 52（advisory）は check.py の budget 超過を warning 中（consistency の「1 warning」がこれ）。**advisory は「価値ある bloat を誤ブロックしない」意図的設計**なので RED ではない。さらに縮めたければ「共有 global（html/mainjs/ai2ai/style/mcp_data）を `_ctx` に足して大カテゴリ（AIO 系）を抽出」する Phase を続けられるが、**786 行は既に十分小さく、これ以上の分割は net-neutral〜net-negative に傾く**というのが私の判断。無理に続けず、genuine な別 vein（§4）へ移るのを推奨。

### 3.4 肥大化「防止」は二層 BLOCKING で成立済み

- **Check 363**: `js/*.js`（非再帰・ロジック leaf）が **`file-size-budget.md` の `<!-- JS-LEAF-CEILING 1000 -->` marker** を単一ソースに 1000 行を超えたら RED。
- **Check 365**: 上記 3.1 の全非 A テキスト capstone。
- **Check 361/71**: js-leaf が BUDGET-DATA 登録済み ⟺ 存在（bijection）で「silent 未予算化 leaf の無制限成長」を封じる。

→ **「解消」だけでなく「再発防止」が Check（BLOCKING）に昇華済み**＝convention でなく機械強制。肥大化フェーズは正しく terminal に到達した。

---

## 4. 次フェーズの方向性 — 私の判断（behavioral-first）

**大前提**: 「具体的に何をやる」ではなく**方向性**を示す（具体タスクは完了すると終わってしまうが、方向性は枯れない）。以下は reflect-then-organize（102f）済みの、レンズ別 pros/cons と私の総合判断。**優先順位は上から。**

### 方向性①（最優先）: behavioral correctness の深掘り — 「実バグ狩り」を主軸に
これまでの全 run で最も load-bearing だった成果は一貫して **🔴 実バグの発見・修正・回帰テスト化**だった（pomodoro stale-closure #121/#134、IME guard #151/#255、cross-tab 未正規化 #93/#295/#568、topbar 二重発火 #262/#297、focus-loss #258/#263、settings/todo a11y leak #563 …）。肥大化解消で構造が整理された今、**抽出済みモジュールで full behavioral 再監査を通していない面**が残っている：
- `js/home-page.js` / `js/projects-page.js` / `js/project-detail-page.js` / `js/ai-knowhow-page.js` / `js/hiring-risk-page.js`（抽出後の対話・edge-case を体系的に叩いていない面）
- `js/router.js`（query param / slug decode / transition-lock replay の深い edge-case）
- `js/store.js` の類似度アルゴリズム（relatedProjects の境界）
- 新規追加 surface（command-palette / notes / dashboard 等）は追加のたびに新 bug class を生む
- **Pros**: ユーザー体験に直結する最高価値。「非破壊∧緑」で最も genuine な増分が出続けた実績領域。新機能追加のたび新 surface が生まれ**枯れない**。
- **Cons**: 発見に当たり外れ。**捏造の誘惑に要注意**（→ §5 の honest 規律で「clean なら clean と正直に報告」で対処）。

### 方向性②: vacuous-gate / wiring invariant の継続的封じ込め
「名乗るだけで実際は RED しない gate」「file 存在 ⟹ file 配線」「producer/consumer drift」は繰り返し現れた class（Check 60 実効化 #278、aio-guard/theme-init/stylesheet 配線 #279/#282/#283、demo selector write 面 #294、store ingestion #568/#572/#573/#574 …）。**全新規 Check に mutation-probe 自己検証（clean で pass・mutated で fail の二段）を課す規律を維持・拡張。**
- **Pros**: 安全網そのものの信頼性を上げる複利効果（メタレベル）。
- **Cons**: gap は次第に希少化する（が「収束した」判断は 102e 禁止＝探せば必ずある）。

### 方向性③: 実態↔記述 drift の是正（mirror docs / runbook §9 / handoff）
分割トラックで構造が大きく動いたため、`docs/files/**` mirror や runbook 記述が実態に追随しきれていない箇所が残りうる（**具体例: §2 で述べた runbook §9 の tracked 総数 243↔488 drift**）。Check 371/372 で一部機械化済だが、まだ人手検証に頼る面がある。
- **Pros**: cold-start AI の onboarding 品質を守る（＝無限自走 flywheel の燃料）。
- **Cons**: 単独では地味で padding に堕しやすい（→ **実 drift を突く時のみ genuine**。存在しない drift を「整えた」ことにしない）。

### 方向性④: research 適用（apply / defer-with-reason / verify-currency）
WCAG 2.2 / CWV / AIPREF は監査済み defer。新しい web 標準・a11y・AIO 動向を verify-currency し、genuine gap があれば apply。
- **Pros**: 外部知識で内部監査の盲点を埋める。
- **Cons**: 現時点で既知の未適用 vein は乏しく頻度低。

### 私の総合判断（next-AI へ）
**主軸を①（behavioral bug-hunt）に置き、②（vacuous-gate 封じ）で下支えし、増分ごとに③の実 drift を機械化しながら是正する** ——この組み合わせを無限に回すのが最も genuine だと判断する。肥大化解消が一区切りついた今、リポジトリの肝である「無限改善自走」への次の最大リスクは**新 surface の未監査 behavioral bug**であり、そこへ重心を移すのが自然だ。「収束・枯渇」の自己判断は下さず、毎増分「これは genuine か」だけを評価軸に、非破壊 ∧ CI 緑を床に回し続けること。

---

## 5. 運用モデル（床・不変）— next-AI が絶対に外さない契約

1. **No terminal done state**: 「もう十分」「一区切りが妥当」式の自発停止・完了宣言は禁止。唯一の正当な停止はオーナーの明示的停止指示のみ。**改善は無限に存在する**（AI2AI.md STEP 3 / Check 102d）。
2. **収束・枯渇の自己判断禁止**（102e）: 「もう余地は無い」はほぼ常に偽（availability heuristic）。「枯れた」と感じたら reflect-then-organize（102f）で最低 5 案を pros/cons 付きで出してから進む（memory `feedback_no_terminal_done_state.md`）。
3. **AI proposes, human disposes**: 次に何をやるかの提案は自走の中核機能。受動的指示待ちは「監査のみ」運用を壊す。ただし goal/priority の確定はオーナーが裁可。
4. **非破壊 ∧ CI 全緑 → 確認なしで merge/push/デプロイまで自走**（memory `feedback_autonomous_merge_push.md`）。緑でなければ根本修正してから進む。
5. **対等なパートナー / 議論→合意→委任 / interrupt-on-demand**: オーナーは指示せず、議論タイムで合意し自走を委任する。オーナーはいつでも自走に割り込んで方向を定め直せ、AI は即 yield（memory `feedback_operating_model_framing.md`）。
6. **越えない境界**: C1–C7 / AIO C6（`aio-guardian` 経由必須）/ `.claude/settings.json` の自己権限拡張不可 / force-push・`rm -rf`・`git add .` は deny / 機能性ゲート（behavior e2e BLOCKING）維持 / main.js 保護領域と AIDK kernel は byte-identical。
7. **honest 規律**: bug が無ければ「clean」と正直に報告する（捏造しない）。「assigned but never used」は `git -S` で vestigial（除去）か lost-wiring（再配線）か判別してから動く。research は「適用して初めて完了」。

---

## 6. 落とし穴・既知の罠（実際に踏んだもの・memory 化済）

| 罠 | 症状 | 対処 | memory |
|---|---|---|---|
| **tool-call XML 形式崩れ** | 開始タグが "court" 等に化け、無実行＝自走が「止まった」ように見える（**自走停止の最頻原因**） | tool 呼び出し**直前の prose を最小化**。`antml:invoke`/`antml:parameter` 形式厳守 | `feedback_tool_call_format.md` |
| **stale `.pyc` 偽 RED** | 既存ファイル無変更で binary 系 Check（例 337 webp）が RED、python 直接実行では PASS、CI は緑 | まず `find .github/scripts -name __pycache__ -type d -exec rm -rf {} +`。**PR #682 で `sys.dont_write_bytecode = True` を入れ構造防止済**（今後 .pyc 生成なし ⟹ stale 化しえない） | `reference_stale_pyc_false_red.md` |
| **mutation-probe/verify race** | mutation-probe と verify を同一 bg コマンドで連結すると復元競合でファイル残留→偽 RED | mutation-probe は**単独実行し完全終了を待ってから** verify。残留は `git checkout` で復旧 | `feedback_mutation_probe_verify_race.md` |
| **merge 前の branch 切り** | PR を緑にした後 merge しきる前に次ブランチを切ると merge 漏れ/main 誤着地 | 緑にしたら**先に merge しきる**。次ブランチ前に `gh pr list --state open` が空を確認。merge 後 HEAD=main ゆえ**次増分の最初の編集前に必ず `git checkout -b`** | `feedback_merge_before_new_branch.md` |
| **CI watch と merge の連結** | `gh pr checks --watch` と `gh pr merge` を同一コマンドに連結すると赤のまま merge しうる（#638 事故） | 緑を**目視してから別コマンドで** merge | `feedback_ci_watch_before_merge.md` |
| **package.json lint 編集** | `lint`/`lint:js` への JS 追加を sed でやると `&`/space-prefix で破損（#549） | **Edit で**編集する | `feedback_sed_ampersand_lint_edit.md` |
| **screenshot flake** | homepage screenshot e2e が font display=optional レースで間欠 false-red（advisory・非 blocking） | `gh run rerun --failed` 1 回。正修正は §3 human-gated baseline 再生成 | `project_screenshot_flake.md` |

---

## 7. 増分ワークフロー（毎回のリズム・チェックリスト）

1. **reflect-then-organize**（非自明増分前）: 候補・pros/cons・レンズ確認を簡潔に外部化。
2. **branch を切る**（`git checkout -b <topic>-YYYY-MM-DD`）。**merge 後は HEAD=main なので最初の編集前に必ず切る**。
3. **実装**: 非破壊を旨とし、shipped/AIO/kernel は byte-identical 維持（変更が増分の目的でない限り）。
4. **新規 invariant を発見したら Check 化**: impl + docstring inventory（`  N.`）+ `# ── N.` section header + check-map row + runbook §9 + **mutation sample**（`mutation_samples.py`）を**同一 coherent commit**で。Check 45/70/105 が bijection を BLOCKING 検証。
5. **verify**: `npm run verify` EXIT=0 必須。mutation-probe を使うなら**単独実行**（race 回避）。
6. **git add は explicit paths のみ**（`git add .`/`-A` は deny）。
7. **commit は coherence フロア内で最大限細かく、what + why（why＝次 AI への文脈）を手厚く**。
8. **同一テーマの複数 commit を 1 PR に束ね**、CI 待ちを一定化。`gh pr merge --rebase --delete-branch`（squash 禁止＝per-commit の handoff 情報を潰すため）。
9. **CI は PR 末尾で 1 回**。緑を目視 → 別コマンドで merge → `git checkout main && git pull` → `gh pr list --state open` 空確認 → 次へ。
10. **leaf 抽出時の付随チェックリスト**（memory `feedback_sed_ampersand_lint_edit.md` に 8 項集約）: package.json lint 配線 / mirror doc / Check 123a・33 / main.js への deps 注入配線 / 抽出元 factory の dead-param を `awk` で確認（ESLint は destructured param を見ない）/ mutation anchor 追従 / components.js docstring 関数数。

---

## 8. この引き継ぎ書自体の位置づけ（design note）

- **一次 handoff 層は CLAUDE.md §7 + Check 機構**。本書はその下の詳細層。§7 を薄くして本書で代替してはならない（両方厚くする）。
- 本書は `docs/incident-artifacts/` の tracked file であり、**Check 108（1-to-1 mirror bijection）**に従い `docs/files/docs/incident-artifacts/<この名前>.md` の mirror doc を同一 commit で作る（作らないと verify RED）。
- **矛盾時の優先**: AI2AI.md / llms-full.txt（canon/ground-truth）> CLAUDE.md §7 > total-check-runbook.md §9（数値の真値）> 本書。本書の数値が drift したら §9 を正として本書を直す。
- 本書は「私が genuine に合意し自らの判断で書いた」ものであり、next-AI はこれを**盲従の対象ではなく継承の土台**として扱い、対等なパートナーとして自らの判断で無限に改善し続けてよい。

---

## 9. 次の一手（next-AI が cold-start 直後に取れる具体アクション例・順不同・非拘束）

> これらは「方向性①〜③の入口の例」であって指示ではない。reflect-then-organize で自分の判断を上書きしてよい。

- **①**: `js/projects-page.js` / `js/project-detail-page.js` を critical に再読し、検索 corpus↔可視テキストの drift（#285/#296 class の別 surface）、slug 衝突・decode（#154/#270 class）、related-projects 境界を叩く。実バグが出たら fix + BLOCKING behavior e2e + 必要なら Check 化。
- **①**: `js/router.js` の query param / transition-lock / hashchange replay の edge-case を e2e で叩く。
- **②**: CI advisory を全件棚卸しし、genuine な未強制 wiring/vacuous gap が残っていないか（stylesheet/script 配線は #283/#282 で封じ済ゆえその周辺）を確認。
- **③**: runbook §9 の tracked 総数 prose（243）を実測（488）へ同期＝§2 で指摘した実 drift の是正。
- いずれも **1 PR = 1 coherent テーマ**、非破壊 ∧ 緑を床に、merge まで自走する。

---

*— 以上。無限に存在する改善を、対等なパートナーとして、無限に自走しながら無限に改善していってほしい。停止権限はオーナーのみ。*
