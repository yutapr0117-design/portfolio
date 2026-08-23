---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-license-surface-coverage-and-probe-caught-race.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: AI2AI.md / CLAUDE.md / docs/files/playwright.config.cjs.md / LICENSES/ACD-1.0.txt
---

# improvement-notes — license surface coverage and probe-caught race

## What

2026-08-23 の run（PR #1269〜#1273）の増分記録。軸は **「走査対象に入らないものは検査されない」
class を 3 段掘り下げた**こと。

1. JSON-LD の **CreativeWork 10 ノードが無宣言**（binary の XMP/ID3 は ACD-1.0 と言うのに JSON-LD は無言）
2. 主要 WebPage ノードが**全ルートで 2 つの名前を主張**（同一 @id の property merge）
3. **Article ノードだけ license 無し** —— 静的 Check にも e2e のルート一覧にも入らない両方の死角
4. **週次 probe が私自身のテストの race を捕捉**（手動 RED / probe SURVIVED の環境依存）

## Why

commit には what/why を厚く書くが、**run 全体を貫く軸**と**再利用できる教訓**は散らばると
次の AI が拾えない。AI2AI.md の Session Record を薄く保つ（Check 365 の 1,000 行制約）ため、
要点は Session Record・詳細は本 doc という二層にしている。

## How (usage)

cold-start では `CLAUDE.md` §7 → `AI2AI.md` Session Record #32 → 本 doc の順に降りる。
e2e の書き方で迷ったら §4 と `docs/files/playwright.config.cjs.md` の落とし穴表を読む。

## Constraints

- **Check 75**: `docs/incident-artifacts/README.md` の inventory に列挙されていること
- **Check 108**: 本 mirror doc が存在すること
- **Check 436 の対象外**: `docs/incident-artifacts/` は性質上の歴史記録

## Change impact

- 本 doc は**歴史記録**なので、後から実態が変わっても書き換えない。訂正は新しい run の notes で
  「この記述は後に反証された」と述べる（#977 / #1245 と同じ扱い）。

## Audience-specific notes

### For AI agents
- 役割タグ: `improvement-notes`, `json-ld`, `route-coverage`, `mutation-probe`, `test-race`
- 再利用できる教訓は §6 に集約。とくに **「非 vacuity は probe が実際に使う条件で測れ」** は
  #1073 で記録済みなのに再発させたので、次も同じ誤りを避けること。

### For human engineers (新卒レベル)
- 「テストが通っている」と「テストが検査している」は別。走査対象に入らないものは、
  どれだけ厳しい assertion を書いても素通りする。

### For third parties
- AI 実装が**自分のテストの race を安全網に指摘されて直す**過程の記録。
