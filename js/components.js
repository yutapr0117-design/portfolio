/**
 * js/components.js — UI page components
 * (Sidebar / AppsPage / AboutPage / ResumePage / ContactPage / FatalPage / ContactCTA)
 * — v80+ Stage 5-m extraction via factory pattern
 *
 * 元は main.js の UI page render 関数群を factory pattern で物理分割した葉モジュール。
 * その後の肥大化解消 (1,000 行しきい値・2026-07) で、当初含んでいた HomePage /
 * ProjectsPage / ProjectDetailPage / AIKnowhowPage を個別葉モジュール (js/home-page.js /
 * js/projects-page.js / js/project-detail-page.js / js/ai-knowhow-page.js) へさらに分離した。
 * 現在の公開 API は下記 7 関数 (return 文と一致)。
 * Brand / Store / State / Theme / Meta Management と同じく、すべての closure 依存を
 * `createComponents` 関数の引数で受け取ることで、葉契約 (Check 47c: import ゼロ) を
 * 維持しつつ各関数の挙動と公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const Components = createComponents({...});
 *   const { Sidebar, AppsPage, AboutPage,
 *           ResumePage, ContactPage, FatalPage, ContactCTA } = Components;
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
 *   - CONSTANTS: js/constants.js
 *   - clear: main.js IIFE の純粋関数 (DOM の子要素を全削除)
 *   - closeDrawer: js/mobile-drawer.js (ナビリンク選択時にドロワーを閉じる)
 *
 * 【非破壊性】
 *   - 上記 7 関数の DOM 出力・class 名・style・aria 属性は byte-equivalent
 *   - イベントハンドラの動作・State.update への副作用も不変
 *   - Sidebar の nav 項目・active 判定は挙動不変
 *   - (HomePage / ProjectsPage / ProjectDetailPage / AIKnowhowPage は個別葉モジュールへ分離済。
 *      検索フィルタ・並び替え・関連プロジェクト類似度・article schema route 表示は各分離先で不変)
 *   - AIDK Kernel / AIO 正本層には影響しない
 */
export function createComponents({ h, createIcon, Toast, BGM, AUTHOR, Router, State, Theme, Brand, Store, CONSTANTS, clear, closeDrawer }) {
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
            { icon: 'edit',        label: 'Markdown ノート', path: 'apps/notes',       active: route.name === 'app-notes' },
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
                h('button', { class: 'btn btn-secondary', onclick: () => {
                    // __fatalError を解除してホームへ。home(#/) で fatal が起きた場合 Router.navigate('')
                    // は同一 hash ゆえ hashchange が発火せず再描画されない (FatalPage から復旧できない
                    // バグだった) ため、明示的に window.render() も呼んで確実に再描画する。
                    window.__fatalError = null;
                    Router.navigate('');
                    if (typeof window.render === 'function') { window.render(); }
                } }, 'ホームへ'),
                h('button', { class: 'btn btn-danger', onclick: clearAllData }, 'データを削除して再起動')
            )
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

    return { Sidebar, AppsPage,
             AboutPage, ResumePage, ContactPage, FatalPage, ContactCTA };
}
