/**
 * js/components.js — UI page components (Sidebar / HomePage / ProjectsPage /
 * ProjectDetailPage / AppsPage / AboutPage / ResumePage / ContactPage /
 * FatalPage / AIKnowhowPage / ContactCTA) — v80+ Stage 5-m extraction via factory pattern
 *
 * main.js の 11 個の UI page render 関数を依存注入 (factory pattern) で物理分割した
 * 葉モジュール。Brand / Store / State / Theme / Meta Management と同じく、すべての closure
 * 依存を `createComponents` 関数の引数で受け取ることで、葉契約 (Check 47c: import ゼロ) を
 * 維持しつつ各関数の挙動と公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const Components = createComponents({...});
 *   const { Sidebar, HomePage, ProjectsPage, ProjectDetailPage, AppsPage, AboutPage,
 *           ResumePage, ContactPage, FatalPage, AIKnowhowPage, ContactCTA } = Components;
 *
 *   ContactCTA はさらに js/pages.js (createPages の引数) へも引き渡され、
 *   HiringRiskPage / RoleSplitPage で使用される。
 *
 * 【依存（引数で注入）】
 *   - h, createIcon, Toast, BGM: js/ui-components.js
 *   - AUTHOR: js/identity.js
 *   - Router: js/router.js
 *   - State: js/state.js factory instance
 *   - Theme: js/theme.js factory instance
 *   - Brand: js/brand.js factory instance
 *   - Store: js/store.js factory instance
 *   - tokenize: js/pure-utils.js (ProjectsPage 検索のスコアリング)
 *   - CONSTANTS: js/constants.js
 *   - clear: main.js IIFE の純粋関数 (DOM の子要素を全削除)
 *   - closeDrawer: js/mobile-drawer.js (ナビリンク選択時にドロワーを閉じる)
 *
 * 【非破壊性】
 *   - 11 関数の DOM 出力・class 名・style・aria 属性は byte-equivalent
 *   - イベントハンドラの動作・State.update への副作用も不変
 *   - Sidebar / HomePage / ProjectsPage の検索フィルタ・並び替えは挙動不変
 *   - ProjectDetailPage の関連プロジェクト類似度計算は Store.autoRelatedCandidates 経由で不変
 *   - AIKnowhowPage の article schema route 表示も不変
 *   - AIDK Kernel / AIO 正本層には影響しない
 */
export function createComponents({ h, createIcon, Toast, BGM, AUTHOR, Router, State, Theme, Brand, Store, tokenize, CONSTANTS, clear, closeDrawer }) {
    function Sidebar(isDrawer = false) {
        const state = State.get();
        const route = Router.getRoute();

        const primaryItems = [
            { icon: 'home',      label: 'ホーム',             path: '',           active: route.name === 'home' },
            { icon: 'users',     label: 'Human vs AI 分担表', path: 'role-split', active: route.name === 'role-split' },
            { icon: 'lightbulb', label: 'AI開発ノウハウ',     path: 'ai-knowhow', active: route.name === 'ai-knowhow' },
            { icon: 'user',      label: 'About',              path: 'about',      active: route.name === 'about' },
            { icon: 'briefcase', label: 'Resume',             path: 'resume',     active: route.name === 'resume' },
            { icon: 'mail',      label: 'Contact',            path: 'contact',    active: route.name === 'contact' },
        ];
        const secondaryItems = [
            { icon: 'briefcase', label: 'プロジェクト', path: 'projects',    active: route.name.startsWith('project') },
            { icon: 'shield',    label: 'Hiring Risk',  path: 'hiring-risk', active: route.name === 'hiring-risk' },
        ];
        const labItems = [
            { icon: 'apps',        label: 'アプリ一覧',    path: 'apps',               active: route.name === 'apps' },
            { icon: 'checkSquare', label: 'タスク管理',    path: 'apps/task',          active: route.name === 'app-task' },
            { icon: 'list',        label: 'クイックTODO',  path: 'apps/todo',          active: route.name === 'app-todo' },
            { icon: 'clock',       label: 'ポモドーロ',    path: 'apps/pomodoro',      active: route.name === 'app-pomodoro' },
            { icon: 'brain',       label: 'AI アシスト',   path: 'apps/ai',            active: route.name === 'app-ai' },
            { icon: 'cloud',       label: 'AWS 問題集',    path: 'quiz?type=aws',      active: route.name === 'quiz' && (!route.query.type || route.query.type === 'aws') },
            { icon: 'clipboard',   label: 'PM 問題集',     path: 'quiz?type=pm',       active: route.name === 'quiz' && route.query.type === 'pm' },
            { icon: 'award',       label: '品質・プロセス', path: 'quiz?type=quality', active: route.name === 'quiz' && route.query.type === 'quality' },
            { icon: 'zap',         label: '設計判断問題集', path: 'quiz?type=architecture', active: route.name === 'quiz' && route.query.type === 'architecture' },
            { icon: 'settings',    label: '設定・データ',   path: 'settings',           active: route.name === 'settings' },
        ];

        const isLabRoute = labItems.some(item => item.active);
        const labKey = 'portfolio_nav_lab_open_v69';
        function isLabOpen() {
            if (isLabRoute) {return true;}
            try { return localStorage.getItem(labKey) === 'true'; } catch { return false; }
        }
        function toggleLab(btn, body) {
            const open = btn.getAttribute('aria-expanded') === 'true';
            const next = !open;
            btn.setAttribute('aria-expanded', String(next));
            body.setAttribute('data-collapsed', String(!next));
            body.style.maxHeight = next ? body.scrollHeight + 'px' : '0';
            // codeql[js/clear-text-storage-of-sensitive-data] - False positive:
            // Stores non-sensitive UI expanded/collapsed state only.
            // No credentials, tokens, or PII are stored.
            try { localStorage.setItem(labKey, String(next)); } catch { /* ignore */ }
        }

        // v56: <a href> でGooglebotのリンク発見を保証しつつSPAルーターへ委譲
        // 改善文書b 11.1: closest() による堅牢なナビゲーションリンク捕捉
        // アイコンSVGや子<span>がクリックされた場合も `.nav-link` まで遡上して確実に発火する
        function navLink(item) {
            return h('a', {
                class: ['nav-link', item.active && 'active'],
                href: '#/' + item.path,
                onclick: (e) => {
                    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) { return; }
                    // closest() で意図した <a> 要素を確実に特定する
                    const link = e.target.closest('.nav-link');
                    if (!link) { return; }
                    e.preventDefault();
                    Router.navigate(item.path);
                    if (isDrawer) { closeDrawer(); }
                },
                'aria-current': item.active ? 'page' : undefined
            }, createIcon(item.icon), h('span', { text: item.label }));
        }

        function navGroupToggleButton(label, open) {
            return h('button', {
                class: 'nav-group-toggle',
                'aria-expanded': String(open),
                'aria-controls': 'nav-lab-body',
                onclick(e) {
                    const body = document.getElementById('nav-lab-body');
                    if (body) {toggleLab(e.currentTarget, body);}
                }
            },
                h('span', { class: 'nav-title' }, label),
                h('span', { class: 'nav-group-chevron', 'aria-hidden': 'true' }, '▼')
            );
        }

        const labOpen = isLabOpen();

        const content = h('div', { class: 'flex flex-col gap-2' },
            h('div', { class: 'flex items-center justify-between mb-4' },
                h('div', { class: 'flex flex-col' },
                    h('div', { class: 'h4' }, AUTHOR.DISPLAY_NAME),
                    h('div', { class: 'text-small text-muted' }, state.profile.title)
                ),
                isDrawer ? h('button', {
                    class: 'icon-btn', onclick: closeDrawer, 'aria-label': '閉じる'
                }, createIcon('x')) : null
            ),
            h('div', { class: 'divider' }),
            h('div', { class: 'nav-title' }, 'Primary'),
            ...primaryItems.map(navLink),
            h('div', { class: 'nav-title' }, 'More'),
            ...secondaryItems.map(navLink),
            navGroupToggleButton('Lab', labOpen),
            h('div', {
                id: 'nav-lab-body', class: 'nav-group-body',
                'data-collapsed': String(!labOpen),
                style: labOpen ? '' : 'max-height:0'
            }, ...labItems.map(navLink)),                h('div', { class: 'divider' }),
            h('div', { class: 'flex items-center justify-between p-3 rounded-lg' },
                h('div', { class: 'flex items-center gap-2' },
                    createIcon('music', 18),
                    h('div', { class: 'flex flex-col' },
                        h('div', { class: 'text-xs text-muted' }, 'BGM'),
                        h('div', { class: 'text-small font-semibold' }, BGM.isOn() ? '再生中' : 'オフ')
                    )
                ),
                h('button', {
                    class: 'icon-btn',
                    dataset: { bgmBtn: '' },
                    onclick: BGM.toggle,
                    'aria-label': BGM.isOn() ? 'BGMを停止する' : 'BGMを再生する',
                    'aria-pressed': String(BGM.isOn())
                }, createIcon(BGM.isOn() ? 'volume2' : 'volumeX'))
            ),
            h('div', { class: 'flex items-center justify-between p-3 rounded-lg' },
                h('div', { class: 'flex items-center gap-2' },
                    createIcon('palette', 18),
                    h('div', { class: 'flex flex-col' },
                        h('div', { class: 'text-xs text-muted' }, 'テーマ'),
                        h('div', { class: 'text-small font-semibold' },
                            state.theme === 'system' ? 'システム' : state.theme === 'dark' ? 'ダーク' : 'ライト'
                        )
                    )
                ),
                h('button', {
                    class: 'icon-btn',
                    onclick: Theme.cycle,
                    'aria-label': 'ライトモードとダークモードを切り替える'
                }, createIcon(state.theme === 'dark' || (state.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'sun' : 'moon'))
            )
        );

        return content;
    }

    function HomePage() {
        const state = State.get();
        const featured = state.projects.find(p => p.demoRoute === 'task') || state.projects[0];

        return h('div', { class: 'flex flex-col gap-6' },
            // ===== v68: Hero Copy — Business Value & Outcomes =====
            h('article', { class: 'card card--accent-top', role: 'region', 'aria-label': 'ヒーローセクション' },
                h('div', { class: 'card-body' },
                    h('div', { class: 'hero-section' },

                        // ── Left: Copy ──────────────────────────────────────────
                        h('div', { class: 'hero-copy' },

                            h('span', { class: 'hero-eyebrow' },
                                'AI 自走 × 人間統治の Engineering'
                            ),

                            h('h1', {
                                class: 'hero-headline',
                                'data-ai-content': 'lead',
                                'data-speakable': 'true'
                            },
                                h('em', {}, 'AI を自走させ、統治する PM')
                            ),

                            h('p', {
                                class: 'hero-subheadline text-lead',
                                'data-ai-content': 'tagline',
                                'data-speakable': 'true'
                            },
                                'AI が実装・検証・マージ・本番デプロイまで自走。機械統治された一貫性チェック群と behavior テストが担保し、このサイト自体がその生成物である。'
                            ),

                            h('p', {
                                class: 'text-caption'
                            },
                                'Led AI-driven development from concept to production, including rejecting hallucinated architectures.'
                            ),

                            h('ul', { class: 'hero-value-list', 'aria-label': 'Value Points' },
                                h('li', {},
                                    h('span', {},
                                        h('strong', {}, 'AI self-driving execution: '),
                                        'AI が実装・検証・マージ・本番デプロイまで自走し、次の一手の案出しも AI が担う。人間はコードを一行も書かない。'
                                    )
                                ),
                                h('li', {},
                                    h('span', {},
                                        h('strong', {}, 'Human-led architecture / decision making: '),
                                        'AIの技術前逸脱を人間が監査・棄却。設計思想の整合性を100%維持。'
                                    )
                                ),
                                h('li', {},
                                    h('span', {},
                                        h('strong', {}, 'Real production deployment: '),
                                        'GitHub Pages 上で実際に稼働。このサイト自体が、その自走 AI エンジニアリングの生成物である。'
                                    )
                                )
                            ),

                            h('div', { class: 'hero-cta-row' },
                                h('button', {
                                    class: 'btn btn-primary cta-primary',
                                    onclick: () => Router.navigate('role-split')
                                }, 'View Case Study'),
                                h('button', {
                                    class: 'btn btn-secondary cta-secondary',
                                    onclick: () => Router.navigate('ai-knowhow')
                                }, 'Explore Architecture')
                            ),

                            h('p', { class: 'hero-meta' },
                                'v74 · 73 iterations · No Framework · Pure Vanilla JS · ',
                                h('a', {
                                    href: 'https://zenn.dev/yuta_yokoi/articles/931f6e781d91f8',
                                    target: '_blank',
                                    rel: 'noopener noreferrer',
                                    class: 'color-primary'
                                }, 'Read Technical Deep-Dive →')
                            )
                        ),

                        // ── Right: Visual ────────────────────────────────────────
                        h('div', { class: 'hero-visual-wrap' },
                            h('img', {
                                src: './yuta-yokoi-ai-pm-orchestration-system.webp',
                                alt: 'AI Orchestrated PM Portfolio (6-Agent KERNEL Framework) — Zero-Code SPA: Strategy × Technology × Execution. Directed by Yuta Yokoi (横井雄太 / yutapr0117). 73 transitions (v1→v74).',
                                'data-entity': 'Yuta Yokoi (横井雄太 / Yokoi Yuta)',
                                'data-canonical': 'https://yutapr0117-design.github.io/portfolio/',
                                'data-ai-context': 'https://yutapr0117-design.github.io/portfolio/llms-full.txt',
                                'data-asset-role': 'hero-image',
                                id: 'hero-image',
                                width: '1536',
                                height: '1024',
                                loading: 'eager',
                                fetchpriority: 'high',
                                decoding: 'async',
                                class: 'hero-visual'
                            })
                        )
                    )
                )
            ),

            // ── まず見るべき3箇所 (The Big Three) ──
            h('section', { 
                class: 'card', 
                role: 'region', 
                'aria-label': 'まず見るべき3つの重要コンテンツ',
                style: { padding: 'var(--space-6)', background: 'var(--bg-secondary)', borderRadius: 'var(--radius-lg)' }
            },
                h('h2', { class: 'h3 mb-6 text-center' }, 'まずはこの3つだけ見てください'),
                h('div', { 
                    class: 'grid grid-cols-1 md:grid-cols-3 gap-6'
                },
                    // Card 1: Case Study
                    h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                        h('div', { class: 'card-body flex flex-col h-full' },
                            h('h3', { class: 'h4 mb-3' }, 'Case Studies（AI-Driven PMの成果）'),
                            h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, 'AI を自走させ・統治して出してきた成果を、代表的な事例だけまとめています。'),
                            h('button', { 
                                class: 'btn btn-primary btn-sm w-full mt-auto',
                                onclick: () => {
                                    const el = document.getElementById('evidence-heading');
                                    if (el) {el.scrollIntoView({ behavior: 'smooth' });}
                                },
                                'aria-label': 'ケーススタディセクションへ移動'
                            }, 'ケースを見る →')
                        )
                    ),
                    // Card 2: Role Split
                    h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                        h('div', { class: 'card-body flex flex-col h-full' },
                            h('h3', { class: 'h4 mb-3' }, 'Human vs AI 分担表'),
                            h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, '人間と複数AIをどう役割分担させているかを、1枚の表で可視化しています。'),
                            h('button', { 
                                class: 'btn btn-primary btn-sm w-full mt-auto',
                                onclick: () => Router.navigate('role-split'),
                                'aria-label': 'Human vs AI 分担表ページへ移動'
                            }, '分担表を見る →')
                        )
                    ),
                    // Card 3: AIO Series
                    h('div', { class: 'card flex flex-col h-full shadow-sm hover-shadow-md transition' },
                        h('div', { class: 'card-body flex flex-col h-full' },
                            h('h3', { class: 'h4 mb-3' }, 'AIO実践シリーズ'),
                            h('p', { class: 'text-muted text-sm mb-6 flex-grow' }, 'このポートフォリオをAIO視点でどう設計し、AIにどう読ませているかの全手順です。'),
                            h('a', { 
                                href: 'https://zenn.dev/yuta_yokoi',
                                target: '_blank',
                                rel: 'noopener noreferrer',
                                class: 'btn btn-primary btn-sm w-full mt-auto flex items-center justify-center',
                                'aria-label': 'ZennのAIO実践シリーズ・発展記事の一覧を新しいタブで開く'
                            }, 'Zennで読む →')
                        )
                    )
                )
            ),

            // ── Verification & Evidence + AIO Series（統合セクション）──
            // 旧: evidence-section と aio-series-section の2セクションが重複していたため統合
            h('section', { class: 'evidence-section', role: 'region', 'aria-label': 'AI-Driven PMとしての主なケーススタディ', 'aria-labelledby': 'evidence-heading' },
                h('h2', { class: 'evidence-title', id: 'evidence-heading' }, 'Verification & Evidence'),
                h('p', { class: 'evidence-summary' },
                    '人間はコードを書かず、AIチームを統制してSPAを構築・公開。AIの設計逸脱を検知し差し戻した実証ケース。'
                ),

                // 証拠カード（3枚）
                h('div', { class: 'evidence-grid' },
                    h('div', { class: 'evidence-card success' },
                        h('h3', {}, h('span', {}, '✅'), '実装証明'),
                        h('p', {}, '人間はコードを1行も書かず、6つのAIを管理してSPAを構築・公開'),
                        h('a', {
                            href: 'https://github.com/yutapr0117-design/portfolio',
                            target: '_blank',
                            rel: 'noopener noreferrer'
                        }, 'Repository →')
                    ),
                    h('div', { class: 'evidence-card source' },
                        h('h3', {}, h('span', {}, '📦'), 'ソースコード'),
                        h('p', {}, 'アプリケーションロジック外部ライブラリ非依存のVanilla JS SPA（GitHub Pagesで公開中）'),
                        h('a', {
                            href: 'https://github.com/yutapr0117-design/portfolio',
                            target: '_blank',
                            rel: 'noopener noreferrer'
                        }, 'GitHub →')
                    ),
                    h('div', { class: 'evidence-card failure' },
                        h('h3', {}, h('span', {}, '⚠️'), '失敗事例'),
                        h('p', {}, 'AIが設計逸脱（React化）→ PM判断でReject・分離'),
                        h('a', {
                            href: 'https://github.com/yutapr0117-design/ai-overengineering-exhibit',
                            target: '_blank',
                            rel: 'noopener noreferrer'
                        }, '失敗を見る →')
                    )
                ),

                // AIO実践シリーズ（同セクション内サブエリア）
                h('div', { class: 'aio-series-sub', 'aria-labelledby': 'aio-series-heading' },
                    h('h3', { class: 'aio-series-sub-title', id: 'aio-series-heading' },
                        h('span', {}, '📝'), 'AIO実践シリーズ＋発展記事（AIO効果順・計11本）'
                    ),
                    h('p', { class: 'aio-series-sub-desc' },
                        'AI-Driven PM による「人間主導 multi-AI オーケストレーション」の完全記録。'
                    ),
                    h('div', { class: 'aio-series-grid' },
                        ...([
                            ['PRIMARY', 'AIO Bot Governance 分類編｜AIクローラーを一括りにするな（学習・検索・ユーザーfetch・AIエージェントを分けて制御）', 'https://zenn.dev/yuta_yokoi/articles/5d1d7a7438d48d'],
                            ['実践編', 'AIO Bot Governance 実践編｜robots/WAF/CIDRでAIボットを本番制御する', 'https://zenn.dev/yuta_yokoi/articles/d99f8171bcf275'],
                            ['第4弾', 'AIOはHTMLで終わらない：実装まで一気通貫で設計する、バイナリ層AIO解説', 'https://zenn.dev/yuta_yokoi/articles/3735dc2683f900'],
                            ['集大成', 'Portfolio AIO Capstone｜AI検索・AI採用に向けた実装の総まとめ', 'https://zenn.dev/yuta_yokoi/articles/c82fe055816454'],
                            ['AI×AI', 'AI-to-AI Pipeline Design｜正典・制約・実ファイルでAIに状態を継承させる', 'https://zenn.dev/yuta_yokoi/articles/91cf894e1072c6'],
                            ['第6弾', 'SEO BotからAIO Botへ――意味のサプライチェーン設計とAIO成熟モデル v1.0（最終回）', 'https://zenn.dev/yuta_yokoi/articles/27fa4c511cd972'],
                            ['第5弾', '人間主導multi-AIオーケストレーションをゼロから再現する完全手順書', 'https://zenn.dev/yuta_yokoi/articles/340dbb85491fc8'],
                            ['第2弾', 'AIにサイトがどう解釈されるか｜llms.txtとAIOで調整した話', 'https://zenn.dev/yuta_yokoi/articles/7e18e6ee1577aa'],
                            ['第1弾', 'AI開発をPMが管理した実験｜コードを書かずにSPAを構築する', 'https://zenn.dev/yuta_yokoi/articles/931f6e781d91f8'],
                            ['第3弾', 'SPAに観測をどう入れるか｜GA4を使わなかった理由と構成', 'https://zenn.dev/yuta_yokoi/articles/49326c5c4e0aae'],
                            ['総括', 'AIO実践シリーズ総括｜全6本完結・6つの設計パターン', 'https://zenn.dev/yuta_yokoi/articles/6dad78f20f2505'],
                        ].map(([badge, title, url]) =>
                            h('div', { class: 'aio-article-card' },
                                h('span', { class: 'aio-article-num' }, badge),
                                h('a', { href: url, target: '_blank', rel: 'noopener noreferrer' }, title),
                                h('span', { class: 'aio-article-arrow' }, 'Zenn →')
                            )
                        ))
                    )
                )
            ),

                            // Featured Project
            h('div', { class: 'grid-2col' },
                h('article', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h3', { class: 'h3 mb-3' }, '注目のプロジェクト'),
                        h('div', { class: 'flex gap-2 mb-3' },
                            h('span', { class: 'badge badge-primary' }, featured.category),
                            featured.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                        ),
                        h('p', { class: 'text-muted mb-4' }, featured.name),
                        h('p', { class: 'text-small text-muted' }, featured.summary),
                        h('div', { class: 'flex gap-2 mt-4' },
                            h('button', {
                                class: 'btn btn-ghost btn-sm',
                                onclick: () => Router.navigate(`projects/${featured.slug}`)
                            }, '詳細 →'),
                            featured.demoRoute ? h('button', {
                                class: 'btn btn-secondary btn-sm',
                                onclick: () => Router.navigate(`apps/${featured.demoRoute}`)
                            }, 'デモ起動') : null
                        )
                    )
                ),

                h('article', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h3', { class: 'h3 mb-3' }, '設計上の工夫'),
                        h('ul', {
                            class: 'text-muted list-indented'
                        },
                            h('li', {}, 'Importは検証＋正規化＋衝突モード'),
                            h('li', {}, '整合性チェック→自動修復（重複/孤立/無効URL等）'),
                            h('li', {}, 'スナップショット→復元で最短復旧'),
                            h('li', {}, 'セマンティックHTML5 + ARIA対応'),
                            h('li', {}, '単一HTMLで完結（依存性最小化）')
                        )
                    )
                )
            ),

            // Stats
            h('section', { class: 'grid grid-cols-3' },
                h('div', { class: 'card' },
                    h('div', { class: 'card-body text-center' },
                        h('div', { class: 'h2 color-primary' }, String(state.projects.length)),
                        h('div', { class: 'text-small text-muted' }, 'プロジェクト')
                    )
                ),
                h('div', { class: 'card' },
                    h('div', { class: 'card-body text-center' },
                        h('div', { class: 'h2 color-success' }, String(state.appsData.tasks.length)),
                        h('div', { class: 'text-small text-muted' }, 'タスク')
                    )
                ),
                h('div', { class: 'card' },
                    h('div', { class: 'card-body text-center' },
                        h('div', { class: 'h2 color-warning' }, String(state.appsData.todos.length)),
                        h('div', { class: 'text-small text-muted' }, 'TODO')
                    )
                )
            ),

            // Contact CTA
            ContactCTA('PM設計・AI開発・アーキテクチャ設計のご相談を受け付けています。このSPAを見て「こういうものを作りたい」「AI導入を相談したい」「設計を一緒に考えたい」と感じた方は、お気軽にどうぞ。')
        );
    }

    function ProjectsPage() {
        const state = State.get();
        const route = Router.getRoute();
        let q = route.query.q || '';
        let cat = route.query.cat || 'All';

        const categories = ['All', ...new Set(state.projects.map(p => p.category))];

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
                                            const inputEl = container.querySelector('input[type="text"]');
                                            const selectEl = container.querySelector('select');
                                            if (inputEl) {inputEl.value = tag;}
                                            if (selectEl) {selectEl.value = 'All';}
                                            renderGrid(); syncURL();
                                        }
                                    }, '#' + tag)
                                )
                            ),
                            h('div', { class: 'flex gap-2 mt-auto' },
                                p.demoRoute ? h('button', { class: 'btn btn-secondary btn-sm', onclick: () => Router.navigate(`apps/${p.demoRoute}`) }, 'デモ') : null,
                                h('button', { class: 'btn btn-ghost btn-sm', onclick: () => Router.navigate(`projects/${p.slug}`) }, '詳細を見る')
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
                        countDisplay = h('p', { class: 'text-muted' }, '')
                    )
                ),
                h('div', { class: 'grid grid-cols-2 gap-4' },
                    h('div', { class: 'relative' },
                        h('div', {
                            class: 'absolute left-3 top-1/2 transform -translate-y-1/2 color-muted'
                        }, createIcon('search', 18)),
                        h('input', {
                            type: 'text',
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
                        value: cat,
                        'aria-label': 'カテゴリフィルター',
                        onchange: (e) => {
                            cat = e.target.value;
                            renderGrid();
                            syncURL();
                        }
                    },
                        ...categories.map(c => h('option', {
                            value: c,
                            text: c === 'All' ? '全カテゴリー' : c
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

    function ProjectDetailPage(slug) {
        const state = State.get();
        const project = state.projects.find(p => p.slug === slug);

        if (!project) {
            return h('div', { class: 'flex flex-col gap-4' },
                h('h1', { class: 'h1' }, 'プロジェクトが見つかりません'),
                h('button', {
                    class: 'btn btn-secondary',
                    onclick: () => Router.navigate('projects')
                }, '一覧へ戻る')
            );
        }

        const related = state.projects.filter(p =>
            project.relatedProjectIds?.includes(p.id) && p.id !== project.id
        );

        const autoRelated = Store.autoRelatedCandidates(project, state.projects, 8);
        return h('article', { class: 'flex flex-col gap-6' },
            // Header
            h('header', {},
                h('button', {
                    class: 'btn btn-ghost btn-sm mb-4',
                    onclick: () => Router.navigate('projects')
                }, '← 一覧に戻る'),
                h('div', { class: 'flex flex-wrap gap-2 mb-3' },
                    h('span', { class: 'badge badge-primary' }, project.category),
                    project.demoRoute ? h('span', { class: 'badge badge-success' }, 'デモあり') : null
                ),
                h('h1', { class: 'h1 mb-3' }, project.name),
                h('p', { class: 'text-muted mb-4' }, project.summary),
                h('div', { class: 'flex flex-wrap gap-2' },
                    ...(project.tags || []).map(tag =>
                        h('span', { class: 'badge badge-secondary' }, '#' + tag)
                    )
                )
            ),

            // Content Grid
            h('div', { class: 'grid-2col grid--align-start' },
                // Left Column
                h('div', { class: 'flex flex-col gap-4' },
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                createIcon('alert', 20),
                                '課題'
                            )),
                            h('p', { class: 'text-muted text-prewrap' }, project.problem)
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                createIcon('brain', 20),
                                'アプローチ'
                            )),
                            h('p', { class: 'text-muted text-prewrap' }, project.approach)
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                createIcon('apps', 20),
                                'アーキテクチャ'
                            )),
                            h('p', { class: 'text-muted font-mono text-small text-prewrap' },
                                project.architecture?.overview || '(未登録)'
                            )
                        )
                    )
                ),

                // Right Column
                h('div', { class: 'flex flex-col gap-4' },
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, '使用技術'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                ...(project.tech || []).map(t =>
                                    h('span', { class: 'badge badge-secondary' }, t)
                                )
                            )
                        )
                    ),
                    project.demoRoute ? h('section', {
                        class: 'card border-primary-faint'
                    },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-2' }, 'デモ'),
                            h('p', { class: 'text-small text-muted mb-3' }, 'このプロジェクトはポートフォリオ内で実際に動作します。'),
                            h('button', {
                                class: 'btn btn-primary',
                                onclick: () => Router.navigate(`apps/${project.demoRoute}`)
                            }, 'アプリを起動')
                        )
                    ) : null,
                    related.length > 0 ? h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h3', { class: 'h3 mb-3' }, '関連プロジェクト'),
                            h('ul', { class: 'list-readable' },
                                ...related.map(r =>
                                    h('li', { class: 'mb-2' },
                                        h('button', {
                                            class: 'btn btn-ghost btn-sm',
                                            onclick: () => Router.navigate(`projects/${r.slug}`)
                                        }, r.name)
                                    )
                                )
                            )
                        )
                    ) : null
                )
            ),

            // Metrics
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h3', { class: 'h3 mb-4' }, 'メトリクス'),
                    project.outcome?.metrics?.length ? h('div', { class: 'grid grid-cols-3' },
                        ...project.outcome.metrics.map(m =>
                            h('div', { class: 'text-center p-4' },
                                h('div', {
                                    class: 'h2 mb-1 color-primary'
                                }, m.value),
                                h('div', { class: 'text-small text-muted' }, m.label)
                            )
                        )
                    ) : h('p', { class: 'text-muted' }, 'メトリクスは未登録です。')
                )
            )

            ,
            autoRelated.length > 0 ? h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h3', { class: 'h3 mb-3' }, 'おすすめ（自動）'),
                    h('p', { class: 'text-muted mb-3' }, 'カテゴリ/タグ/技術/本文の近さから自動で近いプロジェクトを提案します。'),
                    h('ul', { class: 'list-clean' },
                        ...autoRelated.map(r =>
                            h('li', { class: 'mb-2' },
                                h('button', {
                                    class: 'btn btn-ghost btn-sm',
                                    onclick: () => Router.navigate(`projects/${r.slug}`)
                                },
                                    createIcon('sparkles', 16),
                                    h('span', { class: 'icon-gap' }, r.name)
                                )
                            )
                        )
                    )
                )
            ) : null);
    }

    function AppsPage() {
        const apps = [
            { id: 'task', title: 'タスク管理', desc: 'カンバン形式の簡易タスク管理', icon: 'checkSquare' },
            { id: 'todo', title: 'クイックTODO', desc: 'クイック入力 + 完了管理', icon: 'list' },
            { id: 'pomodoro', title: 'ポモドーロ', desc: '耐タブ休眠のタイマー + フォーカス対象', icon: 'clock' },
            { id: 'ai', title: 'AI アシスト', desc: 'ローカルAI（外部API不要）', icon: 'brain' },
            { id: 'notes', title: 'Markdown ノート', desc: 'innerHTML 不使用の安全 MD ライブプレビュー', icon: 'edit' },
        ];

        return h('div', { class: 'flex flex-col gap-6' },
            h('header', {},
                h('h1', { class: 'h1' }, 'アプリ'),
                h('p', { class: 'text-muted' }, 'ポートフォリオに内蔵された実用的なツール')
            ),
            h('div', { class: 'grid grid-cols-2' },
                ...apps.map(app =>
                    h('article', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('div', { class: 'flex items-center gap-3 mb-3' },
                                createIcon(app.icon, 24),
                                h('h2', { class: 'h3' }, app.title)
                            ),
                            h('p', { class: 'text-muted mb-4' }, app.desc),
                            h('button', {
                                class: 'btn btn-secondary',
                                onclick: () => Router.navigate(`apps/${app.id}`)
                            }, '開く')
                        )
                    )
                )
            )
        );
    }

    function AboutPage() {
        return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'data-ai-section': 'about' },
            h('header', {}, h('h1', { class: 'h1', 'data-ai-content': 'lead' }, 'About / Philosophy')),
            
            // コア定義
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h4 mb-4 color-primary' }, 'コア定義'),
                    h('p', { class: 'text-section-lead' },
                        '私は、AIをツールとして扱うPMではありません。', h('br', {}),
                        'AIを開発リソースとして統合し、設計・制約・検証・公開までを一貫して統制するPMです。'
                    ),
                    h('p', { class: 'text-muted' },
                        '人間をマネジメントすることがPMの前提であるように、AIをマネジメントすることもまた、これからのPMにおける前提条件だと考えています。'
                    )
                )
            ),

            // 実務能力の再定義（武器化）
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h4 mb-4 color-primary' }, '実務能力の再定義'),
                    h('p', { class: 'mb-4' }, '本ポートフォリオでは、その前提を実務として実証しています。'),
                    h('ul', { class: 'text-muted list-body' },
                        h('li', {}, '人間はコードを1行も書かず、AIをチームとして編成'),
                        h('li', {}, '複数AIの役割分担と出力統制を設計'),
                        h('li', {}, '制約条件を定義し、逸脱（例：フレームワーク化）を検知・差し戻し'),
                        h('li', {}, 'アプリケーションロジック外部ライブラリ非依存のSPAとして構築・公開'),
                        h('li', {}, 'v1→v74（73回の遷移）の反復改善を継続')
                    ),
                    h('p', { class: 'text-strong' },
                        '重要なのは「AIに作らせたこと」ではなく、AIの出力を制御し、意図を維持したままプロダクトを成立させたことです。'
                    )
                )
            ),

            // 価値の明確化（ビジネス接続）
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h4 mb-4 color-primary' }, '価値の明確化'),
                    h('p', { class: 'mb-4' }, 'AIは高速に実装できますが、同時に容易に破綻します。そのため、これからの開発において重要なのは実装力ではなく、以下の能力です。'),
                    h('ul', { class: 'text-muted list-body' },
                        h('li', {}, '何を作るかを定義する力'),
                        h('li', {}, '制約を設計する力'),
                        h('li', {}, '出力の妥当性を判断する力'),
                        h('li', {}, '崩壊を防ぐ構造を選ぶ力')
                    ),
                    h('p', {}, '私はその領域を担当するPMとして、AIを含めた開発全体を成立させる役割を担っています。')
                )
            ),

            // ポジショニング
            h('section', { class: 'card card--accent-left' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h4 mb-2' }, 'Positioning'),
                    h('p', { class: 'text-cta-emphasis' },
                        'AIを使うPMではなく、AIを制御し、プロダクトを成立させるPMです。'
                    )
                )
            ),

            ContactCTA('自己紹介を読んで、一緒に働くイメージが湧いた方へ。PM・アーキテクチャ設計・AI導入推進のご相談・採用のご連絡はこちらから。')
        );
    }

    function ResumePage() {
        return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'data-ai-section': 'resume' },
            h('header', {}, h('h1', { class: 'h1', 'data-ai-content': 'lead' }, 'Resume')),
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h3 mb-4', 'data-ai-content': 'lead' }, State.get().profile.title),
                    h('ul', { class: 'text-muted list-body-tight', 'data-ai-content': 'body' },
                        h('li', {}, 'ProjectsをCase Study形式で整理'),
                        h('li', {}, '内蔵Apps（Task/Todo/Pomodoro/AI）を作品として掲載'),
                        h('li', {}, '整合性チェック/自動修復＋スナップショットで運用事故率を低減'),
                        h('li', {}, 'セマンティックHTML5 + ARIA対応'),
                        h('li', {}, '単一HTMLで完結（依存性最小化）')
                    )
                )
            ),
            ContactCTA('スキルセット・開発スタイルを確認いただいた方へ。AI駆動開発・PM設計・システムアーキテクチャ設計の相談、採用のご連絡はこちらから。')
        );
    }

    function ContactPage() {
        const profile = State.get().profile;
        return h('article', { class: 'flex flex-col gap-6 max-w-2xl', 'aria-label': 'Contact — yuta AI-Driven PM' },
            h('header', {}, h('h1', { class: 'h1' }, 'Contact')),
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('div', { class: 'flex flex-col gap-4' },
                        h('div', { class: 'flex justify-between py-2 border-bottom border-bottom-themed' },
                            h('span', { class: 'text-muted' }, 'Email'),
                            h('a', { href: `mailto:${profile.email}`, class: 'font-mono' }, profile.email)
                        ),
                        profile.github ? h('div', { class: 'flex justify-between py-2 border-bottom border-bottom-themed' },
                            h('span', { class: 'text-muted' }, 'GitHub'),
                            h('a', { href: profile.github, target: '_blank', rel: 'noopener noreferrer' }, profile.github)
                        ) : null,
                        profile.linkedin ? h('div', { class: 'flex justify-between py-2' },
                            h('span', { class: 'text-muted' }, 'LinkedIn'),
                            h('a', { href: profile.linkedin, target: '_blank', rel: 'noopener' }, profile.linkedin)
                        ) : null,
                        h('button', {
                            class: 'btn btn-primary mt-4',
                            onclick: () => location.href = `mailto:${profile.email}`
                        }, h('span', {}, createIcon('mail', 18), ' メールを作成'))
                    )
                )
            )
        );
    }

    function FatalPage(error) {
        const msg = (error && error.message) ? error.message : String(error || 'Unknown error');
        const stack = (error && error.stack) ? String(error.stack) : '';

        function clearAllData() {
            if (!confirm('LocalStorageのデータを削除して再読み込みしますか？')) {return;}
            try {
                localStorage.removeItem(CONSTANTS.STORAGE_KEY);
                localStorage.removeItem(CONSTANTS.SNAPSHOT_KEY);
            } catch { }
            location.reload();
        }

        return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
            h('h1', { class: 'h1' }, '致命的エラーが発生しました'),
            h('p', { id: 'fallback-details', class: 'text-muted' }, '表示を継続できない例外が発生しました。下の情報を確認し、必要ならデータを初期化してください。'),
            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('div', { class: 'h3 mb-2' }, 'エラー'),
                    h('pre', { class: 'text-prewrap-break' }, msg),
                    stack ? h('details', { class: 'mt-3' },
                        h('summary', { class: 'cursor-pointer text-sm' }, 'スタックトレース'),
                        h('pre', { class: 'text-sm pre-wrap' }, stack)
                    ) : null
                )
            ),
            h('div', { class: 'flex flex-wrap gap-2' },
                h('button', { class: 'btn btn-secondary', onclick: () => { window.__fatalError = null; Router.navigate(''); } }, 'ホームへ'),
                h('button', { class: 'btn btn-danger', onclick: clearAllData }, 'データを削除して再起動')
            )
        );
    }

    function AIKnowhowPage() {
        const C = {
            primary: 'var(--color-primary)',
            success: 'var(--color-success)',
            warning: 'var(--color-warning)',
            info: 'var(--color-info)',
            purple: '#7c3aed'
        };

        function sectionHeader(icon, title, color) {
            return h('div', {
                class: 'row-gap-4-items-start'
            },
                h('div', {
                    class: 'badge-layer--lg', style: { background: color }
                }, icon),
                h('span', { class: 'text-head-lg' }, title)
            );
        }

        function agentRow(name, role, free, note) {
            return h('div', {
                class: 'block-bg-tertiary-pad14'
            },
                h('div', { class: 'role-desc-row' }, name),
                h('div', { class: 'text-detail' }, note),
                h('span', {
                    class: 'free-paid-badge', style: { background: free ? 'rgba(22,163,74,0.12)' : 'rgba(217,119,6,0.12)', color: free ? 'var(--color-success)' : 'var(--color-warning)' }
                }, free ? '無課金' : '有料（最安）')
            );
        }

        function kernelRow(key, label, detail) {
            return h('div', {
                class: 'row-gap-8-border'
            },
                h('div', {
                    class: 'step-num-badge'
                }, key),
                h('div', { class: 'flex flex-col gap-row-sm' },
                    h('div', { class: 'text-label' }, label),
                    h('div', { class: 'text-detail-muted-relaxed' }, detail)
                )
            );
        }

        function phaseCard(num, title, tickets, agents, summary, color) {
            return h('div', {
                class: 'block-phase-card', style: { borderLeft: '3px solid ' + color, padding: '12px 14px', background: 'var(--bg-tertiary)' }
            },
                h('div', { class: 'row-gap-8-nm' },
                    h('div', {
                        class: 'badge-phase', style: { background: color }
                    }, 'Phase ' + num),
                    h('span', { class: 'role-desc-row' }, title),
                    h('span', { class: 'text-label-xs-push' }, tickets)
                ),
                h('div', { class: 'text-detail' }, summary),
                h('div', {
                    class: 'gap-wrap-mt4'
                },
                    ...agents.map(a => h('span', {
                        class: 'badge-agent'
                    }, a))
                )
            );
        }

        return h('article', { class: 'flex flex-col gap-6 max-w-3xl page-knowhow' },

            // ══ ヘッダー ══
            h('header', { class: 'flex flex-col gap-2', 'data-ai-section': 'ai-knowhow' },
                h('h1', { class: 'h1 row-gap-12', 'data-ai-content': 'lead' },
                    createIcon('lightbulb', 28), 'AI開発ノウハウ'
                ),
                h('p', { class: 'text-muted', 'data-ai-content': 'lead' },
                    '6種のAIエージェントを役割分担させ、55枚のチケット（プロンプト）のみでv54 SPAを構築した再現可能な手法のエッセンスです。'
                ),
                h('div', { class: 'flex flex-wrap gap-2 row-mt-4' },
                    h('span', { class: 'badge badge-secondary' }, '🤖 6エージェント構成'),
                    h('span', { class: 'badge badge-secondary' }, '🎫 55チケット'),
                    h('span', { class: 'badge badge-secondary' }, '💰 課金2名のみ'),
                    h('span', { class: 'badge badge-secondary' }, '🔑 KERNELフレームワーク')
                )
            ),

            // ══ 費用感 ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'warning', role: 'region', 'aria-label': 'AI開発の費用感'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('💰', '費用感 — 課金は2名だけ', C.warning),
                    h('p', { class: 'text-body-sm' },
                        'GeminiとChatGPTのみ最も安いプランで課金。残り4名（Kimi・Claude・Manus・Perplexity）は完全無料で運用可能。ツールごとの無料枠を最大活用することでコストを最小化している。'
                    ),
                    h('div', { class: 'flex flex-wrap gap-2' },
                        h('span', {
                            class: 'badge-tool-tier--paid'
                        }, '💳 有料（最安）: Gemini / ChatGPT'),
                        h('span', {
                            class: 'badge-tool-tier--free'
                        }, '✅ 完全無料: Kimi / Claude / Manus / Perplexity')
                    )
                )
            ),

            // ══ 6エージェント役割 ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '6つのAIエージェントの役割分担'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('🤖', '6エージェントの役割分担', C.primary),
                    agentRow('Gemini', false, false,
                        '初期ドラフト（要件定義・ワイヤーフレーム）、BGM（Lyria 3）・画像生成、最終コードレビュー。マルチモーダル能力を活かしてプロジェクトの起点と終点を担う。'
                    ),
                    agentRow('Kimi K2.5', 'init', true,
                        '基盤構築（0-to-1）。Thinkingモード有効で、h()関数・ハッシュルーター・CSS変数フレームワークをゼロから設計。「ゴールを提示してあとは任せる」スタイルが効果的。'
                    ),
                    agentRow('Claude', 'design', true,
                        '中盤〜後半の複雑ロジック設計。状態管理・フォーカス保持・SEOメタデータの動的生成を担当。「設計図を描く」役割に集中させ、実コード変更はManusとChatGPTに委譲する。'
                    ),
                    agentRow('Manus', 'exec', true,
                        '中盤〜後半の厳密実装。「余計なことを一切しない」堅実さが武器。1.6 Maxモードで起動し、CSS/UIの変更のみを精緻に実行。ロジックへの接触を明示的に禁じる。'
                    ),
                    agentRow('Perplexity', 'review', true,
                        'コードレビュー・セキュリティ監査専任。Deep Researchモードで「良い点・悪い点・全指摘事項」を網羅的に抽出。XSSやCSPの脆弱性を主要マイルストーン毎に監査。'
                    ),
                    agentRow('ChatGPT', 'diff', false,
                        'Diff（差分）生成・統合。Perplexityの指摘とClaudeの設計書を受け取り、行番号に依存しない「関数ブロック単位の置換コード」のみを出力。コード統合時のヒューマンエラーを排除。'
                    )
                )
            ),

            // ══ 現在の運用モデル（対話型 → AI 自走への進化）══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': '現在の運用モデル：AI自走運用への進化'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('🔄', '現在の運用モデル — 対話型から AI 自走運用への進化', C.primary),
                    h('p', { class: 'text-detail-muted mb-1' },
                        '上記6エージェントの編成は v1→v74 の「構築期」の役割分担（対話型で起用）。現在の運用は、その一面である Claude Code による自律自走へ進化している。'
                    ),
                    h('p', { class: 'text-body-sm' },
                        'そして——このページを含む本サイトの改善は、今この瞬間も、そしてこれまでもずっと、AI の自走によって行われている。「AI 自走の PM ポートフォリオ」が、文字通り AI 自走で作られ続けているということ自体が、最も確かな実証である。制御も自走も、いずれも完全な事実である。'
                    ),
                    h('p', { class: 'text-body-sm' },
                        'AI（Claude Code）が実装・検証・マージ・本番デプロイまで自走し、さらに「次に何をやるか」の案出し（提案）も AI が行う。オーナー（UI 表記 yuta）は、ゴール／優先度の提示・承認・委任、そして必要時の決定的な是正という形で適度に制御・指示している——丸投げの放置ではなく、要所を押さえた統治である。'
                    ),
                    h('p', { class: 'text-body-sm' },
                        '実態は「案出し → 人間が裁可・委任 → AI が自律実行（ゲート間はほぼ放置）→ 逸脱時に人間が決定的に是正」という、疎だが決定的な統治ループ。無監督の全自動でもマイクロマネジメントでもない。例えば本運用中、AI が「依頼完了後に見解を述べる」約束を破った際、人間が即座に指摘し是正させた——統治が演出ではなく稼働している証拠である。'
                    ),
                    h('p', { class: 'text-detail-muted' },
                        'この AI 自走運用そのものが、現時点では高価値かつ希少と認識している。具体の運用記録は公開リポジトリの AI2AI.md（Session Record）および docs/incident-artifacts/improvement-notes で検証できる。'
                    )
                )
            ),

            // ══ KERNELフレームワーク ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'purple'
            },
                h('div', { class: 'card-body flex flex-col gap-2' },
                    sectionHeader('🔑', 'KERNELフレームワーク — チケット設計の原則', C.purple),
                    h('p', { class: 'text-detail-muted mb-2' },
                        '全チケットはこの6原則で構造化。曖昧さを排除しハルシネーションを防ぐ。'
                    ),
                    kernelRow('K', 'Keep it simple — 1チケット1目標',
                        '複雑な背景説明を省き、実行すべきタスクのみを簡潔に記述する。トークン消費とAIの幻覚を最小化。'
                    ),
                    kernelRow('E', 'Easy to verify — 成否判定基準を明記',
                        '「コンソールエラー0件」「XSS脆弱性なし」など、検証可能な完了条件を明示する。'
                    ),
                    kernelRow('R', 'Reproducible — 時間・文脈依存の表現を禁止',
                        '「最新のトレンド」より「Vanilla JSのみ使用」と厳密に指定。誰がいつ実行しても同結果になる。'
                    ),
                    kernelRow('N', 'Narrow scope — スコープを極限まで絞る',
                        'コード生成・ドキュメント作成・テスト記述を1チケットに詰め込まない。成功率が大幅向上。'
                    ),
                    kernelRow('E', 'Explicit constraints — NOT To-Doを明示',
                        '「外部ライブラリ禁止」「既存CSS変数の削除禁止」など、やってはいけないことを列挙する。リグレッションを90%以上削減。'
                    ),
                    kernelRow('L', 'Logical structure — 固定フォーマットで記述',
                        'Context（入力情報）/ Task（タスク定義）/ Constraints（制約）/ Format（出力形式）の4構造に統一する。'
                    )
                )
            ),

            // ══ 標準チケットテンプレート ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'info'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('📋', '標準チケット・テンプレート', C.info),
                    ...[
                        ['役割の定義', 'あなたは[エージェントの専門性]として、Vanilla JSで構築されたSPAに対する精密な改修を実行します。'],
                        ['タスクの明確化', '[実行すべき具体的なアクションを記述]'],
                        ['コンテキストの提供', '単一HTMLファイル構成。innerHTML禁止。要素生成は必ずh()使用。状態は再レンダリングを越えて保持。'],
                        ['現在の状態', '<current_code>[関連するコードブロック]</current_code>'],
                        ['厳格な制約', '[NOT To-Doを箇条書き]'],
                        ['出力フォーマット', 'ファイル全体ではなく、更新された関数ブロックのみを出力。余計な解説不要。']
                    ].map(([label, val]) =>
                        h('div', {
                            class: 'grid-info-row'
                        },
                            h('div', { class: 'text-info-label' }, '[' + label + ']'),
                            h('div', { class: 'text-secondary-xs' }, val)
                        )
                    )
                )
            ),

            // ══ 5フェーズ概要 ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'success'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('🚀', '55チケットの5フェーズ構成', C.success),
                    h('p', { class: 'text-detail-muted mb-1' },
                        '人間はコードを1行も書かず、チケットを発行し返ってきた差分をローカルファイルに統合するだけ。'
                    ),
                    phaseCard(1, '概念定義と初期スキャフォールディング', 'Ticket 1〜12',
                        ['Gemini', 'Kimi'],
                        'Geminiで要件定義とワイヤーフレームを作成。KimiのThinkingモードでh()関数・カスタムルーター・CSS変数フレームワーク・FOUC防止IIFEをゼロ構築。',
                        C.primary
                    ),
                    phaseCard(2, 'コアロジックと状態永続化', 'Ticket 13〜28',
                        ['Claude', 'Manus'],
                        'Claudeでreplace Silentlyルーター・フォーカス保持（setTimeout hack）・visibilitychangeによる状態保存を設計。ManusでプロジェクトグリッドのCSS Gridレイアウトを厳密実装。',
                        C.purple
                    ),
                    phaseCard(3, 'コンポーネント統合とUI洗練', 'Ticket 29〜40',
                        ['Manus', 'Perplexity'],
                        'ManusでTask/Todo/AIインターフェース・クイズUI・タイマーUIを構築。Perplexityで機能統合後のXSS・CSP・OGタグ・JSON-LDを全面監査。',
                        C.info
                    ),
                    phaseCard(4, '外科的パッチ適用', 'Ticket 41〜49',
                        ['ChatGPT', 'Claude'],
                        'ChatGPTをDiffモードで起動し、Perplexity指摘に基づくCSPヘッダー強化・innerHTML排除・Mapベースデータ構造最適化を行番号不依存の置換ブロックで適用。',
                        C.warning
                    ),
                    phaseCard(5, 'アセット合成と最終確認', 'Ticket 50〜55',
                        ['Gemini', 'Perplexity'],
                        'GeminiでCity Pop/Lo-fi BGMと「AI-Driven PM」コンセプト画像を生成し統合。JSON-LDのDOM整合性をGeminiで検証、Perplexityで最終デグレ確認しv54完成。',
                        C.success
                    )
                )
            ),

            // ══ ハンドオーバープロトコル ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'warning'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    sectionHeader('🔗', 'エージェント引き継ぎ（ハンドオーバー）プロトコル', C.warning),
                    h('p', { class: 'text-body-sm' },
                        '異なるAI間でコンテキストが消失しないよう、各チケットの末尾に以下の定型出力を要求する。'
                    ),
                    h('div', {
                        class: 'block-blockquote-mono'
                    },
                        '「作業完了後、コード全体像・主要アーキテクチャ決定理由・未解決課題・次エージェントへの具体的指示を網羅したhandover-brief.md形式のテキストを出力してください。」'
                    ),
                    h('p', { class: 'text-detail-muted' },
                        '人間はこのハンドオーバー文書と最新ソースコードをセットにして次エージェントへの入力コンテキストとして渡す。共有メモリ不要で一貫したタスク継続性を担保できる。'
                    )
                )
            ),

            // ══ 上級テクニック ══
            h('section', {
                class: 'card card--accent-left', 'data-accent': 'info'
            },
                h('div', { class: 'card-body flex flex-col gap-4' },
                    sectionHeader('⚡', '上級プロンプトエンジニアリングのコツ', C.info),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-3' },
                        ...[
                            ['コンテキスト段階的開示', '3000行のファイル全体を渡さず、変更対象のブロックのみを抽出して渡す。「ファイル全体を書き直さず更新ブロックのみ出力」と明示。'],
                            ['Thinkingモードの強制発動', '「コードを書く前にDOMトポロジーを分析せよ」と前置き。KimiにはAgent Swarmモードを明示的に指定して並列推論させる。'],
                            ['Fan-Out比較パターン', '難解なバグはKimiとClaudeに同時投入して解を比較。最適解をChatGPTでDiff化する。単一AIへの依存を排除。'],
                            ['XMLタグ構造化（Claude専用）', '<instructions><context><example>でプロンプトを構造化。AIがユーザーデータとコマンドを混同することを防ぐ。']
                        ].map(([title, desc]) =>
                            h('div', {
                                class: 'block-section-item'
                            },
                                h('div', { class: 'text-label' }, title),
                                h('div', { class: 'text-detail-muted-relaxed' }, desc)
                            )
                        )
                    )
                )
            ),

            ContactCTA('AI開発ワークフローを読んで、自社への導入や共同プロジェクトに興味を持った方へ。プロンプト設計・マルチエージェント構成・AI開発プロセス設計のご相談を受け付けています。')
        );
    }

    function ContactCTA(desc) {
        const profile = State.get().profile;
        const X_URL         = 'https://x.com/yuta_mezasi';

        function outLink(url, icon, label, colorVar) {
            return h('a', {
                href: url,
                target: '_blank',
                rel: 'noopener noreferrer',
                class: 'cta-pill',
                style: {
                    textDecoration: 'none',
                    border: '1.5px solid ' + colorVar,
                    color: colorVar,
                    background: 'transparent',
                    transition: 'var(--transition)',
                    whiteSpace: 'nowrap'
                }
            }, createIcon(icon, 16), label);
        }

        function mailBtn() {
            return h('button', {
                class: 'cta-pill',
                style: {
                    border: '1.5px solid var(--color-primary)',
                    color: 'var(--color-primary)',
                    background: 'transparent',
                    cursor: 'pointer',
                    whiteSpace: 'nowrap'
                },
                onclick: () => {
                    const subject = encodeURIComponent('ポートフォリオを見てご連絡しました');
                    const body = encodeURIComponent('はじめまして。\nポートフォリオを拝見し、ご相談があってご連絡しました。\n\n【ご相談内容】\n');
                    location.href = 'mailto:' + profile.email + '?subject=' + subject + '&body=' + body;
                }
            }, createIcon('mail', 16), 'メールで相談する');
        }

        return h('section', {
            class: 'card card--contact'
        },
            h('div', { class: 'card-body flex flex-col gap-4' },
                // Header
                h('div', { class: 'gap-row-10' },
                    h('div', {
                        class: 'contact-section-badge'
                    }, 'CONTACT'),
                    h('span', { class: 'text-subhead-lg' }, '気になった方へ')
                ),

                // What can be asked
                h('p', { class: 'text-body-relaxed' }, desc),

                // Divider label row
                h('div', { class: 'gap-col-md' },
                    // Row 1: 技術記事
                    h('div', { class: 'gap-col-sm' },
                        h('div', { class: 'badge-contact-label' }, '📖  技術記事（AIO実践シリーズ＋発展記事・計11本）'),
                        h('div', { class: 'gap-wrap-sm' },
                            outLink('https://zenn.dev/yuta_yokoi', 'externalLink', 'Zennで全11本の記事を読む →', 'var(--color-info)')
                        )
                    ),
                    // Row 2: 相談・依頼
                    h('div', { class: 'gap-col-sm' },
                        h('div', { class: 'badge-contact-label' }, '✉  PM・アーキテクチャ設計の相談・依頼'),
                        h('div', { class: 'gap-wrap-sm' },
                            outLink(X_URL, 'messageCircle', 'X (Twitter) でDMを送る', 'var(--color-primary)'),
                            mailBtn()
                        )
                    )
                )
            )
        );
    }

    return { Sidebar, HomePage, ProjectsPage, ProjectDetailPage, AppsPage,
             AboutPage, ResumePage, ContactPage, FatalPage, AIKnowhowPage, ContactCTA };
}
