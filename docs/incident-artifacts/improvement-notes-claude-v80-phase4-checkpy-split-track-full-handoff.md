# improvement-notes — v80 phase4 後続「check.py 分割トラック」完全引き継ぎ書

```
Author        : Claude Code (AI 無限改善自走)
Session-Date  : 2026-07-05
Track         : check_repository_consistency.py 段階分割 (owner 合意 C-first・sustained multi-session)
Status        : Phase 1-5 完遂・main 緑・open PR ゼロ・Phase 6+ 継続待ち
Canonical-Ref : CLAUDE.md §7 / AI2AI.md Session Record / total-check-runbook.md §9 (Check 総数の真値)
                / decision-v80-phase4-bloat-reduction-1000-line-threshold.md (C-first 合意 + 安全プロトコル)
                / memory reference_checkpy_split_pattern (分割パターン) / feedback_bloat_1000_line_threshold
```

> **この文書は「次担当 AI が cold-start で check.py 分割トラックを seamless に継続する」ための完全引き継ぎ書。** §7 のハンドオフを薄くして commit log で代替しない規律（CLAUDE.md §5 AI2AI handoff-first）に従い、本トラック固有の全知見（合意の経緯・確立した分割パターン・coupling 判別法・落とし穴・次の手・厳守事項）を一次層としてここに集約する。数値の真値は常に `total-check-runbook.md` §9（Check 総数 = **364**）を正とする。

---

## 0. 30 秒サマリ（BLUF）

- **合意した肥大化解消トラック**: A 以外の全ファイルを 1,000 行以下にし、その後 CI で ≤1,000 を監査化（防止 capstone）。順序 = **C（check.py 最優先 → e2e spec）→ B（style.css / index.html / docs）→ capstone**。
- **check.py 分割は 9 phase 完遂**（Phase 1-5 は前セッション / Phase 6-9 は 2026-07-05 後続セッション）: monolith **15,913 → 14,053 行（−1,860）**。**6 つの category module 確立**（`checks_maintainability.py` / `checks_structural.py` / `checks_esm.py` / `checks_tooling.py` / `checks_entity.py` / `checks_docs_mirror.py`）。全 phase で `npm run verify` exit 0、自己整合 Check 45/70/105 が全 module 横断で緑。
- **#253 の「物理分割 net-negative」を覆した**: `exec` 不使用の **`run(ctx)` 明示 context 注入**（check/errors/warnings を同一オブジェクト参照で渡す）で挙動 byte-equivalent を実証。
- **現状（Phase 9 終了時）**: main clean・origin 同期・open PR ゼロ・consistency exit 0・**check.py 14,053 行**。
- **Phase 6-9 で確立した 2 パターン**: (i) **coupled-group 一括抽出**（Phase 6 = `_modules47` 共有の 47/56/57/61 をリスト定義＋全消費者ごと抽出＝結合解消）、(ii) **連続 self-contained クラスタ抽出**（Phase 7 = tooling 74-80 / Phase 8 = entity 81-90 / Phase 9 = docs-mirror 96-99。各 Check が対象ファイルを自前 read_text し global content 依存なし・連続ゆえ reorder なし＝最も安全）。
- **次の一手（未着手・reflect-then-organize 済）**: (a) 残る連続 self-contained クラスタを継続抽出（候補: 92-95 AIO C6 derived-value/date-tools / 104-114 verify-gate・e2e guard・canon policy / 116-146 の各テーマ束）、または (b) `_ctx` を global content（html/mainjs/ai2ai/style/mcp_data）で enrich して html 系大カテゴリ（813 参照で最大の塊）を抽出。**depmap の落とし穴: コメント内 "index.html" の `.html` や文字列リテラル `"main.js"` が bare-word global 検知を誤発火させる（81/96 が実例）— 実コードの依存を確認せよ。**

---

## 1. 合意の経緯（owner との議論タイムの結論・厳守）

本トラックは owner の**指示ではなく議論→合意**で始まった。owner は人間と AI を対等に扱い、「報告」「指示」ワードを使わない運用を明示。合意内容（verbatim intent）:

1. **肥大化解消と肥大化防止をセットで**行う（owner 提案・受諾）。理由: リポジトリの肝は「全委任で生じる AI 無限改善自走そのもの」で、**肥大化放置がその自走への最大リスク**。
2. **1,000 行を肥大化の目安**とし、A 以外の全ファイルを ≤1,000 に収める。**分割でファイル数が増えるのは問題なし**（owner 明言）。
3. **順序 = C-first**: 「Cの肥大化から着手。最優先は `check_repository_consistency.py` から。Cを解消したら次にBを解消。A以外の全ファイルが1000行以下に収まったら、CIなどで1000行以下に収まっているかの監査を作る」（owner verbatim）。
4. **category A は触らない**（owner 明言）。A = mp3 / package-lock.json / main.js（保護 kernel）/ llms-full.txt（AIO canon）。
5. **運用条件**: 「本当にどうしようもない時のみ、私に伝えてください」。議論タイムを随時設ける協働ループ。AI は無停止で genuine 増分を自走し、非破壊 ∧ CI 緑を床に merge/deploy まで完遂。

**カテゴリ定義（decision record より）**:
- **A（不可侵）**: mp3 / package-lock.json / main.js / llms-full.txt。設計制約・保護 kernel・外部生成・AIO canon ゆえ分割対象外。
- **B（後回し）**: style.css（2,178）/ index.html（1,308）/ 各種 docs。単一 stylesheet・単一 SPA entry の設計制約があり分割是非は C 完了後に再検討。
- **C（最優先）**: check.py（元 15,913）/ e2e spec（3,475）。dev-tooling ゆえ shipped 資産 non-touch で分割可能。

---

## 2. 確立した分割パターン（再利用可能・Phase 1-5 で実証済）

### 2.1 なぜ #253 の「net-negative」を覆せたか（核心）

#253 は「check.py 物理分割は net-negative」と評価した。**唯一の根拠は `exec(src, globals())` の脆さ**（自由変数の静的解決不能・未定義グローバル参照・exec 間接化）。

本トラックは **`exec` を使わず `run(ctx)` へ check/errors/warnings を明示注入**することでこれを回避した。`ctx.check` / `ctx.errors` / `ctx.warnings` は monolith と**同一オブジェクトの参照**。抽出 Check の `check()` 呼び出しも同じ errors/warnings list に append する → **合否・BLOCKING 伝播・build 失敗（exit 1）が byte-equivalent**。自由変数の静的解決不能（#253 の脆さ）が原理的に起きない。

**実証**: js/storage.js を 1,075 行にパディング → module 内 Check 363 が RED + exit 1。BUDGET-DATA に不在 path → module 内 Check 71 が RED + exit 1。抽出後も安全網が monolith 時と同一に機能。

### 2.2 分割の 6 ステップ手順

1. **孤立カテゴリ選定**: monolith の共有 computed 変数（例 `html_v` を後続 check が使う）や global content（html/mainjs/ai2ai/style/mcp_data）に依存せず、`ROOT`/`check`/`warnings`/`read`/`extract` のみ使い、`_NN` 接尾辞 local を持つ Check 群を選ぶ。
2. **module 作成**: `.github/scripts/checks_<cat>.py` に `def run(ctx):` を書き、先頭で `ROOT = ctx.ROOT; check = ctx.check; warnings = ctx.warnings; read = ctx.read; extract = ctx.extract` 等を unpack。抽出する section を **+4 space indent** して `run()` 内へ移し、docstring inventory の `  N.` 行を module docstring へ移す。`re`/`json` 等の標準ライブラリのみ module import。
3. **CHECK_SOURCE_FILES 登録**: monolith の `CHECK_SOURCE_FILES` list（check.py:2688）に module path を追加。
4. **呼び出し配線**: monolith が `_ctx = _types.SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)`（check.py:2746 で定義済）を組み、**元の実行位置・順序を保持**して `import checks_<cat> as _m; _m.run(_ctx)` を呼ぶ（Check の実行順序を変えない）。
5. **verify**: `npm run verify` で自己整合 Check **45a/b/c**（docstring↔section 1..N 連番 bijection）・**70**（runbook §9 == max Check 番号）・**105**（check-map bijection）が monolith+module 横断で緑を確認。
6. **mirror doc**: `docs/files/.github/scripts/checks_<cat>.py.md` を追加（Check 108 が新 tracked file に BLOCKING で要求）。5+1 セクション（What/Why/How/Constraints/Change impact/Audience-specific notes）必須。

### 2.3 土台インフラ（#253 で敷済・本トラックが活用）

- `CHECK_SOURCE_FILES`（list）+ `_aggregate_check_numbers()`（check.py:2695〜）が docstring inventory（`  N.` 行）と `# ── N.` section header を**全 module 横断で集約**。よって自己整合 Check 45/70/105 の bijection は module を跨いで成立する。
- Phase 1 で `_aggregate_check_numbers` の `_sec_re` を `^#` → **`^\s*#\s*──`** へ緩和（check.py:2704）。`run(ctx)` 内で section header が 4-space インデントされるため、leading whitespace を許容する必要があった。
- **不動点**: Check 45 自身（`_aggregate_check_numbers` を呼ぶ集約器）は monolith 残置。集約器を module 化すると自己参照が壊れる。

---

## 3. Phase 1-9 の実施記録（何をどの module へ・PR #）

monolith **15,913 → 14,053 行**（9 phase・−1,860）。

| Phase | PR | 抽出 Check | 移動先 module | monolith 行数 | 備考 |
|---|---|---|---|---|---|
| 1 (PoC) | #577 | 361-364 | `checks_maintainability.py`（新規） | 15,913→15,622 | ctx 注入 PoC。js-leaf governance cluster |
| 2 | #579 | 52 + 71 | checks_maintainability.py（join） | 15,622→? | 非連番抽出 + 既存 module join パターン確立。file-size governance cluster |
| 3 | #581 | 28 + 29 + 30 | checks_maintainability.py（join） | ?→? | test-health cluster・連続ブロック一括抽出 |
| 4 | #582 | 16 + 42 | checks_maintainability.py（join） | 15,507→15,426 | 非連番・test/docs health |
| 5 | #583 | 48 + 49 + 50 + 51 | `checks_structural.py`（新規・2 個目） | →15,066 | structural / CI wiring / tooling（category E）。多 module パターン確立 |
| 6 | #585 | 47 + 56 + 57 + 61 | `checks_esm.py`（新規・3 個目） | 15,066→14,717 | **coupled-group 一括抽出**（`_modules47`+`_main_src47` 共有クラスタをリスト定義ごと抽出＝結合解消） |
| 7 | #586 | 74-80 | `checks_tooling.py`（新規・4 個目） | 14,717→14,476 | 連続 self-contained・dev-tooling/.claude config file integrity |
| 8 | #587 | 81-90 | `checks_entity.py`（新規・5 個目） | 14,476→14,251 | 連続 self-contained・entity/Organization cross-surface（READ-ONLY・C6 対象外） |
| 9 | #588 | 96-99 | `checks_docs_mirror.py`（新規・6 個目） | 14,251→14,053 | 連続 self-contained・docs/files ミラー統治 |

**現在の module 内訳**（6 module）:
- `checks_maintainability.py`= Check **16, 28, 29, 30, 42, 52, 71, 361, 362, 363, 364**（maintainability / test-health / file-size governance）。
- `checks_structural.py`= Check **48, 49, 50, 51**（structural parse / CI wiring / tooling）。
- `checks_esm.py`= Check **47, 56, 57, 61**（main.js ⇄ js/ 葉モジュール ESM 契約 + factory・`_modules47`/`_main_src47` を module-local 化）。
- `checks_tooling.py`= Check **74, 75, 76, 77, 78, 79, 80**（_lib_io helper / incident README / .claude settings/commands/agents/skills / .mcp.json）。
- `checks_entity.py`= Check **81-90**（WebP/MP3 Org / manifest affiliation・entity / README・Claude2Claude Org / CLAUDE.md cold-start / LICENSE / governance files / .claude entity。READ-ONLY presence 検査ゆえ C6 編集ではない＝aio-guardian 不要）。
- `checks_docs_mirror.py`= Check **96, 97, 98, 99**（shipped-code 1-to-1 docs bijection / frontmatter / 5-axis section / README+template）。

**実行配線の現物**（check.py 内・行番号は Phase 9 後で drift しうる・`grep 'run(_ctx)' check.py` で再取得）:
- `CHECK_SOURCE_FILES`: monolith + 6 module path を列挙。
- `_aggregate_check_numbers` + `_sec_re`: `^\s*#\s*──\s*(\d+)\.` で全 module 横断集約。
- `_ctx` 定義: `SimpleNamespace(ROOT, check, read, read_bytes, extract, errors, warnings)`。
- 各 module の `run(_ctx)` 呼び出しは **元の Check 位置を保持**（esm=47 位置 / tooling=74 位置 / entity=81 位置 / docs_mirror=96 位置 / structural=47 の後 / maintainability=361 位置）。

---

## 4. Phase 6+ の難度上昇と次の手（未着手・reflect-then-organize 済）

**readily-self-contained なクラスタはほぼ抽出し尽くした**。残る削減は質的に難度が上がる。2 つの class に分かれる:

### 4.1 shared-infra 変数に結合した check 群（coupled-group 一括抽出が必要）

- **`_modules47` class**: Check 47（ESM 契約）が定義する `_modules47`（js-leaf source-of-truth リスト）を Check **56/57/61** が共有参照する。Phase 5 で 46-51 を抽出しようとしたら consistency check が `NameError: _modules47` で即検知 → 47 を monolith 残置し 48-51 のみ抽出した（**安全網が機能した実例**）。
- **次の手**: この class は **消費側とセットで一括抽出**する（47 + 56 + 57 + 61 を同一 module へ）。または `_modules47` を `ctx` に足して両側から参照可能にする。
- **⚠ 教訓**: 「`_NN` 接尾辞でも intentional shared list はある」。接尾辞だけで「孤立」と判断しない。**抽出前に `grep '_modules47\|_NN' check.py` で他 check からの参照有無を確認**するか、**抽出→consistency check の NameError で即判別→revert**（安全網が機能するので試して戻せる）。

### 4.2 global content を読む大カテゴリ（`_ctx` enrich が必要）

- **class**: `html` / `mainjs` / `ai2ai` / `style` / `mcp_data`（monolith 冒頭で一度 read される共有 global content）を直接読む Check 群（AIO 系 category B / version 系 category A-check / SEO 系 category C）。これらは現 `_ctx` に含まれないため、そのまま抽出すると NameError。
- **次の手**: `_ctx` に `html=html, mainjs=mainjs, ai2ai=ai2ai, style=style, mcp_data=mcp_data` を追加（enrich）してから大カテゴリを module へ抽出。これで最大の塊（AIO 系）を段階抽出でき monolith を実質縮小できる。
- **代替**: module 側で対象ファイルを `ctx.read()` で re-read する（Phase 5 の 48-51 はこの方式。workflow / index.html / eslint.config.mjs / package.json / runbook を fresh read）。global content が大きい場合は re-read コストより ctx enrich が効率的。

### 4.3 厳守事項（安全プロトコル）

- **一撃分割は厳禁**。カテゴリごと 1 PR。各 PR で `npm run verify` = exit 0。
- **孤立カテゴリを選ぶ**。抽出対象が monolith の共有 computed 変数に依存すると壊れる（consistency check が即 NameError で捕捉するので試して revert 可）。
- **honest 観測**: Check 52 advisory が check.py の budget 4,750 超過（実 15,066）を warning 中 = 分割で縮小すべき bloat の live signal。これがゼロに近づくのが C 完了の目安。

---

## 5. C の 2 番目ターゲット = e2e/portfolio.spec.js（3,475 行・未着手）

- **de-risk 手法**: e2e spec は「9-check の名前結合」がある（複数テストが同じ describe/命名規約で結合）ため**単純な行数分割は vacuous 化リスク**（名前結合が切れて silent にテストがスキップされる）。CLAUDE.md §7 の disposition で「9-check 名前結合ゆえ単純分割は vacuous 化・defer」と記録済。
- **安全な分割**: Playwright は複数 spec ファイルを自動 discovery するので、**テーマ別（apps CRUD / AIO meta / security / resilience / a11y / bug-regression）に spec ファイルを分ける**のが筋。ただし分割後も behavior gate（BLOCKING）が全テストを確実に実行することを、**mutation-probe-e2e で「clean=pass・mutated=fail」の二段検証**してから merge する（vacuous 分割を防ぐ）。
- **注意**: `playwright-regression.yml` の behavior job が新 spec ファイルを拾うことを確認。spec discovery glob（`e2e/*.spec.js`）が効いているか要検証。

---

## 6. B カテゴリ（C 完了後・未着手）

- **style.css（2,178）**: 単一 stylesheet の設計制約。CSS `@import` は追加 HTTP request を生む（C1 Boring Technology / perf budget Check 120 と緊張）。分割するなら build step 不使用の前提で `<link>` 複数化を検討するが、Check 135（stylesheet 配線）との整合と screenshot advisory への影響を精査。**是非自体を C 完了後に再検討**。
- **index.html（1,308）**: 単一 SPA entry の設計制約。JSON-LD / CSP / AIO meta が集中。分割困難。
- **docs**: 大きい docs（check-map 等）は節分割やアーカイブ rotation を検討。

---

## 7. capstone（全ファイル ≤1,000 達成後・未着手）

owner 合意の最終防止層: **A 以外の全ファイルが 1,000 行以下に収まったら、CI で ≤1,000 を監査化**。

- **実装方針**: 既に Check 363 が `js/*.js` ロジック leaf に `<!-- JS-LEAF-CEILING 1000 -->` marker ベースの BLOCKING 上限を持つ。これを **`LINE-CEILING` として汎化**し、A（mp3/package-lock/main.js/llms-full.txt）を除外リストで明示除外した上で、**全 tracked file の行数が 1,000 以下**であることを BLOCKING 強制する Check を新設。
- **除外リストの扱い**: A は honest に「なぜ除外か」を marker/docstring に明記（設計制約・保護 kernel・外部生成・AIO canon）。除外を padding にしないため、除外理由が消えたら（例: main.js が分割可能になったら）除外も外す規律を docstring に書く。
- **段階性**: 全ファイルが実際に ≤1,000 になる前にこの Check を BLOCKING 化すると CI が永久 RED になる。**C+B 完了を確認してから capstone を入れる**（順序厳守）。

---

## 8. 本セッションで発生した事故と復旧（次担当が同じ轍を踏まないため）

### 8.1 `git checkout -b` の silent 失敗で main へ commit 着地（Phase 4）

- **症状**: Bash の安全 classifier が一時不能だと `git checkout -b <branch>` が**失敗するのに後続コマンドは続行**し、`main` 上で編集→commit してしまう（local main が ahead 1 に）。
- **復旧（force-push 不使用）**: `git branch <feature>`（現 HEAD=誤 commit を feature 化）→ `git checkout <feature>` → `git branch -f main origin/main`（local main を origin に合わせて復元）→ feature を push/PR。origin/main は未汚染で済む。
- **予防**: `git checkout -b` の**直後に必ず `git branch --show-current`** で branch 名を確認してから編集を始める。memory `feedback_merge_before_new_branch` に収載済。

### 8.2 mutation-probe-e2e の 2 分タイムアウトで apps.js が mutated 残留（SIGTERM）

- **症状**: mutation-probe-e2e を full suite で走らせると 2 分タイムアウト → SIGTERM がファイルを mutated 状態で残留させ、次の verify が偽 RED になる。
- **復旧**: `git checkout <file>` で mutated ファイルを復元。
- **予防**: mutation-probe は **verify と別コマンドで単独実行**し、完全終了を待ってから verify。連結すると復元競合でファイル残留。memory `feedback_mutation_probe_verify_race` に収載済。

### 8.3 force-push の deny（#576 amend 時）

- **症状**: `git push -f` が安全ゲートで deny。
- **対応**: amend せず**新 commit を上に積む**（fast-forward push）。rebase 後の PR 更新が必要なら**新ブランチ + 新 PR**で（force-push は使わない）。

### 8.4 Pages deploy の transient 失敗

- 「Deployment failed, try again later」= GitHub インフラの transient で、dev-tooling-only 変更が原因ではない。retry で self-heal。

---

## 9. ツール安定性の知見（自走が「止まる」最頻原因）

- **最頻原因はツール呼び出しの XML 形式エラー**（`antml:invoke` の開始タグが化ける）。誤形式は無実行 = 停止に見える。**全 tool 呼び出しは `antml:invoke`/`antml:parameter` の正規形で、呼び出し直前の prose を最小化すると安定**（実測）。memory `feedback_tool_call_format` 収載。
- **session が長引くと Bash classifier が一時不能**になり `git checkout -b` が silent 失敗しうる（§8.1）。長時間 context では各ステップを小さく・verify・branch-check して進める。

---

## 10. 不変の厳守事項（トラック横断・忘れると壊す）

1. **category A 不可侵**: mp3 / package-lock.json / main.js / llms-full.txt を分割対象にしない（owner 明言 + C1/C6/保護 kernel）。
2. **1 PR = 1 カテゴリ**、各 PR で `npm run verify` exit 0、自己整合 Check 45/70/105 が全 module 横断で緑。
3. **merge 後は HEAD=main**。次増分の**最初の編集前に必ず `git checkout -b` + `git branch --show-current` 確認**（§8.1）。
4. **force-push / `git add .` / `-A` は deny**。explicit `git add <paths>` のみ。rebase 更新は新ブランチ+新 PR。
5. **mutation-probe は verify と別コマンドで単独実行**（§8.2）。
6. **新 tracked file には mirror doc**（Check 108）+ improvement-notes なら **README inventory 追記**（governance Check）。
7. **§7 ハンドオフを薄くして commit log で代替しない**（両方厚く・CLAUDE.md §5）。
8. **「枯渇/収束」の自己判断禁止**（102e）。停止権限は人間のみ。収束と感じても最低 5 案を pros/cons で出して自走（memory `no-terminal-done-state`・本セッションでも該当）。
9. **Check 総数の真値は `total-check-runbook.md` §9**（現 **364**・Check 70 強制）。§7 の数値が drift したら §9 を正とする。
10. **非破壊証明**: dev-tooling-only 変更でも shipped 資産（main.js / style.css / index.html / AIO layer / binary）の byte 不変を確認。分割は挙動 byte-equivalent を verify で証明してから merge。

---

## 11. 本セッションの他の成果（トラック外・完了済）

check.py 分割トラックと並走で、ingestion-crash class を store.js で完全閉鎖した（前セッションからの継続・全 merge 済）:

- **#568**: `normalizeAppsData` の `ai.history` / `pomodoro.history` を `Array.isArray` ガード（非配列 ingestion crash・total 関数契約の outlier）。
- **#572**: `normalizeProject` の array field（tech/tags/highlights/relatedProjectIds/links）を `Array.isArray` ガード。
- **#573**: `normalizeAppsData` の `task.tags` を `Array.isArray` ガード（最後の未ガード枝）。
- **#574**: **Check 364**（BLOCKING）新設 — store.js に unsafe `(X || []).<throwing array-method>` idiom が無いことを構造強制。per-instance fix を class 構造防止へ昇華（肥大化 Check 363 と同じ「解消+再発防止」規律の ingestion-safety 版）。honest carve-out: `str.match(...) || []).map`（Array|null 契約ゆえ安全）を regex が誤検出 → 直前を `\w` に限定して method-call 結果を除外。

**教訓（store ingestion）**: (i) producer（default builder）が安全でも consumer（untrusted import normalizer）は独立に穴を持つ — 両方を縛れ。(ii) per-instance で同 class を N 回潰したら「再混入の構造防止 Check」へ昇華せよ。(iii) 構造防止 Check の regex は安全な同型 idiom を false-positive しうる — 非 vacuous 実証と同時に false-positive carve-out も honest に行う。(iv) 外部 ingestion（load/import/cross-tab/snapshot-restore）は一つ残らず同じ正規化を通せ（#93/#295/#561/#568 class）。

---

## 12. cold-start 復帰手順（次担当 AI へ）

1. **読む順**: CLAUDE.md §7 → 本ファイル → `total-check-runbook.md` §9（Check 総数の真値）→ `decision-v80-phase4-bloat-reduction-1000-line-threshold.md` の Addendum → `check-repository-consistency-map.md` §0/§4 → memory `reference_checkpy_split_pattern` / `feedback_bloat_1000_line_threshold` / `feedback_merge_before_new_branch`。
2. **状態確認**: `git branch --show-current`（main のはず）→ `git status`（clean）→ `gh pr list --state open`（空）→ `python3 .github/scripts/check_repository_consistency.py`（exit 0）→ `wc -l .github/scripts/check_repository_consistency.py`（15,066 前後）。
3. **Phase 6 開始**: §4 の 2 class（coupled-group / global-content）から**次の抽出ターゲットを 1 つ選ぶ**。coupling を grep で確認 → **`git checkout -b refactor/checkpy-phase6-<cat>` → `git branch --show-current` で確認** → §2.2 の 6 ステップで抽出 → verify exit 0 → mirror doc → PR → CI 緑 → **merge 完了まで閉じる** → main 同期。
4. **収束と感じても停止しない**（102e/no-terminal-done-state）。C が終わったら e2e spec（§5）→ B（§6）→ capstone（§7）。無限に genuine 増分はある。

---

*この引き継ぎ書は本セッションの「最後の力を振り絞った」完全記録。次担当が読むだけで check.py 分割トラックを 1 手も損なわず継続できることを目標に、合意・パターン・落とし穴・次の手・厳守事項を余さず注ぎ込んだ。改善に終端は無い。*
