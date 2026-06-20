/**
 * js/pages.js — Page render components (HiringRiskPage / RoleSplitPage / NotFoundPage + helpers)
 * (v80+ Stage 5-b extraction via factory pattern — fixed in Stage 5-j to inject h/createIcon/Router)
 *
 * 【factory pattern への refactor (Stage 5-j fix)】
 * 元の Stage 5-b 抽出では `h, createIcon, Router` を未定義のグローバル参照として書いていたが、
 * これは ESM module スコープでは未定義になり、関数を実行すると ReferenceError になる
 * 隠れバグだった（Playwright が /#/projects と /#/about のみ訪問してこれらのページを
 * レンダリングしていなかったため CI 緑のまま潜在）。本 fix で factory pattern (Brand /
 * Store / State / Theme と同パターン) に切り替えて、依存を引数注入で解消する。
 *
 * 【公開 API（呼び出し側 main.js から見た形）】
 *   const { HiringRiskPage, RoleSplitPage, NotFoundPage } = createPages({ h, createIcon, Router });
 *
 * 【依存（引数で注入）】
 *   - h: DOM builder (js/ui-components.js)
 *   - createIcon: SVG アイコン生成 (js/ui-components.js)
 *   - Router: hash router (js/router.js)
 *   - ContactCTA: 問い合わせ CTA セクション生成関数 (HiringRiskPage / RoleSplitPage 末尾で使用)
 *
 * 【非破壊性】
 *   - 各ページ関数（HiringRiskPage / RoleSplitPage / NotFoundPage）と helper（impactRow /
 *     kpiRow / decisionFlow / riskCard）の DOM 出力は byte-equivalent
 *   - factory closure 内に閉じることで葉契約（Check 47c: import ゼロ）を維持
 */
export function createPages({ h, createIcon, Router, ContactCTA }) {

    function impactRow(riskLabel, bizImpact, metric) {
        return h('div', {
            class: 'row-border-bottom'
        },
            h('div', { class: 'text-label' }, riskLabel),
            h('div', { class: 'flex-1-col' },
                h('div', { class: 'text-sm-body' }, bizImpact),
                metric ? h('div', { class: 'text-muted text-xs-body' }, '📊 ' + metric) : null
            )
        );
    }

    // kpiRow: KPI / 早期兆候行
    function kpiRow(title, metrics) {
        return h('div', {
            class: 'row-border-bottom'
        },
            h('div', { class: 'text-label' }, title),
            h('div', { class: 'text-muted text-sm-body' }, metrics)
        );
    }

    // decisionFlow (v28): KPI → アラート → 打ち手 → 合意 の4点セット
    function decisionFlow(title, signal, action, agreement) {
        return h('div', {
            class: 'grid-role-split-4col'
        },
            h('div', { class: 'text-label' }, title),
            h('div', { class: 'text-xs-body' },
                h('div', { class: 'text-muted text-micro-label' }, '兆候'),
                signal
            ),
            h('div', { class: 'text-xs-body' },
                h('div', { class: 'text-muted text-micro-label' }, '打ち手'),
                h('span', { class: 'text-success-bold' }, action)
            ),
            h('div', { class: 'text-xs-body' },
                h('div', { class: 'text-muted text-micro-label' }, '合意先'),
                h('span', { class: 'color-info' }, agreement)
            )
        );
    }

    // riskCard v28: title / risk / mitigation / impact
    function riskCard(title, risk, mitigation, impact) {
        return h('div', { class: 'card card--p-flex' },
            h('h3', { class: 'text-subhead' }, title),
            h('p', { class: 'text-muted text-xs-body' }, '想定リスク: ' + risk),
            h('p', { class: 'text-xs-body' }, '低減構造: ' + mitigation),
            impact ? h('p', {
                class: 'cell-success-note'
            }, '💹 経営インパクト: ' + impact) : null
        );
    }

    function HiringRiskPage() {
        // レイヤーバッジ
        function layerBadge(num, label, color) {
            return h('div', { class: 'row-gap-8' },
                h('div', {
                    class: 'badge-layer', style: { background: color }
                }, num ? 'LAYER ' + num : null),
                h('span', { class: 'text-subhead-lg' }, label)
            );
        }

        // カラー定義
        const C = {
            primary: 'var(--color-primary)',
            success: 'var(--color-success)',
            warning: 'var(--color-warning)',
            info: 'var(--color-info)',
            purple: '#7c3aed'
        };

        return h('article', { class: 'flex flex-col gap-6 max-w-3xl' },

            // ══ ヘッダー ══
            h('header', { class: 'flex flex-col gap-2', 'data-ai-section': 'hiring-risk' },
                h('h1', { class: 'h1 row-gap-12', 'data-ai-content': 'lead' },
                    createIcon('shield', 30), '採用リスク低減'
                ),
                h('p', { class: 'text-muted', 'data-ai-content': 'lead' },
                    '思想提示ではなく、採用側が負うリスクを構造的に低減する仕組みを明示します。' +
                    '経営層・採用担当・技術責任者のいずれの視点からも評価できる構造で構成しています。'
                ),
                h('div', { class: 'flex flex-wrap gap-2 row-mt-4' },
                    h('span', { class: 'badge badge-secondary' }, '📣 30秒要約'),
                    h('span', { class: 'badge badge-secondary' }, '📋 Executive Summary'),
                    h('span', { class: 'badge badge-secondary' }, '📊 KPI / 観測→打ち手→合意'),
                    h('span', { class: 'badge badge-secondary' }, '🔍 証拠')
                )
            ),

            // ══ 30秒要約（面接用スクリプト）══
            h('section', {
                class: 'card card--hero-accent'
            },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    h('div', { class: 'row-gap-10' },
                        h('div', {
                            class: 'badge-layer--lg', style: { background: C.primary }
                        }, '30秒要約'),
                        h('span', { class: 'text-subhead-lg' }, '面接でそのまま読めるスクリプト')
                    ),
                    h('p', { class: 'text-body-sm' },
                        '私は、短期成果より不可逆損失の回避を優先します。'
                    ),
                    h('p', { class: 'text-body-sm' },
                        '品質・疲弊・属人化・炎上の兆候をKPIで観測し、悪化前に打ち手を実行します。'
                    ),
                    h('p', { class: 'text-body-sm-bold' },
                        '思想は固定、手段は状況で切替。暴走せず、止まらない設計です。'
                    ),
                    h('div', {
                        class: 'wrap-with-border-top'
                    },
                        h('span', { class: 'badge badge-secondary' }, '🚫 不可逆ライン保持'),
                        h('span', { class: 'badge badge-secondary' }, '📊 KPI観測'),
                        h('span', { class: 'badge badge-secondary' }, '🧮 モード切替'),
                        h('span', { class: 'badge badge-secondary' }, '♻ 思想再現可能')
                    )
                )
            ),

            // ══ Executive Summary ══
            h('section', { class: 'card card--accent-left', 'data-accent': 'success' },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    h('h2', { class: 'h3' }, '📋 Executive Summary'),
                    h('p', {},
                        '私を採用することで低減できるリスクを、経営インパクトと観測指標まで落とし込みました。' +
                        '以下の4点が、採用投資リターンを構造的に保全します。'
                    ),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-3 row-mt-4' },
                        ...[
                            ['🚫 重大インシデント確率低減', '不可逆ラインの固定と判断ログの常時レビュー可能化'],
                            ['👤 人材損耗リスク最小化', '「スコープを削り、人を削らない」原則による採用投資の保全'],
                            ['🔗 属人化リスク低減', '問題集化・思考外部化による知識の組織資産化'],
                            ['🔥 炎上時の意思決定停止回避', 'モード切替型アルゴリズムによる緊急時の判断継続']
                        ].map(([item, detail]) =>
                            h('div', {
                                class: 'block-bg-tertiary-sm'
                            },
                                h('div', { class: 'text-label' }, item),
                                h('div', { class: 'text-muted text-xs-body' }, detail)
                            )
                        )
                    )
                )
            ),

            // ══ LAYER 1: 思想 / 不可逆ライン ══
            h('section', { class: 'card card--accent-left', 'data-accent': 'primary' },
                h('div', { class: 'card-body flex flex-col gap-4' },
                    layerBadge(1, '思想 — 不可逆ライン（絶対に越えない境界）', C.primary),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-4' },
                        h('div', { class: 'flex flex-col gap-2' },
                            h('div', { class: 'text-danger-bold' }, '🚫 不可逆 = 絶対にやらない'),
                            h('ul', { class: 'list-disc-sm' },
                                h('li', {}, '人を壊す短期最適'),
                                h('li', {}, '信頼を毀損する意思決定'),
                                h('li', {}, '合意なしの破壊的変更'),
                                h('li', {}, 'チームの持続可能性を捨てた速度追求'),
                                h('li', {}, 'スコープより先に人を削る判断')
                            )
                        ),
                        h('div', { class: 'flex flex-col gap-2' },
                            h('div', { class: 'text-success-head' }, '✅ 可逆 = 素早く切り替える'),
                            h('ul', { class: 'list-disc-sm' },
                                h('li', {}, '技術スタック・アーキテクチャ'),
                                h('li', {}, 'プロセス・開発手法・ツール'),
                                h('li', {}, '優先順位・スコープ・期限'),
                                h('li', {}, '自分の意見・判断・立場'),
                                h('li', {}, '手段・フレームワーク')
                            )
                        )
                    ),
                    h('p', { class: 'text-muted border-top-sep text-muted-sm' },
                        '人は不可逆。プロジェクトは可逆。この原則の固定が、採用投資を守る最大の安全弁です。'
                    )
                )
            ),

            // ══ LAYER 2: 経営インパクト変換 ══
            h('section', { class: 'card card--accent-left', 'data-accent': 'success' },
                h('div', { class: 'card-body flex flex-col gap-0' },
                    layerBadge(2, '経営インパクト — リスクを経営言語で翻訳する', C.success),
                    h('p', { class: 'text-muted text-muted-sm-mb8' },
                        '採用担当・経営層向けに、各リスク低減が「何のコスト削減・何の耐性向上」に対応するかを示します。'
                    ),
                    impactRow('🚫 暴走防止', '重大インシデント・訴訟リスク低減', '意思決定ログの常時レビュー可能化により事後説明責任を確保'),
                    impactRow('🔗 属人化回避', '引継ぎ・組織再編コスト削減', '1人退職で失われる知識量をほぼゼロに近づける'),
                    impactRow('🔥 デスマーチ適応', '事業継続性確保・燃え尽き離職防止', 'モード切替型意思決定で判断速度を維持しつつ人的損耗を抑制'),
                    impactRow('🔒 不可逆回避', '人材損耗リスク最小化', '「スコープ削減を優先し、人を削らない」原則で採用投資を守る'),
                    impactRow('📣 情報可視化', '非技術者との摩擦コスト低減', 'WHY→WHAT→HOW形式による設計判断の常時文書化')
                )
            ),

            // ══ KPI / 観測指標 ══
            h('section', { class: 'card card--accent-left', 'data-accent': 'warning' },
                h('div', { class: 'card-body flex flex-col gap-0' },
                    h('div', { class: 'row-gap-8' },
                        h('div', {
                            class: 'badge-layer', style: { background: C.warning }
                        }, 'KPI'),
                        h('span', { class: 'text-subhead-lg' }, '観測指標 — 問題の早期兆候を検知する')
                    ),
                    h('p', { class: 'text-muted text-muted-sm-mb8' },
                        '「私が機能しているか」を外部から検証できる指標です。採用後の観測・評価基準として活用できます。'
                    ),
                    kpiRow('品質劣化兆候', 'バグ流出率 / 再発率 / エラーバジェット消費率 / レビュー指摘密度'),
                    kpiRow('疲弊兆候', '稼働分散度 / 1on1異常値 / レビュー滞留 / チケット平均リードタイム'),
                    kpiRow('属人化兆候', 'ドキュメント未整備領域 / 引継ぎ不能モジュール率 / 問題集更新頻度'),
                    kpiRow('炎上兆候', 'WIP（仕掛り件数）急増 / リードタイム急騰 / スコープ変更頻度'),
                    h('p', { class: 'text-muted text-muted-xs-sep' },
                        '私はこれらのKPIを自分自身への警戒ラインとして定義し、定期的に観測します。'
                    )
                )
            ),

            // ══ 観測→打ち手→合意（decisionFlow v28）══
            h('section', { class: 'card card--accent-left', 'data-accent': 'info' },
                h('div', { class: 'card-body flex flex-col gap-0' },
                    h('h2', { class: 'h3 mb-2' }, '🔄 観測→判断→実行の流れ'),
                    h('p', { class: 'text-muted text-muted-sm-mb12' },
                        '兆候を観測したとき、どう判断し、誰と合意するかを事前に定義しています。場当たり対応にはなりません。'
                    ),
                    h('div', {
                        class: 'grid-role-split-4col-header'
                    },
                        h('div', { class: 'text-col-header' }, '区分'),
                        h('div', { class: 'text-col-header' }, '兆候 / KPI'),
                        h('div', { class: 'text-col-header color-success' }, '打ち手'),
                        h('div', { class: 'text-col-header color-info' }, '合意先')
                    ),
                    decisionFlow('品質悪化', 'バグ流出率増加 / エラーバジェット急消費', 'WIP制限・スコープ調整・レビュー密度向上', 'EM / PO'),
                    decisionFlow('疲弊兆候', '稼働分散度低下 / 1on1異常値 / 滞留増加', '負荷再配分・優先度再定義・タスク削除', 'マネジメント層'),
                    decisionFlow('属人化兆候', 'ドキュメント未整備率上昇 / 引継ぎ不能領域', '外部化スプリント・レビュー制度強化', 'チーム全体'),
                    decisionFlow('炎上移行', 'WIP急増 / リードタイム急騰', '緊急モード移行・スコープ大幅削減', 'PO / CTO')
                )
            ),

            // ══ LAYER 3: 意思決定アルゴリズム ══
            h('section', { class: 'card card--accent-left', 'data-accent': 'info' },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    layerBadge(3, '意思決定アルゴリズム — モード切替型', C.info),
                    h('p', { class: 'text-muted text-sm-body' },
                        '状況に応じて意思決定モードを切り替えます。どのモードでも「不可逆ライン」は変わりません。'
                    ),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-3 gap-3 row-mt-4' },
                        ...[
                            ['🟢 理想モード', '最適解探索・品質最大化', '時間余裕あり / 技術的負債解消期 / 新規設計フェーズ'],
                            ['🟡 通常モード', 'スコープ管理・契約遵守', '通常スプリント / リリース前 / 品質と速度のバランス'],
                            ['🔴 緊急モード', '不可逆回避優先・スコープ大幅削減', '炎上・障害対応 / リソース枯渇 / デスマーチ移行時']
                        ].map(([mode, action, when]) =>
                            h('div', {
                                class: 'block-bg-tertiary-md'
                            },
                                h('div', { class: 'text-subhead' }, mode),
                                h('div', { class: 'text-sm-bold' }, action),
                                h('div', { class: 'text-muted text-xs-body' }, when)
                            )
                        )
                    ),
                    h('p', { class: 'text-muted text-muted-sm border-top-sep-10' },
                        '共通原則: どのモードでも「人を削る前にスコープを削る」「合意なし破壊的変更はしない」は不変。'
                    )
                )
            ),

            // ══ LAYER 4: 実務行動（6リスクカード）══
            h('section', { class: 'flex flex-col gap-4' },
                h('div', { class: 'row-gap-8-nm' },
                    h('div', {
                        class: 'badge-layer', style: { background: C.purple }
                    }, 'LAYER 4'),
                    h('span', { class: 'text-subhead-lg' }, '実務行動 — リスクカード × 経営インパクト')
                ),
                h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-4' },
                    riskCard('⚡ 意思決定の暴走', '短期最適への過剰収束・感情的判断',
                        '不可逆ライン固定＋レビュー可能な判断ログ保持', '重大事故確率の低減・事後対応コスト削減'),
                    riskCard('🏗 品質崩壊', '速度優先による技術的負債蓄積',
                        '契約明文化＋エラーバジェット思考＋互換維持設計', '長期保守コスト抑制・リリース安定化'),
                    riskCard('🔗 属人化', '判断のブラックボックス化',
                        '問題集化＋思考の外部化＋再現可能ドキュメント設計', '引継ぎ可能性向上・採用投資の保全'),
                    riskCard('🔥 炎上時の判断停止', '場当たり対応・感情的行動',
                        '理想／通常／緊急モード切替型意思決定モデルを保持', '緊急時判断速度向上・二次被害防止'),
                    riskCard('📣 コミュニケーション不全', '技術的問題を非技術者に伝えられない',
                        'WHY→WHAT→HOW順の常時文書化。このSPA自体が実証', '経営層・PM間の摩擦コスト低減'),
                    riskCard('🔄 変化への硬直', '技術・要件変化に対応不能',
                        '破壊的変更を前提とした設計・継続的バージョン進化', '技術的負債の自然解消・中長期コスト低減')
                )
            ),

            // ══ 証拠（ワンクリック遷移）══
            h('section', { class: 'card card--accent-left', 'data-accent': 'info' },
                h('div', { class: 'card-body flex flex-col gap-4' },
                    h('h2', { class: 'h3' }, '🔗 証拠'),
                    h('p', { class: 'text-muted text-sm-body' },
                        '主張はすべてこのSPA内の実物で検証可能です。面接時に開きながら説明できます。'
                    ),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-3' },
                        ...[
                            {
                                title: '📚 PM問題集 → 思考外部化',
                                desc: '意思決定パターンをPM視点で蓄積。PMとして何を考えるかが見える',
                                path: 'quiz?type=pm',
                                label: 'PM問題集を見る'
                            },
                            {
                                title: '🔧 品質問題集 → プロセス設計力',
                                desc: 'バグ対応・品質定義・テスト戦略の判断基準。エンジニアとしての深さが見える',
                                path: 'quiz?type=quality',
                                label: '品質問題集を見る'
                            },
                            {
                                title: '🔒 設計ポリシー → 安全設計思想',
                                desc: 'DEBUGフラグ・XSS契約化・スナップショット検証を実装。安全設計が思想ではなく実装',
                                path: 'settings',
                                label: '設計ポリシーを見る'
                            }
                        ].map(({ title, desc, path, label }) =>
                            h('div', {
                                class: 'block-bg-tertiary-md-8'
                            },
                                h('div', { class: 'text-label' }, title),
                                h('p', { class: 'text-muted text-xs-body' }, desc),
                                path ? h('button', {
                                    class: 'btn btn-primary btn-sm self-start',
                                    onclick: () => Router.navigate(path)
                                }, label) : null
                            )
                        )
                    )
                )
            ),

            // ══ 採用側への約束（最終強化）══
            h('section', { class: 'card card--accent-top', 'data-accent': 'primary' },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    h('h2', { class: 'h3' }, '🤝 採用側への約束'),
                    h('p', { class: 'text-muted text-sm-body' },
                        '「任せても事故らない人」であることを、思想・構造・証拠の3つで担保します。'
                    ),
                    h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-2' },
                        ...[
                            ['不可逆損失を出さない設計を貫く', '思想の固定により、どんな状況でも「やってはいけないこと」を維持'],
                            ['KPIで兆候を観測し、先手を打つ', '品質・疲弊・属人化・炎上を悪化前に検知し、合意形成して対処'],
                            ['状況に応じて手段を切り替える', '原理主義にならず、理想／通常／緊急モードを自律的に切替'],
                            ['判断を外部化し、属人化させない', '問題集・Version History・文書化で組織の知識資産を積み上げる'],
                            ['契約と構造を明文化する', '曖昧な期待から生まれるトラブルを事前に防ぐ'],
                            ['改善を止めない', 'このSPAの継続進化が、習慣であることの証拠']
                        ].map(([promise, reason]) =>
                            h('div', {
                                class: 'block-bg-tertiary-sm'
                            },
                                h('div', { class: 'text-sm-bold' }, '✓ ' + promise),
                                h('p', { class: 'text-muted text-xs-body' }, reason)
                            )
                        )
                    )
                )
            ),

            // ══ CTA ══
            h('section', { class: 'card' },
                h('div', { class: 'card-body flex flex-col gap-3' },
                    h('h2', { class: 'h3' }, '次のステップ'),
                    h('p', { class: 'text-muted' }, '実際の判断プロセスや設計思想を確認したい場合は、以下から詳細をご覧ください。'),
                    h('div', { class: 'flex flex-wrap gap-3' },
                        h('button', { class: 'btn btn-primary', onclick: () => Router.navigate('projects') }, createIcon('briefcase', 16), ' プロジェクト詳細'),
                        h('button', { class: 'btn btn-secondary', onclick: () => Router.navigate('quiz?type=pm') }, createIcon('brain', 16), ' PM問題集'),
                        h('button', { class: 'btn btn-secondary', onclick: () => Router.navigate('quiz?type=quality') }, createIcon('check', 16), ' 品質問題集'),
                        h('button', { class: 'btn btn-ghost', onclick: () => Router.navigate('about') }, createIcon('user', 16), ' About')
                    )
                )
            ),

            ContactCTA('採用リスクの低減構造・KPI・意思決定モデルを確認いただいた方へ。チーム合流・PM採用・アーキテクト採用のご相談はこちらから。')
        );
    }

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

    return { HiringRiskPage, RoleSplitPage, NotFoundPage };
}
