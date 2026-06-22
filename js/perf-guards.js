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
 *   - Media Lifecycle Guard は MutationObserver による audio/video の blob: src 解放のみ機能。
 *     never-activated だった IntersectionObserver(lazy load) / _blobMap(img-video 追跡) /
 *     URL.createObjectURL フックは vestigial として除去済 (機能変化なし=全て dead だった)。
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
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
        const _writeQueue = [];
        let _rafPending = false;

        function _flushQueue() {
            _rafPending = false;
            const q = _writeQueue.splice(0);
            for (let i = 0; i < q.length; i++) { q[i](); }
        }

        function _scheduleFlush() {
            if (!_rafPending) {
                _rafPending = true;
                requestAnimationFrame(_flushQueue);
            }
        }

        // CSSStyleDeclaration.setProperty をフックしてバッチ化
        const _origSetProperty = CSSStyleDeclaration.prototype.setProperty;
        CSSStyleDeclaration.prototype.setProperty = function(prop, value, priority) {
            const self = this;
            _writeQueue.push(function() { _origSetProperty.call(self, prop, value, priority); });
            _scheduleFlush();
        };

        // NOTE: style プロパティの直接代入 (el.style.x = …) は getter/setter の直接
        //       オーバーライドが制限されるためフックしない。setProperty フック (上記) +
        //       DocumentFragment 戦略 (改善文書b 7.1) を主防衛とする。
        // 追加: setAttribute('style', ...) フック
        const _origSetAttr = Element.prototype.setAttribute;
        Element.prototype.setAttribute = function(name, value) {
            if (name === 'style') {
                const self = this;
                _writeQueue.push(function() { _origSetAttr.call(self, 'style', value); });
                _scheduleFlush();
            } else {
                _origSetAttr.call(this, name, value);
            }
        };
    }

    // ─────────────────────────────────────────────────────────────────────────
    // 改善文書c Section 9: メディアアセット ライフサイクル管理（Media Lifecycle Guard）
    // DOM から削除された audio / video 要素の blob: src を MutationObserver で自動解放し、
    // メモリリークを防ぐ。
    // NOTE: かつて存在した IntersectionObserver(lazy loading) / _blobMap(img-video blob 追跡) /
    //   URL.createObjectURL フックは、いずれも配線されたことが一度もない never-activated な
    //   設計残骸 (vestigial) だった (git -S で _blobMap.set / _intersectionObserver.observe /
    //   data-deferred-src の設定箇所が全履歴で不在を確認) ため除去した。createObjectURL は
    //   要素参照を取れず _blobMap を populate できない構造的に未完の実装で、img/video の
    //   blob 追跡分岐は常に dead だった。実機能していた audio/video の el.src 解放のみ残す。
    // ─────────────────────────────────────────────────────────────────────────
    function installMediaLifecycleGuard() {
        'use strict';

        // MutationObserver: DOM 削除時に audio/video の blob: src を解放
        const _removalObserver = new MutationObserver(function(mutations) {
            mutations.forEach(function(m) {
                m.removedNodes.forEach(function(node) {
                    if (!node || node.nodeType !== 1) { return; }
                    _releaseMediaNode(node);
                    if (node.querySelectorAll) {
                        node.querySelectorAll('audio, video').forEach(_releaseMediaNode);
                    }
                });
            });
        });

        function _releaseMediaNode(el) {
            if (!el || el.nodeType !== 1) { return; }
            const tag = el.tagName;
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
    }

    return { installLayoutThrashingGuard, installMediaLifecycleGuard };
}
