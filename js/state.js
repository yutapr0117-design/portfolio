/**
 * js/state.js — UI/data state manager (Proxy-wrapped, subscriber-pattern, cross-tab sync)
 * (v80+ Stage 5-h extraction via factory pattern)
 *
 * main.js の `State` IIFE モジュールを依存注入（factory pattern）で物理分割した葉モジュール。
 * Brand / Store と同じく、CONSTANTS / Store / Storage / Toast への closure 依存を `createState`
 * 関数の引数で受け取ることで、葉契約（Check 47c: import ゼロ）を維持しつつ State の挙動と
 * 公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   { get, set, update, subscribe, saveNow }
 *
 * 【依存（引数で注入）】
 *   - CONSTANTS: { DEBUG, TAB_ID, STORAGE_KEY, DEBOUNCE_DELAY }
 *   - Store: { load() }
 *   - Storage: { set(key, value) }
 *   - Toast: { show(message, type?, durationMs?) }
 *
 * 【非破壊性】
 *   - Proxy 型安全モニターの挙動・Type-guard の判定基準は不変
 *   - subscriber 配列の add/remove と notify の順序も不変
 *   - localStorage への save debounce (CONSTANTS.DEBOUNCE_DELAY) と visibilitychange での
 *     saveNow / cross-tab storage event handling も不変
 *   - 既存テスト（Playwright spec の 5-layer proxy / context override 等）が緑のまま
 *
 * 【副作用（既存挙動と等価）】
 *   - module load 時に document.addEventListener('visibilitychange', ...) と
 *     window.addEventListener('storage', ...) を登録する
 *   - これは main.js IIFE 内の元の登録タイミングと等価（早期に解決される ESM import 文の
 *     ガラの即時評価 ≈ 元の IIFE 即時実行）
 */
export function createState({ CONSTANTS, Store, Storage, Toast }) {
    // 改善文書b 8.1 / 改善文書a 3.3: Proxy型安全モニター
    // appsData内のプリミティブ値への型不一致代入を検知・拒否し、
    // 状態変更時にカスタムイベントを自動発火して再描画漏れを防ぐ。
    // 既存のState.update() API・データ構造には一切変更を加えない（非破壊）。
    function _wrapWithProxy(obj, path) {
        if (!obj || typeof obj !== 'object') { return obj; }
        return new Proxy(obj, {
            get(target, prop) {
                if (
                    typeof prop === 'string' &&
                    !(prop in target) &&
                    prop !== 'then' && prop !== 'toJSON' && prop !== Symbol.toPrimitive
                ) {
                    if (CONSTANTS.DEBUG) {
                        console.warn('[State Proxy] Undefined key accessed: "' + path + '.' + prop + '"');
                    }
                }
                const val = Reflect.get(target, prop);
                if (val && typeof val === 'object' && !Array.isArray(val)) {
                    return _wrapWithProxy(val, path + '.' + String(prop));
                }
                return val;
            },
            set(target, prop, value) {
                const existing = target[prop];
                // Type guard: only applies to non-null primitives
                if (
                    existing !== undefined && existing !== null &&
                    value !== undefined && value !== null &&
                    typeof existing !== typeof value &&
                    typeof existing !== 'object'
                ) {
                    console.error(
                        '[State Proxy] Blocked type mismatch at "' + path + '.' + String(prop) +
                        '": expected ' + typeof existing + ', got ' + typeof value
                    );
                    return false;
                }
                const ok = Reflect.set(target, prop, value);
                if (ok && typeof prop === 'string') {
                    try {
                        window.dispatchEvent(new CustomEvent('appStateChanged', {
                            detail: { path: path + '.' + prop, value }
                        }));
                    } catch { /* non-fatal */ }
                }
                return ok;
            }
        });
    }

    let data = Store.load();
    let saveTimer = null;
    let callbacks = [];

    // Toast Storm (通知スパム) 防止用のタイムスタンプ
    let lastStorageErrorTime = 0;
    function notifyStorageError() {
        const now = Date.now();
        if (now - lastStorageErrorTime > 60000) { // 警告は1分に1回まで
            // beforeunload/visibilitychange 経由ではToastが描画されない場合があるため両方記録
            console.error('[State] ストレージ上限のため保存に失敗しました。');
            Toast.show('ストレージ上限のため保存に失敗しました。不要なデータを削除してください。', 'error', 5000);
            lastStorageErrorTime = now;
        }
    }

    function get() {
        return data;
    }

    function set(newData) {
        data = { ...newData, lastModified: Date.now(), modifiedBy: CONSTANTS.TAB_ID };
        notify();
        scheduleSave();
    }

    function cloneProject(p) {
        const src = p || {};
        return {
            ...src,
            outcome: src.outcome ? {
                ...src.outcome,
                metrics: Array.isArray(src.outcome.metrics)
                    ? src.outcome.metrics.map(m => (m && typeof m === 'object') ? { ...m } : m).slice()
                    : []
            } : src.outcome,
            tech: Array.isArray(src.tech) ? src.tech.slice() : [],
            tags: Array.isArray(src.tags) ? src.tags.slice() : [],
            highlights: Array.isArray(src.highlights) ? src.highlights.slice() : [],
            architecture: src.architecture ? { ...src.architecture } : src.architecture,
            relatedProjectIds: Array.isArray(src.relatedProjectIds) ? src.relatedProjectIds.slice() : [],
            links: Array.isArray(src.links) ? src.links.map(l => (l && typeof l === 'object') ? { ...l } : l).slice() : []
        };
    }

    function cloneProjects(projects) {
        return Array.isArray(projects) ? projects.map(cloneProject) : [];
    }

    function cloneAppsData(appsData) {
        const a = appsData || {};
        const cloneArrObjects = (arr) => Array.isArray(arr) ? arr.map(x => (x && typeof x === 'object') ? { ...x } : x) : [];

        const pomodoro = a.pomodoro ? {
            ...a.pomodoro,
            history: cloneArrObjects(a.pomodoro.history),
            settings: a.pomodoro.settings ? { ...a.pomodoro.settings } : { work: 25, short: 5, long: 15 },
            runtime: a.pomodoro.runtime ? { ...a.pomodoro.runtime } : { isActive: false, mode: 'work', endAtMs: null, remainingSec: 1500, linkedTaskId: null }
        } : { history: [], settings: { work: 25, short: 5, long: 15 }, runtime: { isActive: false, mode: 'work', endAtMs: null, remainingSec: 1500, linkedTaskId: null } };

        return {
            ...a,
            tasks: cloneArrObjects(a.tasks),
            todos: cloneArrObjects(a.todos),
            pomodoro,
            ai: a.ai ? { ...a.ai, history: cloneArrObjects(a.ai.history) } : { history: [] },
        };
    }

    function deepFreezeLimited(obj, depth = 3, seen = new WeakSet()) {
        if (!obj || typeof obj !== 'object') {return obj;}
        if (seen.has(obj)) {return obj;}
        seen.add(obj);
        try { Object.freeze(obj); } catch { return obj; }
        if (depth <= 0) {return obj;}
        for (const k of Object.keys(obj)) {
            const v = obj[k];
            if (v && typeof v === 'object') {deepFreezeLimited(v, depth - 1, seen);}
        }
        return obj;
    }

    function update(fn) {
        // Safe-ish "mutable draft" update:
        // - clone commonly-mutated branches deeply enough to avoid shared references
        // - in DEBUG, deep-freeze the current state to catch accidental writes
        const draft = {
            ...data,
            profile: data.profile ? { ...data.profile } : data.profile,
            projects: cloneProjects(data.projects),
            projectPrefs: data.projectPrefs
                ? { ...data.projectPrefs, hiddenIds: Array.isArray(data.projectPrefs.hiddenIds) ? data.projectPrefs.hiddenIds.slice() : [] }
                : { hiddenIds: [] },
            appsData: cloneAppsData(data.appsData)
        };

        if (CONSTANTS.DEBUG) {
            // Catch accidental writes to the original state (best-effort, bounded depth)
            try { deepFreezeLimited(data, 4); } catch { }
        }

        fn(draft);
        set(draft);
    }

    function subscribe(callback) {
        callbacks.push(callback);
        return () => {
            callbacks = callbacks.filter(cb => cb !== callback);
        };
    }

    function notify() {
        callbacks.forEach(cb => {
            try { cb(data); } catch (e) { }
        });
    }

    function scheduleSave() {
        if (saveTimer) {clearTimeout(saveTimer);}
        saveTimer = setTimeout(() => {
            const success = Storage.set(CONSTANTS.STORAGE_KEY, JSON.stringify(data));
            if (!success) {notifyStorageError();}
            saveTimer = null;
        }, CONSTANTS.DEBOUNCE_DELAY);
    }

    function saveNow() {
        if (saveTimer) {clearTimeout(saveTimer);}
        const success = Storage.set(CONSTANTS.STORAGE_KEY, JSON.stringify(data));
        if (!success) {notifyStorageError();}
    }

    // Auto-save on visibility change
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'hidden') {saveNow();}
    });
    // [NOTE] beforeunload is deprecated for reliable state saving on mobile, rely on visibilitychange.

    // Cross-tab sync
    window.addEventListener('storage', (e) => {
        if (e.key === CONSTANTS.STORAGE_KEY && e.newValue) {
            try {
                const incoming = JSON.parse(e.newValue);
                // Ignore writes originating from this tab
                if (incoming.modifiedBy === CONSTANTS.TAB_ID) {return;}
                if (incoming.lastModified > data.lastModified) {
                    data = incoming;
                    notify();
                    Toast.show('別タブで更新されました', 'info');
                }
            } catch { }
        }
    });

    return { get, set, update, subscribe, saveNow };
}
