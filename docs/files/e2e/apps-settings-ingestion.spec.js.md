---
file: e2e/apps-settings-ingestion.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-15
canonical-ref: playwright.config.cjs / js/store.js / js/state.js / js/settings-page.js / e2e/apps-settings-io.spec.js
---

# e2e/apps-settings-ingestion.spec.js

## What

**外部 ingestion（信用できない入力の取り込み）の正規化と型ガード**を固定する behavior e2e。
import / cross-tab / snapshot 復元 / load の各経路が受け取るデータについて、

- 非配列フィールドで `.filter` が TypeError を投げない（`#93` class）
- truthy な非文字列（`[]` / `{}`）が `String()` を素通りして空欄や `[object Object]` にならない
- 文字列長・件数の bound が効く（AI history / profile email / MAX_PROJECTS）
- 数値 id が文字列 id へ正規化され参照が解決する

を検証する。

## Why

取り込み経路は**アプリ自身が生成したデータとは限らない**（利用者が手で編集した JSON、別バージョンが
書いた store、壊れた localStorage）。正規化を一つの経路で省くと、**その経路のユーザーだけ**が
FatalPage に落ちたり、画面に `[object Object]` が出たり、localStorage が膨らんで描画が重くなる。

しかもこの class は **fatal を出さない形で壊れる**ものが多く、ErrorBoundary にも掛からず、視覚
baseline は ADVISORY なので、**behavior test を書いた面しか守られない**。過去の実バグ:

| 番号 | 内容 |
| :-- | :-- |
| #93 | Settings が Storage 依存の注入漏れで全ユーザー crash |
| #230 | AI history が無制限保存 |
| #295 | cross-tab だけ正規化を省いていた |
| #561 | snapshot 復元が未正規化採用 |
| #568 / #572 / #573 | 非配列フィールドで `.filter` が TypeError |
| #968 / #969 / #970 | truthy な非文字列が `String()` を素通り |

ファイル分離の理由は肥大化の**予防**。`apps-settings-io.spec.js` が 906 行となり早期警告（900）を
超えたため、**Check 365 の BLOCKING（1,000 行）を踏む前に**このテーマの塊を切り出した
（CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」）。mutation の `test` フィールドは
title 一致ゆえ file 移動の影響を受けない。

## How (usage)

```
npm run test:e2e
  └─ Playwright + http-server (playwright.config.cjs testDir: ./e2e)
  └─ e2e/*.spec.js は testMatch デフォルト (**/*.spec.js) で自動 discovery
```

## Constraints

- **Check 28**: 全 e2e/*.spec.js に test() のネスト無し
- **Check 111**: networkidle 待ちは screenshot (portfolio.spec.js) 以外で禁止
- **Check 114**: test.only/describe.only 無し (false-green footgun 防止)
- **Check 151**: 全 e2e/*.spec.js 横断で test() title 一意
- **Check 108**: docs/files ミラー 1 対 1 bijection
- **Check 408**: e2e spec は file-size-budget.md の BUDGET-DATA へ登録必須
- **Check 364 / 417**: store.js 側の構造防止（`(X || []).<throwing method>` 禁止 /
  untrusted 生値を `String()` へ直接渡さない）と対をなす。**静的 Check が書き方を禁じ、
  本 spec が挙動を固定する**二層

## Change impact

- `js/store.js` の正規化子を変更すると本 spec が RED になる
- 新しいフィールドを normalize に足したら、**敵対的な型を流す test も対で足す**
  （producer 側が安全でも consumer 側は独立に穴を持つ・#572）
- spec ファイル rename → docs/files ミラー同期 (Check 108) + BUDGET-DATA 同期 (Check 408)

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `ingestion-safety`, `data-fidelity`
- 「コードを読んで大丈夫そう」で clean と判断しないこと。**敵対的入力を実際に流して確かめる**
  （2026-08-10 に `profile.email` を「normalize で空にならない」と誤記録し、実測で反証された）

### For human engineers (新卒レベル)
- 外部から来たデータは「配列のはず」「文字列のはず」を**信じない**。`Array.isArray` /
  文字列判定を通してから使う。`v || fallback` は `[]` や `{}` のような **truthy な非文字列**を
  素通りさせるので型ガードにならない

### For third parties
- 信用できない入力を扱う層のテスト設計例。**壊れ方が fatal でない**（空欄になる / 文字化けする /
  黙って切り詰められる）ほど発見が遅れるため、挙動を明示的に固定している
