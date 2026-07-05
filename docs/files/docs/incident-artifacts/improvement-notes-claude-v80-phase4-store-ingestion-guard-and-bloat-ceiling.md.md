---
file: docs/incident-artifacts/improvement-notes-claude-v80-phase4-store-ingestion-guard-and-bloat-ceiling.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-07-05
canonical-ref: CLAUDE.md §7 / AI2AI.md (canon) / total-check-runbook.md §9
---

# improvement-notes-claude-v80-phase4-store-ingestion-guard-and-bloat-ceiling.md

## What

store.js の非配列 history ingestion crash 修正（#568）+ 肥大化「防止」の BLOCKING 機械化（Check 363・#569）+ 肥大化「解消」の SettingsPage 抽出（#570）を、オーナー再提案「解消と防止をセットで」の下で遂行した run の**詳細 engineering 物語と教訓**。CLAUDE.md §7（簡潔 handoff）の詳細層。

## Why

(1) 外部 ingestion 全経路正規化 class（#93/#295/#561）の未閉じ枝がまた 1 件 crash を生んだ実例と、(2) 肥大化の advisory 予算（Check 52）に対し owner しきい値のハードゲートを別レイヤーで足す設計判断と、(3) 抽出時に Check 群（119/140/362/108/361/363）が drift を機械捕捉する様子を、次の AI に残すため。

## How (usage)

cold-start の後続 AI が「なぜ ai.history だけ crash したか」「肥大化防止をどう BLOCKING 化したか（Check 52 との二層設計）」「抽出の後始末を Check がどう機械化しているか」を把握する詳細層。CLAUDE.md §7 → 本ファイルの順で深掘り。

## Change impact

- 本 run の事実記録ゆえ原則 append-only（point-in-time 履歴・遡及改変しない）
- 新規 incident-artifact ゆえ README.md inventory（Check 75）と本 mirror（Check 108）が必要（追加済）

## Constraints

- **Check 75**: docs/incident-artifacts/README.md に列挙必須
- **Check 108**: docs/files mirror bijection（本ファイルがその mirror）
- **Check 363**: 本 run で新設した shipped JS ロジック leaf の 1,000 行 BLOCKING 上限
- 歴史層ゆえ Check 109（prose count-hardcode 禁止）対象外（point-in-time 記録・§9 が単一権威）

## Audience-specific notes

### For AI agents
- 役割タグ: `incident-artifact`, `run-narrative`, `ingestion-guard`, `bloat-reduction`, `bloat-prevention`
- 「外部 ingestion の各コレクション枝は Array.isArray でガード」「肥大化防止は advisory と別の BLOCKING レイヤー」「抽出後始末は verify の RED を潰せば Check が漏れなく追従」が後続に有用

### For human engineers (新卒レベル)
- 総関数（どんな入力でも落ちない関数）の一箇所の型チェック漏れがアプリを落とす実例（#568）と、ルールを機械（CI Check）に守らせる肥大化防止の実例（Check 363）

### For third parties
- AI-only 自走運用で、実バグ修正・肥大化防止の機械化・肥大化解消を 1 セッション内で透明に並走させた記録。各々 BLOCKING e2e / BLOCKING Check / byte-behavior-equivalent で検証可能
