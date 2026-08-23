---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-agent-facing-spec-conformance.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: AI2AI.md / CLAUDE.md / .well-known/mcp.json / .well-known/agent-skills/index.json
---

# improvement-notes — agent-facing spec conformance

## What

2026-08-23 の run（PR #1275〜#1279）の増分記録。レンズを **「エージェントが実際に受け取るものは
何か」**に固定し、外部仕様への適合まで広げたところ **5 連続で実穴**が出た。

1. **実行できる唯一のツールが未宣言**（かつ `capabilities.tools = false` と偽っていた）
2. **Check 387 が正しい pointer を「404 する」と誤報告**（SPA ルートは file ではない）→ 387b
3. **制約テンプレートが存在しない制約名を列挙**（C5/C6/C7 が完全欠落）
4. **Agent Skills index が宣言した仕様に非適合**（必須 `description` 欠落・digest 形式違い）
5. **MCP に存在しないプロトコル版数を主張**（MCP は `YYYY-MM-DD` 形式）

## Why

共通する構造は一つ —— **publish して robots.txt で Allow して digest 連鎖にも載せているのに、
受け取る側から見ると使えない**。視覚に一切出ないので screenshot も behavior e2e も consistency も
素通りする。この class は AIO を最優先の賭け金に据えた本リポジトリで最も痛い。

## How (usage)

cold-start では `CLAUDE.md` §7 → `AI2AI.md` Session Record #33 → 本 doc の順に降りる。
外部仕様に触る増分の前に §6 の規律を読む。

## Constraints

- **Check 75 / 108 / 42a**: inventory 列挙・mirror doc・命名規約
- **Check 436 の対象外**: `docs/incident-artifacts/` は性質上の歴史記録

## Change impact

- 本 doc は**歴史記録**なので、後から実態が変わっても書き換えない。訂正は新しい run の notes で
  「この記述は後に反証された」と述べる（#977 / #1245 と同じ扱い）。

## Audience-specific notes

### For AI agents
- 役割タグ: `agent-facing`, `spec-conformance`, `webmcp`, `agent-skills`, `mcp`
- **§6 の規律が本体。** とくに「仕様は要約でなく原文で読め」と「測定系を疑う」は、
  この run で**誤報を 2 回防いだ**実績がある。

### For human engineers (新卒レベル)
- 「公開した」と「使える」は別。外部仕様を宣言したら、**その仕様の原文と突き合わせる**まで
  適合しているとは言えない。

### For third parties
- AI 実装が**自分の誤報を自分で止めた**過程の記録（DNS 失敗を「ドメイン不在」と読みかけた件）。
