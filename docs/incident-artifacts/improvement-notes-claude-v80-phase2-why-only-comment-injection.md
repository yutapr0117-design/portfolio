# improvement-notes-claude-v80-phase2-why-only-comment-injection

```
Last-Updated  : 2026-06-14
Maintained-By : AI agents under Yuta Yokoi (横井雄太) orchestration
Type          : Increment record (why-only comment-injection / handoff §10 の実行)
Incoming-From : improvement-notes-claude-v80-phase2-session-handoff-comment-injection.md §10
AI-this-time  : Claude Code (Anthropic Claude Opus)
Canonical-Ref : AI2AI.md (canon) / CLAUDE.md (router) / llms-full.txt (ground truth)
```

> session-handoff §10「全ファイル (§5.3) に why-only コメントを段階的に注入する」を実行した
> increment の記録。**最重要の発見を honest に残す**: shipped JS/HTML レイヤーは前任セッションの
> 作業で**既に高密度の WHY コメントを完備**しており、盲目的な全 Stage 走査は §5.2「drift 製造機」と
> CLAUDE.md「不要なコメントを書くな」に反する。よって genuine gap だけを埋め、過程で発見した
> 未強制 invariant を Check 100 として systematize した。

---

## 1. このセッションで完遂したこと (3 commit + 1 新 Check)

| commit | 内容 |
|---|---|
| `docs(comments)` Stage A | main.js AIDK Kernel に「なぜ DO NOT EDIT/frozen か + Check 43a-d アンカー + 触ると何が壊れるか」を block 単位で注入。VT proxy / Trusted Types / 2 protected blocks (event listener registry・innerHTML sanitizer) を含む。**実行コード byte-unchanged (39 行すべてコメント追加)** |
| `feat(comments+check)` | theme-init.js (FOUC pre-paint の WHY + hidden key-duplication invariant) / karte-init.js (queue-stub + C7) に WHY 注入。**Check 100 (BLOCKING / 100a・100b) 新設** + 3 governance doc 同期 |
| `docs(comments)` Stage C | index.html CSP meta に各ディレクティブの WHY (Trusted Types↔Check 43c / 3 hash の正確な帰属 / 'unsafe-hashes'↔onload / karte hosts↔C7 / img-src 相対パス↔Check 73c) |
| `docs(increment)` | 本 improvement-notes + docs/files mirror + Check 96 list / incident README 同期 (bijection 139=139=139) |
| `docs(comments)` Stage E | playwright.config.cjs の baseline-gate magic number (threshold/maxDiffPixelRatio/reuseExistingServer) に WHY |
| `docs(handoff)` | CLAUDE.md §7 を Check 100 / N=100 / 本 increment bullet へ同期 (cold-start router 整合) |

## 2. 最重要の honest finding — 次セッションは盲目的に Stage B-E を走らせるな

session-handoff §5.4 は Stage A〜F を推奨したが、実際に main.js / js/*.js (24 葉) /
pure-utils.js / vendor (aio-guard / error-suppressor) / index.html を精査した結果:

- **js/*.js 24 葉モジュールは fileoverview docstring で factory pattern / closure-deps=none /
  Check 47c / byte-equivalent の WHY を既に完備**。関数本体レベルも WHY コメント済 (例:
  pure-utils.js の「fetch 特有の罠: HTTP エラーでも resolve される」)。
- **index.html は error-suppressor inline の WHY (なぜ inline か / timing race / byte-identity) /
  modulepreload / hero preload 相対パスの WHY を完備**。
- **aio-guard.js / error-suppressor.js は DESIGN/GUARD AGAINST の WHY docstring 完備**。

→ これらに追加コメントを注入すると **redundant = drift 製造**。CLAUDE.md「Default to writing
no comments. Only add one when the WHY is non-obvious」と矛盾する。**genuine gap だけ**を埋めるのが
正しい適用。本セッションが埋めた gap は (a) kernel の「なぜ DO NOT EDIT か」+ Check アンカー、
(b) theme-init.js の隠れたキー複製 invariant、(c) karte-init stub の存在理由、(d) CSP 現場の
ディレクトリ連動先 — の 4 点のみ。残りは既に完備。

## 3. discover → document → systematize の実践 (Check 100)

theme-init.js は main.js (ESM, async) ロード前に `<head>` で同期実行され FOUC を防ぐため、
localStorage キー `'portfolio_enhanced_v45'` / `'portfolio_brand_v45'` を **import せず意図的に
ハードコード複製**している。これは現状機械強制されていない drift risk だった (js/constants.js の
STORAGE_KEY や js/brand.js の KEY を変えても theme-init.js は黙って旧キーを読む → 初期ペイント
だけ壊れ、main.js ロード後は正しく動くため test でも気づきにくい silent first-paint drift)。

→ コメントで invariant を document し、**Check 100 (100a/100b) で BLOCKING 機械強制**。非vacuous
確認済 (キーを v46 に rename すると `getItem('...v46')` が theme-init.js に無く ERROR 発火)。

## 4. 環境メモ (次セッションが同マシンを使う場合)

このマシンには初期状態で **node 未インストール / system python3 = 3.9.6** (check スクリプトは
`str | None` = Python 3.10+ 要求)。`npm run verify` を完走させるため以下を導入した:
- `brew install node python@3.12` (node v26 / python 3.12)
- `pip install --break-system-packages pyyaml` (Check 23 の YAML 検証用)
- PATH: `/opt/homebrew/opt/python@3.12/libexec/bin:/opt/homebrew/bin:$PATH` で `python3`→3.12 解決

verify 実行: `export PATH="/opt/homebrew/opt/python@3.12/libexec/bin:/opt/homebrew/bin:$PATH"; npm run verify`

## 5. 状態 (本セッション完遂後)

| 項目 | 値 |
|---|---|
| Check 総数 | **100** (最大番号 100 / BLOCKING 96 + ADVISORY 4: Check 52 + 60) |
| 3 集合 bijection | git(excl docs/files) = _phase1_targets96 = docs/files/*.md = **139** (本ファイル + mirror 追加後) |
| npm run verify | exit 0 |
| 実行コード | main.js / index.html / vendor すべて挙動 byte-unchanged (コメントのみ) |

## 6. 次セッションへの申し送り (defer / 再 litigate 禁止)

- **Stage B-E の残り (js/scripts/workflows/config 等) はファイル単位で「既に WHY 完備か」を
  先に確認**してから注入判断せよ。既完備への追加は drift。
- session-handoff §5.5 の Check 101 (js factory docstring 強制 = Check 61 拡張) / Check 103
  (コメント比率 baseline) は **任意**。Check 101 は既存良コメントを lock-in する価値があるが、
  Check 103 (比率 baseline) は fragile なので慎重に。drift 防止になるものだけ採用。
- backlog (WCAG 2.2 / CWV CSS = baseline-gated、IETF AIPREF = 戦略上不採用) は不変。
