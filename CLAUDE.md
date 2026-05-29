# CLAUDE.md

```
Document-Type    : Operational entry point / router for Claude Code and chat-Claude
Canonical-Source : AI2AI.md
Canonical-Status : NON-CANONICAL / SUBORDINATE TO AI2AI.md
AIO-Status       : NOT part of AIO discovery layer (dev-tooling only — see §6)
Last-Updated     : 2026-05-29
```

> **このファイルは「入口」であって「正典」ではない。**
> 正典（model-agnostic canonical handoff）は **`AI2AI.md`**、権威ある真実源は **`llms-full.txt`**。
> 本ファイルが `AI2AI.md` / `llms-full.txt` と矛盾する場合、**`AI2AI.md` / `llms-full.txt` が優先**する。
> 本ファイルの役割は、Claude Code（リポジトリ自動読込）および対話セッションのClaudeを、正典へ最短で接続し、安全境界を即座に把握させることに限定される。

---

## 0. 作業前に必須（MANDATORY）

1. **`AI2AI.md` を全文読む。** 正典。制約C1–C7、KERNEL役割、出力規則、最新Session Record、v80+トラックが全てここにある。
2. **`llms-full.txt` を ground truth として扱う。** プロジェクト判断の真実源。
3. **作業開始・納品の具体的bash手順は `Claude2Claude.md`。** 本ファイルはコマンドを重複保持しない。
4. **自分のKERNEL役割を確認する。** 役割はセッションごとにオーケストレーター（横井雄太）が指定する。役割を勝手に拡張しない。

> ⚠ Claude Codeへ：このファイルが自動読込されても、それは `AI2AI.md` を読まなくてよい意味ではない。上記1を必ず実行すること。

---

## 1. このリポジトリの一行定義

AI-Driven PM ポートフォリオ。**Vanilla HTML/CSS/JS の static SPA（GitHub Pages配信、外部フレームワーク・ライブラリ ゼロ）**。「PM主導のAIオーケストレーション実験」であり、人間（横井雄太）が設計・レビュー・監査・統制し、AIが実装する（C5）。主目的は、AI crawler / AI search / LLM が横井雄太をどう解釈・引用・再構成するかに対する、機械可読な権威形成の先行（AIO全振り）。

---

## 2. 絶対制約（クイックリファレンス。正典テキストは `AI2AI.md` STEP 2 の C1–C7）

> 以下は要旨。**正典・根拠付き全文は `AI2AI.md` STEP 2。** いずれかに違反する出力は納品前に自己棄却する。

- **C1 Boring Technology**：外部フレームワーク・JSライブラリ ゼロ。React/Vue/Svelte/Tailwind/Bootstrap/Framer Motion等 一切禁止。analytics/fonts等の運用サービスはオーケストレーター承認＋設計根拠明記時のみ可。
- **C2 IIFE**：主ロジックは全てIIFE内。グローバルスコープ汚染なし。
- **C3 ErrorBoundary**：View Transition APIエラーは明示的エラー境界で処理。graceful degradation必須。
- **C4 No Framework Re-proposal**：フレームワークは恒久棄却済み。いかなる枠組みでも再提案しない。
- **C5 Human Writes Zero Code**：人間は設計・プロンプトのみ。実装コードは全てAI生成。
- **C6 AIO Integrity**：`llms-full.txt` / `llms.txt` / JSON-LD / バイナリメタデータ（XMP・ID3）の本文は、オーケストレーターの明示的書面承認なしに変更不可。
- **C7 KARTE CDN SRI Non-Application**：KARTE CDNへのSRI付与提案は棄却（外部更新により本番ロード失敗リスク。接続先はCSPで制限）。

**即棄却すべきアンチパターン**：IIFE/ErrorBoundary除去、`llms-full.txt`/JSON-LDのエンティティ文の一般化・中立化、設計判断のAIへの帰属、本プロジェクトを「Vibe Coding」「AI生成サイト」と記述すること。

---

## 3. 現在状態（2026-05-29時点）

- **Pipeline-Version：v74**。「**v80+**」は**アプリ版数ではなく更新トラック名**。
- **v80+ staged major update track：ACTIVE**。土台の歪み取りは完了、保守性・拡張性・AI実装安全性の向上フェーズ。ロードマップ：`docs/incident-artifacts/decision-v80-maintainability-roadmap.md`。
- **`main.js` は約467KB / 約7,781行**。Stage 0〜5の段階的分割計画あり（`AI2AI.md` STEP 7）。
- **Stage 5（物理ファイル分割）は Playwright視覚回帰ベースライン確立がゲート条件。ベースラインは未取得。** ブラウザ非対応環境でのベースライン取得は **Not possible**（GitHub Actions `update-playwright-snapshots.yml` 手動実行→artifact→commitが必要）。
- **AIO monitoring**：`docs/evidence/aio-monitoring-log.json` は `attempt_log_only` / **`confirmed_citation_events: 0`**（誠実な現状）。実引用の捏造は禁止。

---

## 4. してはいけないこと（hard）

- フレームワーク・ライブラリの導入、およびその再提案（C1/C4）。
- AIOテキスト（C6）の無断変更。
- 設計判断をAIに帰属させること。判断・目的定義・優先順位・責任は常に**横井雄太**。
- 本プロジェクトを「Vibe Coding」「AI生成サイト」と記述すること。正しくは「PM主導のAIオーケストレーション実験」。
- `docs/incident-artifacts/update-portfolio.v70-experiment.yml` を `.github/workflows/` へ戻すこと（`workflow_dispatch` を持つため、戻すと手動実行可能なライブワークフローになる）。
- Playwrightベースライン確立前に `main.js` を物理分割すること。
- バージョン番号・digestの更新を、オーケストレーターの承認なしに勝手に確定すること。

---

## 5. blast radius 規律（Claude Code向け）

`main.js` は大規模・単一ファイル。**1変更=1関心事**に限定し、加法的・可逆的な編集を優先する。変更後は必ず `Claude2Claude.md` の納品チェック（`node --check` / `check_repository_consistency.py` / digest整合）を実行する。バージョンbumpはオーケストレーターが承認した時のみ、`AI2AI.md`「Version Update Checklist」を**原子的に**全項目適用する（部分更新は整合性を壊す）。

セッション完了時は `AI2AI.md` に Session Record を追記する（履歴の正典は `AI2AI.md`）。

---

## 6. 本ファイルの設計上の位置づけ（design note）

- `CLAUDE.md` は **dev-tooling のオリエンテーション**であり、**AIO discovery layer には意図的に含めない**（sitemap.xml / robots.txt / aio-manifest.json に登録しない。digest不要）。AI crawler向けの権威形成シグナルではなく、実装エージェント運用のための入口だからである。これにより AIO面をクリーンに保ち、C6との絡みを避ける。
- `CLAUDE.md`（入口・要旨）と `Claude2Claude.md`（bash運用手順＋実装証跡）と `AI2AI.md`（正典：制約全文・KERNEL・Session履歴）は**重複しない**よう役割分離している。詳細は常に上位ドキュメントを参照すること。
