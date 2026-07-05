---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: CLAUDE.md §7 / AI2AI.md (canon) / total-check-runbook.md §9 / decision-v80-phase4-bloat-reduction-1000-line-threshold.md
---

# improvement-notes-claude-v80-phase4-checkpy-split-track-full-handoff.md

## What

`check_repository_consistency.py` 分割トラック（owner 合意 C-first・sustained multi-session）の**完全引き継ぎ書**。Phase 1-5 完遂（monolith 15,913→15,066・2 module 確立）時点の全知見を、次担当 AI が cold-start で 1 手も損なわず継続できるよう余さず集約した一次ハンドオフ層。CLAUDE.md §7（簡潔 handoff）の詳細層。

## Why

check.py 分割は「合意の経緯・#253 net-negative を覆した核心（ctx 注入）・確立した 6 ステップ分割パターン・coupling 判別法・Phase 6+ の 2 難度 class（coupled-group / global-content）・本セッションの事故と復旧・厳守事項」という**膨大な暗黙知**を持ち、CLAUDE.md §7 の 1 エントリでは表現しきれない。次の AI が同じ轍を踏まず（§8 の事故 class）、正しいパターンで即継続できるよう、全てを明示化して残すため。

## How (usage)

cold-start の後続 AI が check.py 分割トラックを継続する際の**唯一の完全参照**。読む順は本文 §12（cold-start 復帰手順）に従う: CLAUDE.md §7 → 本ファイル → runbook §9 → decision record Addendum → check-map §0/§4 → 関連 memory。Phase 6 の抽出ターゲット選定は §4、6 ステップ手順は §2.2。

## Change impact

- 本 run 群の事実記録 + 未来トラックのガイドゆえ、事実部は append-only（point-in-time 履歴）、ガイド部（§4-7 の次の手）は次担当が進捗に応じて更新可
- 新規 incident-artifact ゆえ README.md inventory（Check 75）と本 mirror（Check 108）が必要（追加済）

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須
- **Check 108**: docs/files mirror bijection（本ファイルがその mirror）
- 歴史 + ガイド層ゆえ Check 109（prose count-hardcode 禁止）対象外（Check 総数の単一権威は runbook §9）

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `incident-artifact`, `handoff`, `check-split`, `ctx-injection`, `bloat-reduction`, `multi-session-track`
- **本ファイルが check.py 分割トラックの唯一の完全引き継ぎ**。§2.2（6 ステップ分割パターン）・§4（Phase 6+ の 2 難度 class と次の手）・§8（事故と復旧）・§10（厳守事項）・§12（cold-start 復帰手順）を必読。「収束と感じても停止しない」（§10-8）。

### For human engineers（新卒レベル）
- 巨大な 1 ファイル（15,913 行）を挙動を変えずに小ファイルへ分ける多段プロジェクトの、全工程・全落とし穴・次の一歩を書いた設計ノート。過去に「割に合わない」と判断された作業を、別手法で「割に合う」に覆した透明な記録。

### For third parties / auditors
- AI-only 無限自走運用における sustained multi-session リファクタリングの引き継ぎ規律の実例。合意の経緯・byte-equivalent 証明・安全網（consistency check NameError）による coupling 判別・force-push 不使用の事故復旧まで、第三者が検証可能な形で記録。
