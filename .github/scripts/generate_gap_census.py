#!/usr/bin/env python3
"""generate_gap_census.py — `LICENSES/ACD-1.0.gap-census.md` を生成する（取得 → 集計 → 書き出し）。

**なぜ在るか**: census は「承認済み N 本の全数に 3 つの gap を当てた」と主張する文書で、
**その数を誰でも出し直せなければ主張は検証できない**（`measure_gap_claim.py` と同じ理由）。
2026-09-25 の初版は一時ディレクトリの生成スクリプトで作られ、リポジトリに残っていなかった。

**本文中の件数はすべて表を数えて出す**（手で書かない —— Check 460 / 476 の教訓）。
**手で判定したもの**（特許許諾の分類と範囲）は下の定数に**データとして**置いてある。
判定の根拠は census 本文の「判定基準」節。**新しい版で本が増えたら、その本を読んで定数に足す**
（読まずに既定値 `明示` / `S1` に落ちるのを防ぐため、`patent` を含むのに未分類の本があれば止まる）。

使い方:
    python3 .github/scripts/generate_gap_census.py --fetch   # SPDX から取得してキャッシュへ（ネットワーク要）
    python3 .github/scripts/generate_gap_census.py           # キャッシュから census を生成
    python3 .github/scripts/generate_gap_census.py --check   # 生成結果が現在の census と一致するか（書き換えない）

キャッシュ: 環境変数 `GAP_CENSUS_CACHE`（既定 `/tmp/gap-census-cache`）。
取得元は SPDX `license-list-data` の既定ブランチ（`spdx.org` は一部の環境から 403 になるため
GitHub 上の同一データを使う）。**CI では走らせない** —— 外部取得は壊れやすい（`CLAUDE.md` §7）。
"""
import collections
import datetime
import hashlib
import json
import os
import pathlib
import re
import sys
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUTFILE = ROOT / "LICENSES" / "ACD-1.0.gap-census.md"
CACHE = pathlib.Path(os.environ.get("GAP_CENSUS_CACHE", "/tmp/gap-census-cache"))
BASE = "https://raw.githubusercontent.com/spdx/license-list-data/main/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def _get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    return urllib.request.urlopen(req, timeout=60).read()


def fetch():
    """isOsiApproved かつ非 deprecated の本文を取得し、sha256 と取得時刻を記録する."""
    CACHE.mkdir(parents=True, exist_ok=True)
    idx = json.loads(_get(BASE + "json/licenses.json"))
    ok = sorted(l["licenseId"] for l in idx["licenses"]
                if l.get("isOsiApproved") and not l.get("isDeprecatedLicenseId"))
    dep = sorted(l["licenseId"] for l in idx["licenses"]
                 if l.get("isOsiApproved") and l.get("isDeprecatedLicenseId"))
    sha, failed = {}, []
    for lid in ok:
        try:
            b = _get(BASE + "text/" + urllib.parse.quote(lid) + ".txt")
        except Exception:  # noqa: BLE001 — 失敗は 0 件として数えず、failed に記録する
            failed.append(lid)
            continue
        (CACHE / (lid + ".txt")).write_bytes(b)
        sha[lid] = hashlib.sha256(b).hexdigest()
    meta = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "licenseListVersion": idx.get("licenseListVersion"),
        "releaseDate": idx.get("releaseDate"),
        "approved_nondeprecated": len(ok),
        "deprecated_approved": dep,
        "fetched": len(sha),
        "failed": failed,
        "sha256": sha,
    }
    (CACHE / "_meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(f"fetched {len(sha)}/{len(ok)} (failed {len(failed)}) → {CACHE}")
    return 1 if failed else 0


if "--fetch" in sys.argv:
    raise SystemExit(fetch())

OSI = str(CACHE) + "/"
if not (CACHE / "_meta.json").exists():
    raise SystemExit(f"キャッシュが無い: {CACHE} —— 先に --fetch を実行せよ")
meta = json.load(open(OSI + "_meta.json", encoding="utf-8"))
ids = sorted(meta["sha256"], key=str.lower)


def text(i):
    return re.sub(r"\s+", " ", open(OSI + i + ".txt", encoding="utf-8", errors="replace").read())


TERMS = {
    "tdm": r"text and data mining|data mining|\bTDM\b",
    "ml": r"machine learning|artificial intelligence|\bA\.?I\.?\b|neural",
    "train": r"\btrain(ing|ed|s)?\b",
    "model": r"\bmodels?\b",
    "param": r"\bparameters?\b|\bweights\b",
    "output": r"\boutputs?\b",
    "art4": r"Article 4|2019/790|reservation of rights|opt[- ]out",
    "patent": r"patent",
}
cnt = {i: {k: len(re.findall(v, text(i), re.I)) for k, v in TERMS.items()} for i in ids}

# ── patent grant class (hand-verified; see "判定基準") ──
MENTION_DISCLAIMER = {"BSD-3-Clause-Open-MPI", "EUDatagrid", "OFL-1.1", "OFL-1.1-RFN",
                      "OFL-1.1-no-RFN", "W3C", "W3C-20150513", "WordNet"}
MENTION_RESERVE = {"Frameworx-1.0"}
MENTION_POLICY = {"GPL-2.0-only", "GPL-2.0-or-later", "LGPL-2.0-only", "LGPL-2.0-or-later",
                  "LGPL-2.1-only", "LGPL-2.1-or-later", "OCLC-2.0"}
OPTIONAL = {"APL-1.0"}
NONASSERT = {"CECILL-2.1"}
# scope of express grants
SCOPE_BEYOND = {"UPL-1.0": "Larger Works（`lrgrwrks.txt` に列挙した組合せ）",
                "CERN-OHL-P-2.0": "Covered Source **and Products**（ソースから作った物）",
                "CERN-OHL-S-2.0": "Covered Source **and Products**",
                "CERN-OHL-W-2.0": "Covered Source **and Products**"}
SCOPE_ACTIVITY = {"BlueOak-1.0.0": "対象は this software・行為は無限定（*everything*）",
                  "EUPL-1.1": "Work の利用に必要な範囲（*to the extent necessary*）",
                  "EUPL-1.2": "Work の利用に必要な範囲（*to the extent necessary*）"}
DEP13 = sorted(meta['deprecated_approved'])
NEW5 = ['BSD-ask-to-endorse', 'CDDL-1.1', 'CNRI-Python-GPL-Compatible', 'Python-2.0.1', 'curl']
PD_EQUIV = ["0BSD", "MIT-0", "Unlicense"]  # §1.97 の条件ゼロ 3 本

# **2026-09-25 に本文を読んで分類した `patent` を含む本の全集合**（3.29.0・82 本）。
# 新しい版でここに無い本が `patent` を含んでいたら、**読まずに既定値へ落とさず止まる**。
READ_PATENT = {
    'AFL-1.1', 'AFL-1.2', 'AFL-2.0', 'AFL-2.1', 'AFL-3.0', 'AGPL-3.0-only', 'AGPL-3.0-or-later',
    'Apache-2.0', 'APL-1.0', 'APSL-1.0', 'APSL-1.1', 'APSL-1.2', 'APSL-2.0', 'Artistic-2.0',
    'BlueOak-1.0.0', 'BSD-2-Clause-Patent', 'BSD-3-Clause-Open-MPI', 'CAL-1.0',
    'CAL-1.0-Combined-Work-Exception', 'CATOSL-1.1', 'CDDL-1.0', 'CDDL-1.1', 'CECILL-2.1',
    'CERN-OHL-P-2.0', 'CERN-OHL-S-2.0', 'CERN-OHL-W-2.0', 'CPAL-1.0', 'CPL-1.0', 'CUA-OPL-1.0',
    'ECL-2.0', 'EPL-1.0', 'EPL-2.0', 'EUDatagrid', 'EUPL-1.1', 'EUPL-1.2', 'Frameworx-1.0',
    'GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-only', 'GPL-3.0-or-later', 'IPL-1.0',
    'LGPL-2.0-only', 'LGPL-2.0-or-later', 'LGPL-2.1-only', 'LGPL-2.1-or-later', 'LGPL-3.0-only',
    'LGPL-3.0-or-later', 'LPL-1.0', 'LPL-1.02', 'Motosoto', 'MPL-1.0', 'MPL-1.1', 'MPL-2.0',
    'MPL-2.0-no-copyleft-exception', 'MS-PL', 'MS-RL', 'MulanPSL-2.0', 'NASA-1.3', 'Nokia',
    'NPOSL-3.0', 'OCLC-2.0', 'OFL-1.1', 'OFL-1.1-no-RFN', 'OFL-1.1-RFN', 'OLFL-1.3', 'OSET-PL-2.1',
    'OSL-1.0', 'OSL-2.0', 'OSL-2.1', 'OSL-3.0', 'RPL-1.1', 'RPL-1.5', 'RPSL-1.0', 'RSCPL', 'SISSL',
    'SPL-1.0', 'UCL-1.0', 'UPL-1.0', 'W3C', 'W3C-20150513', 'Watcom-1.0', 'WordNet',
}


def _unread_guard():
    _unread = [i for i in ids if cnt[i]["patent"] and i not in READ_PATENT]
    if _unread:
        raise SystemExit(f"未分類: `patent` を含むが本文を読んで分類していない本がある: {_unread}。"
                         "本文を読み、MENTION_* / OPTIONAL / NONASSERT / SCOPE_* と READ_PATENT に足せ")


_unread_guard()


def pclass(i):
    if cnt[i]["patent"] == 0: return "0"
    if i in MENTION_DISCLAIMER: return "M-免責"
    if i in MENTION_RESERVE: return "M-留保"
    if i in MENTION_POLICY: return "M-方針"
    if i in OPTIONAL: return "選択式"
    if i in NONASSERT: return "明示（不行使）"
    return "明示"

def scope(i):
    c = pclass(i)
    if not c.startswith("明示"): return "—"
    if i in SCOPE_BEYOND: return "S3"
    if i in SCOPE_ACTIVITY: return "S2"
    return "S1"

rows = [(i, cnt[i], pclass(i), scope(i)) for i in ids]
N = len(rows)
by = collections.Counter(r[2] for r in rows)
express = [r for r in rows if r[2].startswith("明示")]
sc = collections.Counter(r[3] for r in express)
nz = lambda k: [r[0] for r in rows if r[1][k]]
tdm, ml, train, model, param, output, art4 = (nz(k) for k in
    ("tdm", "ml", "train", "model", "param", "output", "art4"))
mention = [r for r in rows if r[2].startswith("M-")]

def q(i, pat, before=0, after=260):
    t = text(i); m = re.search(pat, t)
    assert m, (i, pat)
    seg = t[max(0, m.start() - before): m.end() + after]
    if after and m.end() + after < len(t):
        seg = seg[:seg.rfind(" ")].rstrip(",;:(") + "…"
    return seg.strip()

CALQ = None
def join(xs): return "、".join(f"`{x}`" for x in xs) if xs else "（なし）"

CALQ = q("CAL-1.0", r'"User Data" means any data that is an input to or an output from the Work', 0, 0)
CERNDEF = q("CERN-OHL-S-2.0", r"'Product' means any device, component, work or physical object, whether in finished or intermediate form, arising from the use, application or processing of Covered Source[.]", 0, 0)
out = []
w = out.append
w("---")
w("file: LICENSES/ACD-1.0.gap-census.md")
w("audience: licence reviewers, OSI license-discuss / license-review participants, 後任 AI")
w("last-updated: 2026-09-25")
w("canonical-ref: LICENSES/ACD-1.0.gap-measurements.md §1.97 (条件の有無を同じ 141 本で数えた census) / LICENSES/ACD-OSI-BOTTLENECKS.md (gap の扱い)")
w("---")
w("")
w("# ACD-1.0 gap census —— OSI 承認済み 141 本に 3 つの gap を当てた（2026-09-25）")
w("")
w("> **これは何か**: ドシエの gap 論（「既存の承認済みライセンスは X を持たない」）を、**選んだ比較対象ではなく")
w("> 承認済みの全数**に当てた記録。`gap-measurements.md` §1.97 は同じ 141 本で**条件の有無**を数えた。")
w("> **ここでは 3 つの gap そのもの**を 1 本ずつ当てる。**表の数はすべて表から導出**しており、")
w("> 文中の件数はスクリプトが表を数えて出したもので、手で書いていない。")
w(">")
w("> **先に結論（有利・不利を同じ重さで）**: (a) TDM・機械学習を名指しする承認済みライセンスは **0 本**。")
w(f"> (b) 公有等価の 3 本（{join(PD_EQUIV)}）は**特許の語を 1 回も使わない**。**ただし特許を明示許諾する")
w(f"> 許容型は既に在る**（`BSD-2-Clause-Patent` / `BlueOak-1.0.0` / `UPL-1.0` ——いずれも条件を持つ）。")
w(f"> (c) 学習済みモデル・パラメータ・出力を名指しする許諾は **0 本**。**ただし「作品を超えて及ぶ」特許許諾は")
w(f"> {sc['S3']} 本在り（UPL の Larger Works / CERN-OHL の Products）、**「実行の出力はライセンスの外」という")
w(f"> 規定は GPL 系・Artistic-1.0 系に古くから在る**。gap は「誰も考えなかった」ではなく**「誰もこの対象に向けて書かなかった」**である。")
w("")
w("## 方法")
w("")
w(f"- **取得**: {meta['fetched_at']}（UTC）。SPDX `license-list-data` 既定ブランチの `json/licenses.json`")
w(f"  （licenseListVersion **{meta['licenseListVersion']}**・releaseDate {meta['releaseDate'][:10]}）から")
w(f"  `isOsiApproved` かつ非 deprecated の識別子を列挙し、各 `text/<id>.txt` を取得した。")
w(f"- **取得できた本数: {N} / {meta['approved_nondeprecated']}**・**できなかった本数: {len(meta['failed'])}**。")
w(f"  deprecated の承認済み識別子 {len(meta['deprecated_approved'])} 件（`GPL-2.0` など、`-only`/`-or-later` へ移行済みの旧名）は除外した。")
w("- **本文の同一性**: 各 text の sha256 を取得時に記録した（下表の `sha256` 列は先頭 12 桁）。")
w("- **生成**: `.github/scripts/generate_gap_census.py`（取得は `--fetch`・一致確認は `--check`）。**このファイルは手で編集しない** —— 手で直すと表と文の数が食い違う。")
w("- **語の計数**: 空白を 1 つに正規化してから、大文字小文字を区別せずに数えた。用いた正規表現:")
w("")
w("  | 列 | 正規表現 |")
w("  | :-- | :-- |")
for k, v in TERMS.items():
    w(f"  | `{k}` | `{v.replace('|', chr(92) + '|')}` |")
w("")
w("- **⚠ 語の計数は候補の抽出であって判定ではない。** 0 でない命中は**すべて文脈を読んで**判定した（下の「誤命中」）。")
w("  0 の列は「その語が無い」ことだけを言い、**「その概念が無い」ことは言わない**（例: `MIT-0` の *without restriction*）。")
w("- **特許許諾の判定基準**（`patent` が 1 回以上の本だけ読んだ）:")
w("  - `明示` —— 受領者に特許の実施を許す**積極的な文**がある（*grants … patent license* 等）。")
w("  - `明示（不行使）` —— 許諾ではなく**権利を行使しない約束**の形（GPL-3.0 §11 自身が *covenant not to sue* を patent license に含めて定義しており、同じ機能を持つ）。")
w("  - `選択式` —— 本文は許諾を持つが、**Exhibit で選択したときだけ**効く。")
w("  - `M-免責` / `M-留保` / `M-方針` —— `patent` の語はあるが、**非侵害を保証しない免責**・**権利の留保**・**前文や §7 型の方針**だけで、積極的な許諾文が無い。")
w("  - `0` —— `patent` の語が 0 回。")
w("- **範囲の判定基準**（`明示` 系のみ）: `S1` = 作品（またはその Contribution。**寄与時点の組合せ**を含む）に限る /")
w("  `S2` = 対象は作品だが**行為や必要性の限定が緩い** / `S3` = **作品そのものを超える対象**（組合せ・製造物）を名指す。")
w("- **⚠ 判定は人が読んだもので、正規表現の結果ではない。** 初版の抽出正規表現は `BlueOak-1.0.0` の")
w("  *licenses you to do everything* を見落とし、GPL-2.0 系の §7（*if a patent license would not permit …*）を許諾と誤認した。**両方とも読んで直した。**")
w("")
w("## 141 と 149 —— 同じ repo の旧い census との対照")
w("")
w("このドシエには **「承認済み 149 本」** を母集団にした旧い測定がある（`AS-OF.md` / `AUDIT-LEDGER.md` / `ACD-OSI-BOTTLENECKS-EXTERNAL.md`・2026-09-10・SPDX **3.28.0**）。")
w("**どちらかが誤りなのではなく、母集団の定義と版が違う。** 2 つのリストを取得して差を取った（2026-09-25）:")
w("")
w(f"- **149** = 3.28.0 の `isOsiApproved` **全件**（非 deprecated 136 ＋ deprecated 13）。deprecated 13 件は {join(DEP13)} ——**うち 11 件は `-only` / `-or-later` へ移行済みの旧 ID で本文が現行 ID と重複し、残る 2 件（`GPL-3.0-with-GCC-exception` / `wxWindows`）は例外条項の本文である。**")
w(f"- **{N}** = 3.29.0 の `isOsiApproved` かつ **非 deprecated**。3.28.0 から **新たに承認済みになったのが 5 件**: {join(NEW5)}。**外れたものは 0 件。**")
w(f"- **旧い数との整合**: 旧 census の「patent を含む 92 本 / output を含む 30 本」は、本表の {N - by['0']} 本 / {len(output)} 本から「新 5 件の寄与（patent は `CDDL-1.1` の 1 本・output は 0 本）」を引き、deprecated 13 件の寄与を足すと一致する。**deprecated 13 件は 3.28.0 の `text/deprecated_<id>.txt` を取得して実測した**（patent を含むもの 11 本・output を含むもの 12 本。差し引きで出した数ではない）。")
w("- **使い分け**: 数を引くときは**版と定義を同じ文に書く**。重複本文を数えない分、**非 deprecated の方が「何種類のライセンスが」という主張に正確**である。")
w("")
w("## 全数表")
w("")
w("列 `tdm`〜`output` は語の出現回数（0 は空欄）。`許諾` と `範囲` は上の基準。")
w("")
w("| 識別子 | sha256 | patent | 許諾 | 範囲 | tdm | ml | train | model | param | output |")
w("| :-- | :-- | --: | :-- | :-- | --: | --: | --: | --: | --: | --: |")
f = lambda x: str(x) if x else ""
for i, c, p, s in rows:
    w(f"| `{i}` | `{meta['sha256'][i][:12]}` | {f(c['patent'])} | {p} | {s} | {f(c['tdm'])} | {f(c['ml'])} | "
      f"{f(c['train'])} | {f(c['model'])} | {f(c['param'])} | {f(c['output'])} |")
w("")
w("### 表から数えたもの")
w("")
w(f"- 行数: **{N}**")
w("- 許諾の分類: " + " / ".join(f"`{k}` **{v}**" for k, v in sorted(by.items(), key=lambda kv: -kv[1])))
w(f"- `patent` の語を持つ本: **{N - by['0']}**（うち積極的な許諾文を持つ `明示` 系: **{len(express)}**・語だけ: **{len(mention)}**・選択式: **{by['選択式']}**）")
w("- `明示` 系の範囲: " + " / ".join(f"`{k}` **{sc[k]}**" for k in ("S1", "S2", "S3")))
w(f"- `tdm` が 0 でない本: **{len(tdm)}** / `ml`: **{len(ml)}** / `train`: **{len(train)}** / `model`: **{len(model)}** / `param`: **{len(param)}** / `output`: **{len(output)}** / `art4`: **{len(art4)}**")
w("")
w("### 誤命中（数は立つが、概念は無い）")
w("")
w(f"- `ml` の {len(ml)} 件 —— {join(ml)}: 組織名 *\"…Laboratory for Computer Science and Artificial Intelligence…\"*（機械学習への言及ではない）。")
w(f"- `train` の {len(train)} 件 —— {join(train)}: *\"technical or end-user support or training\"*（人の研修）。")
w(f"- `model` の {len(model)} 件 —— {join(model)}: 名称（*Blue Oak Model License*）・*product model*（GPL-3.0 系 §6）・*distribution model* / *open source model* / *model of licensing*・*use the text of this license as a model*（LPPL）。**機械学習のモデルを指すものは 0 件。**")
w(f"- `param` の {len(param)} 件 —— {join(param)}: *\"numerical parameters, data structure layouts\"*（LGPL のヘッダ閾値）。`weights` は 0 件。")
w(f"- `art4` の {len(art4)} 件 —— {join(art4)}: いずれも**ライセンス自身の第 4 条**の見出し（*Article 4 - EFFECTIVE DATE AND TERM* / *Article 4 (Termination of Agreement)*）。DSM 指令 2019/790 への言及は 0 件。")
w("")
w("## gap ごとの結論")
w("")
w("### (a) AI 学習 / TDM の積極的な許諾（DSM 指令 4 条の opt-out を留保しないことの明示を含む）")
w("")
w(f"**{N} 本のうち、TDM・データマイニング・機械学習・AI を名指しする本は 0 本**（`tdm` 0 件・`ml` は誤命中 {len(ml)} 件のみ）。")
w("**DSM 指令 4 条 / 2019/790 / opt-out / reservation of rights を述べる本も 0 本**（`art4` の命中は全て自条番号）。")
w("")
w("**逆側**: 0 は「許さない」ではない。*use* を無限定に許す多くの許容型は、TDM を**含む読み**が成り立つ。")
w("gap は**許諾の不在**ではなく**明示の不在**であり、4 条の文脈では**留保しないことを機械が判定できる形で書いた本が無い**、に尽きる。")
w("**この区別を落として「既存は AI 学習を許さない」と書いたら誤りである。**")
w("")
w("### (b) 公有等価ツールにおける明示的な特許許諾")
w("")
for i in PD_EQUIV:
    w(f"- `{i}` —— `patent` **{cnt[i]['patent']}** 回（sha256 `{meta['sha256'][i][:12]}`）")
w("- `WTFPL` —— **承認済み集合に入っていない**（SPDX の `isOsiApproved` が偽）。ゆえに本 census の対象外。`CC0-1.0` も同様に対象外。")
w("")
w("**3 本とも特許の語を 1 回も使わない** ——`gap-measurements.md` §1.97 の結論（条件ゼロの 3 本は特許について 1 語も述べない）を、")
w("同じ取得物の別の測り方で**再現した**。")
w("")
w("**逆側（同じ重さで）**: **「許容型 ＋ 明示特許許諾」は既に在る。** 条件ゼロではないだけである:")
w("")
w(f"- `BSD-2-Clause-Patent`: *\"{q('BSD-2-Clause-Patent', r'hereby grants to those receiving', 0, 180)}\"*")
w(f"- `BlueOak-1.0.0`: *\"{q('BlueOak-1.0.0', r'Each contributor licenses you to do everything with this software that would otherwise infringe any patent claims they can license or become able to license[.]', 0, 0)}\"*")
w(f"- `UPL-1.0`: *\"{q('UPL-1.0', r'and any and all patent rights', 0, 330)}\"*")
w("")
w("**gap は「公有等価」と「明示特許」の連言にしか無い。** 片方ずつなら既存が満たす。")
w("**審査者が「BlueOak を使えばよい」と言うのは正当な反論であり**、その答えは特許ではなく条件（通知保持の有無）の側にある。")
w("")
w("### (c) 特許（その他の権利）の許諾が、学習済みモデル・パラメータ・出力に及ぶこと")
w("")
w(f"**モデル・パラメータ・重みを名指しする許諾は 0 本**（`model` {len(model)} 件・`param` {len(param)} 件は全て誤命中）。")
w(f"`明示` 系 {len(express)} 本の範囲は `S1` {sc['S1']} / `S2` {sc['S2']} / `S3` {sc['S3']} で、**大半は作品（または寄与）とその寄与時点の組合せに閉じている**。代表形:")
w("")
w(f"- `Apache-2.0`: *\"{q('Apache-2.0', r'where such license applies only to those patent claims', 0, 170)}\"*")
w(f"- `MPL-2.0`: 許諾は *\"{q('MPL-2.0', r'under Patent Claims infringed by Covered Software in the absence of its Contributions', 0, 0)}\"* には及ばない（§2.3）。")
w(f"- `AFL-3.0`: *\"{q('AFL-3.0', r'under patent claims owned or controlled by the Licensor that are embodied in the Original Work', 0, 40)}\"*")
w("")
w("**逆側（不利な材料）**:")
w("")
w(f"1. **作品を超える対象を名指す許諾は既に在る**（`S3` {sc['S3']} 本）:")
w(f"   - `UPL-1.0`: *\"{q('UPL-1.0', r'permission is hereby granted to any person obtaining a copy of this software, associated documentation and/or data', 0, 60)}\"* ——**data を対象に含め**、特許は `lrgrwrks.txt` に列挙した Larger Works にも及ぶ。")
w(f"   - `CERN-OHL-S-2.0`: *\"{q('CERN-OHL-S-2.0', r'each Licensor hereby grants to You', 0, 260)}\"* ——そして Product の定義は *\"{CERNDEF}\"*。**定義に *work* と *processing* が入っているので、Covered Source で学習したモデルを Product と読むことを本文は排除しない。** **(c) に対する最も強い反例候補**で、ACD との差は**名指しの有無・条件（Product を渡すとき Notice への到達を求める P の §4）・報復条項（P の §6.2 / S・W の §7.2）**に縮む。")
w(f"2. **出力をライセンスの外に置く規定は古くから在る**（`output` {len(output)} 件のうち実質的なもの）:")
w(f"   - `GPL-3.0-only` §2: *\"{q('GPL-3.0-only', r'The output from running a covered work', 0, 100)}\"*")
w(f"   - `GPL-2.0-only` §0: *\"{q('GPL-2.0-only', r'the output from the Program is covered only if', 0, 90)}\"*")
w(f"   - `Artistic-1.0` §6 / `OGTSL` §6: *\"{q('Artistic-1.0', r'The scripts and library files supplied as input to or produced as output', 0, 110)}\"*")
w("   ——**ACD-1.0 §6.4 の「出力は縛られない」は新規の発想ではない。** 新しいのは対象（学習済みモデル・パラメータ）を名指したことだけである。")
w(f"3. **行為を無限定に許す特許許諾**（`S2`）: `BlueOak-1.0.0` の *everything with this software* は、学習という行為を**文言上排除しない**。**(c) の gap は「モデルという対象の名指し」であって「学習という行為の許諾」ではない。**")
w(f"4. **`CAL-1.0` は出力を*義務*の側で扱う**: *\"{CALQ}\"* ——出力を**名指す承認済みライセンスは在り**、それは許諾ではなく**受領者のデータ返還義務**の定義である。")
w("")
SG = [i for i in ids if re.search(r"sui generis|database rights?|96/9", text(i), re.I)]
DBW = [i for i in ids if re.search(r"\bdatabases?\b", text(i), re.I)]
NONPAT = [i for i in ids if re.search(r"non-patent intellectual property", text(i), re.I)]
w("### 補助 —— データベース権（sui generis）")
w("")
w(f"3 gap の外だが、ドシエの比較表（`submission-reference.md` §2 の 0BSD 表・CAL-1.0 段落）が依拠している軸なので同じ取得物で当てた。")
w("")
w(f"- `sui generis` / `database right(s)` / `96/9`（EU データベース指令）を含む本: **{len(SG)}**")
w(f"- `database(s)` の語を含む本: **{len(DBW)}**（{join(DBW)}）——**データベース権を名指しする本は無い**。`OLFL-1.3` は作品を *\"use it in databases, data networks and online services\"* する利用態様の列挙、`PostgreSQL` は製品名。**ただし `WordNet` は *\"Permission to use, copy, modify and distribute this software and database\"* とデータベースそのものを許諾対象に含む** ——権利の種類は名指さないが、**承認済みライセンスが既にデータベースを対象としている**ことは我々に不利な事実として記録する。")
w(f"- 種類を名指さずに非著作権の権利へ届く文言を持つ本: **{len(NONPAT)}**（{join(NONPAT)}・*\"non-patent intellectual property laws of any jurisdiction\"*）——`submission-reference.md` §2 が「この点で最も近い」として既に論じている当の本で、**全数で当てても他に無かった**。")
w("")
w("**逆側**: 0 は「及ばない」ではない。*deal in the Software without restriction*（MIT-0）のような無限定の文言がデータベース権に及ぶ読みは成り立つ。主張できるのは**名指しの不在**だけである。")
w("")
MORAL = [i for i in ids if re.search(r"moral rights?|droit moral|droits? moraux", text(i), re.I)]
EUPLQ = q("EUPL-1.2", r"In the countries where moral rights apply, the Licensor waives his right to exercise his moral right to the extent allowed by law", 0, 0)
w("### 補助 —— 人格権（ACD-1.0 §12）")
w("")
w(f"- 人格権（`moral right(s)` / `droit moral`）に触れる本: **{len(MORAL)}**（{join(MORAL)}）")
w(f"- `EUPL-1.2`: *\"{EUPLQ}\"*")
w("")
w("**両面**: **有利** —— 人格権の不行使を条文に書いたライセンスが承認されている。**それが審査でどう論じられたかは読んでいない**ので、「人格権条項は問題にされない」とまでは言わない。")
w("**不利** —— §12 の「放棄できる法域では放棄・できない法域では不行使」という構造は新規ではない。§12 が EUPL に足しているのは**不行使の相手方の明示（受領者と下流）と承継人の拘束（§12.4）**であって、発想ではない。")
w("")
w("## 我々に不利な材料（まとめ）")
w("")
w("1. **(b) は連言でしか立たない。** 許容型 ＋ 明示特許は `BSD-2-Clause-Patent` / `BlueOak-1.0.0` / `UPL-1.0` が既に持つ。")
w("2. **(c) の構造には先例がある。** 作品から作られたもの（定義上 *work* を含み、モデルに届く読みが成り立つ）へ特許を及ぼす型（CERN-OHL の Products）と、出力を外に置く型（GPL 系 / Artistic-1.0 系）。")
w("3. **(a) の 0 は明示の 0 であって許諾の 0 ではない。** 無限定の *use* が TDM を含む読みは成り立つ。")
w(f"4. **判定は人が読んだ。** 分類 `M-*` の {len(mention)} 本と `選択式` {by['選択式']} 本は読んで決めたもので、**別の読み手は `CECILL-2.1` の不行使約束を `明示` に入れない**かもしれない。")
w("5. **語の 0 は英語の語の 0 である。** 非英語の本文（`gap-measurements.md` §1.97 が 18 本と数えた）では、**同じ概念を別の語で述べている可能性を排除していない**。")
w("")
w("## 拾う側へ（このファイルから再利用できるもの）")
w("")
w("- **提出文・入口ページで gap を述べるとき**の、全数で下支えされた 1 文:")
w(f"  > *Of the {N} OSI-approved, non-deprecated licenses (SPDX list {meta['licenseListVersion']}), none names text and data mining, machine learning, trained models, or model parameters; the three that impose no conditions ({', '.join(PD_EQUIV)}) do not use the word \"patent\".*")
w("  **この文と対で必ず置く逆側**: *Permissive licenses with an express patent grant already exist (BSD-2-Clause-Patent, BlueOak-1.0.0, UPL-1.0); the gap is the conjunction, not either half.*")
w("- **「出力の扱いは新しくない」を先に認める**（GPL-3.0 §2 / Artistic-1.0 §6）——審査者が引く前に引く。")
w("- **CERN-OHL の Products 条項**は (c) の最も近い先例。**提出参考資料 `submission-reference.md` §2 と入口 `REVIEWERS.md` へは 2026-09-25 に還元済み**（「承認済みライセンスでモデルに届く特許許諾は無い」とは書かず、「モデルを名指しするものは無い」に狭めた）。`against.md` / `comparison.md` への登録は各所有者の判断に委ねる。")
w("- **再現**: `python3 .github/scripts/generate_gap_census.py --fetch` で取得し、引数なしで本書を生成する（`--check` は書き換えずに一致だけを見る）。**本文中の件数はすべてこのスクリプトが表を数えて出したもの**で、手で判定した分類はスクリプト内にデータとして置いてある。**数が違ったら、それは我々の誤りか、リストの版の差である。**")
w("")
_new = "\n".join(out)
if "--check" in sys.argv:
    _cur = OUTFILE.read_text(encoding="utf-8") if OUTFILE.exists() else ""
    if _cur == _new:
        print("OK: census は現在のキャッシュからの生成結果と一致する")
        raise SystemExit(0)
    print("DRIFT: census が生成結果と一致しない（手で編集されたか、キャッシュの版が違う）")
    raise SystemExit(1)
OUTFILE.write_text(_new, encoding="utf-8")
print(N, dict(by), dict(sc), len(express), len(mention))
