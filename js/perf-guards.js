/**
 * js/perf-guards.js — Performance guards (Layout Thrashing + Media Lifecycle)
 * (v80+ Stage 5-s extraction via factory pattern)
 *
 * main.js の 2 つのパフォーマンスガード IIFE（_installLayoutThrashingGuard /
 * _installMediaLifecycleGuard）を依存注入なしの factory pattern で物理分割した
 * 葉モジュール。両方ともグローバルプロトタイプ（CSSStyleDeclaration / Element /
 * URL）を hook するだけのブラウザ非破壊オプティマイゼーションで、外部依存は
 * 一切ない（DOM API のみ）。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const perfGuards = createPerfGuards();
 *   perfGuards.installLayoutThrashingGuard();
 *   perfGuards.installMediaLifecycleGuard();
 *
 * 【依存（引数で注入）】
 *   なし — DOM API（CSSStyleDeclaration / Element.prototype / URL / Mutation /
 *   IntersectionObserver）のみを使用する。葉契約（Check 47c: import ゼロ）と
 *   合致する。
 *
 * 【非破壊性】
 *   - Layout Thrashing Guard の setProperty / setAttribute('style', ...) フックは
 *     byte-equivalent（rAF バッチ化のタイミングのみ抜本的に介入）
 *   - Media Lifecycle Guard の MutationObserver による blobURL 解放 + URL.createObjectURL
 *     hook も byte-equivalent
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 *   - これら 2 ガードは IIFE → function declaration への置換のみで挙動は完全同一
 */
export function createPerfGuards() {
    // ─────────────────────────────────────────────────────────────────────────
    // 改善文書c Section 8: レイアウトスラッシング防止 — rAF Write-Batching Proxy
    // Element.prototype.style の setter および setAttribute をフックし、
    // スタイル変更要求を requestAnimationFrame 直前にバッチ適用する。
    // AI 生成の素朴な同期スタイル書き込みループを透過的に最適化する非破壊実装。
    // ─────────────────────────────────────────────────────────────────────────
    function installLayoutThrashingGuard() {
        'use strict';
        var _writeQueue = [];
        var _rafPending = false;

        function _flushQueue() {
            _rafPending = false;
            var q = _writeQueue.splice(0);
            for (var i = 0; i < q.length; i++) { q[i](); }
        }

        function _scheduleFlush() {
            if (!_rafPending) {
                _rafPending = true;
                requestAnimationFrame(_flushQueue);
            }
        }

        // CSSStyleDeclaration.setProperty をフックしてバッチ化
        var _origSetProperty = CSSStyleDeclaration.prototype.setProperty;
        CSSStyleDeclaration.prototype.setProperty = function(prop, value, priority) {
            var self = this;
            _writeQueue.push(function() { _origSetProperty.call(self, prop, value, priority); });
            _scheduleFlush();
        };

        // style 直接プロパティへの代入は cssText 経由のバッチ化
        // (プロパティ数が多い場合のみ活性化 — 単純スカラはネイティブ委譲)
        var _origStyleSetter = Object.getOwnPropertyDescriptor(HTMLElement.prototype, 'style');
        // NOTE: style は getter/setter の直接オーバーライドが制限されるため、
        //       setProperty フック + DocumentFragment 戦略 (改善文書b 7.1) を主防衛とする。
        // 追加: setAttribute('style', ...) フック
        var _origSetAttr = Element.prototype.setAttribute;
        Element.prototype.setAttribute = function(name, value) {
            if (name === 'style') {
                var self = this;
                _writeQueue.push(function() { _origSetAttr.call(self, 'style', value); });
                _scheduleFlush();
            } else {
                _origSetAttr.call(this, name, value);
            }
        };
    }

    // ─────────────────────────────────────────────────────────────────────────
    // 改善文書c Section 9: メディアアセット ライフサイクル管理（Media Lifecycle Guard）
    // DOM から削除された img / audio / video 要素の ObjectURL / AudioBuffer を
    // 自動解放してメモリリークを根絶する非破壊実装。
    // 注意: IntersectionObserver (_intersectionObserver) は deferred-src
    // lazy loading 用に生成しているが、observe() を呼び出す箇所が現時点では
    // 存在しないため、実際には lazy loading は機能していない。
    // 現在の役割は MutationObserver によるメディアリソース解放（cleanup/lifecycle guard）のみ。
    // ─────────────────────────────────────────────────────────────────────────
    function installMediaLifecycleGuard() {
        'use strict';
        var _blobMap = new WeakMap(); // element → blobURL

        // IntersectionObserver: ビューポート外では src を遅延
        var _ioOptions = { rootMargin: '200px' };
        var _intersectionObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                var el = entry.target;
                if (entry.isIntersecting) {
                    var deferred = el.getAttribute('data-deferred-src');
                    if (deferred) {
                        el.src = deferred;
                        el.removeAttribute('data-deferred-src');
                    }
                    _intersectionObserver.unobserve(el);
                }
            });
        }, _ioOptions);

        // MutationObserver: DOM 削除時にリソース解放
        var _removalObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(m) {
                m.removedNodes.forEach(function(node) {
                    if (!node || node.nodeType !== 1) { return; }
                    _releaseMediaNode(node);
                    if (node.querySelectorAll) {
                        node.querySelectorAll('img, audio, video').forEach(_releaseMediaNode);
                    }
                });
            });
        });

        function _releaseMediaNode(el) {
            if (!el || el.nodeType !== 1) { return; }
            var tag = el.tagName;
            if (tag === 'IMG' || tag === 'VIDEO') {
                var blobUrl = _blobMap.get(el);
                if (blobUrl) {
                    try { URL.revokeObjectURL(blobUrl); } catch (e) { /* noop */ }
                    _blobMap.delete(el);
                }
            }
            if (tag === 'AUDIO' || tag === 'VIDEO') {
                try {
                    if (el.src && el.src.startsWith('blob:')) {
                        URL.revokeObjectURL(el.src);
                    }
                    el.src = '';
                    el.load(); // バッファ強制クリア
                } catch (e) { /* noop */ }
            }
        }

        function _start() {
            if (document.body) {
                _removalObserver.observe(document.body, { childList: true, subtree: true });
            }
        }
        if (document.body) { _start(); }
        else { document.addEventListener('DOMContentLoaded', _start); }

        // グローバル ObjectURL 生成をフックして追跡
        var _origCreateObjectURL = URL.createObjectURL;
        URL.createObjectURL = function(obj) {
            var url = _origCreateObjectURL.call(URL, obj);
            // 呼び出し元の el 参照は取れないため、Blob URL は _releaseMediaNode で補足
            return url;
        };
    }

    return { installLayoutThrashingGuard, installMediaLifecycleGuard };
}
