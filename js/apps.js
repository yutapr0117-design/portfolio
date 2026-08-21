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
 *   - h, createIcon, Toast, announce: js/ui-components.js (announce = sr-only 通知チャネルへの書き込み)
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
export function createApps({ h, createIcon, Toast, State, CONSTANTS, generateId, clamp, announce }) {
    // ===== Component: Apps Hub =====

    // ===== Component: Task App =====
    // [FIX] 揮発性クロージャ問題の解決：UIステートをコンポーネント外に保持
    // v80+ lint: 束縛自体は再代入されず .priority のプロパティ変異のみのため const が正しい。
    // NOTE: q フィールドは getFilteredTasks で参照されていたが、UI に対応 input が存在せず
    // q は常に '' のまま = !taskFilter.q は常に true = matchesQ は常に true = dead code。
    // git -S 'taskFilter.q' で UI イベントによる代入歴ゼロを確認後に除去。
    const taskFilter = { priority: 'all' };

    // TaskPage の絞り込み。render / 部分再描画 / 件数アナウンスの複数箇所から使うため factory
    // スコープに置く (TaskPage 内に置くと外から参照できず no-undef になる — getFilteredTodos と同じ)。
    function getFilteredTasks() {
        return State.get().appsData.tasks.filter(t =>
            taskFilter.priority === 'all' || t.priority === taskFilter.priority
        );
    }

    function taskFilterStatusText() {
        const label = ({ all: '全て', high: 'High', med: 'Med', low: 'Low' })[taskFilter.priority] || taskFilter.priority;
        return `優先度: ${label} ${getFilteredTasks().length} 件`;
    }

    // listHost の中だけを作り直す関数。buildUI が描画のたびに新しい host を掴んで再代入する。
    let renderTaskList = () => {};

    function TaskPage() {

        // 追加できたら true。呼び出し側は false のとき入力欄を復元する (下の onkeydown を参照)。
        function addTask(title) {
            if (!title.trim()) {return false;}
            // [FIX] 上限時は断る。従来は unshift 後の正規化 slice(0, MAX) が
            //   **最古のタスクを無通知で捨てていた**（実測 2026-08-18）。詳細は apps-task.spec.js。
            if (State.get().appsData.tasks.length >= CONSTANTS.LIMITS.MAX_TASKS) {
                Toast.show(`タスクは ${CONSTANTS.LIMITS.MAX_TASKS} 件までです。不要なタスクを削除してください`, 'error');
                return false;
            }
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
            return true;
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

        // [A11Y 4.1.3] ステータス移動は **視覚では分かるが SR には無音**だった。カードが別の列へ
        //   動くだけで、ボタンのアクセシブル名 (「次のステータスへ進める：<タスク名>」) は
        //   変わらないため、SR 利用者には **クリックが効いたのかどうかも分からない**。
        //   実測 (2026-08-17): 追加・削除は Toast 経由で通知されるのに、移動だけ
        //   `#action-announcement` が空のままだった (4 操作中 2 つが無音という非対称)。
        //   Toast (視覚ポップアップ) ではなく `announce()` を直接使うのは、**移動は頻繁な操作**で
        //   毎回ポップアップを出すと視覚利用者に煩わしいから。announce は sr-only の
        //   唯一の通知チャネルで、「視覚では分かるが SR には無音」な状態変化を流す用途
        //   (js/ui-components.js の docstring どおり・Check 407 が単一 writer を強制)。
        const TASK_STATUS_LABEL = { 'backlog': '未着手', 'in-progress': '進行中', 'done': '完了' };

        function moveStatus(task, direction) {
            const statuses = ['backlog', 'in-progress', 'done'];
            const idx = statuses.indexOf(task.status);
            const newIdx = clamp(idx + direction, 0, statuses.length - 1);
            if (newIdx !== idx) {
                const next = statuses[newIdx];
                updateTask(task.id, { status: next });
                announce(`「${task.title}」を${TASK_STATUS_LABEL[next]}へ移動しました`);
            }
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
                        // [A11Y 3.3.2/4.1.2] placeholder は入力開始で消え SR が accessible name として
                        // 一貫して読まないため、恒久的な aria-label を付与する (可視ラベル無しデザイン維持)。
                        'aria-label': '新しいタスクを入力',
                        enterkeyhint: 'done',
                        // [DATA] 保存側 (addTask) と同じ定数を UI 上限にし、入力できた文字数と保存
                        // される文字数を一致させる。無いと超過分が黙って捨てられる (Check 410)。
                        maxlength: CONSTANTS.LIMITS.TASK_TITLE,
                        placeholder: '新しいタスクを入力...',
                        onkeydown: (e) => {
                            // [FIX] IME 変換確定の Enter (e.isComposing) では追加しない。日本語入力で
                            // 変換候補を Enter 確定した際に未確定文字が誤ってタスク化される footgun を防ぐ
                            // (todo 入力の todoComposing ガードと同等の保護を task 入力にも付与)。
                            if (e.key === 'Enter' && !e.isComposing) {
                                // [FIX] **値を読んだら同期でクリアする**。入力欄が空になるのは
                                //   再描画の副作用だが、その再描画は非同期 (await yieldToMain) なので、
                                //   Enter を続けて押す / 押しっぱなしでキーリピートが走ると
                                //   **同じ値が何度も登録される** (実測: 3 回押して 3 件の同名タスク)。
                                //   空文字は addTask の空ガードが弾くので、2 回目以降は無害になる。
                                // [FIX] **追加できたときだけ**消す。従来は無条件にクリアしてから
                                //   addTask を呼んでいたため、上限 (MAX_TASKS) に達していると
                                //   「不要なタスクを削除してください」と言われた時点で
                                //   **打ったタスク名が既に失われていた** (実測: 500 件の状態で
                                //   Enter → toast は出るが入力欄は空)。断られた側は打ち直しになる。
                                const _v = e.target.value;
                                e.target.value = '';
                                if (!addTask(_v)) { e.target.value = _v; }
                                // 全体再描画の直後にフォーカスを復元し、連続入力を可能にする
                                setTimeout(() => document.getElementById('task-input')?.focus(), 0);
                            }
                        }
                    }),
                    h('select', {
                        class: 'input',
                        // [A11Y 2.1.1] id は「再描画で消えた後に focus を戻す」ための安定ハンドル
                        //   (main.js _renderCore が _restoreFocusId で復元する)。id が無いと
                        //   絞り込みを変えるたび focus が body へ落ち、キーボード操作が続かない。
                        id: 'task-filter-priority',
                        'aria-label': '優先度で絞り込み',
                        onchange: (e) => {
                            taskFilter.priority = e.target.value;
                            // [FIX] 絞り込みは **表示だけの操作** なので全再描画しない。window.render() は
                            //   #content を作り直すため、その巻き添えで **「新しいタスク」に打ちかけた
                            //   未送信テキストが消えていた** (実測: 8 文字 → 0)。絞り込んで確認してから
                            //   続きを打つのは自然な操作なので実害が大きい。#982 (テーマ切替が入力を消した)
                            //   / #258 (oninput の全再描画) と同じ「無関係な操作の巻き添え」class。
                            //   ProjectsPage / QuizPage が既に採る listHost + 手動再描画へ揃える。
                            renderTaskList();
                        }
                    },
                        h('option', { value: 'all', text: '優先度: 全て', selected: taskFilter.priority === 'all' ? true : undefined }),
                        h('option', { value: 'high', text: 'High', selected: taskFilter.priority === 'high' ? true : undefined }),
                        h('option', { value: 'med', text: 'Med', selected: taskFilter.priority === 'med' ? true : undefined }),
                        h('option', { value: 'low', text: 'Low', selected: taskFilter.priority === 'low' ? true : undefined })
                    ),
                    // [A11Y 4.1.3 Status Messages] 件数は **polite** な status で伝える。
                    //   従来は announce() 経由で `#action-announcement` (aria-live="assertive") へ
                    //   書いていたため、絞り込むたびにスクリーンリーダーの読み上げを**割り込んで**いた。
                    //   assertive は緊急 (エラー等) に限るのが ARIA APG の作法で、件数は status。
                    //   ProjectsPage / QuizPage は既に polite なローカル status を持っており、
                    //   task/todo だけ assertive という非対称だった (実測 #1031)。
                    //   描画のたびに文言が変わることで通知されるので、命令的な announce は不要。
                    //   sr-only ゆえ視覚描画は不変。
                    h('div', { class: 'sr-only', role: 'status', 'aria-live': 'polite', id: 'task-filter-status' },
                        taskFilterStatusText())
                )
            ));

            // Kanban。絞り込みで作り直すのは **この listHost の中と件数 status だけ**。
            const listHost = h('div', { id: 'task-list-host' });
            container.appendChild(listHost);
            renderTaskList = function () {
            while (listHost.firstChild) { listHost.removeChild(listHost.firstChild); }
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
                                            // [A11Y 4.1.2] 全タスクで同一名だと SR はどのタスクを削除するか
                                            //   区別できない。task.title を accessible name に含め一意化する。
                                            // [A11Y 2.1.1] 削除ボタンは自分自身を消すので同じ id は
                                            //   二度と現れない。それでも id を付けるのは、main.js
                                            //   _renderCore の復元が **id を持っていた要素だけ**を対象に
                                            //   するから (opt-in)。id があると「復元先が消えていた」経路に
                                            //   入り、少なくとも #content の h1 へ戻る。
                                            id: 'task-delete-' + task.id,
                                            'aria-label': 'タスクを削除：' + task.title,
                                            onclick: () => deleteTask(task.id)
                                        }, createIcon('trash', 14))
                                    ),
                                    h('div', { class: 'flex items-center justify-between' },
                                        h('select', {
                                            class: 'input btn-sm',
                                            // [A11Y 2.1.1] 再描画後の focus 復元用 (main.js _renderCore)。
                                            //   カード毎に一意にするため task.id を含める。
                                            id: 'task-priority-' + task.id,
                                            // [A11Y 4.1.2] task.title を含め、どのタスクの優先度セレクトか一意化。
                                            'aria-label': 'タスクの優先度：' + task.title,
                                            style: 'width:auto;padding:0.25rem 0.5rem;font-size:0.75rem;',
                                            onchange: (e) => updateTask(task.id, { priority: e.target.value })
                                        },
                                            h('option', { value: 'high', text: 'High', selected: task.priority === 'high' ? true : undefined }),
                                            h('option', { value: 'med', text: 'Med', selected: task.priority === 'med' ? true : undefined }),
                                            h('option', { value: 'low', text: 'Low', selected: task.priority === 'low' ? true : undefined })
                                        ),
                                        h('div', { class: 'flex gap-1' },
                                            // [A11Y] 矢印グリフのみだと SR には「← ボタン」としか聞こえず、
                                            //   タスクをステータス間で移動する目的が不明 (WCAG 2.4.4/4.1.2)。
                                            //   移動先の方向 + task.title を aria-label で明示し一意化する。
                                            h('button', {
                                                class: 'btn btn-ghost btn-sm',
                                                // [A11Y 2.1.1] 再描画後の focus 復元用 (main.js _renderCore)。
                                                //   これが無いとステータスを 1 つ動かすたび focus が body へ
                                                //   落ち、backlog→進行中→done と続けて動かせない。
                                                id: 'task-move-prev-' + task.id,
                                                'aria-label': '前のステータスへ戻す：' + task.title,
                                                disabled: task.status === 'backlog',
                                                onclick: () => moveStatus(task, -1)
                                            }, h('span', { 'aria-hidden': 'true' }, '←')),
                                            h('button', {
                                                class: 'btn btn-ghost btn-sm',
                                                id: 'task-move-next-' + task.id,
                                                'aria-label': '次のステータスへ進める：' + task.title,
                                                disabled: task.status === 'done',
                                                onclick: () => moveStatus(task, 1)
                                            }, h('span', { 'aria-hidden': 'true' }, '→'))
                                        )
                                    )
                                )
                            )
                        )
                    )
                );
                board.appendChild(column);
            });

            listHost.appendChild(board);

            // [UX] 0 件のときは理由まで示す。従来は 3 列とも「0」が並ぶだけで、**フィルタが
            //   隠しているのか本当に空なのか判別できなかった** (TodoPage は同じ状況で
            //   「TODOはありません。」を出しており、task 側だけ欠けていた非対称)。
            //   フィルタ由来なら解除すれば戻ると判るよう文言を分ける。role=status は付けない —
            //   フィルタ変更時の件数は announceFilter が単一チャネルへ通知済みで、ここに live
            //   region を足すと二重読み上げになる (#901 と同 class)。
            if (allTasks.length === 0) {
                listHost.appendChild(h('p', {
                    class: 'text-muted text-center py-8'
                }, taskFilter.priority === 'all'
                    ? 'タスクはありません。上の入力欄から追加できます。'
                    : 'この優先度に一致するタスクはありません。絞り込みを「優先度: 全て」に戻すと表示されます。'));
            }
            // 全再描画をやめた分、件数の polite status は明示的に更新する。
            const statusEl = container.querySelector('#task-filter-status');
            if (statusEl) { statusEl.textContent = taskFilterStatusText(); }
            };
            renderTaskList();
            return container;
        }

        return buildUI();
    }

    // ===== Component: Todo App =====
    // [FIX] 揮発性クロージャ問題の解決
    let todoFilter = 'all';

    // TodoPage の絞り込み。render と filter onchange (件数アナウンス) の両方から使うため factory
    // スコープに置く (TaskPage 内に置くと TodoPage から参照できず no-undef になる — ESLint が検出)。
    function getFilteredTodos() {
        return State.get().appsData.todos.filter(t => {
            if (todoFilter === 'active') {return !t.completed;}
            if (todoFilter === 'completed') {return t.completed;}
            return true;
        });
    }

    let todoComposing = false;

    function todoFilterStatusText() {
        const label = ({ all: '全て', active: '未完了', completed: '完了' })[todoFilter] || todoFilter;
        return `TODO: ${label} ${getFilteredTodos().length} 件`;
    }

    // listHost の中だけを作り直す関数 (TaskPage の renderTaskList と同じ形)。
    let renderTodoList = () => {};
    let todoListHost = null;

    function TodoPage() {

        // 追加できたら true (addTask と同契約)。
        function addTodo(text) {
            if (!text.trim()) {return false;}
            // [FIX] task の addTask と同じ理由で上限時は断る（正規化が最古を無通知で落とす）。
            if (State.get().appsData.todos.length >= CONSTANTS.LIMITS.MAX_TODOS) {
                Toast.show(`TODO は ${CONSTANTS.LIMITS.MAX_TODOS} 件までです。不要な TODO を削除してください`, 'error');
                return false;
            }
            State.update(s => {
                s.appsData.todos.unshift({
                    id: generateId(),
                    text: text.trim().slice(0, CONSTANTS.LIMITS.TODO_TEXT),
                    completed: false,
                    createdAt: Date.now(),
                    dueDate: null
                });
            });
            // [A11Y 4.1.3] task の addTask と対称に完了通知を出す。従来 todo の add/delete だけ Toast が
            //   欠落し、SR ユーザーに追加成功が伝わらず (Toast は #action-announcement へ書き込むため無通知)、
            //   視覚フィードバックも task と非対称だった (「1 ケースだけ処理・他を忘れる」asymmetry)。
            Toast.show('TODOを追加しました', 'success');
            return true;
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
            // [A11Y 4.1.3] deleteTask と対称に削除完了を通知 (上記 addTodo と同じ asymmetry 是正)。
            Toast.show('TODOを削除しました', 'success');
        }

        function clearCompleted() {
            State.update(s => {
                s.appsData.todos = s.appsData.todos.filter(t => !t.completed);
            });
            Toast.show('完了済みを削除しました', 'success');
        }

        const todos = State.get().appsData.todos;
        const filtered = getFilteredTodos();

        // [FIX] TodoPage のルートに紛れ込んでいた ErrorBoundary/FatalPage 用の a11y 属性群を除去。
        // 通常の ToDo アプリなのに role="alert" / aria-invalid="true" / aria-errormessage="fallback-details"
        // / class="error-boundary-fallback" / aria-description="…unstable state transition" を持っており
        // (copy-paste leak・実 FatalPage ですら error-boundary-fallback を使っておらず本箇所のみに存在)、
        // スクリーンリーダーが ToDo ページ全体を「エラーアラート・invalid」として読み上げ、
        // aria-errormessage は TodoPage に存在しない #fallback-details を指す dangling 参照だった。
        // レイアウト class のみ残し a11y セマンティクスを正常化する (視覚描画は不変)。
        renderTodoList = function () {
            if (!todoListHost) { return; }
            while (todoListHost.firstChild) { todoListHost.removeChild(todoListHost.firstChild); }
            const list = getFilteredTodos();
            list.forEach(todo => todoListHost.appendChild(buildTodoItem(todo)));
            if (list.length === 0) {
                todoListHost.appendChild(h('p', { class: 'text-muted text-center py-8' }, 'TODOはありません。'));
            }
            const statusEl = document.getElementById('todo-filter-status');
            if (statusEl) { statusEl.textContent = todoFilterStatusText(); }
        };

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
                        // [A11Y 3.3.2/4.1.2] placeholder-only を避け恒久 accessible name を付与。
                        'aria-label': 'やることを入力',
                        enterkeyhint: 'done',
                        // [DATA] addTodo の LIMITS.TODO_TEXT slice と UI 上限を一致させる (Check 410)。
                        maxlength: CONSTANTS.LIMITS.TODO_TEXT,
                        placeholder: '入力してEnter（IME対応）...',
                        oncompositionstart: () => todoComposing = true,
                        oncompositionend: () => todoComposing = false,
                        onkeydown: (e) => {
                            if (e.key === 'Enter' && !todoComposing) {
                                // [FIX] task 側と同じ理由で同期クリアする (連打・キーリピートでの二重登録防止)。
                                // [FIX] task 側と同じく **追加できたときだけ**消す (上限時の入力消失)。
                                const _v = e.target.value;
                                e.target.value = '';
                                if (!addTodo(_v)) { e.target.value = _v; }
                                // 全体再描画の直後にフォーカスを復元
                                setTimeout(() => document.getElementById('todo-input')?.focus(), 0);
                            }
                        }
                    }),
                    h('div', { class: 'flex gap-2 mt-4' },
                        h('select', {
                            class: 'input w-auto',
                            // [A11Y 2.1.1] 再描画後の focus 復元用 (main.js _renderCore)。
                            id: 'todo-filter',
                            'aria-label': 'TODO を絞り込み',
                            onchange: (e) => {
                                todoFilter = e.target.value;
                                // [FIX] task 側と同じ理由で全再描画しない。絞り込みは表示だけの操作なのに
                                //   window.render() が #content を作り直し、**「新しい Todo」に打ちかけた
                                //   未送信テキストが消えていた**。片方だけ直すと「1 ケースだけ処理して他を
                                //   忘れる」非対称になるので task と対で直す。
                                renderTodoList();
                            }
                        },
                            h('option', { value: 'all', text: '全て', selected: todoFilter === 'all' ? true : undefined }),
                            h('option', { value: 'active', text: '未完了', selected: todoFilter === 'active' ? true : undefined }),
                            h('option', { value: 'completed', text: '完了', selected: todoFilter === 'completed' ? true : undefined })
                        ),
                        // [A11Y 4.1.3] 件数は polite な status で伝える (task 側のコメント参照・sr-only)。
                        h('div', { class: 'sr-only', role: 'status', 'aria-live': 'polite', id: 'todo-filter-status' },
                            todoFilterStatusText()),
                        h('button', {
                            class: 'btn btn-secondary btn-sm',
                            // [A11Y 2.1.1] 押すと自身が disabled になるので復元は h1 へ落ちる (opt-in の id)。
                            id: 'todo-clear-completed',
                            disabled: !todos.some(t => t.completed),
                            onclick: clearCompleted
                        }, '完了済み削除')
                    )
                )
            ),

            todoListHost = h('section', { class: 'flex flex-col gap-2', id: 'todo-list-host' },
                ...filtered.map(todo => buildTodoItem(todo)),
                filtered.length === 0 && h('p', { class: 'text-muted text-center py-8' }, 'TODOはありません。')
            )
        );

        // 1 項目分のテンプレ。初回描画と部分再描画の両方から使う (複製すると drift する)。
        // 関数宣言ゆえ hoist され、上の return 式から呼べる。
        function buildTodoItem(todo) {
            return h('article', { class: 'card' },
                        h('div', { class: 'card-body flex items-center gap-3' },
                            h('input', {
                                type: 'checkbox',
                                checked: todo.completed,
                                // [A11Y 2.1.1] 再描画後の focus 復元用 (main.js _renderCore)。項目毎に一意。
                                //   これが無いと 1 件チェックするたび focus が body へ落ち、
                                //   次の項目を Space で続けてチェックできない。
                                id: 'todo-check-' + todo.id,
                                onchange: () => toggleTodo(todo.id),
                                // [A11Y 4.1.2] 各項目の checkbox が全項目で同一名 (「完了にする」) だと
                                //   SR ユーザーはリスト内でどの項目を操作するか区別できない。todo.text を
                                //   accessible name に含め「『牛乳を買う』を完了にする」のように一意化する。
                                'aria-label': (todo.completed ? '未完了に戻す' : '完了にする') + '：' + todo.text
                            }),
                            h('span', {
                                class: ['flex-1', todo.completed && 'text-muted'],
                                style: todo.completed ? 'text-decoration:line-through;opacity:0.6;' : undefined
                            }, todo.text),
                            h('button', {
                                class: 'icon-btn',
                                // [A11Y 2.1.1] 削除で消える要素にも id を付ける理由は task 側のコメント参照。
                                id: 'todo-delete-' + todo.id,
                                onclick: () => deleteTodo(todo.id),
                                // [A11Y 4.1.2] 削除ボタンも todo.text で一意化 (全項目「削除」だと区別不能)。
                                'aria-label': '削除：' + todo.text
                            }, createIcon('x', 16))
                        )
                    );
        }
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
        // note ごとに「最初に使われた見出しレベル」を基準にする (下の [FIX] 参照)。
        let _mdBase = null;
        let listBuf = null;
        const flushList = () => {
            if (listBuf) { out.push(h('ul', { class: 'md-ul' }, ...listBuf)); listBuf = null; }
        };
        for (const line of lines) {
            const h3 = /^###\s+(.*)$/.exec(line);
            const h2 = /^##\s+(.*)$/.exec(line);
            const h1 = /^#\s+(.*)$/.exec(line);
            const li = /^[-*]\s+(.*)$/.exec(line);
            // [FIX] Markdown 見出しは要素レベルを 2 段 demote する (# → h3, ## → h4, ### → h5)。
            //   preview はページ h1「Markdown ノート」→ セクション h2「プレビュー」の配下にあるため、
            //   ユーザー note の `#` を <h1> で描画すると (1) ページに h1 が 2 個 (default note が
            //   "# メモ" で始まるため out-of-the-box で発生) になり (2) h2「プレビュー」内に page-level
            //   h1 が現れて見出し階層が document 構造を誤表現する (WCAG 1.3.1・SR の見出しナビを混乱)。
            //   視覚サイズは 'h1'/'h2'/'h3' class 維持で不変 (render-neutral)。要素だけ h3/h4/h5 へ
            //   降格し preview の h2 配下に正しく nest させる。
            if (h3 || h2 || h1) {
                flushList();
                const _md = h1 ? 1 : h2 ? 2 : 3;
                // [FIX] **固定 2 段 demote では見出しが飛ぶ。** 従来は # → h3 / ## → h4 / ### → h5 と
                //   絶対対応させていたため、`###` から書き始めた note では preview の h2 の直後に
                //   **h5 が来て h3/h4 を飛ばす** (WCAG 1.3.1)。実測 (2026-08-20): `### 設計メモ` だけの
                //   note で axe の heading-order が 1 件違反を出す。`###` から書き始めるのは
                //   珍しくないので、既定 note が `#` で始まる出荷状態だけが偶然 clean だった。
                //   note 内で **最初に使われたレベルを h3 に対応づけ**、以降は相対差で下げる。
                //   飛びは note 側の構造 (### → ##### 等) を反映する分だけに限られ、
                //   preview の h2 との接続は常に h3 になる。視覚サイズは class 維持で不変。
                if (_mdBase === null) { _mdBase = _md; }
                const _lvl = Math.min(6, 3 + Math.max(0, _md - _mdBase));
                const _cls = _md === 1 ? 'h1' : _md === 2 ? 'h2' : 'h3';
                const _txt = (h1 || h2 || h3)[1];
                out.push(h('h' + _lvl, { class: _cls }, ..._renderMarkdownInline(_txt)));
            }
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
            // [DATA] 本 class で唯一 silent だった面: maxlength が無いと超過分は画面にもプレビューにも
            // 表示され続けたまま保存だけされず、リロードで初めて消失が判明した (Check 410)。
            maxlength: CONSTANTS.LIMITS.NOTES_TEXT,
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
