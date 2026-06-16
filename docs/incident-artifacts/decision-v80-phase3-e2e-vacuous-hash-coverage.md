# decision-v80-phase3-e2e-vacuous-hash-coverage.md

```
Decision-Date : 2026-06-16
Session       : continuous-improvement run (PR #73〜). 非 digest 層 (incident artifact)。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)
Track         : v80+ staged major update (Phase 3 — e2e vacuous-hash coverage 是正 + 教訓)
Fix-PRs       : #96 (ALL_ROUTES app hashes) / #97 (route-render NotFound guard) /
                #98 (HASH_ROUTES) / #99 (project-detail) / 関連: #93 (Settings bug)
Status        : Fixed + systematized
```

> **Canonical hierarchy:** `AI2AI.md` canonical / `llms-full.txt` ground truth. 従属 incident artifact。

---

## 1. 事象：複数の e2e テストが「実ページではなく NotFoundPage」を vacuous に検査していた

深い e2e 対話監査（apps の実操作テスト）中、`#/settings` の Storage 注入バグ (#93) を追ったのを
契機に「e2e の hash が実 route に解決しているか」を全 goto について実測したところ、**誤った
hash が NotFoundPage に解決し、それでもテストが pass している**ケースが複数見つかった:

| 箇所 | 誤 hash | 実 route | 結果 |
|---|---|---|---|
| ALL_ROUTES route-render | `#/app-task` `#/app-todo` `#/app-pomodoro` `#/app-ai` | `#/apps/<x>` | NotFound を 4 回 vacuous 検査 (#96) |
| HASH_ROUTES aria-busy | `#/home` `#/skills` | `#/`（home）/ 実在せず | NotFound を 2 回 vacuous 検査 (#98) |
| project-detail | `#/project/<slug>`（単数） | `#/projects/<slug>`（複数） | NotFound を vacuous 検査 (#99) |

合計 7 つの route テストが、実ページではなく NotFoundPage を検査していた。

## 2. なぜ vacuous でも pass したか（class の本質）

これらのテストの合否条件は「`#content` 非空 + console/page error 無し（+ aria-busy=false）」
だった。**NotFoundPage はこれらをすべて満たす**（正常に描画される有効なページであり、非空で
エラーも出さない）。したがって hash が NotFound に落ちても緑になり、テストは「何かが描画された」
ことしか保証していなかった。これは #93 の Settings バグ（ErrorBoundary 捕捉済み FatalPage が
同様に pass）と同根の「**graceful な代替ページ（NotFound / Fatal）がテストの弱い合否条件を
満たして vacuous に pass する**」class である。

Check 58 は e2e ALL_ROUTES の route NAME 集合と main.js switch case 集合の一致を見るが、
**hash が実際にその name へ解決するかは検査しない**ため、hash の誤りを検出できなかった。

## 3. 修正と systematize

- **fix (#96/#98/#99)**: 全 goto hash を実 route へ是正（`#/apps/<x>` / `#/` / `#/resume` /
  `#/projects/<slug>`）。是正後、各テストは実ページ（TaskPage / AIPage / Resume / ProjectDetail 等）を
  検査する。
- **systematize (#97/#98/#99)**: route-render ループ・HASH_ROUTES ループ・project-detail テストに
  「not-found-fallback 以外は NotFoundPage（h1『Not Found』）を描画していない」アサーションを追加。
  誤った hash を足しても vacuous に pass しない構造へ。
- **網羅確認**: spec 内の全 `goto('/#/...')` を実測し、全て実 route に解決することを確認。

## 4. 再発防止の指針

- e2e で「ページが描画された」ことだけを合否条件にしない。**そのページが意図した route で
  あること**（route 固有の marker の存在 / NotFound・Fatal でないこと）も併せてアサートする。
- graceful degradation（NotFound / ErrorBoundary FatalPage）は「正常に見える代替ページ」を出す
  ため、弱い合否条件のテストを vacuous に pass させやすい。代替ページの marker を negative
  assertion で除外するのが有効（本 increment で route-render/HASH_ROUTES/project-detail に追加済）。
- 新しい route テストを足すときは hash が実 route に解決することを実機で 1 度確認する。
