/**
 * js/ai-page.js — AIPage (AI アシスト・ローカル版) 葉モジュール
 * (v80+ bloat-reduction extraction via factory pattern — js/apps.js から分離)
 *
 * 【背景】
 * js/apps.js は TaskPage / TodoPage / PomodoroPage / AIPage / NotesPage / SettingsPage を
 * 1 ファイルに抱え 1,179 行に肥大化していた。AIPage は private state が `aiLoading` 1 個のみで
 * local helper (analyzeInput / generateResponse / submit / buildUI) と共に完全自己完結する
 * (最も安全な抽出単位)。これを別葉モジュールへ分離し apps.js を縮小する。挙動 byte-equivalent。
 *
 * 【公開 API（呼び出し側 main.js から見た形）】
 *   const { AIPage } = createAIPage({ h, createIcon, State, CONSTANTS });
 *
 * 【依存（引数で注入）】
 *   - h: DOM builder (js/ui-components.js)
 *   - createIcon: SVG アイコン生成 (js/ui-components.js)
 *   - State: アプリ状態ストア (js/state.js) — appsData.ai.history
 *   - CONSTANTS: LIMITS.AI_MESSAGE (prompt bound) 用 (js/constants.js)
 *   - window.render / document: グローバル (再描画・focus 復元)
 *
 * 【非破壊性】
 *   - AIPage 関数本体と private state (aiLoading) の挙動は抽出元から byte-equivalent
 *   - factory closure 内に閉じることで葉契約（Check 47c: import ゼロ）を維持
 */
export function createAIPage({ h, createIcon, State, CONSTANTS }) {

    // ===== Component: AI Assist Page =====
    let aiLoading = false;

    function AIPage() {
        const ai = State.get().appsData.ai;

        function analyzeInput(input) {
            const p = input.toLowerCase();
            if (p.includes('エラー') || p.includes('バグ') || p.includes('失敗')) {return 'troubleshoot';}
            if (p.includes('設計') || p.includes('計画') || p.includes('構成')) {return 'design';}
            if (p.includes('分解') || p.includes('タスク') || p.includes('手順') || p.includes('ステップ') || p.includes('段取り')) {return 'breakdown';}
            if (p.includes('文章') || p.includes('書い') || p.includes('説明') || p.includes('ライティング') || p.includes('文言')) {return 'writing';}
            return 'general';
        }

        function generateResponse(input, type) {
            if (type === 'troubleshoot') {
                return `[AI分析: トラブルシューティング]
    • 再現条件を明確化
    • 影響範囲を特定
    • ログ/証跡を収集
    • 切り分けを実施
    • 修正と回帰テスト

    詳細な手順が必要であれば、「具体的なエラー内容を教えてください」とお伝えください。`;
            }
            if (type === 'design') {
                return `[AI分析: 設計支援]
    • 目的と非目的の定義
    • 依存関係と制約の整理
    • 失敗条件の洗い出し
    • 境界（責任/権限）の明確化
    • 検証手段の設計

    設計書のテンプレートが必要であればお知らせください。`;
            }
            if (type === 'breakdown') {
                return `[AI分析: タスク分解]
    • ゴールと完了条件を定義
    • 大タスクを独立した中タスクへ分割
    • 各タスクの依存関係と順序を整理
    • 見積もりとリスクを付与
    • 検証可能な単位まで具体化

    分解対象を具体的にお知らせいただければ、さらに詳細化できます。`;
            }
            if (type === 'writing') {
                return `[AI分析: 文章生成支援]
    • 目的と読者（誰に何を）を明確化
    • 要点を箇条書きで抽出
    • 構成（導入→本論→結論）を設計
    • トーンと文体を統一
    • 推敲（冗長・曖昧・重複の除去）

    書きたい内容の要点をお知らせいただければ、たたき台を提案できます。`;
            }
            return `[AI分析: 一般支援]
    トラブルシューティング・設計支援・タスク分解・文章生成に対応しています。
    具体的なご質問をお聞かせください。`;
        }

        function submit(input) {
            if (!input.trim() || aiLoading) {return;}
            aiLoading = true;
            window.render(); // ローディング表示のため再描画

            const type = analyzeInput(input);

            setTimeout(() => {
                // [FIX] aiLoading の解除を finally で保証する fail-safe。従来は通常経路末尾で
                //   aiLoading=false を代入していたため、generateResponse / State.update が万一 throw
                //   すると aiLoading が true のまま残り、submit ガード (if (aiLoading) return) が
                //   以後の全 submit をブロックして AI ページが恒久 submit 不能に stuck した
                //   (pomodoro/drawer と同じ「フラグをエラー経路でリセットしない」stuck-state class)。
                //   throw が起きても必ず入力可能へ復帰させる。
                try {
                    const response = generateResponse(input, type);
                    State.update(s => {
                        s.appsData.ai.history.push({
                            // [FIX] prompt を AI_MESSAGE 上限で bound する (他アプリの入力 slice と同様)。
                            // 従来は無制限保存で、巨大入力が ai.history (last AI_HISTORY 件) に蓄積し localStorage を
                            // bloat させ得た。AI_MESSAGE 定数は元来この制限用だが配線が失われていた (Check 125 が検出)。
                            prompt: input.slice(0, CONSTANTS.LIMITS.AI_MESSAGE),
                            response,
                            timestamp: Date.now()
                        });
                        // 履歴保持件数は store.js normalize と同じ CONSTANTS.LIMITS.AI_HISTORY 単一ソース (Check 369 が drift 防止)
                        s.appsData.ai.history = s.appsData.ai.history.slice(-CONSTANTS.LIMITS.AI_HISTORY);
                    });
                } finally {
                    aiLoading = false;
                    // 万一の throw で State.update の notify が走らない場合でもローディング表示を解除。
                    try { window.render(); } catch { /* noop */ }
                    // 応答完了後に再度入力できるようフォーカスを復元
                    setTimeout(() => document.getElementById('ai-input')?.focus(), 0);
                }
            }, 300);
        }

        function buildUI() {
            return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
                h('header', { class: 'flex items-center gap-3' },
                    createIcon('brain', 28),
                    h('h1', { class: 'h1' }, 'AI アシスト（ローカル版）')
                ),

                h('p', { class: 'text-muted' }, '外部APIに依存せず、ブラウザ内で動作するAI支援ツールです。'),

                // Chat History
                h('section', {
                    class: 'card scroll-y-400'
                },
                    h('div', { class: 'card-body flex flex-col gap-4' },
                        ai.history.length === 0 ?
                            h('p', { class: 'text-muted text-center py-8' },
                                '会話を始めましょう。トラブルシューティング・設計支援・タスク分解・文章生成に対応しています。'
                            ) :
                            ai.history.flatMap(histItem => [
                                h('div', { class: 'flex flex-col gap-1' },
                                    h('div', {
                                        class: 'self-end p-3 rounded-lg chat-bubble-own'
                                    }, histItem.prompt),
                                    h('div', {
                                        class: 'self-start p-3 rounded-lg chat-bubble-other'
                                    }, histItem.response),
                                    h('span', { class: 'text-xs text-muted self-start' },
                                        // [FIX] 時刻のみ (toLocaleTimeString) だと複数日にまたがる永続履歴で
                                        // どの日か曖昧なため、date+time のコンパクト表示に変更 (秒は省略)。
                                        new Date(histItem.timestamp).toLocaleString([], { dateStyle: 'short', timeStyle: 'short' })
                                    )
                                )
                            ])
                    )
                ),

                // Input
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('div', { class: 'flex gap-3' },
                            h('input', {
                                id: 'ai-input',
                                class: 'input',
                                // [A11Y 3.3.2/4.1.2] placeholder-only を避け恒久 accessible name を付与。
                                'aria-label': 'AI アシスタントへの依頼を入力',
                                enterkeyhint: 'send',
                                placeholder: '例：デプロイ手順を分解して、タスク管理アプリの説明文を書いて...',
                                disabled: aiLoading,
                                onkeydown: (e) => {
                                    // [FIX] IME 変換確定の Enter (e.isComposing) では submit しない。
                                    // 日本語入力で変換候補を Enter 確定した際の未確定テキスト誤送信を防ぐ
                                    // (task 入力と同クラスの footgun。todo の composing ガードと同等)。
                                    if (e.key === 'Enter' && !e.isComposing) {
                                        submit(e.target.value);
                                        // DOM再構築されるため input の value リセットは不要
                                    }
                                }
                            }),
                            h('button', {
                                class: 'btn btn-primary',
                                disabled: aiLoading,
                                onclick: (e) => {
                                    const input = e.target.previousElementSibling;
                                    submit(input.value);
                                }
                            }, aiLoading ? '生成中...' : '送信')
                        )
                    )
                )
            );
        }

        return buildUI();
    }

    return { AIPage };
}
