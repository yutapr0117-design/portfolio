---
file: LICENSES/MACHINE-SURFACES-AUDIT.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-24
canonical-ref: LICENSES/FROZEN.md / LICENSES/ACD-1.0.txt / LICENSES/ACD-1.1.txt / LICENSES/ACD-1.2-DRAFT.txt
---

# LICENSES/MACHINE-SURFACES-AUDIT.md

## What

**機械可読なライセンスの面が述べていることが、いま真かを検証した報告（2026-09-24）。**
対象は 2 本の記述子（`ACD-1.0/1.1.machine.json`）・`spdx.xml`・`LICENSE`・`REUSE.toml`・
`aio-manifest.json` と `llms-full.txt` のライセンス記述、外縁として sitemap の `image:license` と
バイナリのメタデータ。照合先は凍結テキスト・1.2 草案・`FROZEN.md` の `POSTING-STATUS`。
欠陥の候補 15 件と、clean だった面 10 件を同じ重さで書いている。

## Why

register / 本文の作業と並行して走らせたため、**欠陥を直さず候補として列挙する**分担にした。
件数の同期を 2 か所で走らせると競合するからである。記述子や sitemap のように**人が読まない面**は、
条文の側をいくら整えても drift に気付かれにくい。

## How

各テキストを条単位に分解し、記述子の `clause` が指す条の本文を印字して主題を読んだ。
版をまたぐ番号は定義語と本文の類似度で対応付けた。REUSE は `reuse` 6.2.0 で実際に lint した。
公開面（GitHub Pages）の実物はこの環境から到達できず、測っていない。

## Constraints

- **凍結 2 本と `.well-known/*` は読むだけで、触っていない。**
- **報告であって修正ではない。** 候補を register へ入れるかは register の担当が決める。
- 主題の一致は条文を読んだ判断であって、機械検証ではない。

## Change impact

候補が拾われて直っても、この報告は**その時点の記録**として書き換えない。
同じ検証を繰り返すなら新しい日付の報告を足す。

## Audience-specific notes

- **AI（次のセッション）**: §3 に候補ごとの行き先の見当がある。M1（sitemap の CC BY-NC-ND）と
  M2（`reuse lint` は承認と無関係に止まる）が最も重い。
- **監査人**: 方法と「測っていないもの」を §0 に明記してある。
- **第三者**: これは我々が自分の記述を疑った記録であって、第三者の検証ではない。
