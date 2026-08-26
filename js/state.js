/**
 * js/state.js — UI/data state manager (clone-on-update isolation, subscriber-pattern, cross-tab sync)
 * (v80+ Stage 5-h extraction via factory pattern)
 *
 * main.js の `State` IIFE モジュールを依存注入（factory pattern）で物理分割した葉モジュール。
 * Brand / Store と同じく、CONSTANTS / Store / Storage / Toast への closure 依存を `createState`
 * 関数の引数で受け取ることで、葉契約（Check 47c: import ゼロ）を維持しつつ State の挙動と
 * 公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API】
 *   { get, set, update, updateSilently, subscribe, saveNow }
 *   updateSilently は live-input (notes/quiz search) 用に notify せず persist する（再描画で
 *   focused input が破棄される focus-loss を防ぐ。呼び出し側が sub-DOM を手動更新する契約）。
 *
 * 【依存（引数で注入）】
 *   - CONSTANTS: { DEBUG, TAB_ID, STORAGE_KEY, DEBOUNCE_DELAY, SCHEMA_VERSION }
 *   - Store: { load(), validateAndNormalize() }  ← cross-tab 採用時に load() と同じ正規化を通す
 *   - Storage: { set(key, value) }
 *   - Toast: { show(message, type?, durationMs?) }
 *
 * 【非破壊性】
 *   - update() の clone-on-write（commonly-mutated ブランチを深くクローン）+ DEBUG 時の
 *     deep-freeze による状態隔離の挙動は不変
 *   - subscriber 配列の add/remove と notify の順序も不変
 *   - localStorage への save debounce (CONSTANTS.DEBOUNCE_DELAY) と visibilitychange での
 *     saveNow は不変。cross-tab storage event handling は Stage 5-h 抽出時は byte-equivalent
 *     だったが、後の bug-fix で「採用前に load() と同じ schema 検証 + validateAndNormalize を通す」
 *     よう変更済 (別バージョン tab の未正規化 store を raw 採用して render crash する #93 class を封じる)
 *   - 既存の Playwright behavior テスト（state 永続・cross-tab・schema-mismatch 等）が緑のまま
 *
 * 【副作用（既存挙動と等価）】
 *   - module load 時に document.addEventListener('visibilitychange', ...) と
 *     window.addEventListener('storage', ...) を登録する
 *   - これは main.js IIFE 内の元の登録タイミングと等価（早期に解決される ESM import 文の
 *     ガラの即時評価 ≈ 元の IIFE 即時実行）
 */
export function createState({ CONSTANTS, Store, Storage, Toast }) {
    let data = Store.load();

    // [FIX] スキーマ移行で全データが既定へ戻ったことを伝える。消えたことと復元できること
    // の両方を言わないと復元導線に辿り着けない (経緯は e2e/resilience.spec.js)。
    const _migration = Store.takeMigrationNotice ? Store.takeMigrationNotice() : null;
    if (_migration) {
        setTimeout(() => {
            Toast.show(
                `データ形式が変わったため表示を初期化しました（v${_migration.from}→v${_migration.to}）。`
                + '以前のデータは Settings のスナップショットから復元できます。',
                'warning', 12000);
        }, 0);
    }

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
            settings: a.pomodoro.settings ? { ...a.pomodoro.settings } : { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS },
            runtime: a.pomodoro.runtime ? { ...a.pomodoro.runtime } : { isActive: false, mode: 'work', endAtMs: null, remainingSec: CONSTANTS.POMODORO_DEFAULT_REMAINING_SEC, linkedTaskId: null }
        } : { history: [], settings: { ...CONSTANTS.POMODORO_DEFAULT_SETTINGS }, runtime: { isActive: false, mode: 'work', endAtMs: null, remainingSec: CONSTANTS.POMODORO_DEFAULT_REMAINING_SEC, linkedTaskId: null } };

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

    // Safe-ish "mutable draft": clone commonly-mutated branches deeply enough to avoid shared
    // references with the live state, so callers can mutate the draft freely.
    function _buildDraft() {
        return {
            ...data,
            profile: data.profile ? { ...data.profile } : data.profile,
            projects: cloneProjects(data.projects),
            projectPrefs: data.projectPrefs
                ? { ...data.projectPrefs, hiddenIds: Array.isArray(data.projectPrefs.hiddenIds) ? data.projectPrefs.hiddenIds.slice() : [] }
                : { hiddenIds: [] },
            appsData: cloneAppsData(data.appsData)
        };
    }

    function update(fn) {
        const draft = _buildDraft();
        if (CONSTANTS.DEBUG) {
            // Catch accidental writes to the original state (best-effort, bounded depth)
            try { deepFreezeLimited(data, 4); } catch { }
        }
        fn(draft);
        set(draft);
    }

    // High-frequency live-input persistence WITHOUT a full re-render. set() → notify() drives
    // State.subscribe(render), and render() clear()s #content and rebuilds the page — which
    // destroys the focused input on every keystroke (a confirmed focus-loss bug on the quiz
    // search and Markdown notes inputs). For inputs that must persist on each keystroke while
    // keeping focus, commit the draft + schedule a save but DO NOT notify. Callers MUST update
    // their own affected sub-DOM manually (cf. ProjectsPage's renderGrid / NotesPage's manual
    // preview), because no render will fire to reflect the change.
    function updateSilently(fn) {
        const draft = _buildDraft();
        if (CONSTANTS.DEBUG) {
            try { deepFreezeLimited(data, 4); } catch { }
        }
        fn(draft);
        data = { ...draft, lastModified: Date.now(), modifiedBy: CONSTANTS.TAB_ID };
        scheduleSave();
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

    // ===== Cross-tab 採用の延期機構 =====
    // 採用 (validateAndNormalize + notify) を 1 箇所に集約し、編集中は blur まで待つ。
    // pending は最後の 1 件のみ保持する (中間状態を順に適用する意味は無く、最新が正)。
    let _pendingIncoming = null;
    let _pendingBlurTarget = null;

    function _adopt(incoming) {
        // [FIX] 稼働中のポモドーロは **自タブ固有の実行状態**。別タブは「未起動」の runtime を
        //   持つのが普通なので丸ごと採用すると **走っているタイマーが黙って止まる**
        //   (利用者からは「別タブで作業していたら消えていた」としか見えない)。
        //   採用自体は行い runtime だけ引き継ぐ。実測と経緯は e2e/apps-pomodoro.spec.js。
        const _running = data && data.appsData && data.appsData.pomodoro
            && data.appsData.pomodoro.runtime && data.appsData.pomodoro.runtime.isActive
            ? data.appsData.pomodoro.runtime : null;
        data = Store.validateAndNormalize(incoming);
        if (_running && data.appsData && data.appsData.pomodoro) {
            data.appsData.pomodoro.runtime = _running;
        }
        notify();
        Toast.show('別タブで更新されました', 'info');
    }

    function _isEditingElement(el) {
        if (!el) { return false; }
        if (el.isContentEditable) { return true; }
        const tag = el.tagName;
        if (tag === 'TEXTAREA') { return true; }
        if (tag !== 'INPUT') { return false; }
        // ボタン系 input は「編集中」ではない (押下で focus が乗るだけ)
        return !['button', 'submit', 'reset', 'checkbox', 'radio', 'file'].includes(
            (el.type || 'text').toLowerCase());
    }

    function _deferIfEditing(incoming) {
        const el = document.activeElement;
        if (!_isEditingElement(el)) { return false; }
        _pendingIncoming = incoming;
        if (_pendingBlurTarget !== el) {
            _pendingBlurTarget = el;
            el.addEventListener('blur', () => {
                _pendingBlurTarget = null;
                const pending = _pendingIncoming;
                _pendingIncoming = null;
                // blur までに自タブが更に書いていれば古い incoming は捨てる (last-writer-wins を維持)
                if (pending && pending.lastModified > data.lastModified) { _adopt(pending); }
            }, { once: true });
        }
        return true;
    }

    // Cross-tab sync
    window.addEventListener('storage', (e) => {
        if (e.key === CONSTANTS.STORAGE_KEY && e.newValue) {
            try {
                const incoming = JSON.parse(e.newValue);
                // Ignore writes originating from this tab
                if (incoming.modifiedBy === CONSTANTS.TAB_ID) {return;}
                if (incoming.lastModified > data.lastModified) {
                    // [FIX] 別タブが書いた store を生のまま採用しない。load() / import が必ず通す
                    // 正規化を cross-tab だけが省いており、別バージョン (デプロイ跨ぎで 2 タブ) が書いた
                    // 異 schema / 欠損フィールドの store を raw 採用 → render が未定義参照で FatalPage
                    // crash する (#93 と同 class = 未正規化外部データの取り込み)。load() と同じく
                    // schema 不一致は採用を見送り (現タブの正常 state を保持＝非破壊・データ欠落なし)、
                    // 一致時のみ validateAndNormalize で欠損を backfill してから採用する。
                    if (incoming.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {return;}
                    // [FIX] 入力中は採用を blur まで延期する。採用は notify() = #content 全再描画を
                    //   伴うため、そのまま適用すると **利用者が今書いているテキストと focus が消える**
                    //   (実測: 別タブでタスクを 1 件追加しただけで、こちらのタブの notes 編集中テキストが
                    //   巻き戻り activeElement が body へ落ちた)。#258 の「再描画が focused input を
                    //   破棄する」class が、自分のキーストロークではなく外部イベント起点で起きていた。
                    //   延期しても失うものは無い: 採用は blur 時に lastModified を再判定して行う。
                    if (_deferIfEditing(incoming)) {return;}
                    _adopt(incoming);
                }
            } catch { }
        }
    });

    return { get, set, update, updateSilently, subscribe, saveNow };
}
