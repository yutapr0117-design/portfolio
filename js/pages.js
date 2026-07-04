/**
 * js/pages.js — Page render components (RoleSplitPage / NotFoundPage)
 * (v80+ Stage 5-b extraction via factory pattern — fixed in Stage 5-j to inject h/createIcon/Router)
 * (v80+ bloat-reduction 2026-07-04 — HiringRiskPage + 専用 helper を js/hiring-risk-page.js へ分離)
 *
 * 【factory pattern への refactor (Stage 5-j fix)】
 * 元の Stage 5-b 抽出では `h, createIcon, Router` を未定義のグローバル参照として書いていたが、
 * これは ESM module スコープでは未定義になり、関数を実行すると ReferenceError になる
 * 隠れバグだった（Playwright が /#/projects と /#/about のみ訪問してこれらのページを
 * レンダリングしていなかったため CI 緑のまま潜在）。本 fix で factory pattern (Brand /
 * Store / State / Theme と同パターン) に切り替えて、依存を引数注入で解消する。
 *
 * 【公開 API（呼び出し側 main.js から見た形）】
 *   const { RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router, ContactCTA });
 *   (HiringRiskPage は js/hiring-risk-page.js の createHiringRiskPage で別途生成)
 *
 * 【依存（引数で注入）】
 *   - h: DOM builder (js/ui-components.js)
 *   - createIcon: SVG アイコン生成 (js/ui-components.js)
 *   - Router: hash router (js/router.js)
 *   - ContactCTA: 問い合わせ CTA セクション生成関数 (RoleSplitPage 末尾で使用)
 *
 * 【非破壊性】
 *   - 各ページ関数（RoleSplitPage / NotFoundPage）の DOM 出力は byte-equivalent
 *   - factory closure 内に閉じることで葉契約（Check 47c: import ゼロ）を維持
 */
export function createPages({ h, createIcon, Router, ContactCTA }) {

    // ▼ HiringRiskPage (採用リスク低減 / v28 採用決裁資料レベル) + 専用 helper
    //   (impactRow / kpiRow / decisionFlow / riskCard) は肥大化解消のため
    //   js/hiring-risk-page.js (createHiringRiskPage factory) へ分離した (2026-07-04)。
    //   main.js が createHiringRiskPage で生成し、createPages は RoleSplitPage /
    //   NotFoundPage のみを供給する。挙動は byte-equivalent。

            function NotFoundPage() {
        return h('article', { class: 'flex flex-col gap-6 max-w-2xl' },
            h('header', {}, h('h1', { class: 'h1' }, 'Not Found')),
            h('p', { class: 'text-muted' }, '指定されたページは見つかりません。'),
            h('div', { class: 'flex gap-3' },
                h('button', { class: 'btn btn-secondary', onclick: () => Router.navigate('') }, 'ホームへ'),
                h('button', { class: 'btn btn-ghost', onclick: () => Router.navigate('projects') }, 'プロジェクト一覧へ')
            )
        );
    }

    // ===== Page: RoleSplitPage — Human vs AI 分担表 =====
    function RoleSplitPage() {
        const C = {
            primary: 'var(--color-primary)',
            success: 'var(--color-success)',
            warning: 'var(--color-warning)',
            info: 'var(--color-info)',
            purple: '#7c3aed',
            human: '#2563eb',
            ai: '#7c3aed'
        };

        // ヘッダーバッジ
        function badge(label, color) {
            return h('span', {
                class: 'badge-contact-section', style: { background: color,
                    color: '#fff',
                    textTransform: 'uppercase'
                }
            }, label);
        }

        // 分担行 (Human列 / AI列)
        function splitRow(category, humanItems, aiItems) {
            return h('div', {
                class: 'table-data-row'
            },
                // カテゴリラベル
                h('div', {
                    class: 'cell-category'
                }, category),
                // Human列
                h('div', {
                    class: 'cell-human'
                },
                    ...humanItems.map(item =>
                        h('div', {
                            class: 'cell-bullet-row'
                        },
                            h('span', { class: 'text-bullet-human', style: { color: C.human } }, '✦'),
                            h('span', {}, item)
                        )
                    )
                ),
                // AI列
                h('div', {
                    class: 'cell-ai'
                },
                    ...aiItems.map(item =>
                        h('div', {
                            class: 'cell-bullet-row'
                        },
                            h('span', { class: 'text-bullet-ai', style: { color: C.ai } }, '✦'),
                            h('span', {}, item)
                        )
                    )
                )
            );
        }

        // テーブルヘッダー行
        function tableHeader() {
            return h('div', {
                class: 'table-header-row'
            },
                h('div', {
                    class: 'cell-header-label'
                }, 'カテゴリ'),
                h('div', {
                    class: 'cell-header-col'
                },
                    h('div', {
                        class: 'dot-color-indicator', style: { background: C.human }
                    }),
                    h('span', { class: 'role-label' }, '人間（Human）の役割')
                ),
                h('div', {
                    class: 'cell-header-col-last'
                },
                    h('div', {
                        class: 'dot-color-indicator', style: { background: C.ai }
                    }),
                    h('span', { class: 'role-label' }, 'AI の役割')
                )
            );
        }

        // 原則カード
        function principleCard(icon, title, desc, color) {
            return h('div', {
                class: 'block-section-item', style: { borderLeft: '3px solid ' + color }
            },
                h('div', { class: 'role-desc-row' }, icon + ' ' + title),
                h('div', { class: 'text-muted text-xs-relaxed' }, desc)
            );
        }

        return h('div', { class: 'flex flex-col gap-6' },

            // ── Hero ──
            h('section', { class: 'card card--accent-top', 'data-accent': 'primary', role: 'region', 'aria-label': '役割分担の概要' },
                h('div', { class: 'card-body' },
                    h('div', { class: 'row-gap-10-mb8' },
                        badge('Human', C.human),
                        h('span', { class: 'vs-label' }, 'vs'),
                        badge('AI', C.ai)
                    ),
                    h('h1', { class: 'h2 mb-10px' }, '役割分担表'),
                    h('p', { class: 'text-muted text-muted-intro' },
                        'このサイトは「人間がコードを書かない」AI駆動開発の実験です。人間の貢献は設計・判断・オーケストレーションであり、AIは実装・生成・補助を担います。' +
                        '以下の表で、各工程における責任の所在を明示します。'
                    )
                )
            ),

            // ── 分担表 ──
            h('section', { class: 'card card--overflow-hidden', role: 'region', 'aria-label': 'Human vs AI 詳細分担表', id: 'role-split-table', itemprop: 'hasPart' },
                h('div', { class: 'card-body card-body--no-pad' },
                    tableHeader(),
                    splitRow('設計',
                        ['システムアーキテクチャの決定', 'SPA構成・ルーティング設計', 'コンポーネント責務の定義', '設計上のトレードオフ判断'],
                        ['構造の提案・代替案の列挙', 'コード骨格の自動生成', '既存パターンの適用提案']
                    ),
                    splitRow('プロンプト設計',
                        ['意図・制約・ゴールの言語化', 'AIへの役割割当と指示', 'コンテキスト注入設計', 'Few-shot例の設計'],
                        ['プロンプトへの応答生成', '要求を解釈し実装に変換', '不足情報の補完・推定']
                    ),
                    splitRow('実装',
                        ['実装方針・境界条件の指示', '生成コードの受け入れ判断', 'リファクタリング方向の決定'],
                        ['HTML / CSS / JS のコード生成', 'スタイル・ロジックの実装', '関数・コンポーネントの具体化']
                    ),
                    splitRow('検証・QA',
                        ['動作確認・意図との整合チェック', 'バグの本質原因の特定', '修正方針の最終判断'],
                        ['補助的なレビュー・問題指摘', 'テストケース案の生成', 'エラーメッセージの解説']
                    ),
                    splitRow('コンテンツ生成',
                        ['掲載方針・文体・トーンの決定', '生成物の選択・編集・採否判断'],
                        ['テキスト原稿のドラフト生成', '画像・BGMなどのクリエイティブ生成', '多案の同時生成による選択肢提供']
                    ),
                    splitRow('SEO / AIO',
                        ['メタ設計方針・構造化データ戦略', 'llms.txt・llms-full.txt の設計方針', 'canonical・og 整合の最終確認'],
                        ['JSON-LD・OGタグのコード生成', 'キーワード案・description草案', 'AI-readable コンテキスト文書の草案']
                    ),
                    splitRow('バージョン管理',
                        ['リリース判断・バージョン番号付与', '変更内容の記録・公開可否判断', 'ブレイキングチェンジの意思決定'],
                        ['変更差分の説明補助', '変更点サマリの草案生成']
                    ),
                    splitRow('AIチーム編成',
                        ['目的に応じたAIツール選定', 'モデル・ツールの切り替え判断', '各AIへの役割割当と統制'],
                        ['割り当てられた役割での実行', '他AIとの差別化の自己開示']
                    )
                )
            ),

            // ── 設計原則 ──
            h('section', { class: 'card', role: 'region', 'aria-label': 'AI駆動開発の設計原則' },
                h('div', { class: 'card-body flex flex-col gap-4' },
                    h('h2', { class: 'h3' }, '設計原則 — この分担が機能する理由'),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-3' },
                        principleCard('🧭', '設計は人間が保持する', 'AIは設計を実行できるが、設計を「所有」することはできない。意図・制約・ゴールの定義は常に人間の責任領域。', C.human),
                        principleCard('⚡', 'AIは実装エンジンとして扱う', '単一モデルへの依存ではなく、用途・精度・コストに応じてAIを動的に選択・交代させる。AIは固定のパートナーではなく流動的なチーム。', C.ai),
                        principleCard('🔍', '人間が最終検証者である', 'AIの出力は「ドラフト」として扱う。最終的な受け入れ判断・修正指示・公開判断はすべて人間が行う。', C.human),
                        principleCard('📜', '制約はAIへの設計入力とする', 'AIの能力限界・ツール制約は「バグ」ではなく設計条件。制約を吸収し、その中で最適なアウトプットを得る設計がAI-PM本来の仕事。', C.primary),
                        principleCard('🔄', '反復で品質を高める', '1回の完璧な生成より、多数の反復サイクルが品質に寄与する。各サイクルで人間が方向を修正し、AIが実装を更新する。', C.primary),
                        principleCard('🌐', '方法論も成果物として公開する', '出力物（SPA）だけでなく開発プロセスを公開することで、再現可能なAI-PM能力の証拠とする。', C.info)
                    )
                )
            ),

            // ── 核心テーゼ ──
            h('section', { class: 'card card--accent-left', 'data-accent': 'primary', role: 'region', 'aria-label': 'AI-Driven PMの核心テーゼ' },
                h('div', { class: 'card-body' },
                    h('h2', { class: 'h3 mb-10px' }, '核心テーゼ'),
                    h('p', { class: 'text-muted text-body-relaxed-sm' },
                        '「コードを書く力」はもはや唯一のエンジニアリング価値ではない。' +
                        'AIに設計を任せず・AIを信頼しすぎず・AIを有効活用するために必要なのは、' +
                        '設計を言語化する能力・プロンプトで意図を転写する能力・' +
                        '複数AIをオーケストレーションする能力・出力を判断し改善する能力——の4つである。'
                    ),
                    h('p', { class: 'text-muted text-body-relaxed-sm-mt' },
                        '本サイト（v1→v74）はその実証実験の公開記録であり、' +
                        'Human vs AI の分担を守り続けることが、再現性ある AI-Driven PM の証明になる。'
                    ),
                    // ── Incident Report Link ──
                    h('div', {
                        class: 'card--incident'
                    },
                        h('div', { class: 'row-warning-label' },
                            h('span', {}, '🚨'),
                            h('span', {}, 'Incident Report: AIによるアーキテクチャ逸脱記録')
                        ),
                        h('p', { class: 'text-secondary-xs' },
                            '指示を無視してReact/Tailwindで構築された「オーバーエンジニアリングの残骸」を、ハルシネーションの証拠物件として隔離リポジトリに展示しています。'
                        ),
                        h('a', {
                            href: 'https://github.com/yutapr0117-design/ai-overengineering-exhibit',
                            target: '_blank',
                            rel: 'noopener noreferrer',
                            class: 'btn btn-sm btn-incident'
                        }, '[Quarantine] 隔離リポジトリを見る')
                    )
                )
            ),

            // ── 関連ページ ──
            h('section', { class: 'card' },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    h('h2', { class: 'h3' }, '関連ページ'),
                    h('div', { class: 'flex flex-wrap gap-3' },
                        h('button', { class: 'btn btn-primary', onclick: () => Router.navigate('ai-knowhow') }, createIcon('lightbulb', 16), ' AI開発ノウハウ'),
                        h('button', { class: 'btn btn-secondary', onclick: () => Router.navigate('projects') }, createIcon('briefcase', 16), ' プロジェクト'),
                        h('button', { class: 'btn btn-ghost', onclick: () => Router.navigate('about') }, createIcon('user', 16), ' About')
                    )
                )
            ),

            ContactCTA('分担表を読んで「こういう進め方を自社でも取り入れたい」「一緒にプロジェクトを進めたい」と感じた方へ。AI設計・PMOコンサルティングのご相談はこちらから。')
        );
    }

    return { RoleSplitPage, NotFoundPage };
}
