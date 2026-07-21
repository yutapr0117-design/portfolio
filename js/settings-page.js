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
 *   - CONSTANTS: js/constants.js (SNAPSHOT_KEY / SCHEMA_VERSION)
 *   - generateId, slugify: js/pure-utils.js
 *
 * 不変条件:
 *   - 本モジュールは葉 (ローカル import ゼロ)。依存は createSettingsPage の引数で受け取る。
 *   - restoreSnapshot / importJSON は必ず Store.validateAndNormalize を通す (#93/#295/#561 class:
 *     外部入力 ingestion は全経路正規化)。抽出でこの契約を変えないこと。
 */
export function createSettingsPage({ h, Toast, State, Brand, Store, Storage, CONSTANTS, generateId, slugify }) {
    // ===== Component: Settings Page =====
    let settingsImportMode = 'append';
    let settingsIncludeProfile = true;
    let settingsIncludeProjects = true;
    let settingsIncludeApps = true;
    let settingsNewName = '';
    let settingsNewTech = '';
    let settingsNewDemo = '';

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
            State.set(Store.validateAndNormalize(snap.data));
            Toast.show('スナップショットを復元しました');
        }
        function clearSnapshot() {
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

        function importJSON(file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const parsed = JSON.parse(e.target.result);
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
                    if (settingsIncludeProfile && parsed.profile) { merged.profile = parsed.profile; }
                    if (settingsIncludeProjects && Array.isArray(parsed.projects)) {
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
                    }
                    if (settingsIncludeApps && parsed.appsData) { merged.appsData = parsed.appsData; }

                    // 正規化してから単一 commit。生データは一切 render に届かない。
                    State.set(Store.validateAndNormalize(merged));

                    Toast.show('インポートが完了しました');
                } catch (err) {
                    Toast.show('JSONのパースに失敗しました', 'error');
                }
            };
            reader.readAsText(file);
        }

        function addProjectManual() {
            if (!settingsNewName.trim()) { Toast.show('プロジェクト名を入力してください', 'error'); return; }
            State.update(s => {
                // [FIX] slug 衝突回避: slugify は決定的なので同名追加だと slug が重複し、
                // ProjectDetailPage の find(p.slug===slug) が先頭のみ返して片方の詳細が到達不能に
                // なる。既存 slug と衝突する場合は -2, -3... を付与して一意化する。
                const existing = new Set(s.projects.map(p => p.slug));
                const base = slugify(settingsNewName);
                let slug = base;
                let n = 2;
                while (existing.has(slug)) { slug = `${base}-${n}`; n++; }
                s.projects.unshift({
                    id: 'p_user_' + generateId().slice(0, 6),
                    slug,
                    name: settingsNewName,
                    category: 'User Added',
                    summary: '', problem: '', approach: '',
                    tech: settingsNewTech ? settingsNewTech.split(',').map(t => t.trim()) : [],
                    tags: [],
                    demoRoute: settingsNewDemo || null
                });
            });
            settingsNewName = ''; settingsNewTech = ''; settingsNewDemo = '';
            Toast.show('プロジェクトを追加しました');
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

        function deleteProjectHard(id) {
            if (defaultProjectIds.has(id)) {return;}
            if (!confirm('本当に削除しますか？')) {return;}
            State.update(s => {
                s.projects = s.projects.filter(p => p.id !== id);
            });
        }

        function moveProject(idx, dir) {
            State.update(s => {
                if (idx + dir < 0 || idx + dir >= s.projects.length) {return;}
                const temp = s.projects[idx];
                s.projects[idx] = s.projects[idx + dir];
                s.projects[idx + dir] = temp;
            });
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
                            h('div', { class: 'grid grid-cols-2 gap-3' },
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, 'モード'),
                                    h('select', { class: 'input', 'aria-label': 'インポートモード', onchange: (e) => { settingsImportMode = e.target.value; window.render(); } },
                                        h('option', { value: 'append', selected: settingsImportMode === 'append' ? true : undefined }, 'append（追加のみ）'),
                                        h('option', { value: 'upsert', selected: settingsImportMode === 'upsert' ? true : undefined }, 'upsert（更新+追加）'),
                                        h('option', { value: 'strict', selected: settingsImportMode === 'strict' ? true : undefined }, 'strict（全置換）')
                                    )
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, '対象'),
                                    h('div', { class: 'flex flex-wrap gap-2' },
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeProfile, onchange: (e) => { settingsIncludeProfile = !!e.target.checked; window.render(); } }),
                                            h('span', { class: 'icon-gap' }, 'Profile')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeProjects, onchange: (e) => { settingsIncludeProjects = !!e.target.checked; window.render(); } }),
                                            h('span', { class: 'icon-gap' }, 'Projects')
                                        ),
                                        h('label', { class: 'btn btn-ghost btn-sm' },
                                            h('input', { type: 'checkbox', checked: settingsIncludeApps, onchange: (e) => { settingsIncludeApps = !!e.target.checked; window.render(); } }),
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
                                h('button', { class: 'btn btn-secondary', onclick: setSnapshot }, '保存'),
                                h('button', { class: 'btn btn-secondary', onclick: restoreSnapshot, disabled: !snap }, '復元'),
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
                            h('div', { class: 'flex flex-col gap-2 scroll-container-sm' },
                                ...state.projects.map((p, idx) =>
                                    h('div', { class: 'flex items-center justify-between gap-2' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, String(idx + 1)),
                                            h('span', { class: 'text-sm' }, p.name)
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, -1), disabled: idx === 0 }, '↑'),
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => moveProject(idx, +1), disabled: idx === state.projects.length - 1 }, '↓')
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
                                    h('input', { id: 'settingsNewName', class: 'input', placeholder: 'プロジェクト名', value: settingsNewName, oninput: (e) => { settingsNewName = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted', for: 'settingsNewTech' }, 'Tech（カンマ区切り）'),
                                    h('input', { id: 'settingsNewTech', class: 'input', placeholder: '例: JS,HTML,CSS', value: settingsNewTech, oninput: (e) => { settingsNewTech = e.target.value; } })
                                ),
                                h('div', {},
                                    h('label', { class: 'text-sm text-muted' }, 'Demo（任意）'),
                                    h('select', { class: 'input', 'aria-label': 'Demo アプリの種類', onchange: (e) => { settingsNewDemo = e.target.value; } },
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
                            h('div', { class: 'flex flex-col gap-2 scroll-container-md' },
                                ...state.projects.map(p => {
                                    const hidden = new Set(((state.projectPrefs && state.projectPrefs.hiddenIds) || []).map(String));
                                    const isHidden = hidden.has(String(p.id));
                                    const isDefault = defaultProjectIds.has(String(p.id));
                                    return h('div', { class: 'flex items-center justify-between gap-2' },
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('span', { class: 'badge badge-gray' }, isDefault ? 'default' : 'user'),
                                            h('span', { class: 'text-sm' }, p.name),
                                            isHidden ? h('span', { class: 'badge badge-green' }, 'hidden') : null
                                        ),
                                        h('div', { class: 'flex items-center gap-2' },
                                            h('button', { class: 'btn btn-ghost btn-sm', onclick: () => toggleHiddenProject(p.id) }, isHidden ? '表示' : '非表示'),
                                            h('button', { class: 'btn btn-danger btn-sm', disabled: isDefault, title: isDefault ? 'デフォルトは非表示のみ' : '', onclick: () => deleteProjectHard(p.id) }, '削除')
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
