/**
 * js/home-page.js — HomePage レンダラ (v80+ 肥大化解消: js/components.js から抽出)
 *
 * js/components.js から 2 番目に大きいページ HomePage (~296 行) を factory pattern で
 * 葉モジュールへ分離した。挙動 byte-equivalent (関数本体を無改変で移設)。
 *
 * 【依存 (引数注入)】
 *   - h          : DOM ビルダー (js/ui-components.js)
 *   - Router     : ルーター ({ navigate } 等) — hero CTA の遷移
 *   - State      : アプリ状態 ({ get() }) — プロフィール等の描画
 *   - ContactCTA : 末尾 CTA (js/components.js の共有 helper。main.js が生成後に注入)
 *
 * 【葉契約】ローカル ESM import ゼロ (Check 47c)。全依存を引数注入。
 * 【非破壊性】main.js が createComponents 実行後に ContactCTA を取り出し
 *   createHomePage({ h, Router, State, ContactCTA }) で HomePage を生成し
 *   render dispatch (route 'home') へ従来配線。挙動不変を behavior e2e が保証。
 */
export function createHomePage({ h, Router, State, ContactCTA }) {
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

    return HomePage;
}
