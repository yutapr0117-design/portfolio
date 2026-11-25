---
file: LICENSES/ACD-1.5-GATE.md
audience: 次のセッションの実装者（一次読者）/ 監査人
last-updated: 2026-11-25
canonical-ref: LICENSES/ACD-1.5-CHANGELIST.md（合議の記録・議題 20・24・29・31・32）/ .github/scripts/_lib_gate_pin.py（Check 504 と確定の道具の本体）
---

# ACD-1.5 を出す版に替える前の最後の門

<!-- GATE-TEXT -->
この門は、n8 を読んだ独立の 2 体の結果（1 体 HIGH 3・1 体 HIGH 0。2026-11-25）を見た後に、5 人の合議（議題 29 の丙 + 丁・5/0/0）で選んだ。つまり**結果を見た後に選んだ門**である。その事実は `ACD-1.0.against.md` #332 にも書く。門を選んだ後は、この文と、読み手へ渡す指示文と、草案の本文と、変更の一覧（`CHANGES-ACD-1.5.txt`）を固定し、動かせば 7 日を数え直す。

1. 出す版は、門を通るまで ACD-1.4 のまま動かさない。1.5 は草案として置く。
2. 読む前に 7 日置く（GATE-PIN の since から）。7 日は、草案の本文と一覧の直しが main に入った日から数える。
3. 読むのは**1 回だけ**。独立の読み手 2 体で、互いに見せず、下の指示文だけを渡す。読み手は、これまでの読み（1〜11 回目）をした読み手とは**別の agent**（ドシエも会話も持たない）で、A と B は模型も分ける（A = opus、B = fable。fable が使えなければ opus で読み、使えなかったと結果に書く）。報告が 1 文字でも届いたら 1 回に数え、回し直さない（途中で切れた・指示文のとおりでない報告は、差の数えが終わっていないので不合格）。1 文字も届かなかったとき（利用上限・道具の故障で読み手が始まらなかった）だけは数えず、起きたことを結果に書いて回す。生の出力は reports に置く。
4. 数え方: 一覧に無い HIGH と、PARTLY LISTED の HIGH は、どちらの読み手が出しても「無い HIGH」に数える。LISTED でも、その項目は自分の場面を正しく書いていないと読み手が言った HIGH は「無い HIGH」に数える。数は報告の先頭の行でなく、差ごとの印から数える。MEDIUM と LOW は合否に使わず、全部を記録する。重さは読み手が一覧を開く前に決めたものを使う。
5. この門は、議題 24 の門（HIGH 0）より緩い。緩めたのは 2 度目で、どちらも結果を見た後である。合格: 一覧に無い HIGH 0・PARTLY LISTED の HIGH 0・一覧に在る HIGH は 1 件ごとに、残すことに 5 人が**全員一致**（理由と逆側を `ACD-1.5-EFFECT-DIFF.md` と合議の記録に書く）。1 人でも反対なら不合格とし、6 項に従う（読みの後は本文も一覧も動かさない。動かせば誰も読んでいない本文になる）。条を 1.4 の語へ戻せるのは、7 日を数え始める前の採決（議題 32）だけである。
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

`moved_clauses.py --pin` が書く。**pending の間は日数を数えていない**（n8 と一覧の直し、議題 32 の採決が main に入った日に打つ）。

<!-- GATE-PIN: pending -->

## 読みの結果（1 回だけ）

`ACD-1.5-EFFECT-DIFF.md` の印の `high` は、この読みが残した HIGH の実数で、合格の結果の `listed-high` と同じ数を書く（残すと決めたものも数える）。確定の道具は両方を見る。

始まらなかった回（1 文字も届かなかった回）は、日付と理由を 1 行ずつここに残す: （まだ無い）

形: `date=YYYY-MM-DD unlisted-high=N partly-high=N listed-high=N listed-high-agreed=N models=<A>,<B> reports=<repo の path>`

<!-- GATE-RESULT: none -->
