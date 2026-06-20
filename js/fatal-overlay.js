/**
 * js/fatal-overlay.js — Fatal error overlay + Global Safety Net
 * (v80+ Stage 5-r extraction via factory pattern)
 *
 * main.js の Fatal Overlay 機構（_normalizeError / _isViewTransitionError /
 * _isFatalError + window addEventListener('error'/'unhandledrejection') ハンドラー +
 * _installGlobalSafetyNet IIFE による Shadow DOM フォールバック UI）を依存注入で
 * 物理分割した葉モジュール。
 *
 * 【公開 API（呼び出し側 main.js からの形）】
 *   const fatalOverlay = createFatalOverlay({ render });
 *   fatalOverlay.install();  // window event listener + safety net setInterval を登録
 *   戻り値は { install, _normalizeError, _isViewTransitionError, _isFatalError }。install が主 API
 *   で、`_`接頭辞の 3 helper は main.js IIFE 側の合成 (executeSafeTransition / render 等) が
 *   同じエラー分類ロジックを再利用するために返している internal-composition export（外部公開意図はない）。
 *
 * 【依存（引数で注入）】
 *   - render: main.js の render 関数（Fatal 発生時に再描画を試みる）
 *
 * 【副作用】
 *   - install() 呼び出し時に:
 *     - window.__fatalError = null を初期化
 *     - window.addEventListener('error', ...) を登録
 *     - window.addEventListener('unhandledrejection', ...) を登録
 *     - setInterval で 2秒ごとに window.__fatalError をチェックして Shadow DOM safety net を出す
 *   - これらは元 main.js IIFE 評価時の即時実行と等価
 *
 * 【非破壊性】
 *   - エラー判定ロジック（_isFatalError / _isViewTransitionError）は byte-equivalent
 *   - Shadow DOM safety net の DOM 構造・CSS・テキストは byte-equivalent
 *   - sessionStorage への error context 退避（client-side telemetry only・PII 不保存）も不変
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 */
export function createFatalOverlay({ render }) {
    // ===== Fatal overlay (global error capture) =====
    // ヘルパー 3 関数は factory closure 直下に置き、戻り値で main.js scope にも公開する。
    // executeSafeTransition / render など main.js IIFE 内の他箇所から参照されるため。

    /**
     * v58: エラーを「本当に致命的か」で分類するヘルパー。
     *
     * 非致命的として扱うケース（fatalオーバーレイを出さない）:
     *   - View Transition 関連の DOMException
     *     (InvalidStateError / AbortError / "Transition was aborted" メッセージ)
     *   - startViewTransition の Promise 競合由来のエラー
     *
     * これらはアプリのデータや状態には影響しないため、
     * コンソール警告に留め、ユーザーに致命的エラーとして見せない。
     */
    function _normalizeError(input) {
        if (!input) { return new Error('Unknown error'); }
        if (input instanceof Error) { return input; }
        if (typeof input === 'string') { return new Error(input); }
        try {
            return new Error(JSON.stringify(input));
        } catch {
            return new Error(String(input));
        }
    }

    function _isViewTransitionError(err) {
        const e = _normalizeError(err);
        const name = e && e.name ? String(e.name) : '';
        const msg = e && e.message ? String(e.message) : '';
        const stack = e && e.stack ? String(e.stack) : '';
        const haystack = `${name}\n${msg}\n${stack}`;
        return (
            name === 'InvalidStateError' ||
            name === 'AbortError' ||
            haystack.includes('Transition was aborted') ||
            haystack.includes('startViewTransition') ||
            haystack.includes('view transition') ||
            haystack.includes('ViewTransition') ||
            // Chrome拡張のメッセージチャンネルエラー（ポートフォリオ起因でない）
            haystack.includes('message channel closed') ||
            haystack.includes('asynchronous response') ||
            haystack.includes('A listener indicated')
        );
    }

    function _isFatalError(err) {
        if (!err) { return false; }
        if (_isViewTransitionError(err)) { return false; }
        return true;
    }

    function install() {
        window.__fatalError = null;
        window.addEventListener('error', (ev) => {
            try {
                const err = ev && ev.error ? ev.error : new Error(ev && ev.message ? String(ev.message) : 'Unknown error');
                if (!_isFatalError(err)) {
                    console.warn('[portfolio] non-fatal error suppressed:', err);
                    return;
                }
                window.__fatalError = err;
            } catch (e) {
                window.__fatalError = e;
            }
            try { render(); } catch { }
        });

        window.addEventListener('unhandledrejection', (ev) => {
            try {
                const err = _normalizeError(ev && 'reason' in ev ? ev.reason : new Error('Unhandled rejection'));
                if (!_isFatalError(err)) {
                    ev.preventDefault(); // 非致命的エラーはブラウザ出力ごと抑制
                    return;
                }
                window.__fatalError = err;
            } catch (e) {
                window.__fatalError = e;
            }
            try { render(); } catch { }
        });

        // 改善文書c Section 6: グローバル・セーフティネット
        // Shadow DOM を使ってメインCSSと完全に隔離されたフォールバックUIを提示する。
        // すべての改善のうち最後に起動するため、他のすべての防御レイヤーをすり抜けた
        // 「サイレント・フェイラー」を捕捉できる最終安全網として機能する。
        (function _installGlobalSafetyNet() {
            let _safetyNetShown = false;

            function _showSafetyNet(origin) {
                if (_safetyNetShown) { return; }
                _safetyNetShown = true;

                try {
                    // テレメトリ: エラー情報をsessionStorageに退避（非同期レポートの準備）
                    try {
                        // codeql[js/clear-text-storage-of-sensitive-data] - False positive:
                        // Stores transient client-side error context for local diagnostics only.
                        // No credentials, tokens, or PII are stored.
                        sessionStorage.setItem('portfolio_last_error', JSON.stringify({
                            ts: Date.now(),
                            route: window.location.hash,
                            origin: String(origin || 'unknown')
                        }));
                    } catch { /* storage unavailable — ignore */ }

                    // Shadow DOM でスタイル汚染ゼロのフォールバックUIを構築
                    const host = document.createElement('div');
                    host.id = 'portfolio-safety-net-host';
                    host.style.cssText = 'position:fixed;inset:0;z-index:99998;pointer-events:none;';
                    document.body.appendChild(host);

                    const shadow = host.attachShadow({ mode: 'closed' });

                    const style = document.createElement('style');
                    style.textContent = `
                        :host { all: initial; }
                        .net {
                            position: fixed; inset: 0; display: flex;
                            align-items: center; justify-content: center;
                            background: rgba(2,6,23,0.85);
                            backdrop-filter: blur(4px);
                            font-family: system-ui, sans-serif;
                            pointer-events: auto;
                        }
                        .box {
                            background: #0f172a; color: #e2e8f0;
                            border: 1px solid #334155; border-radius: 12px;
                            padding: 2rem; max-width: 400px; text-align: center;
                        }
                        h2 { font-size: 1.1rem; margin: 0 0 0.75rem; color: #f8fafc; }
                        p  { font-size: 0.875rem; color: #94a3b8; margin: 0 0 1.5rem; line-height: 1.6; }
                        button {
                            background: #6366f1; color: #fff; border: none;
                            border-radius: 8px; padding: 0.6rem 1.4rem;
                            font-size: 0.875rem; font-weight: 600; cursor: pointer;
                        }
                        button:hover { background: #4f46e5; }
                    `;

                    const div = document.createElement('div');
                    div.className = 'net';

                    const box = document.createElement('div');
                    box.className = 'box';

                    const title = document.createElement('h2');
                    title.textContent = '⚠️ アプリを再起動してください';

                    const message = document.createElement('p');
                    message.appendChild(document.createTextNode('予期しないエラーが発生しました。'));
                    message.appendChild(document.createElement('br'));
                    message.appendChild(document.createTextNode('ページを再読み込みすると復旧します。'));

                    const btn = document.createElement('button');
                    btn.id = 'sn-reload';
                    btn.textContent = '再読み込み';

                    box.appendChild(title);
                    box.appendChild(message);
                    box.appendChild(btn);
                    div.appendChild(box);

                    shadow.appendChild(style);
                    shadow.appendChild(div);

                    if (btn) {
                        btn.addEventListener('click', () => {
                            try { sessionStorage.clear(); } catch { /* ignore */ }
                            location.reload();
                        });
                    }
                } catch { /* Safety net itself failed — nothing more we can do */ }
            }

            // 既存のfatal overlayと協調: __fatalErrorが2秒経っても未処理なら安全網を起動
            setInterval(function() {
                if (window.__fatalError && !document.getElementById('portfolio-safety-net-host')) {
                    _showSafetyNet(window.__fatalError);
                }
            }, 2000);
        })();
    }

    return { install, _normalizeError, _isViewTransitionError, _isFatalError };
}
