/**
 * js/projects-page.js — ProjectsPage レンダラ (v80+ 肥大化解消: js/components.js から抽出)
 *
 * js/components.js からプロジェクト一覧ページ ProjectsPage (~172 行) を factory pattern で
 * 葉モジュールへ分離した。挙動 byte-equivalent (関数本体を無改変で移設)。
 *
 * 【依存 (引数注入)】
 *   - h          : DOM ビルダー (js/ui-components.js)
 *   - createIcon : SVG アイコンヘルパー
 *   - Router     : ルーター ({ navigate } 等) — プロジェクト詳細への遷移
 *   - State      : アプリ状態 ({ get() }) — プロジェクト一覧・検索/フィルタ
 *   - tokenize   : 検索トークナイザ (pure-utils)
 *   - clear      : DOM 子要素全削除 (main.js の純粋関数)
 *
 * 【葉契約】ローカル ESM import ゼロ (Check 47c)。全依存を引数注入。
 * 【非破壊性】main.js が createProjectsPage({ h, createIcon, Router, State, tokenize, clear })
 *   で生成し render dispatch (route 'projects') へ従来配線。検索フィルタ (updateSilently +
 *   手動 renderList) の focus 保持挙動含め byte-equivalent。behavior e2e が保証。
 */
export function createProjectsPage({ h, createIcon, Router, State, tokenize, clear }) {
    function ProjectsPage() {
        const state = State.get();
        const route = Router.getRoute();
        let q = route.query.q || '';
        let cat = route.query.cat || 'All';

        // [FIX] カテゴリ選択肢も非表示を除いた集合から導出 (listing 面 mesh・home-page.js 参照)。
        //   従来はカテゴリ全件を非表示にしても「選べるのに必ず 0 件」の option が残っていた。
        const _hiddenForCats = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
        const categories = ['All', ...new Set(state.projects
            .filter(p => !_hiddenForCats.has(String(p.id)))
            .map(p => p.category))];

        // [FIX] 無効な URL query cat (stale bookmark / カテゴリ削除後) は 'All' へ正規化。放置すると
        // <select> は option 不在で 'All' 表示なのに cat は無効値で空 filter = 「All なのに 0 件」desync
        // (外部入力 validate discipline・#93/#295 と同族)。
        if (cat !== 'All' && !categories.includes(cat)) { cat = 'All'; }

        // Uses the global tokenize() utility - no local duplicate

        function scoreProject(p, tokens) {
            if (!tokens.length) {return 1;}
            const corpus = [
                ...tokenize(p.name),
                ...tokenize(p.summary),
                ...(p.tags || []).map(t => String(t).toLowerCase()),
                ...(p.tech || []).map(t => String(t).toLowerCase()),
                ...tokenize(p.category)
            ];

            const freq = new Map();
            corpus.forEach(w => freq.set(w, (freq.get(w) || 0) + 1));
            // 部分一致用に重複を除いたユニークwordSet（toLowerCase多重呼び出し削減）
            const uniqueWords = Array.from(freq.keys());

            let score = 0;
            tokens.forEach(t => {
                if (freq.has(t)) {score += 5 + Math.min(3, freq.get(t));}
                uniqueWords.forEach(w => {
                    if (w !== t && w.includes(t)) {score += 1;}
                });
            });
            return score;
        }

        function getFilteredProjects() {
            let list = state.projects.slice();

            // Hide projects (Settings -> projectPrefs.hiddenIds)
            const hiddenIds = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
            if (hiddenIds.size) {list = list.filter(p => !hiddenIds.has(p.id));}

            if (cat !== 'All') {
                list = list.filter(p => p.category === cat);
            }

            const tokens = tokenize(q);
            if (tokens.length) {
                list = list
                    .map(p => ({ p, s: scoreProject(p, tokens) }))
                    .filter(x => x.s > 0)
                    .sort((a, b) => b.s - a.s)
                    .map(x => x.p);
            }

            return list;
        }

        function buildUI() {
            const container = document.createElement('div');
            container.className = 'flex flex-col gap-6';

            // [FIX] 全体再描画によるフォーカス喪失を防ぐため、リスト部分（Grid）だけを独立させる
            const gridContainer = document.createElement('div');
            gridContainer.className = 'grid-projects';
            gridContainer.dataset.entity = 'PortfolioProject';
            let countDisplay = null;

            function syncURL() {
                const params = new URLSearchParams();
                if (q) {params.set('q', q);}
                if (cat !== 'All') {params.set('cat', cat);}
                Router.replaceSilently('projects' + (params.toString() ? '?' + params.toString() : ''));
            }

            function renderGrid() {
                clear(gridContainer);
                const projects = getFilteredProjects();

                if (countDisplay) {countDisplay.textContent = `合計 ${projects.length} 件`;}

                if (projects.length === 0) {
                    gridContainer.appendChild(h('div', { class: 'card card--full-col', role: 'status', 'aria-live': 'polite' },
                        h('div', { class: 'card-body text-center text-muted' }, '条件に一致するプロジェクトはありません。')
                    ));
                    return;
                }
                projects.forEach(p => {
                    const card = h('article', { class: 'card card--flex-col', 'data-ai-context': 'Architecture designed by human, generated by AI' },
                        h('div', { class: 'card-body card-body--flex' },
                            h('div', { class: 'flex flex-wrap gap-2 mb-3' },
                                h('span', { class: 'badge badge-primary' }, p.category),
                                p.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                            ),
                            h('h2', { class: 'h3 mb-2' }, p.name),
                            h('p', { class: 'text-small text-muted mb-3' }, p.summary),
                            h('div', { class: 'flex flex-wrap gap-2 mb-4' },
                                ...(p.tags || []).slice(0, 4).map(tag =>
                                    h('button', {
                                        class: 'badge badge-secondary',
                                        onclick: () => {
                                            q = tag; cat = 'All';
                                            const inputEl = container.querySelector('input[aria-label="プロジェクト検索"]'); // type 非依存 (type=search でも解決)
                                            const selectEl = container.querySelector('select');
                                            if (inputEl) {inputEl.value = tag;}
                                            if (selectEl) {selectEl.value = 'All';}
                                            renderGrid(); syncURL();
                                            // [A11Y 2.1.1] このタグボタンは grid の中に居るので renderGrid() が
                                            //   自分自身を消し、focus が body へ落ちてドキュメント先頭からの
                                            //   Tab やり直しになる (実測 #995)。検索欄へ移すと「タグを検索語に
                                            //   入れた」という結果そのものが focus 先になり、続けて絞り込める。
                                            //   ここは _renderCore の復元経路 (#994) を通らない手動再描画ゆえ
                                            //   個別に手当てする。
                                            if (inputEl) { inputEl.focus({ preventScroll: true }); }
                                        }
                                    }, '#' + tag)
                                )
                            ),
                            // [A11Y 4.1.2] 「デモ」「詳細を見る」は全カードで同一 accessible name のため、
                            //   SR ユーザーはどのプロジェクトのボタンか区別できなかった。可視テキストは維持し
                            //   aria-label に p.name を suffix して一意化 (可視語を含むため WCAG 2.5.3 も充足)。
                            h('div', { class: 'flex gap-2 mt-auto' },
                                p.demoRoute ? h('button', { class: 'btn btn-secondary btn-sm', 'aria-label': 'デモ：' + p.name, onclick: () => Router.navigate(`apps/${p.demoRoute}`) }, 'デモ') : null,
                                h('button', { class: 'btn btn-ghost btn-sm', 'aria-label': '詳細を見る：' + p.name, onclick: () => Router.navigate(`projects/${p.slug}`) }, '詳細を見る')
                            )
                        )
                    );
                    gridContainer.appendChild(card);
                });
            }

            // Header
            container.appendChild(h('header', {},
                h('div', { class: 'flex flex-wrap items-center justify-between gap-4 mb-4' },
                    h('div', {},
                        h('h1', { class: 'h1' }, 'プロジェクト一覧'),
                        // [A11Y 4.1.3 Status Messages] 検索/カテゴリ絞り込みで件数 (`合計 N 件`) が変わっても
                        //   従来は SR ユーザーへ通知されなかった (0 件 empty-state は role=status 済だが、非 0 件の
                        //   件数変化は silent)。role=status + aria-live=polite で focus を移さずに件数変化を
                        //   アナウンスする (視覚描画は不変・render-neutral)。
                        countDisplay = h('p', { class: 'text-muted', role: 'status', 'aria-live': 'polite' }, '')
                    )
                ),
                h('div', { class: 'grid grid-cols-2 gap-4' },
                    // [A11Y] role='search' で検索入力を landmark 化する (ARIA APG search landmark)。
                    //   SR ユーザーが landmark ナビゲーションで検索領域へ直接ジャンプできる (WCAG 1.3.1
                    //   Info and Relationships)。視覚描画は不変 (role 属性のみ・render-neutral)。単一
                    //   search ゆえ aria-label 不要 (内包する input の aria-label='プロジェクト検索' が
                    //   landmark の意味を担う)。
                    h('div', { class: 'relative', role: 'search' },
                        h('div', {
                            class: 'absolute left-3 top-1/2 transform -translate-y-1/2 color-muted'
                        }, createIcon('search', 18)),
                        h('input', {
                            type: 'search',
                            class: 'input pl-10',
                            placeholder: '検索（名前/概要/タグ/技術/カテゴリ）...',
                            value: q,
                            'aria-label': 'プロジェクト検索',
                            oninput: (e) => {
                                q = e.target.value;
                                renderGrid(); // 部分更新でフォーカスを死守
                                syncURL();    // history.replaceStateで静かにURL同期
                            }
                        })
                    ),
                    h('select', {
                        class: 'input',
                        'aria-label': 'カテゴリフィルター',
                        // [A11Y 2.1.1] 再描画で消えた後に focus を戻すための安定ハンドル
                        //   (main.js _renderCore が復元する / Check 422)。本ページの絞り込みは
                        //   listHost の手動再描画で #content を作り直さないため現状は focus を
                        //   失わないが、全再描画へ変わった瞬間に沈黙して壊れる面なので先に固定する。
                        id: 'projects-category-filter',
                        onchange: (e) => {
                            cat = e.target.value;
                            renderGrid();
                            syncURL();
                        }
                    },
                        ...categories.map(c => h('option', {
                            value: c,
                            text: c === 'All' ? '全カテゴリー' : c,
                            // <select> に value content attribute は HTML 仕様上存在しない (Check 367)。
                            // 選択状態は各 option の selected: で反映する (h() undefined-skip が非選択を除外)。
                            selected: c === cat ? true : undefined
                        }))
                    )
                )
            ));

            renderGrid(); // 初期描画
            container.appendChild(gridContainer);
            return container;
        }

        return buildUI();
    }

    return ProjectsPage;
}
