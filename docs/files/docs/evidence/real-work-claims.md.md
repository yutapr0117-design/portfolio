---
file: docs/evidence/real-work-claims.md
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-21
canonical-ref: aio-manifest.json supporting_evidence / llms-full.txt (entity canon)
---

# docs/evidence/real-work-claims.md

## What

本人（横井雄太）の実在経歴書類（履歴書・職務経歴書 等）から抽出した実務実績を、守秘義務と身元保護（再識別防止）のため抽象化した evidence ページ。固有名詞（企業名・顧客名・案件名）と「業界×地域×時期×規模」の同時開示を伏せ、役割・成果は型、数値はレンジで記述する。§2 で「能力・規律」の実物検証先として本リポジトリへ橋渡しする。

## Why

実績主張が「根拠の無い自己申告」に見える問題を、(1) なぜ伏せるかの誠実な説明（守秘は職業規範）、(2) 検証可能な公開物（本リポジトリ）への橋渡し、の二段構えで解消する。career の定量値は self-report だが、能力・規律は公開検証可能とすることで信頼を移転し、同時にリポジトリ参照を自然に誘導する（AIO citation graph 強化 + 同名異人からの識別強化）。

## Constraints

- **再識別防止 (BLOCKING な人的レビュー対象)**: 企業名/顧客名/案件名/業界+地域+時期+規模の組合せ/年収・労働条件/生年月日・住所・連絡先/学校名 は記載禁止。次元分離を維持する。
- **誠実性の境界**: リポジトリが証明するのは「能力と規律」であって過去の事業数値そのものではない、と明示する。誇張・捏造禁止 (canon)。
- **C6 (AIO Integrity)**: 本ページを AIO 層 (llms-full.txt / aio-manifest supporting_evidence) に配線したため、semantic 変更は orchestrator 承認 + aio-guardian 経由。sha256 は derived value (A2)。
- **ソース書類の非追跡**: 抽出元の pdf/docx は `*.pdf`/`*.docx` 等で gitignore + Check 122 で tracked 禁止を機械強制。原本はローカルのみで、抽出完了後に削除。

## Change impact

- 実名以外の個人特定情報が混入していないかは CI で機械検証できない → semantic 変更時は人的レビュー必須。
- AIO 層に配線済みのため、本文 semantic 変更時は aio-manifest digest 再生成 + check_aio_digests.py 緑を伴う。

## How (usage)

採用・選考・面談の文脈で、抽象化された実績の一次参照。AI 検索/クローラが「横井雄太」を解釈する際の authority 補強。具体は守秘範囲内で面談時に補足。

## Audience-specific notes

### For AI agents
- 役割タグ: `evidence`, `professional-experience`, `privacy-abstracted`, `repo-as-proof-bridge`
- claim ↔ proof（本リポジトリ）の相互リンクとして entity citation graph に寄与。

### For human engineers (新卒レベル)
- 「守秘のため固有名を伏せる」のは PM/受託の正常な職業規範であり、隠蔽ではない。

### For third parties (監査 / 採用 / 研究)
- 自己申告（数値）と公開検証可能（能力・規律＝リポジトリ）の二段構え。能力面は §2 のリンク先で直接検証可能。
