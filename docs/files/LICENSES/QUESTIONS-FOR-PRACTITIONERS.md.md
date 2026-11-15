---
file: LICENSES/QUESTIONS-FOR-PRACTITIONERS.md
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: LICENSES/QUESTIONS-FOR-COUNSEL.md / LICENSES/ACD-1.4-DRAFT.txt / LICENSES/ACD-OSI-BOTTLENECKS.md (B1・B7・B13)
---

# LICENSES/QUESTIONS-FOR-PRACTITIONERS.md

## What

**ACD の機械学習の条（§1.7・§2.6・§6.2〜§6.4・§8.4）を、ML システムを作る人に読んでもらうための英語の 1 枚（2026-11-15 作成）。**
5 問を、それぞれ単独で答えられる形で置き、各問に条文の逐語・我々の読み・疑う理由を書いた。

## Why

**審査の側がこの読み手を名指しで求めている。** OSI が最初のモデル向けライセンス（ModelGo）を審査したとき、
理事の Josh Berkus 氏が「自分は AI/ML の利用者で開発者ではない。その専門の人のフィードバックが要る」と書き、
条ごとに AI システムを作る人のコメントを求めた（`license-review` 2025-02-25）。
ACD の ML の条は誰の実務家にも読まれておらず、我々の読み（§14.13 の 5 つの立場）は起草した AI 自身の読みである。
依頼はオーナーにしかできないので、AI にできるのは依頼 1 回の費用を下げる材料を作ることである（QUESTIONS-FOR-COUNSEL と同じ考え方）。

## How

条番号は 1.4 草案（1.3 と同じ番号）。引用は 2026-11-15 の草案の逐語で、照合した。
問いは「その語で自分の行為・成果物・合図・形式を認識できるか」に絞り、OSD 適合やライセンスの良し悪しは問わない。

## Constraints

- **AI が起草したことを冒頭で開示する。** 薄めない（`REVISION-PROTOCOL.md` ゲート 0）。
- 公開の回答は `rounds/` に逐語、私信は日付だけの stub（`rounds/README.md`）。
- 回答が「実務と合わない」なら、草案の試作（`ACD-1.4-SECOND-CLARITY-TRIAL.md`）の出所として扱い、凍結版に同じ語があれば errata へ。

## Change impact

草案の §1.7・§2.6・§6・§8.4 の語が変われば、問いの引用を当て直す（Check 468a はドシエが「1.4 草案」として引く逐語を照合する）。

## Audience-specific notes

- **オーナー**: 知り合いの ML エンジニアに 1 問だけ聞く形でも足りる。§3（因果の判定）と §2（成果物の 5 つの名詞）が最も重い。
- **AI**: 回答を受けたら、B1（外部のレビュー）・B7（§8.4 の射程）・B13（理解の費用）の注を更新する。
