---
file: STATUS.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-21
canonical-ref: .github/scripts/generate_status.py (generator) / Check 121
---

# STATUS.md

## What

オーナー向けの **機械生成** リポジトリ現況 BLUF（root の `STATUS.md`）。スマホ（GitHub mobile）から一目で「今このリポジトリはどんな状態か」を把握できる短いカード。`.github/scripts/generate_status.py` が authoritative ソースから生成し、`npm run status` で再生成する。

## Why

オーナー（横井雄太）は AI-only 自走実験としてこのリポジトリを運用し、設計上コードを読まず「非破壊 ∧ CI オールグリーン」ゲートを信頼している。その結果「オーナーが自分の repo の状態を一目で見る手段が無い」という gap が生じた。STATUS.md はそれを埋める。hand-maintain だと drift（stale な dashboard = 誤情報 = onboarding 税）するため、**全文機械生成 + Check 121 の regenerate-compare で鮮度を機械強制**する（AIO digest と同思想）。

## How (usage)

```
npm run status            # generate_status.py が STATUS.md を再生成
  └─ build_status() が AI2AI.md から Pipeline-Version / 最新 Session Record # 等を読む
  └─ 高頻度の数値 (Check 数・bytes) は埋め込まず §9 等へポインタ (低 churn 設計)
Check 121                 # generator を import し build_status() と byte 一致を検証 (stale なら fail)
```

## Change impact

- 埋め込み値（version / 最新 Session #）が変わったら `npm run status` で再生成し同コミットで commit（Check 121 が強制）
- generator のフォーマット変更 → STATUS.md も再生成して同期

## Constraints

- **手で編集しない**（全文機械生成。手編集は Check 121 で fail）
- **Check 121**: regenerate-compare で鮮度を BLOCKING 強制
- **Check 108**: 全 tracked file の docs/files mirror bijection（本ファイルがその mirror）

## Audience-specific notes

### For AI agents
- 役割タグ: `generated-artifact`, `owner-dashboard`, `bluf`
- 現況の live な真値は埋め込まず authoritative homes（runbook §9 等）へポインタする低 churn 設計

### For human engineers (新卒レベル)
- 「機械生成される現況サマリ」。直接編集せず generator を直す

### For third parties
- AI-only 自走リポジトリにおける「オーナー可視性」を drift なく保つ machine-generated dashboard の実装例
