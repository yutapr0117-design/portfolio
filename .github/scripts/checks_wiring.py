"""
checks_wiring.py — shipped-asset & AIO wiring / discoverability checks
(extracted from check_repository_consistency.py — check.py split track・category "wiring/discovery").

This module owns the cluster of Checks 132-134 (plus 375, 376) that assert shipped assets and AIO
evidence are actually wired up and discoverable (not merely present): AIO evidence ↔ sitemap
discoverability (132), aio-guard.js `<script src>` wiring (133), root-script wiring
completeness (134), and shipped-JS createIcon name → icon-registry resolution (375, the
"used icon name ⟹ it is actually defined" wiring twin of 133/134's "file exists ⟹ wired").
Each Check reads its own target files directly (index.html, sitemap.xml,
aio-manifest.json, js/*.js) via Path.read_text(); a free-variable analysis confirms zero external `_`-vars
and no global html/style/mainjs dependency, so the cluster is self-contained and needs no ctx
enrichment. NOTE: Check 135 (stylesheet wiring) is the natural sibling but reads the global
`style` content, so it stays in the monolith until a ctx-enrich phase.

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  132. AIO evidence ↔ sitemap discoverability: every text document registered as authoritative
       evidence in .well-known/aio-manifest.json (source_of_truth / supporting_evidence /
       observational_evidence whose path ends in .md / .txt / .json) must also appear as a <loc> in
       sitemap.xml. The manifest declares a doc authoritative for AI crawlers, but a crawler that
       discovers the site via sitemap.xml will never reach a registered doc that is absent from the
       sitemap — a silent discoverability gap (real-work-claims.md and AI2AI-archive.md were
       registered but missing from the sitemap until this Check was added). Binary assets
       (.webp/.mp3) are excluded (images/audio are not sitemap-indexed text). This makes
       "registered-as-evidence ⟹ sitemap-discoverable" an enforced invariant. (BLOCKING)
  133. AIO guard script wiring: aio-guard.js is the AIO asset-anchor lifecycle monitor & self-repair
       mechanism — it watches the hidden <div id="aio-asset-anchor"> and restores it if any AI-run
       "dead code purge" removes it (the anchor is invisible but semantically critical to the AIO
       layer). The monitor only works if index.html actually loads it before the main SPA IIFE.
       The mirror-bijection check only asserts the FILE exists; nothing enforced that index.html
       still REFERENCES it, so deleting the <script src="./aio-guard.js"> tag would leave the file
       present (verify green) while silently deactivating the self-repair monitor — only a
       non-blocking CI advisory caught this. This Check asserts index.html contains a
       <script src="./aio-guard.js"> reference, making "guard file exists ⟹ guard is wired" an
       enforced invariant (regression guard for the AIO self-repair monitor). (BLOCKING)
  134. Root script wiring completeness: index.html must keep loading the root scripts it depends
       on (theme-init.js / karte-init.js / main.js) via a <script src> reference. Like Check 133
       (aio-guard.js), the mirror-bijection only asserts the FILE exists — nothing enforced that the
       <script> tag remains. Removal degrades SILENTLY: theme-init.js is the pre-paint FOUC guard
       (its loss is a flash of unstyled/wrong-theme content that no behavior e2e asserts, and the
       screenshot e2e is now ADVISORY per §3(B) so it would not block); karte-init.js silently
       disables analytics; main.js is the SPA entry point (e2e catches its loss, but a static check
       makes the entry-point wiring explicit and survives an e2e outage). error-suppressor.js is
       NOT covered here because it is inlined (Check 7/7b enforce its inline byte-identity + CSP
       hash), and aio-guard.js is covered by Check 133. This makes "root script file exists ⟹ it is
       wired into index.html" an enforced invariant for the remaining external root scripts.
       (BLOCKING)
  403. sr-only AIO entity anchor presence: index.html は AIO 戦略上 load-bearing な sr-only
       エンティティアンカー — `<div id="aio-footer-entity">` (著作権 / entity / canonical ブロック)
       と `<footer id="aio-main-footer">` (RAG チャンクアンカー) — を **要素として** 保持しなければ
       ならない。これらは視覚的に不可視 (sr-only + aria-hidden) ゆえ、除去しても (a) pixel
       screenshot は無変化 (そもそも §3(B) で advisory)、(b) behavior e2e は素通り、(c) consistency も
       無被覆で、完全に silent に消える。実測: `<div id="aio-footer-entity">` ブロックを丸ごと削除
       しても behavior e2e は PASS し consistency は 0 errors だった (同時に、その e2e が
       `if (await entity.count())` の skip-on-missing で vacuous だったことも判明し是正した)。
       Check 133 (aio-guard.js の script 配線 → #aio-asset-anchor 保護) と同じ「不可視だが
       load-bearing な AIO 要素」class の entity-anchor 面。判定は要素 (`<div ... id="...">`) を
       見るため、changelog コメント中の id 言及では PASS しない。(BLOCKING)
  411. querySelectorAll selector → rendered-markup resolution: a selector that matches nothing the
       app ever renders makes its scan return 0 rows forever, silently disabling the feature built on
       it. The trigger case was the WebMCP (agentic accessibility) tool in main.js, which declares in
       its own description that it extracts evidence from the page's CURRENT DOM. If that selector
       resolves to
       nothing the app actually renders, the tool silently returns its static fallback string forever
       and the declaration is a lie. Measured: BOTH original alternatives (`.role-split-item` and
       `[data-ai-role]`) appeared nowhere in the repo except inside that querySelectorAll itself, so
       the extraction had never once succeeded — the phantom class was removed and js/pages.js
       splitRow now emits stable `data-ai-role` hooks (data attributes are the machine contract; class
       names are styling and may change). Nothing about this is visible, so neither the screenshot nor
       the behavior e2e nor any other Check could catch it, and what breaks is the project's core bet:
       the machine-readable (AIO/agentic) surface. Class (`.x`) and attribute (`[x]`) selectors are
       resolved against the shipped leaves; tag/compound selectors are honestly excluded as
       statically ambiguous. Same used⟹defined wiring lens as Checks 375 / 376 / 391 / 392 / 395.
       The scan set is DERIVED (main.js + every js/*.js), not just the file that happened to hold the
       WebMCP tool, so moving the tool into a leaf cannot silently drop it out of coverage and every
       other scan is held to the same contract (the polarity lesson of Checks 124 / 361: a NEW file is
       guarded by default). The resolution corpus includes index.html, because static markup emits
       attributes the JS never writes — measured: `[data-bgm-btn]` exists ONLY in index.html, and as a
       BARE attribute (`<button data-bgm-btn id=…>`), so quoted-string matching alone reported a false
       positive; attribute selectors are therefore also matched at HTML attribute position.
       `_EXT_POINTS411` allowlists the AIDK BindingRegistry attributes (`data-bind-text/show/list`):
       those are a documented agent-facing extension point ("AI は属性を付与するだけでよい") whose
       emitter count is legitimately zero, so requiring an emitter would be a false positive on
       intentional design. Measured non-vacuity in BOTH directions: a consumer-side typo
       (`[data-bgm-btn]` → `[data-bgm-button]`) and an emitter-side removal (renaming the attribute in
       index.html) each turn this Check RED.
       走査前にコメントを除去する —— しないと **説明コメント中の id 参照が実参照として
       数えられ**、定義側がリテラルでなくなった瞬間に false RED を出す (2026-08-11 に実際に
       発生: `aria-controls="nav-lab-body"` と書いた WHY コメントが dangling 参照と判定された)。
       Check 112 / 421 / 422 と同じ「コメントは違反にも充足にもしない」規律の idref 面。(BLOCKING)

  457. **配線されている shipped 資産は、配信面の sha256 照合対象に入っていること**
       (BLOCKING): `check_deployed_freshness.py` は「200 が返ること」と「中身が最新で
       あること」を分けて検査する層だが、その照合対象のうち **root の資産だけがハード
       コード** (`style.css` / `main.js` / `sw.js`) で、`js/` 配下だけが glob で導出されて
       いた。実測 (2026-08-26): index.html は root script を **5 本**読んでいるのに照合対象は
       main.js だけで、**error-suppressor.js / karte-init.js / theme-init.js / aio-guard.js の
       4 本が配信面で一度も検証されていなかった**。とくに aio-guard.js は AIO asset-anchor の
       self-repair monitor で、その silent な無効化を防ぐために Check 133 (「file が在る ⟹
       配線されている」) を足した面なのに、**配信されているのが古い / 壊れた版でも同じ silent な
       無効化が起きる** —— Check 133 はリポジトリ内の index.html を見るので配信面の齟齬は
       原理的に見えない。本 Check は index.html から**独立に**導出した配線集合が、tool の
       `shipped_sha256_targets()` に含まれることを強制する (ハードコードへ戻すと集合がずれて
       RED)。Check 415 が STATUS.md の workflow 網羅を生成器と独立に導出するのと同じ形。
       (BLOCKING)
"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check
    warnings = ctx.warnings

    # ── 132. AIO evidence ↔ sitemap discoverability (BLOCKING) ────────────────────
    # aio-manifest.json に authoritative evidence として登録された text doc (.md/.txt/.json) は
    # sitemap.xml の <loc> にも載っていなければならない。manifest は AI crawler 向けに doc を権威と
    # 宣言するが、sitemap 経由で discovery する crawler は sitemap 未掲載の登録 doc に到達できない
    # (silent discoverability gap。real-work-claims.md / AI2AI-archive.md が登録済なのに sitemap 欠落
    # だった)。binary (.webp/.mp3) は sitemap-index 対象外ゆえ除外。「evidence 登録 ⟹ sitemap 到達可」
    # を機械強制する。
    _manifest132 = ROOT / ".well-known" / "aio-manifest.json"
    _sitemap132 = ROOT / "sitemap.xml"
    if _manifest132.exists() and _sitemap132.exists():
        _mdata132 = json.loads(_manifest132.read_text(encoding="utf-8"))
        _sitemap_src132 = _sitemap132.read_text(encoding="utf-8")
        _ev_paths132 = []
        for _sec132 in ("source_of_truth", "supporting_evidence", "observational_evidence"):
            for _e132 in _mdata132.get(_sec132, []):
                _p132 = _e132.get("path", "")
                if _p132.endswith((".md", ".txt", ".json")):
                    _ev_paths132.append(_p132)
        _missing132 = [p for p in _ev_paths132 if ("/" + p + "<") not in _sitemap_src132 and ("/" + p + "\n") not in _sitemap_src132 and (p + "</loc>") not in _sitemap_src132]
        check(
            bool(_ev_paths132) and not _missing132,
            f"Check 132: aio-manifest の text evidence {len(_ev_paths132)} 件すべてが sitemap.xml に <loc> 掲載 (crawler discoverability)",
            f"Check 132: aio-manifest 登録 evidence が sitemap.xml に欠落: {_missing132} — "
            "登録済 doc は sitemap.xml にも <loc> を追加せよ (sitemap 経由 crawler が到達できない discoverability gap)"
            if _ev_paths132 else
            "Check 132: aio-manifest から text evidence path を抽出できない (manifest 構造を確認せよ)",
            blocking=True,
        )
    else:
        check(False, "Check 132: aio-manifest.json / sitemap.xml present",
              "Check 132: aio-manifest.json または sitemap.xml が無い — AIO evidence↔sitemap 整合を検証できない", blocking=True)

    # ── 133. AIO guard script wiring (BLOCKING) ───────────────────────────────────
    # aio-guard.js は AIO asset-anchor の lifecycle monitor & self-repair 機構で、hidden な
    # <div id="aio-asset-anchor"> を監視し AI の "dead code purge" 等で除去されたら復元する
    # (anchor は不可視だが AIO 層に semantically critical)。この monitor は index.html が main SPA
    # IIFE より前に aio-guard.js を実際に load して初めて稼働する。mirror-bijection は FILE の存在
    # しか見ないため、<script src="./aio-guard.js"> タグを消しても file は残り verify は緑のまま
    # monitor だけが silent に無効化される (従来は非ブロックの CI advisory だけが捕捉)。本 Check は
    # index.html が aio-guard.js を script 参照することを BLOCKING 強制し、「guard file 存在 ⟹ guard
    # が配線済」を invariant 化する (AIO self-repair monitor の回帰ガード)。
    _index133 = ROOT / "index.html"
    if _index133.exists():
        _html133 = _index133.read_text(encoding="utf-8")
        _wired133 = re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?aio-guard\.js["\']', _html133)
        check(
            bool(_wired133),
            "Check 133: index.html が aio-guard.js を <script src> 参照 (AIO self-repair monitor が配線済)",
            "Check 133: index.html に <script src=\"./aio-guard.js\"> 参照が無い — "
            "aio-guard.js (AIO asset-anchor self-repair monitor) が load されず silent に無効化される。"
            "main IIFE より前に <script src=\"./aio-guard.js\"></script> を index.html へ戻せ",
            blocking=True,
        )
    else:
        check(False, "Check 133: index.html present",
              "Check 133: index.html が無い — aio-guard.js の配線を検証できない", blocking=True)

    # ── 134. Root script wiring completeness (BLOCKING) ───────────────────────────
    # index.html が依存する root スクリプト (theme-init.js / karte-init.js / main.js) を
    # <script src> で実際に load し続けることを BLOCKING 強制する。Check 133 (aio-guard.js) と
    # 同様、mirror-bijection は FILE 存在しか見ず <script> タグの残存は強制されない。タグ除去は
    # silent に劣化する: theme-init.js は pre-paint FOUC ガード (除去すると未スタイル/誤テーマの
    # 一瞬の flash になるが behavior e2e は検査せず、screenshot e2e は §3(B) で advisory ゆえ block
    # しない)、karte-init.js は analytics を無音停止、main.js は SPA エントリポイント (除去は e2e が
    # 捕捉するが静的 check でエントリ配線を明示し e2e 不在時も生存させる)。error-suppressor.js は
    # inline ゆえ対象外 (Check 7/7b が inline byte-identity + CSP hash を強制)、aio-guard.js は
    # Check 133 が担当。「root script file 存在 ⟹ index.html に配線済」を残る外部 root script へ
    # invariant 化する。
    _index134 = ROOT / "index.html"
    if _index134.exists():
        _html134 = _index134.read_text(encoding="utf-8")
        _required134 = ["theme-init.js", "karte-init.js", "main.js"]
        _unwired134 = [
            _s for _s in _required134
            if not re.search(r'<script\b[^>]*\bsrc\s*=\s*["\']\.?/?' + re.escape(_s) + r'["\']', _html134)
        ]
        check(
            not _unwired134,
            f"Check 134: index.html が依存 root script {_required134} をすべて <script src> 配線 (silent degradation 防止)",
            f"Check 134: index.html に <script src> 配線が欠落: {_unwired134} — "
            "これらは除去しても file が残り verify 緑のまま silent に劣化する "
            "(theme-init.js=FOUC / karte-init.js=analytics / main.js=SPA entry)。index.html へ "
            "<script src> 参照を戻せ",
            blocking=True,
        )
    else:
        check(False, "Check 134: index.html present",
              "Check 134: index.html が無い — root script の配線を検証できない", blocking=True)

    # ── 403. sr-only AIO entity anchor の presence (BLOCKING) ─────────────────────
    # index.html の sr-only エンティティアンカー (<div id="aio-footer-entity"> の著作権/entity/
    # canonical ブロックと <footer id="aio-main-footer"> の RAG チャンクアンカー) は AIO 戦略上
    # load-bearing だが **視覚的に不可視** ゆえ、除去しても (a) pixel screenshot は無変化 (そもそも
    # advisory)、(b) behavior e2e は素通り、(c) consistency も無被覆 —— 完全に silent に消える。
    # 実測: <div id="aio-footer-entity"> ブロックを丸ごと削除しても e2e は PASS・consistency は
    # 0 errors だった。Check 133 (aio-guard.js の script 配線) が #aio-asset-anchor を守るのと同じ
    # 「不可視だが load-bearing な AIO 要素」class の entity-anchor 面を閉じる。
    # 判定は **要素** を見る (changelog コメント中の id 言及では PASS しない)。
    _html403 = ROOT / "index.html"
    _raw403 = _html403.read_text(encoding="utf-8") if _html403.exists() else ""
    # index.html 冒頭の changelog は HTML コメント内に `・<div id="aio-footer-entity">に…` のように
    # 要素リテラルを含む。コメントを除去せずに素の regex を当てると、**要素を丸ごと削除しても
    # コメントの言及だけで PASS する vacuous Check** になる (本 Check の非 vacuity 検証で実際に
    # そうなっていたのを mutation で検出し是正した)。判定前に必ずコメントを剥がす。
    _src403 = re.sub(r"<!--.*?-->", "", _raw403, flags=re.S)
    _anchors403 = [
        ("aio-footer-entity", r'<div[^>]*id="aio-footer-entity"'),
        ("aio-main-footer", r'<footer[^>]*id="aio-main-footer"'),
    ]
    _missing403 = [_n403 for _n403, _re403 in _anchors403 if not re.search(_re403, _src403)]
    check(
        bool(_src403) and not _missing403,
        f"Check 403: sr-only AIO entity anchor {[n for n, _ in _anchors403]} が index.html に要素として存在",
        f"Check 403: sr-only AIO entity anchor が index.html から消失: {_missing403} — "
        "著作権/entity/canonical ブロックと RAG チャンクアンカーは AIO 戦略上 load-bearing だが視覚的に "
        "不可視ゆえ、除去しても screenshot・behavior e2e・consistency のいずれも従来は捕捉できなかった "
        "(dead-code purge で silent に消える)。要素を復元せよ (本文の変更は C6 ゆえ aio-guardian 経由)",
        blocking=True,
    )

    # ── 411. WebMCP ツールの DOM セレクタ → 実描画への解決 (BLOCKING) ────────────────
    # main.js の WebMCP (agentic accessibility) ツールは `document.querySelectorAll('<sel>')` で
    # ページの DOM から証拠データを抽出すると *説明文で宣言* する。だがセレクタが実際に描画される
    # class / data 属性に解決しなければ、ツールは常に静的フォールバック文字列を返し、
    # 「現在の DOM 状態から抽出」という宣言は嘘になる (実測: `.role-split-item` も `[data-ai-role]` も
    # リポジトリ全体でこの querySelectorAll 自身にしか出現せず、抽出は一度も成功していなかった)。
    # 視覚に出ないため screenshot も behavior e2e も捕捉できない silent な claim↔実装 drift であり、
    # しかも壊れるのは本プロジェクトの中核賭け金である **機械可読 (AIO/agentic) 面**。
    # Check 375 (icon) / 376 (data-action) / 391 (getElementById) / 392 (aria idref) / 395 (navigate)
    # と同じ used⟹defined wiring レンズの WebMCP 面。
    _main411 = ROOT / "main.js"
    _leaves411 = sorted((ROOT / "js").glob("*.js"))
    _html411 = ROOT / "index.html"
    if _main411.exists() and _leaves411:
        # 走査は全 shipped JS から **導出** する (初版は main.js 限定だった)。WebMCP ツールが葉へ
        # 移っても守り続けるため、および ui-components 等の走査も同じ契約で縛るため。
        # 新規 file が既定で守られる極性 (Check 124/361 と同じ) を最初から取る。
        _scan411 = [_main411] + _leaves411
        _src411 = "\n".join(re.sub(r"(?<!:)//[^\n]*", "", _p411.read_text(encoding="utf-8"))
                            for _p411 in _scan411)
        # 解決先の corpus には index.html も含める。topbar 等の静的マークアップが属性を出しており
        # (実測: data-bgm-btn は index.html にのみ存在)、JS だけを見ると誤検出になる。
        _emitted411 = "".join(_p411.read_text(encoding="utf-8") for _p411 in _leaves411)
        _emitted_html411 = _html411.read_text(encoding="utf-8") if _html411.exists() else ""
        # 拡張点の allowlist: AIDK BindingRegistry の宣言的バインディング属性は
        # 「AI は属性を付与するだけでよい」ための **agent 向け拡張点** であり、現時点で
        # emitter が 0 なのは設計どおり (js/aidk-rails.js の設計コメントに明文化)。
        # 契約破れではないため used⟹defined の対象外とする。
        _EXT_POINTS411 = ("[data-bind-text]", "[data-bind-show]", "[data-bind-list]")
        _unresolved411 = []
        for _m411 in re.finditer(r"""querySelectorAll\(\s*['"]([^'"]+)['"]""", _src411):
            for _sel411 in [_s411.strip() for _s411 in _m411.group(1).split(",") if _s411.strip()]:
                if _sel411 in _EXT_POINTS411:
                    continue
                if _sel411.startswith("."):
                    _ok411 = f"'{_sel411[1:]}'" in _emitted411 or f'"{_sel411[1:]}"' in _emitted411 \
                        or f"{_sel411[1:]} " in _emitted411 or f" {_sel411[1:]}" in _emitted411
                elif _sel411.startswith("[") and _sel411.endswith("]"):
                    _attr411 = _sel411[1:-1]
                    # JS 側は h() の prop として引用符付きで出る。HTML 側は値なしの bare 属性
                    # (`<button data-bgm-btn id=…>`) がありうるため属性位置の正規表現で照合する
                    # (実測: data-bgm-btn は index.html にこの形でのみ存在し、引用符前提だと誤検出した)。
                    _ok411 = (f"'{_attr411}'" in _emitted411 or f'"{_attr411}"' in _emitted411
                              or bool(re.search(r"[\s]" + re.escape(_attr411) + r"(?=[\s=>])",
                                                _emitted_html411)))
                else:
                    continue  # タグ/複合セレクタは対象外 (静的解決が曖昧なため honest に除外)
                if not _ok411:
                    _unresolved411.append(_sel411)
        check(
            not _unresolved411,
            f"Check 411: 全 shipped JS ({len(_scan411)} file) の querySelectorAll セレクタが実描画に解決 (WebMCP の DOM 抽出契約が実在)",
            f"Check 411: querySelectorAll が実在しないセレクタを走査している: {sorted(set(_unresolved411))} — "
            "その走査は永遠に 0 件を返し、機能は静かに無効化される (WebMCP ツールなら「現在の DOM 状態から "
            "抽出」という宣言が嘘になる)。視覚に出ないため screenshot も behavior e2e も捕捉しない。"
            "描画側に data-ai-role 等の機械向けフックを足すか、セレクタを実描画 (js/ の h() prop または "
            "index.html の属性) に合わせよ。agent 向け拡張点として emitter 0 が設計なら "
            "_EXT_POINTS411 へ理由付きで追加せよ",
            blocking=True,
        )
    else:
        check(False, "Check 411: main.js and js/ leaves present",
              "Check 411: main.js または js/ の葉モジュールが無い — WebMCP セレクタ解決を検証できない", blocking=True)

    # ── 457. 配線されている shipped 資産 ⟹ 配信面の sha256 照合対象 (BLOCKING) ────────
    # 「file が在る ⟹ 配線されている」(Check 133/134/135) の**配信面**。リポジトリ内で
    # 配線されていても、公開されているのが古い / 壊れた版なら同じ silent な無効化が起きる。
    # index.html から独立に導出した集合が tool の導出結果に含まれることを見る。
    import importlib.util as _ilu457
    _tool457 = ROOT / ".github" / "scripts" / "check_deployed_freshness.py"
    _html457 = ROOT / "index.html"
    if not _tool457.exists() or not _html457.exists():
        warnings.append("Check 457: freshness tool か index.html が無い — 照合を skip")
    else:
        try:
            _spec457 = _ilu457.spec_from_file_location("_freshness457", _tool457)
            _mod457 = _ilu457.module_from_spec(_spec457)
            _spec457.loader.exec_module(_mod457)
            _targets457 = set(_mod457.shipped_sha256_targets())
        except Exception as _e457:  # noqa: BLE001 — tool 側の import 失敗も検査対象
            _targets457 = None
            check(False, "", f"Check 457: freshness tool から照合対象を取得できない ({_e457})",
                  blocking=True)
        if _targets457 is not None:
            _src457 = _html457.read_text(encoding="utf-8")
            _wired457 = set(re.findall(r'<script[^>]*src="\./([^"/]+\.js)"', _src457))
            _wired457 |= set(re.findall(
                r'<link[^>]*rel="stylesheet"[^>]*href="\./([^"/]+\.css)"', _src457))
            _missing457 = sorted(_wired457 - _targets457)
            check(
                not _missing457,
                f"Check 457: index.html が配線する root 資産 {len(_wired457)} 件が全て "
                f"配信面の sha256 照合対象 ({len(_targets457)} 件) に入っている",
                (f"Check 457: 配線されているのに配信面で照合されない資産がある: {_missing457}。"
                 "リポジトリ内の配線 (Check 133/134/135) は**公開されている中身**を見ないので、"
                 "古い / 壊れた版が配信されても silent に無効化される。"
                 "check_deployed_freshness.py の shipped_sha256_targets() は index.html から"
                 "**導出**せよ (ハードコードは配線の増減に追従しない)"),
                blocking=True,
            )
            # 457b: **導出の起点そのもの**が配信面で検証されていること。
            #   index.html は JSON-LD / CSP / meta / script 配線 / sr-only entity anchor を
            #   載せる最も影響の大きい 1 file なのに、以前は版数 (ai:version / ai:last-modified)
            #   の一致しか見ていなかった。実測 (2026-08-26): 直近 30 日で index.html は
            #   **7 commit で変更され、版数を上げたものは 0 件**。つまり版数チェックは
            #   中身を一切カバーしておらず、古い index.html が配信されても
            #   版数=緑 / 到達性=緑 (file は在る) / sha256=対象外 / リポジトリ側 Check=ローカル、
            #   で **どの層も検出しない**。
            check(
                "index.html" in _targets457,
                "Check 457b: 導出の起点 index.html 自身が配信面の sha256 照合対象に入っている",
                ("Check 457b: index.html が配信面で sha256 照合されていない。版数 "
                 "(ai:version / ai:last-modified) は**中身が変わっても動かない** "
                 "(実測: 直近 30 日で index.html は 7 commit 変更・版数 bump は 0 件) ので、"
                 "版数一致は『最新の index.html が配信されている』ことの証拠にならない。"
                 "JSON-LD / CSP / meta / script 配線 / sr-only entity anchor を載せる"
                 "最も影響の大きい file が silent に古いままになる"),
                blocking=True,
            )
            # 457c: **機械向けの宣言面**も配信面で内容が検証されていること。
            #   実測 (2026-08-26): discovery 層 13 件のうち **10 件は 200 が返ることしか
            #   見られていなかった**。人間向けの shipped 資産 (JS/CSS/HTML) は byte 照合して
            #   いるのに、**このプロジェクトの中核の賭けである機械向けの面だけが存在確認どまり**
            #   という逆転が起きていた。壊れ方も重い —— 古い robots.txt はクローラの到達範囲を
            #   変え、古い .well-known/* は agent が読む契約そのものを変え、古い
            #   aio-manifest.json は **agent へ誤った digest を宣言する**。
            try:
                _disc457 = set(_mod457.discovery_sha256_targets(_src457))
            except Exception as _ed457:  # noqa: BLE001
                _disc457 = None
                check(False, "", f"Check 457c: discovery 層の照合対象を取得できない ({_ed457})",
                      blocking=True)
            if _disc457 is not None:
                import subprocess as _sp457
                _wk457 = {ln.strip() for ln in _sp457.run(
                    ["git", "ls-files", ".well-known"], cwd=str(ROOT),
                    capture_output=True, text=True, check=True).stdout.splitlines() if ln.strip()}
                _want457 = _wk457 | {"robots.txt", "sitemap.xml", "manifest.webmanifest"}
                _want457 = {w for w in _want457 if (ROOT / w).is_file()}
                _gap457 = sorted(_want457 - _disc457 - _targets457)
                check(
                    not _gap457,
                    f"Check 457c: 機械向けの宣言面 {len(_want457)} 件が全て配信面の "
                    f"sha256 照合対象に入っている",
                    (f"Check 457c: 配信面で内容が検証されない機械向け宣言面がある: {_gap457}。"
                     "**200 が返ることと中身が最新であることは別**で、"
                     "古い robots.txt はクローラの到達範囲を変え、古い .well-known/* は agent が"
                     "読む契約そのものを変え、古い aio-manifest.json は agent へ誤った digest を"
                     "宣言する。しかも人間には何も見えない。"
                     "discovery_sha256_targets() は宣言面から**導出**せよ"),
                    blocking=True,
                )
