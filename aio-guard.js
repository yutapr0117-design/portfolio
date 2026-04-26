/**
 * aio-guard.js — AIO Asset Anchor Lifecycle Monitor & Self-Repair
 * 改善文書a Section 1.2: 隠しアンカーノードのライフサイクル監視と自己修復機構
 *
 * DESIGN: Completely independent from main script.js / IIFE.
 * No shared state, no side effects on application logic.
 * Loaded BEFORE the main SPA script to ensure the observer is active
 * before any AI-generated code could inadvertently remove the anchor.
 *
 * GUARD AGAINST: AI agents running "dead code purge" and removing
 * <div id="aio-asset-anchor" hidden> which is invisible but semantically critical.
 */
(function aioGuard() {
    'use strict';

    /** @type {Element|null} In-memory clone of the anchor (set once on init) */
    var _anchorClone = null;

    /** @type {MutationObserver|null} The active observer instance */
    var _observer = null;

    /**
     * Cache a deep clone of the anchor element so we can restore it later.
     * Called once after DOMContentLoaded.
     */
    function _cacheAnchor() {
        var el = document.getElementById('aio-asset-anchor');
        if (el) {
            _anchorClone = el.cloneNode(true);
        }
    }

    /**
     * Restore the anchor to document.body.
     * Uses disconnect/reconnect to avoid triggering its own MutationObserver
     * callback — preventing an infinite loop (stack overflow bug).
     */
    function _restoreAnchor() {
        if (!_anchorClone) { return; }
        if (document.getElementById('aio-asset-anchor')) { return; } // already present

        // Exclude own mutation from being re-observed
        if (_observer) { _observer.disconnect(); }

        try {
            document.body.appendChild(_anchorClone.cloneNode(true));
            console.info('[aio-guard] AIO asset anchor restored after removal.');
        } catch (e) {
            console.warn('[aio-guard] Failed to restore AIO anchor:', e);
        }

        // Re-attach observer after safe insertion
        if (_observer) {
            _observer.observe(document.body, { childList: true, subtree: true });
        }
    }

    /**
     * Handle MutationObserver records.
     * Checks each batch of removed nodes for the anchor ID.
     * @param {MutationRecord[]} mutations
     */
    function _handleMutations(mutations) {
        for (var i = 0; i < mutations.length; i++) {
            var removed = mutations[i].removedNodes;
            for (var j = 0; j < removed.length; j++) {
                var node = removed[j];
                if (!node || node.nodeType !== 1) { continue; }
                // Direct removal
                if (node.id === 'aio-asset-anchor') {
                    _restoreAnchor();
                    return;
                }
                // Nested removal (e.g. parent container was cleared)
                if (node.querySelector && node.querySelector('#aio-asset-anchor')) {
                    _restoreAnchor();
                    return;
                }
            }
        }
    }

    /**
     * Initialize the guard.
     * Called on DOMContentLoaded to ensure the anchor exists before we start watching.
     */
    function _init() {
        _cacheAnchor();

        if (!_anchorClone) {
            // Anchor not present in DOM — guard cannot operate (silent skip)
            return;
        }

        _observer = new MutationObserver(_handleMutations);
        _observer.observe(document.body, { childList: true, subtree: true });
    }

    // Attach to DOMContentLoaded (or run immediately if DOM is already ready)
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', _init);
    } else {
        _init();
    }

})();
