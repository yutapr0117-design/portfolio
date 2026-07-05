/**
 * js/store.js — Application data store (default data + load / validate / normalize / similarity)
 * (v80+ Stage 5-g extraction via factory pattern)
 *
 * main.js の `Store` IIFE モジュールを依存注入（factory pattern）で物理分割した葉モジュール。
 * Brand と同じく、Storage / CONSTANTS / generateId / deepClone / slugify / sanitizeUrl / clamp / AUTHOR
 * への closure 依存を `createStore` 関数の引数で受け取ることで、葉契約（Check 47c: import ゼロ）を
 * 維持しつつ Store の挙動と公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   { load, createDefaultStore, validateAndNormalize, autoRelatedCandidates }
 *
 * 【依存（引数で注入）】
 *   - AUTHOR: { DISPLAY_NAME }
 *   - CONSTANTS: { STORAGE_KEY, SNAPSHOT_KEY, SCHEMA_VERSION, LIMITS, TAB_ID }
 *   - Storage: { parse(key), set(key, value) }
 *   - generateId, deepClone, slugify, sanitizeUrl, clamp (pure-utils)
 *
 * 【非破壊性】
 *   - defaultProfile / defaultProjects / defaultAppsData の各 default 値は文字列まで byte-equivalent
 *   - localStorage schema (key 'portfolio_enhanced_v45') は不変
 *   - LIMITS による slice 上限・validateAndNormalize の挙動は不変
 *   - autoRelatedCandidates のローカル tokenizeForSimilarity も byte-equivalent
 */
export function createStore({ AUTHOR, CONSTANTS, Storage, generateId, deepClone, slugify, sanitizeUrl, clamp }) {
    // Default Data
    const defaultProfile = {
        name: AUTHOR.DISPLAY_NAME,
        title: 'AI-Driven PM',
        bio: `このサイトは完成をゴールにせず、設計判断を検証し続けるためのポートフォリオです。

【設計思想】
• 単一HTMLでの完結（依存性最小化）
• セマンティックHTML5 + ARIA対応
• 型安全なDOM操作
• イベント駆動アーキテクチャ

【見てほしいこと】
• SPAを最小構成で設計する判断
• 壊れる前提で作るための構造
• 作りながら改善していくプロセス

【Why SPA?】
• 構造変更を前提にするため
• 実装より設計判断を検証するため`,
        email: 'yuta.pr.0117@gmail.com',
        github: '',
        linkedin: '',
        location: 'Japan',
    };

    const defaultAppsData = {
        tasks: [
            { id: 't1', title: 'ログの確認', status: 'backlog', priority: 'high', tags: ['運用'], createdAt: Date.now(), updatedAt: Date.now() },
            { id: 't2', title: '資料の更新', status: 'in-progress', priority: 'low', tags: ['ドキュメント'], createdAt: Date.now(), updatedAt: Date.now() }
        ],
        todos: [
            { id: 'td1', text: 'コーヒーを買う', completed: false, createdAt: Date.now(), dueDate: null }
        ],
        pomodoro: {
            history: [],
            settings: { work: 25, short: 5, long: 15 },
            runtime: {
                isActive: false,
                mode: 'work',
                endAtMs: null,
                remainingSec: 1500,
                linkedTaskId: null
            }
        },
        ai: { history: [] },
        quizSearch: "",
        notes: "# メモ\n\nMarkdown で書けます。**太字**・`コード`・- リスト・見出し。"
    };

    function proj(id, slug, name, category, summary, problem, approach, outcome, tech, tags, highlights, architecture, relatedIds, links, demoRoute) {
        return {
            id, slug, name, category,
            summary, problem, approach,
            outcome: outcome || { metrics: [], impact: "" },
            tech: Array.isArray(tech) ? tech : [],
            tags: Array.isArray(tags) ? tags : [],
            highlights: Array.isArray(highlights) ? highlights : [],
            architecture: architecture || { overview: "", mermaid: null },
            relatedProjectIds: Array.isArray(relatedIds) ? relatedIds : [],
            links: Array.isArray(links) ? links : [],
            demoRoute: demoRoute || null
        };
    }

    const defaultProjects = [
        proj("p01", "task-manager", "タスク管理アプリ", "Productivity",
            "このポートフォリオに統合された、オフライン対応のタスク管理ツール。",
            "外部依存のあるツールは、障害時に利用できなくなるリスクがある。",
            "状態・優先度・検索の最低限に絞って堅牢に実装。LocalStorageで永続化。",
            { metrics: [{ label: "耐障害", value: "local-only" }, { label: "状態", value: "3" }], impact: "運用前提の最小機能で事故率を下げる。" },
            ["Vanilla JS", "LocalStorage", "Hash Router"],
            ["ツール", "SPA", "オフライン"], ["検索/フィルタ", "優先度", "状態遷移"],
            { overview: "単一ストア（appsData.tasks）をUIが参照する構造。" },
            ["p02", "p03", "p04"], [], "task"
        ),
        proj("p02", "todo-list", "TODOリスト", "Productivity",
            "クイックTODO。",
            "高機能システムへ移るたびに思考が途切れる。",
            "Enter追加 + IMEガード + フィルタ/一括操作に限定。",
            { metrics: [{ label: "入力導線", value: "Enter" }], impact: "認知負荷を落として記録を継続。" },
            ["Vanilla JS", "IME guard"], ["ツール", "効率化"], ["一括操作", "検索/フィルタ"],
            { overview: "appsData.todosを参照。" },
            ["p01", "p03"], [], "todo"
        ),
        proj("p03", "pomodoro-timer", "ポモドーロタイマー", "Productivity",
            "タブ休眠・スリープ対応ポモドーロ。",
            "setIntervalだけだと非アクティブで精度が落ちる。",
            "endAt(タイムスタンプ)で残秒を復元。二重起動を防止。フォーカス対象（タスク）を記録。",
            { metrics: [{ label: "復元方式", value: "timestamp" }], impact: "タイマーが信頼できる状態を維持。" },
            ["Vanilla JS", "Date API"], ["ツール", "時間管理"], ["timestamp復元", "履歴管理", "フォーカス対象"],
            { overview: "runtime(endAt/remainingSec)を永続化し、tickはUI更新のみ。" },
            ["p01", "p02", "p04"], [], "pomodoro"
        ),
        proj("p09", "local-ai-assist", "ローカルAIアシスト", "AI",
            "外部API無しのAIアシスト。",
            "AI活用は外部依存にすると壊れやすい。",
            "ルール分類（design/troubleshoot/general）＋テンプレ生成＋根拠表示。",
            { metrics: [{ label: "依存", value: "none" }], impact: "オフラインで提案が成立。" },
            ["Rule-based", "Templates"], ["AI", "オフライン"], ["タスク分解", "文章生成"],
            { overview: "appsData.ai.historyにログ。" },
            ["p16", "p17", "p18"], [], "ai"
        ),
        proj("p04", "unified-data-model", "データモデル設計", "Productivity",
            "ローカルアプリ間の整合性を保つ共通スキーマ。",
            "アプリごとに形式がバラバラだと、移行や復旧が破綻する。",
            "schemaVersion付きストア + フォールバック + Import/Export設計。整合性チェック/自動修復導線。",
            { metrics: [{ label: "schema", value: "v2" }, { label: "復旧", value: "safe" }], impact: "破損時も初期化・復元が可能。" },
            ["Schema", "Migration"], ["アーキテクチャ", "データ"], ["破損フォールバック", "Import/Export", "自動修復"],
            { overview: "full-store(schemaVersion:2)を採用。" },
            ["p01", "p02", "p03", "p18"], [], null
        ),
        proj("p05", "offline-sync-notes", "オフライン同期設計メモ", "Productivity",
            "将来同期を見据えた競合解決の整理。",
            "同期時の衝突は後から直せない温床になりやすい。",
            "Upsert/Strictの方針や、衝突キーの設計を文書化。",
            { metrics: [{ label: "方針", value: "append/upsert/strict" }], impact: "運用ポリシーを先に固定。" },
            ["Design Notes"], ["設計", "運用"], ["衝突キー", "適用モード"],
            { overview: "settingsでインポート結果を可視化。" },
            ["p04"], [], null
        ),
        proj("p06", "telemetry-starter", "テレメトリ基盤コンセプト", "Observability",
            "フロントのイベント/ログ/計測の統一案。",
            "ログ形式がバラバラだと調査コストが上がる。",
            "イベントラッパー + 最低限の構造化ログ方針を定義。",
            { metrics: [{ label: "形式", value: "structured" }], impact: "再現可能な調査手順の土台。" },
            ["Structured Logging"], ["DevOps", "運用"], ["統一フォーマット", "最小実装"],
            { overview: "実装は本SPAのsafe方針に反映。" },
            ["p07", "p08"], [], null
        ),
        proj("p07", "slo-dashboard", "SLOダッシュボード試作（UI）", "Observability",
            "SLO/SLIを読み解くUIの構造案。",
            "数字があるのに意思決定に繋がらないことがある。",
            "“見る順序”をUIに埋め込む。フィルタとハイライトを先に置く。",
            { metrics: [{ label: "導線", value: "filter-first" }], impact: "意思決定の遅延を減らす。" },
            ["UI Design"], ["UI", "運用"], ["フィルタ優先", "視認性"],
            { overview: "Projects一覧の検索/カテゴリ選択に思想を反映。" },
            ["p06"], [], null
        ),
        proj("p08", "incident-playbook", "インシデント手順プレイブック", "Observability",
            "事故時に手順抜けを防ぐチェックリスト。",
            "緊急時は認知負荷が上がり、抜けが生まれる。",
            "手順をUI化し、確認ボックスの順序を固定。",
            { metrics: [{ label: "抜け防止", value: "checklist" }], impact: "初動品質を底上げ。" },
            ["Checklist"], ["プロセス", "運用"], ["手順固定", "可視化"],
            { overview: "Task/Todoの最小操作性にも同じ思想。" },
            ["p06", "p09"], [], null
        ),
        proj("p10", "ci-quality-gate", "CIクオリティゲート設計", "Platform",
            "Lint/Test/Typecheckのゲート設計。",
            "品質の劣化は後工程でコスト爆増する。",
            "最小ゲートを固定し、失敗時に原因が即分かる形へ。",
            { metrics: [{ label: "ゲート", value: "3" }], impact: "品質劣化の混入を抑制。" },
            ["Quality Gates"], ["CI/CD"], ["最小セット", "原因特定"],
            { overview: "本HTMLは例外ガード/検証を先に固定。" },
            ["p11"], [], null
        ),
        proj("p11", "release-notes-builder", "リリースノート生成（ルール）", "Platform",
            "変更ログのテンプレ生成。",
            "記録が残らないと説明責任が崩れる。",
            "テンプレ生成 + 必須項目の抜け検出を設計。",
            { metrics: [{ label: "テンプレ", value: "fixed" }], impact: "説明の再現性が上がる。" },
            ["Templates"], ["自動化"], ["抜け検出", "規格化"],
            { overview: "AIアシストのテンプレ生成に思想を反映。" },
            ["p10", "p17"], [], null
        ),
        proj("p12", "design-system-mini", "ミニデザインシステム", "Platform",
            "最低限のUI部品を揃え、崩れを防ぐ。",
            "画面ごとに見た目が違うと学習コストが増える。",
            "ボタン/カード/バッジ/入力などを統一。",
            { metrics: [{ label: "部品", value: "atoms" }], impact: "見た目の一貫性でUXを安定化。" },
            ["CSS Variables"], ["UI/UX"], ["一貫性", "focus-visible"],
            { overview: "単一CSSでテーマ/余白/階層を統一。" },
            ["p01", "p02", "p03"], [], null
        ),
        proj("p13", "security-baseline", "セキュリティベースライン", "Security",
            "Webアプリの最低限チェック。",
            "基本が抜けると致命傷になる。",
            "XSS/リンク安全/入力検証/外部依存の境界を固定。",
            { metrics: [{ label: "XSS", value: "textContent" }], impact: "壊れ方を減らす。" },
            ["Safe DOM"], ["セキュリティ"], ["XSS回避", "境界固定"],
            { overview: "ユーザー入力はDOMにtextとしてのみ挿入。" },
            ["p14", "p15"], [], null
        ),
        proj("p14", "secrets-handling", "設定値管理ガイド", "Security",
            "秘匿情報をフロントへ入れない設計。",
            "クライアント側に秘密は置けない。",
            "外部API不要のAIアシストで運用を成立させる方針。",
            { metrics: [{ label: "外部API", value: "optional" }], impact: "安全側で成立させる。" },
            ["Boundary Design"], ["運用", "セキュリティ"], ["責任境界", "非依存"],
            { overview: "単一HTMLはネットワーク不要で動作。" },
            ["p13"], [], null
        ),
        proj("p15", "link-sanitization", "リンク検証ユーティリティ", "Security",
            "http/httpsのみ許可するURL検証。",
            "リンク注入は温床になりやすい。",
            "URL API + allowlist。",
            { metrics: [{ label: "protocol", value: "http/https" }], impact: "不正URLを排除。" },
            ["URL API"], ["セキュリティ"], ["sanitize", "noopener"],
            { overview: "外部リンクはrel=noopener/noreferrerを付与。" },
            ["p13"], [], null
        ),
        proj("p16", "task-breakdown-engine", "タスク分解エンジン", "AI",
            "キーワードに基づく標準手順の提案。",
            "作業開始できない状態は生産性を壊す。",
            "分類→テンプレ→チェックリスト化。",
            { metrics: [{ label: "分類", value: "3-mode" }], impact: "開始までの摩擦を下げる。" },
            ["Rule-based"], ["AI", "生産性"], ["分解", "根拠表示"],
            { overview: "ローカルルールエンジンを内蔵。" },
            ["p01", "p09", "p18"], [], "ai"
        ),
        proj("p17", "portfolio-copy-generator", "ポートフォリオ文章生成", "AI",
            "ケーススタディ文章の生成支援。",
            "文章作成に時間がかかる。",
            "トーン別テンプレ + ルール根拠の表示。",
            { metrics: [{ label: "トーン", value: "2" }], impact: "説明文作成の工数を削減。" },
            ["Templates"], ["AI"], ["professional/casual", "根拠表示"],
            { overview: "AIアシストで実装。" },
            ["p09", "p11"], [], "ai"
        ),
        proj("p18", "local-semantic-search", "ローカル検索スコアリング", "AI",
            "Projects検索の精度改善（依存なし）。",
            "完全一致だけだと探しにくい。",
            "トークン化→簡易スコア→降順表示。",
            { metrics: [{ label: "deps", value: "0" }], impact: "検索性の底上げ。" },
            ["Scoring"], ["検索", "AI"], ["token scoring", "lightweight"],
            { overview: "Projects一覧の検索にスコアリングを導入。" },
            ["p04", "p09"], [], null
        ),
    ];

    // Load store with migration
    function load() {
        const data = Storage.parse(CONSTANTS.STORAGE_KEY);
        if (!data) {return createDefaultStore();}
        if (data.schemaVersion !== CONSTANTS.SCHEMA_VERSION) {
            // 旧データをスナップショットとして退避してから初期化
            // NOTE: Settings の復元導線とフォーマットを合わせる（{at, reason, data}）
            try {
                Storage.set(CONSTANTS.SNAPSHOT_KEY, JSON.stringify({
                    at: Date.now(),
                    reason: 'schema-mismatch',
                    from: data.schemaVersion,
                    to: CONSTANTS.SCHEMA_VERSION,
                    data
                }));
            } catch { }
            return createDefaultStore();
        }
        return validateAndNormalize(data);
    }

    function createDefaultStore() {
        return {
            schemaVersion: CONSTANTS.SCHEMA_VERSION,
            type: 'full-store',
            profile: deepClone(defaultProfile),
            projects: deepClone(defaultProjects),
            appsData: deepClone(defaultAppsData),
            projectPrefs: { hiddenIds: [] },
            theme: 'system',
            lastModified: Date.now(),
        };
    }

    function validateAndNormalize(data) {
        const store = createDefaultStore();

        // Merge profile
        if (data.profile && typeof data.profile === 'object') {
            // github / linkedin は ContactPage で href として描画されるため、http(s) スキームのみ
            // 許可して javascript:/data: 等の XSS ベクタを遮断する (空文字はクリア扱いで許容)。
            const safeUrl = (v, fallback) => {
                const s = String(v ?? '').trim();
                if (s === '') {return '';}
                return /^https?:\/\//i.test(s) ? s.slice(0, 500) : String(fallback || '');
            };
            store.profile = {
                ...store.profile,
                name: String(data.profile.name || store.profile.name).slice(0, CONSTANTS.LIMITS.PROJECT_NAME),
                title: String(data.profile.title || store.profile.title).slice(0, CONSTANTS.LIMITS.CATEGORY),
                bio: String(data.profile.bio || store.profile.bio).slice(0, 5000),
                email: String(data.profile.email || store.profile.email),
                // schema 定義済みフィールドの取りこぼし防止 (従来 strip され import で消えていた)
                github: safeUrl(data.profile.github, store.profile.github),
                linkedin: safeUrl(data.profile.linkedin, store.profile.linkedin),
                location: String(data.profile.location || store.profile.location || '').slice(0, 200),
            };
        }

        // Merge projects (lossless): keep all defaults (v2 baseline) + preserve user edits + keep user-added projects
        if (Array.isArray(data.projects)) {
            store.projects = mergeProjectsWithDefaults(data.projects);
        }

        // Merge apps data
        if (data.appsData && typeof data.appsData === 'object') {
            store.appsData = normalizeAppsData(data.appsData);
        }

        // Theme
        if (['light', 'dark', 'system'].includes(data.theme)) {
            store.theme = data.theme;
        }


        // Project preferences (hidden list)
        if (data.projectPrefs && typeof data.projectPrefs === 'object' && Array.isArray(data.projectPrefs.hiddenIds)) {
            store.projectPrefs = { hiddenIds: data.projectPrefs.hiddenIds.map(String).filter(Boolean).slice(0, 1000) };
        }

        return store;
    }

    function normalizeProject(raw, idx) {
        const id = String(raw.id || `p${idx}_${generateId()}`).slice(0, CONSTANTS.LIMITS.PROJECT_ID);
        const slug = String(raw.slug || slugify(raw.name || id)).slice(0, 100);

        return {
            id,
            slug,
            name: String(raw.name || 'Untitled').slice(0, CONSTANTS.LIMITS.PROJECT_NAME),
            category: String(raw.category || 'Misc').slice(0, CONSTANTS.LIMITS.CATEGORY),
            summary: String(raw.summary || '').slice(0, CONSTANTS.LIMITS.SUMMARY),
            problem: String(raw.problem || '').slice(0, CONSTANTS.LIMITS.PROBLEM),
            approach: String(raw.approach || '').slice(0, CONSTANTS.LIMITS.APPROACH),
            outcome: {
                impact: String(raw.outcome?.impact || '').slice(0, CONSTANTS.LIMITS.IMPACT),
                metrics: Array.isArray(raw.outcome?.metrics)
                    ? raw.outcome.metrics.slice(0, 12).filter(m => m && m.label && m.value)
                    : []
            },
            // [FIX] Array.isArray ガード必須 (#93/#295/#561/#568 と同じ「外部 ingestion は全経路正規化」class)。
            // 旧 `(raw.tech || [])` は truthy 判定のみで、import/cross-tab/snapshot の project が tech/tags/
            // highlights/relatedProjectIds/links を非配列 (文字列/数値/オブジェクト) で持つと `|| []` が置換せず
            // `.filter` が `TypeError: ... is not a function` を throw → validateAndNormalize が例外 → FatalPage crash。
            // default の proj() builder は既に `Array.isArray(tech) ? tech : []` でガード済 (本 normalizer は
            // untrusted import を処理するゆえ同じガードが必須だった)。非配列は空配列にフォールバック。
            tech: (Array.isArray(raw.tech) ? raw.tech : []).filter(Boolean).slice(0, 12),
            tags: (Array.isArray(raw.tags) ? raw.tags : []).filter(Boolean).slice(0, 12),
            highlights: (Array.isArray(raw.highlights) ? raw.highlights : []).filter(Boolean).slice(0, 20),
            architecture: {
                overview: String(raw.architecture?.overview || '').slice(0, 2000),
                mermaid: raw.architecture?.mermaid || null
            },
            relatedProjectIds: (Array.isArray(raw.relatedProjectIds) ? raw.relatedProjectIds : []).filter(Boolean).slice(0, 20),
            links: (Array.isArray(raw.links) ? raw.links : []).filter(l => l && l.label && sanitizeUrl(l.url)).slice(0, 30),
            demoRoute: ['task', 'todo', 'pomodoro', 'ai', 'notes'].includes(raw.demoRoute) ? raw.demoRoute : null
        };
    }

    // ===== Similarity-based recommendations (v2 feature, adapted) =====
    function tokenizeForSimilarity(s) {
        const str = String(s || '');
        const parts = (str.match(/[A-Za-z0-9]+|[\u3040-\u30ff\u4e00-\u9fff]+/g) || [])
            .map(x => x.toLowerCase().trim())
            .filter(x => x.length >= 2);
        return Array.from(new Set(parts)).slice(0, 200);
    }

    function jaccard(a, b) {
        const A = new Set(Array.isArray(a) ? a.map(String) : []);
        const B = new Set(Array.isArray(b) ? b.map(String) : []);
        if (!A.size && !B.size) {return 0;}
        let inter = 0;
        for (const x of A) {if (B.has(x)) {inter++;}}
        const uni = A.size + B.size - inter;
        return uni ? inter / uni : 0;
    }

    function similarityScore(a, b) {
        if (!a || !b) {return 0;}
        const tagScore = jaccard(a.tags, b.tags);
        const techScore = jaccard(a.tech, b.tech);
        const catScore = (a.category && b.category && String(a.category) === String(b.category)) ? 1 : 0;

        const textA = [a.name, a.summary, a.problem, a.approach].join(' ');
        const textB = [b.name, b.summary, b.problem, b.approach].join(' ');
        const ta = new Set(tokenizeForSimilarity(textA));
        const tb = new Set(tokenizeForSimilarity(textB));
        let inter = 0;
        for (const t of ta) {if (tb.has(t)) {inter++;}}
        const textScore = (ta.size + tb.size) ? (2 * inter / (ta.size + tb.size)) : 0;

        const score = (0.40 * tagScore) + (0.30 * techScore) + (0.15 * catScore) + (0.15 * textScore);
        return Math.max(0, Math.min(1, score));
    }

    function autoRelatedCandidates(target, projects, limit = 8) {
        if (!target || !Array.isArray(projects)) {return [];}
        const fixed = new Set(target.relatedProjectIds || []);

        // Filter early to reduce similarity calculations
        return projects
            .filter(p => p && p.id && p.id !== target.id && !fixed.has(p.id))
            .map(p => ({ p, s: similarityScore(target, p) }))
            .filter(x => x.s > 0)
            .sort((a, b) => b.s - a.s)
            .slice(0, limit)
            .map(x => x.p);
    }



    // ===== Migration helper: keep all default projects (v2 baseline) while preserving user edits =====
    function mergeProjectsWithDefaults(incomingProjects) {
        const normalizedIncoming = (Array.isArray(incomingProjects) ? incomingProjects : [])
            .filter(p => p && typeof p === 'object')
            .map((p, idx) => normalizeProject(p, idx))
            .slice(0, CONSTANTS.LIMITS.MAX_PROJECTS);

        const normalizedDefaults = deepClone(defaultProjects)
            .filter(p => p && typeof p === 'object')
            .map((p, idx) => normalizeProject(p, idx));

        const incomingById = new Map(normalizedIncoming.map(p => [p.id, p]));

        const merged = normalizedDefaults.map(d => {
            const inc = incomingById.get(d.id);
            return inc ? ({ ...d, ...inc, id: d.id }) : d;
        });

        const mergedIds = new Set(merged.map(p => p.id));
        for (const p of normalizedIncoming) {
            if (!mergedIds.has(p.id)) {
                merged.push(p);
                mergedIds.add(p.id);
            }
        }

        // [FIX] slug 一意化: 上記 merge は ID でのみ dedupe するため、import データ等で別 id・同一
        // slug のプロジェクトが混在すると slug が重複し、ProjectDetailPage の find(p.slug===slug) が
        // 先頭のみ返して片方の詳細が到達不能になる。全 load/import/normalize が通るこのチョークポイントで
        // slug を一意化する (先頭=defaults を優先保持し、後続の衝突分へ -2,-3... を付与)。
        const _seenSlugs = new Set();
        for (const p of merged) {
            let s = p.slug || `p-${p.id}`;
            if (_seenSlugs.has(s)) {
                let n = 2;
                while (_seenSlugs.has(`${s}-${n}`)) { n++; }
                s = `${s}-${n}`;
                p.slug = s;
            }
            _seenSlugs.add(s);
        }

        return merged.slice(0, CONSTANTS.LIMITS.MAX_PROJECTS);
    }


    function normalizeAppsData(data) {
        const result = deepClone(defaultAppsData);

        // Tasks
        if (Array.isArray(data.tasks)) {
            result.tasks = data.tasks
                .filter(t => t && t.title)
                .map(t => ({
                    id: String(t.id || generateId()),
                    title: String(t.title).slice(0, CONSTANTS.LIMITS.TASK_TITLE),
                    status: ['backlog', 'in-progress', 'done'].includes(t.status) ? t.status : 'backlog',
                    priority: ['low', 'med', 'high'].includes(t.priority) ? t.priority : 'med',
                    tags: (t.tags || []).filter(Boolean).slice(0, 10),
                    createdAt: Number(t.createdAt) || Date.now(),
                    updatedAt: Number(t.updatedAt) || Date.now()
                }))
                .slice(0, CONSTANTS.LIMITS.MAX_TASKS);
        }

        // Todos
        if (Array.isArray(data.todos)) {
            result.todos = data.todos
                .filter(t => t && t.text)
                .map(t => ({
                    id: String(t.id || generateId()),
                    text: String(t.text).slice(0, CONSTANTS.LIMITS.TODO_TEXT),
                    completed: Boolean(t.completed),
                    createdAt: Number(t.createdAt) || Date.now(),
                    dueDate: t.dueDate ? Number(t.dueDate) : null
                }))
                .slice(0, CONSTANTS.LIMITS.MAX_TODOS);
        }

        // Pomodoro
        if (data.pomodoro) {
            if (data.pomodoro.settings) {
                result.pomodoro.settings = {
                    work: clamp(Number(data.pomodoro.settings.work) || 25, 1, 180),
                    short: clamp(Number(data.pomodoro.settings.short) || 5, 1, 60),
                    long: clamp(Number(data.pomodoro.settings.long) || 15, 1, 120)
                };
            }
            // [FIX] Array.isArray ガード必須。旧 `if (data.pomodoro.history)` は truthy 判定のみで、
            // 別 schema / 破損 store が history を非配列 (文字列等) で持つと String.prototype.slice が
            // 発火し「配列のはずが文字列」に型崩れ → 後続 PomodoroPage の history.map で crash する。
            // tasks/todos と同じく Array.isArray でガードし、非配列は default (空配列) にフォールバック。
            if (Array.isArray(data.pomodoro.history)) {
                result.pomodoro.history = data.pomodoro.history.slice(-200);
            }
            if (data.pomodoro.runtime) {
                const rt = data.pomodoro.runtime;
                const mode = ['work', 'short-break', 'long-break'].includes(rt.mode) ? rt.mode : 'work';
                const isActive = Boolean(rt.isActive) && rt.endAtMs && rt.endAtMs > Date.now();
                result.pomodoro.runtime = {
                    isActive,
                    mode,
                    endAtMs: isActive ? rt.endAtMs : null,
                    remainingSec: clamp(Number(rt.remainingSec) || 1500, 0, 86400),
                    linkedTaskId: rt.linkedTaskId || null
                };
            }
        }

        // AI History
        // [FIX] import / cross-tab 経由の ingestion では prompt / response の文字列長が
        // 未 bound だった (write 側 apps.js は prompt を AI_MESSAGE で bound 済だが、
        // load/import/cross-tab の正規化はこのチョークポイントを通る)。他アプリ
        // (tasks.title / todos.text / notes) と同様に normalize 側でも文字列長を
        // slice し、巨大 prompt/response が localStorage を bloat させる #230 class の
        // ingestion 側 gap を閉じる (entry 数 80 上限は従来どおり)。
        // [FIX] Array.isArray ガード必須 (#93/#295/#561 と同じ「外部 ingestion は全経路正規化」class)。
        // 旧 `if (data.ai?.history)` は truthy 判定のみで、別 schema / 破損 store が ai.history を
        // 非配列 (文字列/数値/オブジェクト) で持つと `.filter` が `TypeError: ... is not a function` を
        // throw し validateAndNormalize が例外 → load()/cross-tab(state.js)/import/snapshot-restore/
        // settings 正規化ボタンの全 ingestion 経路が FatalPage crash する。tasks/todos と同じく
        // Array.isArray でガードし、非配列は default (空配列) にフォールバックする総関数契約を守る。
        if (Array.isArray(data.ai?.history)) {
            result.ai.history = data.ai.history
                .filter(h => h && h.prompt && h.response)
                .map(h => ({
                    ...h,
                    prompt: String(h.prompt).slice(0, CONSTANTS.LIMITS.AI_MESSAGE),
                    response: String(h.response).slice(0, CONSTANTS.LIMITS.AI_MESSAGE)
                }))
                .slice(-80);
        }

        // Notes (Markdown 文字列・additive ゆえ schema bump 不要。上限で防御)
        if (typeof data.notes === 'string') {
            result.notes = data.notes.slice(0, 20000);
        }

        return result;
    }

    return { load, createDefaultStore, validateAndNormalize, autoRelatedCandidates };
}
