---
file: .github/scripts/add_round.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / .github/scripts/sync_stated_counts.py (runbook §9 の数を書き直す)
---

# .github/scripts/add_round.py

## What

公開アーカイブの月の写しから通を切り出し、`LICENSES/rounds/` に受領文を 1 ファイル置く一式を 1 回で行う手回しの道具。

1. 月の写し（`DOSSIER_ARCHIVE_CACHE`、既定 `~/osi-archive-cache`）を pipermail の区切り行で通に分ける。件名・差出人・Date・本文の決め手（`--needle`・引用行を除いた本文の部分一致）で通を選ぶ。
2. ヘッダ（Source / Retrieved / Messages / Senders / Position）と `----- begin verbatim -----` を書き、選んだ通をそのまま続ける。Retrieved の日付は月の写しの更新日時。
3. 1,000 行を越えるなら止め、800 行を越えるなら警告する。
4. `docs/files/` の mirror の雛形を `--what` / `--why` で書く。
5. `rounds/README.md` の在庫表に、日付の位置で 1 行差し込む。
6. 新しい 2 file を `git add` し、`sync_stated_counts.py --apply` で runbook §9 の追跡ファイルの数を書き直す。

`--dry-run` は何も書かない。

2026-11-15 の 2f の検証で 3 点を直した。

- `--subject` は文字どおりに照らす（空白の違いは無視）。正規表現として読んでいたので、"BSD + Patent" が 0 通で止まった。正規表現が要るときは `--subject-regex` を使う。
- `--date` は Date を日付として比べる。部分一致の "2 Sep 2015" は "12 Sep 2015" にも当たっていた。
- `--count N` で、選ばれた通の数が N でなければ止まり、候補を日付・差出人・本文の頭で並べる。同じ人・同じ日に 4 通ある会話（Rosen 氏 2016-01-21）で確かめた。

## Why

2f は受領文を 1 日に 15 回ほど手で置き、2 回ずれた（2026-11-15）。落とし穴は次の 6 つ。

- 件名の折り返し（"PPPL\n BSD-3"）で照合が外れた。
- Date の 1 桁の日は先頭が空白（" 2 Sep"）になる。
- 同じ人・同じ日に複数の通がある。
- 件名が MIME 符号化（=?utf-8?q?…）されている。
- 引用で長くなった通がある。
- 会話が月をまたぐ。

道具は、件名の折り返しをつなぎ、MIME を復号し、`[License-discuss]` と `Re:` を外してから照らす。Date は空白をつぶしてから照らし、`--needle` で 1 通に絞る。`--month` は複数指定できる。

## How (usage)

```bash
python3 .github/scripts/add_round.py --list license-review --month 2025-February \
  --subject "ModelGo Zero License" --sender Berkus --slug modelgo-zero-berkus \
  --position "Not addressed to us. Observed. The message is kept whole." \
  --what "…" --why "`ACD-1.0.review-readings.md` §1.N の一次資料として置く。" --row "**観測（…）**" --dry-run
```

## Constraints

- 通は丸ごと置く（`kept whole`）。引用を切り詰めない。既存の受領文の約半数は、末尾の長い引用を切り詰めて置いている。道具が切り出す通は、末尾の空白を除けば月の写しの通と同じである（既存 61 件のうち、通が丸ごとの 30 件で照合した）。
- 置く先が既に在れば止まる。上書きしない。
- 引用で 1,000 行を越える通は、置かずにアーカイブの月を引く（rounds/README 規則 6）。その判断は人が行う。

## Change impact

- `rounds/README.md` の在庫表の行の形（`| YYYY-MM | \`list\` | … | \`file\` |`）を変えると、差し込みの位置がずれる。

## Audience-specific notes

### For AI agents（次担当）

- 置いたあとに、引く節（`review-readings.md` など）へ § と逐語を書き、verify を回す。

### For human engineers（新卒レベル）

メーリングリストの過去ログから特定のメールを抜き出して、記録用のフォルダに決まった形で保存する道具。

### For third parties / auditors

`----- begin verbatim -----` より下は、元のアーカイブの月の写しの通と同じ byte 列である。
