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
       要求項目ごとの marker が、§B.0 のうち実際に送る部分（行頭の **Subject:** から後・HTML
       コメントを除く）に在ることを機械強制する（数は実装の `_req463` が権威）。**中身の質は検査しない**
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
       463b: 申請日に実際に使う `LICENSES/SUBMISSION-MATERIALS.md` の要件表が、各要件の行（事実の列が空でない）を持つこと (2026-11-01)。
  477. **審査者へ実際に送った本文が、凍結されている canonical テキストと一致すること**
       (BLOCKING): `LICENSES/rounds/*-sent.txt` はリストへ送った文面を逐語で保存した file で、
       そのうち本文を貼り付けたものは **審査者が実際に読んだテキスト**である。Check 453 は
       repo 内の複製の sha256 を pin し、週次の配信検査は公開 URL を pin と照合するが、
       **「送った 1 通の中身」を見ている層は 1 つも無かった。**
       動機は外部の一次資料 (`review-rules.md` §1.124): McCoy Smith 氏が ModelGo の steward へ
       *"the **canonical versions** of the license (which is what, ultimately, **OSI needs to be
       able to see** in order to ensure we know what it is is being approved/disapproved)"* と
       述べ、その submitter は **大学サーバー上の複製が古いまま残る**ことを自ら述べた。
       判定は**空白を正規化した語単位の一致**で行う (メールの折り返しは byte を変えるが
       テキストの同一性を変えないため)。**版は file 自身から導出する** —— 貼り付け部分の
       先頭が一致する `LICENSES/ACD-<版>.txt` を探し、見つからなければ RED。
       ⚠ **射程を正直に書く**: 本 Check は**一致**しか見ない。**届いたかどうかは別の層**であり、
       我々の投稿が moderation で拒否されている事実 (`against.md` #215 / #222) は救えない。
       ⚠ **語の精度**: 候補集合 `ACD-[0-9]*.txt` には**凍結されていない次版の草案も入る**
       （どの file かは Check 468 が導出する）。**比べているのは「リポジトリにある正本」であって、常に「凍結
       テキスト」とは限らない。** 草案を送ることは無いので実害は無いが、**Check の言葉が対象を
       実際より狭く述べるのは、次に読む人へ誤った前提を渡す**（#1103 と同じ規律）。
       導出は 2026-09-27 に 3 版すべてで隔離検証した —— 1.0 / 1.1 / 1.2 草案のいずれも
       先頭行が 20 字以上で一意に決まり、貼り付け本文から正しい正本を選べる。
       ⚠ **mutation は登録しない（理由を残す）**: 非 vacuity は手で 2 通り実測してある
       （貼り付け本文の 1 語を書き換える → 「語 15 番目で食い違う」で RED / 末尾 120 行を削る →
       「途中で切れている」で RED）。**登録しないのは、この Check の対象が `rounds/` だから**で、
       probe は mutate → 復元の順に動くが **SIGTERM で中断すると mutated のまま残る**
       （memory `feedback_mutation_probe_verify_race` に実例がある）。**無改変保存の場所に
       byte を残す危険は、安全網 1 件の自動検証より重い。** 代わりに `ACD-1.0.txt` を mutate
       する形も検討したが、**Check 453 が同時に RED になるので帰属が曖昧になる**（#885 の
       帰属規律）。
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
       **(472d・2026-09-24・2026-11-06 に語数へ)** 入口ページの **"In one screen" が先頭から 450 語以内に在る**こと。
       割合で見ていたときは、ページを短くすると語数は前へ出たのに割合は閾値へ近づいた (440 語 → 375 語で
       8.2% → 9.8%)。B13 が守りたいのは審査者が読む語数なので語数で見る (portfolio-00 の提案)。B13 は
       「長さへの唯一の実効的な緩和は短い入口」と結論し、2026-09-09 に gap への到達を 35% → 5% に
       縮めたが、その後 "The short path" と "Which text you are looking at" が**前に**足され、
       **何も壊れないまま** 4% → 15% へ押し下げられていた（gap 16% / 最近似 25%）。
       **開示を足すたびに起きる後退なので、記憶ではなく位置で守る。**
       **(472h・2026-11-06)** 入口ページの版に紐づく面が SUBMISSION-TARGET の本文を指すこと。語数の行、
       "The licence itself" の行 (行数・節数)、検証コマンド、digest の値。marker を切り替えても 472 / 472f は
       `submission.md` の面しか見ず、入口ページは 1.0 を「the licence」と述べたまま緑だった (1.4 の予行で実測)。
       あわせて QUESTIONS-FOR-COUNSEL の基準の版が LICENSE の適用する版と、objection-map の "Numbers" の基準が
       提出対象と一致すること。
       **(472l・2026-11-06)** 入口ページと申請日の 1 枚が OSI の FAQ として引く文が、`rounds/` の FAQ の本文に在ること。
       承認されるべき理由の先頭に置いた出典なので、語を読みやすく動かすと審査者が最初に確かめて落ちる。
       **(472m / 472n / 472o・2026-11-07)** 入口の表の語数 / 入口の引用 / 送る本文が述べる版 (`checks_license_references.py`)。
       **(472k・2026-11-06)** `objection-map.md` が引く §2〜§16 の条が提出対象に在ること。472 はどれかの版に在る番号しか
       見ないので、どの版にも無い番号は黙って通っていた。§1.x はドシエの節と同じ形なので対象外。
       **(472j・2026-11-06)** `ADOPTING.md` の "the same in every version" の主張。引く条が凍結版すべてと草案に在ること。
       **(472i・2026-11-06)** 入口の 2 つの表が、英語の審査者を読めない文書へ黙って送らないこと。"What to open first" の
       行が指す file の日本語の比率が 30% 以上なら行に Japanese と書く。言語の表が English / Japanese と述べる file は
       実測と合う。比率は日本語の文字 / (日本語の文字 + ラテン文字)。register 63% と READY-TO-SUBMIT 66% が無表示
       だったのを portfolio-00 が見つけた (#2466)。**日本語の文書を減らす検査ではなく、述べることを求める検査である。**
       **(472g・2026-11-06)** "In one screen" の節が 500 語以内、"Status" の節が 600 語以内であること。
       追記のたびに黙って伸びる形で、伸びたのは 09-24 に続いて 2 度目だった。
       **(472e・2026-09-24)** 「placeholder / 置換テキストは 0」という主張が、§16.1 の notice
       雛形の 1 欄 `<location of this file>` の存在を同じ文で限定していること。§4c は数え方を直して
       期待値 1 にしたが、**同じ主張を無限定で繰り返す面が 5 つ残っていた**（REVIEWERS.md に 2 つ、
       submission-reference §3、review-rules、mirror doc）。記録である `against.md` は対象外。
       **(472f・2026-09-26)** 提出パケットの**版に紐づく欄**（識別子・Version・版付き URL・件名・
       SPDX 依頼の Full name）が `SUBMISSION-TARGET` の版と一致すること。確定手順 (3) は「Check 444 が
       一致を強制する」と書いていたが **444 は `submission.md` を読んでいなかった**（存在しない強制の主張）。
       しかも (3) は §B.0 しか挙げず、§A 表・§A.0・§C・§D の 11 行が版の切り替えで 1.0 のまま残る形だった。
"""
import hashlib
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
            # [FIX 2026-11-08] 照合は実際に送る部分だけ。見出しから **Subject:** までの作業メモ (約 13 KB) と、
            #   送られない HTML コメントは除く (法的レビューの段落をコメントにしても通ることを実測した)。
            _s463 = re.search(r"^\*\*Subject:\*\*", _b0, re.M)
            if not _s463:
                _bad463.append("§B.0 に送る文面の始まり (行頭の **Subject:**) が見つからない")
            _b0 = re.sub(r"<!--.*?-->", "", _b0[_s463.start():] if _s463 else "", flags=re.S)
            _req463 = [
                ("attachment", r"attached as plain text"),
                ("OSD affirmation", r"I affirm that ACD-\d+\.\d+ complies with the Open Source Definition"),
                # 要件は「OSD 3, 5, 6, 9 を満たすと specifically 明言する」(原文 "including specifically
                # affirming it meets OSD 3, 5, 6 and 9")。欠落は議論の不成立を招く (`against.md` #97)。
                ("OSD 3/5/6/9 specific", r"OSD 3\*\*[\s\S]{0,400}?OSD 5 and OSD 6\*\*[\s\S]{0,400}?OSD 9\*\*"),
                ("projects using it", r"Approved or Used by Projects"),
                # [2026-11-08] 463b が要件に持つのに、ここに無かった 2 項目 (行を消しても通ることを実測)。
                ("legacy or new", r"^Legacy or New:\s*\S"),
                ("subject", r"^\*\*Subject:\*\*.*For Approval:"),
                ("steward contact", r"Steward:.*@"),
                ("name and version", r"License Name:"),
                # 2026-09-13 追加。Debian / FSF / Fedora の承認を問う項目だけが答えられていなかった。
                # 答えが「無い」項目ほど書き落としても自然に読めるので機械で縛る (`review-precedents.md` §1.76)。
                ("third-party endorsement", r"Third-party Endorsement:"),
                ("SPDX / ScanCode", r"SPDX / ScanCode Identifier"),
                ("proposed tags", r"Proposed Tags:"),
                ("gap statement", r"\*\*The gap\.\*\*"),
                ("nearest approved licences", r"\*\*Nearest approved licences\.\*\*"),
                # **2026-09-13 追記（この項目を足した理由の裏付け）。** 委員長は BOS Public License の
                # 提出に対し、欠けている項目のうち**この 1 件だけを名指しして**
                # *"in particular do not skip 'Describe any legal review the license has been
                # through, including whether it was drafted by a lawyer.'"* と述べている (2026-07-23)。
                # 最大の弱点を述べる項目なので書き落とす圧力が構造的にある (`review-precedents.md` §1.75)。
                ("legal review", r"\*\*Legal review: none\.\*\*"),
                ("entry page URL", r"https://github\.com/\S+/blob/main/LICENSES/REVIEWERS\.md"),  # 読み手に入口への道が無かった
                ("project URL", r"Approved or Used by Projects:.*https://"),
            ]
            _miss463 = [_n for _n, _r in _req463 if not re.search(_r, _b0, re.M)]
            if _miss463:
                _bad463.append(f"§B.0 に OSI 要求項目が欠けている: {_miss463}")
        # ── 463b: 申請日の 1 枚 (SUBMISSION-MATERIALS.md) の要件表が、各要件の行を持つこと ──
        #   §B.0 は 1.0 向けの文面で、申請の日に実際に使うと宣言されているのは
        #   `SUBMISSION-MATERIALS.md` の要件表 (「申請の日に使うのはこの 1 枚」)。そちらはどれかの行が
        #   消えても何も鳴らなかった —— #77 と同じ「答えが無い項目ほど静かに落ちる」class
        #   (2026-11-01・portfolio-25 の提案)。行見出しの語は 25 と合わせて決めた (変えるならここも)。
        #   事実の列が空の行も欠落として数える (見出しだけ残して中身が消える形を止める)。
        _sm463 = ROOT / "LICENSES" / "SUBMISSION-MATERIALS.md"
        _rows463b = ("件名", "名前と版", "本文", "新規か legacy か", "OSD 準拠の明言", "OSD 3",
                     "OSD 5・6", "OSD 9", "使っているプロジェクト", "steward と連絡先",
                     "SPDX / ScanCode 識別子", "第三者の承認", "提案する tag", "gap（",
                     "最も近い承認済みライセンス", "法的レビュー", "来歴", "利益相反")
        if not _sm463.exists():
            _bad463.append("463b: LICENSES/SUBMISSION-MATERIALS.md が無い (申請日の 1 枚)")
        else:
            _tbl463b = {}
            for _ln in _sm463.read_text(encoding="utf-8").splitlines():
                _cells = [_c.strip().strip("\u3000").strip() for _c in _ln.strip().strip("|").split("|")]
                if _ln.lstrip().startswith("|") and len(_cells) >= 2:
                    _tbl463b.setdefault(_cells[0], _cells[1])
            _lack463b = [_r for _r in _rows463b
                         if not any(_k.startswith(_r) and _v for _k, _v in _tbl463b.items())]
            if _lack463b:
                _bad463.append(f"463b: SUBMISSION-MATERIALS.md の要件表に行が無い (または事実が空): {_lack463b}")
        check(
            not _bad463,
            # **件数は導出する（2026-09-13 是正）。** ここは長らく「11 項目」とリテラルで書かれており、
            # **項目を足しても OK メッセージは 11 のままだった** —— Check 460 が他所で禁じている
            # 「自己申告の件数が実測とずれる」を、**Check 自身の成功メッセージでやっていた。**
            # 成功メッセージは読み手が最も信用する場所なので、ここでの drift は最も悪い。
            f"Check 463: 送る文面 (§B.0) が OSI の要求 {len(_req463)} 項目をすべて含み、申請日の 1 枚 (SUBMISSION-MATERIALS.md) も {len(_rows463b)} 行すべてを持つ",
            (f"Check 463: {_bad463}。要件の単一ソースは "
             "https://opensource.org/licenses/review-process。**§B.0 は実際にメールへ貼られる文面**で、"
             "§B.1 以降は貼らない参考資料である。#77 で 3 件の欠落を埋めたが、文面は増分のたび"
             "書き換えられるので同じ欠落は静かに再発する"),
            blocking=True,
        )
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 463: 対象ファイル",
              f"Check 463: 検査対象 {_sb463.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

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
                    _tx472 = _p472.read_text(encoding="utf-8")
                    _cited = set(re.findall(r"§\s?(\d{1,2}\.\d{1,2})(?!\d)", _tx472))
                    _miss = sorted(_c for _c in _cited
                                   if _c in _universe472 and _c not in _have472)
                    # [FIX 2026-11-08] 後の版の条番号はどれも 1.0 の部分集合なので、提出対象が 1.0 の間は
                    #   上の条件が成り立たず、この Check は一度も RED になりえなかった。どの版にも無い番号
                    #   (§8.4 を §8.9 と書いた誤り) も見ていなかった (監査で実測)。条の形の番号 (1〜16 節・
                    #   1〜20 項) で、どの版にも無く、前に file 名・他の版・他のライセンスの名前が無く、
                    #   その file 自身の節でもないものを数える。
                    _own472 = set(re.findall(r"(?m)^#+\s*(\d{1,2}\.\d{1,2})\b", _tx472))
                    for _m472c in re.finditer(r"§\s?(\d{1,2})\.(\d{1,2})(?!\d)", _tx472):
                        _c472 = f"{_m472c.group(1)}.{_m472c.group(2)}"
                        if (_c472 in _universe472 or _c472 in _own472
                                or not (1 <= int(_m472c.group(1)) <= 16 and 1 <= int(_m472c.group(2)) <= 20)):
                            continue
                        _ctx472 = _tx472[max(0, _m472c.start() - 60):_m472c.start()].replace("\n", " ")
                        if re.search(r"(\.md`?\)?[^§]{0,14}$|ACD-1\.[1-9]|1\.[1-9] |from 1\.|in 1\.|draft|草案"
                                     r"|CERN|Apache|GPL|MPL|EPL|CC0|OHL|UPL|Blue ?Oak|FAQ|OSD|minutes)", _ctx472):
                            continue
                        _miss.append(f"{_c472} (どの版にも無い)")
                    if _miss:
                        _bad472.append(f"{_rel472}: {_miss}")
                _cls472 = sorted((ROOT / "LICENSES").glob("ACD-*-CHANGELIST.md"),
                                 key=lambda _p: [int(_x) for _x in re.findall(r"\d+", _p.name)])
                _latest_cl472 = _cls472[-1].name if _cls472 else "ACD-<版>-CHANGELIST.md"
                check(
                    not _bad472,
                    f"Check 472: 提出側 {len(_faces472)} 面の条項引用が {_ver472} に実在する",
                    (f"Check 472: 提出対象 ({_ver472}) に存在しない条を引いている面がある: {_bad472}。"
                     "**条番号は版をまたいで保存されない** —— 1.0 の §15.5 / §15.7 / §15.8 は "
                     "1.1 以降に無く、§16.4〜§16.6 は番号が同じまま意味が違う。"
                     "**提出物が「何も述べていない条」へ審査者を送るのは、最初に確かめられる種類の誤りである** "
                     "(`against.md` #144)。SUBMISSION-TARGET を切り替えたら引用も写像せよ "
                     f"(対応表は最新版の変更リスト `{_latest_cl472}` の「条項の対応表」節。"
                     "旧文は閉じた 1.1 の変更リストを指していた —— 2026-09-29 訂正)"),
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
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 472: 対象ファイル",
              f"Check 472: 検査対象 {_sub472.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

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
            r"(?m)^Version:\s+(\S+)\s*$",  # [2026-11-08] 1.4-rc1 のような値も読む (形が崩れると照合から黙って外れた)
            r"\*\*Subject:\*\* For Approval: .*?\((ACD-\d+\.\d+)\)",
            r"\*\*SPDX XML:\*\* `LICENSES/(ACD-\d+\.\d+)\.spdx",
            r"I am submitting the \*\*Autonomous Commons Dedication [\d.]+ \((ACD-\d+\.\d+)\)",
            r"\*\*Full name:\*\* Autonomous Commons Dedication (\d+\.\d+)",
        ]
        _seen472f, _bad472f = 0, []
        if _mk472f:
            _tg472f = _mk472f.group(1)
            for _p in _pats472f:
                # [2026-11-08] 欄ごとに 1 つ以上在ること。旧版は合計の下限 (10) だけで、欄の形が崩れると
                #   その欄は比べられないまま黙って外れた (16 欄のうち 6 欄まで)
                if not re.search(_p, _t472f):
                    _bad472f.append(f"欄が読めない: {_p[:40]}")
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
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 472f: 対象ファイル",
              f"Check 472f: 検査対象 {_sub472f.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

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
                _me = re.search(r"→\s*(?:expect\s+(\d+)|(\d+)\s*×\s*OK)", _ln)
                if _ln.lstrip().startswith("#") and "→" in _ln and not _me:  # [2026-11-08] 言い換えた期待値は黙って外れていた
                    _bad472c.append(f"期待値の形が読めない (→ expect N / → N× OK で書く): {_ln.strip()[-50:]!r}")
                if not (_ln.lstrip().startswith("#") and _me):
                    continue
                _cmd = next((_c.strip() for _c in _lines[_k + 1:]
                             if _c.strip() and not _c.lstrip().startswith("#")), "")
                if not _cmd.startswith("grep "):
                    _bad472c.append(f"期待値の後のコマンドが grep で始まらないので実行しない: {_cmd[:50]!r}")
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
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 472c: 対象ファイル",
              f"Check 472c: 検査対象 {_rv472c.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

    # ── 472d. 入口ページの "In one screen" が先頭から 450 語以内に在ること ──────────────────
    #   B13 の緩和は位置そのもの。前に節を足すと、何も壊れないまま到達距離だけが伸びる。
    #   割合ではなく語数で見る: ページを短くしても割合は閾値へ近づくので、割合は読む量を測れない (2026-11-06)。
    if _rv472c.exists():
        _t472d = _rv472c.read_text(encoding="utf-8")
        _i472d = re.search(r"(?m)^## In one screen\s*$", _t472d)  # 行頭の見出しだけ (前のコメントや文中の語を測っていた)
        _p472d = len(_t472d[:_i472d.start()].split()) if _i472d else None
        check(
            _p472d is not None and _p472d <= 450,
            f"Check 472d: REVIEWERS.md の \"In one screen\" は先頭から {_p472d} 語に在る (≤ 450 語)",
            (f"Check 472d: REVIEWERS.md の \"In one screen\" が先頭から 450 語より後ろ ({_p472d} 語) か見出しが無い。"
             "B13 の結論では短い入口が長さへの唯一の実効的な緩和で、節を**前に**足すと到達距離だけが黙って伸びる "
             "(2026-09-24 に発見)。新しい節は \"In one screen\" の後ろに置け"),
            blocking=True,
        )
        # ── 472g. 入口の 2 節が上限の語数に収まること ─────────────────────────────────
        #   どちらも追記のたびに黙って伸びる。節は見出しから次の `## ` まで。
        _secs472g = {_b.split("\n", 1)[0][3:].strip(): len(_b.split()) for _b in re.split(r"(?m)^(?=## )", _t472d)}
        _over472g = [f"{_n}: {_secs472g.get(_n, '節が無い')} 語 (≤ {_c})" for _n, _c in (("In one screen", 500), ("Status", 600))
                     if not _secs472g.get(_n) or _secs472g[_n] > _c]
        check(
            not _over472g,
            f"Check 472g: REVIEWERS.md の \"In one screen\" {_secs472g.get('In one screen')} 語 / \"Status\" {_secs472g.get('Status')} 語 (≤ 500 / 600)",
            (f"Check 472g: 入口の節が上限を超えた: {_over472g}。短い入口が長さへの唯一の実効的な緩和なので、"
             "足すなら同じ節の別の文を削るか、後ろの節へ置け"),
            blocking=True,
        )
        # ── 472k. objection-map の条が提出対象に在ること ─────────────────────────────────
        #   472 は「他の版には在るが対象に無い」しか見ない (ドシエの §1.52 のような節番号を誤検出しないため)。
        #   反論の表は条を根拠にするので、この面だけ §2〜§16 の全部を当てる。§1.x はドシエの節と区別できない。
        #   `file.md` §N.M の形は別の文書の節なので見ない (実測: PEER-REVIEW-WATCH.md §3.9)。
        _om472k = ROOT / "LICENSES" / "ACD-1.0.objection-map.md"
        _ot472k = _om472k.read_text(encoding="utf-8") if _om472k.exists() else ""
        _tm472k = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", (ROOT / "LICENSES" / "ACD-1.0.submission.md").read_text(encoding="utf-8"))
        _tg472k = _tm472k.group(1) if _tm472k else "?"
        _tp472k = ROOT / "LICENSES" / f"{_tg472k}.txt"
        _have472k = set(re.findall(r"^  (\d+\.\d+) ", _tp472k.read_text(encoding="utf-8"), re.M)) if _tp472k.exists() else set()
        _cite472k = sorted({_c for _c in re.findall(r"(?<!\.md` )§\s?(\d{1,2}\.\d{1,2})(?!\d)", _ot472k) if 2 <= int(_c.split(".")[0]) <= 16})
        _miss472k = [_c for _c in _cite472k if _c not in _have472k]
        check(
            len(_cite472k) >= 5 and not _miss472k,
            f"Check 472k: objection-map が引く {len(_cite472k)} 条が提出対象 {_tg472k} に在る",
            (f"Check 472k: objection-map が提出対象 {_tg472k} に無い条を引いている: {_miss472k or '引用が読めない'}。"
             "反論への答えの根拠が存在しない条だと、審査者が最初に確かめて落ちる"),
            blocking=True,
        )
        # ── 472j. ADOPTING.md の「どの版でも同じ番号」の主張 ─────────────────────────────
        #   採用者向けの 1 枚は版を問わず読まれるので、引く条は全部の版に在る必要がある。
        _ad472j = ROOT / "LICENSES" / "ADOPTING.md"
        _at472j = _ad472j.read_text(encoding="utf-8") if _ad472j.exists() else ""
        _cite472j = sorted(set(re.findall(r"§(\d+\.\d+)", _at472j)))
        _miss472j = []
        for _v472j in sorted((ROOT / "LICENSES").glob("ACD-*.txt")):
            _t472j = _v472j.read_text(encoding="utf-8")
            if "HAS BEEN FROZEN" in _t472j.split("\n", 1)[0]:
                continue
            _have472j = set(re.findall(r"^  (\d+\.\d+) ", _t472j, re.M))
            _miss472j += [f"§{_c} が {_v472j.name} に無い" for _c in _cite472j if _c not in _have472j]
        check(
            "the same in every version" in _at472j and len(_cite472j) >= 3 and not _miss472j,
            f"Check 472j: ADOPTING.md が引く {len(_cite472j)} 条が全部の版に在る",
            (f"Check 472j: ADOPTING.md の「どの版でも同じ番号」が成り立たない: {_miss472j or '文が無いか引用が読めない'}。"
             "版で番号が違う条を引くなら、その条について版を述べよ"),
            blocking=True,
        )
        # ── 472i. 入口の 2 つの表が、読めない文書へ黙って送らないこと ──────────────────────
        #   B13 の短い入口は読者が英語の審査者である前提に立つ。勧めた文書が読めないと、その行は入口にならない。
        def _jp472i(_rel):
            _s = (ROOT / "LICENSES" / _rel).read_text(encoding="utf-8", errors="replace")
            _n = len(re.findall(r"[\u3040-\u30ff\u3400-\u9fff]", _s))
            _a = len(re.findall(r"[A-Za-z]", _s))
            return _n / (_n + _a) if _n + _a else 0.0

        _rows472i = _t472d.split("## What to open first", 1)[-1].split("\n## ", 1)[0].split("\n")
        _map472i = _t472d.split("## Map of the supporting documents", 1)[-1].split("\n## ", 1)[0].split("\n")
        _bad472i, _seen472i = [], 0
        for _row in _rows472i:
            _m = re.search(r"\]\(([^)#\s]+)(?:#[^)\s]*)?\)", _row)  # [2026-11-08] #節 付きのリンクも読む
            if _row.startswith("|") and _m and (ROOT / "LICENSES" / _m.group(1)).exists():
                _seen472i += 1
                if _jp472i(_m.group(1)) >= 0.30 and "Japanese" not in _row:
                    _bad472i.append(f"{_m.group(1)} は日本語 {_jp472i(_m.group(1)):.0%} なのに行が Japanese と述べない")
        for _row in _map472i:
            _m = re.match(r"\| \[`[^`]+`\]\(([^)#\s]+)(?:#[^)\s]*)?\) \| \**([A-Za-z]+)\b", _row)
            if _m and (ROOT / "LICENSES" / _m.group(1)).exists():
                _seen472i += 1
                if _m.group(2) not in ("English", "Japanese", "Mixed"):  # [2026-11-08] 他の表示は黙って照合から外れていた
                    _bad472i.append(f"{_m.group(1)} の言語の表示 {_m.group(2)!r} を読めない (English / Japanese / Mixed)")
                elif _m.group(2) == "Mixed":
                    if not 0.10 <= _jp472i(_m.group(1)) <= 0.90:
                        _bad472i.append(f"{_m.group(1)} は Mixed と述べるが日本語 {_jp472i(_m.group(1)):.0%}")
                elif (_jp472i(_m.group(1)) >= 0.30) != (_m.group(2) == "Japanese"):
                    _bad472i.append(f"{_m.group(1)} は {_m.group(2)} と述べるが日本語 {_jp472i(_m.group(1)):.0%}")
        check(
            _seen472i >= 20 and not _bad472i,
            f"Check 472i: 入口の 2 つの表の {_seen472i} 行が、指す文書の言語を実測どおり述べる",
            (f"Check 472i: 入口の表の言語の表示が実測と違う (照合 {_seen472i} 行): {_bad472i}。"
             "英語の審査者を読めない文書へ黙って送らない。行に言語を書くか、文書の冒頭に英語の索引を置いて行で述べよ"),
            blocking=True,
        )
        # ── 472h. 入口ページの版に紐づく面が SUBMISSION-TARGET の本文を指すこと ───────────────
        #   marker を切り替えた日に、472 / 472f は submission.md の面を赤くするが入口ページは見ない。
        #   審査者が最初に開くページが古い版を「the licence」と述べたまま緑だった (2026-11-06 の予行)。
        _sb472h = (ROOT / "LICENSES" / "ACD-1.0.submission.md").read_text(encoding="utf-8")
        _mk472h = re.search(r"<!--\s*SUBMISSION-TARGET:\s*(ACD-\d+\.\d+)\s*-->", _sb472h)
        _tg472h = _mk472h.group(1) if _mk472h else "?"
        _tp472h = ROOT / "LICENSES" / f"{_tg472h}.txt"
        _bad472h = []
        if not _tp472h.exists():
            _bad472h.append(f"{_tg472h}.txt が無い")
        else:
            _tt472h = _tp472h.read_text(encoding="utf-8")
            _body472h = _tt472h.split("-" * 80, 1)[1] if "-" * 80 in _tt472h else _tt472h
            _link472h = f"[`{_tg472h}.txt`]({_tg472h}.txt)"
            _mw472h = re.search(re.escape(_link472h) + r" \| \*\*([\d,]+)\*\* \| the licence\b", _t472d)
            if not _mw472h or int(_mw472h.group(1).replace(",", "")) != len(_body472h.split()):
                _bad472h.append(f"語数の行が {_tg472h} の {len(_body472h.split())} 語を述べていない")
            _ml472h = re.search(r"\| The licence itself \| " + re.escape(_link472h) + r" \| ([\d,]+) lines, (\d+) sections", _t472d)
            _secs472h = len(re.findall(r"^\d+\. [A-Z]", _body472h, re.M))
            if not _ml472h or (int(_ml472h.group(1).replace(",", "")), int(_ml472h.group(2))) != (_tt472h.count("\n"), _secs472h):
                _bad472h.append(f"\"The licence itself\" の行が {_tg472h} の {_tt472h.count(chr(10))} lines, {_secs472h} sections を述べていない")
            # digest の照合は grep の正規表現の中に版を書くので、\. の形も読む。素の形だけ見ると、
            # 片方を切り替えたまま審査者の手元で 2 つの digest が食い違っても緑になる (2026-11-07 の予行)。
            _cmd472h = sorted(set(re.findall(r"^(?:shasum -a 256 |grep .* )(?:\./)?LICENSES/(ACD-\d+\.\d+)\.txt$", _t472d, re.M))
                              | {_v.replace("\\.", ".") for _v in re.findall(r"LICENSES/(ACD-\d+\\\.\d+)\\\.txt\$'", _t472d)})
            if _cmd472h != [_tg472h]:
                _bad472h.append(f"検証コマンドの対象が {_tg472h} でない: {_cmd472h}")
            if hashlib.sha256(_tp472h.read_bytes()).hexdigest() not in _t472d:
                _bad472h.append(f"digest の値が {_tg472h} のものでない")
        _om472h = ROOT / "LICENSES" / "ACD-1.0.objection-map.md"
        if f"**Numbers.** Clause numbers are those of {_tg472h}," not in _om472h.read_text(encoding="utf-8"):
            _bad472h.append(f"objection-map の \"Numbers\" の基準が提出対象 {_tg472h} でない")
        _qc472h = ROOT / "LICENSES" / "QUESTIONS-FOR-COUNSEL.md"
        _lc472h = re.search(r"^SPDX-License-Identifier: (ACD-\d+\.\d+)$", (ROOT / "LICENSE").read_text(encoding="utf-8"), re.M)
        if _lc472h and f"Clause numbers are those of **{_lc472h.group(1)}**" not in _qc472h.read_text(encoding="utf-8"):
            _bad472h.append(f"QUESTIONS-FOR-COUNSEL の基準の版が適用する版 {_lc472h.group(1)} でない")
        check(
            not _bad472h,
            f"Check 472h: 入口ページの語数・行数・検証コマンド・digest が提出対象 {_tg472h} を指し、質問票の基準が適用する版を指す",
            (f"Check 472h: 入口ページが提出対象を指していない: {_bad472h}。審査者が最初に開くページなので、"
             "SUBMISSION-TARGET を切り替えたら同じ commit で直せ"),
            blocking=True,
        )
    else:
        # 対象が無いのに黙って skip しない (2026-11-02): 改名・移動を正しく済ませると他の Check は全部緑のまま、
        # ここだけが OK も ERROR も出さずに消える (460 / 469 で踏んだ形)。
        check(False, "Check 472d: 対象ファイル",
              f"Check 472d: 検査対象 {_rv472c.relative_to(ROOT).as_posix()} が無い —— 改名・移動したならこの Check の参照先を直す (黙って skip しない)")

    # ── 472e. 「placeholder は 0」を無限定で述べないこと ────────────────────────────────
    #   §16.1 の notice 雛形に `<location of this file>` が 1 欄あるので、無限定の 0 は偽。
    _pat472e = re.compile(r"zero placeholders|no placeholders?\b|placeholders?:\s*0\b|\b0 placeholders?\b|placeholder-free|"
                          r"置換テキスト(?:は)?\s*0|プレースホルダ(?:は)?\s*0", re.I)
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

    # ── 477. 審査者へ実際に送った本文が、凍結テキストと一致すること (BLOCKING) ──────────
    # `rounds/*-sent.txt` はリストへ送った文面の逐語保存で、本文を貼り付けたものは
    # **審査者が実際に読んだテキスト**である。Check 453 は repo 内の複製を pin し、週次の
    # 配信検査は公開 URL を pin と照合する。**送った 1 通の中身を見る層だけが無かった。**
    #
    # なぜ層が要るか (外部の一次資料・`review-rules.md` §1.124): Licensing Committee の
    # McCoy Smith 氏は ModelGo の steward へ *"the canonical versions of the license (which is
    # what, ultimately, OSI needs to be able to see …)"* と述べ、その submitter は
    # **もう 1 つの公開複製が古いまま残る**と自ら述べた。**複製が食い違う失敗は現に起きている。**
    #
    # 判定を byte でなく**空白正規化した語単位**にする理由: メールの折り返しは byte を変えるが
    # テキストの同一性を変えない。byte 比較にすると**必ず RED になる brittle gate** になる。
    #
    # 版を決め打ちしない理由: 次に送る 1 通は 1.0 ではない (`REVISION-PROTOCOL.md` §3.6 分岐 B)。
    # 貼り付け部分の先頭と一致する `ACD-<版>.txt` を探す形なら、そのまま働く。
    _sent477 = sorted((ROOT / "LICENSES" / "rounds").glob("*-sent.txt"))
    _texts477 = sorted((ROOT / "LICENSES").glob("ACD-[0-9]*.txt"))
    _bad477, _checked477 = [], 0

    def _norm477(s):
        return re.sub(r"\s+", " ", s).strip()

    for _s477 in _sent477:
        try:
            _body477 = _s477.read_text(encoding="utf-8")
        except Exception as _e477:
            _bad477.append(f"{_s477.name}: 読めない ({_e477})")
            continue
        for _c477 in _texts477:
            _canon477 = _c477.read_text(encoding="utf-8")
            # 貼り付けの開始点は、canonical 側の最初の見出し行で決める
            _head477 = next((ln for ln in _canon477.splitlines()
                             if ln.strip() and not ln.startswith(("#", "-"))), "")
            if len(_head477) < 20 or _head477 not in _body477:
                continue
            _checked477 += 1
            _a477 = _norm477(_canon477[_canon477.index(_head477):]).split(" ")
            _b477 = _norm477(_body477[_body477.index(_head477):]).split(" ")
            _n477 = min(len(_a477), len(_b477))
            _diff477 = next((i for i in range(_n477) if _a477[i] != _b477[i]), None)
            if _diff477 is not None:
                _bad477.append(
                    f"{_s477.name} が貼り付けた {_c477.name} の本文が、リポジトリの正本と"
                    f"語 {_diff477} 番目で食い違う "
                    f"(正本={_a477[_diff477]!r} / 送信={_b477[_diff477]!r})")
            elif len(_b477) < len(_a477):
                _bad477.append(
                    f"{_s477.name} が貼り付けた {_c477.name} の本文はリポジトリの正本より短い "
                    f"({len(_b477)} 語 / 正本 {len(_a477)} 語) —— **途中で切れている**")
            break

    check(
        not _bad477,
        f"Check 477: 送信控え {len(_sent477)} 件・本文を貼り付けた {_checked477} 件がリポジトリの正本と一致",
        (f"Check 477: 送った本文がリポジトリの正本と食い違う: {_bad477}。"
         "**審査者が読むのは送った 1 通であって repo の複製ではない。** "
         "直す方向は 2 つとも禁じられている —— `rounds/` は無改変保存であり "
         "(`rounds/README.md`)、凍結テキストは Check 453 が pin している。"
         "**食い違いを見つけたら直さずオーナーへ報告せよ** "
         "(`review-rules.md` §1.124 が、この規則を述べた一次資料である)"),
        blocking=True,
    )
