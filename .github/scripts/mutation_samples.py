#!/usr/bin/env python3
"""mutation_samples.py — Curated mutation DATA for mutation_probe.py (runner is separate).

mutation_probe.py (runner / completeness-critic) から**データのみ**を分離した葉モジュール。
肥大化解消 (自走効率 + 保守性): runner ロジックと curated mutation データを分ける。さらに
データ自体も log-rotation 方式で分割した (1000 行しきい値対応):

- MUTATIONS_ARCHIVE  : mutation_samples_archive.py (最古 / rotated part 1)。
- MUTATIONS_ARCHIVE2 : mutation_samples_archive2.py (次に古い / rotated part 2, 2026-07-28 新設)。
- 本ファイル tail    : 新しい側の entries (新規追記は常に本ファイルの MUTATIONS 末尾へ)。
- MUTATIONS          : ARCHIVE + ARCHIVE2 + tail の連結 (mutation_probe が import する公開 API・不変)。
- E2E_MUTATIONS      : behavior e2e 安全網用 (--e2e モード)。

【追記規約 (生じないように / 恒久)】新規 mutation は本ファイルの MUTATIONS 末尾 (tail) に追記する。
本ファイルが ~900 行を超えたら、最古の tail entries を最新の archive part へ移して rotate する。
part 1/2 が Check 365 の 1,000 cap に近接したら part をさらに増やす (mutation_samples_archive3.py 等)。

各 mutation の意味・非 vacuous 保証・実行機構は mutation_probe.py の docstring を参照。
本ファイルはデータ (dict の list) のみで、副作用も実行ロジックも持たない。
"""
from __future__ import annotations

import sys

if sys.version_info < (3, 10):
    print("ERROR: mutation_samples.py requires Python 3.10+ (got %d.%d)" % sys.version_info[:2])
    sys.exit(1)

from mutation_samples_common import ROOT, CHECK, CURRENT_DRAFT, CURRENT_DRAFT_VER, PREVIOUS_VER  # noqa: F401 (entry 内で参照)
from mutation_samples_archive import MUTATIONS_ARCHIVE
from mutation_samples_archive4 import MUTATIONS_ARCHIVE4
from mutation_samples_archive3 import MUTATIONS_ARCHIVE3
from mutation_samples_archive2 import MUTATIONS_ARCHIVE2
from mutation_samples_e2e_archive import E2E_MUTATIONS_ARCHIVE
from mutation_samples_e2e_archive3 import E2E_MUTATIONS_ARCHIVE3
from mutation_samples_e2e_archive2 import E2E_MUTATIONS_ARCHIVE2

# 新しい側の curated mutation (新規追記は本リスト末尾へ / 上記「追記規約」参照)。
_MUTATIONS_TAIL = [
    # 注: Check 362 (mutation anchor resolution) の curated meta-mutation は敢えて置かない。
    # anchor を orphan 化する mutation は mutation_samples.py 自身の `"find":` 行を quote する
    # 自己参照になり、mutation_probe の replace(find, replace, 1) が先頭 (= その mutation 自身の
    # find 値) に当たって挙動が不安定になるため。Check 362 の非 vacuous 性は手動で実証済
    # (mutation の file を誤り先へ変えると Check 362 が RED・restore で緑)。
]

# 公開 API: archive(古) + archive2 + tail(新) の連結。mutation_probe.py が import する (順序 = 時系列)。










# ── Check 441 (ACD-1.0 ライセンス本文の構造整合と配線) ──────────────────────────
# NOTE: **Check 442 (binary metadata の到達可能性) には mutation を登録できない。**
#   mutation_probe は対象 file を `read_text(encoding="utf-8")` で読むので、WebP / MP3 は
#   UnicodeDecodeError になり適用そのものが成立しない。非 vacuity は 2026-08-23 に手動で
#   実測済 (COMM の size を過大値へ戻す → 442a/442b が RED / RIFF size を 1 ずらす → 442c が RED)。
#   RED を実測できない mutation を安全網に混ぜないための非登録であって、被覆漏れではない。


































































































































































_MUTATIONS_TAIL.append({
    "name": 'Check 71: §4 BUDGET-DATA に存在しない file の行を足す —— 改名・削除の後に予算表だけが古いまま残る (59 も同時に発火)',
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": '.github/scripts/mutation_samples_archive4.py | 950 | advisory',
    "replace": '.github/scripts/mutation_samples_archive4.py | 950 | advisory\n.github/scripts/does-not-exist.py | 100 | advisory',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 50: lint script に旧 eslintrc 時代の flag を戻す —— flat config へ移行した設定が黙って無視される',
    "file": ROOT / "package.json",
    "find": '"lint": "eslint main.js',
    "replace": '"lint": "eslint --no-eslintrc main.js',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 47: 葉 module の export 名を変える —— main.js の import と export の契約が崩れる',
    "file": ROOT / "js" / "brand.js",
    "find": 'export function createBrand(storage) {',
    "replace": 'export function createBrandX(storage) {',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 26: aio-manifest が宣言する archive-2 の Session Record 範囲をずらす —— AIO 層の宣言と実体が食い違う',
    "file": ROOT / ".well-known" / "aio-manifest.json",
    "find": '#15-#30',
    "replace": '#15-#29',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 75: incident-artifacts の README 目録から 1 件を落とす —— 記録はあるのに目録から辿れなくなる',
    "file": ROOT / "docs" / "incident-artifacts" / "README.md",
    "find": '- `improvement-notes-claude-v80-phase4-gate-truth-audit.md`\n',
    "replace": '',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 100: theme-init.js が読む storage key を constants.js とずらす —— 初回描画前のテーマ復元が黙って効かなくなる (FOUC)',
    "file": ROOT / "theme-init.js",
    "find": "localStorage.getItem('portfolio_enhanced_v45')",
    "replace": "localStorage.getItem('portfolio_enhanced_v46')",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 386: sitemap の 1 件の <loc> を存在しない file へ —— crawler が 404 を踏む',
    "file": ROOT / "sitemap.xml",
    "find": '<loc>https://yutapr0117-design.github.io/portfolio/AI2AI.md</loc>',
    "replace": '<loc>https://yutapr0117-design.github.io/portfolio/AI2AI-missing.md</loc>',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 388: sw.js の bot UA 一覧から claude を外す —— AI agent の live fetch が SWR キャッシュの古い応答を受け取る',
    "file": ROOT / "sw.js",
    "find": "'gptbot', 'chatgpt', 'claude', ",
    "replace": "'gptbot', 'chatgpt', ",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 471 (j): 同じ文書に同じ ## 見出しをもう 1 つ置く —— § 参照の着地点が決まらなくなる "
            "(2026-11-01 に jurisdictions.md の「## 9.」と AS-OF.md の同一節で実測・portfolio-bb の発見)",
    "file": ROOT / "LICENSES" / "AS-OF.md",
    "find": "## Status of this submission\n",
    "replace": "## Status of this submission\n\n## Status of this submission\n",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 394: pomodoro の集中時間の UI 側 clamp の上限だけを変える —— UI で入力できた値が reload 後に store の clamp で黙って戻る',
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": 'settings.work = clamp(parseInt(e.target.value, 10) || 25, 1, 180)',
    "replace": 'settings.work = clamp(parseInt(e.target.value, 10) || 25, 1, 240)',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 365: 追跡テキストを 1,000 行超にする —— 全非 A テキスト ≤1,000 行の capstone が肥大化を止めることの確認",
    "file": ROOT / "CONTRIBUTING.md",
    "find": '# Contributing\n',
    "replace": '# Contributing\n' + "\n" * 1001,
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 389: topbar のテーマ切替ボタンの accessible name を sidebar とずらす —— 同じ機能のボタンが 2 つの名前を名乗る (WCAG 4.1.2)',
    "file": ROOT / "js" / "theme.js",
    "find": 'return `テーマを切り替える（現在: ${label}）`;',
    "replace": 'return `テーマ切替（現在: ${label}）`;',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 387: .well-known/mcp.json の同一 origin の pointer を存在しない file へ —— agent が dereference すると 404 になる',
    "file": ROOT / ".well-known" / "mcp.json",
    "find": '"https://yutapr0117-design.github.io/portfolio/llms-full.txt"',
    "replace": '"https://yutapr0117-design.github.io/portfolio/llms-full-missing.txt"',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 56: main.js が factory を呼ばずに関数そのものを束ねる —— 葉 module の依存注入が抜け、実行時に ReferenceError になる',
    "file": ROOT / "main.js",
    # createBrand(storage) は 56 の factory の定義 (先頭引数が分割代入 `{`) に当たらないので、
    # 分割代入で依存を受ける本物の factory を狙う (初版で名指し False を実測)。
    "find": 'const AIKnowhowPage = createAIKnowhowPage({ h, createIcon, ContactCTA });',
    "replace": 'const AIKnowhowPage = null;',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 460: errata 冒頭の「閉じた番号一覧」から E1 を落とす —— 表は E1 を閉じたと述べるのに一覧から消える (face v・目印は一覧の先頭: 末尾は E を足すたびに動き anchor が宙に浮く)',
    "file": ROOT / "LICENSES" / "ACD-1.0.errata.md",
    "find": "of them (E1, E2, E3,",
    "replace": "of them (E2, E3,",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 124: main.js の factory 合成の範囲に実名を描画する —— 旧 2 段のコメント除去はこの 74 行を消しており、匿名性ガードから見えなかった',
    "file": ROOT / "main.js",
    "find": "const Store = createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp });",
    "replace": "const Store = createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp }); const __leak = h('span', {}, '\u6a2a\u4e95\u96c4\u592a');",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 481: JS コメントの字句 helper が正規表現リテラルを読まなくなる —— /[`]/ のバッククォートをテンプレートの始まりと読み、fixture が崩れる',
    "file": ROOT / ".github" / "scripts" / "_lib_io.py",
    "find": 'prev = "/re/"',
    "replace": 'prev = "/re/"; i = i + 1; continue',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 482: index.html の canonical link を説明コメントの中へ移す —— canonical を守る 40 本以上の Check はコメントの文字列で満たされ、気付くのは本 Check だけ',
    "file": ROOT / "index.html",
    "find": '<link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/" />',
    "replace": '<!-- 旧: <link rel="canonical" href="https://yutapr0117-design.github.io/portfolio/" /> -->',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 133: aio-guard.js の script タグを説明コメントの中へ移す —— コメントを除かずに探す形だとコメントの文字列で満たされ緑のままだった',
    "file": ROOT / "index.html",
    "find": '<script src="./aio-guard.js"></script>',
    "replace": '<!-- 旧配線: <script src="./aio-guard.js"></script> -->',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 483: ai-disclosure の帰属を逆にする (設計 = AI / 実装 = 人間) —— 設計を AI に帰すのは reject-on-sight の anti-pattern',
    "file": ROOT / "index.html",
    "find": 'content="Architected and orchestrated by Yuta Yokoi (横井雄太). Implementation generated by AI team',
    "replace": 'content="Architected and orchestrated by an AI team. Code written by Yuta Yokoi (横井雄太), generated by AI team',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 296: AIO manifest への alternate link を消す —— manifest は digest チェーンの根で、HTML から辿る唯一の入口',
    "file": ROOT / "index.html",
    "find": '<link rel="alternate" type="application/json" title="AIO Asset Manifest" href="/portfolio/.well-known/aio-manifest.json" />',
    "replace": '',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 132: sitemap の llms.txt エントリを消す —— 旧形は "/llms.txt<" が .well-known/llms.txt の末尾でも満たされ、消しても緑だった',
    "file": ROOT / "sitemap.xml",
    "find": "<loc>https://yutapr0117-design.github.io/portfolio/llms.txt</loc>",
    "replace": "<loc>https://yutapr0117-design.github.io/portfolio/llms-moved.txt</loc>",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 482: sitemap の llms-full.txt エントリを説明コメントへ移す —— sitemap を読む Check の多くはコメントを除かずに探す',
    "file": ROOT / "sitemap.xml",
    "find": "<loc>https://yutapr0117-design.github.io/portfolio/llms-full.txt</loc>",
    "replace": "<!-- 旧: <loc>https://yutapr0117-design.github.io/portfolio/llms-full.txt</loc> --><loc>https://yutapr0117-design.github.io/portfolio/</loc>",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 342: Bingbot / Googlebot のグループに行末コメント付きの全サイト拒否を足す —— 名前付き bot は * のグループを読まない。旧形は 1 行正規表現で、コメントが付くと行ごと一致しなかった',
    "file": ROOT / "robots.txt",
    "find": "User-agent: Bingbot\n",
    "replace": "User-agent: Bingbot\nDisallow: /  # maintenance\n",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 161: User-agent: * の直後に別 agent 行を足し、そのグループを全サイト拒否にする —— RFC 9309 では 2 行で 1 グループ。旧形は次の User-agent 行で * の section を閉じていた',
    "file": ROOT / "robots.txt",
    "find": "User-agent: *\nAllow: /llms-full.txt",
    "replace": "User-agent: *\nUser-agent: SomeBot\nDisallow: /\nAllow: /llms-full.txt",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 189: googlebot 宛ての meta を noindex にする —— googlebot には robots より優先する。旧形は先頭の robots meta 1 本しか読まなかった',
    "file": ROOT / "index.html",
    "find": '<meta name="googlebot" content="index, follow,',
    "replace": '<meta name="googlebot" content="noindex, follow,',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 444: sitemap からライセンス全文の <loc> を消す —— 旧形は sitemap 全文の部分文字列で見ており、同じ URL を持つ <image:license> で満たされて緑だった',
    "file": ROOT / "sitemap.xml",
    "find": "    <loc>https://yutapr0117-design.github.io/portfolio/LICENSES/ACD-1.3.txt</loc>\n",
    "replace": "",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 444: robots.txt の記述子の Allow を説明コメントにする —— 旧形は robots 全文の部分文字列で見ており、コメント中の path 言及で満たされた',
    "file": ROOT / "robots.txt",
    "find": "Allow: /portfolio/LICENSES/ACD-1.3.machine.json\n",
    "replace": "# 旧: Allow: /portfolio/LICENSES/ACD-1.3.machine.json\n",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 460 (e): against.md の総括の errata 数を、行の折り返しの直前で 1 桁増やす —— 数と語の間に改行があると旧形の空白 1 個の正規表現は一致せず、38 のまま 9 日間素通りした',
    "file": ROOT / "LICENSES" / "ACD-1.0.against.md",
    "find": "\n   errata, and five corrections",
    "replace": "0\n   errata, and five corrections",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 468o: 草案 §8.4 の動詞 "license" を名詞形 "licence" に戻す —— 1.1〜1.3 はこの形のまま凍結された。同じ語数の綴り違いは差分のレンズも語数照合も拾わない',
    "file": ROOT / "LICENSES" / "ACD-1.4-DRAFT.txt",
    "find": "the use of the Work; it does not license\n",
    "replace": "the use of the Work; it does not licence\n",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 482: 資産の JSON-LD ブロックをコメントで無効化する —— 静的 JSON-LD を読む約 30 箇所はコメントを除かず、2 ブロックとも囲んでも 1 本も発火しなかった',
    "file": ROOT / "index.html",
    "find": '<!-- Asset-level structured data (AI-only, dedicated ImageObject / AudioObject) -->\n    <script type="application/ld+json">',
    "replace": '<!-- Asset-level structured data (AI-only, dedicated ImageObject / AudioObject) -->\n    <!-- 一時停止: <script type="application/ld+json">',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 468m: §16.4 の草案の例外を広げる (a draft → a draft or a corrected text) —— 目印は 2 つとも残るので、存在だけを見る形では 1 識別子 = 1 固定本文が崩れても通った',
    "file": ROOT / "LICENSES" / "ACD-1.4-DRAFT.txt",
    "find": "that no earlier text has borne, except a draft identified as such, so",
    "replace": "that no earlier text has borne, except a draft or a corrected text, so",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 484: style.css の stylesheet link に media="print" を足す —— タグは残るので配線の Check 135 は緑のまま、画面ではサイト全体が未スタイルになる',
    "file": ROOT / "index.html",
    "find": '<link rel="stylesheet" href="./style.css">',
    "replace": '<link rel="stylesheet" href="./style.css" media="print">',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 484: aio-guard.js の script に type="text/plain" を足す —— ブラウザは実行しないが src の文字列は残り、Check 133 は緑のままだった',
    "file": ROOT / "index.html",
    "find": '<script src="./aio-guard.js"></script>',
    "replace": '<script type="text/plain" src="./aio-guard.js"></script>',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 242: manifest link に大文字の ONLOAD handler を足す —— HTML の属性名は大文字小文字を区別しないが、旧形は小文字 + 二重引用符しか探さなかった',
    "file": ROOT / "index.html",
    "find": '<link rel="manifest" href="/portfolio/manifest.webmanifest" />',
    "replace": '<link ONLOAD="fetch(\'//x\')" rel="manifest" href="/portfolio/manifest.webmanifest" />',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 323: license link に一重引用符の style 属性を足す —— 旧形は style="…" (二重引用符) しか探さなかった',
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.3.txt" />',
    "replace": "<link rel=\"license\" style='display:none' href=\"/portfolio/LICENSES/ACD-1.3.txt\" />",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 331: skip-link の href を一重引用符の javascript: にする —— 旧形は二重引用符の値しか見ておらず素通りした',
    "file": ROOT / "index.html",
    "find": '<a href="#main-content" class="skip-link">',
    "replace": "<a href='javascript:void(0)' class=\"skip-link\">",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 207: manifest link を大文字の HREF / HTTP:// にする —— 旧形は小文字の属性名と scheme しか見ず Mixed Content を素通りした',
    "file": ROOT / "index.html",
    "find": '<link rel="manifest" href="/portfolio/manifest.webmanifest" />',
    "replace": '<link rel="manifest" HREF="HTTP://yutapr0117-design.github.io/portfolio/manifest.webmanifest" />',
    "check": CHECK,
})

MUTATIONS = MUTATIONS_ARCHIVE4 + MUTATIONS_ARCHIVE3 + MUTATIONS_ARCHIVE + MUTATIONS_ARCHIVE2 + _MUTATIONS_TAIL

_E2E_TAIL = [
]


# 公開 API: e2e archive(古) + tail(新) の連結 (consistency 側 MUTATIONS と同じ log-rotation 方式)。






















































_E2E_TAIL.append({
    "name": "Lab トグルの開閉状態が永続化されなくなる —— 開いておいた利用者はルート遷移やリロードのたびに畳まれた状態へ戻る。1 回の操作では気付けず「たまに閉じている」としか見えない",
    "file": ROOT / "js" / "components.js",
    "find": "            try { localStorage.setItem(labKey, String(next)); } catch { /* ignore */ }",
    "replace": "            /* persistence removed */",
    "test": "toggle flips aria-expanded",
})

_E2E_TAIL.append({
    "name": "ダーク実効の --text-muted が暗背景に暗い色になる —— drawer / palette / toast など**開いた状態でしか見えない面**のコントラストが落ちる。既定の閉じた状態では何も起きないので通常の a11y 走査では踏まれない",
    "file": ROOT / "style.css",
    "find": """                --text-muted: #9aa4b5;""",
    "replace": """                --text-muted: #2b3444;""",
    "test": "ダークの drawer / palette / toast",
})

_E2E_TAIL.append({
    "name": "nav リンクから href が外れる —— マウスの click ハンドラは残るので**見た目も挙動も変わらず**、キーボード利用者だけがナビゲーションへ到達できなくなる (WCAG 2.1.1)。Googlebot のリンク発見も同時に失われる",
    "file": ROOT / "js" / "components.js",
    "find": "                href: '#/' + item.path,",
    "replace": "                'data-href': '#/' + item.path,",
    "test": "Sidebar nav link is keyboard-operable",
})

_E2E_TAIL.append({
    "name": "上限で断られたときに打った文字が消える —— 追加できたときだけクリアする復元を外すと、"
            "「不要なタスクを削除してください」と言われた時点で入力欄が既に空になっており、"
            "削除して戻っても打ち直しになる (クリア自体は #1061 の二重登録ガードとして必要)",
    "file": ROOT / "js" / "apps.js",
    "find": "if (!addTask(_v)) { e.target.value = _v; }",
    "replace": "addTask(_v);",
    "test": "keeps the typed text when the add is refused by the cap",
})

_E2E_TAIL.append({
    "name": "一時的な通信断から quiz が回復しなくなる —— 失敗した動的 import は module map に "
            "キャッシュされ、以降の import はネットワークへ行かず即 reject する。別 URL での "
            "再取得を外すと、開き直しても永久に失敗表示のまま (完全リロードしか直らない)",
    "file": ROOT / "main.js",
    "find": ").catch(() => _retryQuizData(type))",
    "replace": ")",
    "test": "recovers from a transient load failure by refetching under a new URL",
})

_E2E_TAIL.append({
    "name": "JSON-LD の CreativeWork ノードから license が落ちる —— schema.org で license は "
            "CreativeWork に定義される。1 ノードでも欠けると、その経路から来た agent は "
            "「学習してよいか」を判定できない (ACD-1.0 §6.5)。**視覚には一切出ない**",
    "file": ROOT / "js" / "meta-management.js",
    "find": "'license': SITE_CONFIG.LICENSE_URL,\n                'dateModified'",
    "replace": "'dateModified'",
    "test": "レンダリング後の全 CreativeWork ノードが同一のライセンスを宣言する",
})

_E2E_TAIL.append({
    "name": "HTML 標準の license リンクが消える —— rel=license は権利宣言の最も標準的な入口で、"
            "JSON-LD を読まないツール (ライセンススキャナ等) にとっては唯一の手掛かり",
    "file": ROOT / "index.html",
    "find": '<link rel="license" href="/portfolio/LICENSES/ACD-1.3.txt" />',
    "replace": '<!-- removed by mutation probe -->',
    "test": "HTML 標準の license リンクが全ルートで解決可能な形で存在する",
})

_E2E_TAIL.append({
    "name": "runtime の speakable ノードが canonical と同じ @id にルート固有の name を載せる —— "
            "JSON-LD では同一 @id = 同一エンティティなので property が merge され、"
            "**1 つのエンティティが 2 つの名前を主張**する。「このクエリはこのエンティティにのみ "
            "解決すべき」という中核宣言と真っ向から矛盾する (2026-08-23 の実バグ)",
    "file": ROOT / "js" / "meta-management.js",
    "find": "            'license': SITE_CONFIG.LICENSE_URL,\n            'speakable': {",
    "replace": "            'license': SITE_CONFIG.LICENSE_URL,\n            'name': fullTitle,\n            'speakable': {",
    "test": "同一 @id が矛盾する property 値を宣言しない",
})

_E2E_TAIL.append({
    "name": "取り込みモード「全置換」が appsData に効かなくなる —— #1183 の実バグそのもの。"
            "モードは projects にしか効いておらず、appsData はどのモードでも丸ごと置き換えていた "
            "(既定の「追加のみ」で AppsData を含むファイルを取り込むと**既存のタスク・やること・"
            "ノート・履歴が全部消えた**)。**最も安全なつもりの選択が最も破壊的**で、しかもそれが既定値",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (settingsImportMode === 'strict') {\n                        merged.appsData = inc;",
    "replace": "                    if (false) {\n                        merged.appsData = inc;",
    "test": "「全置換」の import は宣言どおり丸ごと置き換える",
})

_E2E_TAIL.append({
    "name": "取り込みモード「更新+追加」が既存 id を更新しなくなる —— append との差が消え、"
            "3 モードのうち 2 つが同じ挙動になる。**利用者は宣言どおりに動いたと信じて元データを"
            "捨てうる**ので、モード間の意味論の差は e2e で固定しておく必要がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "if (!map.has(x.id) || settingsImportMode === 'upsert') { map.set(x.id, x); }",
    "replace": "if (!map.has(x.id)) { map.set(x.id, x); }",
    "test": "「更新+追加」の import は既存を残しつつ取り込む",
})

_E2E_TAIL.append({
    "name": "slug 一意化を無効化する —— #154 の実バグ。同名プロジェクトを追加すると slug が衝突し、"
            "ProjectDetailPage の find(p.slug===slug) が先頭のみ返すため**片方の詳細ページへ"
            "到達不能**になる。一覧には両方出るので気付く手掛かりが薄い",
    "file": ROOT / "js" / "store.js",
    "find": "            if (_seenSlugs.has(s)) {\n                let n = 2;",
    "replace": "            if (false) {\n                let n = 2;",
    "test": "Adding two projects with the same name yields unique slugs",
})

_E2E_TAIL.append({
    "name": "sidebar の nav リンクが指すルートを 1 つ router から落とす —— 利用者にはナビを押すと "
            "NotFound が出るだけに見える。この gate は 2026-08-24 まで **前ルートの DOM に対して "
            "不在アサーションを評価**しており、自分が名乗っている「壊れた nav リンク」を一度も "
            "検出できなかった (遷移直後の NotFound 見出し 0 件で PASS・settle 後は 1 件)",
    "file": ROOT / "js" / "router.js",
    "find": "            case 'role-split':\n                route.name = 'role-split';",
    "replace": "            case 'role-split-DISABLED':\n                route.name = 'role-split';",
    "test": "All sidebar nav links resolve to valid",
})

_E2E_TAIL.append({
    "name": "quiz の章見出しを h2 -> h4 にして heading-order を壊す —— 長い読み物の見出し階層が"
            "飛ぶと、スクリーンリーダーの主要移動手段である見出しジャンプで本文を辿れなくなる。"
            "この違反は 2026-08-24 まで **ダーク走査から構造的に見えなかった**: ループの待ちが汎用で"
            "前ルートの DOM で成立していたため、axe はちょうど 1 つ前のルートを走査しており "
            "`#/quiz` (最大のコンテンツページ) は一度も走査されていなかった (実測: 同じ違反を"
            "注入して旧待ちでは PASS・新待ちでは `#/quiz: heading-order(1)` で FAIL)",
    "file": ROOT / "js" / "quiz-renderer.js",
    "find": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h2\", { class: \"quiz-section-title\" }, section));",
    "replace": "                    sHeader.appendChild(h(\"div\", { class: \"quiz-section-icon\", 'aria-hidden': 'true' }, \"\U0001F4DD\"));\n                    sHeader.appendChild(h(\"h4\", { class: \"quiz-section-title\" }, section));",
    "test": "ダークテーマの全ルート",
})

_E2E_TAIL.append({
    "name": "quiz の章カードに min-width を与えて 320px であふれさせる (WCAG 1.4.10)。この違反は "
            "2026-08-24 まで **reflow の走査から構造的に見えなかった**: ループの待ちが汎用で前ルートの "
            "DOM で成立していたため、6 ルート全てが `#/role-split` を測っており、#962 で直した実バグの "
            "対象 (quiz / hiring-risk / pomodoro) は一度も測られていなかった",
    "file": ROOT / "style.css",
    "find": ".quiz-section-card {",
    "replace": ".quiz-section-card { min-width: 420px;",
    "test": "320px 幅でどのルートも横スクロールしない",
})

_E2E_TAIL.append({
    "name": "AI 応答到着時のルート判定を潰す —— 応答は submit の 300ms 後に非同期で届くので、"
            "その間に別アプリへ移っているのは普通にある。ルートを見ずに State.update すると "
            "notify → #content の全再描画が起き、**操作していない画面の未送信入力が消える** "
            "(実測: AI-INTERRUPT-DRAFT → \"\")。#994 の focus 復元が id で働くぶん "
            "**activeElement は残って値だけ消える**ので、利用者は原因に見当がつかない。"
            "#982 / #1055 / #1056 と同じ class",
    "file": ROOT / "js" / "ai-page.js",
    "find": "if (onAiRoute) { State.update(applyResponse); }",
    "replace": "if (true) { State.update(applyResponse); }",
    "test": "別アプリで入力中のテキストを消さない",
})

_E2E_TAIL.append({
    "name": "「全リセット」を appsData だけ戻す部分リセットへ退行させる —— projects / profile / "
            "theme / projectPrefs が残る。**「全」と名乗る操作が一部しか戻さない**のは、利用者が"
            "「初期化した」と信じて元データを捨てうる silent failure。実測 (2026-08-26): "
            "pomodoro/quiz/notes を見る multi-app リセット test も、AI 応答待ち中のリセット test も"
            "**appsData しか見ないので素通り**する。捕捉層は apps-settings-io の 2 件だけだった",
    "file": ROOT / "js" / "settings-page.js",
    "find": "State.set(Store.createDefaultStore());",
    "replace": "State.set({ ...State.get(), appsData: Store.createDefaultStore().appsData });",
    "test": "表示テーマが export → import で復元され",
})

_E2E_TAIL.append({
    "name": "theme を「値が変わらなくても applied に数える」形へ戻す —— フルバックアップには "
            "**必ず theme が入る**ので、この 1 行だけで #1040 の「0 セクションなら成功と言わない」"
            "ガードが最も一般的なファイル形式に対して丸ごと無効化される。実測 (2026-08-26): "
            "対象 3 つを全て外して読み込むと state は前後で完全に同一なのに「完了しました」と出る。"
            "既存の #1040 test は theme を含まない `AppsDataのみ` を使うためこの枝を踏めない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    if (parsed.theme !== base.theme) { applied = true; }",
    "replace": "                    applied = true;",
    "test": "フルバックアップでも、対象を全部外したら成功と report しない",
})


_E2E_TAIL.append({
    "name": "`Projectsのみ` の書き出しを projects の素の配列へ戻す —— 既定プロジェクトは削除できず "
            "**「非表示」が唯一の非公開手段** (#886) なのに、このファイルから復元すると "
            "隠したプロジェクトが黙って再公開される。フルバックアップは #1037 で projectPrefs を "
            "含むよう直したのに、部分 export だけ取り残されていた形 (実測 2026-08-26)",
    "file": ROOT / "js" / "settings-io.js",
    "find": "downloadJSON({ projects: s.projects, projectPrefs: s.projectPrefs },",
    "replace": "downloadJSON(s.projects,",
    "test": "Projectsのみ の往復で非表示設定が戻る",
})


_E2E_TAIL.append({
    "name": "貼り付けが maxlength で切られたことを黙らせる (通知条件を殺す) —— **打鍵は「入らなく"
            "なる」のが見えるが貼り付けは無反応**。実測 (2026-08-26): タスク入力へ 500 文字を貼ると "
            "200 文字だけ残り 300 文字が通知ゼロで消えた。既定動作は妨げず報告だけを足す設計なので、"
            "この条件を殺すと**元の silent な消失に戻る**",
    "file": ROOT / "js" / "ui-components.js",
    "find": "        if (dropped > 0) {",
    "replace": "        if (false) {",
    "test": "上限を超える貼り付けは、消えた文字数を通知する",
})


_E2E_TAIL.append({
    "name": "スナップショットの上書き確認を無効化する —— スロットは**単一**なので 2 度目の「保存」は "
            "前の内容を消して現在の状態で置き換える = **削除と同じく不可逆**。clearSnapshot は "
            "#1185 で confirm を得たのに**上書きだけ取り残されていた** (実測 2026-08-26: 2 回目の "
            "クリックで dialog ゼロのまま保存日時が置き換わった)。壊れた状態を実験したあと反射的に "
            "「保存」を押すと、**戻るはずだった良い状態を自分で消す**",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (_prev) {",
    "replace": "            if (false) {",
    "test": "スナップショットの上書きは確認を求め、キャンセルすると元が残る",
})


_E2E_TAIL.append({
    "name": "全置換 (strict) モードの取り込み確認を無効化する —— **最も破壊的な経路**なのに、"
            "プロジェクト 1 件の削除も全リセットもスナップショットの削除・上書きも confirm を通すのに"
            "ここだけ素通りしていた (実測 2026-08-26: dialog ゼロで既存タスクが消えた)。"
            "**モードは遷移を跨いで残る**ので、一度 strict にした利用者が後で別のファイルを"
            "取り込むときに選択を覚えていない、という現実的な経路がある",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (settingsImportMode === 'strict') {\n                    if (!confirm(",
    "replace": "                if (false) {\n                    if (!confirm(",
    "test": "全置換モードの取り込みは確認を求め、キャンセルすると既存データが残る",
})


_E2E_TAIL.append({
    "name": "プロジェクト削除の確認文から**対象の名前**を落とす —— 成功 Toast は名前を出すのに "
            "確認が「本当に削除しますか？」だけだと、**一覧で行を押し間違えても気付けない** "
            "(名前が出るのは消えた後)。#1185 が「文言は何を失うかを明示する」と原則を書いたのに、"
            "その比較対象だった当の削除が取り残されていた",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (!confirm(_target && _target.name",
    "replace": "            if (!confirm(false && _target && _target.name",
    "test": "Deleting a user project (confirm accepted) removes it everywhere",
})


_E2E_TAIL.append({
    "name": "全リセットの確認文から「元に戻せません／スナップショットは残ります」を落とす —— "
            "**何を失い何が残るかを言わない確認は判断材料にならない**。残るものを伝えるほうが"
            "利用者は判断できる (消える恐れで踏みとどまる必要が無くなる)。#1185 が書いた"
            "「文言は何を失うかを明示する」原則の、全リセット面",
    "file": ROOT / "js" / "settings-page.js",
    "find": "                + '元に戻せません。スナップショットは残ります。')) {return;}",
    "replace": "                + '')) {return;}",
    "test": "全リセットの確認文は、元に戻せないことと残るものを伝える",
})


_E2E_TAIL.append({
    "name": "取り込み失敗の文言から**受け付ける形式の案内**を落とす —— 利用者はこのアプリ自身が"
            "書き出したファイルを読み込もうとして失敗しており、「失敗した」だけでは**次の一手が"
            "無い行き止まり**になる。受け付ける 4 形式はアプリ自身が知っているのだから伝える",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                    Toast.show('認識できない形式のファイルです。'",
    "replace": "                    Toast.show('認識できない形式のファイルです', 'error'); if (0) Toast.show('x'",
    "test": "認識できない形式の JSON は成功と report しない",
})

_E2E_TAIL.append({
    "name": "スキーマ移行の通知を落とす —— 版数が変わったデプロイで**全データが既定へ戻る**のに、"
            "消えたことも復元できることも伝えない状態に戻す。退避先は作られているので救えるのに、"
            "利用者からは「開いたら全部消えていた」としか見えず復元導線へ辿り着けない",
    "file": ROOT / "js" / "state.js",
    "find": "const _migration = Store.takeMigrationNotice ? Store.takeMigrationNotice() : null;",
    "replace": "const _migration = null;",
    "test": "Schema migration tells the user what was reset",
})

_E2E_TAIL.append({
    "name": "スナップショットの由来判定を潰す —— 移行時の自動退避を「手動で保存」と表示させる。"
            "自動退避は load 時に走るため確認を挟めず手動保存を黙って上書きするので、由来を"
            "誤って表示すると利用者は自分の復元点が残っていると誤解したまま別物を復元する",
    "file": ROOT / "js" / "settings-page.js",
    "find": "            if (snap.reason === 'schema-mismatch') {",
    "replace": "            if (false) {",
    "test": "自動退避されたスナップショットは移行元と移行先を示す",
})

_E2E_TAIL.append({
    "name": "brand の取り込みを落とす —— 「フルバックアップ」に配色が入っていても復元されない"
            "状態に戻す。brand は store の外なので merged に載せても normalize が落とす。theme が"
            "戻るのに brand だけ戻らない非対称は利用者から見て「フル」の約束破り",
    "file": ROOT / "js" / "settings-io.js",
    "find": "                if (typeof parsed.brand === 'string' && Brand && Brand.set) {",
    "replace": "                if (false) {",
    "test": "配色 (brand) が export → import で復元される",
})

_E2E_TAIL.append({
    "name": "書き出しの成功通知を落とす —— ファイルは落ちるのに何も報告しない状態に戻す。"
            "他の操作は全て報告するのに書き出しだけ黙る非対称で、SR 利用者は成否を知る手段が"
            "無い (WCAG 4.1.3)。バックアップは「取れたつもり」が最も危ない",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show(`${filename} を書き出しました`);",
    "replace": "            void filename;",
    "test": "書き出しは成功を報告する",
})
_E2E_TAIL.append({
    "name": "書き出しの失敗を握り潰さず再送出する —— 修正前の挙動に戻す。例外がそのまま致命"
            "エラーへ昇格し FatalPage と全画面オーバーレイで Settings が消える＝**バックアップを"
            "取ろうとして画面を失う**。失敗の伝え方として最悪の形",
    "file": ROOT / "js" / "settings-io.js",
    "find": "            Toast.show('書き出しに失敗しました。ブラウザのダウンロード設定を確認してください。', 'error', 5000);",
    "replace": "            throw e;",
    "test": "書き出しが失敗しても致命エラーにせず理由を伝える",
})

_E2E_TAIL.append({
    "name": "リセットの通知を落とす —— 押してもボタン名は変わらず、タイマーは意図的に非 live"
            "なので、結果だけ変わって無音になる。見えない利用者にはリセットできたのかどうかが"
            "分からない (開始/一時停止はラベル、モード切替は aria-pressed が変化を伝える)",
    "file": ROOT / "js" / "pomodoro-page.js",
    "find": "            announce(`${label}のタイマーをリセットしました。残り ${formatTime(duration)}`);",
    "replace": "            void label;",
    "test": "リセットは結果を支援技術へ伝える",
})



_E2E_TAIL.append({
    "name": "nav リンク自身の closeDrawer を落とす —— 別ルートへの遷移は hashchange の配線 (#998) が"
            "閉じるので気付けないが、**今いるページのリンクを押したとき**は hash が変わらず hashchange が"
            "発火しないため drawer が開いたまま残る。モバイルでは画面を覆うので、メニューを閉じるつもりの"
            "普通の操作で閉じなくなる",
    "file": ROOT / "js" / "components.js",
    "find": "                    if (isDrawer) { closeDrawer(); }",
    "replace": "                    if (false) { closeDrawer(); }",
    "test": "今いるページの nav リンクを押しても drawer は閉じる",
})
_E2E_TAIL.append({
    "name": "詳細ページの「一覧に戻る」が絞り込みを捨てる —— router が戻り先を query 込みで保持する"
            "単一ソース (#951) を潰す。1 件に絞り込んだ状態から戻ると全件に戻り、利用者は同じ意味の"
            "操作 (ブラウザの戻る) との食い違いに気付けない",
    "file": ROOT / "js" / "router.js",
    "find": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = raw; }",
    "replace": "        if (raw === 'projects' || raw.startsWith('projects?')) { _lastListPath = 'projects'; }",
    "test": "In-page \"back to list\" preserves the active filter",
})

_E2E_TAIL.append({
    "name": "カテゴリ絞り込みの URL 同期を落とす —— 画面上は絞り込まれるのに URL に残らないので、"
            "共有したリンクや再読み込みで全件へ戻る。絞り込みは「今見ている範囲」そのものなので、"
            "URL に出ないと共有も復元もできない",
    "file": ROOT / "js" / "projects-page.js",
    "find": "                if (cat !== 'All') {params.set('cat', cat);}",
    "replace": "                if (false) {params.set('cat', cat);}",
    "test": "Projects category filter narrows the list and syncs to the URL",
})
_E2E_TAIL.append({
    "name": "nav リンクの aria-current を落とす —— 支援技術に「今どのページにいるか」が伝わらなくなる"
            "(WCAG 2.4.8)。視覚的な強調は class で別に付くので**目では気付けない**。sidebar と drawer は"
            "同じ実装を共有するが、mobile では drawer が唯一のナビなので両方が守られる必要がある",
    "file": ROOT / "js" / "components.js",
    "find": "                'aria-current': item.active ? 'page' : undefined",
    "replace": "                'aria-current': undefined",
    "test": "モバイルの drawer が現在ルートに aria-current を付け、遷移に追従する",
})

E2E_MUTATIONS = E2E_MUTATIONS_ARCHIVE3 + E2E_MUTATIONS_ARCHIVE2 + E2E_MUTATIONS_ARCHIVE + _E2E_TAIL
