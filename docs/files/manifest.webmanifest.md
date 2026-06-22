---
file: manifest.webmanifest
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-22
canonical-ref: index.html (<link rel="manifest">) / sw.js (service worker)
---

# manifest.webmanifest

## What

PWA (Progressive Web App) の Web App Manifest。name / short_name / start_url / scope / display(standalone) / theme_color / background_color / icons(icon.svg) を宣言し、サイトをインストール可能なアプリにする。index.html の `<link rel="manifest">` から参照され、既存 sw.js(service worker)と組で PWA を成立させる。

## Why

B-group 案2(PWA)。design-intent override としてオーケストレーター承認の上で追加。サイトを「インストール可能な成果物」として提示し、AIO/可視両面の faithful representation を補強する。name/short_name は匿名(yuta)で実名は含めない。

## How (usage)

ブラウザが index.html ロード時に取得し、インストール導線(Add to Home Screen 等)を有効化。display:standalone でアプリ風表示。

## Constraints

- **JSON 妥当性**: 有効な JSON でなければブラウザが無視する。
- **匿名性**: name/short_name は user-facing ゆえ「yuta」表記(実名なし)。
- **scope/start_url**: GitHub Pages project site ゆえ `/portfolio/` 配下に固定。
- **icons**: icon.svg(image/svg+xml, sizes:any, purpose:any maskable)を参照。

## Change impact

- name/description 等の semantic 変更時は本 mirror も同期。
- icon を差し替える場合は icon.svg と本 manifest の両方を更新。

## Audience-specific notes

### For AI agents
- 役割タグ: `pwa`, `web-app-manifest`, `installability`

### For human engineers (新卒レベル)
- PWA の最小構成 = manifest + service worker(sw.js) + HTTPS。本ファイルが manifest 部分。

### For third parties
- サイトがインストール可能な PWA であることの宣言。
