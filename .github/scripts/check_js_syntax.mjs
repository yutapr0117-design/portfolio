#!/usr/bin/env node
/**
 * check_js_syntax.mjs — `npm run lint:js` の実体 (BLOCKING syntax gate)
 *
 * 【なぜこの file があるか】
 * 従来の `lint:js` は `node --check <file>` を 40 個並べた && chain だった。これは
 * **shipped JS 40 file 中 35 file (87.5%) に対して何も検査していなかった**。
 *
 *   実測 (node v26.3.0 / 2026-08-22):
 *     js/brand.js の createBrand 本体に `let let = 1;` を植える
 *       → `node --check js/brand.js`  … rc=0   ← 素通り
 *       → `npm run lint` (ESLint)     … rc=1   ← "Parsing error: The keyword 'let' is reserved"
 *
 * 原因は package.json に `"type": "module"` が無いこと。node は拡張子 .js を
 * CommonJS として parse し、失敗すると module-syntax detection で ESM として
 * 再 parse するが、**その再 parse の SyntaxError を報告せず exit 0 する**。
 * 同じ壊れた file を `"type":"module"` 下に置くと rc=1 になることも実測済み。
 *
 * package.json に `"type":"module"` を足す一行修正は採れない —— **e2e spec 62 file が
 * すべて `require()` を使っており**、BLOCKING merge gate である behavior e2e が丸ごと
 * 動かなくなる (実測)。よって「file ごとに、その file が実際に走る mode で parse する」
 * runner を置く。
 *
 * 【mode の決め方】
 * ESM 構文 (top-level の import / export) を持つ file は module mode、持たない file は
 * classic script mode。後者は index.html が `<script src>` (type=module なし) で読む
 * root script と service worker で、ブラウザでの読まれ方と一致する。
 * 判定は **コメントを除去してから** 行う (block comment 中の "export" を実装と誤認する
 * class を避ける —— この file を書く過程で実際に踏んだ)。
 *
 * 【非 goal (正直に記録)】
 * classic script が誤って `export` を獲得した場合、この gate は module mode へ分類して
 * 素通しする。ブラウザは classic script として throw するので実害はあるが、それは
 * 「syntax が妥当か」ではなく「module 配線が妥当か」の invariant で、Check 43d / 47 系の
 * 担当面。ここで曖昧に兼務させない。
 */

import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import vm from 'node:vm';

const files = process.argv.slice(2);
if (files.length === 0) {
    console.error('check_js_syntax: no files given (usage: node check_js_syntax.mjs <file>...)');
    process.exit(2);
}

/** block/line コメントを潰す (文字列リテラル内の "//" を守るため、素朴だが保守的な走査)。 */
function stripComments(src) {
    let out = '';
    let i = 0;
    let quote = null;
    while (i < src.length) {
        const c = src[i];
        const next = src[i + 1];
        if (quote) {
            if (c === '\\') { out += '  '; i += 2; continue; }
            if (c === quote) { quote = null; }
            out += c === '\n' ? '\n' : ' ';
            i += 1;
            continue;
        }
        if (c === '"' || c === "'" || c === '`') { quote = c; out += ' '; i += 1; continue; }
        if (c === '/' && next === '*') {
            i += 2;
            while (i < src.length && !(src[i] === '*' && src[i + 1] === '/')) {
                out += src[i] === '\n' ? '\n' : ' ';
                i += 1;
            }
            i += 2;
            out += '  ';
            continue;
        }
        if (c === '/' && next === '/') {
            while (i < src.length && src[i] !== '\n') { out += ' '; i += 1; }
            continue;
        }
        out += c;
        i += 1;
    }
    return out;
}

const ESM_SYNTAX = /^[ \t]*(?:import|export)[\s{('"*;]/m;

let failed = 0;
for (const file of files) {
    let src;
    try {
        src = readFileSync(file, 'utf8');
    } catch (err) {
        console.error(`check_js_syntax: cannot read ${file} — ${err.message}`);
        failed += 1;
        continue;
    }

    const isModule = ESM_SYNTAX.test(stripComments(src));

    if (isModule) {
        // module mode は file 引数では正しく効かない (上の WHY) ので stdin 経由で渡す。
        // node は診断に "[stdin]" と出すため、file 名はこちらで補って帰属可能にする。
        const res = spawnSync(process.execPath, ['--input-type=module', '--check'], {
            input: src,
            encoding: 'utf8'
        });
        if (res.status !== 0) {
            const detail = (res.stderr || '').replace(/\[stdin\]/g, file).trimEnd();
            console.error(`✖ ${file} (module)\n${detail}\n`);
            failed += 1;
        }
    } else {
        // classic script は vm.Script が V8 の parser をそのまま通す (実行はしない)。
        try {
            new vm.Script(src, { filename: file });
        } catch (err) {
            console.error(`✖ ${file} (script)\n${err.stack || err.message}\n`);
            failed += 1;
        }
    }
}

if (failed > 0) {
    console.error(`check_js_syntax: ${failed} of ${files.length} file(s) failed to parse`);
    process.exit(1);
}
console.log(`check_js_syntax: ${files.length} files OK`);
