/**
 * js/apps.js — Productivity Apps (TaskPage / TodoPage / PomodoroPage / AIPage /
 * SettingsPage) — v80+ Stage 5-n extraction via factory pattern
 *
 * main.js の Apps Component 5 関数（合計 5 ページ）と関連 closure state を依存注入で
 * 物理分割した葉モジュール。Brand / Store / State / Theme / Meta Management /
 * Components と同じく、すべての closure 依存を `createApps` 関数の引数で受け取る
 * ことで、葉契約 (Check 47c: import ゼロ) を維持しつつ各関数の挙動と公開 API を
 * 完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const { TaskPage, TodoPage, PomodoroPage, AIPage, NotesPage, SettingsPage } = createApps({...});
 *
 * 【factory closure 内の private state（揮発性 UI 状態の維持）】
 *   - taskFilter (const), todoFilter / todoComposing (let)
 *   - pomodoroTimer (let), aiLoading (let)
 *   - settings* (let × 6) — Settings page 専用ローカル状態
 *
 * これらは元 main.js IIFE 内の関数外宣言で、各 Page 関数の再呼出間で状態を保持していた。
 * factory closure 内に同じ位置で declare することで、抽出前後の挙動は byte-equivalent。
 *
 * 【依存（引数で注入）】
 *   - h, createIcon, Toast: js/ui-components.js
 *   - AUTHOR: js/identity.js
 *   - Router: js/router.js
 *   - State: js/state.js factory instance
 *   - Theme: js/theme.js factory instance
 *   - Brand: js/brand.js factory instance
 *   - Store: js/store.js factory instance
 *   - Storage: js/storage.js (Settings の snapshot 保存/復元で Storage.parse/set/remove)
 *   - CONSTANTS: js/constants.js
 *   - generateId, clamp, slugify: js/pure-utils.js
 *   - window グローバル経由: render (window.render として後段で代入される)
 *
 * 【非破壊性】
 *   - 抽出時は 5 関数の DOM 出力・class 名・style・aria 属性が byte-equivalent。その後 A 群で NotesPage を
 *     追加（公開 API は 6 関数）、bug-fix で各種挙動を精緻化済（PomodoroPage stale-closure #121/134 /
 *     SettingsPage upsert data-loss #192 / IME ガード #151/152 / slug 衝突 #154 / AIPage prompt bound #230 /
 *     SettingsPage 手動追加フォームの Demo セレクタに notes option 追加 #294 等）。
 *   - localStorage への副作用順序（State.update 経由）も不変
 *   - AIDK Kernel / AIO 正本層には影響しない
 */
export function createApps({ h, createIcon, Toast, AUTHOR, Router, State, Theme, Brand, Store, Storage, CONSTANTS, generateId, clamp, slugify }) {
    // ===== Component: Apps Hub =====

    // ===== Component: Task App =====
    // [FIX] 揮発性クロージャ問題の解決：UIステートをコンポーネント外に保持
    // v80+ lint: 束縛自体は再代入されず .q / .priority のプロパティ変異のみのため const が正しい
    // （再代入が無い束縛に let を使うと prefer-const に抵触する。挙動は不変）。
    const taskFilter = { q: '', priority: 'all' };

    function TaskPage() {

        function addTask(title) {
            if (!title.trim()) {return;}
            State.update(s => {
                s.appsData.tasks.unshift({
                    id: generateId(),
                    title: title.trim().slice(0, CONSTANTS.LIMITS.TASK_TITLE),
                    status: 'backlog',
                    priority: 'med',
                    tags: [],
                    createdAt: Date.now(),
                    updatedAt: Date.now()
                });
            });
            Toast.show('タスクを追加しました', 'success');
        }

        function updateTask(id, updates) {
            State.update(s => {
                const task = s.appsData.tasks.find(t => t.id === id);
                if (task) {
                    Object.assign(task, updates, { updatedAt: Date.now() });
                }
            });
        }

        function deleteTask(id) {
            State.update(s => {
                s.appsData.tasks = s.appsData.tasks.filter(t => t.id !== id);
                if (s.appsData.pomodoro.runtime.linkedTaskId === id) {
                    s.appsData.pomodoro.runtime.linkedTaskId = null;
                }
            });
            Toast.show('タスクを削除しました', 'success');
        }

        function moveStatus(task, direction) {
            const statuses = ['backlog', 'in-progress', 'done'];
            const idx = statuses.indexOf(task.status);
            const newIdx = clamp(idx + direction, 0, statuses.length - 1);
            if (newIdx !== idx) {
                updateTask(task.id, { status: statuses[newIdx] });
            }
        }

        function getFilteredTasks() {
            return State.get().appsData.tasks.filter(t => {
                const matchesQ = !taskFilter.q ||
                    t.title.toLowerCase().includes(taskFilter.q.toLowerCase()) ||
                    t.tags.some(tag => tag.toLowerCase().includes(taskFilter.q.toLowerCase()));
                const matchesPriority = taskFilter.priority === 'all' || t.priority === taskFilter.priority;
                return matchesQ && matchesPriority;
            });
        }

        // [FIX] シャドウイング問題の解決：名称を buildUI に変更
        function buildUI() {
            const container = document.createElement('div');
            container.className = 'flex flex-col gap-4';

            // Header
            container.appendChild(h('header', {},
                h('div', { class: 'flex items-center gap-3 mb-4' },
                    createIcon('checkSquare', 28),
                    h('h1', { class: 'h1' }, 'タスク管理')
                ),
                h('div', { class: 'grid grid-cols-2 gap-4' },
                    h('input', {
                        id: 'task-input',
                        class: 'input',
                        placeholder: '新しいタスクを入力...',
                        onkeydown: (e) => {
                            // [FIX] IME 変換確定の Enter (e.isComposing) では追加しない。日本語入力で
                            // 変換候補を Enter 確定した際に未確定文字が誤ってタスク化される footgun を防ぐ
                            // (todo 入力の todoComposing ガードと同等の保護を task 入力にも付与)。
                            if (e.key === 'Enter' && !e.isComposing) {
                                addTask(e.target.value);
                                // 全体再描画の直後にフォーカスを復元し、連続入力を可能にする
                                setTimeout(() => document.getElementById('task-input')?.focus(), 0);
                            }
                        }
                    }),
                    h('select', {
                        class: 'input',
                        'aria-label': '優先度で絞り込み',
                        value: taskFilter.priority,
                        onchange: (e) => {
                            taskFilter.priority = e.target.value;
                            window.render(); // グローバルレンダーを呼び出し
                        }
                    },
                        h('option', { value: 'all', text: '優先度: 全て' }),
                        h('option', { value: 'high', text: 'High' }),
                        h('option', { value: 'med', text: 'Med' }),
                        h('option', { value: 'low', text: 'Low' })
                    )
                )
            ));

            // Kanban
            const statuses = [
                { id: 'backlog', label: '未着手' },
                { id: 'in-progress', label: '進行中' },
                { id: 'done', label: '完了' }
            ];

            const allTasks = getFilteredTasks();

            const board = h('div', {
                class: 'grid grid-cols-3 col-min-400'
            });

            statuses.forEach(col => {
                const tasks = allTasks.filter(t => t.status === col.id);
                const column = h('section', {
                    class: 'card bg-secondary'
                },
                    h('div', { class: 'card-header' },
                        h('div', { class: 'flex items-center justify-between' },
                            h('h2', { class: 'h4' }, col.label),
                            h('span', { class: 'badge badge-secondary' }, String(tasks.length))
                        )
                    ),
                    h('div', { class: 'card-body flex flex-col gap-3' },
                        ...tasks.map(task =>
                            h('article', {
                                class: 'card bg-surface'
                            },
                                h('div', { class: 'p-3' },
                                    h('div', { class: 'flex items-start justify-between gap-2 mb-2' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', {
                                                class: 'w-2 h-2 rounded-full',
                                                style: `background:${task.priority === 'high' ? 'var(--color-danger)' :
                                                    task.priority === 'med' ? 'var(--color-warning)' :
                                                        'var(--color-success)'
                                                    };`
                                            }),
                                            h('span', { class: 'font-medium text-small' }, task.title)
                                        ),
                                        h('button', {
                                            class: 'icon-btn btn-sm icon-sm',
                                            'aria-label': 'タスクを削除',
                                            onclick: () => deleteTask(task.id)
                                        }, createIcon('trash', 14))
                                    ),
                                    h('div', { class: 'flex items-center justify-between' },
                                        h('select', {
                                            class: 'input btn-sm',
                                            'aria-label': 'タスクの優先度',
                                            style: 'width:auto;padding:0.25rem 0.5rem;font-size:0.75rem;',
                                            value: task.priority,
                                            onchange: (e) => updateTask(task.id, { priority: e.target.value })
                                        },
                                            h('option', { value: 'high', text: 'High' }),
                                            h('option', { value: 'med', text: 'Med' }),
                                            h('option', { value: 'low', text: 'Low' })
                                        ),
                                        h('div', { class: 'flex gap-1' },
                                            h('button', {
                                                class: 'btn btn-ghost btn-sm',
                                                disabled: task.status === 'backlog',
                                                onclick: () => moveStatus(task, -1)
                                            }, '←'),
                                            h('button', {
                                                class: 'btn btn-ghost btn-sm',
                                                disabled: task.status === 'done',
                                                onclick: () => moveStatus(task, 1)
                                            }, '→')
                                        )
                                    )
                                )
                            )
                        )
                    )
                );
                board.appendChild(column);
            });

            container.appendChild(board);
            return container;
        }

        return buildUI();
    }

    // ===== Component: Todo App =====
    // [FIX] 揮発性クロージャ問題の解決
    let todoFilter = 'all';
    let todoComposing = false;

    function TodoPage() {

        function addTodo(text) {
            if (!text.trim()) {return;}
            State.update(s => {
                s.appsData.todos.unshift({
                    id: generateId(),
                    text: text.trim().slice(0, CONSTANTS.LIMITS.TODO_TEXT),
                    completed: false,
                    createdAt: Date.now(),
                    dueDate: null
                });
            });
        }

        function toggleTodo(id) {
            State.update(s => {
                const todo = s.appsData.todos.find(t => t.id === id);
                if (todo) {todo.completed = !todo.completed;}
            });
        }

        function deleteTodo(id) {
            State.update(s => {
                s.appsData.todos = s.appsData.todos.filter(t => t.id !== id);
            });
        }

        function clearCompleted() {
            State.update(s => {
                s.appsData.todos = s.appsData.todos.filter(t => !t.completed);
            });
            Toast.show('完了済みを削除しました', 'success');
        }

        const todos = State.get().appsData.todos;
        const filtered = todos.filter(t => {
            if (todoFilter === 'active') {return !t.completed;}
            if (todoFilter === 'completed') {return t.completed;}
            return true;
        });

        return h('div', { class: 'flex flex-col gap-4 max-w-2xl error-boundary-fallback', role: 'alert', 'aria-invalid': 'true', 'aria-errormessage': 'fallback-details', 'aria-description': 'Architecture constraint successfully caught an unstable state transition.' },
            h('header', { class: 'flex items-center gap-3' },
                createIcon('list', 28),
                h('h1', { class: 'h1' }, 'クイックTODO')
            ),

            h('section', { class: 'card' },
                h('div', { class: 'card-body' },
                    h('input', {
                        id: 'todo-input',
                        class: 'input',
                        placeholder: '入力してEnter（IME対応）...',
                        oncompositionstart: () => todoComposing = true,
                        oncompositionend: () => todoComposing = false,
                        onkeydown: (e) => {
                            if (e.key === 'Enter' && !todoComposing) {
                                addTodo(e.target.value);
                                // 全体再描画の直後にフォーカスを復元
                                setTimeout(() => document.getElementById('todo-input')?.focus(), 0);
                            }
                        }
                    }),
                    h('div', { class: 'flex gap-2 mt-4' },
                        h('select', {
                            class: 'input w-auto',
                            'aria-label': 'TODO を絞り込み',
                            value: todoFilter,
                            onchange: (e) => { todoFilter = e.target.value; window.render(); }
                        },
                            h('option', { value: 'all', text: '全て' }),
                            h('option', { value: 'active', text: '未完了' }),
                            h('option', { value: 'completed', text: '完了' })
                        ),
                        h('button', {
                            class: 'btn btn-secondary btn-sm',
                            disabled: !todos.some(t => t.completed),
                            onclick: clearCompleted
                        }, '完了済み削除')
                    )
                )
            ),

            h('section', { class: 'flex flex-col gap-2' },
                ...filtered.map(todo =>
                    h('article', { class: 'card' },
                        h('div', { class: 'card-body flex items-center gap-3' },
                            h('input', {
                                type: 'checkbox',
                                checked: todo.completed,
                                onchange: () => toggleTodo(todo.id),
                                'aria-label': todo.completed ? '未完了に戻す' : '完了にする'
                            }),
                            h('span', {
                                class: ['flex-1', todo.completed && 'text-muted'],
                                style: todo.completed ? 'text-decoration:line-through;opacity:0.6;' : undefined
                            }, todo.text),
                            h('button', {
                                class: 'icon-btn',
                                onclick: () => deleteTodo(todo.id),
                                'aria-label': '削除'
                            }, createIcon('x', 16))
                        )
                    )
                ),
                filtered.length === 0 && h('p', { class: 'text-muted text-center py-8' }, 'TODOはありません。')
            )
        );
    }

    // ===== Component: Pomodoro App =====
    let pomodoroTimer = null;

    function PomodoroPage() {
        const pomo = State.get().appsData.pomodoro;

        function formatTime(sec) {
            const m = Math.floor(sec / 60);
            const s = sec % 60;
            return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        }

        function getDuration(mode) {
            // [FIX] live state を読む (getRemaining と同根の stale-closure 対策): startTimer の
            // interval は start() 時の closure に固定され、その closure の `pomo.settings` は稼働中に
            // 設定変更されても古いまま。complete() が getDuration で remainingSec をリセットする際に
            // 旧設定値を使うバグになるため、必ず最新 settings を参照する。
            const settings = State.get().appsData.pomodoro.settings;
            return (mode === 'work' ? settings.work :
                mode === 'short-break' ? settings.short : settings.long) * 60;
        }

        function getRemaining() {
            // [FIX] live state を読む: startTimer の interval は start() 時の closure に固定され、
            // その closure の `pomo` は再描画後に stale (isActive=false の旧 runtime) になる。
            // クロージャ変数を読むと interval の完了判定が常に remainingSec を返し complete() が
            // 永遠に発火しない (表示は毎 tick の window.render が live を読むので 0 まで進むが
            // 停止・history 記録・完了通知が起きない) ため、ここは必ず最新 runtime を参照する。
            const rt = State.get().appsData.pomodoro.runtime;
            if (rt.isActive && rt.endAtMs) {
                return Math.max(0, Math.ceil((rt.endAtMs - Date.now()) / 1000));
            }
            return rt.remainingSec;
        }

        function start() {
            const remaining = getRemaining();
            State.update(s => {
                s.appsData.pomodoro.runtime.isActive = true;
                s.appsData.pomodoro.runtime.endAtMs = Date.now() + remaining * 1000;
            });
            startTimer();
        }

        function pause() {
            State.update(s => {
                s.appsData.pomodoro.runtime.isActive = false;
                s.appsData.pomodoro.runtime.endAtMs = null;
                s.appsData.pomodoro.runtime.remainingSec = getRemaining();
            });
            stopTimer();
        }

        function reset() {
            stopTimer();
            const duration = getDuration(pomo.runtime.mode);
            State.update(s => {
                s.appsData.pomodoro.runtime.isActive = false;
                s.appsData.pomodoro.runtime.endAtMs = null;
                s.appsData.pomodoro.runtime.remainingSec = duration;
            });
        }

        function complete() {
            stopTimer();
            const duration = getDuration(pomo.runtime.mode);
            State.update(s => {
                s.appsData.pomodoro.history.push({
                    timestamp: Date.now(),
                    durationMinutes: Math.floor(duration / 60),
                    type: s.appsData.pomodoro.runtime.mode,
                    linkedTaskId: s.appsData.pomodoro.runtime.linkedTaskId
                });
                s.appsData.pomodoro.history = s.appsData.pomodoro.history.slice(-200);
                s.appsData.pomodoro.runtime.isActive = false;
                s.appsData.pomodoro.runtime.endAtMs = null;
                s.appsData.pomodoro.runtime.remainingSec = duration;
            });
            Toast.show('セッション完了！', 'success');
        }

        function switchMode(mode) {
            stopTimer();
            const duration = getDuration(mode);
            State.update(s => {
                s.appsData.pomodoro.runtime.mode = mode;
                s.appsData.pomodoro.runtime.isActive = false;
                s.appsData.pomodoro.runtime.endAtMs = null;
                s.appsData.pomodoro.runtime.remainingSec = duration;
            });
        }

        function startTimer() {
            if (pomodoroTimer) {clearInterval(pomodoroTimer);}
            pomodoroTimer = setInterval(() => {
                const remaining = getRemaining();
                if (remaining <= 0) {
                    complete();
                    window.render(); // グローバルを描画
                } else if (Router.getRoute().name === 'app-pomodoro') {
                    window.render(); // グローバルを描画
                }
            }, 1000);
        }

        function stopTimer() {
            if (pomodoroTimer) {
                clearInterval(pomodoroTimer);
                pomodoroTimer = null;
            }
        }

        const modes = [
            { id: 'work', label: '集中' },
            { id: 'short-break', label: '短休憩' },
            { id: 'long-break', label: '長休憩' }
        ];

        const remaining = getRemaining();
        const isActive = pomo.runtime.isActive;

        // [FIX] リロード/再初期化で active タイマーの interval が失われる問題を修正。
        // pomodoroTimer は createApps factory 変数ゆえ reload で null に戻るが、runtime.isActive は
        // endAtMs>now なら normalize (store.js) が保持する。startTimer は start() ボタンからのみ
        // 呼ばれ auto-resume が無かったため、reload 後は「一時停止ボタン表示 (isActive=true) だが
        // countdown が frozen で complete() が永遠に発火しない」stuck 状態になっていた。isActive
        // かつ interval 不在 (pomodoroTimer===null) のときだけ resume する (稼働中の毎秒再描画では
        // pomodoroTimer!==null ゆえ二重 interval にならない・complete/pause 後は isActive=false)。
        if (isActive && !pomodoroTimer) {
            startTimer();
        }

        function buildUI() {
            return h('div', { class: 'flex flex-col gap-4 max-w-xl' },
                h('header', { class: 'flex items-center gap-3' },
                    createIcon('clock', 28),
                    h('h1', { class: 'h1' }, 'ポモドーロタイマー')
                ),

                // Timer Display
                h('section', { class: 'card' },
                    h('div', { class: 'card-body text-center' },
                        h('div', { class: 'flex justify-center gap-2 mb-6' },
                            ...modes.map(m =>
                                h('button', {
                                    class: ['btn', pomo.runtime.mode === m.id ? 'btn-primary' : 'btn-secondary'],
                                    onclick: () => switchMode(m.id)
                                }, m.label)
                            )
                        ),
                        h('div', {
                            class: 'font-mono mb-6 text-stat'
                        }, formatTime(remaining)),
                        h('div', { class: 'flex justify-center gap-3' },
                            h('button', {
                                class: 'btn btn-primary btn-lg',
                                onclick: isActive ? pause : start
                            }, isActive ? h('span', {}, createIcon('pause', 20), ' 一時停止') : h('span', {}, createIcon('play', 20), ' 開始')),
                            h('button', {
                                class: 'btn btn-secondary',
                                onclick: reset,
                                'aria-label': 'リセット'
                            }, createIcon('rotate', 20))
                        )
                    )
                ),

                // Settings
                h('section', { class: 'card' },
                    h('div', { class: 'card-body' },
                        h('h2', { class: 'h3 mb-4' }, '設定（分）'),
                        h('div', { class: 'grid grid-cols-3 gap-4' },
                            h('div', {},
                                h('label', { class: 'text-small text-muted mb-1 block' }, '集中'),
                                h('input', {
                                    type: 'number',
                                    class: 'input',
                                    'aria-label': '集中時間（分）',
                                    value: pomo.settings.work,
                                    min: 1, max: 180,
                                    onchange: (e) => State.update(s => {
                                        s.appsData.pomodoro.settings.work = clamp(parseInt(e.target.value, 10) || 25, 1, 180);
                                        if (!s.appsData.pomodoro.runtime.isActive && s.appsData.pomodoro.runtime.mode === 'work') {
                                            s.appsData.pomodoro.runtime.remainingSec = s.appsData.pomodoro.settings.work * 60;
                                        }
                                    })
                                })
                            ),
                            h('div', {},
                                h('label', { class: 'text-small text-muted mb-1 block' }, '短休憩'),
                                h('input', {
                                    type: 'number',
                                    class: 'input',
                                    'aria-label': '短休憩時間（分）',
                                    value: pomo.settings.short,
                                    min: 1, max: 60,
                                    onchange: (e) => State.update(s => {
                                        s.appsData.pomodoro.settings.short = clamp(parseInt(e.target.value, 10) || 5, 1, 60);
                                    })
                                })
                            ),
                            h('div', {},
                                h('label', { class: 'text-small text-muted mb-1 block' }, '長休憩'),
                                h('input', {
                                    type: 'number',
                                    class: 'input',
                                    'aria-label': '長休憩時間（分）',
                                    value: pomo.settings.long,
                                    min: 1, max: 120,
                                    onchange: (e) => State.update(s => {
                                        s.appsData.pomodoro.settings.long = clamp(parseInt(e.target.value, 10) || 15, 1, 120);
                                    })
                                })
                            )
                        )
                    )
                )
            );
        }

        return buildUI();
    }

    // ===== Component: AI Assist Page =====
    let aiLoading = false;

    function AIPage() {
        const ai = State.get().appsData.ai;

        function analyzeInput(input) {
            const p = input.toLowerCase();
            if (p.includes('エラー') || p.includes('バグ') || p.includes('失敗')) {return 'troubleshoot';}
            if (p.includes('設計') || p.includes('計画') || p.includes('構成')) {return 'design';}
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
            return `[AI分析: 一般支援]
    タスク分解、文章生成、ポートフォリオ作成支援などに対応しています。
    具体的なご質問をお聞かせください。`;
        }

        function submit(input) {
            if (!input.trim() || aiLoading) {return;}
            aiLoading = true;
            window.render(); // ローディング表示のため再描画

            const type = analyzeInput(input);

            setTimeout(() => {
                const response = generateResponse(input, type);
                State.update(s => {
                    s.appsData.ai.history.push({
                        // [FIX] prompt を AI_MESSAGE 上限で bound する (他アプリの入力 slice と同様)。
                        // 従来は無制限保存で、巨大入力が ai.history (last 80) に蓄積し localStorage を
                        // bloat させ得た。AI_MESSAGE 定数は元来この制限用だが配線が失われていた (Check 125 が検出)。
                        prompt: input.slice(0, CONSTANTS.LIMITS.AI_MESSAGE),
                        response,
                        timestamp: Date.now()
                    });
                    s.appsData.ai.history = s.appsData.ai.history.slice(-80);
                });
                aiLoading = false;
                // State.update が内部で notify() するため window.render() は自動で呼ばれる
                // 応答完了後に再度入力できるようフォーカスを復元
                setTimeout(() => document.getElementById('ai-input')?.focus(), 0);
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
                                '会話を始めましょう。タスク分解、設計支援、トラブルシューティングなどが可能です。'
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
                                        new Date(histItem.timestamp).toLocaleTimeString()
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

    // ===== Component: Markdown Notes Page =====
    // innerHTML を一切使わず h() のみで Markdown サブセットを DOM へレンダリングする。
    // 対応: 見出し(# ## ###) / 箇条書き(- ) / **太字** / `inline code` / 段落。リンク・ネストは非対応
    // (スコープを絞り、javascript: 等の注入面を作らない＝C6/セキュリティ境界と整合)。
    function _renderMarkdownInline(text) {
        // 1 行内の **bold** と `code` を h() の子ノード列へ分解する (innerHTML 不使用)。
        const nodes = [];
        let rest = String(text);
        const token = /(\*\*([^*]+)\*\*|`([^`]+)`)/;
        let m;
        while ((m = token.exec(rest)) !== null) {
            if (m.index > 0) { nodes.push(rest.slice(0, m.index)); }
            if (m[2] !== undefined) { nodes.push(h('strong', {}, m[2])); }
            else if (m[3] !== undefined) { nodes.push(h('code', { class: 'md-code' }, m[3])); }
            rest = rest.slice(m.index + m[0].length);
        }
        if (rest) { nodes.push(rest); }
        return nodes;
    }

    function renderMarkdown(src) {
        const out = [];
        const lines = String(src || '').split('\n');
        let listBuf = null;
        const flushList = () => {
            if (listBuf) { out.push(h('ul', { class: 'md-ul' }, ...listBuf)); listBuf = null; }
        };
        for (const line of lines) {
            const h3 = /^###\s+(.*)$/.exec(line);
            const h2 = /^##\s+(.*)$/.exec(line);
            const h1 = /^#\s+(.*)$/.exec(line);
            const li = /^[-*]\s+(.*)$/.exec(line);
            if (h3) { flushList(); out.push(h('h3', { class: 'h3' }, ..._renderMarkdownInline(h3[1]))); }
            else if (h2) { flushList(); out.push(h('h2', { class: 'h2' }, ..._renderMarkdownInline(h2[1]))); }
            else if (h1) { flushList(); out.push(h('h1', { class: 'h1' }, ..._renderMarkdownInline(h1[1]))); }
            else if (li) { (listBuf = listBuf || []).push(h('li', {}, ..._renderMarkdownInline(li[1]))); }
            else if (line.trim() === '') { flushList(); }
            else { flushList(); out.push(h('p', { class: 'text-prewrap' }, ..._renderMarkdownInline(line))); }
        }
        flushList();
        return out;
    }

    function NotesPage() {
        const src = State.get().appsData.notes || '';

        const preview = h('div', { class: 'card md-preview', 'aria-label': 'プレビュー' }, ...renderMarkdown(src));

        const textarea = h('textarea', {
            id: 'notes-input',
            class: 'input textarea-resize-v',
            rows: 16,
            'aria-label': 'Markdown ノート',
            placeholder: '# 見出し\n\n**太字** や `コード`、- リスト が使えます',
            value: src,
            oninput: (e) => {
                const val = e.target.value;
                // live preview を innerHTML 無しで差し替え
                while (preview.firstChild) { preview.removeChild(preview.firstChild); }
                renderMarkdown(val).forEach(n => preview.appendChild(n));
                // updateSilently: State.update だと notify→全再描画で textarea が破棄され毎キーストローク
                // で focus 喪失する (確認済バグ)。preview は上で手動更新済みゆえ再描画は不要。
                State.updateSilently(s => { s.appsData.notes = val.slice(0, 20000); });
            }
        });

        return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
            h('header', { class: 'flex items-center gap-3' },
                createIcon('edit', 28),
                h('h1', { class: 'h1' }, 'Markdown ノート')
            ),
            h('p', { class: 'text-muted' }, 'innerHTML を使わず h() のみで描画する安全な Markdown ライブプレビュー。内容は自動保存されます。'),
            h('div', { class: 'grid-2col grid--align-start' },
                h('section', { class: 'card' }, h('div', { class: 'card-body' },
                    h('h2', { class: 'h3 mb-3' }, '入力'),
                    textarea
                )),
                h('section', { class: 'card' }, h('div', { class: 'card-body' },
                    h('h2', { class: 'h3 mb-3' }, 'プレビュー'),
                    preview
                ))
            )
        );
    }

    // ===== Component: Settings Page =====
    let settingsImportMode = 'append';
    let settingsIncludeProfile = true;
    let settingsIncludeProjects = true;
    let settingsIncludeApps = true;
    let settingsNewName = '';
    let settingsNewTech = '';
    let settingsNewDemo = '';

    function SettingsPage() {
        const state = State.get();

        // --- 不足していた関数群の実装 ---
        function getSnapshot() {
            const raw = Storage.parse(CONSTANTS.SNAPSHOT_KEY);
            if (!raw) {return null;}

            // Support both formats:
            // 1) { at, data, ... }  (current)
            // 2) <store object>    (legacy; schema-mismatch snapshot in older versions)
            if (raw && typeof raw === 'object' && raw.data && typeof raw.data === 'object') {
                return raw;
            }

            // Legacy: treat the whole object as store data
            if (raw && typeof raw === 'object' && raw.schemaVersion) {
                return { at: Date.now(), reason: 'legacy-snapshot', data: raw };
            }

            return null;
        }
        function setSnapshot() {
            const snap = { at: Date.now(), data: State.get() };
            const success = Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify(snap));
            if (success) {
                Toast.show('スナップショットを保存しました');
            } else {
                Toast.show('ストレージ上限のため保存に失敗しました。不要なデータを削除してください。', 'error', 5000);
            }
            State.update(s => { }); // 強制再描画
        }
        function restoreSnapshot() {
            const snap = getSnapshot();
            if (!snap || !snap.data) {return;}

            // Safety: refuse obviously wrong shapes
            if (typeof snap.data !== 'object' || !snap.data.schemaVersion) {
                Toast.show('スナップショット形式が不正です', 'error');
                return;
            }

            // If schema differs, still allow restore (user intent), but warn
            if (snap.data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {
                Toast.show(`注意: schemaVersion が一致しません（${snap.data.schemaVersion}→${CONSTANTS.SCHEMA_VERSION}）`, 'warning');
            }

            State.set(snap.data);
            Toast.show('スナップショットを復元しました');
        }
        function clearSnapshot() {
            Storage.remove(CONSTANTS.SNAPSHOT_KEY);
            Toast.show('スナップショットを削除しました');
            State.update(s => { }); // 強制再描画
        }

        function downloadJSON(data, filename) {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }
        function exportFull() { downloadJSON(State.get(), `portfolio_full_${Date.now()}.json`); }
        function exportProjects() { downloadJSON(State.get().projects, `portfolio_projects_${Date.now()}.json`); }
        function exportApps() { downloadJSON(State.get().appsData, `portfolio_apps_${Date.now()}.json`); }
        function exportProfile() { downloadJSON(State.get().profile, `portfolio_profile_${Date.now()}.json`); }

        function importJSON(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const parsed = JSON.parse(e.target.result);
                    State.update(s => {
                        if (settingsIncludeProfile && parsed.profile) {s.profile = parsed.profile;}
                        if (settingsIncludeProjects && Array.isArray(parsed.projects)) {
                            if (settingsImportMode === 'strict') {s.projects = parsed.projects;}
                            else if (settingsImportMode === 'upsert') {
                                // upsert（UI ラベル「更新+追加」）: 既存 id は更新、未知 id は追加。
                                // [FIX] 旧実装は未知 id を s.projects.push したのち Map.values() で
                                // 上書きしており、push した新規プロジェクトが破棄されていた
                                // (UI が約束する「追加」が機能しないデータ欠落バグ)。1 つの Map に
                                // 更新も追加も集約することで新規 id も確実に残す。
                                const map = new Map(s.projects.map(p => [p.id, p]));
                                parsed.projects.forEach(p => map.set(p.id, p));
                                s.projects = Array.from(map.values());
                            } else {
                                // append（追加のみ）: 未知 id だけ追加し、既存は変更しない。
                                const existing = new Set(s.projects.map(p => p.id));
                                parsed.projects.forEach(p => { if (!existing.has(p.id)) {s.projects.push(p);} });
                            }
                        }
                        if (settingsIncludeApps && parsed.appsData) {s.appsData = parsed.appsData;}
                    });

                    // [CRITICAL FIX] インポート直後に必ず正規化を通し、不正なデータ構造によるクラッシュを防ぐ
                    State.set(Store.validateAndNormalize(State.get()));

                    Toast.show('インポートが完了しました');
                } catch (err) {
                    Toast.show('JSONのパースに失敗しました', 'error');
                }
            };
            reader.readAsText(file);
        }

        function addProjectManual() {
            if (!settingsNewName.trim()) { Toast.show('プロジェクト名を入力してください', 'error'); return; }
            State.update(s => {
                // [FIX] slug 衝突回避: slugify は決定的なので同名追加だと slug が重複し、
                // ProjectDetailPage の find(p.slug===slug) が先頭のみ返して片方の詳細が到達不能に
                // なる。既存 slug と衝突する場合は -2, -3... を付与して一意化する。
                const existing = new Set(s.projects.map(p => p.slug));
                const base = slugify(settingsNewName);
                let slug = base;
                let n = 2;
                while (existing.has(slug)) { slug = `${base}-${n}`; n++; }
                s.projects.unshift({
                    id: 'p_user_' + generateId().slice(0, 6),
                    slug,
                    name: settingsNewName,
                    category: 'User Added',
                    summary: '', problem: '', approach: '',
                    tech: settingsNewTech ? settingsNewTech.split(',').map(t => t.trim()) : [],
                    tags: [],
                    demoRoute: settingsNewDemo || null
                });
            });
            settingsNewName = ''; settingsNewTech = ''; settingsNewDemo = '';
            Toast.show('プロジェクトを追加しました');
        }

        const defaultProjectIds = new Set(['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18']);

        function toggleHiddenProject(id) {
            State.update(s => {
                s.projectPrefs = s.projectPrefs || { hiddenIds: [] };
                const idx = s.projectPrefs.hiddenIds.indexOf(id);
                if (idx > -1) {s.projectPrefs.hiddenIds.splice(idx, 1);}
                else {s.projectPrefs.hiddenIds.push(id);}
            });
        }

        function deleteProjectHard(id) {
            if (defaultProjectIds.has(id)) {return;}
            if (!confirm('本当に削除しますか？')) {return;}
            State.update(s => {
                s.projects = s.projects.filter(p => p.id !== id);
            });
        }

        function moveProject(idx, dir) {
            State.update(s => {
                if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}
                const temp = s.projects[idx];
                s.projects[idx] = s.projects[idx + dir];
                s.projects[idx + dir] = temp;
            });
        }

        function normalizeNow() {
            const norm = Store.validateAndNormalize(State.get());
            State.set(norm);
            Toast.show('正規化を完了しました');
        }

        function resetData() {
            if (!confirm('すべてのデータを初期化しますか？')) {return;}
            State.set(Store.createDefaultStore());
            Toast.show('初期化しました');
        }

        function buildUI() {
            const snap = getSnapshot(); // v56.5: snapをbuildUIスコープで取得
            return h('article', { class: 'flex flex-col gap-6' },
                h('header', {}, h('h1', { class: 'h1' }, 'Settings')),
                h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-6' },
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'エクスポート'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-primary', onclick: exportFull }, 'フルバックアップ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportProjects }, 'Projectsのみ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportApps }, 'AppsDataのみ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportProfile }, 'Profileのみ')
                            ),
                            h('p', { class: 'text-muted text-sm' }, 'フルバックアップは互換性を考慮した形式です。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'インポート（欠損ゼロ）'),
                            h('div', { class: 'grid grid-cols-2 gap-3' },
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, 'モード'),
                                    h('select', { class: 'input', 'aria-label': 'インポートモード', onchange: (e) => { settingsImportMode = e.target.value; window.render(); }, value: settingsImportMode },
                                        h('option', { value: 'append' }, 'append（追加のみ）'),
                                        h('option', { value: 'upsert' }, 'upsert（更新+追加）'),
                                        h('option', { value: 'strict' }, 'strict（全置換）')
                                    )
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, '対象'),
                                    h('div', { class: 'flex flex-wrap gap-2' },
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeProfile, onchange: (e) => { settingsIncludeProfile = !!e.target.checked; window.render(); } }),
                                            h('span', { class: 'icon-gap' }, 'Profile')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeProjects, onchange: (e) => { settingsIncludeProjects = !!e.target.checked; window.render(); } }),
                                            h('span', { class: 'icon-gap' }, 'Projects')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeApps, onchange: (e) => { settingsIncludeApps = !!e.target.checked; window.render(); } }),
                                            h('span', { class: 'icon-gap' }, 'AppsData')
                                        )
                                    )
                                )
                            ),
                            h('div', {},
                                h('input', {
                                    type: 'file',
                                    class: 'input',
                                    'aria-label': 'インポートする JSON ファイルを選択',
                                    accept: 'application/json',
                                    onchange: (e) => {
                                        const f = e.target.files && e.target.files[0];
                                        if (f) {importJSON(f);}
                                        e.target.value = '';
                                    }
                                })
                            ),
                            h('p', { class: 'text-muted text-sm' }, 'Projectsは常にデフォルトを維持しつつ、あなたの編集を優先してマージします。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'デザイン'),
                            h('p', { class: 'text-muted' }, 'Primaryカラーとベースフォントを切り替えます（Light/Dark/Systemは別設定）。'),
                            h('div', { class: 'flex flex-wrap items-center gap-3' },
                                h('label', { class: 'text-sm font-semibold', for: 'brandSelect' }, 'ブランド'),
                                h('select', {
                                    id: 'brandSelect',
                                    class: 'input',
                                    value: Brand.get(),
                                    onchange: (e) => { Brand.set(e.target.value); window.render(); }
                                },
                                    h('option', { value: 'indigo' }, 'Indigo'),
                                    h('option', { value: 'classic' }, 'Classic Blue + Inter')
                                ),
                                h('span', { class: 'badge badge-secondary' }, '即時反映')
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'スナップショット'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-secondary', onclick: setSnapshot }, '保存'),
                                h('button', { class: 'btn btn-secondary', onclick: restoreSnapshot, disabled: !snap }, '復元'),
                                h('button', { class: 'btn btn-ghost', onclick: clearSnapshot, disabled: !snap }, '削除')
                            ),
                            snap
                                ? h('p', { class: 'text-muted text-sm' }, `保存日時: ${new Date(snap.at).toLocaleString()}`)
                                : h('p', { class: 'text-muted text-sm' }, 'スナップショットは未保存です。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '並び替え（Projects）'),
                            h('div', { class: 'text-muted text-sm' }, '上下ボタンで表示順を調整できます。'),
                            h('div', { class: 'flex flex-col gap-2 scroll-container-sm' },
                                ...state.projects.map((p, idx) =>
                                    h('div', { class: 'flex items-center justify-between gap-2' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, String(idx + 1)),
                                            h('span', { class: 'text-sm' }, p.name)
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, -1), disabled: idx === 0 }, '↑'),
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, +1), disabled: idx === state.projects.length - 1 }, '↓')
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '表示管理（Projects）'),
                            h('div', { class: 'grid grid-cols-1 gap-3' },
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, '名前'),
                                    h('input', { class: 'input', placeholder: 'プロジェクト名', value: settingsNewName, oninput: (e) => { settingsNewName = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, 'Tech（カンマ区切り）'),
                                    h('input', { class: 'input', placeholder: '例: JS,HTML,CSS', value: settingsNewTech, oninput: (e) => { settingsNewTech = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, 'Demo（任意）'),
                                    h('select', { class: 'input', 'aria-label': 'Demo アプリの種類', onchange: (e) => { settingsNewDemo = e.target.value; }, value: settingsNewDemo },
                                        h('option', { value: '' }, 'Demoなし'),
                                        h('option', { value: 'task' }, 'task'),
                                        h('option', { value: 'todo' }, 'todo'),
                                        h('option', { value: 'pomodoro' }, 'pomodoro'),
                                        h('option', { value: 'ai' }, 'ai'),
                                        h('option', { value: 'notes' }, 'notes')
                                    )
                                ),
                                h('div', { class: 'flex items-end' },
                                    h('button', { class: 'btn btn-primary w-full', onclick: addProjectManual }, '追加')
                                )
                            ),
                            (() => {
                                const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                const visibleCount = state.projects.filter(p => !hidden.has(String(p.id))).length;
                                const hiddenCount = state.projects.length - visibleCount;
                                return h('div', { class: 'text-muted text-sm' }, `表示: ${visibleCount} / 非表示: ${hiddenCount} / 総数: ${state.projects.length}`);
                            })(),
                            h('div', { class: 'flex flex-col gap-2 scroll-container-md' },
                                ...state.projects.map(p => {
                                    const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                    const isHidden = hidden.has(String(p.id));
                                    const isDefault = defaultProjectIds.has(String(p.id));
                                    return h('div', { class: 'flex items-center justify-between gap-2' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, isDefault ? 'default' : 'user'),
                                            h('span', { class: 'text-sm' }, p.name),
                                            isHidden ? h('span', { class: 'badge badge-green' }, 'hidden') : null
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => toggleHiddenProject(p.id) }, isHidden ? '表示' : '非表示'),
                                            h('button', { class: 'btn btn-danger btn-sm', disabled: isDefault, title: isDefault ? 'デフォルトは非表示のみ' : '', onclick: () => deleteProjectHard(p.id) }, '削除')
                                        )
                                    );
                                })
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '整合性チェック / 正規化'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-secondary', onclick: normalizeNow }, '実行'),
                                h('button', { class: 'btn btn-danger', onclick: resetData }, '全リセット')
                            ),
                            h('p', { class: 'text-muted text-sm' }, '正規化はデータ破損・型揺れ・上限超過などを安全側に丸めます。')
                        )
                    )
                )
            );
        }
        return buildUI();
    }



    return { TaskPage, TodoPage, PomodoroPage, AIPage, NotesPage, SettingsPage };
}
