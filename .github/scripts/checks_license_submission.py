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
       **(472b・2026-09-24)** 提出パケット（`ACD-1.0.submission*.md` から導出・分割しても射程が変わらない）＋入口 2 面の**逐語引用** (`*"…"*`) が、いずれかの版の本文から
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
       **⚠ そして 472c 自身が同じ形で誤っていた（2026-09-24・#223）**: 初版は実行前に
       `shasum -a 256 -c` を `sha256sum -c` へ置換しており、**審査者が貼る文字列ではなく
       別の文字列を実行していた**。Linux では両者の結果が同じなので CI は緑、macOS では
       `sha256sum -c` が operand 省略時に stdin へ落ちないため**入口ページのコマンドは
       正しいのにこの Check だけが RED** になる。置換をやめて逐語で実行する。
       **(472d・2026-09-24)** 入口ページの **"In one screen" が冒頭 10% 以内に在る**こと。B13 は
       「長さへの唯一の実効的な緩和は短い入口」と結論し、2026-09-09 に gap への到達を 35% → 5% に
       縮めたが、その後 "The short path" と "Which text you are looking at" が**前に**足され、
       **何も壊れないまま** 4% → 15% へ押し下げられていた（gap 16% / 最近似 25%）。
       **開示を足すたびに起きる後退なので、記憶ではなく位置で守る。**
       **(472e・2026-09-24)** 「placeholder / 置換テキストは 0」という主張が、§16.1 の notice
       雛形の 1 欄 `<location of this file>` の存在を同じ文で限定していること。§4c は数え方を直して
       期待値 1 にしたが、**同じ主張を無限定で繰り返す面が 5 つ残っていた**（REVIEWERS.md に 2 つ、
       submission-reference §3、review-rules、mirror doc）。記録である `against.md` は対象外。
       **(472f・2026-09-26)** 提出パケットの**版に紐づく欄**（識別子・Version・版付き URL・件名・
       SPDX 依頼の Full name）が `SUBMISSION-TARGET` の版と一致すること。確定手順 (3) は「Check 444 が
       一致を強制する」と書いていたが **444 は `submission.md` を読んでいなかった**（存在しない強制の主張）。
       しかも (3) は §B.0 しか挙げず、§A 表・§A.0・§C・§D の 11 行が版の切り替えで 1.0 のまま残る形だった。
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
                # **面の集合は導出する。** 決め打ちの 4 面だったときの被覆を測ると
                #   (2026-09-25・#227)、**提出側が審査者を送る 35 file のうち 4 file** しか
                #   見ていなかった。**現時点では実害ゼロ**（回答文書 9 面 272 引用すべてが
                #   対象版に実在する）だが、**危険が最大化するのは SUBMISSION-TARGET を
                #   切り替えた瞬間**である —— そのとき `ACD-1.0.faq.md` などは「別の版について
                #   書かれた文書」に変わり、決め打ちの 4 面はその変化を一切見ない。#144 が
                #   一度踏んだ class で、**審査者が最初に確かめる種類の誤り**。
                #   導出規則は 2 つだけにする（複雑な規則は誤検出を生む）:
                #     (1) 名前が `<target>.` で始まる file —— その版について書かれている
                #     (2) 版に中立な入口・索引の面 —— どの版が対象でも対象版を指すべき
                #   **版名を持つ他版の file は自然に外れる** —— `ACD-1.1-CHANGELIST.md` が
                #   1.1 の条を引くのは正しく、対象版で照合したら誤検出になる。
                _neutral472 = ("REVIEWERS.md", "READY-TO-SUBMIT.md", "QUESTION-INDEX.md",
                               "ACD-1.0.objection-map.md")
                _faces472 = sorted(
                    {_q.name for _q in (ROOT / "LICENSES").glob(f"{_ver472}.*.md")} |
                    {_n for _n in _neutral472 if (ROOT / "LICENSES" / _n).exists()})
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

                # **472b の面は広げない（2026-09-25・#227 で測って決めた）。**
                #   472 を 4 面 → 25 面へ導出型にした直後、472b が 4 file・16 件で発火した。
                #   **読むとすべて正当だった** —— `errata.md` が「E<n> は 1.1 でこう直った」と
                #   **後継の文言を逐語で引く**のはその文書の仕事そのもので、`against.md` /
                #   `discussion-log.md` / `jurisdictions.md` も版をまたぐ記録である。
                #   **条*番号*と逐語*引用*は別の性質だった**: 番号は対象版で解決すべきだが、
                #   引用は「版を比較する文書」が他版から引くのが正当。
                #   **広げた scope をそのまま両方に使うと、正しい記述を RED にする。**
                #   **2026-09-25: 提出パケットの部分だけは導出にした。** 決め打ちの 4 面は
                #   `submission-reference.md` の §3 系を `submission-osd.md` へ切り出した瞬間に
                #   **移した逐語引用を射程から外した**（mutation の anchor 追従で発覚）。
                #   広げるのではなく**同じ文書を分割しても射程が変わらない**ようにする。
                _faces472b = sorted({_q.name for _q in (ROOT / "LICENSES").glob("ACD-1.0.submission*.md")}
                                    | {"REVIEWERS.md", "ACD-1.0.objection-map.md"})
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
                for _rel472 in _faces472b:
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
                    (f"Check 472b: 提出側 {len(_faces472b)} 面の本文逐語引用 {_nq472} 件のうち "
                     f"{_nq472 - _marked472} 件が {_ver472} の本文に実在し、"
                     f"{_marked472} 件は他の版を明示して引いている"),
                    (f"Check 472b: 提出対象 ({_ver472}) の本文に無い語句を、版を示さずに引いている: {_qbad472}。"
                     "**番号は両方の版に在っても、語句は別の版のものでありうる** —— "
                     "審査者は存在しない条文を読まされる (`against.md` #160)。"
                     "提出対象の版の語句で引き直すか、直前で版を明示せよ"),
                    blocking=True,
                )

    # ── 472f. 提出パケットの版に紐づく欄が、SUBMISSION-TARGET の版と一致すること ───────────
    #   2026-09-26: 確定手順 (3) は「§B.0 の header・URL を新版へ向ける。Check 444 が一致を強制する」
    #   と書いていたが、444 は submission.md を読まず、§A 表・§A.0・§C・§D の欄は手順にも無かった。
    #   版を切り替えた日に、これらが黙って旧版を指したまま送られる形。欄を列挙して marker と照合する。
    _sub472f = ROOT / "LICENSES" / "ACD-1.0.submission.md"
    if _sub472f.exists():
        _t472f = _sub472f.read_text(encoding="utf-8")
        _mk472f = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", _t472f)
        _pats472f = [
            r"https://yutapr0117-design\.github\.io/portfolio/LICENSES/(ACD-\d+\.\d+)\.",
            r"Short [Ii]dentifier(?: requested)?[:*| ]+`?(ACD-\d+\.\d+)",
            r"(?m)^Version:\s+(\d+\.\d+)\s*$",
            r"\*\*Subject:\*\* For Approval: .*?\((ACD-\d+\.\d+)\)",
            r"\*\*SPDX XML:\*\* `LICENSES/(ACD-\d+\.\d+)\.spdx",
            r"I am submitting the \*\*Autonomous Commons Dedication [\d.]+ \((ACD-\d+\.\d+)\)",
            r"\*\*Full name:\*\* Autonomous Commons Dedication (\d+\.\d+)",
        ]
        _seen472f, _bad472f = 0, []
        if _mk472f:
            _tg472f = _mk472f.group(1)
            for _p in _pats472f:
                for _m in re.finditer(_p, _t472f):
                    _seen472f += 1
                    _v = _m.group(1) if _m.group(1).startswith("ACD-") else "ACD-" + _m.group(1)
                    if _v != _tg472f:
                        _ln = _t472f.count("\n", 0, _m.start()) + 1
                        _bad472f.append(f"L{_ln} {_v}")
        check(
            bool(_mk472f) and _seen472f >= 10 and not _bad472f,
            f"Check 472f: 提出パケットの版に紐づく欄 {_seen472f} 箇所が SUBMISSION-TARGET と一致",
            (f"Check 472f: 版に紐づく欄が提出対象と食い違う、または欄を見失った "
             f"(照合 {_seen472f} 箇所・不一致 {_bad472f})。**版を切り替えたら、識別子・Version・URL・件名・"
             "SPDX 依頼の Full name をすべて新版へ向ける** ——片側だけ直すと、審査者には旧版の URL と新版の本文が届く。"
             "照合数が 10 を下回るときは欄の書式が変わって検出器が見失っている"),
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
                # **書き換えないこと。** 初版は `shasum -a 256 -c` を `sha256sum -c` へ
                # 置換してから実行していた。Linux では両者が同じ結果を出すので CI は緑のまま
                # だったが、macOS では `sha256sum -c` が **operand を省くと stdin へ落ちず
                # usage を出して何も検証しない**ため、入口ページのコマンド自体は正しいのに
                # この Check だけが RED になっていた (2026-09-24 実測)。
                # **審査者が貼る文字列を検査すると名乗る Check が、別の文字列を実行していた。**
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

    # ── 472d. 入口ページの "In one screen" が冒頭 10% 以内に在ること ──────────────────────
    #   B13 の緩和は位置そのもの。前に節を足すと、何も壊れないまま到達距離だけが伸びる。
    if _rv472c.exists():
        _w472d = " ".join(_rv472c.read_text(encoding="utf-8").split())
        _i472d = _w472d.find("## In one screen")
        _p472d = (100.0 * len(_w472d[:_i472d].split()) / max(1, len(_w472d.split()))
                  if _i472d >= 0 else 100.0)
        check(
            _i472d >= 0 and _p472d <= 10.0,
            f"Check 472d: REVIEWERS.md の \"In one screen\" は冒頭 {_p472d:.1f}% に在る (≤ 10%)",
            (f"Check 472d: REVIEWERS.md の \"In one screen\" が冒頭 10% より後ろ ({_p472d:.1f}%) か見出しが無い。"
             "B13 の結論では短い入口が長さへの唯一の実効的な緩和で、節を**前に**足すと到達距離だけが黙って伸びる "
             "(2026-09-24 に 4% → 15% を発見)。新しい節は \"In one screen\" の後ろに置け"),
            blocking=True,
        )

    # ── 472e. 「placeholder は 0」を無限定で述べないこと ────────────────────────────────
    #   §16.1 の notice 雛形に `<location of this file>` が 1 欄あるので、無限定の 0 は偽。
    _pat472e = re.compile(r"zero placeholders|no placeholders?\b|placeholders?:\s*0\b|"
                          r"置換テキスト\s*0|プレースホルダ\s*0", re.I)
    #   限定は**直後**に在ること（前方を見ると無関係な語で充足する）。「条項」単独は
    #   後続の別の文にも現れて素通りしたので（mutation で実測）、特定的な語に限る。
    _qual472e = re.compile(r"16\.1|in the (?:operative )?clauses|notice template|雛形", re.I)
    _bad472e = []
    _files472e = sorted((ROOT / "LICENSES").glob("*.md")) + sorted(
        (ROOT / "docs" / "files" / "LICENSES").glob("*.md"))
    for _f472e in _files472e:
        if _f472e.name.startswith(("ACD-1.0.against.md", "BLIND-SPOTS-LOG", "AUDIT-LEDGER",
                                   "MACHINE-SURFACES-AUDIT")):
            continue
        _s472e = _f472e.read_text(encoding="utf-8")
        for _m in _pat472e.finditer(_s472e):
            _win = _s472e[_m.start():_m.end() + 100]
            if not _qual472e.search(_win):
                _bad472e.append(f"{_f472e.relative_to(ROOT)}:{_s472e.count(chr(10), 0, _m.start()) + 1}")
    check(
        not _bad472e,
        "Check 472e: placeholder / 置換テキスト 0 の主張はすべて §16.1 の雛形 1 欄で限定されている",
        (f"Check 472e: 無限定の「placeholder 0」がある: {_bad472e}。§16.1 の推奨 notice の雛形に "
         "`<location of this file>` が 1 欄あるので、限定しない 0 は偽 (REVIEWERS.md のコマンドも期待値 1)"),
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

