/**
 * js/theme.js — Theme manager factory (system / dark / light) — v80+ Stage 5-i extraction
 *
 * main.js の `Theme` IIFE モジュールを依存注入（factory pattern）で物理分割した葉モジュール。
 * Brand / Store / State と同じく、State / Toast への closure 依存を `createTheme` 関数の
 * 引数で受け取ることで、葉契約（Check 47c: import ゼロ）を維持しつつ Theme の挙動と公開 API
 * を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   { apply, cycle, init }
 *
 * 【依存（引数で注入）】
 *   - State: { get(), update(fn) }
 *   - Toast: { show(message, type?) }
 *
 * 【非破壊性】
 *   - document.documentElement の data-theme 属性と classList.toggle('dark', ...) の挙動不変
 *   - meta[name="theme-color"] の content 切替 (dark: '#0b0f19' / light: '#ffffff') は不変
 *   - cycle の遷移順 (system → dark → light → system) と Toast 文言は byte-equivalent
 *   - init での matchMedia('(prefers-color-scheme: dark)').addEventListener('change', ...) も
 *     不変（system 選択時のみ apply('system') 再呼び出し）
 *
 * 【副作用】
 *   - apply(theme): document.documentElement の DOM 副作用、meta theme-color の content 変更
 *   - init: window.matchMedia の change イベントリスナー登録
 *   - cycle: State.update() による永続化トリガと Toast.show による UI 通知
 */
export function createTheme({ State, Toast }) {
    function apply(theme) {
        document.documentElement.setAttribute('data-theme', theme);

        const isDark = theme === 'dark' ||
            (theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);

        document.documentElement.classList.toggle('dark', isDark);

        // Update meta theme-color
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            meta.content = isDark ? '#0b0f19' : '#ffffff';
        }
    }

    function cycle() {
        const current = State.get().theme;
        const next = current === 'system' ? 'dark' : current === 'dark' ? 'light' : 'system';
        State.update(s => s.theme = next);
        apply(next);
        Toast.show(`テーマ: ${next === 'system' ? 'システム設定' : next === 'dark' ? 'ダーク' : 'ライト'}`, 'info');
        return next;
    }

    function init() {
        apply(State.get().theme);

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
            if (State.get().theme === 'system') {
                apply('system');
            }
        });
    }

    return { apply, cycle, init };
}
