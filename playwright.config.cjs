// playwright.config.cjs
// Shared Playwright configuration for regression and snapshot-update workflows.
// Used by:
//   .github/workflows/playwright-regression.yml
//   .github/workflows/update-playwright-snapshots.yml
// Do NOT duplicate this config inside workflow heredocs.

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './e2e',
  timeout: 30000,
  expect: {
    timeout: 5000,
    // WHY この許容値か (baseline-gate の感度設計): threshold/maxDiffPixelRatio はフォント
    // アンチエイリアス等の環境差由来の微小ピクセル差で false-fail しない緩さを持たせつつ、
    // レイアウト崩れ等の本物の視覚 regression は捕まえる balance。0 に締めると baseline が
    // flaky になり「壊れていないのに赤」を量産し、緩めすぎると regression を見逃す。baseline は
    // CLAUDE.md §3 の Stage 5 安全ゲートの中核なので値の変更は慎重に。
    toHaveScreenshot: { threshold: 0.05, maxDiffPixelRatio: 0.02 }
  },
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
    screenshot: 'on',
    // WHY env-gated serviceWorkers: mutation-probe (MUTATION_PROBE=1) 実行時のみ SW を block する。
    // 通常 e2e/CI では SW を許可し実アプリ (SWR キャッシュ/オフライン層込み) を検証する。だが
    // mutation-probe は「JS ロジックを 1 箇所壊して e2e が RED になるか」で安全網の非 vacuity を
    // 検証するツールで、sw.js の SWR キャッシュが壊す前の旧 JS を配信すると mutated コードが
    // 反映されず mutation を見逃す (net が「捕捉した/しない」を誤報告する) false-result を生む。
    // probe 実行に限り SW を block し、毎ロード必ず network から mutated JS を取得させて結果を
    // 決定的にする。E2E_MUTATIONS の全テストはアプリ*ロジック*を検証し SW 挙動には非依存ゆえ
    // block しても clean baseline は緑のまま (SW はキャッシュ/オフライン層で機能性の前提でない)。
    serviceWorkers: process.env.MUTATION_PROBE ? 'block' : undefined,
  },
  projects: [{
    name: 'chromium',
    use: {
      ...devices['Desktop Chrome'],
      // WHY env-gated hermetic mode (E2E_HERMETIC=1):
      //   実測では 1 ナビゲーションごとに **6 つの第三者ホストへ 9 リクエスト** が飛ぶ
      //   (KARTE: cdn-edge / static / b / mirror2、Google Fonts: fonts.googleapis.com /
      //   fonts.gstatic.com)。しかも `page.goto()` の既定 waitUntil は 'load' なので、
      //   **それらの完了を待つ**。suite 全体では ~334 ナビゲーション ＝ BLOCKING ゲートの
      //   合否が第三者 CDN の可用性とレイテンシに依存していた (2026-08-10 に実際
      //   `.hero-section` の 30s timeout として flake 化し、rerun 1 回で緑になった)。
      //   Chromium の DNS ルールで localhost 以外を即 NOTFOUND にすると、外部は
      //   **ハングせず即失敗**する。実測: goto の所要が 447ms → 39ms、アプリは fatal なし
      //   (KARTE も Fonts も機能性の前提ではなく、behavior test は一切 assert していない)。
      // WHY 既定 ON にしないか:
      //   screenshot baseline は実フォントで撮られているため、フォントを遮断すると
      //   ADVISORY の視覚シグナルが恒久的に無意味になる。CI は behavior と screenshot を
      //   別ステップに分けている (--grep-invert / --grep "screenshot regression") ので、
      //   **behavior ステップだけ** に env を立てる。ローカルの全件実行は従来どおり
      //   (外部あり) で、CI 側だけが厳密になる = ローカルが CI より緩い安全な向き。
      //   MUTATION_PROBE と同じ env-gate の作法 (Check 416 が behavior ステップでの
      //   設定を機械強制する)。
      launchOptions: process.env.E2E_HERMETIC
        ? { args: ['--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost'] }
        : {},
    },
  }],
  webServer: {
    command: 'npx http-server . -p 8080 --silent',
    url: 'http://localhost:8080',
    // WHY reuseExistingServer: false — CI / ローカルとも必ず新しい static server を起動し、
    // commit 済みファイルに対してテストする。既存 dev server を再利用すると stale な編集前
    // 状態を検証してしまい「緑なのに実際は壊れている」false-green を招く。
    reuseExistingServer: false,
    timeout: 15000,
  },
});
