    (function() {
        'use strict';
        // Known browser extension / messaging infrastructure error patterns.
        // These are NOT caused by portfolio code — they originate from Chrome
        // extension content scripts whose message channels close before responding.
        // We must register this suppressor here (head, blocking) because the
        // unhandledrejection fires at portfolio/:1 (document start) before the
        // main error handler at the bottom of the page is registered.
        var SUPPRESS_PATTERNS = [
            'message channel closed',
            'asynchronous response',
            'A listener indicated',
            'The message port closed'
        ];
        window.addEventListener('unhandledrejection', function(ev) {
            try {
                var reason = ev && ev.reason;
                var msg = reason
                    ? (reason.message || (typeof reason === 'string' ? reason : ''))
                    : '';
                var stack = (reason && reason.stack) ? reason.stack : '';
                var haystack = msg + '\n' + stack;
                for (var i = 0; i < SUPPRESS_PATTERNS.length; i++) {
                    if (haystack.indexOf(SUPPRESS_PATTERNS[i]) !== -1) {
                        ev.preventDefault();
                        return;
                    }
                }
            } catch (e) { /* never propagate from suppressor */ }
        });
    })();
