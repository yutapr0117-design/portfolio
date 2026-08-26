/**
 * js/settings-io.js — Settings の入出力 (export / import) と損失レポート
 *
 * @fileoverview v80+ bloat-reduction (2026-08-20): js/settings-page.js から
 * **入出力クラスタ**を factory pattern で分離した葉モジュール。settings-page.js は
 * import/export・snapshot・手動追加・正規化を 1 file で抱えて 746 行まで伸びており、
 * その中で最大かつ最も独立していたのが IO 面だった (専用 spec が 3 本ある:
 * apps-settings-io / -import-shape / -ingestion)。
 *
 * **なぜ clean に切れるか**: IO クラスタが参照する UI 状態 (取り込みモード / 対象の
 * チェックボックス 4 つ) は **読み取りのみ** で、書き込みは settings-page.js 側の
 * onchange が行う。よって getter 1 つ (`getImportOptions`) を注入すれば closure を
 * 持ち出さずに済む。
 *
 * export:
 *   createSettingsIO({ deps }) -> { exportFull, exportProjects, exportApps, exportProfile, importJSON, lossParts }
 *   (lossParts も返すのは、snapshot 復元 (settings-page.js) が **同じ言葉で** 損失を報告するため。
 *    片方だけ honest だと「復元は無事だった」と誤解される —— #1186)
 *
 * 【依存（引数で注入）】(葉契約 = ローカル ESM import ゼロ)
 *   - State: js/state.js factory instance
 *   - Store: js/store.js factory instance (validateAndNormalize)
 *   - Toast: js/ui-components.js
 *   - getImportOptions: () => ({ mode, includeProfile, includeProjects, includeApps })
 *     取り込み時の UI 選択を **その時点で** 読むための getter。値を引数で渡すと
 *     FileReader の onload (非同期) が **選択時ではなく読み込み開始時の値** を使うことになる。
 *
 * 不変条件:
 *   - importJSON は必ず Store.validateAndNormalize を通してから State.set する
 *     (#93/#295/#561 class: 外部入力 ingestion は全経路正規化・Check 374 が強制)。
 *   - 取り込み/復元で失われた分は lossParts が数え、**黙って捨てない**
 *     (#1143/#1178/#1181/#1182/#1186/#1187 の「切り捨てたら黙るな」class)。
 */
export function createSettingsIO({ State, Store, Toast, getImportOptions }) {
    // 取り込み時点の UI 選択を読む (非同期 onload の中で評価されるので getter 経由)。
    const _opt = () => getImportOptions();

// キー順に依存しない安定化 JSON。オブジェクトの等価判定に使う (手書きの取り込み
// ファイルは export と キー順が違いうるので、素の JSON.stringify では別物と誤判定する)。
const _stable = (v) => JSON.stringify(v, (k, val) =>
    (val && typeof val === 'object' && !Array.isArray(val))
        ? Object.keys(val).sort().reduce((o, kk) => { o[kk] = val[kk]; return o; }, {})
        : val);

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
    // [FIX] `Projectsのみ` に **非表示設定 (projectPrefs) を含める**。既定プロジェクトは削除できず
    //   「非表示」が唯一の非公開手段 (#886) なので、素の配列だけを書き出していた従来は、この
    //   ファイルから復元すると**隠したプロジェクトが黙って再公開**されていた (フルは #1037 で
    //   直済・部分 export だけ取り残されていた)。import 側は変更不要・旧形式も読める (詳細は e2e)。
    function exportProjects() {
        const s = State.get();
        downloadJSON({ projects: s.projects, projectPrefs: s.projectPrefs },
            `portfolio_projects_${Date.now()}.json`);
    }
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
            // **取り込みの瞬間**の UI 選択をここで 1 回読む (onload は非同期なので、
            // 読み込み開始時ではなくこの時点の選択を使う)。
            const { mode: settingsImportMode, includeProfile: settingsIncludeProfile,
                includeProjects: settingsIncludeProjects, includeApps: settingsIncludeApps } = _opt();
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
                    // [FIX] 行き止まりにしない。**受け付ける形はこのアプリ自身が知っている**。
                    Toast.show('認識できない形式のファイルです。'
                        + 'このアプリの書き出し（フルバックアップ / Projectsのみ / '
                        + 'AppsDataのみ / Profileのみ）を選んでください', 'error', 6000);
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
                // [FIX] **全置換は最も破壊的なのに無確認だった。** 削除も全リセットもスナップショットの
                //   削除・上書きも confirm を通すのに、ここだけ素通りしていた。しかも**モードは遷移を
                //   跨いで残る**ので、選択を覚えていない利用者が踏む (経緯と実測は e2e 側)。
                if (settingsImportMode === 'strict') {
                    if (!confirm('「全置換」モードです。選択した対象の現在のデータを、'
                        + 'ファイルの内容で置き換えます。\n元には戻せません。続けますか？')) { return; }
                }
                let applied = false;
                // [FIX] theme は **実際に変わるときだけ** applied に数える。フルバックアップには
                //   必ず theme が入るため、無条件に立てると上の #1040 ガードが最も一般的な形式に
                //   対して無効化される (経緯と実測は e2e/apps-settings-import-shape.spec.js)。
                if (typeof parsed.theme === 'string') {
                    merged.theme = parsed.theme;
                    if (parsed.theme !== base.theme) { applied = true; }
                }
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
                            // append: tasks/todos 以外は既存を優先し、**実際に違う**分だけ数える。
                            // 内容が同じなら何も失っていないので報告しない —— 失っていないのに
                            // 警告を出すと、本物の切り捨て警告が信用されなくなる (#1181 と同じ理由)。
                            // キー順に依存しないよう安定化して比較する (手書きファイルは
                            // export と順序が違いうる)。
                            _keptOwn = Object.keys(inc).filter(k => k !== 'tasks' && k !== 'todos'
                                && _stable(inc[k]) !== _stable(baseApps[k])).length;
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

    // lossParts も返す: snapshot 復元 (settings-page.js) が同じ言葉で損失を報告するため
    // (#1186 —— 片方だけ honest だと「復元は無事だった」と誤解される)。
    return { exportFull, exportProjects, exportApps, exportProfile, importJSON, lossParts };
}
