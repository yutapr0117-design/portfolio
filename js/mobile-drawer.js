/**
 * js/mobile-drawer.js — Mobile drawer + focus trap + secureExternalLinks
 * (v80+ Stage 5-q extraction via factory pattern)
 *
 * main.js の Mobile Drawer 関連の関数群（syncMobileDrawer / secureExternalLinks /
 * __setAppInert / __lockBodyScroll / __trapFocus / __releaseFocusTrap / openDrawer /
 * closeDrawer）と関連 closure state を依存注入で物理分割した葉モジュール。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const Drawer = createMobileDrawer({...});
 *   const { syncMobileDrawer, secureExternalLinks, openDrawer, closeDrawer } = Drawer;
 *
 * 【依存（引数で注入）】
 *   - CONSTANTS: js/constants.js (MOBILE_BREAKPOINT)
 *   - clear: main.js IIFE 内の純粋関数（DOM の子要素を全削除）
 *   - Sidebar: js/components.js factory instance の Sidebar 関数
 *   - closePalette: js/command-palette.js の close（main.js が late-binding holder 経由で注入）。
 *     openDrawer 時に command palette を閉じ、aria-modal の領域が 2 つ同時に有効になる二重モーダルを
 *     防ぐ。palette 側 open() の closeDrawer と対をなす。未注入でも動作するよう typeof ガードあり
 *
 * 【factory closure 内の private state】
 *   - __drawerTrapHandler: focus trap のイベントハンドラ参照
 *   - __drawerLastFocused: drawer 開く前にフォーカスしていた要素
 *   - __drawerScrollY: body scroll lock の復元 Y 位置
 *
 * これらは元 main.js IIFE 内の let 宣言で、各 drawer open/close 間で状態を保持していた。
 * factory closure 内に同じ位置で declare することで、抽出前後の挙動は byte-equivalent。
 *
 * 【非破壊性】
 *   - 抽出時は 8 関数の DOM 出力・aria 属性・focus 管理・body scroll lock が byte-equivalent
 *     だったが、後の bug-fix で openDrawer に idempotency ガード（drawer aria-hidden==='false' なら
 *     再入しない）を追加済（#menuBtn が #app 外で inert 非対象ゆえ開放中の再 open が __drawerScrollY を
 *     0 上書きし close 時に先頭ジャンプする scroll-clobber を封じる・command-palette open() と同型）。
 *   - rel=noopener / referrerpolicy の付与ロジックも不変
 *   - Escape キーで closeDrawer、Tab/Shift+Tab で focusable 要素間のループも不変
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 *
 * 【secureExternalLinks の二重利用】
 *   AIDK Rails (js/aidk-rails.js) の EffectRails._dispatch でも secureExternalLinks を
 *   呼ぶため、本 factory の戻り値から secureExternalLinks を取り出して createAIDKRails の
 *   引数にも渡す（main.js の合成側で行う）。
 */
export function createMobileDrawer({ CONSTANTS, clear, Sidebar, closePalette }) {
    // ===== Mobile Drawer =====
    function syncMobileDrawer() {
        const isMobile = window.matchMedia(`(max-width: ${CONSTANTS.MOBILE_BREAKPOINT}px)`).matches;
        const topbar = document.getElementById('topbar');

        if (topbar) {
            topbar.style.display = isMobile ? 'flex' : 'none';
        }

        // [FIX] drawer 開放中に mobile→desktop へリサイズすると、openDrawer が付与した
        //   inline `display:block` は media query より優先されるため drawer/overlay が desktop で
        //   残り、__setAppInert(true)+__lockBodyScroll(true) のまま app が inert・scroll lock された
        //   stuck 状態になる (topbar=display:none で menuBtn も隠れる。overlay click / Escape でしか
        //   脱出できない broken UX)。desktop 遷移時に開いている drawer を明示的に閉じて isolation を
        //   解除する。closeDrawer は関数宣言ゆえ hoist され本関数から呼べる。
        if (!isMobile) {
            const drawer = document.getElementById('drawer');
            if (drawer && drawer.getAttribute('aria-hidden') === 'false') {
                closeDrawer();
            }
        }
    }


    // ===== Security: enforce noopener on target=_blank links (including dynamic links) =====
    function secureExternalLinks(root = document) {
        try {
            const links = root.querySelectorAll('a[target="_blank"]');
            links.forEach((a) => {
                const rel = (a.getAttribute('rel') || '').split(/\s+/).filter(Boolean);
                if (!rel.includes('noopener')) {rel.push('noopener');}
                if (!rel.includes('noreferrer')) {rel.push('noreferrer');}
                a.setAttribute('rel', rel.join(' '));
                // Optional: reduce referrer leakage for external links
                if (!a.getAttribute('referrerpolicy')) {a.setAttribute('referrerpolicy', 'no-referrer');}
            });
        } catch { /* noop */ }
    }

    // ===== Drawer Focus Trap / Accessibility helpers =====
    let __drawerTrapHandler = null;
    let __drawerLastFocused = null;
    let __drawerScrollY = 0;

    function __setAppInert(isInert) {
        const app = document.getElementById('app');
        if (!app) {return;}
        // Prefer native inert if available; fallback to aria-hidden + pointer-events
        try {
            if ('inert' in app) {app.inert = !!isInert;}
        } catch { /* noop */ }

        if (isInert) {
            app.setAttribute('aria-hidden', 'true');
            app.style.pointerEvents = 'none';
        } else {
            app.removeAttribute('aria-hidden');
            app.style.pointerEvents = '';
        }
    }

    function __lockBodyScroll(lock) {
        if (lock) {
            __drawerScrollY = window.scrollY || 0;
            document.body.style.position = 'fixed';
            document.body.style.top = `-${__drawerScrollY}px`;
            document.body.style.width = '100%';
        } else {
            const y = __drawerScrollY || 0;
            document.body.style.position = '';
            document.body.style.top = '';
            document.body.style.width = '';
            window.scrollTo(0, y);
        }
    }

    function __trapFocus(container) {
        const focusable = container.querySelectorAll(
            'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (!focusable.length) {return;}

        const first = focusable[0];
        const last = focusable[focusable.length - 1];

        __drawerTrapHandler = function (e) {
            if (e.key === 'Escape') {
                closeDrawer();
                return;
            }
            if (e.key !== 'Tab') {return;}

            if (e.shiftKey && document.activeElement === first) {
                e.preventDefault();
                last.focus();
            } else if (!e.shiftKey && document.activeElement === last) {
                e.preventDefault();
                first.focus();
            }
        };

        document.addEventListener('keydown', __drawerTrapHandler);
        first.focus();
    }

    function __releaseFocusTrap() {
        if (__drawerTrapHandler) {
            document.removeEventListener('keydown', __drawerTrapHandler);
            __drawerTrapHandler = null;
        }
    }

    function openDrawer() {
        const drawer = document.getElementById('drawer');
        const overlay = document.getElementById('overlay');
        const menuBtn = document.getElementById('menuBtn');

        if (!drawer || !overlay) {return;}

        // [FIX] 二重モーダルの防止 (逆方向)。command palette は overlay であって #app の inert 対象
        //   ではないため、palette 表示中も #topbar の menuBtn はクリックでき、そのまま drawer が開くと
        //   aria-modal="true" の領域が 2 つ同時に有効になる (実測: visibleModals=2)。palette 側の
        //   open() が drawer を閉じる対の処理と合わせ、**どちらの順序でも開くモーダルは常に 1 つ**に
        //   なる。片方向だけ塞ぐと「1 ケースだけ処理して他を忘れる」非対称バグになる (CLAUDE.md §7)。
        if (typeof closePalette === 'function') { closePalette(); }

        // [FIX] 既に開いている場合は再入しない (idempotency)。#menuBtn は #topbar 内＝#app の外に
        // あり __setAppInert の inert 対象外ゆえ、drawer 開放中も menuBtn はクリック可能。menuBtn は
        // toggle でなく常に openDrawer を呼ぶため、開放中の再クリックで __lockBodyScroll(true) が
        // body=position:fixed 状態の window.scrollY (=0) を読み __drawerScrollY を 0 に上書きし、
        // close 時に window.scrollTo(0,0) で先頭へジャンプする scroll-clobber バグになる (#262 と
        // 同症状・別トリガ)。再入を防ぐと __trapFocus の二重 addEventListener leak も同時に封じる。
        // (command-palette open() の `if (isOpen()) return` と同じ idempotency ガード)
        if (drawer.getAttribute('aria-hidden') === 'false') {return;}

        __drawerLastFocused = document.activeElement;

        clear(drawer);
        drawer.appendChild(Sidebar(true));

        // Visible
        drawer.removeAttribute('hidden');
        drawer.style.display = 'block';
        overlay.style.display = 'block';

        // ARIA
        drawer.setAttribute('aria-hidden', 'false');
        overlay.setAttribute('aria-hidden', 'false');
        menuBtn?.setAttribute('aria-expanded', 'true');

        // Background isolation
        __setAppInert(true);
        __lockBodyScroll(true);

        // Ensure rel=noopener for dynamic links inside drawer
        secureExternalLinks(drawer);

        // Focus
        __trapFocus(drawer);
    }

    function closeDrawer() {
        const drawer = document.getElementById('drawer');
        const overlay = document.getElementById('overlay');
        const menuBtn = document.getElementById('menuBtn');

        if (!drawer || !overlay) {return;}

        // [FIX] 閉じている状態での再入を弾く (openDrawer 側 #297 のガードの対。**片方にしか無かった**)。
        //   本関数は末尾で __lockBodyScroll(false) を呼び、その中で window.scrollTo(0, __drawerScrollY)
        //   が走る。drawer を一度も開いていなければ __drawerScrollY は 0 のままなので、**閉じている
        //   drawer を閉じるだけでページ先頭へ飛ぶ**。実際 command palette が open() で無条件に
        //   closeDrawer() を呼ぶ配線 (二重モーダル防止) を入れた結果、y=300 までスクロールした状態で
        //   Cmd/Ctrl+K を押すと y=0 へジャンプする回帰が実測された (#297 と同じ scroll-clobber class)。
        //   他の呼び出し元 (syncMobileDrawer / Escape ハンドラ) は既に aria-hidden を確認済みで、
        //   overlay click は drawer 開放時のみ到達するため、このガードで挙動が変わるのは再入経路だけ。
        if (drawer.getAttribute('aria-hidden') !== 'false') { return; }

        // Hide
        drawer.style.display = 'none';
        overlay.style.display = 'none';
        drawer.setAttribute('hidden', '');

        // ARIA
        drawer.setAttribute('aria-hidden', 'true');
        overlay.setAttribute('aria-hidden', 'true');
        menuBtn?.setAttribute('aria-expanded', 'false');

        // Release isolation
        __releaseFocusTrap();
        __setAppInert(false);
        __lockBodyScroll(false);

        // Focus restore
        (menuBtn || __drawerLastFocused)?.focus?.();
    }

    return {
        syncMobileDrawer, secureExternalLinks,
        openDrawer, closeDrawer,
        // 背景 (#app) の inert 化は command palette も同じ契約を要する。実装を複製すると
        // drift するため (Check 100 等が示す単一ソース原則) 唯一の実装をここから公開する。
        setAppInert: __setAppInert
    };
}
