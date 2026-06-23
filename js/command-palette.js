/**
 * js/command-palette.js — Command palette (Cmd/Ctrl+K quick navigation overlay)
 *
 * @fileoverview キーボード駆動の横断ナビゲーション overlay。Cmd/Ctrl+K で開き、入力で
 * 行き先を絞り込み、↑↓ で選択・Enter で遷移・Esc/背景クリックで閉じる。新ルートは追加せず
 * 既存 Router.navigate を呼ぶだけの純追加機能（route cascade 無し）。overlay DOM は初回 open 時に
 * 動的生成して body へ append する（index.html を変更しない）。
 *
 * 【公開 API（main.js から合成）】
 *   const CommandPalette = createCommandPalette({ Router, h, createIcon });
 *   CommandPalette.init();   // global Cmd/Ctrl+K keydown を登録
 *
 * 【依存（引数で注入）】
 *   - Router: js/router.js（navigate(hash) で遷移）
 *   - h: js/ui-components.js（型安全 DOM ビルダー）
 *   - createIcon: js/ui-components.js（SVG アイコン）
 *   - State: js/state.js factory instance（open 時に現在のプロジェクト一覧を検索対象へ加える）
 *
 * 【不変条件】
 *   - 本モジュールは葉（ローカル ESM import ゼロ。Check 47c）。
 *   - 既存の global keydown（main.js の Escape / aidk-rails）と非衝突: 本 module は
 *     `(meta|ctrl)+k` のみを横取りし preventDefault、それ以外は素通し。
 *   - 開いている間だけ focus を overlay 内に trap し、閉じたら直前 focus を復元する。
 *   - DOM 副作用は body 末尾の #command-palette-host に限定（render の #content には触れない）。
 */
export function createCommandPalette({ Router, h, createIcon, State }) {
    // 横断ナビの固定行き先（curated quick-nav）。label は人間可読、hash は Router.navigate 引数。
    const NAV = [
        { label: 'Home（ホーム）', hash: '' },
        { label: 'Projects（プロジェクト一覧）', hash: 'projects' },
        { label: 'Apps（内蔵アプリ）', hash: 'apps' },
        { label: 'Task Manager（タスク管理）', hash: 'apps/task' },
        { label: 'Quick TODO', hash: 'apps/todo' },
        { label: 'Pomodoro Timer（ポモドーロ）', hash: 'apps/pomodoro' },
        { label: 'AI Assist（ローカル AI）', hash: 'apps/ai' },
        { label: 'Markdown ノート', hash: 'apps/notes' },
        { label: 'Quiz（問題集）', hash: 'quiz' },
        { label: 'AI Know-how（AI 開発ノウハウ）', hash: 'ai-knowhow' },
        { label: 'Role Split（人間 vs AI 分担）', hash: 'role-split' },
        { label: 'Hiring Risk（採用リスク低減）', hash: 'hiring-risk' },
        { label: 'About（思想・経歴）', hash: 'about' },
        { label: 'Resume（職務経歴）', hash: 'resume' },
        { label: 'Contact（問い合わせ）', hash: 'contact' },
        { label: 'Settings（設定）', hash: 'settings' },
    ];

    let host = null;        // #command-palette-host（body 直下・初回生成）
    let inputEl = null;
    let listEl = null;
    let trapHandler = null;
    let lastFocused = null;
    let activeIdx = 0;
    let rendered = [];      // 現在描画中の DESTINATIONS 部分集合

    function isOpen() {
        return !!host && host.getAttribute('aria-hidden') === 'false';
    }

    // 固定 NAV に「現在のプロジェクト一覧」を加えた検索対象を返す。プロジェクトは open 毎に
    // State から取得するので、追加/削除/import 後も最新が反映される (stale にならない)。
    function _allDestinations() {
        const projects = (State && State.get().projects) || [];
        const projItems = projects
            .filter(p => p && p.slug && p.name)
            .map(p => ({ label: 'プロジェクト: ' + p.name, hash: 'projects/' + p.slug }));
        return NAV.concat(projItems);
    }

    function _renderList(query) {
        const q = String(query || '').trim().toLowerCase();
        const all = _allDestinations();
        rendered = q
            ? all.filter(d => d.label.toLowerCase().includes(q) || d.hash.toLowerCase().includes(q))
            : all;
        activeIdx = 0;
        while (listEl.firstChild) { listEl.removeChild(listEl.firstChild); }
        if (!rendered.length) {
            listEl.appendChild(h('li', { class: 'cmdk-empty', role: 'status' }, '一致する行き先はありません'));
            return;
        }
        rendered.forEach((d, i) => {
            listEl.appendChild(h('li', {
                class: 'cmdk-item' + (i === activeIdx ? ' is-active' : ''),
                role: 'option',
                'aria-selected': i === activeIdx ? 'true' : 'false',
                'data-idx': String(i),
                onclick: () => _choose(i),
            }, createIcon('arrowUpRight', 16), h('span', { class: 'icon-gap' }, d.label)));
        });
    }

    function _highlight() {
        Array.from(listEl.children).forEach((li, i) => {
            const on = i === activeIdx;
            li.classList.toggle('is-active', on);
            if (li.setAttribute) { li.setAttribute('aria-selected', on ? 'true' : 'false'); }
        });
        const activeLi = listEl.children[activeIdx];
        if (activeLi && activeLi.scrollIntoView) { activeLi.scrollIntoView({ block: 'nearest' }); }
    }

    function _choose(i) {
        const dest = rendered[i];
        if (!dest) { return; }
        close();
        Router.navigate(dest.hash);
    }

    function _build() {
        host = document.createElement('div');
        host.id = 'command-palette-host';
        host.className = 'cmdk-host';
        host.setAttribute('aria-hidden', 'true');

        const backdrop = h('div', { class: 'cmdk-backdrop', onclick: close });
        inputEl = h('input', {
            type: 'text',
            class: 'cmdk-input',
            'aria-label': 'コマンドパレット: 行き先を検索',
            placeholder: '行き先を検索… (Esc で閉じる)',
            oninput: (e) => _renderList(e.target.value),
        });
        listEl = h('ul', { class: 'cmdk-list', role: 'listbox', 'aria-label': '行き先候補' });
        const panel = h('div', {
            class: 'cmdk-panel', role: 'dialog', 'aria-modal': 'true', 'aria-label': 'コマンドパレット',
        }, inputEl, listEl);

        host.appendChild(backdrop);
        host.appendChild(panel);
        document.body.appendChild(host);
    }

    function open() {
        if (!host) { _build(); }
        if (isOpen()) { return; }
        lastFocused = document.activeElement;
        _renderList('');
        inputEl.value = '';
        host.setAttribute('aria-hidden', 'false');
        host.style.display = 'block';
        // focus trap: Tab/Shift+Tab は overlay 内 focusable (input) に focus を保持 (背景へ抜けない)、
        // 矢印で list 候補を選択、Enter で遷移、Esc で閉じる
        trapHandler = function (e) {
            // IME 変換中 (e.isComposing) は全キーを IME に委ねる。日本語でプロジェクト名等を検索する際、
            // 変換確定の Enter が _choose (遷移) を誤発火する footgun と、矢印が変換候補選択を横取りするのを防ぐ。
            // (CLAUDE.md 教訓 B「日本語が主対象ゆえ全 Enter-submit に IME ガード必須」/ Check 112 と同クラス)
            if (e.isComposing) { return; }
            if (e.key === 'Escape') { e.preventDefault(); close(); return; }
            if (e.key === 'ArrowDown') { e.preventDefault(); activeIdx = Math.min(activeIdx + 1, rendered.length - 1); _highlight(); return; }
            if (e.key === 'ArrowUp') { e.preventDefault(); activeIdx = Math.max(activeIdx - 1, 0); _highlight(); return; }
            if (e.key === 'Enter' && !e.isComposing) { e.preventDefault(); _choose(activeIdx); return; }
            if (e.key === 'Tab') {
                // focus trap (mobile-drawer __trapFocus と同パターン): overlay 内の focusable に
                // focus を保持し、aria-modal="true" の背景へ Tab で抜けるのを防ぐ。本 palette の
                // focusable は input のみ (list 候補は arrow で操作・tabindex 無し) ゆえ first===last
                // となり Tab/Shift+Tab とも input に留まる。将来 focusable が増えても wrap で循環する。
                const focusable = host.querySelectorAll(
                    'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
                );
                if (focusable.length) {
                    const first = focusable[0];
                    const last = focusable[focusable.length - 1];
                    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
                    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
                }
                return;
            }
        };
        document.addEventListener('keydown', trapHandler);
        inputEl.focus();
    }

    function close() {
        if (!host) { return; }
        host.setAttribute('aria-hidden', 'true');
        host.style.display = 'none';
        if (trapHandler) { document.removeEventListener('keydown', trapHandler); trapHandler = null; }
        if (lastFocused && lastFocused.focus) { try { lastFocused.focus(); } catch (e) { /* noop */ } }
    }

    function init() {
        // global opener: Cmd/Ctrl+K のみ横取り（他キーは素通し）
        document.addEventListener('keydown', (e) => {
            if ((e.metaKey || e.ctrlKey) && (e.key === 'k' || e.key === 'K')) {
                e.preventDefault();
                isOpen() ? close() : open();
            }
        });
    }

    return { init, open, close };
}
