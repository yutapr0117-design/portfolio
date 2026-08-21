---
file: .github/scripts/check_js_syntax.mjs
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-22
canonical-ref: package.json / .github/scripts/checks_structural_ci.py (Check 46a-46d)
---

# .github/scripts/check_js_syntax.mjs

## What

`npm run lint:js` の実体。package.json が引数で渡す shipped JS 40 file を、**その file が実際に走る mode**（ESM module / classic script）で V8 に parse させ、構文エラーがあれば file 名・行番号つきで報告して exit 1 する BLOCKING syntax gate。

## Why

従来の `lint:js` は `node --check <file>` を 40 個 `&&` で連ねたものだったが、**40 file 中 35 file (87.5%) に対して何も検査していなかった**。

実測（node v26.3.0 / 2026-08-22）:

| 仕掛け | `node --check js/brand.js` | `npm run lint` (ESLint) |
|---|---|---|
| `js/brand.js` の `createBrand` 本体に `let let = 1;` を植える | **rc=0（素通り）** | rc=1 `Parsing error: The keyword 'let' is reserved` |

原因は package.json に `"type": "module"` が無いこと。node は拡張子 `.js` を CommonJS として parse し、失敗すると module-syntax detection で ESM として再 parse するが、**その再 parse の SyntaxError を報告せずに exit 0 する**。同じ壊れた file を `"type":"module"` 下に置くと rc=1 になることも実測で確認済み。

`"type":"module"` を足す一行修正は採れない —— **e2e spec 62 file がすべて `require()` を使っており**、BLOCKING merge gate である behavior e2e が丸ごと動かなくなる（実測）。よって file ごとに mode を選ぶ runner を置いた。

なお、この期間にサイトが壊れていた事実はない。ESLint (`npm run lint`) が同じ 40 file を parse しており実際に検出する（上表）。塞いだのは **gate が名ばかりだったこと** であって、shipped code の欠陥ではない。

## How (usage)

```bash
npm run lint:js          # package.json が 40 file を引数で渡す
node .github/scripts/check_js_syntax.mjs main.js js/brand.js   # 個別実行も可
```

出力:

```
check_js_syntax: 40 files OK
```

失敗時（実測）:

```
✖ js/brand.js (module)
js/brand.js:36
    let let = 1;
        ^^^
SyntaxError: Unexpected strict mode reserved word
check_js_syntax: 1 of 40 file(s) failed to parse
```

## Constraints

- **mode 判定**: コメントを除去した source に top-level の `import` / `export` があれば module、無ければ classic script。実測で **module 35 / script 5**（script = `sw.js` / `aio-guard.js` / `error-suppressor.js` / `theme-init.js` / `karte-init.js`）＝ index.html が `<script src>` で読む root script と service worker に一致する。コメント除去を先に行うのは、block comment 中の "export" を実装と誤認する class を避けるため（この file を書く過程で実際に踏んだ）。
- **module mode は stdin 経由**。`node --input-type=module --check` は file 引数では効かないため source を stdin に流す。node は診断に `[stdin]` と出すので、runner 側で file 名へ置換して帰属可能にしている。
- **classic script は `vm.Script`**（in-process・V8 の parser をそのまま通す・実行はしない）。
- **非 goal（正直に記録）**: classic script が誤って `export` を獲得した場合、この gate は module へ分類して素通しする。ブラウザは classic script として throw するので実害はあるが、それは「syntax が妥当か」ではなく「module 配線が妥当か」の invariant で、Check 43d / 47 系の担当面。ここで曖昧に兼務させない。
- **C1**: 外部依存ゼロ（`node:fs` / `node:child_process` / `node:vm` のみ）。
- 実行時間は実測 **約 1.8 秒**（40 file・module 35 件を spawn）。

## Change impact

- file 一覧は package.json の `lint:js` が単一の与え手。**Check 46a** が `lint` の一覧と一致することを、**Check 46b** がそれがディスク上の shipped JS（root ∪ `js/`）と一致することを BLOCKING で強制する。
- **Check 46c** が「lint:js がこの runner に配線されていること」を、**Check 46d** が「bare `node --check <file>` の形へ戻していないこと」を BLOCKING で強制する（46d は旧 script に対して RED になる＝この gate が名ばかりへ戻る経路を構造的に塞ぐ）。
- runner の path を変えるなら package.json・checks_structural_ci.py の `_RUNNER46`・本 doc を同一 commit で同期すること。

## Audience-specific notes

- **AI（後続実装者）**: 「gate が緑」と「gate が見ている」は別物。この file はその distinction の実例で、**87.5% の file に対して何も見ていない gate が長期間緑を返し続けていた**。新しい gate を足したら、動機となった欠陥を実際に植えて RED を実測すること。
- **監査人**: 非 vacuity は両 mode で実証済み —— module 面（`js/brand.js` に `let let`）・script 面（`theme-init.js` に `function broken( {`）でいずれも rc=1、clean tree で rc=0。
- **人間（新卒）**: 「構文チェックが通った」は「そのツールが実際にその file を読んだ」を意味しない。ツールの既定の解釈（ここでは CommonJS）が対象と食い違うと、黙って何もしないことがある。
