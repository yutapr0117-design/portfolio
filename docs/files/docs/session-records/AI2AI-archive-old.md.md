---
file: docs/session-records/AI2AI-archive-old.md
audience: ai, human (新卒), 監査人, 学術研究者, 第三者全般
last-updated: 2026-07-07
canonical-ref: docs/session-records/AI2AI-archive.md (Sessions #5–#11) / AI2AI.md
---

# docs/session-records/AI2AI-archive-old.md

## What

`AI2AI-archive.md` のログローテーションで分離した**旧 Session Records #1–#4 と旧プロトコルノート**（2026-07-07 分割）。現行の Sessions #5–#11 は `AI2AI-archive.md` に残る。

## Why

owner 目標「A 以外の全ファイル ≤1,000 行」に従い `AI2AI-archive.md`（1,513 行）を分割。Sessions #1–#4 + 旧プロトコルノート（Repository Improvement Protocol / Authority Tier Model 等）を本ファイルへ分離し、main archive を 690 行に圧縮。

## How

- 本ファイルは読み取り専用アーカイブ。新規 Session Records は `AI2AI-archive.md` に追記される
- Check 26（max session number 検証）は `AI2AI-archive.md` のみ参照。本ファイルは対象外
- Check 96（1-to-1 mirror bijection）が本ファイルの存在を BLOCKING で要求

## Constraints

- **変更不可**: Sessions #1–#4 は immutable historical record
- **Check 96**: 本 mirror doc が tracked-file bijection を満たす
- aio-manifest の digest 対象外（supporting_evidence には `AI2AI-archive.md` のみ登録）

## Change impact

- 追加により Check 96 が 1 件増加（本 mirror doc が必要）
- aio-manifest の digest 連鎖は `AI2AI-archive.md` が対象で変わらない
- Check 26 への影響なし（max session number は main archive で引き続き 11）

## Audience-specific notes

### For AI agents
- 役割タグ: `session-records-archive`, `old`, `read-only`, `sessions-1-to-4`
- **追記禁止**: 新規 Session Records は `AI2AI-archive.md` へ
- 次のローテーション時: `AI2AI-archive.md` が再び ≤1,000 行を超えたら古い sessions を本ファイルへ移すか `AI2AI-archive-old-2.md` を新設

### For human engineers（新卒レベル）
- 古い session records（最初の 4 セッション）と旧プロトコルノートの保管庫

### For third parties / auditors
- 2026-04-17〜04-25 の Sessions #1–#4 と旧プロトコル制定記録。歴史的 audit trail。
