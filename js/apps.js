/**
 * js/apps.js — Productivity Apps (TaskPage / TodoPage / NotesPage)
 * — v80+ Stage 5-n extraction via factory pattern
 * (v80+ bloat-reduction 2026-07-04 — AIPage を js/ai-page.js / PomodoroPage を
 *  js/pomodoro-page.js へ分離。2026-07-05 — SettingsPage を js/settings-page.js へ分離し
 *  837→461 行へ縮小 = Check 363 の 1,000 行ハード上限への headroom 確保)
 *
 * main.js の Apps Component 関数と関連 closure state を依存注入で
 * 物理分割した葉モジュール。Brand / Store / State / Theme / Meta Management /
 * Components と同じく、すべての closure 依存を `createApps` 関数の引数で受け取る
 * ことで、葉契約 (Check 47c: import ゼロ) を維持しつつ各関数の挙動と公開 API を
 * 完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const { TaskPage, TodoPage, NotesPage } = createApps({...});
 *   (AIPage は js/ai-page.js の createAIPage / PomodoroPage は js/pomodoro-page.js の
 *    createPomodoroPage / SettingsPage は js/settings-page.js の createSettingsPage で別途生成)
 *
 * 【factory closure 内の private state（揮発性 UI 状態の維持）】
 *   - taskFilter (const, priority のみ — q フィールドは UI 入力未配線だったため除去), todoFilter / todoComposing (let)
 *   (settings* は SettingsPage と共に js/settings-page.js へ移動した)
 *
 * これらは元 main.js IIFE 内の関数外宣言で、各 Page 関数の再呼出間で状態を保持していた。
 * factory closure 内に同じ位置で declare することで、抽出前後の挙動は byte-equivalent。
 *
 * 【依存（引数で注入）】
 *   - h, createIcon, Toast: js/ui-components.js
 *   - State: js/state.js factory instance
 *   - CONSTANTS: js/constants.js
 *   - generateId, clamp: js/pure-utils.js
 *   (Brand / Store / Storage / slugify は SettingsPage 分離後 createApps 本体で未使用になった
 *    ため除去した。settings-page.js が自前の createSettingsPage で受け取る。AUTHOR / Router /
 *    Theme も AIPage / PomodoroPage 分離時に同様に除去済)
 *   - window グローバル経由: render (window.render として後段で代入される)
 *
 * 【非破壊性】
 *   - 抽出時は各関数の DOM 出力・class 名・style・aria 属性が byte-equivalent。bug-fix で各種挙動を
 *     精緻化済（IME ガード #151/152 / slug 衝突 #154 等）。SettingsPage 系 fix (#192/#294/#561) は
 *     js/settings-page.js へ移動。
 *   - localStorage への副作用順序（State.update 経由）も不変
 *   - AIDK Kernel / AIO 正本層には影響しない
 */
export function createApps({ h, createIcon, Toast, State, CONSTANTS, generateId, clamp }) {
    // ===== Component: Apps Hub =====

    // ===== Component: Task App =====
    // [FIX] 揮発性クロージャ問題の解決：UIステートをコンポーネント外に保持
    // v80+ lint: 束縛自体は再代入されず .priority のプロパティ変異のみのため const が正しい。
    // NOTE: q フィールドは getFilteredTasks で参照されていたが、UI に対応 input が存在せず
    // q は常に '' のまま = !taskFilter.q は常に true = matchesQ は常に true = dead code。
    // git -S 'taskFilter.q' で UI イベントによる代入歴ゼロを確認後に除去。
    const taskFilter = { priority: 'all' };

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
            return State.get().appsData.tasks.filter(t =>
                taskFilter.priority === 'all' || t.priority === taskFilter.priority
            );
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
                        onchange: (e) => {
                            taskFilter.priority = e.target.value;
                            window.render(); // グローバルレンダーを呼び出し
                        }
                    },
                        h('option', { value: 'all', text: '優先度: 全て', selected: taskFilter.priority === 'all' ? true : undefined }),
                        h('option', { value: 'high', text: 'High', selected: taskFilter.priority === 'high' ? true : undefined }),
                        h('option', { value: 'med', text: 'Med', selected: taskFilter.priority === 'med' ? true : undefined }),
                        h('option', { value: 'low', text: 'Low', selected: taskFilter.priority === 'low' ? true : undefined })
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
                                            onchange: (e) => updateTask(task.id, { priority: e.target.value })
                                        },
                                            h('option', { value: 'high', text: 'High', selected: task.priority === 'high' ? true : undefined }),
                                            h('option', { value: 'med', text: 'Med', selected: task.priority === 'med' ? true : undefined }),
                                            h('option', { value: 'low', text: 'Low', selected: task.priority === 'low' ? true : undefined })
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

        // [FIX] TodoPage のルートに紛れ込んでいた ErrorBoundary/FatalPage 用の a11y 属性群を除去。
        // 通常の ToDo アプリなのに role="alert" / aria-invalid="true" / aria-errormessage="fallback-details"
        // / class="error-boundary-fallback" / aria-description="…unstable state transition" を持っており
        // (copy-paste leak・実 FatalPage ですら error-boundary-fallback を使っておらず本箇所のみに存在)、
        // スクリーンリーダーが ToDo ページ全体を「エラーアラート・invalid」として読み上げ、
        // aria-errormessage は TodoPage に存在しない #fallback-details を指す dangling 参照だった。
        // レイアウト class のみ残し a11y セマンティクスを正常化する (視覚描画は不変)。
        return h('div', { class: 'flex flex-col gap-4 max-w-2xl' },
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
                            onchange: (e) => { todoFilter = e.target.value; window.render(); }
                        },
                            h('option', { value: 'all', text: '全て', selected: todoFilter === 'all' ? true : undefined }),
                            h('option', { value: 'active', text: '未完了', selected: todoFilter === 'active' ? true : undefined }),
                            h('option', { value: 'completed', text: '完了', selected: todoFilter === 'completed' ? true : undefined })
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

    // ▼ PomodoroPage (ポモドーロタイマー) は肥大化解消のため js/pomodoro-page.js
    //   (createPomodoroPage factory) へ分離した (2026-07-04)。private state は pomodoroTimer
    //   (interval id) 1 個で自己完結。stale-closure 対策 (#121/#134) と reload auto-resume は
    //   移設後も維持。main.js が createPomodoroPage で生成し合成する。挙動は byte-equivalent。

    // ▼ AIPage (AI アシスト・ローカル版) は肥大化解消のため js/ai-page.js
    //   (createAIPage factory) へ分離した (2026-07-04)。private state は aiLoading 1 個で
    //   local helper (analyzeInput / generateResponse) と共に完全自己完結ゆえ最も安全な抽出単位。
    //   main.js が createAIPage で生成し合成する。挙動は byte-equivalent。

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
                State.updateSilently(s => { s.appsData.notes = val.slice(0, CONSTANTS.LIMITS.NOTES_TEXT); });
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

    return { TaskPage, TodoPage, NotesPage };
}
