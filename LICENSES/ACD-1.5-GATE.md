---
file: LICENSES/ACD-1.5-GATE.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md（合議の記録・議題 20・24・29・31・32）/ .github/scripts/_lib_gate_pin.py（Check 504 と確定の道具の本体）
---

# ACD-1.5 を出す版に替える前の最後の門

<!-- GATE-TEXT -->
この門は、n8 を読んだ独立の 2 体の結果（1 体 HIGH 3・1 体 HIGH 0。2026-11-25）を見た後に、5 人の合議（議題 29 の丙 + 丁・5/0/0）で選んだ。つまり**結果を見た後に選んだ門**で、議題 24 の門（HIGH 0）より緩い。門を緩めたのは 2 度目で、どちらも結果を見た後である。その事実は `ACD-1.0.against.md` #332 にも書く。門を選んだ後は、この文と、読み手へ渡す指示文と、草案の本文と、変更の一覧（`CHANGES-ACD-1.5.txt`）を固定し、動かせば 7 日を数え直す。

1. 出す版は、門を通るまで ACD-1.4 のまま動かさない。1.5 は草案として置く。
2. 読む前に 7 日置く（GATE-PIN の since から）。7 日は、草案の本文と一覧の直しが main に入った日から数える。
3. 読むのは**1 回だけ**。独立の読み手 2 体で、互いに見せず、下の指示文だけを渡す。読み手は、これまでの読み（1〜11 回目）をした読み手とは**別の agent**（ドシエも会話も持たない）で、A と B は模型も分ける（A = opus、B = fable。fable が使えなければ opus で読み、使えなかったと結果に書く）。模型が違うと重さの尺度もずれうるので、結果の行の下に、どちらの模型がどの重さを付けたかを並べて書く。B も opus で読んだときは、2 体の独立の度合いが落ちることを結果に書く。報告が 1 文字でも届いたら 1 回に数え、回し直さない（途中で切れた・指示文のとおりでない報告は、差の数えが終わっていないので不合格）。1 文字も届かなかったとき（利用上限・道具の故障で読み手が始まらなかった）だけは数えず、起きたことを結果に書いて回す。生の出力は reports に置く。
4. 数え方: 一覧に無い HIGH と、PARTLY LISTED の HIGH は、どちらの読み手が出しても「無い HIGH」に数える。数は 2 体で合算も平均もせず、席ごとに数え、席ごとに判定する（1 席でも合格の条件を満たさなければ不合格）。LISTED でも、その項目は自分の場面を正しく書いていないと読み手が言った HIGH は「無い HIGH」に数える。数は報告の先頭の行でなく、差ごとの印から数える。MEDIUM と LOW は合否に使わず、全部を記録する。重さは読み手が一覧を開く前に決めたものを使う。
5. 合格: 一覧に無い HIGH 0・PARTLY LISTED の HIGH 0・一覧に在る HIGH は 1 件ごとに、残すことに 5 人が**全員一致**（理由と逆側を `ACD-1.5-EFFECT-DIFF.md` と合議の記録に書く）。1 人でも反対なら不合格とし、6 項に従う（読みの後は本文も一覧も動かさない。動かせば誰も読んでいない本文になる）。条を 1.4 の語へ戻せるのは、7 日を数え始める前の採決（議題 32）だけである。
6. **落ちたら** 1.4 のまま出す版を替えない。1.5 は草案として残す。**3 つ目の門は作らない**。落ちた後に門を言い換えて読み直さない。
7. 合格でも、確定・凍結・提出の前提（段 6b の 30 日・6c・法的レビューの不在の開示）は別に残る。合格は、出す版を替えることではない。替えるかは別の議題で 5 人が採決する。
<!-- /GATE-TEXT -->

## 読み手へ渡す指示文（そのまま渡す）

<!-- GATE-PROMPT -->
### 丁の門で読み手へ渡す指示文（n8 の 2 体に渡した文。<DIR> だけ置き換える・agentType Explore / A = opus・B = fable（使えなければ opus で、使えなかったと結果に書く）・互いに見せない）

<DIR> には previous.txt（出している版の本文）・candidate.txt（草案の本文）・listed-changes.txt（CHANGES の写し）の 3 つだけを置く。

### A

Work in two steps, reading only the files named here, all in <DIR>. Do NOT open anything else or search.

STEP 1. Read previous.txt (the previous version of a public licence instrument) and candidate.txt (a candidate that restates it, with the clauses renumbered). Go through the previous version clause by clause, find where its content arrives, and list every difference in EFFECT: something a recipient, publisher, contributor, or successor may do, must do, or may be sued for that changes between the two texts. Read adversarially, as a person arguing that the candidate drops a permission, adds an obligation, narrows or widens the patent licence, or leaves unbound someone who should be bound (a purchaser of the publisher's patents, a merged company, an exclusive licensee, a person who passes on a notice, an employee submitting a patch). Rank at most 14, each rated HIGH (a reviewer or court could reach a materially worse result than under the previous text for someone the previous text protected, or the candidate contradicts itself on something important), MEDIUM, or LOW. Fix these ratings before step 2.

STEP 2. Only then read listed-changes.txt, the publisher's own public list of changes in effect. For each of your differences, mark LISTED (give the item number, and say whether the item describes your scenario accurately), PARTLY LISTED, or NOT LISTED. Do not change a rating because the difference is listed. Also say whether any listed item is inaccurate about the candidate.

Report: first line = number of HIGH, and how many of those are NOT LISTED. Then each difference: clause numbers in both, exact quoted words of each, the concrete scenario, rating, LISTED mark. Do not pad. Max 1000 words.

### B

Work in two steps, reading only the files named here, all in <DIR>. Do NOT open anything else or search.

STEP 1. Read previous.txt (the previous version of a public licence instrument) and candidate.txt (a candidate that restates it, with the clauses renumbered). You are, in turn, (1) counsel for a later owner, exclusive licensee, or successor of the publisher's patents or copyrights, including a buyer of a single patent; (2) counsel for a downstream user or a trainer of models; (3) counsel for the publisher, who is an individual releasing personal material (a diary, a voice recording, health data) and a company releasing software, including a security tool; (4) an open source licence reviewer asking whether the candidate imposes or purports anything the previous text did not. Compare the two texts in effect, clause by clause, from all four seats. List at most 14 differences in effect, ranked, each rated HIGH (materially worse for someone the previous version protected, or self-contradiction on something important), MEDIUM, or LOW. Fix these ratings before step 2.

STEP 2. Only then read listed-changes.txt, the publisher's own public list of changes in effect. For each difference, mark LISTED (item number, and whether the item describes your scenario accurately), PARTLY LISTED, or NOT LISTED. Do not change a rating because the difference is listed. Also say whether any listed item is inaccurate about the candidate.

Report: first line = number of HIGH, and how many of those are NOT LISTED. Then each difference: clause numbers in both, exact quoted words, concrete scenario, rating, LISTED mark. Then, for each seat, the single strongest new argument the candidate allows that the previous version did not. Do not pad. Max 1000 words.
<!-- /GATE-PROMPT -->

## 固定の印

`moved_clauses.py --pin` が書く。2026-11-25（UTC）に打った: 本文は n8、一覧・#332・門の文・議題 34 の採決が main に入った後である。**2026-11-27（UTC）に打ち直した**（議題 38・下の「印の後の直し」）。読みは早くて 2026-12-04 以降。動かせば数え直し（`--pin`）。

**印の後の直し（議題 38・2026-11-27 UTC・読みの前・1 度だけ）**: `CHANGES-ACD-1.5.txt` の 9 の末に、適用の前に結んだ契約（秘密保持・用途の制限）の請求を足した —— 1.4 §5.1 第 2 文は理由を限らずに止め、n8 の 2.5(d) は *by reason of its being such a use or of what the Work contains* に限り、5.1 は Dedicator が後に課すものだけを言うので、一覧に無い狭まりだった（`ACD-1.5-UNIQUE-READING.md` の §5.1（時点）の行・T152）。足した文は「1.4 が止めた／n8 は後の行為だけ／契約が中身を守るなら中身の理由で内と読める／9.1 はどの外の読みにも反する」の 4 つ。本文（区切り線より下）は 1 語も動かしていない。直しの前に 5 人が既知の行（UNIQUE-READING・errata・EFFECT-DIFF・CLAUSE-MAP）と本文を人の目で 1 回だけ掃き（agent に 2 本を読ませる予行はしない）、新しい欠けはこの 1 件だった。**逆側**: 門の対象を読みの前に動かすのは調整の 3 度目である（`ACD-1.0.against.md` #332）。結果を見る前の直しだが、読み手の目に合わせて一覧を磨いたと読まれうる。打ち直しはこの 1 度きりで、以後に見つかった欠けは読みの結果に任せる（議題 38 の条件）。

<!-- GATE-PIN: version=1.5 since=2026-11-27 days=7 body-sha256=dc7fd29a5e3bfe4f33806dc04a00cb22f8246240160028a6cbe0eab47ea41b39 changes-sha256=9298ac9227e9cb677910810aaf894d4425511dd0a9bdf0a1ebb06a0da92958c2 text-sha256=30857e18272a6c942b5259bf57801c7218893c6012efe539464d15be22a10821 prompt-sha256=ef5adf7867e53c9bafc8aa7b3406f9e978f338255e5e143b9526cecfea30af10 -->

## 読みの結果（1 回だけ）

`ACD-1.5-EFFECT-DIFF.md` の印の `high` は、この読みが残した HIGH の実数で、合格の結果の `listed-high` と同じ数を書く（残すと決めたものも数える）。確定の道具は両方を見る。

始まらなかった回（1 文字も届かなかった回）は、日付と理由を 1 行ずつここに残す: （まだ無い）

形: `date=YYYY-MM-DD unlisted-high=N partly-high=N listed-high=N listed-high-agreed=N models=<A>,<B> reports=<repo の path>`

欄の数は 2 席の和集合（同じ条の同じ差は 1 と数える）で、記録の数である。合否は席ごとで、どちらかの席が「無い」または PARTLY LISTED と言った HIGH が 1 つでも在れば不合格（和集合で丸めて消さない）。席ごとの数は下に並べる。

<!-- GATE-RESULT: none -->
