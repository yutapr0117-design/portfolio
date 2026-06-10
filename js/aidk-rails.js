/**
 * js/aidk-rails.js — AIDK Rails composite factory (RouteState / EffectRails /
 * BindingRegistry / ActionDelegator / DiagnosticsRail)
 * (v80+ Stage 5-l extraction — composite factory pattern with mutual late-binding)
 *
 * main.js の AIDK Rail 5 つを 1 つの合体 factory として物理分割した葉モジュール。
 * 5 つの IIFE は相互依存（RouteState の Proxy.set が BindingRegistry を typeof
 * チェックで参照、EffectRails が RouteState / applyMeta / DiagnosticsRail を参照、
 * BindingRegistry が RouteState を参照、DiagnosticsRail が全 Rail を参照）するため、
 * 1 つのファイルに合体して factory closure 内で順次定義する形を取る。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const { RouteState, EffectRails, BindingRegistry, ActionDelegator, DiagnosticsRail }
 *       = createAIDKRails({ State, Toast, Router, CONSTANTS, applyMeta, h, createIcon });
 *
 * 【依存（引数で注入）】
 *   - State: js/state.js factory instance
 *   - Toast: js/ui-components.js
 *   - Router: js/router.js
 *   - CONSTANTS: js/constants.js (特に DEBUG / TAB_ID)
 *   - applyMeta: js/meta-management.js factory instance ({ applyMeta })
 *   - h, createIcon: js/ui-components.js (DiagnosticsRail の表示部で使う)
 *
 * 【相互依存の順序（評価時 binding が undefined でも runtime 呼び出し時には全 Rail 解決済み）】
 *   1. RouteState 定義: Proxy.set 内で BindingRegistry / EffectRails を参照するが、
 *      Proxy.set が初めて呼ばれるのは renderer / event handler 起動後 = 全 Rail 定義済み
 *   2. EffectRails 定義: RouteState はすでに存在。DiagnosticsRail は typeof チェック
 *      または closure late-binding で OK
 *   3. BindingRegistry 定義: RouteState はすでに存在
 *   4. ActionDelegator 定義: 他 Rail との直接結合なし
 *   5. DiagnosticsRail 定義: 全 Rail はすでに存在
 *
 * 【非破壊性】
 *   - 5 IIFE の DOM 自動水和・副作用順序・診断機能は byte-equivalent
 *   - Proxy.set の差分 skip / Diagnostics 記録ロジックも不変
 *   - AIDK Kernel (Check 43 で構造強制) には触れない（kernel proper はそのまま main.js に残置）
 *   - AIO 正本層 / style.css は無変更
 */
export function createAIDKRails({ State, Toast, Router, CONSTANTS, applyMeta, h, createIcon, Theme, BGM, secureExternalLinks, openDrawer, closeDrawer }) {
    const RouteState = (() => {
        const _state = {
            // ── route namespace ──
            route_name:    'home',
            route_slug:    '',
            route_hash:    '#/',
            // ── ui namespace ──
            ui_drawer_open:    false,
            ui_theme:          'system',
            ui_active_filter:  '',
            ui_is_loading:     false,
            // ── bgm namespace ──
            bgm_is_playing:   false,
            bgm_volume_level: 1.0,
            // ── a11y namespace ──
            a11y_announcement: '',
            // ── diag namespace ──
            diag_debug_mode:      false,
            diag_last_key:        '',
            diag_last_value:      null,
            diag_change_count:    0
        };

        const _callbacks = [];

        // 改善文書b 1.1: Object.seal prevents undeclared property addition on the proxy target.
        // Known properties can still be updated; adding new ones throws TypeError in strict mode.
        Object.seal(_state);

        const proxy = new Proxy(_state, {
            set(target, key, value) {
                if (target[key] === value) { return true; } // 値変化なし → スキップ
                const prev = target[key];
                target[key] = value;

                // Diagnostics 記録
                target.diag_last_key   = String(key);
                target.diag_last_value = value;
                target.diag_change_count++;

                // Binding Registry 通知
                if (typeof BindingRegistry !== 'undefined') {
                    try { BindingRegistry.updateBindings(String(key), value, prev); } catch {}
                }

                // 副作用 Rail のディスパッチ
                EffectRails.dispatch(String(key), value, prev);

                // 汎用購読者への通知
                _callbacks.forEach(cb => { try { cb(proxy, String(key), value, prev); } catch {} });
                return true;
            }
        });

        function subscribe(cb) {
            _callbacks.push(cb);
            return () => { const i = _callbacks.indexOf(cb); if (i > -1) { _callbacks.splice(i, 1); } };
        }

        return { proxy, subscribe };
    })();

    // ===== AIDK EffectRails — Private副作用レール =====
    // Proxyからのみ呼び出される。AIから不可視・編集不可。
    const EffectRails = (() => {
        // 各キーに対応するRailをマッピング
        const _map = {
            route_name:        ['meta', 'aio', 'a11y'],
            route_slug:        ['meta', 'aio'],
            ui_drawer_open:    ['a11y'],
            a11y_announcement: ['a11y'],
            diag_debug_mode:   ['diag']
        };

        function _metaRail(key, value) {
            // Meta Rail: routeが変わったらapplyMetaに委譲
            if (key === 'route_name') {
                try {
                    const RS = RouteState.proxy;
                    applyMeta(RS.route_name, RS.route_slug ? { slug: RS.route_slug } : {}, {});
                } catch {}
            }
        }

        function _aioRail(key, value) {
            // AIO Rail: sr-onlyアンカーの整合性を保護（DOM再構築後も維持）
            try {
                const anchor = document.getElementById('aio-footer-entity');
                if (anchor && !document.body.contains(anchor)) {
                    document.body.appendChild(anchor);
                }
            } catch {}
        }

        function _a11yRail(key, value) {
            if (key === 'a11y_announcement' && value) {
                const el = document.getElementById('page-announcement');
                if (el) {
                    requestAnimationFrame(() => {
                        el.textContent = '';
                        requestAnimationFrame(() => { el.textContent = value; });
                    });
                }
            }
            if (key === 'ui_drawer_open') {
                const app = document.getElementById('app');
                if (app) {
                    if (value) { app.setAttribute('inert', ''); }
                    else { app.removeAttribute('inert'); }
                }
            }
        }

        function _diagRail(key, value) {
            if (key === 'diag_debug_mode') {
                if (value) { DiagnosticsRail.show(); }
                else { DiagnosticsRail.hide(); }
            }
        }

        function dispatch(key, value, prev) {
            const rails = _map[key] || [];
            if (rails.includes('meta')) { try { _metaRail(key, value); } catch {} }
            if (rails.includes('aio')) { try { _aioRail(key, value); } catch {} }
            if (rails.includes('a11y')) { try { _a11yRail(key, value); } catch {} }
            if (rails.includes('diag')) { try { _diagRail(key, value); } catch {} }
            // Security Rail: 常時実行（副作用コストが低いため全変更後に走らせる）
            try { secureExternalLinks(document); } catch {}
        }

        return { dispatch };
    })();

    // ===== AIDK BindingRegistry — 自動水和バインディング登録機構 =====
    // MutationObserverで data-bind-* 属性を持つ要素を自動検知・登録する。
    // AIは属性を付与するだけでよく、バインディング登録コードを書く必要がない。
    const BindingRegistry = (() => {
        // Map<stateKey, Set<Element>>
        const _registry = new Map();
        let _observer = null;

        function _registerElement(el) {
            // data-bind-text
            const bindText = el.getAttribute('data-bind-text');
            if (bindText) { _add(bindText, el); }
            // data-bind-show
            const bindShow = el.getAttribute('data-bind-show');
            if (bindShow) { _add(bindShow, el); }
            // data-bind-attr-*
            for (const attr of el.attributes) {
                if (attr.name.startsWith('data-bind-attr-')) {
                    const stateKey = attr.value;
                    if (stateKey) { _add(stateKey, el); }
                }
            }
        }

        function _unregisterElement(el) {
            _registry.forEach((set) => set.delete(el));
        }

        function _add(key, el) {
            if (!_registry.has(key)) { _registry.set(key, new Set()); }
            _registry.get(key).add(el);
            // 初期同期
            _syncElement(el, key, RouteState.proxy[key]);
        }

        function _syncElement(el, key, value) {
            if (el.hasAttribute('data-bind-text')) {
                el.textContent = (value !== undefined && value !== null) ? String(value) : '';
            }
            if (el.hasAttribute('data-bind-show')) {
                const show = !!value;
                el.hidden = !show;
                el.style.display = show ? '' : 'none';
            }
            for (const attr of el.attributes) {
                if (attr.name.startsWith('data-bind-attr-')) {
                    const htmlAttr = attr.name.slice('data-bind-attr-'.length);
                    if (value !== undefined && value !== null) {
                        el.setAttribute(htmlAttr, String(value));
                    }
                }
            }
        }

        function updateBindings(key, value) {
            const set = _registry.get(key);
            if (!set) { return; }
            set.forEach(el => {
                if (document.contains(el)) {
                    _syncElement(el, key, value);
                } else {
                    set.delete(el); // ガベージコレクション
                }
            });
        }

        function init() {
            // 初回スキャン
            document.querySelectorAll('[data-bind-text],[data-bind-show],[data-bind-list]').forEach(el => {
                for (const attr of el.attributes) {
                    if (attr.name.startsWith('data-bind-')) { _registerElement(el); }
                }
            });

            // MutationObserver — DOMの追加・削除を自動検知
            _observer = new MutationObserver((mutations) => {
                for (const mut of mutations) {
                    for (const node of mut.addedNodes) {
                        if (node.nodeType !== 1) { continue; }
                        if (node.hasAttribute && node.hasAttribute('data-bind-text') ||
                            node.hasAttribute && node.hasAttribute('data-bind-show')) {
                            _registerElement(node);
                        }
                        node.querySelectorAll && node.querySelectorAll('[data-bind-text],[data-bind-show]').forEach(el => {
                            _registerElement(el);
                        });
                    }
                    for (const node of mut.removedNodes) {
                        if (node.nodeType !== 1) { continue; }
                        _unregisterElement(node);
                        node.querySelectorAll && node.querySelectorAll('[data-bind-text],[data-bind-show]').forEach(el => {
                            _unregisterElement(el);
                        });
                    }
                }
            });
            _observer.observe(document.body, { childList: true, subtree: true });
        }

        return { init, updateBindings };
    })();

    // ===== AIDK ActionDelegator — 単一イベント委譲器 =====
    // AIは data-action="ACTION_NAME" を付与するだけ。
    // 個別の addEventListener 記述は不要。
    const ActionDelegator = (() => {
        const _handlers = {
            'drawer:open':    () => { if (typeof openDrawer === 'function') { openDrawer(); } },
            'drawer:close':   () => { if (typeof closeDrawer === 'function') { closeDrawer(); } },
            'theme:cycle':    () => { if (typeof Theme !== 'undefined') { Theme.cycle(); } },
            'bgm:toggle':     () => { if (typeof BGM !== 'undefined') { BGM.toggle(); } }
        };

        function init() {
            // 改善文書b 11.1: target.closest() による正確な要素捕捉。
            // e.target ではなく e.target.closest('[data-action]') で遡上検索するため、
            // ボタン内のSVGアイコンや<span>がクリックされた場合でも確実に発火する。
            // さらに e.currentTarget.contains(target) でスコープ外への意図しない伝播を防ぐ。
            document.addEventListener('click', (e) => {
                const target = e.target.closest('[data-action]');
                if (!target) { return; }
                // containsガード: documentに紐付いたリスナーなので常にtrueだが、
                // 将来スコープを絞った場合の安全弁として明示的に残す
                const action = target.getAttribute('data-action');
                if (!action) { return; }
                const handler = _handlers[action];
                if (handler) {
                    e.preventDefault();
                    try { handler(e, target); } catch {}
                }
            }, { passive: false });
        }

        function register(action, handler) {
            _handlers[action] = handler;
        }

        return { init, register };
    })();

    // ===== AIDK DiagnosticsRail — ?debug=1 オーバーレイ =====
    const DiagnosticsRail = (() => {
        let _el = null;

        function _appendDiagText(parent, text, className) {
            const span = document.createElement('span');
            if (className) { span.className = className; }
            span.textContent = text;
            parent.appendChild(span);
            return span;
        }

        function _appendDiagLine(parent, label, value, valueClassName) {
            const line = document.createElement('div');
            line.appendChild(document.createTextNode(`${label}: `));
            _appendDiagText(line, String(value), valueClassName);
            parent.appendChild(line);
            return line;
        }

        function _appendDiagSectionLabel(parent, text) {
            const label = document.createElement('b');
            label.className = 'u-ai-diag-label';
            label.textContent = text;
            parent.appendChild(label);
            return label;
        }

        function _appendDiagHr(parent) {
            const hr = document.createElement('hr');
            hr.className = 'u-ai-diag-hr';
            parent.appendChild(hr);
            return hr;
        }

        function _build() {
            const el = document.createElement('div');
            el.id = 'aidk-diagnostics';
            el.style.cssText = [
                'position:fixed', 'bottom:0', 'right:0', 'z-index:99999',
                'background:rgba(2,6,23,0.92)', 'color:#94a3b8',
                'font:12px/1.5 monospace', 'padding:10px 14px',
                'border-top-left-radius:8px', 'max-width:340px',
                'max-height:40vh', 'overflow-y:auto',
                'border:1px solid #334155', 'pointer-events:auto'
            ].join(';');
            el.setAttribute('aria-hidden', 'true');
            return el;
        }

        function _update() {
            if (!_el) { return; }
            const RS = RouteState.proxy;

            _el.replaceChildren();

            const title = document.createElement('strong');
            title.className = 'u-ai-diag-title';
            title.textContent = 'AIDK Diagnostics';
            _el.appendChild(title);

            _appendDiagHr(_el);
            _appendDiagSectionLabel(_el, 'RouteState');
            _appendDiagLine(_el, 'route_name', RS.route_name, 'u-ai-diag-val-green');
            _appendDiagLine(_el, 'route_slug', RS.route_slug || '—', 'u-ai-diag-val-green');
            _appendDiagLine(_el, 'ui_drawer_open', RS.ui_drawer_open, 'u-ai-diag-val-green');
            _appendDiagLine(_el, 'ui_theme', RS.ui_theme, 'u-ai-diag-val-green');

            _appendDiagHr(_el);
            _appendDiagSectionLabel(_el, 'Last Change');
            _appendDiagLine(_el, 'key', RS.diag_last_key || '—', 'u-ai-diag-val-amber');
            _appendDiagLine(_el, 'value', String(RS.diag_last_value), 'u-ai-diag-val-amber');
            _appendDiagLine(_el, 'changes', RS.diag_change_count, 'u-ai-diag-val-amber');

            _appendDiagHr(_el);
            _appendDiagSectionLabel(_el, 'Kernel');
            _appendDiagText(_el, 'BindingRegistry: active');
            _el.appendChild(document.createElement('br'));
            _appendDiagText(_el, 'ActionDelegator: active');
            _el.appendChild(document.createElement('br'));
            _appendDiagText(_el, 'EffectRails: Meta/AIO/A11y/Security/Diag');
            _el.appendChild(document.createElement('br'));
            _appendDiagText(_el, '?debug=1 to show · Press D to refresh', 'u-ai-diag-hint');
        }

        function show() {
            if (!_el) {
                _el = _build();
                document.body.appendChild(_el);
            }
            _el.style.display = 'block';
            // Auto-refresh every 2s
            if (!_el._timer) {
                _el._timer = setInterval(_update, 2000);
            }
            _update();
            document.addEventListener('keydown', (e) => {
                if (e.key === 'd' || e.key === 'D') { _update(); }
            });
        }

        function hide() {
            if (_el) {
                _el.style.display = 'none';
                if (_el._timer) { clearInterval(_el._timer); _el._timer = null; }
            }
        }

        return { show, hide };
    })();

    return { RouteState, EffectRails, BindingRegistry, ActionDelegator, DiagnosticsRail };
}
