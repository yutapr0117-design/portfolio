---
file: .github/scripts/checks_license_draft.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-26
canonical-ref: .github/scripts/check_repository_consistency.py (集約器) / LICENSES/ACD-1.2-DRAFT.txt (検査対象) / docs/architecture/check-repository-consistency-map.md (全 Check の一覧)
---

# .github/scripts/checks_license_draft.py

## What

**次版の草案 `LICENSES/ACD-1.2-DRAFT.txt` だけを検査する consistency Check module。**
Check **468**（草案が NOT IN FORCE / NOT SUBMITTED / NOT APPLIED を述べること・純 ASCII・節の連番・
参照の解決・申告語数と条数の一致・ヘッダの箇条書き・descriptor の記述ほか）を持つ。

## Why

`checks_license_submission.py` が 801 行になり Check 52 の advisory (800) を越えた（2026-09-24）。
**予算を上げず、テーマで分けた。** あちらは**審査者がいま受け取る面**を守り、壊れたときの損害は
「審査者が誤った物を読む」。こちらは**まだ誰にも渡していない草案**を守り、損害は
「確定の日に、誤った状態の草案から版を切る」。

## How

- 集約器の `CHECK_SOURCE_FILES` に登録し `_checks_license_draft.run(_ctx)` で呼ぶ（Check 431 が実在 ⟺ 登録 ⟺ 実行を強制）
- `run(ctx)` は `ROOT` と `check` だけを bind する。**移動は逐語**で、条文ロジックは 1 バイトも変えていない
  （移動元が module 先頭で import していた `json` を持ってくるのを忘れ、468 が「descriptor を JSON として読めない
  (NameError)」と**誤った理由で**RED になったのを実行して捕まえた）

## Constraints

- `# ── N.` と docstring inventory の bijection は Check 45 が強制する
- 番号 468 は動かさない（他文書が番号で参照している）

## Change impact

草案の性質を検査する Check を足すときはここへ。800 行を越えたら、また圧縮ではなくテーマで割る。

## Audience-specific notes

- **後任 AI**: 草案を確定して新しい版を切るとき、この module の対象 path も新しい草案へ向け直すこと

## 2026-09-26: 草案が無いときの挙動

以前は `if ACD-1.2-DRAFT.txt exists` の中に全体があり else が無く、**草案が無いと 468 は OK も ERROR も出さずに消えていた**。版を確定して DRAFT を改名した日に、次版の検査が黙って止まる形である（`ACD-1.1-CHANGELIST.md` §0.13 は RED になると書いていた）。else で明示的に RED にし、mutation（草案 path を存在しない名前にずらす）を登録した。
