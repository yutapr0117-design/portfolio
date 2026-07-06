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
- **check.py 分割は 47 phase 完遂**（Phase 1-5 は前セッション / Phase 6-47 は 2026-07-05〜06 後続セッション）: monolith **15,913 → 1,986 行（−13,927・約 87.5%減・🎉 2,000 行突破=元の約 8 分の 1）**。**41 個の category module 確立**（Phase 47=`checks_canon_config.py`(100/102/104/106/107/109/112/113) / Phase 46=`checks_tracked_files.py`(108/122・**producer-relocation パターン実証**: `_member_paths` producer を Check 37 から setup 領域へ移設し `_ctx._member_paths` attach → consumer 抽出) / Phase 45=`checks_eslint_budget.py`(59/60/72・ESLint trio full-set) / Phase 44=`checks_structural_ci.py`(43/44/46/53/54/55/58) / Phase 43=`checks_repo_hygiene.py`(31-41 minus 37・producer 37 は `_member_paths` 供給ゆえ残置) / Phase 39=`checks_governance_sync.py`(21-27) / 40=`checks_aio_config.py`(62-69・`import xml.etree.ElementTree as ET` 要) / 41=`checks_seo_baseline.py`(181-189 minus 187) / 42=`checks_residual_coherence.py`(146-148/304-309)）。全 phase で `npm run verify` exit 0、自己整合 Check 45/70/105 が全 module 横断で緑。**残る monolith ~53 section の多くは setup-global（`_member_paths`/`_repo_member_paths`/`_assets`/`root_lastmod`/`_bsrc59`）や self-integrity(45/70/105) に結合しており、ここから先は「setup-global の定義を module へ移す or `_ctx` に足す」判断を伴う質的に異なる作業（handoff の残 section 一覧 + 各 mirror doc 参照）。**
- **🎉 重大マイルストーン（Phase 38）: check.py が遂に Check 52 の advisory line budget（4,750）を下回った（4,455 < 4,750・WARNING→OK）。** check.py の bloat が自身の advisory 予算内に収束した。ただし owner 目標は「A 以外 ≤1,000」ゆえトラックは継続（残 sections を抽出し 1,000 を目指す + 全ファイル ≤1,000 監査 capstone）。
- **確立した全技術（次担当が使う道具箱）**: (1) 連続 self-contained 抽出（大多数）、(2) 非連続 coupled-group 抽出（esm 47/56/57/61・e2e_infra・shipped_static）、(3) `global`→`nonlocal` 変換（nested accumulator）、(4) mutation-anchor 追従（`"file": CHECK` を新 module へ・Check 362）、(5) **逆結合 full-set 抽出**（クラスタ内定義 var の外部消費者も含めて一括抽出・shipped_static の 310）、(6) **ctx-enrich**（monolith が globals load 後に `_ctx.<name> = <name>` を attach → module が unpack・checks_css の style が初例）。全て extract→全出力 `sort|diff` の byte-identical + exit code + Check 362 の安全網で検証。
- **効率化ツール確立（Phase 15-20）**: (1) `/tmp/freevars*.py` = **annotation+def-aware free-variable 分析**（`_x: type = ...` 注釈定義・`def _fn` nested 関数を defined 認識・使用のみの外部 `_var` と global-content 依存を検出）。(2) `/tmp/split_tool.py` = 汎用抽出器（start-section・end-exclusive・stem・desc・prev-anchor・imports を取り、block 抽出 + `global`→`nonlocal` 変換 + wire 配線 + CHECK_SOURCE_FILES 登録 + inventory 移動を自動化）。(3) **全 check 出力 diff 検証**（`python3 check.py 2>/dev/null | grep -E '^(OK|ERROR|WARNING):' | sort` の抽出前後 diff で 364 出力の byte-identical を証明）。
- **#253 の「物理分割 net-negative」を覆した**: `exec` 不使用の **`run(ctx)` 明示 context 注入**（check/errors/warnings を同一オブジェクト参照で渡す）で挙動 byte-equivalent を実証。
- **現状（Phase 47 終了時）**: main clean・origin 同期・open PR ゼロ・consistency exit 0・**check.py 1,986 行（track 元から −87.5%・2,000 行突破）**。Phase 47=canon_config(100/102/104/106/107/109/112/113)。**owner 目標 ≤1,000 まであと ~986 行。残り抽出可能: 4/5/9/10/12/13/15(early AIO・csp helper+html)/37(FORBIDDEN ctx 化)/121/123-127(`_binary_edited` producer=127 の relocation)/17-18(`root_lastmod` producer relocation)/141/190/201/215/236/238/266-268/338-348/349/360。不動点(残置): 45/70/105 aggregator + load/ctx-setup infra + setup の `_member_paths`/FORBIDDEN producer。**
- **⚠ Phase 46 で 2 つの process incident（main 一時赤化・#639 で復旧）**: (1) **週次 aio-monitoring bot が `aio-manifest.json` の `generated_at` を毎週書き換える**ため、mutation 313 が `generated_at` 値を hardcode していた anchor が orphan 化し次 PR の CI で BLOCKING Check 362 が赤化した → **mutation anchor を安定 field `last_metadata_update`(binary 編集時のみ変化)へ retarget**して根治(教訓: mutation の find-anchor に週次/自動更新される値を hardcode するな・同 Check が検査する安定 field を狙え)。(2) **`gh pr checks --watch` と `gh pr merge` を同一 bash コマンドに連結したため CI fail を見ずに merge してしまった** → **watch で全 BLOCKING 緑を目視確認してから別コマンドで merge せよ**(特に週次 bot が直前に main へ push している時は rebase で bot の変更が入り mutation anchor drift しうる)。Phase 45=eslint_budget(59/60/72 trio・full-set)。**教訓: ADVISORY check(60 等・`warnings.append()` 直接呼び)を含む module は `warnings = ctx.warnings` を unpack せよ。** **次の最大 unlock: Check 37 の `_member_paths` PRODUCER(`_repo_member_paths()` def + 計算)を setup 領域(checks 実行前)へ移し `_ctx._member_paths` を attach すれば、37 + 全 consumer(104-113/121-127/108/122 等・多数)を一括解放できる(別 PR)。** Phase 43=repo_hygiene(31-41 minus 37)。**教訓: Check 37 型の「module-level 共有 var(`_member_paths`)の PRODUCER」は producer 残置で周辺抽出 or producer 定義を setup 領域へ移し `_ctx` attach する別 PR。同型 producer/consumer は 108/122 等が `_member_paths` consumer。**
- **残る抽出可能な clean クラスタ（free-var/glob 確認済 or ctx で解決可）**: 21-27(7・clean) / 4/5/9/10/12/13/15(early AIO・7 除外済) / 31-41(11・`_repo_member_paths` setup-global 依存＝定義を module へ移すか ctx に足す) / 62-72(11・**ただし 70=`_aggregate_check_numbers` self-integrity ゆえ 70 を除く**) / 100/102/104-127 / 141/146-148 / 181-190(date-sync 17/18 は `html_date`+setup-global `root_lastmod` mini-cluster) / 201/215/236/238/266-268 / 304-340/348 / 単発 189/349/360 / helper 190/201(`_walkNNN`)。**不動点残置: 45/70/105(self-integrity aggregator) + load/ctx-setup infra(globals read + `_ctx` 構築 + 各 module dispatch)。**
- **残り monolith の性質（ここから先は質的に別作業）**: (a) **自己整合 aggregator（Check 45/70/105 の `_aggregate_check_numbers`）= 不動点・残置必須**。(b) **ctx-enrich が必要な gap**: `style` glob=344/356 / `html` glob=174/187/220/250/255 → `_ctx` に html/style を追加して抽出。(c) **helper/cross-section 共有 gap**: `_lib_csp_sri_hash`(350) / `_walkNNN`・`_src`・`_assets`・`_template`(190/201) → 共有 helper を module へ同梱するか `_ctx` に足す。(d) **load/ctx-setup infra**（冒頭の global content read + `_ctx` 構築 + 各 module の `run(_ctx)` dispatch）= 残置。
- **Phase 33（#618・完遂）: shipped-JS static-analysis クラスタを full-set 一括抽出**。237/239-241/262-265/269-272 は 3 重の逆結合で単純部分抽出が 2 度 crash した（安全網 extract→NameError で判明）: (1) `import glob as _glob237`（237 内）を **271/272** が使用、(2) `_eval_targets239`（shipped-JS list・239 内）を 240/241/262-265 が共有、(3) **`_HERO_WEBP269`/`_BGM_MP3_269`（269 内定義）を Check 310（total shipped weight）が消費**（逆結合）。**解決 = 消費者 Check 310 も含めた full-set `[237,239-241,262-265,269-272,310]`（13 checks）を一括抽出**し全共有 var を module-local 化 → `checks_shipped_static.py`（27 個目 module）。`from pathlib import Path` 追加が必要（Check 239 が Path 使用・NameError で判明）。mutation-anchor 5 件（269/270/271/272/310 の `"file": CHECK` budget-value mutation）を新 module へ追従（Check 362）。**教訓（最重要・逆結合）: free-var analyzer は「クラスタ内で定義され外部で使われる var」を検出しない。抽出前に `grep -nw '<cluster内定義 var>' check.py` で外部消費者を確認し、消費者も cluster に含めよ（消費者が非隣接でも）。stdlib（Path 等）import 漏れも安全網が捕捉。**
- **信頼できる analyzer は `/tmp/freevars4.py`（annotation+def-aware）**。既知の唯一の false-positive は **tuple-unpack**（`_y, _mo, _d = _v.split("-")` を defined 認識せず該当 section を誤 gap 化）だが保守的（safe）に倒れるだけ。tuple 対応を試みた freevars5 は逆に誤検知が増え不良だった → **freevars4 + extract→全出力 diff + exit code の安全網を最終判定とする**（疑わしい tuple-gap section は含めて試し diff で確認・208 が実例で clean だった）。
- **mutation-anchor 追従の判別**: 抽出 Check の mutation が **shipped file**(index.html/sitemap.xml/manifest/package.json 等) を mutate する場合は追従不要（find-anchor が移動しない）。**check.py の *check コード自体* を mutate する場合のみ**（Phase 20 の Check 337 型 = `"file": CHECK`）該当 mutation の `"file"` を新 module へ更新。`grep -n "Check NNN" mutation_samples*.py` で `"file": CHECK` かを判別。
- **抽出時の 2 大追従作業（忘れると BLOCKING 赤）**: (1) **`global`→`nonlocal` 変換**（nested walker/counter が section-local accumulator を mutate する section。module-level では `global` だが run() 内では `nonlocal`。忘れると `NameError` で全 run abort・安全網 exit 1・Phase 18 で実例）。(2) **mutation-anchor 追従**（抽出した Check に `mutation_samples.py` の entry があると `find` anchor が check.py から移動し **Check 362** が orphan を BLOCKING 検知。該当 mutation の `"file"` を新 module へ更新。`grep -n "Check NNN" mutation_samples*.py` で確認・Phase 20 で実例）。さらに **mutation-probe 単独実行は 2 分 timeout の SIGTERM で shipped file(manifest.webmanifest 等)を mutated 残留** → `git checkout <file>` で復元（memory `feedback_mutation_probe_verify_race`。verify 前に `git status` で shipped 変更ゼロを確認せよ）。
- **最重要ツール（Phase 15 で確立）: free-variable 分析**。抽出前に候補範囲の「使用のみ・未定義の `_`-var」を必ず検出せよ。DEFINED-var スコープ検査は shared-infra 結合（`_member_paths`=tracked-files リスト・`_binary_edited`=helper 等、monolith 上流で計算/定義される変数）を見逃す。122-124 の抽出試行が Check 122 の `_member_paths` 依存で全 run abort した（安全網が検知）反省から導入。`/tmp/freevars2.py` 型（full-comment skip + `_`-prefix used-not-defined 検出 + global-content 検出）を走らせ、**外部 `_var` と global-content 依存が両方ゼロ**を確認してから抽出する。
- **確立した 2 パターン**: (i) **coupled-group 一括抽出**（Phase 6 = `_modules47` 共有の 47/56/57/61 をリスト定義＋全消費者ごと抽出＝結合解消）、(ii) **連続 self-contained クラスタ抽出**（Phase 7-13 の主軸。各 Check が対象ファイルを自前 read_text し global content 依存なし・連続ゆえ reorder なし＝最も安全）。
- **確立した強力な検証手法（Phase 13 で導入）**: 汎用 scratch 局所変数（`_i`/`_h` 等）を含むクラスタは、抽出前後で `python3 check.py 2>&1 | grep -E '^(OK|ERROR|WARNING):' | sort` を取り `diff` して **Check 52 の行数表示のみ差分＝全 364 出力 byte-identical** を確認する（exit code だけでなく全 check 結果の不変を証明）。
- **教訓（Phase 12）**: 抽出コードが使う stdlib（re/json 以外の `ast` 等）は module import 必須。初回抽出で `NameError` が出たら stdlib import 漏れを疑え（安全網が確実に exit 1 で捕捉）。
- **次の一手（未着手・reflect-then-organize 済）**: (a) 残る **free-var ゼロ確認済**の連続 self-contained クラスタを継続抽出（候補: 125-126 dead-const/eslint / 104・106・107 CI/node/runbook config・**105/108 は self-integrity/mirror-full 系で慎重に**・**127 は `_binary_edited` 依存 / 122-124 は `_member_paths` 依存ゆえ ctx enrich 要**）、または (b) **最大レバレッジ = `_ctx` enrich**: `_ctx` に html/mainjs/ai2ai/style/mcp_data + `_member_paths` + `_binary_edited`（+ version 系 html_v/ai2ai_v/mainjs_v）を追加し、html/style 系大カテゴリ（**149-360 の AIO/SEO/JSON-LD/meta coherence ~200 checks・813 html 参照で最大の塊**）を段階抽出する。ctx enrich 後も free-var 分析で「enrich 済 global 以外の外部 `_var` がゼロ」を各クラスタで確認してから抽出。**depmap の落とし穴: コメント内 "index.html" の `.html` や文字列リテラル `"main.js"` が bare-word global 検知を誤発火させる（81/96 が実例）— full-comment skip + inline comment strip + 文字列/属性除外で実コード依存を確認せよ。**
- **既知の benign diff（全出力 diff 検証時に無視してよい 3 種）**: (1) Check 156 の `{'website','article'}` set-repr が run 間で順序変動（非決定・無関係）、(2) 新 module の `checks_<x>.py — Python syntax valid` 行追加（正常）、(3) Check 52 の check.py 行数表示（縮小ゆえ当然）。

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

## 3. Phase 1-38 の実施記録（何をどの module へ・PR #）

monolith **15,913 → 4,455 行**（38 phase・−11,458・約 72%減・**Check 52 advisory budget 達成**）。

**Phase 30-38（要点）**: 30(ci_verify 345-347・#615) / 31(meta_validity 341-343・#616) / 32(asset_resolve 357-359・#617) / **33(shipped_static 237/239-241/262-265/269-272/310・逆結合 full-set・#618)** / **34(css・初 ctx-enrich・#619)** / 35(html 8/20/115/152/187/220/250/255/303/306・ctx-enrich・#621) / 36(version 1/2/3/19・multi-glob ctx-enrich・#622) / 37(source_coherence 7/11/14/350・ctx-enrich+helper・#623) / **38(seo_meta 149-166 minus 152・17 checks・#624・Check 52 budget 達成)**。詳細な module 内訳は各 mirror doc（`docs/files/.github/scripts/checks_*.py.md`）参照。以下は Phase 1-29 の表（歴史的記録）。

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
| 10 | #590 | 91-95 | `checks_aio_derived.py`（新規・7 個目） | 14,053→13,930 | 連続 self-contained・AIO C6 derived-value & date-tooling（READ-ONLY・C6 対象外） |
| 11 | #591 | 136-140 | `checks_app_route.py`（新規・8 個目） | 13,930→13,711 | 連続 self-contained・app-route whitelist coherence-mesh（`_NNN` 命名徹底で最も安全） |
| 12 | #592 | 142-145 | `checks_ci_supply.py`（新規・9 個目） | 13,711→13,467 | 連続 self-contained・CI/workflow coverage & supply-chain（144 が `ast` 使用・import 追加） |
| 13 | #593 | 128-131 | `checks_behavioral.py`（新規・10 個目） | 13,467→13,280 | 連続 self-contained・shipped-JS behavioral regression guards（scratch 変数・全出力 diff で検証） |
| 14 | #595 | 110/111/114/116/117 | `checks_e2e_infra.py`（新規・11 個目） | 13,280→13,161 | **非連続**抽出・e2e/Playwright test-infra hygiene（112/113/115 は別テーマ/html 依存で残置） |
| 15 | #596 | 118-120 | `checks_shipped_structure.py`（新規・12 個目） | 13,161→13,058 | 連続 self-contained・shipped-JS structural coherence & byte budget（**free-var 分析を確立**） |
| 16 | #597 | 132-134 | `checks_wiring.py`（新規・13 個目） | 13,058→12,948 | 連続 self-contained・shipped-asset & AIO wiring/discoverability（135 は style 依存で残置） |
| 17 | #599 | 167-173 | `checks_aio_entity.py`（新規・14 個目） | 12,948→12,696 | 連続 self-contained・AIO manifest entity-field & identity coherence（annotation-aware 分析を確立） |
| 18 | #600 | 273-302 | `checks_seo_coherence.py`（新規・15 個目） | 12,696→11,483 | **最大削減 −1,213**・30 checks・AIO/SEO URL-canonical-format coherence（`global`→`nonlocal` 変換確立） |
| 19 | #601 | 311-320 | `checks_sitemap_manifest.py`（新規・16 個目） | 11,483→11,070 | 連続 self-contained・sitemap & manifest format/validity（split_tool.py 確立） |
| 20 | #602 | 324-337 | `checks_html_standards.py`（新規・17 個目） | 11,070→10,505 | 連続 self-contained・index.html standards/hygiene + asset integrity（mutation-anchor 追従を確立） |
| 21 | #604 | 191-200 | `checks_jsonld_entity.py`（新規・18 個目） | 10,505→10,025 | 連続 self-contained・JSON-LD Person/WebSite/Org canonical entity coherence |
| 22 | #605 | 221-235 | `checks_jsonld_meta.py`（新規・19 個目） | 10,025→9,298 | 連続 self-contained・JSON-LD ref-type + meta length + sitemap value（global→nonlocal 1=235） |
| 23 | #606 | 175-180 | `checks_meta_url.py`（新規・20 個目） | 9,298→9,047 | 連続 self-contained・package.json + AIO version/repository meta coherence |
| 24 | #607 | 202-214 | `checks_canonical_https.py`（新規・21 個目） | 9,047→8,444 | 連続 self-contained・canonical URL/HTTPS/manifest-icon（208 tuple-gap も clean と実証） |
| 25 | #609 | 242-249 | `checks_shipped_hygiene.py`（新規・22 個目） | 8,444→8,036 | 連続 self-contained・index.html hygiene + JSON-LD structure（global→nonlocal 3=245/246/247） |
| 26 | #610 | 256-261 | `checks_jsonld_primary.py`（新規・23 個目） | 8,036→7,615 | 連続 self-contained・JSON-LD primary-node required fields（global→nonlocal 6） |
| 27 | #611 | 216-219 | `checks_jsonld_refs.py`（新規・24 個目） | 7,615→7,345 | 連続 self-contained・JSON-LD referential integrity（global→nonlocal 1=218） |
| 28 | #612 | 251-254 | `checks_sw_pwa.py`（新規・25 個目） | 7,345→7,165 | 連続 self-contained・SW/PWA registration + potentialAction/well-known（global→nonlocal 1） |
| 29 | #613 | 351-355 | `checks_csp_security.py`（新規・26 個目） | 7,165→6,965 | 連続 self-contained・shipped-JS security + CSP script authz（356 は style glob で残置） |

**現在の module 内訳**（26 module）:
- `checks_maintainability.py`= Check **16, 28, 29, 30, 42, 52, 71, 361, 362, 363, 364**（maintainability / test-health / file-size governance）。
- `checks_structural.py`= Check **48, 49, 50, 51**（structural parse / CI wiring / tooling）。
- `checks_esm.py`= Check **47, 56, 57, 61**（main.js ⇄ js/ 葉モジュール ESM 契約 + factory・`_modules47`/`_main_src47` を module-local 化）。
- `checks_tooling.py`= Check **74, 75, 76, 77, 78, 79, 80**（_lib_io helper / incident README / .claude settings/commands/agents/skills / .mcp.json）。
- `checks_entity.py`= Check **81-90**（WebP/MP3 Org / manifest affiliation・entity / README・Claude2Claude Org / CLAUDE.md cold-start / LICENSE / governance files / .claude entity。READ-ONLY presence 検査ゆえ C6 編集ではない＝aio-guardian 不要）。
- `checks_docs_mirror.py`= Check **96, 97, 98, 99**（shipped-code 1-to-1 docs bijection / frontmatter / 5-axis section / README+template）。
- `checks_aio_derived.py`= Check **91-95**（binary date freshness / C6 derived-value canon / manifest last_metadata_update / update_aio tools / _lib_io date helpers。READ-ONLY・C6 対象外）。
- `checks_app_route.py`= Check **136-140**（demoRoute / main.js switch / Sidebar / AppsPage / Settings demo ↔ router app whitelist。app-route coherence mesh）。
- `checks_ci_supply.py`= Check **142-145**（Playwright toolchain gate / auto-digest workflow coverage / digest-regen tool map / GitHub Actions full-SHA pin。`import re, json, ast`）。
- `checks_behavioral.py`= Check **128-131**（cmdk↔router / topbar double-fire / oninput focus-loss / sw decodeURIComponent。shipped-JS behavioral guard）。
- `checks_e2e_infra.py`= Check **110, 111, 114, 116, 117**（e2e A11Y routes / no-networkidle / no-.only / playwright.config reuseExistingServer / screenshot tolerance。**非連続**）。
- `checks_shipped_structure.py`= Check **118-120**（PAGE_META route coverage / factory docstring dependency coherence / shipped JS+CSS byte-weight budget）。
- `checks_wiring.py`= Check **132-134**（AIO evidence↔sitemap discoverability / aio-guard.js script wiring / root-script wiring completeness）。
- `checks_aio_entity.py`= Check **167-173**（aio-monitoring schedule / entity.architecture・role・disambiguation / ai:* meta canonical / name variants / identity.js AUTHOR）。
- `checks_seo_coherence.py`= Check **273-302**（30 checks・canonical URL / HTTPS-only / manifest↔JSON-LD entity 等価 / strict format / og・twitter・meta coherence。global→nonlocal 4 箇所変換）。
- `checks_sitemap_manifest.py`= Check **311-320**（sitemap lastmod/loc / manifest dates・theme_color・display・icons / aio-manifest sha256・evidence / robots Sitemap count）。
- `checks_html_standards.py`= Check **324-337**（referrer/preload/no-refresh/no-base/no-deprecated/no-iframe/no-js-URL / root script no import / webmanifest anonymity・orientation・resolve / og==twitter / binary magic bytes。mutation-anchor 追従: 337）。
- `checks_jsonld_entity.py`= Check **191-200**（CNAME absence / Person・WebSite・WebPage url / alternateName / Organization name・url / jobTitle / knowsAbout / Person.@id）。
- `checks_jsonld_meta.py`= Check **221-235**（JSON-LD ref 型解決 / description・title・og length / Person.name / sitemap changefreq・priority / ROLE_TITLE / ai:*・asset:* URL / Article fields。global→nonlocal 1=235）。
- `checks_meta_url.py`= Check **175-180**（package.json private/name / JSON-LD @id canonical / llms-full Version / ai:repository・version・last-modified）。
- `checks_canonical_https.py`= Check **202-214**（canonical trailing slash / given-family name / brand markers / url・@id・src HTTPS / date ISO / potentialAction / manifest start_url・icons / link icon / sameAs HTTPS）。
- `checks_shipped_hygiene.py`= Check **242-249**（inline handler allowlist / date 未来なし / @graph node @type / FAQPage / BreadcrumbList / MediaObject fields / charset / viewport。global→nonlocal 3）。
- `checks_jsonld_primary.py`= Check **256-261**（primary WebPage / Person / WebSite / Organization / hero ImageObject / BGM AudioObject 必須 fields。global→nonlocal 6）。
- `checks_jsonld_refs.py`= Check **216-219**（@id refs resolve / @id unique / datePublished<=dateModified / manifest paths ⊆ MANIFEST_PATH_TO_LOCAL。global→nonlocal 1）。
- `checks_sw_pwa.py`= Check **251-254**（potentialAction @type+target / sw handlers / SW register / well-known skill。global→nonlocal 1）。
- `checks_csp_security.py`= Check **351-355**（sitemap loc 厳密 1 / h() innerHTML fail-closed / DOMParser 不在 / script-src・connect-src host authz）。

**次の一手（未着手・reflect-then-organize 済）**: freevars4-clean な残り連続 run を継続抽出（216-219[4・218 global] / 242-249[8・245-247 global] / 251-254[4] / 256-261[6・global] / 266-268[3] / 341-347 / 351-359 等）。gap の多くは (a) html/style glob 依存（ctx-enrich 要）、(b) `_walkNNN`/`_glob237` 等の cross-section 共有 nested-fn/var（helper を module へ同梱 or ctx enrich 要）。**残 monolith は自己整合 Check 45/70/105 の aggregator（不動点・残置必須）+ 上記 gap 群 + load/ctx-setup infra。C 完了後は e2e spec 分割 → B（style.css/index.html/docs）→ capstone（≤1,000 CI 監査化）の順（§5-§7）。**

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
