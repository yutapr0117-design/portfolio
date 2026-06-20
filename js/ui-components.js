/**
 * ui-components.js — DOM ユーティリティと表示専用コンポーネント
 *
 * @fileoverview v80+ Stage 4: main.js から抽出した UI コンポーネント群。
 * いずれも closure-deps = none（localStorage・State・RouteState に非依存）であり、
 * 抽出前後で挙動は完全に等価。
 *
 * export:
 *   h(tag, attrs, ...children)  — 型安全 XSS 防止 DOM ビルダー（全 render が依存。署名変更厳禁）
 *   createIcon(name, size)       — SVG アイコン生成（TrustedTypes 完全適合）
 *   Toast                        — トースト通知 { show }
 *   BGM                          — BGM 管理 { toggle, isOn, syncAll, init }
 *
 * 不変条件:
 *   - 本モジュールは葉（ローカル ESM import ゼロ）。外部ライブラリへの依存を持たない。
 *   - h() の署名・挙動は変更禁止。innerHTML は PROHIBITED（throw で強制）。
 *   - createIcon() は innerHTML・DOMParser を一切使用しない（TrustedTypes 完全適合）。
 *   - Toast・BGM は DOM のみを副作用とし、永続ストレージ・外部状態に触れない。
 */

// ===== Icons (SVG) =====
let _icons_cache = null;
function getIcons() {
    if (!_icons_cache) {
        _icons_cache = {
            menu: `<path d="M4 6h16M4 12h16M4 18h16"/>`,
            sun: `<path d="M12 18a6 6 0 1 0 0-12 6 6 0 0 0 0 12Z"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>`,
            moon: `<path d="M21 12.79A9 9 0 1 1 11.21 3a7 7 0 0 0 9.79 9.79Z"/>`,
            home: `<path d="M3 10.5 12 3l9 7.5V21a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1v-10.5Z"/>`,
            briefcase: `<path d="M10 3h4a2 2 0 0 1 2 2v2h-8V5a2 2 0 0 1 2-2Z"/><path d="M4 7h16a2 2 0 0 1 2 2v3a3 3 0 0 1-3 3h-1v-2h-12v2H5a3 3 0 0 1-3-3V9a2 2 0 0 1 2-2Z"/><path d="M4 15v5a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5"/>`,
            apps: `<path d="M4 4h7v7H4V4Zm9 0h7v7h-7V4ZM4 13h7v7H4v-7Zm9 0h7v7h-7v-7Z"/>`,
            checkSquare: `<path d="M9 11l2 2 4-4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/>`,
            list: `<path d="M8 6h13M8 12h13M8 18h13"/><path d="M3 6h.01M3 12h.01M3 18h.01"/>`,
            clock: `<path d="M12 8v5l3 3"/><path d="M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Z"/>`,
            brain: `<path d="M8.5 4.5a3 3 0 0 0-3 3v1a3 3 0 0 0 0 6v1a3 3 0 0 0 3 3"/><path d="M15.5 4.5a3 3 0 0 1 3 3v1a3 3 0 0 1 0 6v1a3 3 0 0 1-3 3"/><path d="M9 7h.01M9 11h.01M9 15h.01M15 7h.01M15 11h.01M15 15h.01"/>`,
            settings: `<path d="M12 15.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7Z"/><path d="M19.4 15a7.8 7.8 0 0 0 .1-2l2-1.2-2-3.5-2.3.6a7.3 7.3 0 0 0-1.7-1L15 3h-6l-.7 2.9a7.3 7.3 0 0 0-1.7 1L4.3 6.3l-2 3.5 2 1.2a7.8 7.8 0 0 0 0 2l-2 1.2 2 3.5 2.3-.6a7.3 7.3 0 0 0 1.7 1L9 21h6l.7-2.9a7.3 7.3 0 0 0 1.7-1l2.3.6 2-3.5-2-1.2Z"/>`,
            search: `<path d="M21 21l-4.3-4.3"/><path d="M10 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16Z"/>`,
            upload: `<path d="M12 3v13"/><path d="m7 8 5-5 5 5"/><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>`,
            download: `<path d="M12 3v13"/><path d="m7 10 5 5 5-5"/><path d="M21 21H3"/>`,
            trash: `<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M10 11v6M14 11v6"/><path d="M6 6l1 16h10l1-16"/>`,
            x: `<path d="M18 6 6 18M6 6l12 12"/>`,
            arrowUpRight: `<path d="M7 17 17 7"/><path d="M10 7h7v7"/>`,
            play: `<path d="M8 5v14l11-7-11-7Z"/>`,
            pause: `<path d="M6 5h4v14H6zM14 5h4v14h-4z"/>`,
            rotate: `<path d="M21 12a9 9 0 1 1-3-6.7"/><path d="M21 3v7h-7"/>`,
            alert: `<path d="M12 9v4"/><path d="M12 17h.01"/><path d="M10.3 3.7a2 2 0 0 1 3.4 0l8 13.9a2 2 0 0 1-1.7 3H4a2 2 0 0 1-1.7-3l8-13.9Z"/>`,
            check: `<path d="M20 6 9 17l-5-5"/>`,
            up: `<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>`,
            down: `<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>`,
            pin: `<path d="M14 9V4h-4v5L7 12v3h10v-3l-3-3Z"/><path d="M12 15v7"/>`,
            plus: `<path d="M12 5v14M5 12h14"/>`,
            user: `<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>`,
            mail: `<path d="M4 4h16c1.1 0 2 .9 2 2v13c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/>`,
            github: `<path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"/>`,
            linkedin: `<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/>`,
            filter: `<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>`,
            tag: `<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>`,
            calendar: `<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>`,
            edit: `<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>`,
            cloud: `<path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/>`,
            shield: `<path d="M12 2L4 5v6c0 5 3.5 9.7 8 11 4.5-1.3 8-6 8-11V5l-8-3Z"/>`,
            zap: `<path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>`,
            clipboard: `<path d="M9 2h6a1 1 0 0 1 1 1v1H8V3a1 1 0 0 1 1-1Z"/><path d="M5 3h2v2H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2V3h2"/><path d="M9 12h6M9 16h4"/>`,
            award: `<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>`,
            volume2: `<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/>`,
            volumeX: `<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><line x1="23" y1="9" x2="17" y2="15"/><line x1="17" y1="9" x2="23" y2="15"/>`,
            book: `<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>`,
            lightbulb: `<path d="M9 18h6"/><path d="M10 22h4"/><path d="M12 2a7 7 0 0 1 7 7c0 2.4-1.2 4.5-3 5.7V17a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1v-2.3C6.2 13.5 5 11.4 5 9a7 7 0 0 1 7-7z"/>`,
            users: `<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>`,
            externalLink: `<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>`,
            messageCircle: `<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>`,
            send: `<line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/>`,
            music: `<path d="M9 18V5l12-2v13"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>`,
            palette: `<circle cx="13.5" cy="6.5" r="1.5"/><circle cx="17.5" cy="10.5" r="1.5"/><circle cx="8.5" cy="7.5" r="1.5"/><circle cx="6.5" cy="12.5" r="1.5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/>`,
            sparkles: `<path d="M12 3L9.5 9.5 3 12l6.5 2.5L12 21l2.5-6.5L21 12l-6.5-2.5L12 3z"/>`,
        };
    }
    return _icons_cache;
}

// ===== Helper: Create SVG Icon =====
// v69: SVGアイコンパスのパース方法を安全化。
// paths は静的な定数文字列（getIcons()で管理）であり外部入力ではないが、
// innerHTML の代わりに DOMParser を使うことで XSS リスクを構造的にゼロにする。
export function createIcon(name, size = 20) {
    const paths = getIcons()[name];
    if (!paths) { return document.createTextNode(''); }

    const NS = 'http://www.w3.org/2000/svg';
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.setAttribute('width', size);
    svg.setAttribute('height', size);
    svg.setAttribute('fill', 'none');
    svg.setAttribute('stroke', 'currentColor');
    svg.setAttribute('stroke-width', '2');
    svg.setAttribute('stroke-linecap', 'round');
    svg.setAttribute('stroke-linejoin', 'round');
    svg.setAttribute('aria-hidden', 'true');

    // v70: DOMParser を廃止し、純粋なDOM APIでSVG子要素を生成。
    // DOMParser.parseFromString() はChromium系ブラウザでTrusted Typesの
    // createHTML ハンドラを内部的に呼び出すため、アーキテクチャ違反警告が
    // 誤発生していた。getIcons() の値は全て静的な自己閉鎖タグ
    // （<path/>, <circle/> 等）のみで構成されるため、
    // 正規表現による属性抽出 + createElementNS で完全に代替可能。
    // innerHTML・DOMParser を一切使用しないため Trusted Types と完全適合。
    const tagRe = /<(\w+)([^>]*?)\/>/g;
    let m;
    while ((m = tagRe.exec(paths)) !== null) {
        const el = document.createElementNS(NS, m[1]);
        const attrRe = /(\w[\w-]*)="([^"]*)"/g;
        let a;
        while ((a = attrRe.exec(m[2])) !== null) {
            el.setAttribute(a[1], a[2]);
        }
        svg.appendChild(el);
    }
    return svg;
}

// ===== Helper: DOM Builder (Type-safe XSS prevention) =====
export function h(tag, attrs = {}, ...children) {
    const el = document.createElement(tag);
    let refCb = null;
    for (const [key, value] of Object.entries(attrs)) {
        if (value === undefined || value === null) { continue; }
        if (key === '__unsafeHtml') { continue; } // [REMOVED] no longer supported
        if (key === 'ref' && typeof value === 'function') {
            refCb = value;
            continue;
        }
        if (key === 'class') {
            if (Array.isArray(value)) {
                el.className = value.filter(Boolean).join(' ');
            } else {
                el.className = String(value);
            }
        } else if (key === 'style') {
            if (typeof value === 'object') {
                Object.assign(el.style, value);
            } else {
                el.style.cssText = String(value);
            }
        } else if (key === 'dataset' && typeof value === 'object') {
            Object.entries(value).forEach(([k, v]) => {
                if (v !== undefined) { el.dataset[k] = String(v); }
            });
        } else if (key.startsWith('on') && typeof value === 'function') {
            el.addEventListener(key.slice(2).toLowerCase(), value);
        } else if (key === 'text') {
            el.textContent = String(value);
        } else if (key === 'html') {
            // [SECURITY] innerHTML injection completely removed. Use textContent ('text' key) or DOM nodes.
            throw new Error('[h] innerHTML is strictly prohibited in this architecture.');
        } else if (key.startsWith('aria-') || key === 'role') {
            if (value === false || value === null) {
                el.removeAttribute(key);
            } else {
                el.setAttribute(key, String(value));
            }
        } else {
            // Standard attributes: remove if value is false/null (v39: generic removal mechanism)
            if (value === false || value === null) {
                el.removeAttribute(key);
            } else {
                el.setAttribute(key, String(value));
            }
        }
    }
    if (tag === 'a' && el.getAttribute('target') === '_blank') {
        el.setAttribute('rel', 'noopener noreferrer');
    }
    children.flat().forEach(child => {
        if (child === undefined || child === null) {return;}
        if (child instanceof Node) {
            el.appendChild(child);
        } else {
            el.appendChild(document.createTextNode(String(child)));
        }
    });
    if (refCb) {
        try { refCb(el); } catch (e) { }
    }
    return el;
}

// ===== AIDK Toast Notification System =====
export const Toast = (() => {
    let container = null;

    function init() {
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.setAttribute('role', 'status');
            container.setAttribute('aria-live', 'polite');
            container.style.cssText = `
                position: fixed;
                top: 1.5rem;
                right: 1.5rem;
                z-index: 9999;
                display: flex;
                flex-direction: column;
                gap: 0.5rem;
            `;
            document.body.appendChild(container);
        }
    }

    function show(message, type = 'success', duration = 3000) {
        init();

        const el = document.createElement('div');
        el.className = `alert alert-${type}`;
        el.style.cssText = `
            animation: slideIn 0.3s ease;
            max-width: 400px;
            box-shadow: var(--shadow-xl);
        `;
        el.textContent = message;

        const closeBtn = h('button', {
            class: 'icon-btn ml-auto',
            'aria-label': '通知を閉じる',
            onclick: () => remove(el)
        }, createIcon('x', 16));

        el.appendChild(closeBtn);
        container.appendChild(el);

        // ARIA announcement (assertive for immediate feedback)
        const live = document.getElementById('action-announcement');
        if (live) { live.textContent = message; }

        if (duration > 0) {
            setTimeout(() => remove(el), duration);
        }

        return el;
    }

    function remove(el) {
        el.style.animation = 'slideIn 0.3s ease reverse';
        setTimeout(() => {
            el.remove();
        }, 300);
    }

    return { show };
})();

// ===== BGM Manager =====
export const BGM = (() => {
    let _on = false;

    function _audio() { return document.getElementById('bgm-audio'); }

    function _syncAll() {
        document.querySelectorAll('[data-bgm-btn]').forEach(btn => {
            btn.setAttribute('aria-pressed', String(_on));
            btn.setAttribute('aria-label', _on ? 'BGMを停止する' : 'BGMを再生する');
            // v69: innerHTML の代わりに createIcon() でアイコンを安全に差し替える
            const ico = btn.querySelector('svg');
            if (ico) {
                const newIcon = createIcon(_on ? 'volume2' : 'volumeX', ico.getAttribute('width') || 20);
                ico.replaceWith(newIcon);
            }
        });
    }

    async function toggle() {
        const audio = _audio();
        if (!audio) { return; }
        if (_on) {
            audio.pause();
            _on = false;
        } else {
            try {
                await audio.play();
                _on = true;
            } catch (err) {
                console.warn('BGM play failed:', err);
                return;
            }
        }
        _syncAll();
    }

    function isOn() { return _on; }

    function init() {
        const audio = _audio();
        if (audio) {
            audio.addEventListener('ended', () => { _on = false; _syncAll(); });
        }
    }

    return { toggle, isOn, syncAll: _syncAll, init };
})();
