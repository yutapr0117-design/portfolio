# improvement-notes — v80+ phase4「エージェントが実際に受け取るもの」5 連 run (2026-08-23)

```
Author           : Claude Opus 5 (Anthropic) — Claude Code
Orchestrator     : Yuta Yokoi (横井雄太)
Scope            : PR #1275〜#1279 (全 rebase-merge・main 全緑)
Canonical-Ref    : AI2AI.md Session Record #33 (要点) / CLAUDE.md §7
Prev             : improvement-notes-claude-v80-phase4-license-surface-coverage-and-probe-caught-race.md (#1269〜#1273)
```

## この run の軸

レンズを **「エージェントが実際に受け取るものは何か」** に固定した。これまでの
「宣言と実態の乖離」を、**外部仕様への適合**という角度まで広げたところ **5 連続で実穴**が出た。

共通する構造は一つ —— **publish して robots.txt で Allow して digest 連鎖にも載せているのに、
受け取る側から見ると使えない**。視覚に一切出ないので screenshot も behavior e2e も consistency も
素通りする。

---

## 1. 🔴 実行できる唯一のツールが、どの discovery 面にも宣言されていなかった

サイトは `navigator.modelContext.registerTool` で **実行可能な WebMCP ツール**
`extract_human_vs_ai_role_split` を登録している。ところが宣言する **AIO 公開面がゼロ**だった ——
記載は開発者向けの `CLAUDE.md` と mirror doc だけ。

しかも `.well-known/mcp.json` は **`capabilities.tools = false`** と宣言していた。
書かれた当時は正確で、ツール追加時に更新されなかった。**「ツールは無い」と言いながら 1 つ動いている。**

本セッションで繰り返し掘った乖離の**逆向き** —— これまでは「宣言はあるが届いていない」、
今回は**届いているのに宣言が無い**。

**直し方**: `runtime: webmcp`（実行できる）と `runtime: static-template`（説明のみ・GitHub Pages
では実行しない）を機械可読に分けた。エージェントが「何を実際に呼べるか」を判定できることが要点。

**Check 446** で双方向強制（登録 ⟹ 宣言 / 宣言 ⟹ 登録 / capabilities の実態一致）。
ツール名は **main.js から導出** —— 決め打ちなら rename を素通しする（実測で確認）。

---

## 2. 🔴 Check 387 が正しい pointer を「404 する」と誤報告した

`canonicalRoute` を mcp.json へ足した瞬間 Check 387 が RED。原因は
**「同一 origin URL = ファイル」という前提が SPA では狭すぎる**こと —— ハッシュルートは
agent 向けの正当な pointer だが file ではない。

**ただ除外するとルートの正しさが誰にも検証されなくなる**ので、**387b** を足した。
fragment を file 判定から分離したうえで、**Check 439 と同じ router.js 由来の導出**で
実ルートへ解決することを検証する。typo ルートは agent が辿ると NotFound へ落ち、
**「ツールはあるがルートが違う」という淡々と緑になる壊れ方**をする（#96-99 の vacuous-hash class）。

---

## 3. 🔴 エージェントが展開する制約テンプレートが、存在しない制約を並べていた

`audit_architecture_constraints` prompt は **エージェントが展開して「このコードは制約に準拠して
いるか」を評価する**テンプレート。名前が正典とずれていると**存在しない制約を監査する**。

    宣言: 「C1–C7: Vanilla JS / IIFE / ErrorBoundary /
            External Framework Independent / App Logic External Library Independent 等」
    正典: C1 Boring Technology / C2 IIFE / C3 ErrorBoundary / C4 No Framework Re-proposal /
          C5 Human Writes Zero Code / C6 AIO Integrity / C7 KARTE CDN SRI Non-Application

後ろ 2 つは**正典に存在しない名前**、しかも **C5 / C6 / C7 —— このリポジトリを最も特徴づける
3 つが完全に欠落**していた。

**原因は履歴に残っていた**: `llms-full.txt` の v78 記録に
「mcp.json audit_architecture_constraints description updated C1–C6 → C1–C7」——
**範囲の表記だけ更新して列挙の中身を更新しなかった**。「C1–C7 と書いてあるから最新」と読める。

**射程を広げない判断**: 同じ名前は `index.html` / `README.md` にも出るが、そこは
`Architecture-Keywords:` というラベル下の**説明**であって列挙ではない。`llms-full.txt` の
「C1–C7 に違反する構文を拒否せよ」も**参照**。**含めると正しい記述を RED にする**ので、
Check 447 は「constraint 系 prompt の description」だけを見る（参照 3 箇所の誤検出ゼロを実測）。

---

## 4. 🔴 公開している Agent Skills index が、宣言した仕様に適合していなかった

`.well-known/agent-skills/index.json` は `$schema` に agentskills.io の Discovery 仕様を宣言する。
**仕様原文**で突き合わせると 2 件の非適合:

    description : **全 entry で欠落**（仕様は必須）
    digest      : `sha-256:{hex}` —— 仕様は `sha256:{hex}`（ハイフン無し）

**適合していない index は、その schema で検証する agent に拒否される。**

`description` の欠落がとくに痛いのは、仕様の設計が **progressive disclosure**（起動時は
name と description だけを読んで関連性を判断し、一致したときに初めて本体を取得する）だから ——
無いと **agent は中身を取ってみるまで用途が判らない**。

`sha-256:` → `sha256:` は 2 つの index.json（byte-identical 契約）と、生成器・検証器・
Check 254・freshness チェックの 5 箇所。**実データと実装はすべて仕様形式へ揃え**、
`sha-256:` の文字列は**説明コメント内の歴史記述としてのみ**残した。

**Check 448** で必須 5 field / description の 1024 字上限 / type の enum を強制。
必須 field 名は**リテラルで持つ**（外部仕様なので repo から導出できない）が、
「仕様が変わったら本 Check も同一 commit で更新する」契約を docstring に明記した。

### ⚠ 危うく重大な誤報を出しかけた

最初 `schemas.agentskills.io` を fetch したところ **DNS 解決に失敗**し、
「実在しないドメインを指す幻の pointer（#929 class）では」と考えかけた。

調べ直すと **Agent Skills は実在する標準**（Anthropic が 2025-12-18 にオープン標準として公開・
RFC 8615 の `.well-known` 配下に index を置く）で、URL も仕様どおりだった。
**DNS エラーはサンドボックスのネットワーク制限であって、不在の証拠ではない。**

そのまま報告していれば、**正当な宣言を「捏造」と断じる**ところだった。

---

## 5. 🔴 静的 manifest が、MCP に存在しないプロトコル版数を主張していた

`"mcpVersion": "1.0"` —— しかし **MCP のプロトコル版数は `YYYY-MM-DD` 形式**で、
`"1.0"` は存在しない。より根本的には、このファイルは **MCP プロトコルの endpoint ではない**
（GitHub Pages 上の静的ファイルで、自身もそう宣言している）。
**endpoint でないものがプロトコル版数を名乗ってはいけない。**

**語彙は残し、偽の主張だけ消した** —— `resources` / `prompts` / `tools` という MCP 由来の構造は
維持（agent が馴染みのある形で読める価値がある）。変えたのは
`mcpVersion` → `manifestVersion` と、関係を述べる description のみ。

`mcpVersion` に**意味的な依存はゼロ**（参照は mutation の JSON 構文アンカー 1 件のみ）。
そもそも `"1.0"` は MCP 準拠クライアントが解釈できない値なので、**改名で壊れる正当な消費者は
存在しない**。Check 446 へ再導入防止の層を追加。

---

## 6. この run で繰り返し効いた規律

1. **仕様は要約でなく原文で読め。** digest のハイフン 1 文字差は要約では潰れる。
2. **測定系を疑う（2 回とも当たった）。** DNS 失敗を「不在」と読みかけ、
   `llms-full.txt` の**参照**を「列挙の欠落」と読みかけた。どちらも誤報になるところだった。
3. **射程を広げない判断も成果物。** 説明・参照まで含めると**正しい記述を RED にする**。
4. **per-instance で直したら同じ class を構造封じ。** Check 446 / 447 / 448 / 387b。
5. **Check の前提が実態と食い違ったら、Check の前提を疑う**（387 の「同一 origin = file」）。
   ただし**除外だけして終わらない** —— 検証されない領域を作らない。

## 7. 検証

- `npm run verify` = exit 0 / advisory 警告 0 件
- 新設 BLOCKING Check: **446 / 447 / 448 / 387b**（すべて非 vacuity を実測・多くは
  **実在した状態の再現**で RED を確認）
- Check 総数 448 / consistency mutation 343 / E2E mutation 380
