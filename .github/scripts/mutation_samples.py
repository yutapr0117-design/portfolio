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
    "name": 'Check 121: STATUS.md の最新 Session Record を手で書き換える —— 機械生成の owner dashboard が実態とずれる',
    "file": ROOT / "STATUS.md",
    "find": '- **最新 Session Record**: #',
    "replace": '- **最新 Session Record**: #X',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 6: style.css に古い release marker を戻す —— 版の記述が CSS の中で古いまま残る',
    "file": ROOT / "style.css",
    "find": '/* ╔══',
    "replace": '/* NEXT_PLANNED_RELEASE */\n        /* ╔══',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 7: CSP meta を別名にする —— inline suppressor より前に CSP が来る順序の保証が崩れる',
    "file": ROOT / "index.html",
    "find": '<meta http-equiv="Content-Security-Policy"',
    "replace": '<meta http-equiv="X-Content-Security-Policy"',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 10: 手で回す道具 (verify_dossier_quotations.py) に構文エラーを入れる —— verify が呼ばない script の破損は Check 10 だけが見る',
    "file": ROOT / ".github" / "scripts" / "verify_dossier_quotations.py",
    "find": 'def norm(text):',
    "replace": 'def norm(text:',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 12: README の現在の記述に古い「72回以上」を戻す',
    "file": ROOT / "README.md",
    "find": '# Yuta Yokoi — AI-Driven PM Portfolio',
    "replace": '# Yuta Yokoi — AI-Driven PM Portfolio 72回以上',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 28: CSP 違反を見る e2e の題名を変える —— セキュリティ gate が在ることの保証が消える',
    "file": ROOT / "e2e" / "security-proxy.spec.js",
    "find": "test('No Trusted Types or CSP violations in console',",
    "replace": "test('No Trusted Types or CSP violations in the console log',",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 53: index.html の modulepreload の href を存在しない file へ —— 先読みが 404 になり、宣言だけが残る',
    "file": ROOT / "index.html",
    "find": '<link rel="modulepreload" href="./js/pure-utils.js" />',
    "replace": '<link rel="modulepreload" href="./js/pure-utils-missing.js" />',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 61: factory module の docstring から factory pattern の印を落とす —— file 単体を読んでも抽出の経緯が分からなくなる',
    "file": ROOT / "js" / "ai-page.js",
    "find": 'factory pattern',
    "replace": 'factory-less',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 57: modulepreload を 1 行消す —— main.js が import する葉の集合と先読みの集合が食い違い、その葉だけ直列に取得される",
    "file": ROOT / "index.html",
    "find": '    <link rel="modulepreload" href="./js/ui-components.js" />\n',
    "replace": "",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468m: §16.4 の Steward 例外から「新しい版番号でのみ」の限定を外す —— Steward が同じ識別子で"
            "別本文を出せる形に戻る (2026-11-01 外部レビュー #279)。語数を変えない置換にして 468 の語数 face と分ける",
    "file": CURRENT_DRAFT,
    # 同じ語句が草案冒頭の変更一覧にも引用されている (初版の find は 2 箇所に当たり、先頭 = 変更一覧を
    # 打って §16.4 は無傷だった)。§16.4 の行だけにある直後の "," まで含めて一意にする。
    "find": "no earlier text has borne,",
    "replace": "an earlier text has borne,",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 13: README の現在の記述に「70超」を戻す —— 履歴の文脈でない場所に古い数が残る',
    "file": ROOT / "README.md",
    "find": '# Yuta Yokoi — AI-Driven PM Portfolio',
    "replace": '# Yuta Yokoi — AI-Driven PM Portfolio 70超',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 58: e2e の ALL_ROUTES から 1 ルートの名前をずらす —— main.js の switch と全ルート訪問 e2e の集合が食い違う',
    "file": ROOT / "e2e" / "security-proxy.spec.js",
    "find": "{ hash: '#/projects',          name: 'projects' }",
    "replace": "{ hash: '#/projects',          name: 'projectz' }",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 66: index.html の <title> から entity 名を落とす —— 検索結果と AI の要約で誰のサイトか分からなくなる',
    "file": ROOT / "index.html",
    "find": '<title>AI-Driven PM yuta｜',
    "replace": '<title>AI-Driven PM｜',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 67: workflow の top-level permissions を外す —— 既定の広い token 権限で走る',
    "file": ROOT / ".github" / "workflows" / "update-playwright-snapshots.yml",
    "find": '\npermissions:\n',
    "replace": '\npermissionz:\n',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 107: runbook §11 の workflow 一覧から 1 本の名前を外す —— CI の在庫表が実体と食い違う',
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    # update-playwright-snapshots.yml は §11 の別の行の説明文にも出るので、消しても集合から落ちない
    # (初版で名指し False を実測)。§11 に 1 回しか出ない mutation-probe.yml を外す。
    "find": '| `mutation-probe.yml` |',
    "replace": '| mutation-probe |',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 59: §4 BUDGET-DATA の 1 行の path をずらす —— 人間可読の §2 表と機械可読の §4 の集合が食い違う (71 も同時に発火)',
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": '.github/scripts/mutation_samples_archive4.py | 950 | advisory',
    "replace": '.github/scripts/mutation_samples_archive4x.py | 950 | advisory',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 468k (表の形): README の「次版の草案（作業場）」行を前の版の草案へ戻す —— 2026-11-01 まで表の行は射程外で、faq.md の同じ行が 7 日間古いままだった (portfolio-bb の発見)',
    "file": ROOT / "LICENSES" / "README.md",
    "find": '| **次版の草案（作業場）** | [`',
    "replace": '| **次版の草案（作業場）** | [`ACD-0.9-DRAFT.txt`](ACD-0.9-DRAFT.txt) [`',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 460 (t): FAQ の B1 を A 番号へ変える —— 項番の頭文字が置かれた節と食い違い、索引の数え方で読み手が別の節を探す (portfolio-bb の発見)',
    "file": ROOT / "LICENSES" / "ACD-1.0.faq.md",
    "find": '\n### B1. ',
    "replace": '\n### A99. ',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 110: 2 つ目の A11Y_ROUTES (a11y-lang-of-parts.spec.js) から 1 ルートを落とす —— 2026-11-01 まで 110 は連結した本文の最初の定義しか見ず、この list は一度も照合されていなかった',
    "file": ROOT / "e2e" / "a11y-lang-of-parts.spec.js",
    "find": "'#/ai-knowhow', '#/role-split', '#/not-found'];",
    "replace": "'#/ai-knowhow', '#/not-found'];",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 109: README に「all 480 checks」と現在の総数を書き込む —— 総数は runbook §9 だけが持ち、他所は書いた日に古くなる',
    "file": ROOT / "README.md",
    "find": '# Yuta Yokoi — AI-Driven PM Portfolio',
    "replace": '# Yuta Yokoi — AI-Driven PM Portfolio (all 480 checks)',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 123: llms-full.txt の運用モデル節の見出しを変える —— サイトと AIO 層の運用モデルの記述が対応しなくなる',
    "file": ROOT / "llms-full.txt",
    "find": 'Current Operating Model',
    "replace": 'Current Operating Mode',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 113: AI2AI.md から「commit 数は OUTPUT であって TARGET」の条項を消す —— 次の AI が padding commit に退行する',
    "file": ROOT / "AI2AI.md",
    "find": 'OUTPUT であって TARGET',
    "replace": 'OUTPUT',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 453 (453b): FREEZE-DATA から確定済みの 1.3 本文の行を消す —— 冒頭で FROZEN TEXT を名乗る本文が"
            "黙って編集可能になる (2026-11-01 の版移行シミュレーションで、新しく確定した版を足し忘れても何も鳴らないと実測)",
    "file": ROOT / "LICENSES" / "FROZEN.md",
    "find": '3b72d36b4962467365ff8742abe09d66eb577c7f7ae8617ea0c5adb02c8dfcfd  LICENSES/ACD-1.3.txt\n',
    "replace": "",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 70: runbook §9 の consistency Check 総数を 1 つ減らす —— 総数の単一権威が実装の最大番号とずれる (値を含まない prefix で当てる)',
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": '| consistency Check 総数 | **',
    "replace": '| consistency Check 総数 | **9',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 73: index.html の preload から as= を落とす —— ブラウザが資源の種類を知らず二重取得になる',
    "file": ROOT / "index.html",
    "find": '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=DM+Sans',
    "replace": '<link rel="preload" href="https://fonts.googleapis.com/css2?family=DM+Sans',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 77: slash command の frontmatter から description を落とす —— command 一覧で何をするか分からなくなる',
    "file": ROOT / ".claude" / "commands" / "audit.md",
    "find": '\ndescription: ',
    "replace": '\ndescriptionx: ',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 78: sub-agent の frontmatter から description を落とす —— いつ呼ぶべき agent かが読めなくなる',
    "file": ROOT / ".claude" / "agents" / "repo-auditor.md",
    "find": '\ndescription: ',
    "replace": '\ndescriptionx: ',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 79: .mcp.json の mcpServers を別の key にする —— MCP の設定が読まれなくなる。**2026-11-01 まで、この形は Check 79 の OK 文の f-string が KeyError を投げて suite ごと止まり、79 は自分の失敗を一度も報告できなかった** (fail-soft へ直した)',
    "file": ROOT / ".mcp.json",
    "find": '"mcpServers"',
    "replace": '"mcpServerz"',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 80: skill の frontmatter から description を落とす —— skill の起動条件が読めなくなる',
    "file": ROOT / ".claude" / "skills" / "repo-status" / "SKILL.md",
    "find": '\ndescription: ',
    "replace": '\ndescriptionx: ',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 460 (u): 172 観点の仕分け表の 1 行の分類を変える —— 冒頭の TRIAGE-TALLY が行の中身とずれる "
            "(分類は検証のたびに動き、相互検証だけで 4 行が変わった)",
    "file": ROOT / "LICENSES" / "ACD-1.4-ADVERSARIAL-TRIAGE.md",
    "find": "| bb | ［外部］ 既知・外部: register B15",
    "replace": "| bb | ［取引］ 既知・外部: register B15",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 40b: CSS lint の local binary 優先を消して npx だけにする —— 2026-11-01 まで 40b は docstring とコメントの文字列で満たされ、このコードを丸ごと消しても緑だった',
    "file": ROOT / ".github" / "scripts" / "check_css_stylelint.py",
    "find": '    local_bin = ROOT / "node_modules" / ".bin" / "stylelint"\n    if local_bin.exists():\n        return [str(local_bin)], True\n    return ["npx", "stylelint"], False',
    "replace": '    return ["npx", "stylelint"], False',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 51: runbook に pin と違う Playwright の版を書き足す —— baseline を生成した版の記述が pin とずれる',
    "file": ROOT / "docs" / "architecture" / "total-check-runbook.md",
    "find": 'Last-Updated  : 2026-06-16',
    "replace": 'Last-Updated  : 2026-06-16 (Playwright 9.9.9)',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": "Check 468n: 草案冒頭の変更一覧の 1 箇条の語数申告をずらす —— 申告の合計が「申告語数 − 前の凍結版の語数」と"
            "合わなくなる。一覧は差分のすべてだと宣言しており、468 は合計語数しか見ていなかった (portfolio-25 の自己記述レンズ)",
    "file": CURRENT_DRAFT,
    "find": "(+21 words.)",
    "replace": "(+20 words.)",
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 54: @eslint/js の major を eslint と食い違わせる —— flat config の推奨ルールが別 major の定義で読まれる',
    "file": ROOT / "package.json",
    "find": '"@eslint/js": "1',
    "replace": '"@eslint/js": "9',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 69: package.json の engines から CI が使う Node の major を外す —— 宣言した対応範囲で CI が走っていない',
    "file": ROOT / "package.json",
    "find": ' || >=24"',
    "replace": '"',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 72: ESLint の warning baseline を上限より大きくする —— 回帰の比較基準そのものが緩む',
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": '<!-- ESLINT-BASELINE-DATA ',
    "replace": '<!-- ESLINT-BASELINE-DATA 9',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 18: sitemap の root <loc> の lastmod を千年前へずらす —— root の更新日が ai:last-modified と食い違う (値を含まない prefix で当てる)',
    "file": ROOT / "sitemap.xml",
    "find": '<loc>https://yutapr0117-design.github.io/portfolio/</loc>\n    <lastmod>2',
    "replace": '<loc>https://yutapr0117-design.github.io/portfolio/</loc>\n    <lastmod>1',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 49: Person の worksFor が指す Organization の @id をずらす —— 所属の参照が宙に浮き、構造化データの上では誰の所属か分からなくなる',
    "file": ROOT / "index.html",
    "find": '"startDate": "2026-06-11",\n                        "worksFor": {\n                              "@id": "https://nkgr.co.jp/#organization"',
    "replace": '"startDate": "2026-06-11",\n                        "worksFor": {\n                              "@id": "https://nkgr.co.jp/#organisation"',
    "check": CHECK,
})

_MUTATIONS_TAIL.append({
    "name": 'Check 71: §4 BUDGET-DATA に存在しない file の行を足す —— 改名・削除の後に予算表だけが古いまま残る (59 も同時に発火)',
    "file": ROOT / "docs" / "architecture" / "file-size-budget.md",
    "find": '.github/scripts/mutation_samples_archive4.py | 950 | advisory',
    "replace": '.github/scripts/mutation_samples_archive4.py | 950 | advisory\n.github/scripts/does-not-exist.py | 100 | advisory',
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
