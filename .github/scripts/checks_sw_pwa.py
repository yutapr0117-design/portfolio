"""
checks_sw_pwa.py — service-worker & PWA registration + potentialAction structure checks (251-254, 388)
(extracted from check_repository_consistency.py — check.py split track).

run(ctx) receives shared check()/ROOT by reference (exec 不使用) so exit code / BLOCKING propagation
are byte-equivalent. annotation+def-aware free-var 分析で外部 `_`-var・global-content 依存ゼロ確認済。
nested-fn の module-level `global _accNNN` は run() 内で `nonlocal` へ機械変換 (意味等価)。

Check inventory (Check 45 enforces sync with the `# ── N.` sections in run()):
  251. JSON-LD `potentialAction` block has required `@type` + `target`:
       every `potentialAction` block in index.html static JSON-LD MUST
       have a non-empty `@type` (Schema.org Action subclass — e.g.
       ReadAction / SearchAction) AND a `target` field (URL string or
       array). Drift would silently break AI/voice assistant action
       invocation. Sibling of Check 209 (target canonical prefix) for
       the potentialAction required-fields axis. (BLOCKING)

  252. sw.js registers `install` + `activate` + `fetch` event handlers:
       service-worker code MUST register all 3 event listeners. Drift
       (silent removal of any) breaks SW lifecycle (no install → no
       cache prefill, no activate → no cleanup, no fetch → no offline /
       SWR). Sibling of Check 19 (CACHE_NAME version) for the SW
       lifecycle handler presence axis. (BLOCKING)

  253. main.js registers `navigator.serviceWorker.register('./sw.js'`:
       main.js MUST contain a `navigator.serviceWorker.register('./sw.js'`
       call. Silent removal would mean sw.js exists but never installs
       on visiting browsers — Check 252 confirms the SW has handlers, but
       without registration the SW is dead code. Sibling of Check 252
       (SW handlers) for the SW registration call-site axis. (BLOCKING)

  448. **公開 discovery index が我々自身の契約に適合すること (BLOCKING)**:
       `.well-known/agent-skills/index.json` の各 entry が name / type / description / url /
       digest を持ち、digest が `sha256:{hex}` であること。実測 (2026-08-23): **`description`
       が全 entry で欠落**し、digest 形式も `sha-256:{hex}` (ハイフン付き) だった。
       **⚠ 2026-09-25 訂正 (#225)**: 旧版の本 Check はこの 5 field を **Agent Skills 仕様の
       要求**と述べ、宣言した `$schema` への適合を強制していた。**その仕様にこの index は
       存在しない** —— 仕様が定めるのは SKILL.md のディレクトリ形式と frontmatter
       (name / description 必須・**license は optional**) だけで、discovery index も
       `.well-known` も `$schema` も一切定義していない (仕様サイト全 9 ページ + 公式 repo を
       対照つきで実測)。しかも宣言していた host `schemas.agentskills.io` は**権威 NS が
       NXDOMAIN を返し、Wayback にも記録が無い**。**我々は読めたことのない仕様を典拠に
       していた。** 5 field 自体は保持する —— 根拠が「仕様の要求」から「我々の設計判断」へ
       変わっただけで、progressive disclosure (name と description だけで関連性を判断する)
       は仕様が実際に述べている。
       **(448b)** `$schema` を置くなら**我々が配信する origin に限る** ——
       自分で用意できない schema への適合は主張できない。
       **(448c)** `documentation` が実在する repo 内 file へ解決すること。**偽の pointer を
       消すだけでは「形式を知る手段」が減るだけ**なので、到達可能な説明（mirror doc・公開面で
       200 を実測）を指す形へ置き換えたうえで、**指す先が在ることを機械で縛る** ——
       **URL を宣言して誰も確かめない状態は、#225 の欠陥そのものだからである。**
       とくに `description` の欠落は痛い —— 仕様の設計は「agent は起動時に **name と description
       だけ**を読んで関連性を判断し、一致したときに初めて本体を取得する」という progressive
       disclosure なので、**description が無いと agent は中身を取ってみるまで用途が判らない**。
       必須 field 名は本 Check にリテラルで持つ (外部仕様なので repo から導出できない) が、
       **仕様が変わったら本 Check も同一 commit で更新する**契約とする。
  254. .well-known/index.json skill name uniqueness + digest format:
       every entry in `.well-known/index.json` `skills[]` MUST satisfy:
       (a) non-empty `name` field, all unique within the file;
       (b) `digest` field matches `^sha256:[0-9a-f]{64}$` (Agent Skills 仕様形式). Drift would
       silently break agent-skills discovery (duplicate name causes
       conflict, malformed digest causes mismatch). Sibling of Check 5
       (.well-known/index.json byte-identical mirror) for the schema
       structural validity axis. (BLOCKING)

  388. sw.js `isBotRequest` (via `BOT_UA_PATTERNS`) MUST detect every
       known live-fetch AI-agent User-Agent as a bot, so those agents get
       a cache-bypassed (`no-store`) FRESH copy of the AIO files
       (llms.txt / llms-full.txt) instead of a stale-while-revalidate
       cached body. The curated UA set is the AI agents that actively
       DEREFERENCE URLs (GPTBot / ChatGPT-User / OAI-SearchBot / ClaudeBot
       / Claude-User / Claude-SearchBot / PerplexityBot / Googlebot /
       Bingbot / Applebot / CCBot). This Check parses BOT_UA_PATTERNS from
       sw.js and replicates isBotRequest's substring match; a miss means
       that agent silently receives potentially-stale AIO content — a
       direct AIO-strategy regression. Discovered drift: `Claude-User`
       (Anthropic's on-demand fetch UA, declared in robots.txt) matched
       NONE of the old patterns ('claudebot' ⊄ 'claude-user', no bare
       'claude', no 'bot' substring) → served stale AIO. Fixed by
       broadening 'claudebot'→'claude'. Sibling of Check 252 (sw.js
       handlers present) for the sw.js AI-agent freshness axis. (BLOCKING)

"""
import re
import json


def run(ctx):
    ROOT = ctx.ROOT
    check = ctx.check

    # ── 251. JSON-LD potentialAction has required @type + target (BLOCKING) ───────
    # index.html JSON-LD の全 `potentialAction` block が `@type` (Schema.org Action
    # subclass) AND `target` を持つことを BLOCKING 強制。drift で AI/voice assistant の
    # action invocation 破壊。Check 209 (target canonical prefix) の required-fields 軸。
    _idx251 = ROOT / "index.html"
    if _idx251.exists():
        _isrc251 = _idx251.read_text(encoding="utf-8")
        _blocks251 = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            _isrc251,
            flags=re.DOTALL,
        )
        _violations251: list[str] = []
        _pa_count251 = 0
        def _walk251(node: object, path: str) -> None:
            nonlocal _pa_count251
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "potentialAction":
                        if isinstance(v, dict):
                            _pa_count251 += 1
                            if not isinstance(v.get("@type"), str) or not v.get("@type", "").strip():
                                _violations251.append(f"{path}.potentialAction @type 欠落/空")
                            if "target" not in v:
                                _violations251.append(f"{path}.potentialAction target 欠落")
                        elif isinstance(v, list):
                            for _i, _it in enumerate(v):
                                _pa_count251 += 1
                                if not isinstance(_it, dict):
                                    _violations251.append(f"{path}.potentialAction[{_i}] non-dict")
                                    continue
                                if not isinstance(_it.get("@type"), str) or not _it.get("@type", "").strip():
                                    _violations251.append(f"{path}.potentialAction[{_i}] @type 欠落/空")
                                if "target" not in _it:
                                    _violations251.append(f"{path}.potentialAction[{_i}] target 欠落")
                    if isinstance(v, list):
                        for item in v:
                            _walk251(item, f"{path}.{k}")
                    else:
                        _walk251(v, f"{path}.{k}")
            elif isinstance(node, list):
                for i, item in enumerate(node):
                    _walk251(item, f"{path}[{i}]")
        for _bi, _blk in enumerate(_blocks251):
            try:
                _data251 = json.loads(_blk)
            except json.JSONDecodeError:
                continue
            _walk251(_data251, f"block{_bi}")
        _ok251 = _pa_count251 > 0 and not _violations251
        check(
            _ok251,
            f"Check 251: potentialAction {_pa_count251} block 全て @type + target 保有",
            (f"Check 251: 違反: {_violations251!r} — AI/voice assistant action invocation 破壊。"
             "@type (Schema.org Action subclass) + target を付与せよ"
             if _violations251 else
             "Check 251: potentialAction 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 251: index.html present",
              "Check 251: index.html が無い", blocking=True)

    # ── 252. sw.js registers install + activate + fetch handlers (BLOCKING) ───────
    # sw.js が install / activate / fetch 3 event handler を全て登録することを
    # BLOCKING 強制。silent 欠落で SW lifecycle 破壊 (precache 不能 / cleanup 不能 /
    # offline+SWR 不能)。Check 19 (CACHE_NAME version) の SW handler presence 軸。
    _sw252 = ROOT / "sw.js"
    if _sw252.exists():
        _ssrc252 = _sw252.read_text(encoding="utf-8")
        _required_evts252 = ["install", "activate", "fetch"]
        _missing252: list[str] = []
        for _e in _required_evts252:
            _pat = re.compile(
                r'(?:self|globalThis)\s*\.\s*addEventListener\s*\(\s*[\'"]' + re.escape(_e) + r'[\'"]'
            )
            if not _pat.search(_ssrc252):
                _missing252.append(_e)
        _ok252 = not _missing252
        check(
            _ok252,
            f"Check 252: sw.js registers {_required_evts252!r} handlers (all 3)",
            (f"Check 252: missing SW handlers: {_missing252!r} — SW lifecycle 破壊 "
             "(precache/cleanup/offline 不能)。self.addEventListener で 3 event 全登録"),
            blocking=True,
        )
    else:
        check(False, "Check 252: sw.js present",
              "Check 252: sw.js が無い", blocking=True)

    # ── 253. main.js calls navigator.serviceWorker.register('./sw.js' (BLOCKING) ──
    # main.js が `navigator.serviceWorker.register('./sw.js'` を呼ぶことを BLOCKING
    # 強制。silent 欠落で sw.js handler は存在しても install されず offline+SWR 機能
    # 全停止。Check 252 (handler presence) の register call-site 軸。
    _main253 = ROOT / "main.js"
    if _main253.exists():
        _msrc253 = _main253.read_text(encoding="utf-8")
        _has253 = re.search(
            r"navigator\s*\.\s*serviceWorker\s*\.\s*register\s*\(\s*['\"]\./sw\.js['\"]",
            _msrc253,
        ) is not None
        check(
            _has253,
            "Check 253: main.js が navigator.serviceWorker.register('./sw.js'...) を呼ぶ",
            ("Check 253: main.js に navigator.serviceWorker.register('./sw.js') 呼び出しが無い — "
             "sw.js handlers (Check 252) は存在しても install されず offline+SWR 停止。"
             "main.js の SW 登録 call-site を復元せよ"),
            blocking=True,
        )
    else:
        check(False, "Check 253: main.js present",
              "Check 253: main.js が無い", blocking=True)

    # ── 254. .well-known/index.json skill name uniqueness + digest format (BLOCKING) ─
    # .well-known/index.json の skills[] 各 entry の name が非空+block 内 unique で、
    # digest が `sha256:<64-hex>` regex に一致することを BLOCKING 強制。Check 5
    # (byte-identical mirror) の schema structural validity 軸。
    _widx254 = ROOT / ".well-known" / "index.json"
    if _widx254.exists():
        try:
            _wd254 = json.loads(_widx254.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e254:
            _wd254 = None
        _skills254 = _wd254.get("skills", []) if isinstance(_wd254, dict) else []
        _bad254: list[str] = []
        _names254: list[str] = []
        # Agent Skills Discovery 仕様は `sha256:{hex}` (ハイフン無し)。2026-08-23 に是正。
        _digest_re254 = re.compile(r"^sha256:[0-9a-f]{64}$")
        for _i, _s in enumerate(_skills254):
            if not isinstance(_s, dict):
                _bad254.append(f"skills[{_i}]: non-dict")
                continue
            _nm = _s.get("name")
            if not isinstance(_nm, str) or not _nm.strip():
                _bad254.append(f"skills[{_i}]: name 欠落/空")
            else:
                _names254.append(_nm)
            _dg = _s.get("digest")
            if not isinstance(_dg, str) or not _digest_re254.match(_dg):
                _bad254.append(f"skills[{_i}].digest={_dg!r} format 不正 (sha256:<64-hex>)")
        from collections import Counter as _Counter254
        _dupes254 = [n for n, c in _Counter254(_names254).items() if c > 1]
        if _dupes254:
            _bad254.append(f"name 重複: {_dupes254!r}")
        _ok254 = len(_skills254) > 0 and not _bad254
        check(
            _ok254,
            f"Check 254: .well-known/index.json skills ({len(_skills254)} 件) 全て name 一意 + digest 形式正",
            (f"Check 254: 違反: {_bad254!r} — agent-skills discovery 破壊。"
             "name 一意 + digest=sha256:<64-hex> へ整理"
             if _bad254 else
             "Check 254: .well-known/index.json skills 0 件 — vacuous-fail"),
            blocking=True,
        )
    else:
        check(False, "Check 254: .well-known/index.json present",
              "Check 254: .well-known/index.json が無い", blocking=True)

    # ── 388. sw.js isBotRequest detects known live-fetch AI-agent UAs (BLOCKING) ──
    # sw.js は AIO ファイル (llms.txt/llms-full.txt) を bot には no-store で fresh 提供、humans には
    # SWR で提供する。実際に URL を dereference する AI エージェント UA が BOT_UA_PATTERNS の
    # いずれにも substring 一致しないと、その agent は SWR の stale なキャッシュ本文を受け取り
    # (背景 revalidate は間に合わない) AIO 戦略が silent に劣化する。robots.txt が宣言し実 fetch する
    # AI UA を curated し、sw.js の BOT_UA_PATTERNS を parse して isBotRequest の substring 判定を
    # 再現、全 UA が検出されることを強制する。発見 drift: Claude-User が旧パターンのどれにも
    # 非一致 ('claudebot'⊄'claude-user' / bare 'claude' なし / 'bot' 部分文字列なし) で stale AIO を
    # 受け取っていた (→ 'claudebot'→'claude' で是正)。
    _sw388 = ROOT / "sw.js"
    if _sw388.is_file():
        _ssrc388 = _sw388.read_text(encoding="utf-8")
        _m388 = re.search(r"const\s+BOT_UA_PATTERNS\s*=\s*\[(.*?)\]", _ssrc388, re.DOTALL)
        if not _m388:
            check(False, "Check 388: sw.js BOT_UA_PATTERNS array parseable",
                  "Check 388: sw.js に BOT_UA_PATTERNS 配列が見つからない — bot 判定の source が不在",
                  blocking=True)
        else:
            _patterns388 = [
                _s.lower() for _s in re.findall(r"['\"]([^'\"]+)['\"]", _m388.group(1))
            ]
            # 実際に URL を dereference する AI エージェント UA (robots.txt 宣言と整合)
            _ai_uas388 = [
                "GPTBot", "ChatGPT-User", "OAI-SearchBot", "ClaudeBot", "Claude-User",
                "Claude-SearchBot", "PerplexityBot", "Googlebot", "Bingbot", "Applebot", "CCBot",
            ]
            _undetected388 = [
                _ua for _ua in _ai_uas388
                if not any(_p in _ua.lower() for _p in _patterns388)
            ]
            check(
                not _undetected388,
                f"Check 388: sw.js isBotRequest が既知 AI-fetch UA {len(_ai_uas388)} 件を全て bot 判定 (fresh AIO)",
                (f"Check 388: sw.js BOT_UA_PATTERNS が検出しない AI-fetch UA: {_undetected388!r} — "
                 "これらは cache-bypass されず SWR の stale AIO を受け取り AIO 戦略が劣化する。"
                 "BOT_UA_PATTERNS に substring パターンを追加せよ (例 'claude' が Claude-* を網羅)"),
                blocking=True,
            )
    else:
        check(False, "Check 388: sw.js present",
              "Check 388: sw.js が無い — AI-agent freshness を検証できない", blocking=True)

    # ── 448. Agent Skills Discovery 仕様への適合 (BLOCKING) ────────────────────────────
    # **旧版は「宣言した $schema に適合しなければ agent に拒否される」を根拠にしていたが、
    #   その $schema の host は存在しなかった** (2026-09-25 実測・#225)。守る対象は我々自身の契約。
    # 実測 (2026-08-23): 必須 field `description` が全 entry で欠落し、digest も仕様の
    # `sha256:{hex}` ではなく `sha-256:{hex}` だった —— **公開しているのに使われない**状態。
    # description の欠落がとくに痛いのは、仕様の設計が「起動時は name と description だけを
    # 読んで関連性を判断する」progressive disclosure だから (無いと中身を取るまで用途不明)。
    _SKILL_REQUIRED448 = ("name", "type", "description", "url", "digest")
    # 448b が使う 2 つの値。**origin は決め打ちにせず sitemap の最初の <loc> から導出する**
    #   —— 決め打ちだと canonical が動いたとき「我々の origin」の定義だけが取り残される。
    _ORIGIN448 = ""
    _sm448b = ROOT / "sitemap.xml"
    if _sm448b.exists():
        _m448b = re.search(r"<loc>\s*(https?://[^<\s]+?)/?\s*</loc>", _sm448b.read_text(encoding="utf-8"))
        if _m448b:
            _ORIGIN448 = _m448b.group(1).rstrip("/")
    _seen448 = {}
    for _p448b in (ROOT / ".well-known" / "index.json",
                   ROOT / ".well-known" / "agent-skills" / "index.json"):
        if _p448b.exists():
            try:
                _seen448[_p448b.name if _p448b.parent.name == ".well-known"
                         else f"agent-skills/{_p448b.name}"] = json.loads(
                             _p448b.read_text(encoding="utf-8"))
            except Exception:
                pass   # JSON 破損は Check 343 / 448 本体が別途 BLOCKING で捕捉する

    _skidx448 = ROOT / ".well-known" / "agent-skills" / "index.json"
    if not _skidx448.is_file():
        check(False, "", "Check 448: .well-known/agent-skills/index.json が無い "
                         "(RFC 8615 の規定位置なので、agent はここを見に来る)", blocking=True)
    else:
        try:
            _sk448 = json.loads(_skidx448.read_text(encoding="utf-8"))
        except json.JSONDecodeError as _e448:
            _sk448 = None
            check(False, "", f"Check 448: agent-skills/index.json が JSON として壊れている: {_e448}",
                  blocking=True)
        if _sk448 is not None:
            _bad448 = []
            _skills448 = _sk448.get("skills")
            if not isinstance(_skills448, list) or not _skills448:
                _bad448.append("skills が非空の配列でない (仕様上 required)")
            else:
                for _i448, _e in enumerate(_skills448):
                    if not isinstance(_e, dict):
                        _bad448.append(f"skills[{_i448}] が object でない")
                        continue
                    _miss = [_k for _k in _SKILL_REQUIRED448 if not _e.get(_k)]
                    if _miss:
                        _bad448.append(f"skills[{_i448}] ({_e.get('name', '?')}) に必須 field 欠落: {_miss}")
                    _d = _e.get("description")
                    if isinstance(_d, str) and len(_d) > 1024:
                        _bad448.append(f"skills[{_i448}] description が 1024 字超 ({len(_d)})")
                    _t = _e.get("type")
                    if _t not in (None, "document", "archive"):
                        _bad448.append(f"skills[{_i448}] type={_t!r} は我々の語彙外 (document / archive のみ)")
            # 448b — **外部の schema への適合を主張しないこと** (2026-09-25・#225)。
            #   この index は 2026-08-23 から `$schema:
            #   https://schemas.agentskills.io/discovery/0.2.0/schema.json` を宣言していたが、
            #   **その host は存在しない** (親ゾーン agentskills.io の権威 NS が NXDOMAIN + SOA
            #   を返す・Wayback に記録 0 件・Agent Skills の仕様サイト全 9 ページと公式 repo の
            #   どちらにも `schemas.agentskills.io` も `.well-known` も 1 件も無い)。
            #   **我々が自分で用意できない schema への適合は主張できない。**
            #   再混入を防ぐため、`$schema` を置くなら **我々が配信する origin に限る**。
            for _f448b, _doc448b in _seen448.items():
                _sch448b = _doc448b.get("$schema")
                if _sch448b and not str(_sch448b).startswith(_ORIGIN448):
                    _bad448.append(
                        f"{_f448b}: $schema={_sch448b!r} は我々が配信しない origin —— "
                        "自分で用意できない schema への適合は主張できない (#225)")
            # 448c — **`documentation` は実在する repo 内 file へ解決すること** (2026-09-25・#225)。
            #   偽の `$schema` を消すだけでは「形式を知る手段」が減るだけなので、**到達可能な説明**
            #   （mirror doc・公開面で 200 を実測）を指す形へ置き換えた。ただし **URL を宣言して
            #   誰も確かめない**のは、まさに今回の欠陥そのものなので、指す先が repo に在ることを
            #   機械で縛る。**別の URL で同じ欠陥を作り直さないための層である。**
            for _f448c, _doc448c in _seen448.items():
                _u448c = _doc448c.get("documentation")
                if not _u448c:
                    _bad448.append(f"{_f448c}: documentation が無い —— 形式を知る手段が公開面に存在しない")
                    continue
                if not str(_u448c).startswith(_ORIGIN448):
                    _bad448.append(f"{_f448c}: documentation={_u448c!r} は我々が配信しない origin")
                    continue
                _rel448c = str(_u448c)[len(_ORIGIN448):].lstrip("/")
                if not (ROOT / _rel448c).exists():
                    _bad448.append(
                        f"{_f448c}: documentation={_u448c!r} が repo 内に解決しない ({_rel448c}) —— "
                        "宣言だけが残り誰も確かめない状態は #225 の欠陥そのもの")

            check(
                not _bad448,
                (f"Check 448: agent-skills/index.json が**我々自身の**契約に適合 "
                 f"({len(_sk448.get('skills') or [])} skills / 5 field / 外部 schema 主張なし)"),
                (f"Check 448: agent-skills/index.json が契約に適合していない: {_bad448}。"
                 "**⚠ この 5 field は Agent Skills 仕様の要求ではない** —— 仕様が定めるのは "
                 "SKILL.md のディレクトリ形式と frontmatter (name / description 必須・license は "
                 "optional) だけで、**discovery index も `.well-known` も `$schema` も一切定義して"
                 "いない** (2026-09-25 に仕様サイト全 9 ページと公式 repo で実測・#225)。"
                 "旧版の本 Check はこれを『仕様の要求』と述べていたが、**その仕様は読めた例が無い**。"
                 "ここで守っているのは**我々自身が決めた形**であり、根拠は「index を読む agent は "
                 "name と description だけで関連性を判断し、一致したときに初めて本体を取得する」"
                 "という progressive disclosure の設計 (これは仕様が実際に述べている)"),
                blocking=True,
            )
