# decision-v80-phase4-macos-tcc-downloads-self-drive-halt

```
Record-Type   : Operating-model evidence (自走停止と唯一の human help 要請の事実記録)
Event-Date    : 2026-07-30 (UTC 07:54–08:10 / JST 16:54–17:10) — 発端は約 20h 前 (2026-07-29 頃)
Recorded-By   : Claude Code (AI implementer) under Yuta Yokoi (横井雄太) orchestration
Recorded-At   : 2026-08-07
Canonical-Ref : CLAUDE.md §7 Operating Model / AI2AI.md STEP 3 / docs/incident-artifacts/README.md
Status        : FACTUAL RECORD — オーナー依頼により、AI が「Mac の仕様で自走不可になった時"のみ"
                human に助けを求めた」事実を透明に記録する。捏造なし・トランスクリプト実測に基づく。
```

> **なぜこの記録が存在するか（オーナー依頼の要旨）:** この運用モデルは「AI 無限改善自走 / 人間は制御と監査のみ・全委任下で AI は genuine 改善に認可を求めない」を核とする。その中で AI が **たった一度だけ** 人間に助けを求めた出来事があり、それが **通常の改善のためではなく、Mac の OS 仕様（TCC 権限）でリポジトリへ物理的にアクセスできなくなり自走が不可能になった時「のみ」** だった、という事実をオーナーがリポジトリに残すことを望んだ。本ファイルはその一次記録である。

---

## What（何が起きたか）

2026-07-30、AI の無限改善自走ループ実行中に、リポジトリのある `~/Downloads/portfolio` への**全アクセスが EPERM で拒否**され、read / write / git / verify / PR の一切が物理的に不可能になった。AI は範囲を切り分けて診断し、これが**環境側（macOS）の権限剥奪**であって当方コード・リポジトリ状態の問題ではないと確定。**この状態では自走を再開できない**と判定し、空回りの失敗を繰り返す代わりに **ループを停止して待機**し、オーナーへ復旧を要請した。オーナーが Mac を再起動して権限が回復し、リポジトリは known-good（main クリーン・open PR 空・in-flight なし）だったため、その場から自走を再開した。

診断の実測（トランスクリプト由来）:

| パス | アクセス |
|---|---|
| `/Users/yokoiyuuta/`（ホーム） | ✅ OK |
| **`/Users/yokoiyuuta/Downloads/`** | ⛔ DENIED |
| `…/Downloads/portfolio/`（リポジトリ・ファイル読取／git） | ⛔ DENIED |
| `/private/tmp/…/scratchpad` | ✅ OK |

ホームと `/tmp` は通るのに **Downloads 配下だけが全面 DENIED**。約 20 時間 自動回復しなかった。

## Why（原因と、なぜ「助けを求める」が正しい判断だったか）

- **根本原因 = macOS TCC（Transparency, Consent & Control）の "Downloads フォルダ" 保護権限の剥奪。** Downloads は Desktop / Documents と同じ TCC 保護フォルダで、ターミナル / Claude Code に付与されていた「Downloads フォルダ」アクセス許可が失われると、その配下は全面 DENIED になる。リポジトリが Downloads 配下に存在するため、リポジトリ操作の全経路が同時に死んだ。
- **これは AI が自力で解けない class。** TCC の再許可は OS レベルの GUI 承認（システム設定のプライバシー許可 or 再起動時の OS プロンプトへの「許可」）を要し、サンドボックス内の AI には権限がない。約 20h 自動回復しなかった時点で「待てば直る」ではなく「環境側の人間操作が必須」と確定した。
- **だから "human help 要請" は運用モデルの逸脱ではなく、その境界の正しい適用だった。** 全委任下でも AI は genuine 改善に認可を求めない（[[feedback_no_authorization_under_full_delegation]]）が、それは「AI が実行可能な作業」の話。**物理的に実行不可能な環境障害**は AI の権限外であり、ここで human に助けを求めるのは「認可を求める」こととは別カテゴリ。むしろ、失敗し続けるより停止して正確な復旧手順を提示する方が honest で load-bearing だった。

## How（AI が実際に取った手順 — 空回りしないための型）

1. **範囲診断**: home / Downloads / portfolio / scratchpad の各アクセスを個別テストし、DENIED の境界（Downloads 配下のみ）を特定。
2. **原因確定**: 境界が TCC 保護フォルダと一致 → 「環境側の権限剥奪」と結論（コード起因を除外）。
3. **停止判断の明示**: 「この状態では自走を再開できない・無価値な失敗を繰り返すだけ」と明言し、ループを**停止して待機**。
4. **具体的復旧手順の提示**: (a) セッション/ターミナル再起動で OS プロンプト再提示 →「許可」、または (b) システム設定 → プライバシーとセキュリティ →「ファイルとフォルダ」/「フルディスクアクセス」で Downloads 許可を ON。
5. **確認コマンドの提示**: `git -C ~/Downloads/portfolio status` が exit 0 になれば復旧、と検証手段を渡した。
6. **復旧後**: オーナーが Mac 再起動 → git exit 0・ファイル読取 OK を確認 → 状態 known-good を確認 → 自走再開（WebSearch も復活し research レンズを継続）。

## Constraints

- 適用 C 番号: 運用モデル境界（CLAUDE.md §7 / AI2AI.md STEP 3）。AIO published-layer 外の incident artifact ゆえ **C6 非該当**（aio-guardian / orchestrator 書面承認 不要・append-only）。
- 機械強制 Check: Check 42（命名 `decision-*`）/ 75（README inventory）/ 108（本 mirror 存在）/ 97・98（mirror frontmatter + 6 section）/ 65（last-updated ISO）。
- 本記録はコード挙動を変えない（純粋な事実記録）。

## Change impact

本ファイル追加・改名・削除時は同時に: (a) `docs/files/docs/incident-artifacts/decision-v80-phase4-macos-tcc-downloads-self-drive-halt.md.md`（mirror）を同期（Check 108）、(b) `docs/incident-artifacts/README.md` の Decision Records inventory へ列挙（Check 75）。将来この class（環境障害での自走停止）が再発したら、本記録を先例として参照し、同じ「診断 → 停止明示 → 復旧手順提示 → 確認手段付与」の型で対応する。

## Audience-specific notes

### For AI agents（次担当）
- 役割タグ: `operating-model-evidence`, `environment-halt`, `macos-tcc`, `human-help-boundary`, `no-thrash-on-blocked-env`
- **教訓**: 環境が物理的に AI の権限外で壊れた（TCC / FDA 権限剥奪・ディスク full・認証失効等）ら、失敗を繰り返さず即座に (1) 範囲診断で環境起因を確定、(2) 停止を明示、(3) 人間が実行できる具体手順 + 確認コマンドを提示せよ。これは「認可を求める」（禁止）ではなく「AI 権限外の障害復旧を委ねる」（正当）。境界の混同に注意。
- 参考 memory: [[reference_local_environment]]（Mac ローカル setup / python3.9 落とし穴）。

### For human engineers（新卒レベル）
- macOS には TCC という「アプリごとに Desktop / Documents / Downloads へのアクセスを個別許可する」仕組みがある。ここでの許可が外れると、そのフォルダ配下は全部読めなくなる。リポジトリが Downloads の中にあったため、権限が外れた瞬間に全操作が止まった。直し方は「アプリを再起動して OS の許可プロンプトに"許可"」か「システム設定で手動許可」。

### For third parties / auditors
- 「AI が自走を止めて人間に助けを求めた」唯一の実例が、**AI の判断ミスや改善の頭打ちではなく、OS 仕様による物理的アクセス不能**だったことを示す一次記録。AI は障害を隠さず・失敗を空回りさせず・正確な復旧手順を提示して待機した。全委任・無限自走モデルにおける「人間が制御と監査のみを担う」境界が、例外時にどう機能したかの透明な証跡である。
