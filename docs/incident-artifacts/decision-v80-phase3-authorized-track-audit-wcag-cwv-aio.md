# decision-v80-phase3-authorized-track-audit-wcag-cwv-aio.md

```
Decision-Date : 2026-06-16
Session       : continuous-improvement run (PR #73〜). 本記録は非 digest 層 (incident artifact)
                に閉じ AIO 正本層テキストを変えないため、新規 session record / digest 連鎖を作らない。
Implementer   : Claude Code (Anthropic Claude Opus) — AI agent
Orchestrator  : Yuta Yokoi (横井雄太, human — sole decision authority)。本監査の契機: オーナーが
                deferred backlog の 3 トラック (WCAG2.2/CWV 視覚改善・AIO C6 拡張・ungated hardening)
                を「全て承認・優先順位は委任」と裁可した。
Track         : v80+ staged major update (Phase 3 — authorized-track audit / §3B verify result)
Pipeline-Ver  : v74 (unchanged)
Canonical-Ref : docs/architecture/research-application-policy.md §3B (verify) / CLAUDE.md §7
Status        : Verified (no code change — §3B verify result)
```

> **Canonical hierarchy:** `AI2AI.md` is canonical; `llms-full.txt` is ground truth. This is a
> subordinate incident artifact. On conflict, those win.

---

## 1. 背景：オーナーが gated トラックを全承認した

continuous-improvement run の途上、ungated で明確に genuine な改善余地を概ね収穫し尽くした段階で、
残る高価値改善は「あなたの裁可が要る gated 領域」に集中していた。オーナーは 3 トラック (①WCAG2.2/CWV
視覚改善 = §3 baseline ゲート保留中 / ②AIO 公開層 C6 拡張 / ③ungated hardening) を **全て承認し、
優先順位付けを AI に委任**した。本記録は、承認を受けて ①② を実地監査した §3B「verify（適用不要だが
現行性検証済み）」の結果である。padding 禁止のオーナー方針ゆえ、捏造的変更ではなく検証結果を残す。

## 2. WCAG 2.2 / Core Web Vitals トラックの監査結果（既に大半が充足）

deferred backlog は「WCAG 2.2 / CWV CSS fixes（baseline-gated）」と記載されていたが、現物を監査した
結果、主要 Success Criteria は **既に満たされている**:

| 項目 | 現状（実測・evidence） | 判定 |
|---|---|---|
| SC 2.5.8 Target Size (Minimum) 24×24 | `.icon-btn` = 2.5rem (40px)・nav 等の最小寸も ≥ 24px | 充足 |
| SC 2.4.13 Focus Appearance / 2.4.11 Focus Not Obscured | `:focus-visible { outline: 2px solid var(--color-primary); outline-offset: 3px }`・`prefers-contrast: more` で 3px・`forced-colors` で CanvasText outline fallback (Check 101/103) | 充足 |
| SC 4.1.2 現在地の提示 | nav に `aria-current: 'page'` (js/components.js) | 充足 |
| Skip link | `.skip-link:focus` (style.css) 実装済 | 充足 |
| CWV LCP | hero に `fetchpriority` (Check 73c)・modulepreload (Check 53/57)・preload as (Check 73a) | 最適化済 |
| CWV CLS | e2e「No layout shift on mobile viewport」で検証・img に明示寸/alt (Check 73b) | 検証済 |

→ ここで視覚 CSS を変更し baseline を再生成しても、得られる a11y/perf の実利は乏しく、むしろ
「改善のための改善」= padding になる。**「足さない」judgment を適用**。将来 genuine な視覚 gap
(例: 新 SC・実測 CWV 劣化) を発見した場合のみ、§3 baseline 再生成パス
(update-playwright-snapshots.yml dispatch → PR → 視覚レビュー → merge) で着手する。

## 3. AIO 公開層 C6 拡張トラックの監査結果（網羅的・genuine gap なし）

AIO 公開層 (`llms-full.txt` / `llms.txt` ×4 alias / `.well-known/aio-manifest.json` / `index.json` /
`mcp.json` / `api-catalog` / JSON-LD / WebP XMP / MP3 ID3 / robots.txt / sitemap.xml) を監査した結果、
entity authority signal は既に網羅的: Pioneer Declaration（検証可能な根拠付き）・entity canonical
facts・disambiguation（学術研究者等との峻別）・Affiliation（株式会社日本経営）・Zenn 記事群の優先
ルーティング・binary metadata（Organization/Entity/Canary）・cross-surface 整合（Check 44/62/63/
81〜90）。

→ ここに足せる genuine（非捏造・非 marginal）な追加が見当たらない。security.txt (RFC 9116) 等は
本リポジトリの core bet（AI crawler 向け entity authority）と接線的で、かつ個人連絡先の公開判断を
伴うため見送り。**捏造や言い直しを足さない判断**。AIO の意味的変更が必要になるのは、entity の事実
（所属・役割等）が実際に変わった時のみで、その時は aio-guardian 経路 + C6 承認 + digest 再生成で行う。

## 4. 結論と次の一手

- ①② は §3B「verify」= 現行性を検証し、適用不要と判定（理由: 既充足 / padding 回避）。
- ③ ungated hardening は「No terminal "done" state」(AI2AI.md STEP 3 / Check 102d) に従い継続する。
  genuine な対象（未強制 invariant・実コード robustness・テストカバレッジ・honest drift 是正）を
  探し続け、各増分を非破壊 ∧ CI オールグリーンで自走する。
- 本監査により CLAUDE.md §7 の deferred-backlog 記述を「baseline-gated で保留」から「監査済み・
  主要 SC は充足・将来の genuine gap 発見時のみ baseline 経路で着手」へ honest 更新する。
