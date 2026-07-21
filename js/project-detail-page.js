/**
 * js/project-detail-page.js — ProjectDetailPage レンダラ (v80+ 肥大化解消: components.js から抽出)
 *
 * js/components.js からプロジェクト詳細ページ ProjectDetailPage(slug) (~154 行) を
 * factory pattern で葉モジュールへ分離。挙動 byte-equivalent (関数本体を無改変で移設)。
 *
 * 【依存 (引数注入)】
 *   - h, createIcon : DOM ビルダー / SVG アイコン (js/ui-components.js)
 *   - Router        : ルーター ({ navigate } 等)
 *   - State         : アプリ状態 ({ get() }) — プロジェクト lookup (slug→project)
 *   - Store         : createStore instance — autoRelatedCandidates(関連プロジェクト推薦)
 *
 * 【葉契約】ローカル ESM import ゼロ (Check 47c)。全依存を引数注入。
 * 【非破壊性】main.js が createProjectDetailPage({ h, createIcon, Router, State, Store })
 *   で ProjectDetailPage(slug) を生成し render dispatch (route 'project-detail') へ従来配線。
 *   slug 衝突時の一意 slug 解決 (#154) は Store 側 normalize 済ゆえ本ページは find で解決。
 *   behavior e2e (project-detail route) が挙動不変を保証。
 */
export function createProjectDetailPage({ h, createIcon, Router, State, Store }) {
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
                            // [FIX] 各セクション見出しは <h2> (ページ h1=project.name 直下の唯一の
                            //   サブ階層)。従来 <h3> で h1→h3 の見出しレベルスキップ (WCAG 1.3.1 /
                            //   axe heading-order) だった。要素は h2、CSS class は 'h3' 維持ゆえ視覚
                            //   サイズ不変 (render-neutral)。#/projects/:slug は A11Y_ROUTES 未被覆で
                            //   本違反が axe を逃れていたため a11y-axe.spec.js に detail route を追加。
                            h('h2', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                createIcon('alert', 20),
                                '課題'
                            )),
                            h('p', { class: 'text-muted text-prewrap' }, project.problem)
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h2', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
                                createIcon('brain', 20),
                                'アプローチ'
                            )),
                            h('p', { class: 'text-muted text-prewrap' }, project.approach)
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h2', { class: 'h3 mb-3' }, h('div', { class: 'flex items-center gap-2' },
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
                            h('h2', { class: 'h3 mb-3' }, '使用技術'),
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
                            h('h2', { class: 'h3 mb-2' }, 'デモ'),
                            h('p', { class: 'text-small text-muted mb-3' }, 'このプロジェクトはポートフォリオ内で実際に動作します。'),
                            h('button', {
                                class: 'btn btn-primary',
                                onclick: () => Router.navigate(`apps/${project.demoRoute}`)
                            }, 'アプリを起動')
                        )
                    ) : null,
                    related.length > 0 ? h('section', { class: 'card' },
                        h('div', { class: 'card-body' },
                            h('h2', { class: 'h3 mb-3' }, '関連プロジェクト'),
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
                    h('h2', { class: 'h3 mb-4' }, 'メトリクス'),
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
                    h('h2', { class: 'h3 mb-3' }, 'おすすめ（自動）'),
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

    return ProjectDetailPage;
}
