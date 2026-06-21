/**
 * page-meta.js — 全ページの SEO メタ情報（タイトル・説明文）の単一ソース
 *
 * @fileoverview v80+ Stage 5: main.js から抽出した AI SURFACE 層のデータモジュール。
 * 静的エントリは純データ。動的エントリ（project-detail / quiz）は
 * { params, state, route } を受け取る純粋関数——外部状態を閉じ込めず、
 * 呼び出し側が State.get() の結果を渡す設計のため closure-deps = none。
 *
 * export:
 *   PAGE_META  — ルート名 → { title, desc } のマップ（AI SURFACE・編集可）
 *
 * 不変条件:
 *   - 本モジュールは葉（ローカル ESM import ゼロ）。
 *   - 動的 title/desc は引数の state/params/route のみを参照し、グローバル状態に触れない。
 *   - キー一覧はルーター定義（Router.parse）と一致させること（不一致は MetaMgmt で silent fallback）。
 */

// ===== v27: PAGE_META — 全ページSEOの単一ソース =====
/* ╔══ AI SURFACE START — PAGE_META（ルートメタ情報）はAIが編集可能 ══╗ */
export const PAGE_META = {
    home: { title: 'Home', desc: '設計思想と実験的SPAポートフォリオ。最小構成での設計判断を重視。' },
    projects: { title: 'Projects', desc: '設計判断と成果物。Case Study形式でアーキテクチャ・成果を掲載。' },
    'project-detail': {
        title: ({ params, state }) => {
            const p = state.projects.find(x => x.slug === params.slug);
            return p ? p.name : 'Project Detail';
        },
        desc: ({ params, state }) => {
            const p = state.projects.find(x => x.slug === params.slug);
            return p ? p.summary : 'プロジェクトの設計意図、技術選定、および成果の詳細。';
        }
    },
    apps: { title: 'Apps', desc: '内蔵アプリ（タスク管理 / TODO / ポモドーロ / ローカルAI）。' },
    'app-task': { title: 'Task Manager', desc: 'タスク管理アプリ。ステータス管理・優先順位付き。' },
    'app-todo': { title: 'Quick TODO', desc: 'クイックTODOリスト。シンプルで高速。' },
    'app-pomodoro': { title: 'Pomodoro Timer', desc: 'ポモドーロタイマー。集中と休憩を自動制御。' },
    'app-ai': { title: 'AI Assist', desc: 'AIアシスト。ローカル思考補助ツール。' },
    'app-notes': { title: 'Markdown Notes', desc: 'Markdown ライブプレビュー・ノート。innerHTML 不使用の安全レンダリング。' },
    settings: { title: 'Settings', desc: '設定・テーマ・DEBUG。Import/Export・整合性チェック・スナップショット。' },
    about: { title: 'About', desc: 'プロフィール。ITエンジニアとしての経歴・思想。' },
    resume: { title: 'Resume', desc: '職務経歴。設計力・問題解決能力・継続改善習慣。' },
    contact: { title: 'Contact', desc: 'お問い合わせ。メール・GitHub・LinkedIn。' },
    quiz: {
        title: ({ route }) => {
            const type = route.query.type || 'aws';
            const map = {
                aws: 'AWS問題集',
                pm: 'PM問題集',
                quality: '品質・プロセス問題集',
                architecture: '設計判断問題集'
            };
            return map[type] || 'Quiz';
        },
        desc: 'AWS / PM / 品質 / 意思決定問題集。実務シナリオ×思考外部化ライブラリ。'
    },
    'hiring-risk': {
        title: 'Hiring Risk Reduction',
        desc: '採用側リスク低減構造・経営インパクト・KPI・意思決定アルゴリズムを明示。経営層・PM・エンジニア全層対応。'
    },
    'not-found': { title: 'Not Found', desc: 'ページが見つかりません。' },
    'ai-knowhow': { title: 'AI開発ノウハウ', desc: 'KERNELフレームワーク・6エージェント役割・LLMコスト管理など、AI-Driven PMのリアルな開発ノウハウを公開。' },
    'role-split': { title: 'Human vs AI 分担表', desc: '人間とAIの役割分担を明示。アーキテクチャ・判断・検証を担う人間と、実装・生成・補助を担うAIの具体的な責任範囲を整理。' }
};
/* ╚══ AI SURFACE END ══╝ */
