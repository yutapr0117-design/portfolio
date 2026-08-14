---
file: e2e/apps-settings-import-shape.spec.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-14
canonical-ref: playwright.config.cjs / .github/workflows/playwright-regression.yml / js/settings-page.js / e2e/apps-settings-io.spec.js
---

# e2e/apps-settings-import-shape.spec.js

## What

Settings の import が **「どの形のファイルを、どこまで受け付けるか」** の契約を固定する e2e。3 面:

1. **受け付ける形** — `Projectsのみ` (素の配列) / `AppsDataのみ` (素の appsData オブジェクト) を
   import で戻せる (往復)
2. **受け付けない形** — 判定できない JSON は成功と report せず、明示エラーを出す
3. **「対象」で全部落ちる形** — 形は認識できるがチェックボックスの選択で 1 セクションも
   適用されない場合も、成功と report しない

## Why

エクスポートは 4 つの形を書き出す (full backup / Projectsのみ / AppsDataのみ / Profileのみ)。import 側が
その一部しか受け付けないと、**バックアップとして提示している機能が「戻せないファイル」を作る**ことに
なる。しかも従来は戻せないときでも「インポートが完了しました」と報告していたため、利用者は復元できたと
信じてしまう —— これは失敗するより悪い。

- **#1038/#1039**: 部分 export の 3 形を import が一切受け付けていなかった (silent no-op + 成功報告)
- **#1040**: 形は認識できるのに「対象」の選択で中身が全部落ちる残り半分。加えて #1039 の e2e は
  `Projectsのみ` の枝しか通っておらず、`AppsDataのみ` / `Profileのみ` の枝は誰も踏んでいなかった

ファイル分離の理由は肥大化の**予防**。`apps-settings-io.spec.js` が 938 行となり早期警告 (900) を
超えたため、**Check 365 の BLOCKING (1,000 行) を踏む前に**このテーマの塊を切り出した
(CLAUDE.md §7「advisory は BLOCKING を踏む前に効かせる」)。mutation の `test` フィールドは title 一致
ゆえ file 移動の影響を受けない。

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
- **Check 420**: 登録する mutation の `find` は対象 file 内で一意

## Change impact

- test 追加/削除 → CI 時間 + behavior gate カバレッジ + mutation-probe-e2e の対応
- `js/settings-page.js` の `_normalizeImportShape` / `applied` 追跡を変更すると本 spec が RED になる
- spec ファイル rename → docs/files ミラー同期 (Check 108) + BUDGET-DATA 同期 (Check 408)

## Audience-specific notes

### For AI agents
- 役割タグ: `e2e-spec`, `behavior-gate`, `apps-settings`, `data-fidelity`
- 「成功と report しない」系の assertion は `#action-announcement` を読む (toast は 3 秒で消えるため
  CI 負荷で間欠 RED になる・#1018)。`.not.toContain('完了')` を併用して**嘘の成功報告**を直接禁じている

### For human engineers (新卒レベル)
- 「何も起きなかった」を検証するテストは、**control** (仕掛けが実際に効いている状態) を同じテストに
  埋めないと、条件が崩れた瞬間に何も検査せず緑になる。本 spec では
  `expect(isChecked()).toBe(false)` がその control

### For third parties
- backup/restore 機能の往復契約を e2e で固定した例。export と import はキー集合が非対称になりやすく、
  **アプリ自身の出力を入力に戻す**テストだけがその非対称を検出できる
