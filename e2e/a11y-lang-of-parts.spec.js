const { test, expect } = require('@playwright/test');

// ===== WCAG 3.1.2 Language of Parts — 英語だけの塊に lang="en" が付くこと =====
// `a11y-axe.spec.js` から分離 (2026-08-22)。同 file が advisory 予算 900 行を超え
// BLOCKING の 1,000 行まで 50 行に迫っていたため、**当たってから慌てるのではなく**
// 手前で、単一の達成基準 (WCAG 3.1.2) という coherent な塊として切り出した。
//
// この面で behavior e2e が唯一の gate である理由:
//   **axe には該当ルールが無い** (`html-lang-valid` は文書全体の lang しか見ない)。
//   行の言語は data 側で混在しうるので静的にも決められず、描画時に文字種で判定する
//   (判定の実体は `js/pure-utils.js` の `langOfText` に一本化されている)。
//
// 日本語 (`html lang="ja"`) の文書に英語だけの塊があると、日本語 SR は
// **英語を日本語の音韻で読み上げる**。

const A11Y_ROUTES = ['#/', '#/projects', '#/about', '#/contact', '#/resume', '#/apps', '#/settings', '#/quiz', '#/apps/task', '#/apps/todo', '#/apps/pomodoro', '#/apps/ai', '#/apps/notes', '#/hiring-risk', '#/ai-knowhow', '#/role-split', '#/not-found'];

// `a11y-axe.spec.js` から複製 (分離時 2026-08-22)。e2e は spec 完全自己完結が house pattern で
// spec 間で require し合う前例が無いため、`A11Y_ROUTES` と同じく helper も複製する。
//
// 走査の直前に #content の描画が落ち着くのを待つ。**見出しが変わったことだけでは足りない** ——
// 見出しは DOM の先頭に出るが、この test が見る要素 (英語だけの塊を含む本文・badge・CTA) は
// 後から描かれる。要素数が 2 フレーム連続で変わらなくなるまで待つ。
async function settleContent(page) {
  await expect.poll(async () => await page.evaluate(() => {
    const before = document.querySelectorAll('#content *').length;
    return new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(
      () => resolve(before === document.querySelectorAll('#content *').length ? before : -1))));
  }), '#content の描画が落ち着かない').toBeGreaterThan(0);
}

// ===== 全ルートで「英語だけの文」に lang="en" が付くこと (WCAG 3.1.2・quiz 以外) =====
// 下の test は **quiz 限定**で、しかも判定が `^[\x20-\x7E]+$` (ASCII のみ) なので
// 絵文字や `→` を含む英語見出し ("📋 Executive Summary" / "Read Technical Deep-Dive →") を
// 見逃す。実測 (2026-08-21): 全 16 ルートを走査すると **5 箇所**が未指定で残っていた ——
// home の Value Points 3 件 (`<strong>AI self-driving execution:</strong>` 等) /
// home の英語 CTA リンク / hiring-risk の "📋 Executive Summary" (badge と h2 の 2 箇所)。
//
// **意図的に対象外にしているもの** (機械的に全部付けるのは意味論の水増しになる):
//   - 英単語が 1 つだけのラベル (カテゴリ名 "Productivity" 等)
//   - メールアドレス / URL / 版数のような識別子 (自然言語ではない)
//   - 固有名詞だけの塊 (ブランド名 + フォント名 "Classic Blue + Inter")
// これらは除外条件として下のコードに書いてあるので、**除外を緩めると RED になる**。
test('全ルートで英語だけの文に lang="en" が付く (WCAG 3.1.2)', async ({ page }) => {
  test.setTimeout(150000);
  const misses = [];
  let scanned = 0;

  let prevHeading = null;
  for (const route of A11Y_ROUTES) {
    await page.goto('/' + route, { waitUntil: 'domcontentloaded' });
    // [FIX] `#content h1` の可視だけで待つと **前ルートの DOM で充足**し、まだ描画されていない
    //   ページを走査して「違反ゼロ」と誤報告する (実測 2026-08-21: hiring-risk の h2 から
    //   lang を外す mutation が素通りした)。見出しが前ルートと変わったことを待つ ——
    //   同ファイルの LABEL_IN_NAME_ROUTES ループと同じ手法。
    await expect
      .poll(() => page.locator('#content').getByRole('heading').first().textContent().catch(() => null))
      .not.toBe(prevHeading);
    prevHeading = await page.locator('#content').getByRole('heading').first().textContent();
    await settleContent(page);
    scanned += 1;

    const rows = await page.evaluate(() => {
      const out = [];
      const walk = document.createTreeWalker(document.getElementById('content'), NodeFilter.SHOW_TEXT);
      let n;
      while ((n = walk.nextNode())) {
        const t = (n.textContent || '').trim();
        if (t.length < 12) { continue; }
        // 日本語 (かな/漢字/全角記号/波ダッシュ) を含む → 対象外
        if (/[\u3000-\u303f\u3040-\u30ff\u4e00-\u9fff\uff00-\uffef]/.test(t)) { continue; }
        // メール / URL / 版数のような識別子は自然言語ではない
        if (/@|https?:|\.(com|dev|io|jp)\b/.test(t)) { continue; }
        if (!/[A-Za-z]{3}/.test(t)) { continue; }
        // 英単語が 2 語以上 (1 語だけのラベルは「文」ではないので対象外)
        if ((t.match(/[A-Za-z][A-Za-z'-]{1,}/g) || []).length < 2) { continue; }
        let el = n.parentElement, lang = null;
        while (el && el !== document.body) {
          if (el.getAttribute('lang')) { lang = el.getAttribute('lang'); break; }
          el = el.parentElement;
        }
        if (lang !== 'en') { out.push(n.parentElement.tagName + ':' + t.slice(0, 34)); }
      }
      return out;
    });
    for (const x of rows) { misses.push(route + ' ' + x); }
  }

  // control: 全ルートを走査できたこと (途中で落ちていると「違反ゼロ」と区別が付かない)
  expect(scanned, 'control: 全ルートを走査できていない').toBe(A11Y_ROUTES.length);

  // 既知の例外 —— 自然言語の「文」ではないので lang を付けない (付けると意味論の水増し)
  const KNOWN = [
    'P:v74 ',                    // 版数 + 技術スタックの識別子列
    'OPTION:Classic Blue + Inter', // ブランド名 + フォント名 (固有名詞のみ)
  ];
  const genuine = misses.filter((m) => !KNOWN.some((k) => m.includes(k)));
  expect(genuine,
    '英語だけの文に lang="en" が無い: ' + genuine.slice(0, 4).join(' / ')).toEqual([]);

  // control: 既知の例外が実在すること —— 消えたら KNOWN も畳むべきで、
  //   残したままだと「例外リストが実態と乖離する」drift になる
  expect(misses.length,
    'control: 既知の例外が 1 つも見つからない — KNOWN が実態と乖離している').toBeGreaterThan(0);
});


// ===== 英語だけの塊に lang="en" が付くこと (WCAG 3.1.2 Language of Parts) =====
// 文書は `html lang="ja"`。日本語文字を 1 つも含まない塊をそのまま置くと、日本語の
// スクリーンリーダーが **英語を日本語の音韻で読み上げる**。実測 (#1020) では quiz だけで
// 49 箇所あり、うち "Core Knowledge & Tech Lead's View:" が 34 回繰り返されていた。
//
// 行の言語は data (js/quiz/*.js) 側で混在するので静的には決められない。描画時にその行の
// 文字種で判定する (日本語文字が無く Latin 文字がある → en)。AWS のサービス名のような
// 固有名詞にも付くが、英語音韻で読ませたいのはむしろ正しい。
//
// axe には該当ルールが無い (`html-lang-valid` は文書全体の lang しか見ない)。捕捉層はこの test だけ。
test('quiz の英語だけの塊に lang="en" が付く', async ({ page }) => {
  await page.goto('/#/quiz', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: '問題集' })).toBeVisible();

  const s = await page.evaluate(() => {
    const c = document.getElementById('content');
    const leaves = Array.from(c.querySelectorAll('h1,h2,h3,p,span,div,li,td,th'))
      .filter(e => !e.querySelector('h1,h2,h3,p,span,div,li,td,th'));
    const isEnglishOnly = (t) => t.length >= 12 && /^[\x20-\x7E]+$/.test(t) && /[A-Za-z]{4,}/.test(t);
    const JA = /[ぁ-んァ-ヶ一-龯]/;
    return {
      leafCount: leaves.length,
      taggedEn: c.querySelectorAll('[lang="en"]').length,
      // (a) 英語だけなのに lang 指定が無い塊
      untagged: leaves.filter(e => isEnglishOnly((e.textContent || '').trim()) && !e.closest('[lang="en"]'))
        .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 30)}`),
      // (b) 逆方向 — 日本語を含むのに lang="en" が付いている (過剰適用)
      overTagged: Array.from(c.querySelectorAll('[lang="en"]'))
        .filter(e => JA.test(e.textContent || ''))
        .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 30)}`),
    };
  });

  // control: そもそも描画されていること (0 件なら何も検証していない)
  expect(s.leafCount, '本文が描画されていない — この test の前提が崩れている').toBeGreaterThan(100);
  expect(s.taggedEn, `lang="en" が付いた要素が少なすぎる (${s.taggedEn} 件) — 付与経路のどれかが落ちている`).toBeGreaterThanOrEqual(20);

  expect(s.untagged, `英語だけなのに lang 指定が無い塊: ${s.untagged.slice(0, 4).join(' / ')}`).toEqual([]);
  expect(s.overTagged, `日本語を含むのに lang="en" が付いている (過剰適用): ${s.overTagged.slice(0, 4).join(' / ')}`).toEqual([]);
});

// ===== 固定の英語文字列にも lang="en" が付くこと (WCAG 3.1.2) =====
// #1020 は data 由来の行 (quiz) を描画時判定で処理した。こちらは **コードに直書きされた
// 英語文字列**で、判定の余地が無いのでリテラルに付ける。
// 対象は実測 (#1021) で見つかった 5 箇所 — home の英文キャプション / hero の CTA 2 つ /
// 「Verification & Evidence」見出し / About の h1。
test('固定の英語文字列に lang="en" が付く (home / about)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();

  await expect(page.locator('#content p.text-caption')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#content .cta-primary')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#content .cta-secondary')).toHaveAttribute('lang', 'en');
  await expect(page.locator('#evidence-heading')).toHaveAttribute('lang', 'en');

  await page.goto('/#/about', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'About' })).toBeVisible();
  await expect(page.locator('#content h1')).toHaveAttribute('lang', 'en');

  // 逆方向: 日本語の見出しに lang="en" が付いていないこと (過剰適用の検出)
  const overTagged = await page.evaluate(() =>
    Array.from(document.querySelectorAll('#content [lang="en"]'))
      .filter(e => /[ぁ-んァ-ヶ一-龯]/.test(e.textContent || ''))
      .map(e => (e.textContent || '').trim().slice(0, 24)));
  expect(overTagged, `日本語を含むのに lang="en" が付いている: ${overTagged.join(' / ')}`).toEqual([]);
});

// data 由来のテキスト (利用者が編集できる profile / project) にも同じ判定が効くこと。
// 判定は js/pure-utils.js の `langOfText` に一本化されており、quiz / home / resume の
// 3 箇所が注入で共有する (1 行の正規表現でもコピーすれば invariant の二重化になる)。
test('data 由来のテキストにも lang="en" が付く (home badge / resume 職種)', async ({ page }) => {
  await page.goto('/#/', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1')).toBeVisible();
  await expect(page.locator('#content span.badge-primary').first()).toHaveAttribute('lang', 'en');

  await page.goto('/#/resume', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('#content h1', { hasText: 'Resume' })).toBeVisible();
  await expect(page.locator('#content h2').first()).toHaveAttribute('lang', 'en');

  // 英語だけなのに lang 指定が無い塊が resume に残っていないこと
  const remaining = await page.evaluate(() => {
    const c = document.getElementById('content');
    return Array.from(c.querySelectorAll('h1,h2,h3,p,span,div,li,td,th,button'))
      .filter(e => !e.querySelector('h1,h2,h3,p,span,div,li,td,th,button'))
      .filter(e => { const t = (e.textContent || '').trim(); return t.length >= 12 && /^[\x20-\x7E]+$/.test(t) && /[A-Za-z]{4,}/.test(t); })
      .filter(e => !e.closest('[lang="en"]'))
      .map(e => `${e.tagName}:${e.textContent.trim().slice(0, 24)}`);
  });
  expect(remaining, `英語だけなのに lang 指定が無い: ${remaining.join(' / ')}`).toEqual([]);
});
