---
file: .github/scripts/make_redline.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-24
canonical-ref: LICENSES/ACD-1.1-CHANGELIST.md §0.5 (1.0 → 1.1 の条番号対応・この道具が読む単一の出所) / LICENSES/OSI-APPROVAL-PLAN.md (段 6b)
---

# .github/scripts/make_redline.py

## What

ACD の 2 つの版の差（redline）を、新しい版の条の順に、条ごとに出す手回しの道具。出力は 80 桁以内の ASCII の plain text で、メールに貼ることも添付することもできる。

- 各条を「unchanged」「changed」「not in ACD-旧」「not in ACD-新」のどれかに分ける。changed の条は語の差を `[-旧-]{+新+}` で示す。
- 同じ番号が両方の版に別の中身で在るとき（1.0 の §15.5 / §15.6 / §16.5 は消え、後の版が同じ番号に別の条を置いた）は、その旨を見出しに添える（2026-11-15・50 の検証）。
- 前文と節の見出しも同じ扱いにする。
- 冒頭には 2 つの入力の file 名・sha256 の先頭 16 桁・語数を書く。最後に 4 区分の件数を書く。
- 述べ直した版（`CLAUSE-MAP-x-y.tsv` が間に在る）をまたぐ差は、同じ番号で別の条どうしを並べてしまうので、終了コード 2 で止まり、全文・`CHANGES-ACD-*.txt`・CLAUSE-MAP を案内する（2026-11-24）。
- `--changed-only` は unchanged の条を省き、「新しいところだけ」の抜粋にする。
- `--context N`（2026-11-15）は、変わった語の前後 N 語だけを残し、間の変わらない語を `...` にする。全文の redline は 1.0→1.4 で 5,702 語あり本体とほぼ同じ長さだった（`--context 8` で約 4,500 語。増えた語と減った語そのものが約 2,700 語あるので、それ以上は縮まない）。list に貼る抜粋か、添付にするかの判断の材料にする。

## Why

審査者は新しいライセンスに、既存のものとの差を求める。Chestek 氏（2026-01-23）と Sado 氏（2026-01-24）は、redline か *"innovations only"* の抜粋を求めた。計画の段 6b では、本申請の前に、1.4 の新しい語を 1.0 との差としてオーナーが license-discuss へ出す（50 の依頼・2026-11-15）。差を手で作ると、条の対応を取り違えやすく、語も落としやすい。1.0 と 1.1 以降では、§1 と §15 の条番号がずれている。

## How (usage)

```bash
python3 .github/scripts/make_redline.py LICENSES/ACD-1.0.txt LICENSES/ACD-1.4-DRAFT.txt > redline-1.0-1.4.txt
python3 .github/scripts/make_redline.py --changed-only LICENSES/ACD-1.3.txt LICENSES/ACD-1.4-DRAFT.txt
```

CI では回さない。出力は投稿の日・申請の日に作る。どの commit の本文から作ったかは、冒頭の sha256 で確かめられる。

`--coverage <前版> <草案>`（2026-11-20・50 の依頼）: 条ごとの語の差の塊（hunk）それぞれを、変更の一覧（`CHANGES-ACD-N.M.txt`、無ければ草案の
冒頭）の箇条に当てる。quote = その条（N.M・前文は Preamble・節の見出しは "heading of Section N"）を名指す箇条の引用が塊の語の 3 語の
連なりを持つ / named = 条を名指す箇条は在るが言い換えで述べる / none = どの箇条もその条を名指さない（述べられない変更）。none があれば
終了コード 1。段 7 の「1.3 との差分の完全性」を確定の日にも回せるようにした（1.3 → 1.4 で 214 塊・quote 112・named 102・none 0）。
1.0 を前版にしたときの条の対応（§0.5 の表）は当てない —— 前版は直前の版を想定する。

## Constraints

- 1.0 を旧にしたときだけ、`ACD-1.1-CHANGELIST.md` §0.5 の表で条番号を対応させる。それ以外の組は同じ番号を当てる（1.1 以降は番号を変えていない）。表を読めなければ止まる。黙って同じ番号を当てることはしない。
- 語の差は効果の差の証拠ではない。版番号と識別子の差も、そのまま差として出す。
- 草案の冒頭の注記（区切り線より上）は読まない。

## Change impact

- §0.5 の表の形（`| 1.0 | 1.1 | 何が起きたか |`）を変えると、1.0 との redline が止まる。
- 新しい版で条番号を並べ替えたときは、同じ形の対応表を足し、この道具の読み先を広げる。

## Audience-specific notes

### For AI agents（次担当）

- 投稿や申請の文面を AI が完成品として書かないのと同じく（B14）、この出力も材料として渡す。送るかどうか、何を添えるかはオーナーが決める。

### For human engineers（新卒レベル）

2 つの版の条文を並べて、どの条のどの語が増えたか・消えたかを印で示す、差分の表を作る道具。

### For third parties / auditors

冒頭の sha256 を `sha256sum LICENSES/<file>` の先頭 16 桁と照らせば、どの本文の差かを確かめられる。
