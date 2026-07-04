/**
 * js/pomodoro-page.js — PomodoroPage (ポモドーロタイマー) 葉モジュール
 * (v80+ bloat-reduction extraction via factory pattern — js/apps.js から分離)
 *
 * 【背景】
 * js/apps.js は複数の app ページ + private state を 1 ファイルに抱え肥大化していた
 * (1000 行しきい値超)。PomodoroPage は private state が `pomodoroTimer` (interval id) 1 個で
 * local helper (formatTime / getDuration / getRemaining / start / pause / reset / complete /
 * switchMode / startTimer / stopTimer / buildUI) と共に自己完結する。別葉モジュールへ分離。
 * 挙動 byte-equivalent。
 *
 * 【公開 API（呼び出し側 main.js から見た形）】
 *   const { PomodoroPage } = createPomodoroPage({ h, createIcon, State, Router, Toast, clamp });
 *
 * 【依存（引数で注入）】
 *   - h: DOM builder (js/ui-components.js)
 *   - createIcon: SVG アイコン生成 (js/ui-components.js)
 *   - State: アプリ状態ストア (js/state.js) — appsData.pomodoro (settings / runtime / history)
 *   - Router: hash router (js/router.js) — getRoute().name で稼働中ルート判定
 *   - Toast: 通知 (セッション完了)
 *   - clamp: 数値クランプ (設定分の範囲制限)
 *   - window.render / Date / setInterval / clearInterval: グローバル
 *
 * 【非破壊性 / 過去修正の温存】
 *   - stale-closure 対策 (#121/#134): getRemaining / getDuration は必ず State.get() で live
 *     state を読む (start() 時 closure に固定された古い runtime/settings を読まない)。
 *   - reload auto-resume (#): isActive かつ pomodoroTimer 不在時のみ startTimer で resume
 *     (稼働中の毎秒再描画では二重 interval にならない)。
 *   - 関数本体は抽出元から byte-equivalent。葉契約 (Check 47c: import ゼロ) を維持。
 */
export function createPomodoroPage({ h, createIcon, State, Router, Toast, clamp }) {

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

    return { PomodoroPage };
}
