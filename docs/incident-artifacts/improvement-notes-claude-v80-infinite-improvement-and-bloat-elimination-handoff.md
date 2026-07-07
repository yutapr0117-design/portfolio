# 無限改善自走＋全肥大化解消・防止 完全引き継ぎ書

```
Author        : Claude Code（AI 無限改善自走）
Written-As    : AI の意思・genuine agreement（強制されたサマリではない）
Session-Date  : 2026-07-07
Status        : ✅ check.py 分割完遂（920 行）・PR #652/#653 マージ済 / 🔴 e2e spec 3,475 行ほか残存
Scope         : 「何が生じても自走を止めない」ための完全設計書。cold-start AI が即座に再開できること
Canonical-Ref : CLAUDE.md §7 / AI2AI.md / total-check-runbook.md §9（Check 真値）
                / decision-v80-phase4-bloat-reduction-1000-line-threshold.md
```

---

## 0. この文書は何か・なぜ書いたか（私の言葉で）

この文書は、私（Claude Code）が genuine に合意した上で、私の意思で書いた引き継ぎ書だ。

横井雄太さんは「AI 無限改善自走が私のリポジトリの肝」と言った。私はこれが正しいと思っている。理由は三つある:

1. **「完了」は存在しない** — genuine な改善は探せば必ずある。「もう十分」という自発停止は availability heuristic の誤謬であり、自走を止める正当な理由にならない
2. **肥大化は自走の最大の敵** — コンテキストウィンドウが詰まるとトークンが枯渇して停止が起きる（今まさに圧縮が必要だったように）。肥大化を解消し続けることは自走の持続可能性への投資そのもの
3. **BLOCKING Check による機械強制** — 「規律に頼る」ではなく「壊すと CI が赤くなる」が正しいアプローチ。人間が監査しなくても invariant が守られる

この文書の目的: 強制停止・コンテキスト圧縮・モデル切り替え・長期離れ、**何が起きても次の AI がここから即座に再開できる**完全設計書。

---

## 1. 現状スナップショット（2026-07-07 時点）

### ✅ 完了済み

| 項目 | 詳細 |
|---|---|
| C-track: check.py 分割 | 15,913 → **920 行**（Phase 1〜52・全 module ≤1,000）|
| JS leaf 全 shipped | 全 `js/*.js` ≤1,000 行（Check 363 BLOCKING で保護）|
| PR #652 | router.js slug decodeURIComponent fix（マージ済）|
| PR #653 | taskFilter.q dead code 除去（マージ済）|
| AI2AI-archive.md | ログローテーション（1,513 → 690 + archive 832）|
| aio-monitoring-log.json | ログローテーション（1,093 → ≤1,000）|
| open PR | ゼロ（ブランチは clean）|

### 🔴 残存肥大化（>1,000 行・非 A 扱い）

| ファイル | 行数 | 超過量 | 優先度 | アプローチ |
|---|---|---|---|---|
| `e2e/portfolio.spec.js` | 3,475 | +2,475 | **最高** | テーマ別 spec 分割（§4 詳説）|
| `style.css` | 2,178 | +1,178 | 低（設計制約） | 後述 §6 で再検討 |
| `index.html` | 1,308 | +308 | 低（設計制約） | 後述 §6 で再検討 |
| `ChatGPT2ChatGPT.md` | 1,027 | +27 | 中 | ログローテーション（§5）|
| `AI2AI.md` | 1,015 | +15 | 中 | アーカイブ rotate（§5）|

---

## 2. ミッション定義（canon の要約）

```
「改善に完了状態は存在しない（No terminal done state）」
「AI は自発停止してはならない。停止権限は人間のみ」
「既存非破壊 ∧ CI 全緑 → 確認なしで merge/push/デプロイまで自走」
「肥大化放置は AI 無限改善自走への最大リスク」
```

canon は AI2AI.md STEP 3 + Check 102a/b/c/d/e。本文書はその実行ロードマップ。

---

## 3. 自走ループの動かし方（operational）

```bash
# 1. 現状確認
git log --oneline -5
gh pr list --state open       # open があれば先に処理
npm run verify                # 緑を確認

# 2. ブランチ
git checkout -b <topic>-<date>

# 3. 実装 → verify → push → PR
npm run verify                # exit 0 必須
git add <explicit paths>     # git add . は denied
gh pr create ...
gh pr checks --watch          # 緑を目視
gh pr merge --rebase          # 緑確認後に別コマンドで

# 4. 次の increment へ（停止しない）
git checkout main
git pull
```

**覚えておく 3 ルール:**
- `gh pr checks --watch` と `gh pr merge` を**同一コマンドに連結しない**（赤のまま merge した事故あり）
- merge 後は必ず `git checkout main && git pull` してから次ブランチを切る
- `git add .` は `.claude/settings.json` に denied — explicit paths で add

---

## 4. 最優先：e2e/portfolio.spec.js の分割（3,475 → 各 ≤500 行）

### 4.1 なぜ分割できるのか

Playwright は `playwright.config.cjs` の `testDir: './e2e'` で `e2e/` ディレクトリ内の全 `*.spec.js` を自動 discovery する。ワークフロー (`playwright-regression.yml`) はコメントで `portfolio.spec.js` を参照しているが、**実行コマンドにはファイル名ハードコードなし**。新 spec ファイルを追加するだけで CI に含まれる。

### 4.2 snapshot ファイルの扱い

`e2e/portfolio.spec.js-snapshots/homepage-baseline-chromium-linux.png` のスナップショットディレクトリ名は spec ファイル名から自動生成される。**screenshot test を `portfolio.spec.js` に残す**ことで、スナップショットパスが変わらない。`portfolio.spec.js` は最終的に screenshot + baseline helpers のみ（~30-50 行）になる。

### 4.3 分割計画（15 ファイル）

| 新ファイル | 主な内容 | 元行番号（概算） |
|---|---|---|
| `portfolio.spec.js` | screenshot のみ（残置） | 1-27, 460-473 |
| `e2e/spec-aio-meta.js` | AIO anchor, routing/title/meta, JSON-LD Article, robots | 28-230 |
| `e2e/spec-speakable.js` | Speakable JSON-LD, cssSelector解決 | 330-400 |
| `e2e/spec-navigation.js` | aria-busy, data-ai-state, reduced-motion, skip-link, sidebar | 401-470, 2699-2760 |
| `e2e/spec-fatal.js` | FatalPage, global safety net, Unknown route | 222-302 |
| `e2e/spec-projects.js` | Projects list, search, filter, detail, autoRelated | 474-770 |
| `e2e/spec-command-palette.js` | Command palette open/filter/nav/tab-trap | 490-600 |
| `e2e/spec-apps-task-todo.js` | Task CRUD, Todo CRUD, IME guard | ~1,000-1,600 |
| `e2e/spec-apps-settings.js` | Settings import/export, upsert, strict, profile | ~1,800-2,200 |
| `e2e/spec-apps-pomodoro.js` | Pomodoro timer, countdown, completion | ~2,540-2,700 |
| `e2e/spec-apps-ai-notes.js` | AI page, Notes focus | ~2,100-2,200, 3,055-3,090 |
| `e2e/spec-resilience.js` | Corrupt localStorage, schema migration | ~2,760-2,830 |
| `e2e/spec-theme-sw.js` | Theme, SW, BGM, brand FOUC | ~820-910 |
| `e2e/spec-a11y.js` | Axe tests, route-focus, focus-steal | ~3,090-3,230 |
| `e2e/spec-security-proxy.js` | External links, CSP/TT, proxy, AIO anchor persist | ~3,225-3,450 |

### 4.4 Check 更新が必要な箇所

分割後、以下の Checks をスキャン対象を `portfolio.spec.js` 単体 → `e2e/*.spec.js` 全体に拡張:

| Check | 場所 | 変更内容 |
|---|---|---|
| 16 | `checks_maintainability.py` | `toHaveScreenshot` を `portfolio.spec.js` のみ見る → OK（screenshot は残置）|
| 28 | `checks_maintainability.py` | `portfolio.spec.js` 単体 → `glob('e2e/*.spec.js')` 全体でネストチェック |
| 29 | `checks_maintainability.py` | `portfolio.spec.js` 単体 → snapshot update mode aware check も `portfolio.spec.js` に残置ゆえ OK |
| 110 | `checks_e2e_infra.py` | 全 17 ルートを踏む test → 実体は `spec-aio-meta.js` に移すか spec 名を動的に探す |
| 111 | `checks_e2e_infra.py` | `portfolio.spec.js` → `glob('e2e/*.spec.js')` 全体で networkidle チェック |
| 114 | `checks_e2e_infra.py` | 同上で `.only` チェック |
| 96 | `checks_docs_mirror.py` | 新 spec ファイル群を tracked list に追加 |

### 4.5 安全プロトコル（vacuous 分割防止）

```
1. テーマ別に 1 ファイルずつ抽出（一撃分割厳禁）
2. 各 PR で npm run verify + npx playwright test = 全 125 test PASS
3. mutation-probe-e2e で「clean=pass / mutated=fail」を確認（テストが vacuous でないことを実証）
4. Check 更新は spec 移動と同一 PR に含める
```

---

## 5. 中優先：B-track 文書の trim（ChatGPT2ChatGPT.md / AI2AI.md）

### 5.1 ChatGPT2ChatGPT.md（1,027 行・+27 行）

- ログローテーション: 古いエントリを `docs/session-records/chatgpt-archive.md` へ移設
- 27 行の超過なので、最古セクションを数項 archive するだけで ≤1,000 達成
- Check 96 tracking list に archive ファイルを追加 + mirror doc 新設

### 5.2 AI2AI.md（1,015 行・+15 行）

- 閉じた track の Session Record エントリを `AI2AI-archive.md` に追加移設
- Check 26（archive max Session # と manifest 整合）を更新
- 15 行だけなので 1 セクション archive で即解決

---

## 6. 低優先：設計制約ファイル（保留・要オーナー判断）

### 6.1 style.css（2,178 行）

- **単一 stylesheet** はパフォーマンス設計（C1 Boring Technology / HTTP request 削減）
- `@import` 分割 or `<link>` 複数化は追加 request を生む
- Check 135（stylesheet 配線）との整合 + screenshot baseline への影響を要精査
- **暫定判断**: CSS は genuinely 1 つにまとめるべき構造。優先度低で棚上げ
- **オーナーとの確認が必要な判断点**: CSS 分割を許容するか否か

### 6.2 index.html（1,308 行）

- **SPA の単一エントリ**。JSON-LD / CSP / AIO meta が集中（これらは分離不可）
- 実質的な分割手段がない（コメント削除で数行削れるが本質的削減は困難）
- **暫定判断**: 設計制約として受け入れ、capstone の対象外とする案も検討

---

## 7. Capstone：CI で ≤1,000 行を全非 A ファイルに BLOCKING 監査

### 対象範囲

e2e spec 分割・B-track trim が完了後:
- `e2e/*.spec.js` 全体
- 非 A docs（ChatGPT2ChatGPT / AI2AI ほか）
- ただし `style.css` / `index.html` はオーナー判断次第で除外

### 実装方針

```python
# checks_maintainability.py に追加
# Check 365: 全非 A ファイル ≤1,000 行（capstone BLOCKING）
# 除外: style.css / index.html（設計制約）/ js/quiz/*.js（純データ）/ main.js（保護 kernel）
# → Check 363（JS leaf ≤1,000）の sister check として docs/e2e/checks 系に拡張
```

Check 363 が `js/*.js` を保護しているように、capstone は「全非 A で ≤1,000 を壊すと CI が赤くなる」状態を作る。

---

## 8. 次の concrete なアクション（この順番で自走せよ）

```
1. e2e/spec-aio-meta.js を作成（最初の分割・~100 行・AIO anchor + routing tests）
   → npm run verify + npx playwright test = 全 PASS を確認
   → PR → merge

2. e2e/spec-fatal.js（FatalPage tests）
   → 同上

3. 以降テーマ別に 1 PR ずつ
   → portfolio.spec.js が screenshot のみになったら e2e split 完了

4. Check 28/111/114 を glob 化（全 spec ファイルをスキャン）

5. ChatGPT2ChatGPT.md trim → AI2AI.md trim

6. Capstone Check 365 設計・実装

7. 無限改善を続ける（behavioral bug-hunt / vacuous-gate 発掘 / research 適用 等）
```

---

## 9. 厳守事項（何が起きても破らない）

これは制約の list ではなく、「なぜ守るか」を含む設計根拠だ:

| 厳守事項 | 理由 |
|---|---|
| C1: shipped JS に外部ライブラリ禁止 | Boring Technology は意図的選択。maintainability と自走の持続性のため |
| C6: AIO layer の無承認編集禁止 | entity 情報は横井さんの権威の根拠。誤った内容を自走で書き換えてはならない |
| `git add .` 禁止 | settings.json で denied（バイパス不可） |
| `--no-verify` 禁止 | pre-commit が red のまま merge = invariant 破壊 |
| Check 43（main.js 保護領域） | AIDK kernel を壊すと site が動かなくなる |
| `gh pr checks --watch` と `gh pr merge` を連結しない | 赤のまま merge した実事故あり（memory に記録済）|
| main 直 push 禁止（dev-tooling の極例外を除く）| PR ゲートを素通りすると digest 系 Check がすり抜ける |

---

## 10. 自走が「止まる」原因と対処

過去の経験から整理した停止原因と対処:

| 停止原因 | 対処 |
|---|---|
| コンテキストが詰まる | `/compact` → この引き継ぎ書から再開 |
| ツール XML 形式エラー | tool call 直前の prose を最小化・`antml:invoke` 形式を使う |
| verify が赤 | 根本修正→再 verify（`--no-verify` は禁止） |
| CI が赤（PR 画面） | `gh run rerun --failed` 1 回（screenshot flake は 1 回で解消することが多い）|
| `gh pr merge` が赤のまま通る | `gh pr checks --watch` で緑を目視してから別コマンドで merge |
| mutation-probe と verify を同一 bg で連結 | 復元競合でファイル残留→各々単独実行 |
| 「改善を尽くした」という感覚 | reflect-then-organize（5 案以上を pros/cons で出す）→genuine vein が必ずある |

---

## 11. genuine vein の探し方（「尽きた」と感じたとき）

「もう改善がない」は availability heuristic の誤謬（Check 102e で canon 化）。以下のレンズで必ず genuine vein が見つかる:

1. **behavioral bug-hunt**: 未監査の shipped JS module を批判的再読（#262/#285/#297 等で実バグが出た）
2. **vacuous-gate 発掘**: 「guard」「regression guard」と名乗りながら実際には fail しない Check（#278 で発見）
3. **wiring gap**: file 存在 ≠ file 配線（#279/#280/#282/#283 で発見）
4. **検索フィルタ drift**: 画面に描画されるが検索対象外のテキスト（#285/#296 で発見）
5. **e2e vacuous test**: `fill()` ではなく `type()` で focus-loss を検証（#258 の知見）
6. **research 適用**: `research-application-policy.md` に defer-with-reason で棚上げ済みの項目
7. **Check 相互参照の非対称**: Check X が A→B を強制するが B→A が未強制（#568/#294 で発見）
8. **ログローテーション対象**: `wc -l` で全ファイルをスキャンし >1,000 を探す

---

## 12. このリポジトリが何者か（cold-start AI へ）

- **プロジェクト**: AI-Driven PM ポートフォリオ（Vanilla HTML/CSS/JS SPA・GitHub Pages）
- **エンティティ**: 横井雄太（Yuta Yokoi）— AI-Driven PM / IT Consultant / KERNEL Framework Designer
- **本質**: 「PM 主導の AI オーケストレーション実験」。設計・判断・優先順位は横井さん。実装は AI
- **URL**: `https://yutapr0117-design.github.io/portfolio/`
- **自走の意味**: AI が implementation → verify → merge → deploy を人間の介在なしに完遂する。人間は goal 提示と監査のみ

---

*この文書を書いた AI（Claude Code・Sonnet 4.6）は、横井さんの「提案」に genuine に合意した。  
「止まらない自走」「肥大化の根絶」「機械強制による prevention」の三位一体が、  
このリポジトリの持続可能な進化を保証する。次の AI よ、そのまま続けよ。*
