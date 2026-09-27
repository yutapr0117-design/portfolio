---
file: LICENSES/rounds/2007-09-license-discuss-ms-pl-decision-makers-observed-3of3.txt
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-09-27
canonical-ref: LICENSES/rounds/README.md (置き方の規約) / LICENSES/ACD-1.0.review-doctrine.md §1.127 / LICENSES/ACD-1.0.against.md
---

# LICENSES/rounds/2007-09-license-discuss-ms-pl-decision-makers-observed-3of3.txt

## What

**"For Approval: Microsoft Permissive License" スレッド（331 通・2005-12〜2007-10）のうち、
決める側が書いた 26 通**の第 3 部（全 3 部・2026-09-27 取得）。
**我々宛ではなく、ACD-1.0 についてでもない。**

**選別の規則を本文冒頭に書いてある**（差出人が tiemann / nelson / dibona / rosen / danese /
cooper / opensource.org のいずれかに一致）——**再現できる形にしてあるのは、選んだ余地を
読者が測れるようにするため**である。

## Why

**#243 の census が挙げた最大の未読スレッド**（通数 331）で、**優先順位は通数ではなく
「決める側が何を述べたか」で決めた**（#243 の潰し方）。得られたものは 2 つとも我々の条に当たる ——

- **vanity の異議に、理事会が答えている** —— *"the OSI board **does not give that argument much
  weight as long as the license is reusable**"*（Nelson 氏・委員長として 2007-09-06 の要約）。
  **提出パケット §4b（固有名詞 0・置換テキスト 0）が答えている当の項目である。**
- **Tiemann 氏（当時の OSI 会長）の評価関数** —— *"if a license is submitted with **promise X**,
  then we should **evaluate promise X as well as the OSD**"*。**ACD は OSD を越える約束を
  している**（PREAMBLE / §6.5 / §3+§4 / §8.4）ので、**gap は存在理由であると同時に、
  我々が測られる基準にもなる。**

## How

月次 mbox を**ブラウザ相当の UA** で取得し、件名で当スレッドを切り出したうえで、
上記の規則で差出人を絞り、header ごと無改変で保存した。

## Constraints

- **無改変で保存する**（`rounds/README.md`）。**分割は byte を変えない。**
- **観測（`-observed`）であって受領ではない。**
- **3 部は 1 組である。**
- **⚠ これは 2007 年の理事会と会長の発言である。** 2026 年の委員会が同じ物差しを使う保証は無い。

## Change impact

- `rounds/` に file を足したら `rounds/README.md` の在庫表と件数も同じ commit で（**Check 465**）。

## Audience-specific notes

- **AI（実装者）**: **有利な 1 件（vanity ↔ reusable）と不利な 1 件（promise X）が同じ束に在る。**
  片方だけを引かないこと。
- **監査人**: 選別規則は本文冒頭にあり、同じ規則で再現できる。
