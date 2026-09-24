"""LICENSES/ 提出物そのものについての consistency Check 群.

**このファイルが分かれている理由**: `checks_license_dossier.py` が 914 行になり、
Check 52 の advisory (800) を越えた。**圧縮ではなくテーマ分割**で対処する規律に従い、
**「審査者が受け取るもの」についての Check** をここへ出した。
`checks_license_dossier.py` に残るのは**ドシエの運用記録**についての Check
（投稿先 / 索引 / 鮮度 / errata↔変更リスト / `rounds/` 在庫 / 表紙 / 発信停止）である。

**分ける基準は「対象が誰の手に渡るか」**: 提出パケットの送る文面・次版の草案・
提出対象の版への条項引用・来歴の開示は、**いずれも審査者が直接読む面**であり、
壊れたときの損害が「記録が古い」ではなく「**審査者が誤った物を読む**」である。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  463. **提出パケットの「送る文面」が、OSI が求める項目をすべて含むこと** (BLOCKING):
       `submission.md` §B.0 は**実際にメールへ貼られる ~600 語**である。OSI の
       review-process ページは提出時に 10 項目を求めるが、**2026-09-06 まで packet はそのうち
       3 件を欠いていた**（OSD 準拠の積極的言明 / ScanCode 識別子 / 提案 tag —— #77）。
       欠落の原因は「要件表を隣人の提出から再構成し、出典で読んでいなかった」ことで、
       **同じ形は静かに再発する** —— 文面は増分のたびに書き換えられ、項目は 1 つずつ落ちる。
       10 個の marker が §B.0 に存在することを機械強制する。**中身の質は検査しない**
       （それは散文の判断である）。守るのは「**項目が消えていないこと**」だけ。(BLOCKING)
       **(468g・2026-09-22)** 草案の**本文側**に `shall` / `must` が無いこと。提出パケットは
       「ACD-1.0 は measurably not proscriptive ——`shall` と `must` は **0 回**」を #116 への
       緩和として publish している。**⚠ この entry の初版は「1.0 は凍結されているので
       その性質を検査する Check は定義により発火しえない」と書いていた。誤りである（#193）** ——
       **Check 441d が ACD-1.0 に対して BLOCKING でこれを検査している。**
       **真なのは草案の側だけだった** ——441d の対象は `ACD-1.0.txt` に限られ、
       **次に提出する版を守るものは 1 つも無かった。** パターンは 441d と同じ 7 つに
       `shall` / `must` の裸形を足す ——**草案の被覆が凍結済み 1.0 の被覆より狭くてはならない。**
       **ヘッダは対象外** ——実測で草案の `must` 2 件は条文ではなく草案についての注記で、
       **file 全体で数えるとヘッダの散文が条文の性質として報告される。**
  472. **提出側の文書の `§N.M` 引用が、`SUBMISSION-TARGET` が宣言する版の条文に実在すること** (BLOCKING):
       **条番号は版をまたいで保存されない。** 1.0 の §15.5 / §15.7 / §15.8 は 1.1 以降に無く、
       §16.4〜§16.6 は番号が同じまま意味が違う。**提出対象を切り替えた瞬間に、提出物が
       「何も述べていない条」へ審査者を送る** (`against.md` #144 で一度踏んだ class で、
       **審査者が最初に確かめる種類の誤り**)。**確定手順 §0.13 はこの再写像を列挙していなかった。**
       `§N.M` は条とドシエの節の 2 系統に使われるので、**いずれかの版に条として実在する番号だけ**を見る。
       **(472b・2026-09-24)** 同じ 4 面の**逐語引用** (`*"…"*`) が、いずれかの版の本文から
       取られているなら、**提出対象の版の本文にも実在する**こと。**番号が実在しても語句が
       別の版のものなら、審査者は存在しない条文を読まされる** —— 実例: `submission-reference.md`
       §4b が ACD-1.0 の §16.4 を *"except by the Steward"* と引いていたが、その語句は 1.1 で
       入ったもので **1.0 には Steward という役割自体が無い**（`against.md` #160）。**472 は番号の
       存在しか見ないので通していた。** 引用の直前 250 字が他の版を名指しているもの
       （`1.1` / `1.2` / successor / draft / 草案）は、版を明示した引用として許す。
       **(472c・2026-09-24)** 入口ページ `REVIEWERS.md` が審査者に貼らせる検証コマンドの**期待値**
       （sh ブロックのコメント `→ expect N` / `→ N× OK`）が、**実際に実行した結果と一致する**こと。
       `grep` で始まるコマンドだけを実行する。#190 は同じページの期待値が実行結果と食い違っていた件を
       手で直したが、**機械で照合する層が無かった**。さらに 2026-09-24、置換テキストの検査が
       `<[a-z]+>` で**複数語の雛形 `<location of this file>` を拾えず 0 を返していた** ——
       **期待値が合っていても、測り方が対象を見ていないことがある。** 472c が守るのは前者だけで、
       後者は正規表現を広げて直した（期待値 1）。
  468. **次版の草案が、自分が何であるかを述べ、内部的に健全であること** (BLOCKING): 2026-09-10 に
       オーナーが「現行は保持、次版を作って改善し続けるのは問題ない」と述べたので
       次版の草案 (**現在は `LICENSES/ACD-1.2-DRAFT.txt`**) を置いた。**草案は確定版と紛らわしい** —— 同じ書式・同じ節見出しで、
       条番号だけが §1（定義の並べ替え・E13）と §15 以降でずれている。**読み手が取り違えると、凍結中の提出物について
       誤った条番号を引くことになる。** 3 つを強制する: **(a)** 冒頭が **NOT IN FORCE /
       NOT SUBMITTED / NOT APPLIED** を述べること、**(b)** 純 ASCII・節が連番・`Section N.M` の
       参照がすべて実在すること（**1.0 について §4c が測っている性質を、草案でも同じ形で保つ**）、
       **(c)** 冒頭が申告する語数・条数が実測と一致すること。**(c) が要るのは、本日 6 回
       「数えられるものを、数える前に書いた」からである。**
       **468d は別の危険を見る** —— **この instrument が新規である理由は §6 / §8.4 / §9 の 3 点**
       であり（register B10）、**次版で「短くする」圧力がかかったとき最初に削られうるのがここである。**
       §6 と §9 は 1.0 と等価であること、§8.4 は射程語（model / parameter set / weight /
       embedding / output）が残っていることを求める。**正当な改訂は止めず、静かな喪失だけを止める。**
       **468e は「まだ open な errata」の宣言を errata の現物と照合し、468f は冒頭が主張する
       「1.1 との同一性」をすぐ下の変更一覧と照合する** ——**どちらも「やることリストは項目を
       消化した瞬間に古くなり、消化しているその瞬間こそ一覧を見ていない」class** で、
       468f は **2026-09-22 に外部の AI レビューが見つけた** (`against.md` #207)。 (BLOCKING)
  473. **来歴の開示が、否定の半分だけで現れないこと** (BLOCKING): steward は
       *"the drafting was not directed by me, **but the direction of the licence was mine**"*
       と述べており、2026-09-14 (#125) に開示を**両方の半分を持つ形**へ訂正した。
       **にもかかわらず、短い写しを載せている面は列挙されなかった** —— 2026-09-22 の実測で
       **`LICENSE`・入口 2 面（#187）に続き、`submission.md` §B.0（実際に送る本文そのもの）と
       Q10 の日英 2 面（#189）**が否定の半分だけを述べていた。**同じ族の 4 回目**
       （#66 送る文面に開示が無い / #67 採用者が開く `LICENSE` に無い / #125 / #187）なので、
       per-instance をやめて構造で縛る。**開示を薄める向きではなく、*人間の関与を過少に述べる*
       向きの誤り**であり、moderator が AI の関与度をまさに問うている最中 (B14) に最も不利である。
       **検出器の設計が本体である**（今日 3 回外した）: (1) **行の折り返しを潰す** ——
       `I did\nnot commission` は素の正規表現では一致しない。(2) **`>` の引用マーカーを剥がす**
       —— 剥がさないと `the direction of the licence\n> was mine` が語として繋がらない。
       (3) **段落粒度で見る** —— file 粒度の集合演算は、**訂正済みの写しと未訂正の写しを
       同じ file に持つ**場合を必ず取り逃がす（`submission.md` が実例で、#187 はこれで
       「一覧は 3 項目」と誤って完全性を主張した）。(BLOCKING)
"""
import json
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 463. 提出パケットの「送る文面」が OSI の要求項目をすべて含むこと (BLOCKING) ──────
    # §B.0 は**実際に貼られる文面**で、§B.1 以降は貼らない参考資料である。#77 で 3 件の欠落を
    # 埋めたが、**文面は増分のたびに書き換えられる**ので、同じ欠落は静かに再発する。
    # marker の存在だけを見る —— 中身の質は散文の判断であって Check の仕事ではない。
    # **`_L460` に依存しない。** それは Check 460 の分岐内で定義される名前で、本 Check は
    # 460 より前に走る。他の Check の局所名を借りると、順序を変えた瞬間に NameError で
    # suite ごと止まる —— それは「Check が働いた」ではなく「Check が一度も走らなかった」
    # である（#885 と同型）。実際、初版はそれで落ちた。
    _sb463 = ROOT / "LICENSES" / "ACD-1.0.submission.md"
    if _sb463.exists():
        _t463 = _sb463.read_text(encoding="utf-8")
        _i463 = _t463.find("### B.0 The message as it should actually be sent")
        _j463 = _t463.find("### B.1 Reference material", _i463 + 1) if _i463 >= 0 else -1
        _bad463 = []
        if _i463 < 0 or _j463 < 0:
            _bad463.append("§B.0 / §B.1 の見出しが見つからない (送る文面と参考資料の境界が失われている)")
        else:
            _b0 = _t463[_i463:_j463]
            _req463 = [
                ("attachment", r"attached as plain text"),
                ("OSD affirmation", r"I affirm that ACD-1\.0 complies with the Open Source Definition"),
                # **要件は「OSD に準拠する」ではなく「OSD 3, 5, 6, 9 を満たすと specifically 明言する」**。
                # 原文: "Affirmatively state that the license complies with the Open Source Definition,
                # including specifically affirming it meets OSD 3, 5, 6 and 9."
                # 一般的な準拠宣言だけでは要件を満たさない。2026-09-07 に Carlo Piana 氏が別の提出に対し
                # 「required information が無いので**解決するまでコメントしない**」と述べており
                # (`against.md` #97)、欠落は議論の遅れではなく**議論の不成立**を招く。
                ("OSD 3/5/6/9 specific", r"OSD 3\*\*[\s\S]{0,400}?OSD 5 and OSD 6\*\*[\s\S]{0,400}?OSD 9\*\*"),
                ("projects using it", r"Approved or Used by Projects"),
                ("steward contact", r"Steward:.*@"),
                ("name and version", r"License Name:"),
                # **2026-09-13 追加。** 要件リストを原典で 1 項目ずつ突き合わせたら、
                # *"Provide **any additional information** … For example, approval of the license by
                # **Debian, the FSF or the Fedora Project** would be relevant"* だけが §B.0 で
                # 答えられていなかった (#77 と同じ形 —— 原典で読んで初めて出る欠落)。
                # **我々の答えは「無い」なので、書き落としても文面は自然に読める** ——
                # だから機械で縛る (`review-precedents.md` §1.76)。
                ("third-party endorsement", r"Third-party Endorsement:"),
                ("SPDX / ScanCode", r"SPDX / ScanCode Identifier"),
                ("proposed tags", r"Proposed Tags:"),
                ("gap statement", r"\*\*The gap\.\*\*"),
                ("nearest approved licences", r"\*\*Nearest approved licences\.\*\*"),
                # **2026-09-13 追記（この項目を足した理由の裏付け）。** 委員長は BOS Public License の
                # 提出に対し、欠けている項目のうち**この 1 件だけを名指しして**
                # *"in particular do not skip 'Describe any legal review the license has been
                # through, including whether it was drafted by a lawyer.'"* と述べている (2026-07-23)。
                # **我々の最大の弱点そのものを述べる項目なので、書き落とす方向の圧力が構造的にある。**
                # 実測: この行を "**Legal review status.**" へ変えると Check 463 が RED になる
                # (`review-precedents.md` §1.75)。
                ("legal review", r"\*\*Legal review: none\.\*\*"),
            ]
            _miss463 = [_n for _n, _r in _req463 if not re.search(_r, _b0, re.M)]
            if _miss463:
                _bad463.append(f"§B.0 に OSI 要求項目が欠けている: {_miss463}")
        check(
            not _bad463,
            # **件数は導出する（2026-09-13 是正）。** ここは長らく「11 項目」とリテラルで書かれており、
            # **項目を足しても OK メッセージは 11 のままだった** —— Check 460 が他所で禁じている
            # 「自己申告の件数が実測とずれる」を、**Check 自身の成功メッセージでやっていた。**
            # 成功メッセージは読み手が最も信用する場所なので、ここでの drift は最も悪い。
            f"Check 463: 送る文面 (§B.0) が OSI の要求 {len(_req463)} 項目をすべて含む",
            (f"Check 463: {_bad463}。要件の単一ソースは "
             "https://opensource.org/licenses/review-process。**§B.0 は実際にメールへ貼られる文面**で、"
             "§B.1 以降は貼らない参考資料である。#77 で 3 件の欠落を埋めたが、文面は増分のたび"
             "書き換えられるので同じ欠落は静かに再発する"),
            blocking=True,
        )

    # ── 472. 提出側の文書の条項引用が、提出対象の版に実在すること (BLOCKING) ──────────────
    #   **条番号は版をまたいで保存されない。** 1.0 の §15.5 / §15.7 / §15.8 は 1.1 以降に無く、
    #   §16.4〜§16.6 は番号が同じまま意味が違う。**提出対象を切り替えた瞬間に、提出物が
    #   「何も述べていない条」へ審査者を送る。** `against.md` #144 で一度踏んだ class で、
    #   **審査者が最初に確かめる種類の誤り**である。
    #   **確定手順 (§0.13) はこの再写像を列挙していなかった** —— 列挙は、列挙した時点で
    #   見えていたものしか含まない（Check 464 / 469(b) / 468e と同じ形で本日 2 度目）。
    #   単一ソースは `submission.md` の `SUBMISSION-TARGET` marker。**そこを変えれば残りは CI が指す。**
    _sub472 = ROOT / "LICENSES" / "ACD-1.0.submission.md"
    if _sub472.exists():
        _st472 = _sub472.read_text(encoding="utf-8")
        _m472 = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", _st472)
        if not _m472:
            check(False, "",
                  "Check 472: `submission.md` に SUBMISSION-TARGET marker が無い "
                  "(値は `ACD-<版>`。提出対象が宣言されていないと、条項引用をどの版に対して"
                  "照合すべきか決まらない)",
                  blocking=True)
        else:
            _ver472 = _m472.group(1)
            _txt472 = ROOT / "LICENSES" / (
                f"{_ver472}.txt" if (ROOT / "LICENSES" / f"{_ver472}.txt").exists()
                else f"{_ver472}-DRAFT.txt")
            if not _txt472.exists():
                check(False, "",
                      f"Check 472: SUBMISSION-TARGET が {_ver472} を指すが本文が無い "
                      f"({_txt472.name})",
                      blocking=True)
            else:
                _body472 = _txt472.read_text(encoding="utf-8")
                _sep472 = "-" * 80
                if _sep472 in _body472:
                    _body472 = _body472.split(_sep472, 1)[1]
                _have472 = set(re.findall(r"^  (\d+\.\d+) ", _body472, re.M))
                # **`§N.M` は 2 つの採番体系に使われている** —— ライセンスの条と、ドシエの節
                # (`§1.96` / `§3.6` など。`§1.xx` は file をまたぐ共有系列で Check 471(f) が担当)。
                # **どちらか判らない番号を条として扱うと誤検出になる**ので、
                # **「いずれかの版に条として実在する番号」だけを条項引用とみなす。**
                # ドシエの節番号はどの版の条にも無いので自然に外れ、
                # **版をまたいで消えた条 (1.0 の §15.7 など) は残る** —— 見たいのはそれである。
                _universe472 = set(_have472)
                for _other472 in sorted((ROOT / "LICENSES").glob("ACD-*.txt")):
                    _ot = _other472.read_text(encoding="utf-8")
                    if _sep472 in _ot:
                        _ot = _ot.split(_sep472, 1)[1]
                    _universe472 |= set(re.findall(r"^  (\d+\.\d+) ", _ot, re.M))
                # 提出側の面だけを見る。分析・記録の面は 1.0 について述べるのが正しい。
                _faces472 = ["ACD-1.0.submission.md", "ACD-1.0.submission-reference.md",
                             "REVIEWERS.md", "ACD-1.0.objection-map.md"]
                _bad472 = []
                for _rel472 in _faces472:
                    _p472 = ROOT / "LICENSES" / _rel472
                    if not _p472.exists():
                        continue
                    _cited = set(re.findall(r"§\s?(\d{1,2}\.\d{1,2})",
                                            _p472.read_text(encoding="utf-8")))
                    _miss = sorted(_c for _c in _cited
                                   if _c in _universe472 and _c not in _have472)
                    if _miss:
                        _bad472.append(f"{_rel472}: {_miss}")
                check(
                    not _bad472,
                    f"Check 472: 提出側 {len(_faces472)} 面の条項引用が {_ver472} に実在する",
                    (f"Check 472: 提出対象 ({_ver472}) に存在しない条を引いている面がある: {_bad472}。"
                     "**条番号は版をまたいで保存されない** —— 1.0 の §15.5 / §15.7 / §15.8 は "
                     "1.1 以降に無く、§16.4〜§16.6 は番号が同じまま意味が違う。"
                     "**提出物が「何も述べていない条」へ審査者を送るのは、最初に確かめられる種類の誤りである** "
                     "(`against.md` #144)。SUBMISSION-TARGET を切り替えたら引用も写像せよ "
                     "(対応表は `ACD-1.1-CHANGELIST.md` の条項対応節)"),
                    blocking=True,
                )

                # ── 472b. 提出側の逐語引用が、提出対象の版の本文に実在すること ────────────────
                #   472 は**番号の存在**しか見ない。§16.4 は 1.0 にも 1.1 にも在るので、
                #   1.1 の語句 *"except by the Steward"* を 1.0 の §16.4 として引いても通った
                #   (`against.md` #160)。**番号が一致し語句が別の版のもの**という形を捕まえる。
                #   本文から取られていない引用（リストの発言など）はどの版にも無いので対象外になる。
                def _norm472(_t):
                    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", _t)).strip().lower()
                _tgt472 = _norm472(_txt472.read_text(encoding="utf-8"))
                _vers472 = {}
                for _vp472 in sorted((ROOT / "LICENSES").glob("ACD-*.txt")):
                    _vers472[_vp472.name] = _norm472(_vp472.read_text(encoding="utf-8"))
                _qbad472 = []
                _nq472 = 0
                _marked472 = 0
                for _rel472 in _faces472:
                    _p472 = ROOT / "LICENSES" / _rel472
                    if not _p472.exists():
                        continue
                    _raw472 = _p472.read_text(encoding="utf-8")
                    for _mq in re.finditer(r'\*"([^"\n]{12,400})"\*', _raw472):
                        _parts = [_x.strip() for _x in re.split(r"…|\.\.\.", _mq.group(1))
                                  if len(_x.strip()) >= 12]
                        if not _parts:
                            continue
                        _np = [_norm472(_x) for _x in _parts]
                        _from = [_n for _n, _vt in _vers472.items() if all(_x in _vt for _x in _np)]
                        if not _from:
                            continue
                        _nq472 += 1
                        if all(_x in _tgt472 for _x in _np):
                            continue
                        _pre = _raw472[max(0, _mq.start() - 250):_mq.start()]
                        if re.search(r"1\.[1-9](?!\d)|successor|draft|草案|次版", _pre, re.I):
                            _marked472 += 1
                            continue
                        _ln = _raw472.count("\n", 0, _mq.start()) + 1
                        _qbad472.append(f"{_rel472}:{_ln} *\"{_mq.group(1)[:60]}\"* ({'/'.join(_from)} にだけ在る)")
                check(
                    not _qbad472,
                    (f"Check 472b: 提出側 {len(_faces472)} 面の本文逐語引用 {_nq472} 件のうち "
                     f"{_nq472 - _marked472} 件が {_ver472} の本文に実在し、"
                     f"{_marked472} 件は他の版を明示して引いている"),
                    (f"Check 472b: 提出対象 ({_ver472}) の本文に無い語句を、版を示さずに引いている: {_qbad472}。"
                     "**番号は両方の版に在っても、語句は別の版のものでありうる** —— "
                     "審査者は存在しない条文を読まされる (`against.md` #160)。"
                     "提出対象の版の語句で引き直すか、直前で版を明示せよ"),
                    blocking=True,
                )

    # ── 472c. 入口ページの検証コマンドの期待値が、実行結果と一致すること ─────────────────
    #   審査者は「コピーして貼るだけ」のコマンドを最も信用する。その期待値が実行結果と違えば、
    #   正しいテキストを前にして「改変されている」と読ませる (#190)。grep 始まりだけを実行する。
    _rv472c = ROOT / "LICENSES" / "REVIEWERS.md"
    if _rv472c.exists():
        import subprocess as _sp472c
        _bad472c, _n472c = [], 0
        for _blk in re.findall(r"```sh\n(.*?)```", _rv472c.read_text(encoding="utf-8"), re.S):
            _lines = _blk.split("\n")
            for _k, _ln in enumerate(_lines):
                _me = re.search(r"→\s*(?:expect\s+(\d+)|(\d+)×\s*OK)", _ln)
                if not (_ln.lstrip().startswith("#") and _me):
                    continue
                _cmd = next((_c.strip() for _c in _lines[_k + 1:]
                             if _c.strip() and not _c.lstrip().startswith("#")), "")
                if not _cmd.startswith("grep "):
                    continue
                _cmd = _cmd.replace("shasum -a 256 -c", "sha256sum -c")
                _out = _sp472c.run(_cmd, shell=True, cwd=str(ROOT), capture_output=True,
                                   text=True).stdout
                _n472c += 1
                if _me.group(1) is not None:
                    _got = _out.strip()
                    if _got != _me.group(1):
                        _bad472c.append(f"{_cmd[:60]} → 期待 {_me.group(1)} / 実行 {_got!r}")
                else:
                    _ok = sum(1 for _o in _out.splitlines() if _o.rstrip().endswith(": OK"))
                    if _ok != int(_me.group(2)):
                        _bad472c.append(f"{_cmd[:60]} → 期待 {_me.group(2)}× OK / 実行 {_ok}× OK")
        check(
            _n472c > 0 and not _bad472c,
            f"Check 472c: REVIEWERS.md の検証コマンド {_n472c} 本の期待値が実行結果と一致",
            (f"Check 472c: 入口ページの検証コマンドの期待値が実行結果と違う: {_bad472c or '照合できたコマンドが 0 本'}。"
             "**審査者はこれを貼って結果を比べる** —— 食い違えば、正しいテキストを前に改変を疑わせる (#190)"),
            blocking=True,
        )

    # ── 468. 次版の草案が自分を述べ、内部的に健全であること (BLOCKING) ─────────────────────
    #   草案は 1.0 と書式が同じで、条番号だけ §15 以降がずれている。**取り違えは実害を生む**
    #   (凍結中の提出物について誤った条番号を引く)。だから「自分が何か」を本文に述べさせる。
    _dr468 = ROOT / "LICENSES" / "ACD-1.2-DRAFT.txt"
    if _dr468.exists():
        _t468 = _dr468.read_text(encoding="utf-8")
        _bad468 = []
        for _phrase in ("NOT IN FORCE", "NOT SUBMITTED", "NOT APPLIED"):
            if _phrase not in _t468:
                _bad468.append(f"冒頭に {_phrase!r} が無い (草案は自分の身分を述べること)")
        _na468 = sum(1 for _b in _dr468.read_bytes() if _b > 127)
        if _na468:
            _bad468.append(f"非 ASCII が {_na468} バイトある (1.0 の §4c が測る性質を草案でも保つ)")
        _sep468 = "-" * 80
        _lic468 = _t468.split(_sep468, 1)[1] if _sep468 in _t468 else _t468
        _secs468 = [int(_m) for _m in re.findall(r"^(\d+)\. [A-Z]", _lic468, re.M)]
        if _secs468 != list(range(1, len(_secs468) + 1)):
            _bad468.append(f"節番号が連番でない: {_secs468}")
        _cl468 = set(re.findall(r"^  (\d+\.\d+) ", _lic468, re.M))
        _refs468 = set(re.findall(r"Sections?\s+(\d+\.\d+)", _lic468))
        _dang468 = sorted(_r for _r in _refs468 if _r not in _cl468)
        if _dang468:
            _bad468.append(f"解決しない参照: {_dang468} (**行をまたぐ参照は素の置換では当たらない**)")

        # ── 468g. 草案の**本文側**に義務語 (`shall` / `must`) が現れないこと ─────────────
        # WHY: 提出パケットは「ACD-1.0 は measurably not proscriptive —— `shall` と `must` は
        #   **0 回**」を #116 への緩和として publish している。
        #   **⚠ 初版のこのコメントは「1.0 は凍結されているのでその性質を検査する Check は
        #   定義により発火しえない」と書いていた。誤りである（#193）** ——**Check 441d が
        #   ACD-1.0 に対して BLOCKING でまさにこれを検査している。** 凍結は byte を守るが、
        #   441d は 1.0 が凍結される前から在り、いまも走っている。
        #   **真なのは草案の側だけだった**: 441d の対象は `ACD-1.0.txt` に限られ、
        #   **次に提出する版を守るものは 1 つも無かった。**
        #   パターンは 441d と同じ 7 つに、`shall` / `must` の裸形を足したものにしてある ——
        #   **草案の被覆が、凍結された 1.0 の被覆より狭くてはならない。**
        # ⚠ **射程を正直に書く（2026-09-22 の vacuity 掃引で実測）**: この face は**綴りで見る**ので、
        #   *"did not **steer** the drafting"* のような**同義語の言い換えは素通りする**（実測で確認）。
        #   **同義語を投機的に足さないのは、開示文が steward 本人の言葉として固定されており、
        #   言い換えが現れる経路が無いからである。** 経路ができたら（例えば要約文を別に置くなら）
        #   そのときに広げる。**「広げなかった」ことと「見ている」ことを混同しない。**
        # ⚠ **ヘッダは対象外**である —— 実測 (2026-09-22) で草案の `must` 2 件はどちらも
        #   「1.0 への引用は 1.0 の本文を使うこと」等の**草案についての注記**で、条文ではない。
        #   `_lic468`（セパレータ以降）で見るのはそのためで、**file 全体で数えると
        #   ヘッダの散文が条文の性質として報告される。**
        _pat468g = (r"\b(shall|must)\b", r"You are required\b", r"provided that\b",
                    r"on condition\b", r"You agree\b", r"You may not\b")
        _deon468 = sorted({_m.group(0).lower()
                           for _p in _pat468g
                           for _m in re.finditer(_p, _lic468, re.I)})
        if _deon468:
            _bad468.append(
                f"本文側に義務語がある: {_deon468} "
                "(#116 の緩和は「shall と must は 0 回」を測った値に依っている。"
                "1.0 は凍結が守るが、草案は誰も守らない)")
        _mw468 = re.search(r"This draft: ([\d,]+) words, (\d+) clauses", _t468)
        if not _mw468:
            _bad468.append("冒頭に語数/条数の申告が無い (消して黙らせない)")
        else:
            _dw468 = int(_mw468.group(1).replace(",", ""))
            _dc468 = int(_mw468.group(2))
            _aw468 = len(_lic468.split())
            _ac468 = len(_cl468)
            if _dw468 != _aw468:
                _bad468.append(f"語数: 申告 {_dw468} / 実測 {_aw468}")
            if _dc468 != _ac468:
                _bad468.append(f"条数: 申告 {_dc468} / 実測 {_ac468}")
        # ── 468f. 草案ヘッダの箇条書きが壊れていないこと ─────────────────────────────
        #   **468 は区切り線より*後*（ライセンス本文）しか読まない。** 語数も条数も ASCII も
        #   参照の解決も、すべて本文についての検査である。**区切り線より前の編集用ヘッダは、
        #   どの Check も一度も読んでいなかった。**
        #   **2026-09-20 に実害**: 同日の reflow で `* A new Section 15.5 restores …` が
        #   **`* w Section 15.5 restores …` に化けた**（`block[len('    * '):]` が、既に
        #   空白正規化されて `* A new …` で始まる文字列から 6 文字を削り、`* A ne` を落とした）。
        #   **`npm run verify` は緑のまま**で、**その状態の草案が外部レビュー 2 件へ渡った。**
        #   **ヘッダは「この草案が何であるか」を読み手に説明する唯一の面**であり、
        #   本文と同じ重みで壊れてはならない。
        #   **検査は最小の字面規約 1 つに絞る** ——英文の箇条書きは大文字か数字で始まる。
        #   意味は見ない（見ようとすると brittle gate になる・§2.9 の線）。
        _headbad468 = []
        _head468 = _t468.split(_sep468, 1)[0] if _sep468 in _t468 else ""
        for _hm468 in re.finditer(r"^\s*\* (.+)$", _head468, re.M):
            _first468 = _hm468.group(1).strip()
            if not _first468[:1].isupper() and not _first468[:1].isdigit():
                _headbad468.append(_first468[:48])
        if _headbad468:
            _bad468.append(f"ヘッダの箇条書きが大文字/数字で始まっていない: {_headbad468}")

        # ── 468d. gap を担う条項が successor でも生き残っていること ──────────────────────
        #   **この instrument が新規である理由は §6 / §8.4 / §9 の 3 点である** (register B10)。
        #   **次版で「短くする」圧力がかかったとき、最初に削られうるのがここである** ——
        #   実際 B3 の測定は「機構部だけを削る」と明記しているが、**明記は強制ではない。**
        #   §6 と §9 は 1.0 と byte 等価 (空白正規化後) であることを求める。
        #   **§8.4 は 2026-09-10 に因果の限定 (E15) を入れたので等価ではない** ——
        #   代わりに **gap の核となる語** (model / parameter set / weight / embedding / output) が
        #   すべて残っていることを見る。**正当な改訂を止めず、静かな喪失だけを止める。**
        _10_468 = ROOT / "LICENSES" / "ACD-1.0.txt"
        if _10_468.exists():
            _t10 = _10_468.read_text(encoding="utf-8")
            _draft_lic = _t468.split(_sep468, 1)[1] if _sep468 in _t468 else _t468

            def _sec468(_txt, _n):
                _m = re.search(r"^%d\. [A-Z].*?(?=^\d+\. [A-Z])" % _n, _txt, re.M | re.S)
                return re.sub(r"\s+", " ", _m.group(0)).strip() if _m else ""

            # **byte 等価では厳しすぎる。** 2026-09-11 に E4 (§6.4 の "is not encumbered" →
            # "no enforceable claim arises") で実際に発火した —— **記録済みの欠陥を直す正当な改訂**
            # まで止めてしまう。守りたいのは**文面の同一性ではなく gap の生存**なので、
            # **各 gap 条項が担っている中身を marker で見る**形へ変えた。
            # **marker は「その条項が何をするか」を一言で表す語句**であり、言い回しを変えても残る。
            _lost468 = []
            _markers468 = {
                6: ["Computational Use of the Work is expressly permitted",
                    "without condition",
                    "makes no Reservation",
                    "expressly declines to make one",
                    "withdraws it and disclaims reliance",
                    "no permission at all"],
                9: ["makes no representation that any right subsists",
                    "asserts no right in Machine-Generated Material",
                    "are not required to determine",
                    "depends on that"],
            }
            for _n468, _ms468 in _markers468.items():
                _sec_txt468 = _sec468(_draft_lic, _n468)
                for _mk468 in _ms468:
                    if _mk468 not in _sec_txt468:
                        _lost468.append(f"§{_n468} から gap の中身が消えている: {_mk468!r}")
            for _kw468 in ("model", "parameter set", "weight", "embedding", "output"):
                if _kw468 not in _draft_lic.lower():
                    _lost468.append(f"§8.4 の gap 語 {_kw468!r} が草案から消えている")
            check(
                not _lost468,
                "Check 468d: gap を担う条項 (§6 / §9 / §8.4 の射程語) が successor でも生きている",
                (f"Check 468d: 次版で gap が失われている: {_lost468}。**この instrument が新規である"
                 "理由は §6 / §8.4 / §9 の 3 点であり、短くする圧力がかかったとき最初に削られうるのが"
                 "ここである。** 意図的に変えるなら `ACD-1.1-CHANGELIST.md` に記録し、"
                 "**register B10 の主張も同時に書き換えること**"),
                blocking=True,
            )

        # ── 468e: 草案が宣言する「まだ open な errata」が、errata の現物と一致すること ────
        # Check 468 は語数・条数・参照の解決を見るが、**草案が自分の*状態*について述べる文**は
        # 見ていなかった。実測 (2026-09-14): preamble の status block が
        # 「Still open in this draft, deliberately: E11 / E13 / E15 / E16」と述べ、
        # **4 件とも errata では閉じていた** —— E13 は 2026-09-10、E15 は 09-11、E16 は 09-13 から
        # 誤っており、**4 日間、提出される文書が自分の状態について偽の宣言を持っていた**。
        # **しかも「They are not oversights」と*意図的である*ことまで主張していた** ——
        # 直した項目について「わざと残した」と述べるのは、単に古いより悪い。
        # **これは「やることリストは、項目を消化した瞬間に古くなる」class の最も外へ出る面である**
        # (Check 469 が CHANGELIST について守っているのと同じ invariant を、**本文側**で守る)。
        _st468 = re.search(r"Still open in this draft[^:]*:(.*?)(?:cost\.|\n\n)", _t468, re.S)
        if _st468 is None:
            _bad468.append("preamble に「Still open in this draft」の宣言が無い "
                           "(宣言しないなら本 face を外すこと。黙って消さない)")
        else:
            _declared468 = set(re.findall(r"\bE\d+\b", _st468.group(1)))
            _erp468 = ROOT / "LICENSES" / "ACD-1.0.errata.md"
            if _erp468.exists():
                _ert468 = _erp468.read_text(encoding="utf-8")
                _openset468 = set()
                for _ln468 in _ert468.splitlines():
                    _m468 = re.match(r"\|\s*\*{0,2}(E\d+)\*{0,2}\s*\|", _ln468)
                    if not _m468:
                        continue
                    # **「確定手順へ回した」は「閉じた」ではない。** E10 は 1.1 の descriptor が
                    # 存在しないので*ここでは*閉じられないだけで、欠陥としては残っている。
                    # 初版はこれを closed 扱いにし、**本 face が導入直後に自分の誤りを指摘した。**
                    # **版番号を決め打ちしない。** 1.1 を確定させた時点で作業場は 1.2 へ移り、
                    # **1.2 で閉じた entry が「まだ open」と読まれた**（2026-09-18 に実際に発火）。
                    if re.search(r"\d+\.\d+ 草案で閉じた", _ln468):
                        continue
                    _openset468.add(_m468.group(1))
                if _declared468 != _openset468:
                    _bad468.append(
                        f"preamble の「Still open」が errata と食い違う: "
                        f"宣言のみ {sorted(_declared468 - _openset468)} / "
                        f"errata のみ {sorted(_openset468 - _declared468)}")

        # ── 468h: 版ごとの機械可読 descriptor が、この instrument の*唯一の制限*を述べること ──
        #   **`against.md` #59 / errata E10。** `reservationsAndLimits` は「しないこと」を 6 つ
        #   並べる一方、**この文書が現に持つ 1 つの制限**（改変テキストを名称・識別子の下で
        #   頒布しないこと・§16.4）に key が無かった。**descriptor だけを読む消費者は
        #   「何も制限しない」と結論する** ——著作物については真で、テキストについては偽である。
        #   **§6.5 の理由は両刃**（自動化システムが判定できない制限は、知らずに破られる）。
        #   1.1 では `reservationsAndLimits.textRedistribution` で閉じた。
        #   ⚠ **E10 は「版ごとに閉じ直す」種類**なので、**新しい版の descriptor を作る瞬間が
        #   再発の瞬間である。** そこを機械で押さえる。
        #   ⚠ **`ACD-1.0.machine.json` は対象外** —— **凍結された欠陥そのもの**であり
        #   （Check 453 が byte を pin している）、直すことは凍結の趣旨に反する。
        _desc468h = [p for p in sorted((ROOT / "LICENSES").glob("ACD-*.machine.json"))
                     if p.name != "ACD-1.0.machine.json"]
        _bad468h = []
        for _d in _desc468h:
            try:
                _j = json.loads(_d.read_text(encoding="utf-8"))
            except Exception as _e:
                _bad468h.append(f"{_d.name}: JSON として読めない ({type(_e).__name__})")
                continue
            _r = _j.get("reservationsAndLimits")
            if not isinstance(_r, dict):
                _bad468h.append(f"{_d.name}: reservationsAndLimits が無い")
                continue
            _tr = _r.get("textRedistribution")
            if not isinstance(_tr, dict):
                _bad468h.append(f"{_d.name}: textRedistribution が無い "
                                "(§16.4 —— この文書が現に持つ唯一の制限)")
            elif str(_tr.get("clause", "")) != "16.4":
                _bad468h.append(f"{_d.name}: textRedistribution.clause が "
                                f"{_tr.get('clause')!r} (16.4 であること)")
        if _bad468h:
            _bad468.append(f"descriptor が唯一の制限を述べていない: {_bad468h}")

        # ── 468f: 草案の冒頭が主張する「1.1 との同一性」が、すぐ下の変更一覧と整合すること ──
        # **2026-09-22 に外部の AI レビューが見つけた** (`against.md` #207)。status block が
        # *"It is at present identical to ACD-1.1 apart from the version number and the
        # identifiers that name it"* と述べたまま、**すぐ下に E22〜E30 の 9 件が並び、同じ
        # ヘッダが 5,051→5,207 語・78→80 条と申告していた。**
        # **468c は申告した数を守り、468e は open な errata の一覧を守っていたが、
        # 「自分は前版と同一である」という文だけは、どの face も見ていなかった。**
        # 害は文言ではない ——`ACD-1.1-SELF-AUDIT.md` の同一性監査が **この文を根拠として引いて
        # おり**、偽になった文の上に「§16.2 の変更は宣言済み」という結論が載っていた。
        # **⚠ 片側だけ禁じない。** 変更一覧が空のときに同一性の主張を*消して*黙らせるのも
        # 同じ drift なので、両向きで要求する（空なら述べよ・空でないなら述べるな）。
        _hdr468f = _t468.split(_sep468, 1)[0] if _sep468 in _t468 else _t468
        _blk468f = re.search(r"Changes in this draft[^:]*:(.*?)(?:\n  Still open|\Z)",
                             _hdr468f, re.S)
        if _blk468f is None:
            _bad468.append("冒頭に「Changes in this draft」の一覧が無い "
                           "(空でも見出しは残すこと。消して黙らせない)")
        else:
            # 末尾の語数・条数 bullet は変更ではないので数えない。
            _items468f = [_b for _b in re.findall(r"^    \* (.*)$", _blk468f.group(1), re.M)
                          if not re.search(r"words, \d+ clauses", _b)]
            _claim468f = re.search(r"is (?:at present )?identical to ACD-1\.\d", _hdr468f)
            if _items468f and _claim468f:
                _bad468.append(
                    f"冒頭が「1.1 と同一」と述べているのに変更一覧に {len(_items468f)} 件ある "
                    f"({_claim468f.group(0)!r})。**同一性の主張は一覧が空のときだけ真である。** "
                    "一覧に項目が在るなら「下に列挙した変更と版数識別子を除いて 1.1 の本文である」"
                    "の形にすること (`against.md` #207)")
            if not _items468f and not _claim468f:
                _bad468.append(
                    "変更一覧が空なのに、冒頭が 1.1 との同一性を述べていない。"
                    "**空であることは黙っていてよい理由ではない** ——読み手には "
                    "「まだ変えていない」と「記録が無い」の区別がつかない")

        check(
            not _bad468,
            f"Check 468: 次版草案が自分を述べ内部的に健全 ({len(_cl468)} 条 / {len(_lic468.split())} 語)",
            (f"Check 468: 次版草案に問題がある: {_bad468}。**草案は 1.0 と書式が同じで条番号だけ"
             "ずれているので、取り違えると凍結中の提出物について誤った条番号を引くことになる。**"
             "自分が何であるかを本文に述べ、1.0 について測っている性質を同じ形で保つこと"),
            blocking=True,
        )

    # ── 473. 来歴の開示が、否定の半分だけで現れないこと (BLOCKING) ─────────────────────
    # WHY: steward 本人の言葉は 2 つの半分から成る ——
    #   *"the drafting was not directed by me, but the direction of the licence was mine"*。
    #   2026-09-14 (#125) に開示を訂正したが、**短い写しを載せている面は列挙されなかった**。
    #   2026-09-22 に 5 段落が否定の半分だけを述べており、その中に
    #   **実際に送る本文 (§B.0)** と **不利な一覧の来歴 entry (#5)** が入っていた。
    #   誤りの向きは「AI をより自律的に見せる」側で、B14 の最中に最も不利である。
    # 検出器の設計 (今日 3 回外したので、外し方を実装に残す):
    #   (1) 行の折り返しを潰す —— `I did\nnot commission` は素の正規表現に当たらない。
    #   (2) `>` の引用マーカーを剥がす —— 剥がさないと語が繋がらない。
    #   (3) **段落粒度**で見る —— file 粒度の集合演算は、訂正済みと未訂正の写しを
    #       同じ file に持つ場合を必ず取り逃がす (#187 がこれで完全性を誤主張した)。
    _NEG473 = re.compile(
        r"(did not (ask for|commission|direct)|not commissioned or directed"
        r"|not directed by me|指示してもいない|起草に関与していない)", re.I)
    _DIR473 = re.compile(
        r"(direction of the licen[cs]e was (mine|his)|direction was (mine|his)"
        r"|involved in determining the direction|nonetheless his|方向づけ)", re.I)
    # この欠陥そのものを記録している段落は対象外。記録を禁じると、
    # **欠陥の記録が Check に消される**という逆向きの害が出る (#977 と同じ線引き)。
    _META473 = re.compile(r"(#18[5-9]|#12[45]|#6[67]|訂正|corrected|初版|BLIND|旧文|Check 473)")
    _SUBJ473 = re.compile(r"(drafting|drafted|起草|licen[cs]e|ライセンス)", re.I)

    def _norm473(s):
        s = re.sub(r"(?m)^\s*>+\s?", "", s)   # (2) 引用マーカー
        return re.sub(r"\s+", " ", s)          # (1) 折り返し

    # ⚠ **初版はここで ctx の `read()` を呼び、module に bind されていないので NameError を投げ、
    #    それを裸の `except Exception: continue` が握り潰して 79 file すべてを読み飛ばした。**
    #    **動機となった欠陥を戻しても GREEN のまま**で、非 vacuity 検証だけがそれを教えた
    #    （`BLIND-SPOTS.md`「crash は grep をすり抜ける」の 2 例目）。
    #    **対処は 2 つとも要る**: (i) 未 bind の名前に依存せず Path から直接読む、
    #    (ii) **例外を握り潰さない** ——読めない file は数え、0 件でないなら RED にする。
    _paths473 = sorted(
        list((ROOT / "LICENSES").glob("*.md"))
        + list((ROOT / "docs" / "files" / "LICENSES").glob("*.md"))
        + [ROOT / "LICENSE"]
    )
    _files473 = [str(q) for q in _paths473]
    _bad473 = []
    _unread473 = []
    for _q473 in _paths473:
        try:
            _t473 = _q473.read_text(encoding="utf-8")
        except Exception as _e473:          # (ii) 握り潰さない
            _unread473.append(f"{_q473.name}: {type(_e473).__name__}")
            continue
        _f473 = str(_q473)
        for _para473 in re.split(r"\n\s*\n|\n(?=\| )", _t473):   # (3) 段落粒度
            _p473 = _norm473(_para473)
            if not _NEG473.search(_p473):
                continue
            if not _SUBJ473.search(_p473):
                continue
            if _META473.search(_p473):
                continue
            if _DIR473.search(_p473):
                continue
            _bad473.append(f"{_f473.split('portfolio/')[-1]}: {_p473.strip()[:90]}")

    # ── 473b: 2026-09-23 に事実として否定された文が、現在形の言明として残らないこと ────────
    # **`against.md` #216。** steward の 2026-09-14 の手紙（`rounds/2026-09-15-…round3.txt`）は
    # *"I then told the AI that I wanted my own license to aim for external approval …
    # I gave the goal, and the AI generated and developed the license"* と述べており、
    # **我々が 8 日間 publish していた「人間は作る判断をしていない」「頼んでいない」
    # 「AI がリポジトリにライセンスが要ると判断した」は誤りだった。**
    # **473 本体は「否定の半分だけで現れるな」を守るが、否定そのものが偽になった場合は見ない。**
    #
    # ⚠ **初版は射程を 4 面に決め打ちし、`review-responses-meta.md` の Q10 English を
    #   見逃した**（オーナー指摘・2026-09-23）——**同じ Q10 の日本語だけが直り、英語が
    #   訂正前の説明を現行の回答として載せたままだった。** 決め打ちをやめて導出に変える。
    # ⚠ **是正史は禁じない。** `against.md` や Q&A の訂正記録は、これらの句を**歴史として**
    #   引く。全面禁止は履歴を消す圧力になる（#977 の線引き）ので、**473 本体と同じ手で
    #   「訂正の印が近くに在るか」で分ける。** `rounds/` は無改変保存ゆえ対象外。
    _dead473b = ("did not ask for it", "not commissioned", "did not commission it",
                 "determined that the repository needed a licence",
                 "I did not direct the drafting",
                 "判断自体、人間は出していない")
    _mark473b = re.compile(r"(#216|#125|#187|#191|訂正|corrected|誤りだった|旧文|是正|history|"
                           r"Check 473|superseded|歴史として)")
    # ⚠ **mirror 層を射程に入れる（2026-09-23・`against.md` #218）。** 初版は `LICENSES/` だけを
    #   見ており、**`docs/files/` の mirror は同じ主張を写しているのに一度も射程に入っていなかった。**
    #   実測でそこに 3 件残っていた。**「本体を直した」は「写しも直った」ではない。**
    _scope473b = ([ROOT / "LICENSE"] + sorted((ROOT / "LICENSES").rglob("*.md"))
                  + sorted((ROOT / "docs" / "files" / "LICENSES").rglob("*.md")))
    _bad473b, _unread473b = [], []
    for _f473b in _scope473b:
        if "rounds" in _f473b.parts:
            continue
        try:
            _raw473b = _f473b.read_text(encoding="utf-8")
        except Exception:
            _unread473b.append(str(_f473b.relative_to(ROOT)))
            continue
        # **粒度が本体である。** 初版は正規化後の ±300 字の窓で見て、
        # **`against.md` の 1 行 3,000 字の entry 内に在る訂正印に届かなかった。**
        # 単位は「その句を含む*行*」または「その句を含む*段落*」——どちらかに印が在れば可。
        # 行は register の 1 entry に、段落は折り返された散文に対応する。
        _paras473b = _raw473b.split("\n\n")
        _units473b = _raw473b.splitlines() + _paras473b
        for _d in _dead473b:
            _dn = re.sub(r"\s+", " ", _d)
            for _u in _units473b:
                if _dn not in re.sub(r"\s+", " ", _u):
                    continue
                if not _mark473b.search(_u):
                    _bad473b.append(f"{_f473b.relative_to(ROOT)}: 否定済みの句 {_d!r} が"
                                    "訂正の印なしで現れる")
                    break
    # 肯定側（目的の出所）が、現在形で読まれる主要 4 面に在ること。**消して黙らせる経路も塞ぐ。**
    for _rel473b in ("LICENSE", "LICENSES/REVIEWERS.md", "LICENSES/ACD-1.0.submission.md",
                     "LICENSES/ACD-1.0.submission-reference.md"):
        _p473b = ROOT / _rel473b
        if not _p473b.exists():
            _bad473b.append(f"{_rel473b}: 存在しない (射程が drift したら Check を直せ)")
            continue
        _t473b = re.sub(r"\s+", " ", _p473b.read_text(encoding="utf-8"))
        if "aim at external approval" not in _t473b and "aim for external approval" not in _t473b:
            _bad473b.append(f"{_rel473b}: 目的の出所（人間が外部承認を目指すと述べたこと）が無い")
    # ── 473c: `rounds/` の運用規約と、実際の file の状態が食い違わないこと ────────────────
    # **`against.md` #219。** 2026-09-23 に off-list 私信 5 件を stub 化したが、
    # **`rounds/README.md` / `REVISION-PROTOCOL.md` / `CLAUDE.md` は「無改変で本文そのものを
    # 置く」と規定したままだった** ——**規則と現物が真っ向から食い違い、しかも 473b は
    # 「否定済みフレーズ」しか見ないので原理的に検出しない**（オーナー指摘）。
    # **両向きで強制する** ——stub が在るなら例外を述べよ / 例外を述べるなら stub が在ること
    # （**死んだ規則を作らない**）。
    _stub473c = [p for p in sorted((ROOT / "LICENSES" / "rounds").glob("*.txt"))
                 if "THE TEXT HAS BEEN WITHDRAWN" in p.read_text(encoding="utf-8", errors="replace")]
    _conv473c = ("LICENSES/rounds/README.md", "LICENSES/REVISION-PROTOCOL.md", "CLAUDE.md")
    _bad473c = []
    for _rel in _conv473c:
        _p = ROOT / _rel
        if not _p.exists():
            _bad473c.append(f"{_rel}: 存在しない"); continue
        _has = "off-list correspondence" in _p.read_text(encoding="utf-8", errors="replace")
        if _stub473c and not _has:
            _bad473c.append(f"{_rel}: stub が {len(_stub473c)} 件在るのに例外が書かれていない")
        if not _stub473c and _has:
            _bad473c.append(f"{_rel}: 例外を述べているが stub が 1 件も無い (死んだ規則)")
    check(
        not _bad473c,
        f"Check 473c: rounds/ の規約と現物が整合 (stub {len(_stub473c)} 件 / 規約 {len(_conv473c)} 面)",
        (f"Check 473c: {_bad473c}。**`rounds/` は「無改変で本文を置く」場所だと 3 面が規定して"
         "いる。第三者との private off-list correspondence を stub 化するなら、その例外を同じ "
         "3 面に書かなければ、規則と現物が食い違ったまま公開される**"
         " (`against.md` #219・オーナー指摘 2026-09-23)。**逆に、例外を書いて stub が 1 件も"
         "無ければ死んだ規則である**"),
        blocking=True,
    )

    check(
        not _bad473b and not _unread473b,
        f"Check 473b: 来歴 {len(_scope473b)} 面に否定済みの句 0 件（訂正の印つきは可）",
        (f"Check 473b: {_bad473b}。**2026-09-23 に steward 本人が訂正した** —— "
         "ライセンスを持つ判断と上位の方向づけは人間発であり、"
         "*\"the agent determined that the repository needed a licence\"* 等は事実として誤り "
         "(`against.md` #216)。**順序は 3 段** —— 人間発の目的・上位設計 → "
         "AI による具体的な法的設計と起草 → 委任下の自走による発展・一般化。"
         "**「後から知った」を書くなら対象を 3 段目に明示せよ。** "
         "歴史として引くなら、同じ段落に訂正の印（#216 等）を置くこと"
         f" / 読めなかった file: {_unread473b}"),
        blocking=True,
    )

    check(
        not _bad473 and not _unread473,
        f"Check 473: 来歴の開示 {len(_files473)} file、否定の半分だけで現れる段落 0 件",
        (f"Check 473: 来歴の開示が否定の半分だけで現れている: {_bad473}。**steward 本人は "
         "*\"the drafting was not directed by me, but the direction of the licence was mine\"* と "
         "述べている。**「指示していない」だけを書くと、人間の関与を実際より小さく述べることになり、"
         "moderator が AI の関与度を問うている最中 (B14) には最も不利な向きである。"
         "同じ段落に肯定の半分を置け (`submission.md` §E.1 が権威)"
         f" / 読めなかった file: {_unread473}"),
        blocking=True,
    )

