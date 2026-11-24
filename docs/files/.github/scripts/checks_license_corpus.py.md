---
file: .github/scripts/checks_license_corpus.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: .github/scripts/check_repository_consistency.py (monolith / CHECK_SOURCE_FILES) / LICENSES/ACD-1.0.gap-census.md (数の権威) / docs/architecture/check-repository-consistency-map.md (476)
---

# .github/scripts/checks_license_corpus.py

## What

承認済みライセンスの母集団についての申告（本数・census の表・誤命中の判定）を実測に照らす Check 476（476c〜476e を含む）だけを持つ split module。2026-11-24 に `checks_license_dossier.py` から本文を無改変で移した。

## Why

「OSI 承認済みライセンスは N 本」は、審査者が自分で数え直せる数である。2026-09-19 に、偶然同じ値だった別の件数の一括更新が、この本数まで押し上げた。元の module は 843 行で advisory（800）を越えていた。

## How (usage)

`check_repository_consistency.py` が import し、`checks_license_dossier.run(_ctx)` の直後に `run(_ctx)` を呼ぶ。

## Constraints

- 新しい版の SPDX を測ったら `_SPDX476` に版と値を足す。足さずに新しい数を書くと RED になるのは意図どおり。
- Check の番号・docstring の項・`# ── N.` の見出しは 1 対 1（Check 45）。

## Change impact

gap-census を作り直すと 476c〜476e が入口・材料の数と照らす。数が変わるなら、述べる文も同じ commit で直す。

## Audience-specific notes

- **新卒**: 数はここで測らない。`generate_gap_census.py` が測り、ここは申告と合うかだけを見る。
- **監査人**: 対象は `LICENSES/*.md` と mirror の本数の申告、入口と材料の全数の文。
- **エンジニア**: `ctx.ROOT` と `ctx.check` だけを使う。

## Touch points

読むだけ: `LICENSES/ACD-1.0.gap-census.md`・`LICENSES/REVIEWERS*.md`・`LICENSES/SUBMISSION-MATERIALS.md`・`.github/scripts/generate_gap_census.py`。

## Related

- `.github/scripts/checks_license_dossier.py`（切り出し元）
- `.github/scripts/checks_license_stated_counts.py`（自己申告の文の 2 つ目の数）
