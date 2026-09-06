---
file: LICENSES/rounds/2026-08-26-license-discuss-sent.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-06
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.submission.md (license-review 向けに用意した別文書) / LICENSES/REVIEWERS.md
---

# LICENSES/rounds/2026-08-26-license-discuss-sent.txt

## What

**2026-08-26 に OSI `license-discuss` へ実際に送った文面**を、公開アーカイブから逐語で写した
もの。本文 5,778 語。冒頭に出所・取得日・ヘッダのみを付し、`----- begin verbatim -----` 以降は
一字も変えていない。

## Why

`rounds/` は「受け取った本文を無改変で置く」ための場所だが、**その規約は相手の言葉についてだけ
書かれていて、自分の言葉には向けられていなかった**。結果として、この track で最も一次的な
資料 ——「我々が実際に何と言ったか」—— が **リポジトリのどこにも無く、第三者のアーカイブに
しか存在しない**状態が 11 日続いた（`ACD-1.0.against.md` #82）。

同じ期間、`REVIEWERS.md` と 2 つの front matter は `ACD-1.0.submission.md` を
"the message as sent" と名乗っていた。だが送ったのは 5,778 語で、submission.md §B.0 は
**11 日後に書いた ≈600 語の別物**である。**送った文面を持っていないと、「送った文面」を
名乗る文書が別物であることにも気付けない。**

## How

- 出所は OSI の公開アーカイブ（`license-discuss_lists.opensource.org/2026-August.txt`）
- 逐語部分は編集しない。誤字も改行も送ったままにする
- 返信が来た場合、それは**別ファイル**として `rounds/` に置く（`README.md` の規約に従う）
- この file を「今の主張」として引用しない。**送った時点の記録**であって、その後の是正
  （#79 / #80 / #82）は反映されていない

## Constraints

- ACD-1.0 本文は凍結中（`FROZEN.md` / Check 453）。この file は本文ではないので凍結対象外だが、
  **逐語部分を書き換えることは記録の破壊**であって改善ではない
- Check 108 が `docs/files/` mirror との 1 対 1 を BLOCKING で強制する

## Change impact

逐語部分を変更する正当な理由は存在しない。ヘッダ部分（出所・取得日）を直すのは可。

## Audience-specific notes

- **審査者**: 我々がリストに何と言ったかは、この file が権威。`submission.md` は
  `license-review` 向けに用意したもので、**まだどこにも送っていない**
- **監査人**: 語数・日付はアーカイブから機械的に取れる。`REVIEWERS.md` の表と突き合わせよ
- **後任 AI**: 「送った文面」を名乗る文書が実物と違いうる、という class の実例
