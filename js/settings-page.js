/**
 * js/settings-page.js — Settings Page (import/export/snapshot/manual project add + normalize)
 *
 * @fileoverview v80+ bloat-reduction (2026-07-05): js/apps.js から SettingsPage を
 * factory pattern で分離した葉モジュール。createApps が肥大化 (837 行) していたため、最大の page
 * (SettingsPage ~373 行) を独立葉へ抽出し apps.js を ~464 行へ縮小する (Check 363 の 1,000 行
 * ハード上限に対する headroom 確保・肥大化「生じないように」の解消側)。
 *
 * SettingsPage は import/export (full/projects/apps/profile)・snapshot (save/restore/clear)・
 * 手動プロジェクト追加・整合性チェック/正規化 (validateAndNormalize) を提供する。private state
 * (settingsImportMode / settingsInclude* / settingsNew*) も factory closure 内へ移動 (揮発性 UI
 * 状態は元と同位置で保持・挙動 byte-equivalent)。
 *
 * export:
 *   createSettingsPage({ deps }) -> { SettingsPage }
 *
 * 【依存（引数で注入）】(葉契約 = ローカル ESM import ゼロ)
 *   - h: js/ui-components.js
 *   - Toast: js/ui-components.js
 *   - State: js/state.js factory instance
 *   - Brand: js/brand.js factory instance (ブランド切替)
 *   - Store: js/store.js factory instance (validateAndNormalize)
 *   - Storage: js/storage.js (snapshot parse/set/remove)
 *   - CONSTANTS: js/constants.js (SNAPSHOT_KEY / SCHEMA_VERSION / LIMITS.PROJECT_NAME)
 *   - generateId, slugify: js/pure-utils.js
 *   - announce: js/ui-components.js (sr-only の唯一の通知チャネル・Check 407 が単一 writer を強制)
 *
 * 不変条件:
 *   - 本モジュールは葉 (ローカル import ゼロ)。依存は createSettingsPage の引数で受け取る。
 *   - restoreSnapshot / importJSON は必ず Store.validateAndNormalize を通す (#93/#295/#561 class:
 *     外部入力 ingestion は全経路正規化)。抽出でこの契約を変えないこと。
 */
export function createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify, announce }) {
    // ===== Component: Settings Page =====
    let settingsImportMode = 'append';
    let settingsIncludeProfile = true;
    let settingsIncludeProjects = true;
    let settingsIncludeApps = true;
    let settingsNewName = '';
    let settingsNewTech = '';
    let settingsNewDemo = '';

    /**
     * lossParts — 正規化で失われた分を数え、利用者に見せる文言の配列を返す。
     *
     * import と snapshot 復元は同じ validateAndNormalize を通すので、報告も同じ言葉で行う
     * (片方だけ honest だと「復元は無事だった」と誤解される)。数えるのは 3 面:
     *   dropped   entry ごと落ちた数 (件数上限 / 必須フィールド欠落)
     *   trimmed   entry は残るが list フィールド (tech/tags/highlights/task.tags) が削られた数
     *   shortened 文字列が文字数上限で短縮された項目数
     * 照合は id で行い、entry ごと落ちた分と二重計上しない。id 衝突で改名された entry は
     * 照合不能で数えないが **過少に出る方向**なので「実際より多く失われた」と誤報しない。
     * b 側を trim して比較するのは profile の safeEmail/safeUrl が trim 後の値を返すため
     * (前後の空白だけで「短縮しました」と誤報しない)。実測値は
     * e2e/apps-settings-import-shape.spec.js に記録。
     */
    function lossParts(before, after) {
        const countOf = (o, k) => (o && Array.isArray(o[k]) ? o[k].length : 0);
        const apps = (o) => (o && o.appsData) || {};
        const byId = (a) => new Map((Array.isArray(a) ? a : []).map((x) => [x && x.id, x]));
        const listLen = (o) => (Array.isArray(o) ? o.length : 0);

        const dropped = ['tasks', 'todos'].reduce(
            (n, k) => n + Math.max(0, countOf(apps(before), k) - countOf(apps(after), k)), 0)
            + Math.max(0, listLen(before.projects) - listLen(after.projects))
            + ['ai', 'pomodoro'].reduce((n, k) => n + Math.max(0,
                countOf(apps(before)[k], 'history') - countOf(apps(after)[k], 'history')), 0);

        const trimmedIn = (b0, a0, fields) => {
            const m = byId(a0);
            return (Array.isArray(b0) ? b0 : []).reduce((n, b) => {
                const a = b && m.get(b.id);
                if (!a) { return n; }
                return n + fields.reduce((k, f) => k + Math.max(0, countOf(b, f) - countOf(a, f)), 0);
            }, 0);
        };
        const trimmed = trimmedIn(before.projects, after.projects, ['tech', 'tags', 'highlights'])
            + trimmedIn(apps(before).tasks, apps(after).tasks, ['tags']);

        const shortenedObj = (b, a) => Object.keys(b || {}).reduce((n, k) => n
            + (typeof b[k] === 'string' && typeof (a || {})[k] === 'string'
                && a[k].length < b[k].trim().length ? 1 : 0), 0);
        const shortenedIn = (b0, a0) => {
            const m = byId(a0);
            return (Array.isArray(b0) ? b0 : []).reduce((n, b) => {
                const a = b && m.get(b.id);
                return a ? n + shortenedObj(b, a) : n;
            }, 0);
        };
        const shortened = shortenedIn(before.projects, after.projects)
            + shortenedIn(apps(before).tasks, apps(after).tasks)
            + shortenedIn(apps(before).todos, apps(after).todos)
            + shortenedObj(before.profile, after.profile)
            // notes は単一ドキュメントゆえ上限超過で末尾がまるごと消えるが、entry も件数も
            // 減らないため他の 2 面では 0 のままになる。
            + shortenedObj({ notes: apps(before).notes }, { notes: apps(after).notes });

        const parts = [];
        if (dropped > 0) { parts.push(`${dropped} 件は取り込めませんでした`); }
        if (trimmed > 0) { parts.push(`${trimmed} 件のタグ・技術・ハイライトが上限を超えて削られました`); }
        if (shortened > 0) { parts.push(`${shortened} 件の項目が文字数上限で短縮されました`); }
        return parts;
    }

    function SettingsPage() {
        const state = State.get();

        // --- 不足していた関数群の実装 ---
        function getSnapshot() {
            const raw = Storage.parse(CONSTANTS.SNAPSHOT_KEY);
            if (!raw) {return null;}

            // Support both formats:
            // 1) { at, data, ... }  (current)
            // 2) <store object>    (legacy; schema-mismatch snapshot in older versions)
            if (raw && typeof raw === 'object' && raw.data && typeof raw.data === 'object') {
                return raw;
            }

            // Legacy: treat the whole object as store data
            if (raw && typeof raw === 'object' && raw.schemaVersion) {
                return { at: Date.now(), reason: 'legacy-snapshot', data: raw };
            }

            return null;
        }
        function setSnapshot() {
            const snap = { at: Date.now(), data: State.get() };
            const success = Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify(snap));
            if (success) {
                Toast.show('スナップショットを保存しました');
            } else {
                Toast.show('ストレージ上限のため保存に失敗しました。不要なデータを削除してください。', 'error', 5000);
            }
            State.update(s => { }); // 強制再描画
        }
        function restoreSnapshot() {
            const snap = getSnapshot();
            if (!snap || !snap.data) {return;}

            // Safety: refuse obviously wrong shapes
            if (typeof snap.data !== 'object' || !snap.data.schemaVersion) {
                Toast.show('スナップショット形式が不正です', 'error');
                return;
            }

            // If schema differs, still allow restore (user intent), but warn
            if (snap.data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {
                Toast.show(`注意: schemaVersion が一致しません（${snap.data.schemaVersion}→${CONSTANTS.SCHEMA_VERSION}）`, 'warning');
            }

            // [FIX] snapshot data は必ず正規化を通してから採用する (#93/#295 class:
            // 「外部入力 ingestion 経路は全て同じ正規化を通せ」)。importJSON は
            // validateAndNormalize を通すのに restore だけ生 State.set していた未被覆経路。
            // getSnapshot は旧 schema の legacy-snapshot を明示サポートし schema mismatch も
            // 上で warn するため、旧版が保存した欠損/型揺れ snapshot を生採用すると renderer が
            // 期待するフィールド不在で FatalPage crash し得た。normalize が安全側に丸めて防ぐ
            // (valid な snapshot は不変で通過ゆえ非破壊)。
            // [FIX] 復元も正規化で entry / 中身を失うのに **無条件で「復元しました」**と
            //   報告していた。実測 (2026-08-20): 505 件の tasks と 30,000 文字のノートを
            //   持つ snapshot を復元すると 500 件 / 20,000 文字になり **5 件と 10,000 文字が
            //   消える**。snapshot は単一スロット = 利用者の**唯一の復元点**なので、
            //   import 経路より無防備なのは筋が通らない (getSnapshot は旧版が保存した
            //   legacy 形も明示サポートしており、上限が違う版の snapshot は現実に起こりうる)。
            const _norm = Store.validateAndNormalize(snap.data);
            const _parts = lossParts(snap.data, _norm);
            State.set(_norm);
            Toast.show(_parts.length
                ? `スナップショットを復元しました（${_parts.join('・')}）`
                : 'スナップショットを復元しました');
        }
        function clearSnapshot() {
            // [FIX] 破壊的操作の確認ガードを他と対称にする。プロジェクト 1 件の削除
            //   (deleteProject) と全リセット (resetData) は confirm を通すのに、**スナップショット
            //   削除だけが無確認**だった。スナップショットは単一スロットでありユーザーの唯一の
            //   復元点なので、失う影響はむしろプロジェクト 1 件より大きい。「1 ケースだけ処理して
            //   他を忘れる」非対称 (CLAUDE.md §7 の反復 class) がデータ喪失面に残っていたもの。
            //   文言は保存日時を含め「何を失うか」を明示する (単なる『削除しますか？』より判断できる)。
            const _snap = Storage.parse(CONSTANTS.SNAPSHOT_KEY, null);
            const _at = _snap && _snap.at ? new Date(_snap.at).toLocaleString() : null;
            if (!confirm(_at
                ? `スナップショット（保存日時: ${_at}）を削除しますか？\n復元できなくなります。`
                : 'スナップショットを削除しますか？\n復元できなくなります。')) { return; }
            Storage.remove(CONSTANTS.SNAPSHOT_KEY);
            Toast.show('スナップショットを削除しました');
            State.update(s => { }); // 強制再描画
        }

        function downloadJSON(data, filename) {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }
        function exportFull() { downloadJSON(State.get(), `portfolio_full_${Date.now()}.json`); }
        function exportProjects() { downloadJSON(State.get().projects, `portfolio_projects_${Date.now()}.json`); }
        function exportApps() { downloadJSON(State.get().appsData, `portfolio_apps_${Date.now()}.json`); }
        function exportProfile() { downloadJSON(State.get().profile, `portfolio_profile_${Date.now()}.json`); }

        /**
         * _normalizeImportShape — export が書く 4 つの形を full-state 形へ揃える。
         *
         *   full backup      : { schemaVersion, profile, projects, appsData, projectPrefs, theme, … }
         *   Projectsのみ      : [ …projects ]                (素の配列)
         *   AppsDataのみ      : { tasks, todos, pomodoro, ai, … }
         *   Profileのみ       : { name, title, bio, email, … }
         *
         * 判定できない形は null を返し、呼び出し側がエラーを出す (silent no-op を作らない)。
         */
        function _normalizeImportShape(raw) {
            if (Array.isArray(raw)) { return { projects: raw }; }
            if (!raw || typeof raw !== 'object') { return null; }
            const has = (...keys) => keys.some(k => Object.prototype.hasOwnProperty.call(raw, k));
            // full-state 形 (これらのキーを持つなら他の判定より優先)
            if (has('schemaVersion', 'projects', 'appsData', 'profile', 'projectPrefs')) { return raw; }
            if (has('tasks', 'todos', 'pomodoro', 'ai', 'notes', 'quizSearch')) { return { appsData: raw }; }
            if (has('name', 'title', 'bio', 'email', 'github', 'linkedin', 'location')) { return { profile: raw }; }
            return null;
        }

        function importJSON(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const rawParsed = JSON.parse(e.target.result);
                    // [FIX] **部分 export したファイルを import し直せなかった** (実測 #1038)。
                    //   `Projectsのみ` は projects の**素の配列**を、`AppsDataのみ` / `Profileのみ` は
                    //   それぞれの**素のオブジェクト**を書き出すが、import は full-state 形
                    //   (`parsed.projects` 等) しか見ていなかったため、
                    //   **何も起きないのに「インポートが完了しました」と報告**していた。
                    //   バックアップとして提示している機能が「戻せないファイル」を作り、しかも
                    //   成功したと言うのは、失敗するより悪い (利用者は復元できたと信じる)。
                    //   export が実際に書く 4 形をそのまま受け付ける。形は互いに素なので判定は決定的。
                    const parsed = _normalizeImportShape(rawParsed);
                    if (!parsed) {
                        Toast.show('認識できない形式のファイルです', 'error');
                        return;
                    }
                    // [FIX] 外部 JSON を State.update で生のまま commit しない (normalize-before-commit)。
                    // 旧実装は生 parsed を State.update で adopt → notify→render() が走った後で
                    // validateAndNormalize していた。strict モードは `s.projects = parsed.projects` の生代入
                    // ゆえ、生データが render に届く経路があった (malformed entry が SettingsPage の
                    // p.name/p.id dereference を crash させうる)。現状は render の abort ordering (State.set の
                    // 2 度目 render が 1 度目の生 render を SettingsPage 到達前に abort) で偶発的に守られて
                    // いたが、data-safety を incidental な描画順に依存させず、restoreSnapshot と同じ
                    // 「adopt する前に正規化を通せ」(#295/#561 invariant) に importJSON も整合させる。
                    // 現在 state を base にマージした結果を validateAndNormalize してから単一 State.set で
                    // commit することで、生データが render に届く窓を構造的に無くす (Check 374 が再発防止)。
                    const base = State.get();
                    const merged = { ...base };
                    // [FIX] theme は full export に含まれるのに import が無視しており、
                    //   「フルバックアップ」を復元しても表示テーマの設定だけが失われていた
                    //   (実測 #1036: export に theme:'dark' が入っていても import 後は 'system')。
                    //   export が書くキーを import が読まないのは backup 契約の破れ。
                    //   セクション別チェックボックス (Profile/Projects/AppsData) は「データ」の
                    //   区分けなので、表示設定はどれにも属さず常に復元する (値は下の
                    //   validateAndNormalize が既知の enum へ正規化する)。
                    // [FIX] **「対象」で除外された形のファイルを import すると、中身が丸ごと
                    //   捨てられるのに「インポートが完了しました」と報告していた** (実測 #1040)。
                    //   例: `AppsDataのみ` で書き出したファイルを、AppsData のチェックを外した
                    //   状態で読み込むと、タスクは 1 件も置き換わらないのに成功メッセージが出る。
                    //   #1039 で「形を認識できないファイル」の silent no-op は塞いだが、
                    //   **形は認識できるのに選択で全部落ちる**残り半分が空いていた。どちらも
                    //   「バックアップを戻したつもりで戻っていない」に見えるのは同じで、
                    //   利用者が復元できたと信じてしまう点で失敗するより悪い。
                    //   実際に 1 セクションでも適用したかを追跡し、0 件なら成功と言わない。
                    let applied = false;
                    if (typeof parsed.theme === 'string') { merged.theme = parsed.theme; applied = true; }
                    if (settingsIncludeProfile && parsed.profile) { merged.profile = parsed.profile; applied = true; }
                    if (settingsIncludeProjects && Array.isArray(parsed.projects)) {
                        applied = true;
                        if (settingsImportMode === 'strict') {
                            merged.projects = parsed.projects;
                        } else if (settingsImportMode === 'upsert') {
                            // upsert（UI ラベル「更新+追加」）: 既存 id は更新、未知 id は追加。
                            // 1 つの Map に更新も追加も集約することで新規 id も確実に残す (#192 の
                            // 「push 後に Map.values() で上書きして新規を破棄」バグを回避した形を維持)。
                            const map = new Map(base.projects.map(p => [p.id, p]));
                            parsed.projects.forEach(p => map.set(p.id, p));
                            merged.projects = Array.from(map.values());
                        } else {
                            // append（追加のみ）: 未知 id だけ追加し、既存は変更しない。
                            const existing = new Set(base.projects.map(p => p.id));
                            const appended = base.projects.slice();
                            parsed.projects.forEach(p => { if (!existing.has(p.id)) { appended.push(p); } });
                            merged.projects = appended;
                        }
                        // [FIX] 非表示設定 (projectPrefs.hiddenIds) も一緒に復元する。
                        //   これも export には入るのに import が無視しており、backup を戻すと
                        //   **意図的に隠したプロジェクトが再び公開状態になっていた** (実測 #1037)。
                        //   既定プロジェクトは削除できず「非表示」が唯一の非公開手段 (#886) なので、
                        //   単なる表示設定ではなく**公開/非公開の意思**が失われることになる。
                        //   projects セクションのチェックボックスで gate するのは、これが
                        //   「どのプロジェクトを見せるか」という projects 側のデータだから
                        //   (theme のような全体の表示設定とは別扱い)。
                        if (parsed.projectPrefs && Array.isArray(parsed.projectPrefs.hiddenIds)) {
                            merged.projectPrefs = { ...merged.projectPrefs, hiddenIds: parsed.projectPrefs.hiddenIds };
                        }
                    }
                    // [FIX] モードは projects にしか効いておらず、appsData はどのモードでも
                    //   丸ごと置き換えていた。既定の「追加のみ」で取り込むと既存のタスク・
                    //   やること・ノート・履歴が全部消える = **最も安全なつもりの選択が最も
                    //   破壊的**だった。projects と同じ id 併合を tasks/todos にも適用し、
                    //   append で既存優先にした分は silent にせず件数を報告する (実測は e2e)。
                    let _keptOwn = 0;
                    if (settingsIncludeApps && parsed.appsData) {
                        applied = true;
                        const inc = parsed.appsData;
                        if (settingsImportMode === 'strict') {
                            merged.appsData = inc;
                        } else {
                            const mergeById = (b, i) => {
                                if (!Array.isArray(i)) { return b; }
                                const map = new Map((Array.isArray(b) ? b : []).map(x => [x && x.id, x]));
                                i.forEach(x => {
                                    if (!x) { return; }
                                    if (!map.has(x.id) || settingsImportMode === 'upsert') { map.set(x.id, x); }
                                });
                                return Array.from(map.values());
                            };
                            // 併合は spread より **前** に済ませる。後にすると upsert の
                            // `...inc` が tasks/todos を先に上書きし、自分自身と併合して
                            // 既存が消える (実装中に実測で踏んだ)。
                            const baseApps = merged.appsData || {};
                            const _tasks = mergeById(baseApps.tasks, inc.tasks);
                            const _todos = mergeById(baseApps.todos, inc.todos);
                            if (settingsImportMode === 'upsert') {
                                merged.appsData = { ...baseApps, ...inc };
                            } else {
                                // append: tasks/todos 以外は既存を優先し、落とした分を数える。
                                _keptOwn = Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos').length;
                                merged.appsData = { ...baseApps };
                            }
                            merged.appsData.tasks = _tasks;
                            merged.appsData.todos = _todos;
                        }
                    }

                    if (!applied) {
                        Toast.show('「対象」の選択に一致するデータがファイルにありませんでした', 'error');
                        return;
                    }

                    // 正規化してから単一 commit。生データは一切 render に届かない。
                    const normalized = Store.validateAndNormalize(merged);
                    State.set(normalized);

                    // [FIX] **取り込めなかった件数を honest に報告する。**
                    //   正規化は (a) 件数上限 (MAX_TASKS 500 / MAX_TODOS 1000 / MAX_PROJECTS 1000) の
                    //   slice と (b) 必須フィールドを欠く entry の除去、の 2 つで entry を落とすが、
                    //   従来はどちらの場合も無条件に「インポートが完了しました」と報告していた。
                    //   実測 (2026-08-18): 505 件の tasks を含む JSON を取り込むと保存は 500 件で
                    //   **5 件が黙って消え**、メッセージは「完了しました」。バックアップから復元した
                    //   利用者は**失われたことに気付かないまま元データを捨てうる**。
                    //   #1039/#1040 で塞いだ「何もしていないのに成功と言う」の *部分適用* 版で、
                    //   silent なのは同じ。落ちた理由 (上限 / 不正 entry) は利用者にとって同じ
                    //   「取り込まれなかった」なので、件数だけを正直に伝える。
                    const _parts = lossParts(merged, normalized);

                    if (_keptOwn > 0) { _parts.push(`${_keptOwn} 件の項目は「追加のみ」のため既存を残しました`); }
                    Toast.show(_parts.length
                        ? `インポートが完了しました（${_parts.join('・')}）`
                        : 'インポートが完了しました');
                } catch (err) {
                    Toast.show('JSONのパースに失敗しました', 'error');
                }
            };
            // [FIX] onerror も処理する。readAsText は mid-read のファイル消失・リムーバブル
            // メディア/ネットワークドライブ切断等で失敗しうるが、従来 onerror 未処理で silent
            // no-op (無反応) だった。parse 失敗 (onload catch) と同様に明示フィードバックを出す。
            reader.onerror = () => {
                Toast.show('ファイルの読み込みに失敗しました', 'error');
            };
            reader.readAsText(file);
        }

        function addProjectManual() {
            // [A11Y 3.3.1/2.4.3] 検証エラーを Toast だけで伝えると SR は「どの入力が不正か」を判別できず
            //   フォームを探し直すことになる。不正な入力へ aria-invalid を立て focus を移す
            //   (quiz フォーム #913 と同じ扱い。属性 + focus のみ = 視覚描画は不変)。
            const nameEl = document.getElementById('settingsNewName');
            if (!settingsNewName.trim()) {
                if (nameEl) { nameEl.setAttribute('aria-invalid', 'true'); nameEl.focus(); }
                Toast.show('プロジェクト名を入力してください', 'error');
                return;
            }
            if (nameEl) { nameEl.removeAttribute('aria-invalid'); }
            // [FIX] 上限時は断る。task/todo (#1152) と同形で、従来は unshift 後の正規化
            //   slice(0, MAX_PROJECTS) が最古を無通知で捨てていた。詳細は apps-settings.spec.js。
            if (State.get().projects.length >= CONSTANTS.LIMITS.MAX_PROJECTS) {
                Toast.show(`プロジェクトは ${CONSTANTS.LIMITS.MAX_PROJECTS} 件までです。不要なプロジェクトを削除してください`, 'error');
                return;
            }
            // slug は追加後の照合にも使うので update の外で作る (中で宣言すると
            //   スコープ外参照になり `slug is not defined` で FatalPage に落ちる・実測で踏んだ)。
            const newSlug = slugify(settingsNewName);
            State.update(s => {
                // slug 衝突の一意化 (#154) は **store.js の normalize が単一ソース**で行う。
                // #1064 で手動追加も `Store.validateAndNormalize` を通すようにしたため、ここで
                // 同じ処理を持つと二重化になり、実際 mutation-probe で「インラインの重複を外しても
                // 何も壊れない」(= 冗長ガード) と検出された。一意化の責務は store.js に一本化する。
                s.projects.unshift({
                    id: 'p_user_' + generateId().slice(0, 6),
                    slug: newSlug,
                    name: settingsNewName,
                    category: 'User Added',
                    summary: '', problem: '', approach: '',
                    tech: settingsNewTech ? settingsNewTech.split(',').map(t => t.trim()) : [],
                    tags: [],
                    demoRoute: settingsNewDemo || null
                });
            });
            // [DATA] **追加したものを保存される形へ正規化してから確定する**。normalizeProject は
            //   name を LIMITS.PROJECT_NAME、tech を「12 項目・各 LIMITS.CATEGORY 文字」で切るので、
            //   正規化を通さないと **追加直後は入力どおりに見えるのに、リロードで黙って減る**
            //   (実測: Tech 20 個 → 12 個)。件数の制限は maxlength では表現できないため、
            //   入力欄側の上限だけでは揃えられない。import / snapshot 復元と同じ
            //   「adopt する前に正規化を通せ」(#295/#561) を手動追加にも適用する。
            //   境界の定義は store.js に一本化されたままなので、ここに定数は複製しない。
            State.set(Store.validateAndNormalize(State.get()));

            // [FIX] 正規化で **落ちたぶんを honest に報告する**。tech は「12 項目・各
            //   LIMITS.CATEGORY 文字」で切られるが、従来は素の「プロジェクトを追加しました」
            //   だけだった (実測 2026-08-20: 16 件投入 → 12 件保存・1 件目は 120 → 80 文字)。
            //   件数上限は maxlength では表現できないので入力欄側だけでは防げない。
            //   #1143 で import の切り捨てを「完了しました」で済ませないようにしたのと同じ規律。
            const _saved = (State.get().projects.find(p => p.slug === newSlug) || {}).tech || [];
            const _wanted = settingsNewTech ? settingsNewTech.split(',').map(t => t.trim()).filter(Boolean) : [];
            const _dropped = Math.max(0, _wanted.length - _saved.length);
            const _truncated = _saved.filter((t, i) => (_wanted[i] || '').length > t.length).length;
            settingsNewName = ''; settingsNewTech = ''; settingsNewDemo = '';
            Toast.show(_dropped || _truncated
                ? `プロジェクトを追加しました（Tech: ${_dropped ? `${_dropped} 件を取り込めず` : ''}`
                  + `${_dropped && _truncated ? '・' : ''}${_truncated ? `${_truncated} 件を短縮` : ''}しました）`
                : 'プロジェクトを追加しました');
        }

        const defaultProjectIds = new Set(['p01', 'p02', 'p03', 'p04', 'p05', 'p06', 'p07', 'p08', 'p09', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p17', 'p18']);

        function toggleHiddenProject(id) {
            State.update(s => {
                s.projectPrefs = s.projectPrefs || { hiddenIds: [] };
                const idx = s.projectPrefs.hiddenIds.indexOf(id);
                if (idx > -1) {s.projectPrefs.hiddenIds.splice(idx, 1);}
                else {s.projectPrefs.hiddenIds.push(id);}
            });
        }

        // [A11Y 4.1.3] 削除は **破壊的な単体操作なのに唯一無音**だった。並べ替えは announce、
        //   全リセット / スナップショット保存・削除 / 正規化は Toast を出すのに、削除だけが
        //   何も出さない非対称。実測 (2026-08-20): 削除後も通知領域は直前の「プロジェクトを
        //   追加しました」のままで、SR 利用者には**無音どころか誤った内容が残る**。
        //   実際に消えたときだけ報告する (見つからない id を成功と言わない・#1039 class)。
        function deleteProjectHard(id) {
            if (defaultProjectIds.has(id)) {return;}
            if (!confirm('本当に削除しますか？')) {return;}
            let removed = null;
            State.update(s => {
                const target = s.projects.find(p => p.id === id);
                if (!target) {return;}
                removed = target.name;
                s.projects = s.projects.filter(p => p.id !== id);
            });
            if (removed) { Toast.show(`「${removed}」を削除しました`); }
        }

        // [A11Y 4.1.3] 並べ替えは **視覚では分かるが SR には無音**だった。ボタンのアクセシブル名
        //   (「下へ移動：<プロジェクト名>」) は移動後も変わらず、focus も同じボタンへ戻る (#1000) ため、
        //   SR 利用者には **押しても何も起きていないのと区別がつかない**。実測 (2026-08-17) で
        //   `#action-announcement` が空のままだったことを確認した (task のステータス移動 #1107 と同型)。
        //   位置と総数まで読むのは、**一覧を見渡せない利用者には「何番目へ動いたか」が唯一の手がかり**だから。
        //   Toast (視覚ポップアップ) にしないのは、並べ替えが連続操作だから (#1107 と同じ判断)。
        function moveProject(idx, dir) {
            let moved = null;
            State.update(s => {
                if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}
                const temp = s.projects[idx];
                s.projects[idx] = s.projects[idx + dir];
                s.projects[idx + dir] = temp;
                moved = { name: temp.name, pos: idx + dir + 1, total: s.projects.length };
            });
            if (moved) {
                announce(`「${moved.name}」を ${moved.pos} 番目へ移動しました（全 ${moved.total} 件）`);
            }
        }

        function normalizeNow() {
            const norm = Store.validateAndNormalize(State.get());
            State.set(norm);
            Toast.show('正規化を完了しました');
        }

        function resetData() {
            if (!confirm('すべてのデータを初期化しますか？')) {return;}
            State.set(Store.createDefaultStore());
            Toast.show('初期化しました');
        }

        function buildUI() {
            const snap = getSnapshot(); // v56.5: snapをbuildUIスコープで取得
            return h('article', { class: 'flex flex-col gap-6' },
                h('header', {}, h('h1', { class: 'h1' }, 'Settings')),
                h('div', { class: 'grid grid-cols-1 md:grid-cols-2 gap-6' },
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'エクスポート'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-primary', onclick: exportFull }, 'フルバックアップ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportProjects }, 'Projectsのみ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportApps }, 'AppsDataのみ'),
                                h('button', { class: 'btn btn-secondary', onclick: exportProfile }, 'Profileのみ')
                            ),
                            h('p', { class: 'text-muted text-sm' }, 'フルバックアップは互換性を考慮した形式です。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'インポート（欠損ゼロ）'),
                            // [A11Y 2.1.1] 以下の select / checkbox に付けた id は「再描画で消えた後に
                            //   focus を戻す」ための安定ハンドル (main.js _renderCore が復元する)。
                            //   これらの onchange は window.render() で #content を作り直すため、id が
                            //   無いと 1 つ切り替えるたび focus が body へ落ち、対象を続けて選べない。
                            h('div', { class: 'grid grid-cols-2 gap-3' },
                                h('div', {},
                                    // [FIX] これらの「モード」/「対象」コントロールの onchange は
                                    //   **window.render() を呼ばない**。値は import 実行時にしか読まれず
                                    //   (下の importJSON)、コントロール自身の選択状態はブラウザが既に
                                    //   更新しているので、全再描画には何も得るものが無い。むしろ:
                                    //   (1) #content ごと作り直すので **隣の file input が差し替わり**、
                                    //       「対象を変えてすぐファイルを選ぶ」操作で change が
                                    //       古い input に飛んで **import が起きない** (実測: CI で
                                    //       #1053 が RED・#1040 でも同じレースを踏んだ)。
                                    //   (2) focus が一度失われ _renderCore が id を鍵に戻す往復が要る。
                                    //       再描画しなければそもそも失われない (WCAG 2.1.1)。
                                    //   これらのフラグを読む描画は自分自身の selected/checked だけである
                                    //   ことを全走査で確認済み。
                                    h('label', { class: 'text-sm text-muted', for: 'settingsImportMode' }, 'モード'),
                                    h('select', { class: 'input', id: 'settingsImportMode', 'aria-label': 'インポートモード', onchange: (e) => { settingsImportMode = e.target.value; } },
                                        h('option', { value: 'append', selected: settingsImportMode === 'append' ? true : undefined }, 'append（追加のみ）'),
                                        h('option', { value: 'upsert', selected: settingsImportMode === 'upsert' ? true : undefined }, 'upsert（更新+追加）'),
                                        h('option', { value: 'strict', selected: settingsImportMode === 'strict' ? true : undefined }, 'strict（全置換）')
                                    )
                                ),
                                h('div', {},
                                    h('span', { class: 'text-sm text-muted', id: 'settingsIncludeGroupLabel' }, '対象'),
                                    h('div', { class: 'flex flex-wrap gap-2', role: 'group', 'aria-labelledby': 'settingsIncludeGroupLabel' },
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', id: 'settingsIncludeProfile', checked: settingsIncludeProfile, onchange: (e) => { settingsIncludeProfile = !!e.target.checked; } }),
                                            h('span', { class: 'icon-gap' }, 'Profile')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', id: 'settingsIncludeProjects', checked: settingsIncludeProjects, onchange: (e) => { settingsIncludeProjects = !!e.target.checked; } }),
                                            h('span', { class: 'icon-gap' }, 'Projects')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', id: 'settingsIncludeApps', checked: settingsIncludeApps, onchange: (e) => { settingsIncludeApps = !!e.target.checked; } }),
                                            h('span', { class: 'icon-gap' }, 'AppsData')
                                        )
                                    )
                                )
                            ),
                            h('div', {},
                                h('input', {
                                    type: 'file',
                                    class: 'input',
                                    'aria-label': 'インポートする JSON ファイルを選択',
                                    accept: 'application/json',
                                    onchange: (e) => {
                                        const f = e.target.files && e.target.files[0];
                                        if (f) {importJSON(f);}
                                        e.target.value = '';
                                    }
                                })
                            ),
                            h('p', { class: 'text-muted text-sm' }, 'Projectsは常にデフォルトを維持しつつ、あなたの編集を優先してマージします。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'デザイン'),
                            h('p', { class: 'text-muted' }, 'Primaryカラーとベースフォントを切り替えます（Light/Dark/Systemは別設定）。'),
                            h('div', { class: 'flex flex-wrap items-center gap-3' },
                                h('label', { class: 'text-sm font-semibold', for: 'brandSelect' }, 'ブランド'),
                                h('select', {
                                    id: 'brandSelect',
                                    class: 'input',
                                    onchange: (e) => { Brand.set(e.target.value); window.render(); }
                                },
                                    h('option', { value: 'indigo', selected: Brand.get() === 'indigo' ? true : undefined }, 'Indigo'),
                                    h('option', { value: 'classic', selected: Brand.get() === 'classic' ? true : undefined }, 'Classic Blue + Inter')
                                ),
                                h('span', { class: 'badge badge-secondary' }, '即時反映')
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, 'スナップショット'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-secondary', id: 'settings-snapshot-save', onclick: setSnapshot }, '保存'),
                                h('button', { class: 'btn btn-secondary', id: 'settings-snapshot-restore', onclick: restoreSnapshot, disabled: !snap }, '復元'),
                                h('button', { class: 'btn btn-ghost', onclick: clearSnapshot, disabled: !snap }, '削除')
                            ),
                            snap
                                ? h('p', { class: 'text-muted text-sm' }, `保存日時: ${new Date(snap.at).toLocaleString()}`)
                                : h('p', { class: 'text-muted text-sm' }, 'スナップショットは未保存です。')
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '並び替え（Projects）'),
                            h('div', { class: 'text-muted text-sm' }, '上下ボタンで表示順を調整できます。'),
                            // [A11Y 1.3.1] プロジェクト行は 18 件並ぶ同質なリスト。role が無いと
                            //   SR 利用者は件数も項目の切れ目も掴めない。既存のラッパーへ role を
                            //   足すだけなので DOM は増えず描画は不変。
                            h('div', { class: 'flex flex-col gap-2 scroll-container-sm', role: 'list' },
                                ...state.projects.map((p, idx) =>
                                    h('div', { class: 'flex items-center justify-between gap-2', role: 'listitem' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, String(idx + 1)),
                                            h('span', { class: 'text-sm' }, p.name)
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            // [A11Y 2.1.1] id は再描画後の focus 復元ハンドル (main.js _renderCore)。
                                            //   **idx ではなく p.id で鍵を作る**のが要点で、そうすると移動後も
                                            //   「同じプロジェクトの ↓」へ focus が戻り、続けて押して何段でも
                                            //   動かせる (idx で鍵を作ると、その位置に来た別プロジェクトの
                                            //   ボタンへ focus が移ってしまう)。実測 (#1000): id が無いと
                                            //   1 回押しただけで focus が外れ、2 回目以降が効かなかった。
                                            // [A11Y 4.1.2] 名前に **どのプロジェクトか** を含める。矢印だけだと
                                            //   36 個のボタンが「↑」「↓」の 2 種類の名前しか持たず、SR 利用者は
                                            //   どれを操作するのか区別できない (実測: uniq な名前が 2 つだけ)。
                                            //   同じ行の削除・非表示は既に「削除：<名前>」と一意化されており、
                                            //   **並べ替えだけ取り残されていた**非対称。矢印そのものは装飾なので
                                            //   aria-hidden にして二重読み上げを防ぐ (quiz の ✦ と同じ扱い)。
                                            h('button', { class: 'btn btn-ghost btn-sm', id: 'settings-move-up-' + p.id, onclick: () => moveProject(idx, -1), disabled: idx === 0, 'aria-label': '上へ移動：' + p.name },
                                                h('span', { 'aria-hidden': 'true' }, '↑')),
                                            h('button', { class: 'btn btn-ghost btn-sm', id: 'settings-move-down-' + p.id, onclick: () => moveProject(idx, +1), disabled: idx === state.projects.length - 1, 'aria-label': '下へ移動：' + p.name },
                                                h('span', { 'aria-hidden': 'true' }, '↓'))
                                        )
                                    )
                                )
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '表示管理（Projects）'),
                            h('div', { class: 'grid grid-cols-1 gap-3' },
                                h('div', {},
                                    // [FIX] label↔input を for/id で関連付ける (WCAG 3.3.2 / 4.1.2)。
                                    //   従来は visible <label> が for 無し・input が id 無しで未関連付けのため、
                                    //   アクセシブル名が入力で消失する placeholder のみだった (SR 利用者はどの
                                    //   フィールドか判別不能)。同ファイル brand select の for/id パターンに倣う。
                                    h('label', { class: 'text-sm text-muted', for: 'settingsNewName' }, '名前'),
                                    // [DATA] 保存側の上限と入力できる範囲を一致させる。normalizeProject が
                                    //   name を LIMITS.PROJECT_NAME で切り詰めるのに入力欄が無制限だと、
                                    //   長い名前は **追加した直後は全部見えているのに、リロード後に黙って
                                    //   短くなる** (実測: 200 文字 → 120 文字)。消えたことに気付くのが
                                    //   後になるほど原因が分からない (#924 と同じ class)。
                                    //   NOTE: Check 410 は「同じ file 内で LIMITS を使って slice している」
                                    //   ことを条件に maxlength を要求するため、上限が store.js 側にある
                                    //   このケースは射程外だった。
                                    h('input', { id: 'settingsNewName', class: 'input', placeholder: 'プロジェクト名', maxlength: CONSTANTS.LIMITS.PROJECT_NAME, value: settingsNewName, oninput: (e) => { settingsNewName = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted', for: 'settingsNewTech' }, 'Tech（カンマ区切り）'),
                                    h('input', { id: 'settingsNewTech', class: 'input', placeholder: '例: JS,HTML,CSS', value: settingsNewTech, oninput: (e) => { settingsNewTech = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted', for: 'settingsNewDemo' }, 'Demo（任意）'),
                                    h('select', { class: 'input', id: 'settingsNewDemo', 'aria-label': 'Demo アプリの種類', onchange: (e) => { settingsNewDemo = e.target.value; } },
                                        h('option', { value: '', selected: settingsNewDemo === '' ? true : undefined }, 'Demoなし'),
                                        h('option', { value: 'task', selected: settingsNewDemo === 'task' ? true : undefined }, 'task'),
                                        h('option', { value: 'todo', selected: settingsNewDemo === 'todo' ? true : undefined }, 'todo'),
                                        h('option', { value: 'pomodoro', selected: settingsNewDemo === 'pomodoro' ? true : undefined }, 'pomodoro'),
                                        h('option', { value: 'ai', selected: settingsNewDemo === 'ai' ? true : undefined }, 'ai'),
                                        h('option', { value: 'notes', selected: settingsNewDemo === 'notes' ? true : undefined }, 'notes')
                                    )
                                ),
                                h('div', { class: 'flex items-end' },
                                    h('button', { class: 'btn btn-primary w-full', onclick: addProjectManual }, '追加')
                                )
                            ),
                            (() => {
                                const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                const visibleCount = state.projects.filter(p => !hidden.has(String(p.id))).length;
                                const hiddenCount = state.projects.length - visibleCount;
                                return h('div', { class: 'text-muted text-sm' }, `表示: ${visibleCount} / 非表示: ${hiddenCount} / 総数: ${state.projects.length}`);
                            })(),
                            h('div', { class: 'flex flex-col gap-2 scroll-container-md', role: 'list' },
                                ...state.projects.map(p => {
                                    const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                    const isHidden = hidden.has(String(p.id));
                                    const isDefault = defaultProjectIds.has(String(p.id));
                                    return h('div', { class: 'flex items-center justify-between gap-2', role: 'listitem' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, isDefault ? 'default' : 'user'),
                                            h('span', { class: 'text-sm' }, p.name),
                                            isHidden ? h('span', { class: 'badge badge-green' }, 'hidden') : null
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            // [A11Y 4.1.2] 全プロジェクト行でボタン名が同一 (「表示/非表示」「削除」) だと
                                            //   SR ユーザーはどのプロジェクトの操作か区別できない。可視テキストは維持しつつ
                                            //   aria-label に p.name を含め一意化する (可視語を含むため WCAG 2.5.3 も充足)。
                                            h('button', { class: 'btn btn-ghost btn-sm', id: 'settings-toggle-hidden-' + p.id, 'aria-label': (isHidden ? '表示' : '非表示') + '：' + p.name, onclick: () => toggleHiddenProject(p.id) }, isHidden ? '表示' : '非表示'),
                                            h('button', { class: 'btn btn-danger btn-sm', id: 'settings-delete-' + p.id, 'aria-label': '削除：' + p.name, disabled: isDefault, title: isDefault ? 'デフォルトは非表示のみ' : '', onclick: () => deleteProjectHard(p.id) }, '削除')
                                        )
                                    );
                                })
                            )
                        )
                    ),
                    h('section', { class: 'card' },
                        h('div', { class: 'card-body flex flex-col gap-3' },
                            h('h2', { class: 'h3' }, '整合性チェック / 正規化'),
                            h('div', { class: 'flex flex-wrap gap-2' },
                                h('button', { class: 'btn btn-secondary', onclick: normalizeNow }, '実行'),
                                h('button', { class: 'btn btn-danger', onclick: resetData }, '全リセット')
                            ),
                            h('p', { class: 'text-muted text-sm' }, '正規化はデータ破損・型揺れ・上限超過などを安全側に丸めます。')
                        )
                    )
                )
            );
        }
        return buildUI();
    }

    return { SettingsPage };
}
