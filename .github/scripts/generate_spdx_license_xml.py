#!/usr/bin/env python3
"""
generate_spdx_license_xml.py — ACD-1.0 の SPDX 提出用 XML を **本文から生成** する。

実行: python3 .github/scripts/generate_spdx_license_xml.py
出力: LICENSES/ACD-1.0.spdx.xml

## なぜ生成にするのか

SPDX License List への収録が受理されると、提出者は **XML とテストテキストの作成を手伝う**
ことを求められる。その XML を手書きすると、**ライセンス本文を改善するたびに XML が silent に
古くなる** —— しかも XML は普段誰も読まないので、drift に気付く経路が無い。
これは本リポジトリが繰り返し潰してきた「宣言はあるが実態が伴わない」class そのもの。

そこで **`LICENSES/ACD-1.0.txt` を単一ソースとして XML を導出**し、Check 445 が
「再生成して一致するか」を BLOCKING で検証する (STATUS.md に対する Check 121 と同じ設計)。
本文を直したら `npm run spdx-xml` を叩くだけで提出物が追従する。

## SPDX の schema

    <SPDXLicenseCollection xmlns="http://www.spdx.org/license">
      <license isOsiApproved="..." licenseId="..." name="...">
        <crossRefs><crossRef>...</crossRef></crossRefs>
        <notes>...</notes>
        <text>
          <titleText><p>...</p></titleText>
          <p>...</p>
        </text>
      </license>
    </SPDXLicenseCollection>

`<optional>` / `<alt>` によるマッチング緩和は**使わない**。ACD-1.0 は
「識別子は一つの固定テキストを指す」(§16.4) と定めており、変異を許す表現は
その設計と矛盾するため。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

if sys.version_info < (3, 10):
    # check_repository_consistency.py 等と同様 3.10+ 専用 (PEP 604 の `str | None` を使う)。
    # guard が無いと Python 3.9 で cryptic な TypeError になる (Check 104 が強制)。
    print("ERROR: generate_spdx_license_xml.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "LICENSES" / "ACD-1.0.txt"
OUT = ROOT / "LICENSES" / "ACD-1.0.spdx.xml"
LICENSE_DECL = ROOT / "LICENSE"


def _meta() -> tuple[str, str, str]:
    """LICENSE (適用宣言) から識別子と canonical URL を導出する。

    Check 444 と同じ単一ソースを使う —— 決め打ちすると、path を変えたときに
    生成器だけが古い場所を指す。
    """
    text = LICENSE_DECL.read_text(encoding="utf-8")
    m_spdx = re.search(r"SPDX-License-Identifier:\s*(\S+)", text)
    m_path = re.search(r"^Full text:\s*(\S+)$", text, re.M)
    if not (m_spdx and m_path):
        raise SystemExit("ERROR: LICENSE から SPDX 識別子 / Full text path を導出できない")
    url = f"https://yutapr0117-design.github.io/portfolio/{m_path.group(1)}"
    return m_spdx.group(1), url, m_path.group(1)


def _blocks(body: str) -> list[str]:
    """空行区切りの段落へ分割する (行内の折り返しは 1 段落に畳む)。

    ライセンス本文は 79 桁で折り返してあるが、XML では段落が意味単位なので
    改行を空白へ潰す。ただし**条項番号で始まる行は新しい段落**として扱う
    (`  3.1  ...` のような番号が段落頭に来ないと、条項の境界が失われる)。
    """
    out: list[str] = []
    cur: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped:
            if cur:
                out.append(" ".join(cur))
                cur = []
            continue
        # 条項番号 / 節見出し / 小項目は新しい段落を開始する。
        # [FIX 2026-08-23] 判定を **インデント込み**にした。従来は行を strip してから番号
        #   パターンを見ていたため、**折り返しの継続行がたまたま番号で始まる**と新段落として
        #   切られ、**1 つの文が 2 つの <p> に割れていた** (実測 3 箇所。例: §16.5 の
        #   「…and Section」/「10.5 applies.」、§5.2(c) の「…narrower than Section」/
        #   「15.1 requires it to be read.」)。SPDX はテキスト照合なので、提出物が文を壊すのは
        #   体裁の問題では済まない。本文は桁揃えが厳密 (条項 = indent 2 / 節見出し = 0 /
        #   小項目 = 7 / 継続行 = それより深い) なので、インデントで確実に判別できる。
        _ind = len(line) - len(line.lstrip())
        _is_start = (
            (_ind == 0 and re.match(r"^\d+\.\s+[A-Z]", stripped))
            or (_ind == 2 and re.match(r"^\d+\.\d+\s", stripped))
            or (_ind == 7 and re.match(r"^\([a-z]\)\s", stripped))
        )
        if _is_start and cur:
            out.append(" ".join(cur))
            cur = []
        cur.append(stripped)
    if cur:
        out.append(" ".join(cur))
    return out


def _standard_header(src: str) -> str:
    """§16.1 が定める通知文を **本文から導出**して standardLicenseHeader 用に整形する。

    SPDX ツールはこの要素で「ソースファイルに書かれた通知」を照合する。§16.2 は
    「識別子・SPDX タグ・名称による参照で十分な通知になる」と述べているので、その通知が
    **機械に認識されなければ宣言が届かない** —— ライセンス本文だけ登録して header を
    省くと、識別子タグは拾えても散文の通知は拾えない。

    `<location of this file>` は適用ごとに変わるので `<alt>` で可変部として表す。これは
    §16.4 (本文を改変して同名で配布しない) と衝突しない —— **header は Work に添える通知
    であって、この Dedication の本文ではない** (§16.5 が両者を分けている)。
    """
    # [FIX 2026-08-24] 通知文の抽出を**インデント由来**にした。従来は行頭の文字列
    #   ("This work" / "(ACD-1.0)" / "Full text:" / "SPDX-License") をハードコードした
    #   リストで絞っており、§16.1 に行を足すと **silent に落ちた** (実測: 「Machine learning
    #   … a patent licence is granted.」を足したら header から消え、Check 445e は 3 つの
    #   マーカー存在しか見ないので緑のままだった)。本文では通知ブロックだけが
    #   **条項本文より深くインデント**されている (条項継続 = 7 / 通知 = 11) ので、
    #   そこから導出すれば行を足しても落ちない。
    i = src.index("16.1 To apply this Dedication")
    block = src[i:src.index("16.2", i)]
    raw = [l.strip() for l in block.splitlines()
           if l.strip() and (len(l) - len(l.lstrip())) >= 11]
    # 79 桁の折り返しを論理単位へ畳む (本文側と同じ規律 —— **折り返しを段落境界にしない**)。
    # 新しい論理単位が始まるのは "Full text:" と "SPDX-License-Identifier:" の 2 つだけ。
    notice: list[str] = []
    for l in raw:
        if notice and not l.startswith(("Full text:", "SPDX-License-Identifier:")):
            notice[-1] += " " + l
        else:
            notice.append(l)
    out = []
    for l in notice:
        if l.startswith("Full text:"):
            out.append('      <p>Full text: <alt match=".+" name="fullTextLocation">'
                       '&lt;location of this file&gt;</alt></p>')
        else:
            out.append(f"      <p>{escape(l)}</p>")
    return "\n".join(out)


def build() -> str:
    spdx_id, url, _rel = _meta()
    src = SRC.read_text(encoding="utf-8")

    title = src.splitlines()[0].strip()
    version_line = next(l.strip() for l in src.splitlines()[1:] if l.strip())
    # SPDX の name は版数まで含めるのが慣例 (例: "Creative Commons Zero v1.0 Universal")。
    # 識別子側は ACD-1.0 なので、name も "…… 1.0" まで書かないと一覧で版が判らない。
    full_name = f"{title} {version_line.split()[-1]}"

    # 本文は PREAMBLE 以降すべて (preamble は informative だが SPDX のテキスト一致は
    # file 全体で行われるので、落とすと提出テキストと配布テキストが食い違う)
    i = src.index("PREAMBLE")
    body = src[i:]

    paragraphs = "\n".join(
        f"        <p>{escape(p)}</p>" for p in _blocks(body)
    )
    header = _standard_header(src)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!--
  自動生成 — 手で編集しないこと。
  単一ソース: LICENSES/ACD-1.0.txt
  再生成    : npm run spdx-xml   (= python3 .github/scripts/generate_spdx_license_xml.py)
  同期強制  : Check 445 (BLOCKING) が「再生成して一致するか」を検証する
-->
<SPDXLicenseCollection xmlns="http://www.spdx.org/license">
  <license isOsiApproved="false" licenseId="{escape(spdx_id)}" name="{escape(full_name)}">
    <crossRefs>
      <crossRef>{escape(url)}</crossRef>
    </crossRefs>
    <notes>
      A zero-condition public dedication written for works that are meant to be learned
      from. It differs from existing dedications in three operative respects: it grants an
      express patent licence (section 8), it affirmatively permits text and data mining and
      machine learning and declines to make any reservation (section 6), and it makes the
      recipient's permissions independent of whether copyright subsists in machine-generated
      material (section 9). Not submitted to OSI at the time of this entry.
    </notes>
    <standardLicenseHeader>
{header}
    </standardLicenseHeader>
    <text>
      <titleText>
        <p>{escape(title)}</p>
      </titleText>
      <p>{escape(version_line)}</p>
{paragraphs}
    </text>
  </license>
</SPDXLicenseCollection>
"""


def main() -> int:
    xml = build()
    changed = not OUT.exists() or OUT.read_text(encoding="utf-8") != xml
    if "--check" in sys.argv:
        if changed:
            print("ERROR: LICENSES/ACD-1.0.spdx.xml が本文と同期していない — `npm run spdx-xml`")
            return 1
        print("OK: SPDX XML は本文と同期している")
        return 0
    OUT.write_text(xml, encoding="utf-8")
    print(f"{'regenerated' if changed else 'unchanged'}: {OUT.relative_to(ROOT)} "
          f"({len(xml.splitlines())} 行)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
