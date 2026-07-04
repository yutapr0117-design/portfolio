/**
 * js/hiring-risk-page.js — HiringRiskPage (採用リスク低減 / v28 採用決裁資料レベル) 葉モジュール
 * (v80+ bloat-reduction extraction via factory pattern — js/pages.js から分離)
 *
 * 【背景】
 * js/pages.js は HiringRiskPage / RoleSplitPage / NotFoundPage + helper を 1 ファイルに
 * 抱え 642 行に肥大化していた。HiringRiskPage は単独で ~326 行を占める最大ページ (v28
 * 採用決裁資料レベルの静的コンテンツ) で、専用 helper (impactRow / kpiRow / decisionFlow /
 * riskCard) と共に完全に自己完結する (mutable state ゼロ・呼び出しは本ページ span 内のみ)。
 * これを別葉モジュールへ分離し pages.js を保守しやすく縮小する。挙動は byte-equivalent。
 *
 * 【公開 API（呼び出し側 main.js から見た形）】
 *   const HiringRiskPage = createHiringRiskPage({ h, createIcon, Router, ContactCTA });
 *
 * 【依存（引数で注入）】
 *   - h: DOM builder (js/ui-components.js)
 *   - createIcon: SVG アイコン生成 (js/ui-components.js)
 *   - Router: hash router (js/router.js)
 *   - ContactCTA: 問い合わせ CTA セクション生成関数 (末尾で使用・js/components.js から供給)
 *
 * 【非破壊性】
 *   - HiringRiskPage 関数本体と helper (impactRow / kpiRow / decisionFlow / riskCard) の
 *     DOM 出力は抽出元から byte-equivalent
 *   - factory closure 内に閉じることで葉契約（Check 47c: import ゼロ）を維持
 */
export function createHiringRiskPage({ h, createIcon, Router, ContactCTA }) {

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

    return { HiringRiskPage };
}
