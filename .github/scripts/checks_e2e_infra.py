"""
checks_e2e_infra.py — e2e / Playwright test-infrastructure hygiene checks
(extracted from check_repository_consistency.py — check.py split track・category "e2e/test-infra").

This module owns the (non-contiguous) cluster of Checks 110/111/114/116/117 that keep the
Playwright behavior-e2e harness sound: e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection (110),
the no-`networkidle` wait guard (111), the no-`.only` guard (114), playwright.config
reuseExistingServer=false (116), and the screenshot tolerance sanity ceiling (117). They were
interleaved with 112 (IME guard・shipped-JS→checks_behavioral sibling) / 113 (canon discipline) /
115 (CSP・html-dependent), which stay in the monolith. Each Check reads its own target files
directly (e2e/*.spec.js, playwright.config.cjs) via Path.read_text(); none depends on the
monolith's global html/style/mainjs content. Executed together at Check 110's original position;
order-independent since each only appends to the shared errors/warnings (proven byte-identical
via full-output diff).

Self-integrity: aggregated by _aggregate_check_numbers() via CHECK_SOURCE_FILES (Checks 45/70/105
span this file). run(ctx) receives shared check()/ROOT by reference (exec 不使用), so append
semantics / BLOCKING propagation / exit code are byte-equivalent to the monolith.

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection: the axe a11y test loops over A11Y_ROUTES
       asserting zero render-neutral critical violations per route; this Check asserts that
       A11Y_ROUTES's hash set equals ALL_ROUTES's hash set, so a route added to the route-render
       coverage (ALL_ROUTES) but forgotten in the a11y coverage (A11Y_ROUTES) is caught — no shipped
       route can silently escape automated accessibility scanning (the a11y counterpart of Check 58). (BLOCKING)
  111. e2e no-networkidle guard: no e2e/*.spec.js may call
       waitForLoadState('networkidle') anywhere except inside the screenshot regression test
       (recognised by a toHaveScreenshot call within a few lines). networkidle waits for ALL
       network to settle, but the site loads external Google Fonts and a service-worker SWR
       background fetch, so on CI it can never reach idle and the wait hangs to the 30s test
       timeout (the hang flake fixed repo-wide in PR #132). Behavior tests must synchronise via
       'domcontentloaded' + expect() auto-wait instead; only the screenshot capture legitimately
       needs networkidle (font/image load determinism). This Check blocks reintroduction of the
       hang-flake class. (BLOCKING)
  432. e2e no-declarative-skip guard: `test.skip('title', fn)` / `test.describe.skip('title', fn)`
       のように **第 1 引数が文字列リテラル** の skip を BLOCKING で禁止する。この形は
       「テストごと宣言的に無効化する」もので、失敗しているテストを黙らせる最短経路でありながら
       **CI は緑のまま**になり、覆っていたはずの挙動が誰にも気付かれず無防備になる
       (Check 114 の `.only` = 他が全部 skip される、の裏返し。あちらは「1 本だけ走る」、
       こちらは「1 本だけ走らない」)。**runtime の条件付き skip とは区別する**:
       `test.skip(cond, 'reason')` を test 本体の中で呼ぶ形は第 1 引数が式なので対象外で、
       実際 `portfolio.spec.js` の screenshot baseline 不在時 skip がこれに当たる (正当な用途)。
       #1141 (登録したのに probe に乗っていなかった mutation) / #1142 (登録したのに実行されない
       Check モジュール) と同じ **「登録されているのに実行されない」** class の e2e 面。(BLOCKING)

  114. e2e no-`.only` guard: no e2e/*.spec.js may contain `test.only` /
       `describe.only` / `test.describe.only`. A stray `.only` makes Playwright run ONLY that
       test and silently skip every other test, so CI passes green while the suite is gutted
       (a false-green footgun, the inverse of the vacuous-gate class). This Check blocks any
       `.only(` left in the spec. (BLOCKING)
  116. playwright.config.cjs reuseExistingServer=false: the Playwright webServer must NOT
       reuse an existing server. If flipped to true, CI/local could test a stale already-running
       dev server (pre-edit state) and pass green while the committed files are broken — a
       false-green vector. This Check asserts `reuseExistingServer: false` and rejects `: true`. (BLOCKING)
  117. playwright.config.cjs screenshot tolerance sanity ceiling: `toHaveScreenshot`'s
       `maxDiffPixelRatio` must stay <= 0.05. Per Session Record #20 §3(B) the screenshot
       regression test is now ADVISORY (non-blocking observation), not the merge gate — but the
       tolerance ceiling still matters so the advisory OBSERVATION stays meaningful: loosening it
       (e.g. 0.5) would make the observation blind to real visual drift. This Check caps the
       tolerance so the visual-regression signal cannot be gutted by a config tweak. (BLOCKING)
  402. e2e 不在アサーションの描画確定ガード: `toHaveCount(0)` / `not.toBeVisible()` /
       `not.toBeAttached()` は **初回 poll で成立するとそれ以上再検査されない**ため、SPA の非同期
       描画とレースすると「まだ描画されていない」を「無い」と誤認して vacuous に PASS し、機能が
       壊れていても緑になる (#825 が #830 でまさにこの理由により vacuous と発覚した実例がある)。
       本 Check は各 e2e spec を走査し、不在アサーションの直前 14 行以内で「最後の goto/reload」の
       後に settle が無いものを BLOCKING で禁止する。settle と認めるのは (a) positive な auto-wait
       assertion (toBeVisible / toHaveText / toContainText / toHaveAttribute / toHaveURL /
       toHaveValue / toBeFocused / toBeEnabled / toBeDisabled / toBeChecked / toHaveCount(n>0)) と
       (b) locator 相互作用 (click/fill/type/check/selectOption/hover — actionability 待ちを伴う。
       `page.keyboard.press` は locator を持たず待たないので除外)。修正は「直前に positive を 1 行
       足す」だけで済むため false-positive でも実害が小さい。Check 111 (networkidle 禁止) /
       Check 130 (oninput の State.update 禁止) と同じ「e2e/実装の構造的落とし穴を静的に封じる」系。
       検出は **matcher 自体** (`toHaveCount(0)` 等) を行単位で見る。初版は `await expect(` が
       matcher と同一行にあることを要求しており、多行に折り返した assertion を丸ごと見逃していた
       (実測: navigation-a11y.spec.js の nav-link ループ = 全 sidebar リンクが NotFound に落ちない
       ことを検査する重要な gate が未検出だった)。行全体がコメントの行は判定から除外する。
       (BLOCKING)

  416. BLOCKING behavior ゲートが第三者 CDN から切り離されていること。実測では
       1 ナビゲーションごとに **6 つの第三者ホストへ 9 リクエスト** が飛び (KARTE ×4 /
       Google Fonts ×2)、`page.goto()` の既定 waitUntil='load' が **その完了を待って**いた。
       suite 全体で ~334 ナビゲーションあるため、ゲートの合否が外部 CDN の可用性と
       レイテンシに依存していた (2026-08-10 に `.hero-section` の 30s timeout として
       実際に flake 化し、rerun 1 回で緑になった)。本 Check は
       (a) playwright.config.cjs が `E2E_HERMETIC` を読んで `--host-resolver-rules` を
           launchOptions に渡すこと、
       (b) playwright-regression.yml の behavior ステップ (`--grep-invert
           "screenshot regression"`) が `E2E_HERMETIC` を設定していること、
       (c) screenshot ステップには **設定しない**こと (実フォントで撮られた baseline を
           壊さないための意図的な非対称。ここが崩れると ADVISORY の視覚シグナルが
           恒久的に無意味になる)、
       (d) `mutation_probe.py` の e2e 実行も `E2E_HERMETIC` を渡すこと — **probe では通常の
           CI 以上に重要**で、外部 CDN の一時失敗で test が落ちると probe はそれを
           「mutation を捕捉した」と報告する = **false CAUGHT**。安全網の自己検証そのものが
           嘘をつくうえ、週次実行ゆえ誰も rerun せず気付けない
       の 4 点を BLOCKING 強制する。env-gate 自体は MUTATION_PROBE と同じ作法。(BLOCKING)
"""
import re


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 110. e2e A11Y_ROUTES ↔ ALL_ROUTES coverage bijection (BLOCKING) ────────────
    # axe a11y テスト (A11Y_ROUTES でループ) は render-neutral critical 違反ゼロを全ルートで機械強制
    # するが、その対象集合 A11Y_ROUTES が手動配列ゆえ、新ルートを ALL_ROUTES (route-render が網羅) に
    # 足したのに A11Y_ROUTES へ足し忘れると「新ルートが a11y 未検証」の silent coverage gap が生じる。
    # 両配列の hash 集合が一致することを機械強制し、a11y カバレッジが shipped route 集合を常に追従する
    # ことを保証する (Check 58 の e2e↔main.js route 版の a11y 面)。
    # A11Y_ROUTES (a11y-axe.spec.js) と ALL_ROUTES (security-proxy.spec.js) は e2e spec の
    # テーマ別分割 (2026-07-07) で別ファイルに移動したため、e2e/*.spec.js 全体を連結して照合する。
    _specs110 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs110:
        _src110 = "\n".join(p.read_text(encoding="utf-8") for p in _specs110)
        _a11y_m110 = re.search(r"const A11Y_ROUTES\s*=\s*\[(.*?)\]", _src110, re.DOTALL)
        _all_m110 = re.search(r"const ALL_ROUTES\s*=\s*\[(.*?)\];", _src110, re.DOTALL)
        _a11y_set110 = set(re.findall(r"'([^']+)'", _a11y_m110.group(1))) if _a11y_m110 else set()
        _all_set110 = set(re.findall(r"hash:\s*'([^']+)'", _all_m110.group(1))) if _all_m110 else set()
        _only_all110 = sorted(_all_set110 - _a11y_set110)
        _only_a11y110 = sorted(_a11y_set110 - _all_set110)
        check(
            bool(_a11y_set110) and bool(_all_set110) and _a11y_set110 == _all_set110,
            f"Check 110: e2e A11Y_ROUTES ({len(_a11y_set110)}) covers exactly the ALL_ROUTES hash set ({len(_all_set110)}) — a11y axe runs on every shipped route",
            f"Check 110: a11y coverage drift — in ALL_ROUTES but missing from A11Y_ROUTES (a11y 未検証ルート): "
            f"{_only_all110}; in A11Y_ROUTES but not ALL_ROUTES: {_only_a11y110}. e2e の A11Y_ROUTES を同期せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 110: e2e/*.spec.js not found — a11y coverage bijection を検証できない", blocking=True)

    # ── 111. e2e no-networkidle guard (BLOCKING) ──────────────────────────────────
    # `waitForLoadState('networkidle')` は全ネット通信が 500ms 落ち着くのを待つが、本サイトは外部
    # Google Fonts と service worker の SWR background fetch を持つため、CI のネット遅延窓では idle に
    # 到達せず 30s test-timeout までハングする (PR #132 で repo 全体を root-fix した hang flake クラス)。
    # behavior テストは 'domcontentloaded' + expect() の auto-wait で同期すべきで、networkidle が正当
    # なのは screenshot capture (フォント/画像ロードの決定化が必要) のみ。本 Check は screenshot テスト
    # 以外での networkidle 再導入を pre-commit でブロックし flake クラスの再発を構造的に封じる。
    # 許容判定: networkidle 行の直後数行以内に toHaveScreenshot があれば screenshot テスト内とみなす。
    # spec テーマ別分割 (2026-07-07) 後は e2e/*.spec.js 全体を走査する。networkidle が正当なのは
    # screenshot regression テスト (portfolio.spec.js に残置) のみ。
    _specs111 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs111:
        _viol111 = []
        for _sp111 in _specs111:
            _lines111 = _sp111.read_text(encoding="utf-8").splitlines()
            for _i111, _line111 in enumerate(_lines111):
                if "waitForLoadState('networkidle')" in _line111 or 'waitForLoadState("networkidle")' in _line111:
                    _window111 = "\n".join(_lines111[_i111:_i111 + 6])
                    if "toHaveScreenshot" not in _window111:
                        _viol111.append(f"{_sp111.name}:{_i111 + 1}")
        check(
            not _viol111,
            f"Check 111: e2e/*.spec.js ({len(_specs111)}) uses waitForLoadState('networkidle') only in the screenshot regression test",
            f"Check 111: e2e/*.spec.js: waitForLoadState('networkidle') が screenshot テスト外の {_viol111} に存在 — "
            f"'domcontentloaded' + expect() auto-wait を使え (networkidle は外部 Fonts/SW で CI hang する。PR #132 参照)",
            blocking=True,
        )
    else:
        check(False, "", "Check 111: e2e/*.spec.js not found — networkidle guard を検証できない", blocking=True)

    # ── 114. e2e no-`.only` guard (BLOCKING) ──────────────────────────────────────
    # Playwright で test.only / describe.only が 1 つでも残ると、その test だけが走り他は全 skip され、
    # CI は緑のまま suite が空洞化する (false-green footgun = vacuous-gate の裏返し)。spec 内の
    # `(test|describe).only(` を検出して BLOCKING で禁止し、デバッグ用 .only の commit 漏れを封じる。
    _specs114 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs114:
        _only114 = []
        for _sp114 in _specs114:
            _src114 = _sp114.read_text(encoding="utf-8")
            _only114 += [f"{_sp114.name}:{_m}" for _m in re.findall(r"\b(?:test|describe)(?:\.[A-Za-z]+)*\.only\s*\(", _src114)]
        check(
            not _only114,
            f"Check 114: e2e/*.spec.js ({len(_specs114)}) に test.only/describe.only が無い (false-green footgun 防止)",
            f"Check 114: e2e/*.spec.js に .only が {len(_only114)} 個ある ({_only114[:5]}) — 全 suite が skip され CI が false-green 化する。.only を除去せよ",
            blocking=True,
        )
    else:
        check(False, "", "Check 114: e2e/*.spec.js not found — no-.only guard を検証できない", blocking=True)

    # ── 116. playwright.config.cjs reuseExistingServer=false (BLOCKING) ────────────
    # reuseExistingServer:true だと既に起動中の dev server を再利用し、commit 前の stale 状態を検証して
    # CI が緑になる false-green vector。`reuseExistingServer: false` の存在 + `: true` の不在を機械強制。
    _pwcfg = ROOT / "playwright.config.cjs"
    _pwsrc = _pwcfg.read_text(encoding="utf-8") if _pwcfg.exists() else ""
    if _pwcfg.exists():
        _reuse_ok = bool(re.search(r"reuseExistingServer\s*:\s*false\b", _pwsrc)) and \
            not re.search(r"reuseExistingServer\s*:\s*true\b", _pwsrc)
        check(
            _reuse_ok,
            "Check 116: playwright.config.cjs reuseExistingServer が false (stale-server false-green 防止)",
            "Check 116: playwright.config.cjs の reuseExistingServer が false でない — 既存 server 再利用で stale 状態を検証し false-green 化する。false に戻せ",
            blocking=True,
        )
    else:
        check(False, "", "Check 116: playwright.config.cjs not found — webServer 設定を検証できない", blocking=True)

    # ── 117. playwright.config.cjs screenshot tolerance sanity ceiling (BLOCKING) ──
    # maxDiffPixelRatio を緩めすぎると §3 baseline ゲートが本物の視覚 regression を見逃す。<=0.05 を強制。
    if _pwcfg.exists():
        _mdpr = re.search(r"maxDiffPixelRatio\s*:\s*([0-9.]+)", _pwsrc)
        _mdpr_val = float(_mdpr.group(1)) if _mdpr else None
        check(
            _mdpr_val is not None and _mdpr_val <= 0.05,
            f"Check 117: playwright.config.cjs maxDiffPixelRatio={_mdpr_val} <= 0.05 (§3 baseline 感度を維持)",
            f"Check 117: maxDiffPixelRatio={_mdpr_val} が sanity ceiling 0.05 を超過 (or 未設定) — 緩めると視覚 regression を見逃す。締め直せ",
            blocking=True,
        )
    else:
        check(False, "", "Check 117: playwright.config.cjs not found — screenshot tolerance を検証できない", blocking=True)

    # ── 402. e2e 不在アサーションの描画確定ガード (BLOCKING) ───────────────────────────
    # `toHaveCount(0)` / `not.toBeVisible()` は **初回 poll で成立するとそれ以上再検査されない**。
    # SPA の非同期描画とレースすると「まだ描画されていない」を「無い」と誤認して vacuous に PASS し、
    # 機能が壊れていても緑になる (#825 が #830 でこの理由により vacuous と発覚した実例がある)。
    # ゆえに不在アサーションの前には、直近の goto/reload 以降に「必ず在るはず」の要素を待つ
    # positive assertion (toBeVisible 等) か locator 相互作用 (click/fill 等は actionability 待ちを
    # 伴うため settle とみなす) が無ければならない。修正は「先に positive を 1 行足す」だけで済む。
    # [FIX] 初版は `await expect(...)` が **matcher と同一行** にあることを要求していたため、
    #   多行に折り返した assertion (`await expect(\n  locator,\n  msg\n).toHaveCount(0);`) を
    #   丸ごと見逃していた (実測: navigation-a11y.spec.js の nav-link ループ = 全 sidebar リンクが
    #   NotFound に落ちないことを検査する重要な gate が未検出だった)。matcher 自体を検出対象にし、
    #   行全体がコメントの行は producer/settle 判定から除外する (説明文中の記述で誤検出しないため)。
    _abs402 = re.compile(r"(?<!not\.)(?:toHaveCount\(0\)|not\.toBeVisible\(\)|not\.toBeAttached\(\))")
    _pos402 = re.compile(r"(?:toBeVisible|toHaveText|toContainText|toBeFocused|toHaveAttribute|toHaveURL|toHaveValue|toBeEnabled|toBeDisabled|toBeChecked)\(")
    _poscount402 = re.compile(r"toHaveCount\((?!0\))")
    _inter402 = re.compile(r"(?<!keyboard)\.(?:click|fill|type|check|uncheck|selectOption|hover|dblclick)\(")
    _nav402 = re.compile(r"page\.(?:goto|reload)\(")
    _cmt402 = re.compile(r"\s*(?://|\*|/\*)")
    _e2e_dir402 = ROOT / "e2e"
    _bad402 = []
    if _e2e_dir402.is_dir():
        for _f402 in sorted(_e2e_dir402.glob("*.spec.js")):
            _lines402 = _f402.read_text(encoding="utf-8").splitlines()
            for _i402, _l402 in enumerate(_lines402):
                if _cmt402.match(_l402) or not _abs402.search(_l402):
                    continue
                _nav_at, _settle_at = -1, -1
                for _j402 in range(max(0, _i402 - 14), _i402):
                    if _cmt402.match(_lines402[_j402]):
                        continue
                    if _nav402.search(_lines402[_j402]):
                        _nav_at = _j402
                    if (_pos402.search(_lines402[_j402]) or _poscount402.search(_lines402[_j402])
                            or _inter402.search(_lines402[_j402])):
                        _settle_at = _j402
                if _nav_at > _settle_at:
                    _bad402.append(f"{_f402.name}:{_i402 + 1}")
    check(
        _e2e_dir402.is_dir() and not _bad402,
        f"Check 402: e2e の不在アサーションはすべて描画確定後に評価される ({len(_bad402)} offenders)",
        f"Check 402: goto/reload 直後に positive な settle 無しで不在アサーションを評価している箇所: "
        f"{_bad402[:8]} — toHaveCount(0)/not.toBeVisible() は初回 poll で成立すると再検査されないため、"
        "SPA の非同期描画とレースして「まだ描画されていない」を「無い」と誤認し vacuous に PASS する "
        "(#825/#830 class)。直前に「必ず在るはず」の要素の toBeVisible 等を 1 行足して描画を確定させよ",
        blocking=True,
    )

    # ── 416. BLOCKING behavior ゲートが第三者 CDN から切り離されている (BLOCKING) ────────
    # 実測: 1 ナビゲーションごとに 6 ホストへ 9 リクエスト (KARTE / Google Fonts) が飛び、
    # goto の既定 waitUntil='load' がそれを待っていた = ゲートの合否が外部依存。遮断後は
    # goto 447ms → 39ms。screenshot ステップにだけは付けない (実フォント baseline を守る)。
    _cfg416 = (ROOT / "playwright.config.cjs").read_text(encoding="utf-8", errors="replace")
    _wf416p = ROOT / ".github" / "workflows" / "playwright-regression.yml"
    _wf416 = _wf416p.read_text(encoding="utf-8", errors="replace") if _wf416p.exists() else ""
    _cfg_ok416 = ("E2E_HERMETIC" in _cfg416) and ("host-resolver-rules" in _cfg416)
    # NOTE: コメント行を先に落とす。初版はここを素の substring で見ており、**同じ step 内の
    # 説明コメントに書いた "E2E_HERMETIC" を実設定と誤認して**、env を丸ごと削っても GREEN の
    # ままだった (自分で非 vacuity を測って気付いた comment-match vacuous PASS)。
    # 判定は「YAML の mapping キーとしての `E2E_HERMETIC:`」に限定する。
    _wf_nc416 = "\n".join(_l for _l in _wf416.splitlines() if not _l.lstrip().startswith("#"))
    _steps416 = re.split(r"\n      - name: ", _wf_nc416)
    _behavior416 = [_st for _st in _steps416 if 'grep-invert "screenshot regression"' in _st]
    _shot416 = [_st for _st in _steps416 if re.search(r'--grep\s+"screenshot regression"', _st)]
    _env_re416 = re.compile(r"^\s*E2E_HERMETIC\s*:", re.M)
    _beh_ok416 = bool(_behavior416) and all(_env_re416.search(_st) for _st in _behavior416)
    _shot_ok416 = all(not _env_re416.search(_st) for _st in _shot416)
    # (d) mutation probe の e2e 実行も hermetic であること。probe では外部起因の失敗が
    # 「捕捉した」と誤報告される (false CAUGHT) ため、通常 CI より重要度が高い。
    _probe416 = (ROOT / ".github" / "scripts" / "mutation_probe.py").read_text(encoding="utf-8", errors="replace")
    _probe_nc416 = "\n".join(_l for _l in _probe416.splitlines() if not _l.lstrip().startswith("#"))
    _probe_ok416 = bool(re.search(r'"E2E_HERMETIC"\s*:', _probe_nc416))
    _why416 = []
    if not _probe_ok416:
        _why416.append("mutation_probe.py の e2e 実行が E2E_HERMETIC を渡していない (外部起因の失敗が false CAUGHT になる)")
    if not _cfg_ok416:
        _why416.append("playwright.config.cjs が E2E_HERMETIC / host-resolver-rules を持たない")
    if not _behavior416:
        _why416.append('behavior ステップ (--grep-invert "screenshot regression") が見つからない')
    elif not _beh_ok416:
        _why416.append("behavior ステップが E2E_HERMETIC を設定していない")
    if not _shot_ok416:
        _why416.append("screenshot ステップに E2E_HERMETIC が付いている (実フォント baseline が壊れる)")
    check(
        _cfg_ok416 and _beh_ok416 and _shot_ok416 and _probe_ok416,
        "Check 416: BLOCKING behavior ゲートが第三者 CDN から切り離されている (E2E_HERMETIC 配線)",
        ("Check 416: behavior ゲートの hermetic 配線が崩れている: " + " / ".join(_why416)
         + " — ゲートの合否が KARTE / Google Fonts の可用性に依存すると、"
           "コードが正しくても外部起因で赤くなり (実測 2026-08-10 に flake)、"
           "rerun 頼みの運用が常態化して安全網の信頼性が落ちる"),
        blocking=True,
    )

    # ── 432. e2e no-declarative-skip guard (BLOCKING) ─────────────────────────────
    # `test.skip('title', fn)` は **テストごと宣言的に無効化する**形で、失敗を黙らせる最短経路
    # なのに CI は緑のまま = 覆っていた挙動が無防備になったことに誰も気付けない (Check 114 の
    # `.only` の裏返し: あちらは「1 本だけ走る」、こちらは「1 本だけ走らない」)。
    # **runtime の条件付き skip は対象外**: `test.skip(cond, 'reason')` を test 本体で呼ぶ形は
    # 第 1 引数が式ゆえ正当 (portfolio.spec.js の baseline 不在時 skip が実例)。
    # 判定は「第 1 引数が文字列リテラルか」で行い、両者を構文的に分ける。
    _specs432 = sorted((ROOT / "e2e").glob("*.spec.js"))
    if _specs432:
        _skip432 = []
        _re432 = re.compile(r"""\b(?:test|describe)(?:\.[A-Za-z]+)*\.skip\s*\(\s*['"`]""")
        for _sp432 in _specs432:
            for _i432, _ln432 in enumerate(_sp432.read_text(encoding="utf-8").splitlines(), 1):
                if _re432.search(_ln432):
                    _skip432.append(f"{_sp432.name}:{_i432}")
        check(
            not _skip432,
            f"Check 432: e2e/*.spec.js ({len(_specs432)}) に宣言的 skip (test.skip('title', fn)) が無い "
            f"(条件付き runtime skip は対象外)",
            (f"Check 432: 宣言的な test.skip が {len(_skip432)} 個ある ({_skip432[:5]}) — "
             "テストごと無効化されているのに CI は緑のままで、覆っていた挙動が無防備になったことに"
             "誰も気付けない。落ちるテストは黙らせずに直すか、削除して理由を spec に残せ。"
             "実行時の条件で飛ばしたいなら test 本体の中で `test.skip(cond, 'reason')` を使う "
             "(第 1 引数が式なら本 Check の対象外)"),
            blocking=True,
        )
    else:
        check(False, "", "Check 432: e2e/*.spec.js not found — declarative-skip guard を検証できない",
              blocking=True)
