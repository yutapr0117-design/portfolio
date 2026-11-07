---
file: .github/scripts/entry_quotes_verified.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-07
canonical-ref: .github/scripts/verify_dossier_quotations.py (`--record-entry` が更新する) / .github/scripts/checks_license_references.py (Check 472n が読む)
---

# .github/scripts/entry_quotes_verified.txt

## What

入口の面の斜体の引用のうち、手元の全 corpus で原文を確かめたものの hash の一覧。`own: ` の行は我々自身の文である。

## Why

引用を読みやすく動かす誤りが 6 回出て、どれも手の照合でしか見つからなかった。公開アーカイブの全文は CI に無いので、CI は原文そのものを見られない。確かめた時点の引用の hash を置けば、語を動かした時点で RED にできる。

## How

```sh
DOSSIER_ARCHIVE_CACHE=<cache> python3 .github/scripts/verify_dossier_quotations.py --record-entry
```

確認できた引用の hash を書き直す。`own: ` の行と `#` の行は残す。確認できない引用が 1 件でもあれば一覧に出して、file は書き換えない。

## Constraints

- 原文を持たない文を hash の側へ入れない。我々自身の文は `own: ` の行で足す。
- `rounds/` か本文に在る引用は、この file が無くても解決する。
- hash は正規化した引用について取るので、約物と大文字小文字の差は見ない。

## Change impact

入口の面の範囲は `measure_citation_drift.py` の `FIRST_READ` が決める。範囲を広げたら `--record-entry` を回す。

## Audience-specific notes

- **AI**: 入口へ引用を足すときは、原文に当ててから `--record-entry` を回す。Check 472n が RED になったら、hash を足すのではなく原文を読む。
- **監査人**: この file は確かめた事実の記録で、hash だけでは原文の正しさを証明しない。確かめ直すには `--record-entry` を回す。
