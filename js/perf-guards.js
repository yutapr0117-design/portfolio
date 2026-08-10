/**
 * js/perf-guards.js — Performance guard (Media Lifecycle)
 * (v80+ Stage 5-s extraction via factory pattern)
 *
 * main.js のパフォーマンスガード IIFE を依存注入なしの factory pattern で物理分割した
 * 葉モジュール。外部依存は一切ない（DOM API のみ）。
 *
 * 【公開 API】
 *   const perfGuards = createPerfGuards();
 *   perfGuards.installMediaLifecycleGuard();
 *
 * 【依存（引数で注入）】
 *   なし — DOM API（MutationObserver / Element）のみを使用する。葉契約（Check 47c: import ゼロ）と
 *   合致する。
 *
 * 【かつてあった Layout Thrashing Guard を除去した理由（2026-08-10）】
 *   `CSSStyleDeclaration.prototype.setProperty` と `Element.prototype.setAttribute('style', …)` を
 *   上書きし、書き込みを rAF まで遅延バッチする hook を持っていた。狙いは「素朴な同期スタイル
 *   書き込みループの透過的な最適化」だったが、**一度も発火していなかった**。
 *   - 実測（15 ルート走査 + drawer/palette/theme/入力の対話）で **setProperty 0 回 /
 *     setAttribute('style') 0 回**。shipped JS は例外なく `el.style.x = …` か `style.cssText` を
 *     使い、hook 自身の NOTE が明記するとおり**直接代入は hook 対象外**だったため。
 *   - 一方コストは実在した: (i) アプリの**全** `setAttribute` 呼び出し（ARIA 更新など hot path）に
 *     ラッパーが 1 段挟まる、(ii) `removeProperty` は hook されないので
 *     `setProperty(x,v)` → `removeProperty(x)` の順で書くと**順序が反転して x が設定されたまま残る**、
 *     (iii) DOM API が標準と異なる意味論になる。
 *   - 実害も出た: e2e で候補 CSS を当てて同期で読む診断が**全て偽陰性**になり、
 *     「要素を隠しても幅が変わらない ＝ コンテンツは無関係」と誤結論しかけた（1 サイクル分を無効化）。
 *   利益ゼロ・実コストあり・診断を壊す、の三点で除去した。#261 で同ファイルの
 *   never-activated な vestigial（IntersectionObserver / _blobMap / createObjectURL フック）を
 *   除去したのと同じ判断を、一段深い層に適用したもの。
 *
 * 【非破壊性】
 *   - Media Lifecycle Guard は MutationObserver による audio/video の blob: src 解放のみ機能。
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 */
export function createPerfGuards() {
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

    return { installMediaLifecycleGuard };
}
