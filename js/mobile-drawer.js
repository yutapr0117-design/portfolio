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
 *   - 8 関数の DOM 出力・aria 属性・focus 管理・body scroll lock は byte-equivalent
 *   - rel=noopener / referrerpolicy の付与ロジックも不変
 *   - Escape キーで closeDrawer、Tab/Shift+Tab で focusable 要素間のループも不変
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 *
 * 【secureExternalLinks の二重利用】
 *   AIDK Rails (js/aidk-rails.js) の EffectRails._dispatch でも secureExternalLinks を
 *   呼ぶため、本 factory の戻り値から secureExternalLinks を取り出して createAIDKRails の
 *   引数にも渡す（main.js の合成側で行う）。
 */
export function createMobileDrawer({ CONSTANTS, clear, Sidebar }) {
    // ===== Mobile Drawer =====
    function syncMobileDrawer() {
        const isMobile = window.matchMedia(`(max-width: ${CONSTANTS.MOBILE_BREAKPOINT}px)`).matches;
        const topbar = document.getElementById('topbar');

        if (topbar) {
            topbar.style.display = isMobile ? 'flex' : 'none';
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
        openDrawer, closeDrawer
    };
}
