---
file: js/settings-io.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-20
canonical-ref: js/settings-page.js / js/store.js / e2e/apps-settings-io.spec.js / e2e/apps-settings-import-shape.spec.js / e2e/apps-settings-ingestion.spec.js
---

# js/settings-io.js

## What

Settings の**入出力**を担う葉モジュール。`createSettingsIO({ deps })` が
`{ exportFull, exportProjects, exportApps, exportProfile, importJSON, lossParts }` を返す。

- **export**: フルバックアップ / Projectsのみ / AppsDataのみ / Profileのみ の 4 形
- **import**: 上記 4 形すべてを受け付け、モード（追加のみ / 更新+追加 / 全置換）と
  「対象」チェックボックスに従って適用する
- **lossParts**: 正規化で失われた分（entry / list 件数 / 文字数）を数え、報告文言を返す

## Why

`js/settings-page.js` が 746 行まで伸び、その中で**最大かつ最も独立していたのが IO 面**
だった（専用 spec が 3 本ある: `apps-settings-io` / `-import-shape` / `-ingestion`）。
分離により settings-page は 483 行になり、IO の契約とその spec が 1 対 1 で対応する。

**なぜ clean に切れたか**: IO クラスタが参照する UI 状態（取り込みモードと対象の
チェックボックス 4 つ）は **読み取りのみ**で、書き込みは settings-page 側の onchange が
行う。よって getter 1 つ（`getImportOptions`）を注入すれば closure を持ち出さずに済む。

## How (usage)

```js
// main.js（late-binding holder パターン）
let _opts = () => ({ mode: 'append', includeProfile: true, includeProjects: true, includeApps: true });
const SettingsIO = createSettingsIO({ State, Store, Toast, Brand, getImportOptions: () => _opts() });
const { SettingsPage, getImportOptions } = createSettingsPage({ …, IO: SettingsIO });
_opts = getImportOptions;   // 相互参照を holder で解く
```

**なぜ値ではなく getter か**: `importJSON` は `FileReader` の `onload`（非同期）で適用する。
値を渡すと **選択時ではなく読み込み開始時の値**を使うことになる。

## Constraints

- **葉契約**: ローカル ESM import ゼロ。依存は `createSettingsIO` の引数で受け取る。
- **外部入力は全経路正規化**（#93/#295/#561）: `importJSON` は必ず
  `Store.validateAndNormalize` を通してから `State.set` する。**Check 374** が強制。
- **切り捨てたら黙るな**（#1143/#1178/#1181/#1182/#1186/#1187）: 取り込み・復元で
  失われた分は `lossParts` が数えて報告する。過少報告も**過剰報告**も等しく悪い ——
  失っていないのに警告を出すと本物の警告が信用されなくなる。
- **Check 46a/46b**（lint 対象）/ **Check 381**（`_modules47`）/ **Check 57**（modulepreload）/
  **Check 108**（mirror doc）/ **Check 119a・372**（依存契約）が配線の欠落を止める。

## Change impact

- モードの意味論を変えるときは **3 モードすべて**を測ること。「追加のみ」は
  「既存を壊さない」という約束で、ここが崩れると**最も安全なつもりの選択が最も破壊的**に
  なる（#1183 の実バグ）。
- `lossParts` は import と snapshot 復元の**両方**が使う。片方だけ honest だと
  「復元は無事だった」と誤解される（#1186）。

## Audience-specific notes

### For AI agents
- 役割タグ: `leaf-module`, `settings-io`, `ingestion`, `data-safety`

### For human engineers (新卒レベル)
- 「バックアップを戻す」機能は、**書き出す側と読み込む側のキー集合**が一致していないと
  黙ってデータを失う。往復（export → import）で確かめるのが唯一の検出手段。

### For third parties
- 取り込みの損失を利用者へ honest に報告する実装例（件数・文字数・既存優先の 3 面）。
