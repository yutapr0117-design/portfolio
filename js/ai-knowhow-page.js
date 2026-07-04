/**
 * js/ai-knowhow-page.js — AIKnowhowPage レンダラ (v80+ 肥大化解消: js/components.js から抽出)
 *
 * 肥大化していた js/components.js (1,370 行) から最大の単一ページ AIKnowhowPage (~295 行) を
 * factory pattern で葉モジュールへ分離した。挙動は byte-equivalent (関数本体を無改変で移設)。
 *
 * 【依存 (引数注入)】
 *   - h          : DOM ビルダー (js/ui-components.js)
 *   - createIcon : SVG アイコンヘルパー (js/ui-components.js)
 *   - ContactCTA : 末尾 CTA コンポーネント (js/components.js の共有 helper。複数ページで使用され
 *                  createComponents が返すため、main.js が生成後に本 factory へ注入する)
 *
 * 【葉契約】ローカル ESM import ゼロ (Check 47c)。h/createIcon/ContactCTA は全て引数で受け取る。
 * 【非破壊性】main.js は createComponents 実行後に ContactCTA を取り出し
 *   createAIKnowhowPage({ h, createIcon, ContactCTA }) で AIKnowhowPage を生成し、
 *   render dispatch (route 'ai-knowhow') へ従来どおり配線する。挙動不変を behavior e2e が保証。
 */
export function createAIKnowhowPage({ h, createIcon, ContactCTA }) {
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
                        '本質は「人間が（自走の最中でも随時）AI と議論の場＝議論タイムを設け → 互いの合意 → その合意に基づき AI に無限改善自走を委任 → 逸脱時に人間が決定的に是正」という協働ループ。人間は AI が提示した選択肢に縛られず、いつでも自走に割り込んで対話で方向を定め直せる——AI はそれに即 yield する。合意した方向に沿って AI が案を出しつつ自律実行（実装・検証・マージ・本番デプロイ）し、次の一手も提案する。無監督の全自動でもマイクロマネジメントでもなく、議論と合意に基づく統治である。'
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

    return AIKnowhowPage;
}
