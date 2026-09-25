---
file: LICENSES/ACD-1.0.gap-census.md
audience: licence reviewers, OSI license-discuss / license-review participants, 後任 AI
last-updated: 2026-09-25
canonical-ref: LICENSES/ACD-1.0.comparison.md §1.97 (条件の有無を同じ 141 本で数えた census) / LICENSES/ACD-OSI-BOTTLENECKS.md (gap の扱い)
---

# ACD-1.0 gap census —— OSI 承認済み 141 本に 3 つの gap を当てた（2026-09-25）

> **これは何か**: ドシエの gap 論（「既存の承認済みライセンスは X を持たない」）を、**選んだ比較対象ではなく
> 承認済みの全数**に当てた記録。`comparison.md` §1.97 は同じ 141 本で**条件の有無**を数えた。
> **ここでは 3 つの gap そのもの**を 1 本ずつ当てる。**表の数はすべて表から導出**しており、
> 文中の件数はスクリプトが表を数えて出したもので、手で書いていない。
>
> **先に結論（有利・不利を同じ重さで）**: (a) TDM・機械学習を名指しする承認済みライセンスは **0 本**。
> (b) 公有等価の 3 本（`0BSD`、`MIT-0`、`Unlicense`）は**特許の語を 1 回も使わない**。**ただし特許を明示許諾する
> 許容型は既に在る**（`BSD-2-Clause-Patent` / `BlueOak-1.0.0` / `UPL-1.0` ——いずれも条件を持つ）。
> (c) 学習済みモデル・パラメータ・出力を名指しする許諾は **0 本**。**ただし「作品を超えて及ぶ」特許許諾は
> 4 本在り（UPL の Larger Works / CERN-OHL の Products）、**「実行の出力はライセンスの外」という
> 規定は GPL 系・Artistic-1.0 系に古くから在る**。gap は「誰も考えなかった」ではなく**「誰もこの対象に向けて書かなかった」**である。

## 方法

- **取得**: 2026-09-25T03:51:32Z（UTC）。SPDX `license-list-data` 既定ブランチの `json/licenses.json`
  （licenseListVersion **3.29.0**・releaseDate 2026-09-16）から
  `isOsiApproved` かつ非 deprecated の識別子を列挙し、各 `text/<id>.txt` を取得した。
- **取得できた本数: 141 / 141**・**できなかった本数: 0**。
  deprecated の承認済み識別子 13 件（`GPL-2.0` など、`-only`/`-or-later` へ移行済みの旧名）は除外した。
- **本文の同一性**: 各 text の sha256 を取得時に記録した（下表の `sha256` 列は先頭 12 桁）。
- **語の計数**: 空白を 1 つに正規化してから、大文字小文字を区別せずに数えた。用いた正規表現:

  | 列 | 正規表現 |
  | :-- | :-- |
  | `tdm` | `text and data mining\|data mining\|\bTDM\b` |
  | `ml` | `machine learning\|artificial intelligence\|\bA\.?I\.?\b\|neural` |
  | `train` | `\btrain(ing\|ed\|s)?\b` |
  | `model` | `\bmodels?\b` |
  | `param` | `\bparameters?\b\|\bweights\b` |
  | `output` | `\boutputs?\b` |
  | `art4` | `Article 4\|2019/790\|reservation of rights\|opt[- ]out` |
  | `patent` | `patent` |

- **⚠ 語の計数は候補の抽出であって判定ではない。** 0 でない命中は**すべて文脈を読んで**判定した（下の「誤命中」）。
  0 の列は「その語が無い」ことだけを言い、**「その概念が無い」ことは言わない**（例: `MIT-0` の *without restriction*）。
- **特許許諾の判定基準**（`patent` が 1 回以上の本だけ読んだ）:
  - `明示` —— 受領者に特許の実施を許す**積極的な文**がある（*grants … patent license* 等）。
  - `明示（不行使）` —— 許諾ではなく**権利を行使しない約束**の形（GPL-3.0 §11 自身が *covenant not to sue* を patent license に含めて定義しており、同じ機能を持つ）。
  - `選択式` —— 本文は許諾を持つが、**Exhibit で選択したときだけ**効く。
  - `M-免責` / `M-留保` / `M-方針` —— `patent` の語はあるが、**非侵害を保証しない免責**・**権利の留保**・**前文や §7 型の方針**だけで、積極的な許諾文が無い。
  - `0` —— `patent` の語が 0 回。
- **範囲の判定基準**（`明示` 系のみ）: `S1` = 作品（またはその Contribution。**寄与時点の組合せ**を含む）に限る /
  `S2` = 対象は作品だが**行為や必要性の限定が緩い** / `S3` = **作品そのものを超える対象**（組合せ・製造物）を名指す。
- **⚠ 判定は人が読んだもので、正規表現の結果ではない。** 初版の抽出正規表現は `BlueOak-1.0.0` の
  *licenses you to do everything* を見落とし、GPL-2.0 系の §7（*if a patent license would not permit …*）を許諾と誤認した。**両方とも読んで直した。**

## 141 と 149 —— 同じ repo の旧い census との対照

このドシエには **「承認済み 149 本」** を母集団にした旧い測定がある（`AS-OF.md` / `AUDIT-LEDGER.md` / `ACD-OSI-BOTTLENECKS-EXTERNAL.md`・2026-09-10・SPDX **3.28.0**）。
**どちらかが誤りなのではなく、母集団の定義と版が違う。** 2 つのリストを取得して差を取った（2026-09-25）:

- **149** = 3.28.0 の `isOsiApproved` **全件**（非 deprecated 136 ＋ deprecated 13）。deprecated 13 件は `AGPL-3.0`、`GPL-2.0`、`GPL-2.0+`、`GPL-3.0`、`GPL-3.0+`、`GPL-3.0-with-GCC-exception`、`LGPL-2.0`、`LGPL-2.0+`、`LGPL-2.1`、`LGPL-2.1+`、`LGPL-3.0`、`LGPL-3.0+`、`wxWindows` ——**うち 11 件は `-only` / `-or-later` へ移行済みの旧 ID で本文が現行 ID と重複し、残る 2 件（`GPL-3.0-with-GCC-exception` / `wxWindows`）は例外条項の本文である。**
- **141** = 3.29.0 の `isOsiApproved` かつ **非 deprecated**。3.28.0 から **新たに承認済みになったのが 5 件**: `BSD-ask-to-endorse`、`CDDL-1.1`、`CNRI-Python-GPL-Compatible`、`Python-2.0.1`、`curl`。**外れたものは 0 件。**
- **旧い数との整合**: 旧 census の「patent を含む 92 本 / output を含む 30 本」は、本表の 82 本 / 18 本から「新 5 件の寄与（patent は `CDDL-1.1` の 1 本・output は 0 本）」を引き、deprecated 13 件の寄与を足すと一致する。**deprecated 13 件は 3.28.0 の `text/deprecated_<id>.txt` を取得して実測した**（patent を含むもの 11 本・output を含むもの 12 本。差し引きで出した数ではない）。
- **使い分け**: 数を引くときは**版と定義を同じ文に書く**。重複本文を数えない分、**非 deprecated の方が「何種類のライセンスが」という主張に正確**である。

## 全数表

列 `tdm`〜`output` は語の出現回数（0 は空欄）。`許諾` と `範囲` は上の基準。

| 識別子 | sha256 | patent | 許諾 | 範囲 | tdm | ml | train | model | param | output |
| :-- | :-- | --: | :-- | :-- | --: | --: | --: | --: | --: | --: |
| `0BSD` | `e3f18c71e10d` |  | 0 | — |  |  |  |  |  |  |
| `AAL` | `0f4015683803` |  | 0 | — |  |  |  |  |  |  |
| `AFL-1.1` | `1b078d9b349e` | 4 | 明示 | S1 |  |  |  |  |  |  |
| `AFL-1.2` | `a8c17d2bcdad` | 5 | 明示 | S1 |  |  |  |  |  |  |
| `AFL-2.0` | `7ecc7db84298` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `AFL-2.1` | `fbedf33db9a4` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `AFL-3.0` | `de0612c5780d` | 13 | 明示 | S1 |  |  |  |  |  |  |
| `AGPL-3.0-only` | `d8a6cc31abc1` | 25 | 明示 | S1 |  |  |  | 1 |  | 2 |
| `AGPL-3.0-or-later` | `d8a6cc31abc1` | 25 | 明示 | S1 |  |  |  | 1 |  | 2 |
| `ALGLIB-Documentation` | `e38f858c0805` |  | 0 | — |  |  |  |  |  |  |
| `Apache-1.1` | `1521ffd9660f` |  | 0 | — |  |  |  |  |  |  |
| `Apache-2.0` | `074e6e32c86a` | 7 | 明示 | S1 |  |  |  |  |  |  |
| `APL-1.0` | `ee583972c3b5` | 37 | 選択式 | — |  |  |  |  |  |  |
| `APSL-1.0` | `54702bc17c8a` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `APSL-1.1` | `81757b1a656d` | 10 | 明示 | S1 |  |  |  |  |  |  |
| `APSL-1.2` | `ea3732a5beb2` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `APSL-2.0` | `2d0c12edaaf8` | 13 | 明示 | S1 |  |  |  |  |  |  |
| `Artistic-1.0` | `b50b4f007fb6` |  | 0 | — |  |  |  |  |  | 1 |
| `Artistic-1.0-cl8` | `a0db94ded051` |  | 0 | — |  |  |  |  |  | 1 |
| `Artistic-1.0-Perl` | `9e18ef4d50fa` |  | 0 | — |  |  |  |  |  | 1 |
| `Artistic-2.0` | `bae466ac8d71` | 4 | 明示 | S1 |  |  |  |  |  |  |
| `BlueOak-1.0.0` | `8a1af140fdfb` | 2 | 明示 | S2 |  |  |  | 1 |  |  |
| `BSD-1-Clause` | `244e17b6f024` |  | 0 | — |  |  |  |  |  |  |
| `BSD-2-Clause` | `f32fb3b417a1` |  | 0 | — |  |  |  |  |  |  |
| `BSD-2-Clause-Patent` | `10500282524f` | 3 | 明示 | S1 |  |  |  |  |  |  |
| `BSD-3-Clause` | `5a93d5831e12` |  | 0 | — |  |  |  |  |  |  |
| `BSD-3-Clause-LBNL` | `49d63fdb269a` |  | 0 | — |  |  |  |  |  |  |
| `BSD-3-Clause-Open-MPI` | `a4bd3317cea7` | 1 | M-免責 | — |  |  |  |  |  |  |
| `BSD-ask-to-endorse` | `a4db73b0f831` |  | 0 | — |  |  |  |  |  |  |
| `BSL-1.0` | `84c6ef3ea9e3` |  | 0 | — |  |  |  |  |  |  |
| `CAL-1.0` | `a24987ff96bf` | 4 | 明示 | S1 |  |  |  |  |  | 1 |
| `CAL-1.0-Combined-Work-Exception` | `a24987ff96bf` | 4 | 明示 | S1 |  |  |  |  |  | 1 |
| `CATOSL-1.1` | `c30f1f9fafed` | 11 | 明示 | S1 |  |  |  |  |  |  |
| `CDDL-1.0` | `fde9ef484615` | 13 | 明示 | S1 |  |  |  |  |  |  |
| `CDDL-1.1` | `b5bbb5ac38b5` | 16 | 明示 | S1 |  |  |  |  |  |  |
| `CECILL-2.1` | `4ea234937bc7` | 4 | 明示（不行使） | S1 |  |  |  | 1 |  |  |
| `CERN-OHL-P-2.0` | `eeecc593866f` | 7 | 明示 | S3 |  |  |  |  |  |  |
| `CERN-OHL-S-2.0` | `d6475a84171f` | 7 | 明示 | S3 |  |  |  |  |  |  |
| `CERN-OHL-W-2.0` | `c1432111d0ae` | 7 | 明示 | S3 |  |  |  |  |  |  |
| `CNRI-Python` | `69b5d7d41a6e` |  | 0 | — |  |  |  |  |  |  |
| `CNRI-Python-GPL-Compatible` | `8e1f50d9b3c3` |  | 0 | — |  |  |  |  |  |  |
| `CPAL-1.0` | `54cef60295bd` | 17 | 明示 | S1 |  |  |  |  |  |  |
| `CPL-1.0` | `9698f2ba346a` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `CUA-OPL-1.0` | `2fa6914d4062` | 17 | 明示 | S1 |  |  |  |  |  |  |
| `curl` | `272d1239bdce` |  | 0 | — |  |  |  |  |  |  |
| `ECL-1.0` | `c3b96326d1e6` |  | 0 | — |  |  |  |  |  |  |
| `ECL-2.0` | `49831d277a9e` | 11 | 明示 | S1 |  |  |  |  |  |  |
| `EFL-1.0` | `76631db9123a` |  | 0 | — |  |  |  |  |  |  |
| `EFL-2.0` | `1d7818c8d044` |  | 0 | — |  |  |  |  |  |  |
| `Entessa` | `548c65ff7aad` |  | 0 | — |  |  |  |  |  |  |
| `EPL-1.0` | `f3d8dc494be2` | 11 | 明示 | S1 |  |  |  |  |  |  |
| `EPL-2.0` | `61616a406670` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `EUDatagrid` | `6508739a64a1` | 1 | M-免責 | — |  |  |  |  |  |  |
| `EUPL-1.1` | `1480d19681cf` | 2 | 明示 | S2 |  |  |  |  |  |  |
| `EUPL-1.2` | `57fb42fbcd0b` | 2 | 明示 | S2 |  |  |  |  |  |  |
| `Fair` | `59954017f5a1` |  | 0 | — |  |  |  |  |  |  |
| `Frameworx-1.0` | `073806e49e90` | 1 | M-留保 | — |  |  | 1 |  |  |  |
| `GPL-2.0-only` | `aaf135472f81` | 8 | M-方針 | — |  |  |  |  |  | 2 |
| `GPL-2.0-or-later` | `aaf135472f81` | 8 | M-方針 | — |  |  |  |  |  | 2 |
| `GPL-3.0-only` | `fb981668c18a` | 29 | 明示 | S1 |  |  |  | 1 |  | 3 |
| `GPL-3.0-or-later` | `fb981668c18a` | 29 | 明示 | S1 |  |  |  | 1 |  | 3 |
| `HPND` | `4d9ae4a36816` |  | 0 | — |  |  |  |  |  |  |
| `ICU` | `c7922dccc709` |  | 0 | — |  |  |  |  |  |  |
| `Intel` | `6337a14cec9c` |  | 0 | — |  |  |  |  |  |  |
| `IPA` | `f5449912f9a7` |  | 0 | — |  |  |  |  |  |  |
| `IPL-1.0` | `0d7fbdd478bb` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `ISC` | `521c6f0ed8e6` |  | 0 | — |  |  |  |  |  |  |
| `Jam` | `5239625d8bf5` |  | 0 | — |  |  |  |  |  |  |
| `LGPL-2.0-only` | `86dc99d7e506` | 8 | M-方針 | — |  |  |  |  | 1 | 1 |
| `LGPL-2.0-or-later` | `86dc99d7e506` | 8 | M-方針 | — |  |  |  |  | 1 | 1 |
| `LGPL-2.1-only` | `5749785c8bde` | 8 | M-方針 | — |  |  |  |  | 1 | 1 |
| `LGPL-2.1-or-later` | `5749785c8bde` | 8 | M-方針 | — |  |  |  |  | 1 | 1 |
| `LGPL-3.0-only` | `996af0513df2` | 29 | 明示 | S1 |  |  |  | 1 | 1 | 3 |
| `LGPL-3.0-or-later` | `996af0513df2` | 29 | 明示 | S1 |  |  |  | 1 | 1 | 3 |
| `LiLiQ-P-1.1` | `e29a35c0a27e` |  | 0 | — |  |  |  |  |  |  |
| `LiLiQ-R-1.1` | `efc4ee7d7064` |  | 0 | — |  |  |  |  |  |  |
| `LiLiQ-Rplus-1.1` | `a26dc35b0586` |  | 0 | — |  |  |  |  |  |  |
| `LPL-1.0` | `84110c251f5f` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `LPL-1.02` | `bc4fd6a85cae` | 14 | 明示 | S1 |  |  |  |  |  |  |
| `LPPL-1.3c` | `f0f307427080` |  | 0 | — |  |  |  | 1 |  |  |
| `MirOS` | `79da9e5c37ad` |  | 0 | — |  |  |  |  |  |  |
| `MIT` | `b05785f9f18e` |  | 0 | — |  |  |  |  |  |  |
| `MIT-0` | `59746d6285ff` |  | 0 | — |  |  |  |  |  |  |
| `MIT-Modern-Variant` | `d7366190045a` |  | 0 | — |  |  |  |  |  |  |
| `Motosoto` | `217f381da7c4` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `MPL-1.0` | `819b323d7e6d` | 5 | 明示 | S1 |  |  |  |  |  |  |
| `MPL-1.1` | `6214f8b1300b` | 17 | 明示 | S1 |  |  |  |  |  |  |
| `MPL-2.0` | `66a3107d5ad6` | 10 | 明示 | S1 |  |  |  |  |  |  |
| `MPL-2.0-no-copyleft-exception` | `66a3107d5ad6` | 10 | 明示 | S1 |  |  |  |  |  |  |
| `MS-PL` | `7a162b1da10f` | 8 | 明示 | S1 |  |  |  |  |  |  |
| `MS-RL` | `7c69e20ff863` | 8 | 明示 | S1 |  |  |  |  |  |  |
| `MulanPSL-2.0` | `eb7a1d713eb9` | 10 | 明示 | S1 |  |  |  |  |  |  |
| `Multics` | `d61ab7b7b6e9` |  | 0 | — |  | 1 |  |  |  |  |
| `NASA-1.3` | `fe59e577293a` | 6 | 明示 | S1 |  |  |  |  |  |  |
| `Naumen` | `ab999583e09a` |  | 0 | — |  |  |  |  |  |  |
| `NCSA` | `b31bbfd06e22` |  | 0 | — |  |  |  |  |  |  |
| `NGPL` | `c0c36141bbc8` |  | 0 | — |  |  |  |  |  |  |
| `Nokia` | `15425a7c7bbd` | 15 | 明示 | S1 |  |  |  |  |  |  |
| `NPOSL-3.0` | `72bd990f4e37` | 11 | 明示 | S1 |  |  |  |  |  |  |
| `NTP` | `290eb479deee` |  | 0 | — |  |  |  |  |  |  |
| `OCLC-2.0` | `dbf0de8b5934` | 3 | M-方針 | — |  |  |  |  |  |  |
| `OFL-1.1` | `8eea8287e587` | 1 | M-免責 | — |  |  |  |  |  |  |
| `OFL-1.1-no-RFN` | `8eea8287e587` | 1 | M-免責 | — |  |  |  |  |  |  |
| `OFL-1.1-RFN` | `8eea8287e587` | 1 | M-免責 | — |  |  |  |  |  |  |
| `OGTSL` | `1866b77e78b7` |  | 0 | — |  |  |  |  |  | 1 |
| `OLDAP-2.8` | `bf30f8254b66` |  | 0 | — |  |  |  |  |  |  |
| `OLFL-1.3` | `a9996155436c` | 15 | 明示 | S1 |  |  |  |  |  |  |
| `OSC-1.0` | `63648e4e7fd5` |  | 0 | — |  |  |  |  |  |  |
| `OSET-PL-2.1` | `ed99f44eca38` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `OSL-1.0` | `cce19c78a02a` | 8 | 明示 | S1 |  |  |  |  |  |  |
| `OSL-2.0` | `e1f0417f3b2d` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `OSL-2.1` | `0545a54adffe` | 11 | 明示 | S1 |  |  |  |  |  |  |
| `OSL-3.0` | `9329b26bc401` | 13 | 明示 | S1 |  |  |  |  |  |  |
| `PHP-3.0` | `8c18adf2c052` |  | 0 | — |  |  |  |  |  |  |
| `PHP-3.01` | `c288e228ae7c` |  | 0 | — |  |  |  |  |  |  |
| `PostgreSQL` | `d443a7dc550d` |  | 0 | — |  |  |  |  |  |  |
| `Python-2.0` | `893c2bafbb81` |  | 0 | — |  |  |  |  |  |  |
| `Python-2.0.1` | `1d165c0d2550` |  | 0 | — |  |  |  |  |  |  |
| `QPL-1.0` | `524dce795dfc` |  | 0 | — |  |  |  | 1 |  |  |
| `RPL-1.1` | `ea8d9811a051` | 16 | 明示 | S1 |  |  |  |  |  |  |
| `RPL-1.5` | `9bdb5f2d5854` | 14 | 明示 | S1 |  |  |  | 1 |  |  |
| `RPSL-1.0` | `358012b3f023` | 17 | 明示 | S1 |  |  |  |  |  |  |
| `RSCPL` | `190ee7c947dc` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `SimPL-2.0` | `c914635c3f2f` |  | 0 | — |  |  |  |  |  |  |
| `SISSL` | `51a1c0347887` | 6 | 明示 | S1 |  |  |  |  |  |  |
| `Sleepycat` | `74e179cd51df` |  | 0 | — |  |  |  |  |  |  |
| `SPL-1.0` | `5a38bd15c6dd` | 17 | 明示 | S1 |  |  |  |  |  |  |
| `UCL-1.0` | `81c86c108696` | 13 | 明示 | S1 |  |  |  |  |  |  |
| `Unicode-3.0` | `f7db81051789` |  | 0 | — |  |  |  |  |  |  |
| `Unicode-DFS-2016` | `1a33fc12a3ab` |  | 0 | — |  |  |  |  |  |  |
| `Unlicense` | `0bdebfeda07d` |  | 0 | — |  |  |  |  |  |  |
| `UPL-1.0` | `2f81e75033a0` | 1 | 明示 | S3 |  |  |  |  |  |  |
| `VSL-1.0` | `435a7448a471` |  | 0 | — |  |  |  |  |  |  |
| `W3C` | `df7429635bac` | 1 | M-免責 | — |  |  |  |  |  |  |
| `W3C-20150513` | `38b688e653a9` | 1 | M-免責 | — |  |  |  |  |  |  |
| `Watcom-1.0` | `6aae307240e4` | 12 | 明示 | S1 |  |  |  |  |  |  |
| `WordNet` | `3cafea2fc628` | 1 | M-免責 | — |  |  |  |  |  |  |
| `Xnet` | `55105d933d1a` |  | 0 | — |  |  |  |  |  |  |
| `Zlib` | `bfb1112d49db` |  | 0 | — |  |  |  |  |  |  |
| `ZPL-2.0` | `f7a42094e22b` |  | 0 | — |  |  |  |  |  |  |
| `ZPL-2.1` | `3ab20c1a7550` |  | 0 | — |  |  |  |  |  |  |

### 表から数えたもの

- 行数: **141**
- 許諾の分類: `明示` **64** / `0` **59** / `M-免責` **8** / `M-方針` **7** / `選択式` **1** / `明示（不行使）` **1** / `M-留保` **1**
- `patent` の語を持つ本: **82**（うち積極的な許諾文を持つ `明示` 系: **65**・語だけ: **16**・選択式: **1**）
- `明示` 系の範囲: `S1` **58** / `S2` **3** / `S3` **4**
- `tdm` が 0 でない本: **0** / `ml`: **1** / `train`: **1** / `model`: **11** / `param`: **6** / `output`: **18** / `art4`: **2**

### 誤命中（数は立つが、概念は無い）

- `ml` の 1 件 —— `Multics`: 組織名 *"…Laboratory for Computer Science and Artificial Intelligence…"*（機械学習への言及ではない）。
- `train` の 1 件 —— `Frameworx-1.0`: *"technical or end-user support or training"*（人の研修）。
- `model` の 11 件 —— `AGPL-3.0-only`、`AGPL-3.0-or-later`、`BlueOak-1.0.0`、`CECILL-2.1`、`GPL-3.0-only`、`GPL-3.0-or-later`、`LGPL-3.0-only`、`LGPL-3.0-or-later`、`LPPL-1.3c`、`QPL-1.0`、`RPL-1.5`: 名称（*Blue Oak Model License*）・*product model*（GPL-3.0 系 §6）・*distribution model* / *open source model* / *model of licensing*・*use the text of this license as a model*（LPPL）。**機械学習のモデルを指すものは 0 件。**
- `param` の 6 件 —— `LGPL-2.0-only`、`LGPL-2.0-or-later`、`LGPL-2.1-only`、`LGPL-2.1-or-later`、`LGPL-3.0-only`、`LGPL-3.0-or-later`: *"numerical parameters, data structure layouts"*（LGPL のヘッダ閾値）。`weights` は 0 件。
- `art4` の 2 件 —— `CECILL-2.1`、`IPA`: いずれも**ライセンス自身の第 4 条**の見出し（*Article 4 - EFFECTIVE DATE AND TERM* / *Article 4 (Termination of Agreement)*）。DSM 指令 2019/790 への言及は 0 件。

## gap ごとの結論

### (a) AI 学習 / TDM の積極的な許諾（DSM 指令 4 条の opt-out を留保しないことの明示を含む）

**141 本のうち、TDM・データマイニング・機械学習・AI を名指しする本は 0 本**（`tdm` 0 件・`ml` は誤命中 1 件のみ）。
**DSM 指令 4 条 / 2019/790 / opt-out / reservation of rights を述べる本も 0 本**（`art4` の命中は全て自条番号）。

**逆側**: 0 は「許さない」ではない。*use* を無限定に許す多くの許容型は、TDM を**含む読み**が成り立つ。
gap は**許諾の不在**ではなく**明示の不在**であり、4 条の文脈では**留保しないことを機械が判定できる形で書いた本が無い**、に尽きる。
**この区別を落として「既存は AI 学習を許さない」と書いたら誤りである。**

### (b) 公有等価ツールにおける明示的な特許許諾

- `0BSD` —— `patent` **0** 回（sha256 `e3f18c71e10d`）
- `MIT-0` —— `patent` **0** 回（sha256 `59746d6285ff`）
- `Unlicense` —— `patent` **0** 回（sha256 `0bdebfeda07d`）
- `WTFPL` —— **承認済み集合に入っていない**（SPDX の `isOsiApproved` が偽）。ゆえに本 census の対象外。`CC0-1.0` も同様に対象外。

**3 本とも特許の語を 1 回も使わない** ——`comparison.md` §1.97 の結論（条件ゼロの 3 本は特許について 1 語も述べない）を、
同じ取得物の別の測り方で**再現した**。

**逆側（同じ重さで）**: **「許容型 ＋ 明示特許許諾」は既に在る。** 条件ゼロではないだけである:

- `BSD-2-Clause-Patent`: *"hereby grants to those receiving rights under this license a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except for failure to satisfy the conditions of this license) patent…"*
- `BlueOak-1.0.0`: *"Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license."*
- `UPL-1.0`: *"and any and all patent rights owned or freely licensable by each licensor hereunder covering either (i) the unmodified Software as contributed to or provided by such licensor, or (ii) the Larger Works (as defined below), to deal in both (a) the Software, and (b) any piece of software and/or hardware listed in the lrgrwrks.txt file if one is included with…"*

**gap は「公有等価」と「明示特許」の連言にしか無い。** 片方ずつなら既存が満たす。
**審査者が「BlueOak を使えばよい」と言うのは正当な反論であり**、その答えは特許ではなく条件（通知保持の有無）の側にある。

### (c) 特許（その他の権利）の許諾が、学習済みモデル・パラメータ・出力に及ぶこと

**モデル・パラメータ・重みを名指しする許諾は 0 本**（`model` 11 件・`param` 6 件は全て誤命中）。
`明示` 系 65 本の範囲は `S1` 58 / `S2` 3 / `S3` 4 で、**大半は作品（または寄与）とその寄与時点の組合せに閉じている**。代表形:

- `Apache-2.0`: *"where such license applies only to those patent claims licensable by such Contributor that are necessarily infringed by their Contribution(s) alone or by combination of their Contribution(s) with the Work to which such…"*
- `MPL-2.0`: 許諾は *"under Patent Claims infringed by Covered Software in the absence of its Contributions"* には及ばない（§2.3）。
- `AFL-3.0`: *"under patent claims owned or controlled by the Licensor that are embodied in the Original Work as furnished by the Licensor, for the…"*

**逆側（不利な材料）**:

1. **作品を超える対象を名指す許諾は既に在る**（`S3` 4 本）:
   - `UPL-1.0`: *"permission is hereby granted to any person obtaining a copy of this software, associated documentation and/or data (collectively the "Software"), free of charge and under…"* ——**data を対象に含め**、特許は `lrgrwrks.txt` に列挙した Larger Works にも及ぶ。
   - `CERN-OHL-S-2.0`: *"each Licensor hereby grants to You a perpetual, worldwide, non-exclusive, no-charge, royalty-free, irrevocable (except as stated in subsections 7.2 and 8.4) patent license to Make, have Made, use, offer to sell, sell, import, and otherwise transfer the Covered Source and Products, where such…"* ——そして Product の定義は *"'Product' means any device, component, work or physical object, whether in finished or intermediate form, arising from the use, application or processing of Covered Source."*。**定義に *work* と *processing* が入っているので、Covered Source で学習したモデルを Product と読むことを本文は排除しない。** **(c) に対する最も強い反例候補**で、ACD との差は**名指しの有無・条件（Product を渡すとき Notice への到達を求める P の §4）・報復条項（P の §6.2 / S・W の §7.2）**に縮む。
2. **出力をライセンスの外に置く規定は古くから在る**（`output` 18 件のうち実質的なもの）:
   - `GPL-3.0-only` §2: *"The output from running a covered work is covered by this License only if the output, given its content, constitutes a covered work. This…"*
   - `GPL-2.0-only` §0: *"the output from the Program is covered only if its contents constitute a work based on the Program (independent of having been made by…"*
   - `Artistic-1.0` §6 / `OGTSL` §6: *"The scripts and library files supplied as input to or produced as output from the programs of this Package do not automatically fall under the copyright of this Package, but belong…"*
   ——**ACD-1.0 §6.4 の「出力は縛られない」は新規の発想ではない。** 新しいのは対象（学習済みモデル・パラメータ）を名指したことだけである。
3. **行為を無限定に許す特許許諾**（`S2`）: `BlueOak-1.0.0` の *everything with this software* は、学習という行為を**文言上排除しない**。**(c) の gap は「モデルという対象の名指し」であって「学習という行為の許諾」ではない。**
4. **`CAL-1.0` は出力を*義務*の側で扱う**: *""User Data" means any data that is an input to or an output from the Work"* ——出力を**名指す承認済みライセンスは在り**、それは許諾ではなく**受領者のデータ返還義務**の定義である。

### 補助 —— データベース権（sui generis）

3 gap の外だが、ドシエの比較表（`submission-reference.md` §2 の 0BSD 表・CAL-1.0 段落）が依拠している軸なので同じ取得物で当てた。

- `sui generis` / `database right(s)` / `96/9`（EU データベース指令）を含む本: **0**
- `database(s)` の語を含む本: **3**（`OLFL-1.3`、`PostgreSQL`、`WordNet`）——**データベース権を名指しする本は無い**。`OLFL-1.3` は作品を *"use it in databases, data networks and online services"* する利用態様の列挙、`PostgreSQL` は製品名。**ただし `WordNet` は *"Permission to use, copy, modify and distribute this software and database"* とデータベースそのものを許諾対象に含む** ——権利の種類は名指さないが、**承認済みライセンスが既にデータベースを対象としている**ことは我々に不利な事実として記録する。
- 種類を名指さずに非著作権の権利へ届く文言を持つ本: **2**（`CAL-1.0`、`CAL-1.0-Combined-Work-Exception`・*"non-patent intellectual property laws of any jurisdiction"*）——`submission-reference.md` §2 が「この点で最も近い」として既に論じている当の本で、**全数で当てても他に無かった**。

**逆側**: 0 は「及ばない」ではない。*deal in the Software without restriction*（MIT-0）のような無限定の文言がデータベース権に及ぶ読みは成り立つ。主張できるのは**名指しの不在**だけである。

## 我々に不利な材料（まとめ）

1. **(b) は連言でしか立たない。** 許容型 ＋ 明示特許は `BSD-2-Clause-Patent` / `BlueOak-1.0.0` / `UPL-1.0` が既に持つ。
2. **(c) の構造には先例がある。** 作品から作られたもの（定義上 *work* を含み、モデルに届く読みが成り立つ）へ特許を及ぼす型（CERN-OHL の Products）と、出力を外に置く型（GPL 系 / Artistic-1.0 系）。
3. **(a) の 0 は明示の 0 であって許諾の 0 ではない。** 無限定の *use* が TDM を含む読みは成り立つ。
4. **判定は人が読んだ。** 分類 `M-*` の 16 本と `選択式` 1 本は読んで決めたもので、**別の読み手は `CECILL-2.1` の不行使約束を `明示` に入れない**かもしれない。
5. **語の 0 は英語の語の 0 である。** 非英語の本文（`comparison.md` §1.97 が 18 本と数えた）では、**同じ概念を別の語で述べている可能性を排除していない**。

## 拾う側へ（このファイルから再利用できるもの）

- **提出文・入口ページで gap を述べるとき**の、全数で下支えされた 1 文:
  > *Of the 141 OSI-approved, non-deprecated licenses (SPDX list 3.29.0), none names text and data mining, machine learning, trained models, or model parameters; the three that impose no conditions (0BSD, MIT-0, Unlicense) do not use the word "patent".*
  **この文と対で必ず置く逆側**: *Permissive licenses with an express patent grant already exist (BSD-2-Clause-Patent, BlueOak-1.0.0, UPL-1.0); the gap is the conjunction, not either half.*
- **「出力の扱いは新しくない」を先に認める**（GPL-3.0 §2 / Artistic-1.0 §6）——審査者が引く前に引く。
- **CERN-OHL の Products 条項**は (c) の最も近い先例。**提出参考資料 `submission-reference.md` §2 と入口 `REVIEWERS.md` へは 2026-09-25 に還元済み**（「承認済みライセンスでモデルに届く特許許諾は無い」とは書かず、「モデルを名指しするものは無い」に狭めた）。`against.md` / `comparison.md` への登録は各所有者の判断に委ねる。
- **再現**: 上の正規表現と `licenses.json` の版数があれば、誰でも同じ表を作り直せる。**数が違ったら、それは我々の誤りか、リストの版の差である。**
