# decision-v80-phase3-deep-specialized-audit.md

```
Decision-Date : 2026-06-16
Session       : continuous-improvement run (PR #73〜). 非 digest 層 (incident artifact) に閉じる。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)。指示: 「深い専門監査を
                継続前提・選択肢不要・AI 優先順位付けで全て自走」。
Track         : v80+ staged major update (Phase 3 — deep specialized audit / coverage map + §3B verify)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : docs/architecture/research-application-policy.md §3B / CLAUDE.md §7
Status        : Audit pass complete (4 genuine fixes applied + clean dimensions verified)
```

> **Canonical hierarchy:** `AI2AI.md` canonical / `llms-full.txt` ground truth. 従属 incident artifact。

---

## 1. 目的：深い専門監査の coverage を記録し再監査浪費を防ぐ

オーナーの「深い専門監査を継続」指示を受け、リポジトリの安全性の根幹（「Check が実際に drift
を捕捉するか」「docs が実物を正しく記述するか」「実コードが堅牢か」）を次元ごとに監査した。
本記録は **どの次元を監査し、何を fix し、何を clean と検証したか** の coverage map であり、
次セッションが同じ監査を重複実行しないための §3B verify-result である。

## 2. 監査次元と結果

| 監査次元 | 方法 | 結果 |
|---|---|---|
| **Vacuous-gate**（対象集合が空でも `not <list>`/対称差 0 で pass する false-confidence） | 全 `check()` 条件を静的抽出し非空ガードの有無を点検 | **genuine 1件: Check 39**（gutted sitemap が「all 0 URLs resolve」で vacuous pass）→ `_sm_checked > 0` ガード追加 (#86)。同クラスの **57/58/59** に非空ガードを一貫追加。Check 33/37/38/42a/42b は「空=clean が正/ハードコード非空」で安全と確認 |
| **Mirror file-coherence**（`file:` frontmatter が指す先の正しさ） | 143 mirror の `file:` == 派生パスを照合 | 現状全一致。copy-paste drift を防ぐ機械強制を **Check 97 に追加** (#87) |
| **Mirror date honest-dating**（`last-updated:` の ISO 形式） | 143 mirror の `last-updated:` 形式を照合 | 現状全 ISO。**Check 65 の scope を mirror 全面へ拡張** (#88) |
| **Mirror content-accuracy**（mirror が実ソースの挙動を正しく記述するか） | 高 behavioral-complexity な shipped 系 mirror を実ソースと突合 | **genuine 1件: sw.js.md**（「asset precache する cache-first PWA」と誤記 / 実体は llms*.txt のみ傍受する AIO 正規化 SW）→ 全面是正 (#89)。main.js.md / e2e / theme-init / error-suppressor / aio-guard / karte-init mirror は**正確と確認** |
| **Python script robustness**（bare except / 宙吊り promise 相当） | `.github/scripts/*.py` の except 用法を点検 | clean。唯一の `except Exception`（aio_monitoring.py）は error-body 読取失敗時の graceful fallback で適切。**変更不要** |
| **Shipped JS promise handling**（未処理 rejection） | leaf module の fetch/.then/async を点検 | **genuine 1件: sw.js SWR の宙吊り networkFetch**（オフライン時 unhandledrejection）→ `.catch` 追加 (#84)。ui-components の `audio.play()` / router / pure-utils は try/catch 済で安全 |
| **高 stakes regex 精度**（canary/CSP/version の false-pass） | 主要 regex の anchor/format を点検 | canary `\d{4}-[0-9A-F]{8}` 等は厳密。CSP hash は live 内容から再計算でロバスト。**変更不要** |

## 3. 結論

- 深い監査で **genuine な gap 4 件**（Check 39 vacuous-gate / Check 97 file-coherence の欠如 /
  Check 65 mirror date scope の欠如 / sw.js.md 内容誤記）を発見し全て fix。さらに sw.js promise
  gap (#84) もこの監査文脈で fix 済。
- **複数次元を clean と検証**（python / 大半の mirror 内容 / 高 stakes regex / set-equality の
  authoritative 集合非空性）。これらは re-audit 不要。
- リポジトリは安全機構・docs 整合・実コード堅牢性のいずれも極めて健全。今後の deep audit は
  「新規追加された Check/mirror/コードに対する同次元の再点検」を増分的に行えば足り、既監査
  次元の全面再走査は不要。

## 4. 次の一手

「No terminal "done" state」(Check 102d) に従い継続。新規に追加される mirror/Check/コードへの
同次元監査、および未だ深掘りしていない角度（例: cross-document の数値整合の網羅性、e2e の未
カバー対話機能）を AI 優先順位付けで genuine な範囲で進める。padding は引き続き禁止。
