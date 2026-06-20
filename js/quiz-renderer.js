/**
 * js/quiz-renderer.js — QuizPage renderer (4 quiz domain selector + question / answer flow)
 * (v80+ Stage 5-o extraction via factory pattern)
 *
 * main.js の QuizPage を依存注入で物理分割した葉モジュール。Brand / Store / State /
 * Theme / Meta Management / Components / Apps と同じく、すべての closure 依存を
 * `createQuizRenderer` 関数の引数で受け取ることで、葉契約 (Check 47c: import ゼロ) を
 * 維持しつつ QuizPage の挙動と公開 API を完全に byte-equivalent に保つ。
 *
 * 【公開 API（抽出前後で byte-equivalent）】
 *   const { QuizPage } = createQuizRenderer({...});
 *
 * 【依存（引数で注入）】
 *   - h, createIcon, Toast: js/ui-components.js
 *   - Router: js/router.js
 *   - State: js/state.js factory instance
 *   - awsQuizData, pmQuizData, qualityQuizData, architectureQuizData:
 *     js/quiz/{aws,pm,quality,architecture}-quiz-data.js
 *
 * 【非破壊性】
 *   - QuizPage の DOM 出力・選択ロジック・スコア計算は byte-equivalent
 *   - 4 quiz domain (AWS / PM / Quality / Architecture) の lookup table は不変
 *   - State.appsData.quizSearch 等の永続化への副作用も不変
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 */
export function createQuizRenderer({ h, createIcon, Toast, Router, State, awsQuizData, pmQuizData, qualityQuizData, architectureQuizData }) {
    function QuizPage() {
        const state = State.get();
        const quizSearch = state.appsData.quizSearch || "";

        function handleSearch(e) {
            const val = e.target.value;
            State.update(s => { s.appsData.quizSearch = val; });
        }

        const route = Router.getRoute();
        const quizType = route.query.type || 'aws';

        // ===== v40: Quiz data lookup table for extensibility =====
        const QUIZ_DATA_MAP = {
            aws: { title: 'AWS問題集', data: awsQuizData },
            pm: { title: 'PM問題集', data: pmQuizData },
            quality: { title: '品質・プロセス問題集', data: qualityQuizData },
            architecture: { title: '設計判断問題集', data: architectureQuizData }
        };
        const quizConfig = QUIZ_DATA_MAP[quizType] || QUIZ_DATA_MAP.aws;
        const pageTitle = quizConfig.title;  // v40: BUGFIX - Define pageTitle from QUIZ_DATA_MAP
        let quizData = quizConfig.data;      // v40: BUGFIX - Use let for reassignment
        const isArchitecture = quizType === 'architecture';

        const box = h("div", { class: "col col-centered" });

        box.appendChild(h("h1", { class: "h2", text: pageTitle }));

        // Search Input
        box.appendChild(h("div", { class: "mb-6" },
            h("div", { class: "relative" },
                h("input", {
                    type: "text",
                    class: "input pl-10",
                    placeholder: "問題を検索...",
                    value: quizSearch,
                    'aria-label': '問題検索',
                    oninput: handleSearch
                }),
                h("div", {
                    class: "absolute left-3 top-1/2 -translate-y-1/2 text-muted pointer-events-none"
                }, createIcon("search", 18))
            )
        ));

        // v40: QUIZ_DATA_MAP moved above for early pageTitle definition


        // Filter quizData based on search query
        const filteredQuizData = {};
        const query = quizSearch.toLowerCase().trim();

        Object.keys(quizData).forEach(section => {
            const questions = quizData[section].filter(q => {
                if (!query) {return true;}
                const titleMatch = q.title.toLowerCase().includes(query);
                const idMatch = q.id.toLowerCase().includes(query);
                const contentMatch = q.content ? q.content.some(line => line.toLowerCase().includes(query)) : false;
                const situationMatch = q.situation ? q.situation.some(line => line.toLowerCase().includes(query)) : false;
                const questionMatch = q.question ? q.question.toLowerCase().includes(query) : false;
                return titleMatch || idMatch || contentMatch || situationMatch || questionMatch;
            });
            if (questions.length > 0) {
                filteredQuizData[section] = questions;
            }
        });
        quizData = filteredQuizData;

        // 0件時UI
        if (query && Object.keys(quizData).length === 0) {
            box.appendChild(h("div", {
                class: 'card panel-empty',
                role: 'status',
                'aria-live': 'polite'
            }, '「' + query + '」に一致する問題は見つかりませんでした。'));
            const contactBox2 = h("div", { class: "card p col col-gap" });
            contactBox2.appendChild(h("div", { class: "h3", text: "模範解答について" }));
            contactBox2.appendChild(h("div", { class: "muted" }, "模範解答をご希望の方は、以下のフォームからお気軽にご連絡ください。"));
            box.appendChild(contactBox2);
            return box;
        }

        // ===== v29: 意思決定問題集 — 構造化レンダリング =====
        if (isArchitecture) {
            const wrapper = h("div", { class: "quiz-page-wrapper" });

            // intro banner
            const introBanner = h("div", {
                class: 'card card--gradient-primary'
            },
                h("div", { class: 'text-overline' }, "設計判断問題集（SREサバイバル）"),
                h("div", { class: 'text-body-relaxed' },
                    "実務で起きる「誘惑的な技術的判断ミス」を題材にした問題集。各問はステークホルダーの主張とともに提示される。トレードオフを整理し、現場指揮官として意思決定を下せ。"
                )
            );
            wrapper.appendChild(introBanner);

            Object.keys(quizData).forEach((section, sIdx) => {
                const questions = quizData[section];
                const icons = ['🏛️', '🗄️', '🔌', '⚖️', '🚨', '🔁'];

                const sCard = h("div", { class: "quiz-section-card" });

                const sHeader = h("div", { class: "quiz-section-header" });
                sHeader.appendChild(h("div", { class: "quiz-section-icon" }, icons[sIdx] || '📌'));
                sHeader.appendChild(h("div", { class: "quiz-section-title" }, section));
                sCard.appendChild(sHeader);

                questions.forEach((q) => {
                    const qBlock = h("div", { class: "quiz-question-block" });

                    // Q header
                    const qHeader = h("div", { class: "quiz-q-header" });
                    qHeader.appendChild(h("div", { class: "quiz-q-badge" }, q.id));
                    qHeader.appendChild(h("div", { class: "quiz-q-title" }, q.title));
                    qBlock.appendChild(qHeader);

                    // 状況ゾーン
                    const sitZone = h("div", { class: "quiz-zone" });
                    sitZone.appendChild(h("div", { class: "quiz-zone-label situation" }, "📋 状況"));
                    const sitBody = h("div", { class: "quiz-zone-body" });
                    q.situation.forEach(line => {
                        sitBody.appendChild(h("p", { text: line }));
                    });
                    sitZone.appendChild(sitBody);
                    qBlock.appendChild(sitZone);

                    // ステークホルダーゾーン
                    const shZone = h("div", { class: "quiz-zone" });
                    shZone.appendChild(h("div", { class: "quiz-zone-label stakeholder" }, "💬 ステークホルダーの主張"));
                    q.stakeholders.forEach(sh => {
                        const quote = h("div", { class: "quiz-stakeholder-quote" });
                        quote.appendChild(h("span", { class: "quiz-stakeholder-name" }, sh.name + ":"));
                        quote.appendChild(h("span", { text: "「" + sh.quote + "」" }));
                        shZone.appendChild(quote);
                    });
                    qBlock.appendChild(shZone);

                    // 問ゾーン
                    const qZone = h("div", { class: "quiz-zone" });
                    qZone.appendChild(h("div", { class: "quiz-zone-label question" }, "🎯 問"));
                    qZone.appendChild(h("div", { class: "quiz-question-prompt" }, q.question));
                    qBlock.appendChild(qZone);

                    sCard.appendChild(qBlock);
                });

                wrapper.appendChild(sCard);
            });

            box.appendChild(wrapper);
        } else {
            // ===== v29: 既存問題集 — 改良レンダリング =====
            const wrapper = h("div", { class: "quiz-page-wrapper" });
            Object.keys(quizData).sort().forEach(section => {
                const sCard = h("div", { class: "quiz-section-card" });

                const sHeader = h("div", { class: "quiz-section-header" });
                sHeader.appendChild(h("div", { class: "quiz-section-icon" }, "📝"));
                sHeader.appendChild(h("div", { class: "quiz-section-title" }, section));
                sCard.appendChild(sHeader);

                const questions = quizData[section];
                questions.forEach((q) => {
                    const qBlock = h("div", { class: "quiz-question-block" });

                    const qHeader = h("div", { class: "quiz-q-header" });
                    qHeader.appendChild(h("div", { class: "quiz-q-badge" }, q.id));
                    qHeader.appendChild(h("div", { class: "quiz-q-title" }, q.title.replace(q.id + '. ', '')));
                    qBlock.appendChild(qHeader);

                    q.content.forEach(line => {
                        if (!line.trim()) {return;}
                        // Check if it's a label line (ends with ':' or is a short header)
                        const isLabel = /^(状況|問|Challenge|Core Knowledge|境界点|Reboot vs|Stop|ASG|io2|gp[23]|注意|現場|意図|ポイント|解説|補足)[：:。]?/.test(line) || (line.endsWith(':') && line.length < 50);
                        qBlock.appendChild(h("div", {
                            class: "quiz-content-line text-prewrap" + (isLabel ? " is-label" : "")
                        }, line));
                    });

                    sCard.appendChild(qBlock);
                });

                wrapper.appendChild(sCard);
            });
            box.appendChild(wrapper);
        }

        // Contact form section
        const contactBox = h("div", { class: "card p col col-gap" });
        contactBox.appendChild(h("div", { class: "h3", text: "模範解答について" }));
        contactBox.appendChild(h("div", { class: "muted" }, "模範解答をご希望の方は、以下のフォームからお気軽にご連絡ください。"));

        const nameInput = h("input", { class: "input", type: "text", placeholder: "お名前", 'aria-label': 'お名前' });
        const emailInput = h("input", { class: "input", type: "email", placeholder: "メールアドレス", 'aria-label': 'メールアドレス' });
        const messageInput = h("textarea", { class: "input textarea-resize-v", rows: 4, placeholder: "メッセージ（任意）", 'aria-label': 'メッセージ' });

        const submitBtn = h("button", {
            class: "btn btn-primary",
            onclick: () => {
                const name = nameInput.value.trim();
                const email = emailInput.value.trim();
                const message = messageInput.value.trim();

                if (!name || !email) {
                    Toast.show("お名前とメールアドレスを入力してください", "error");
                    return;
                }

                const subject = encodeURIComponent(`${pageTitle}の模範解答について`);
                const body = encodeURIComponent(
                    `お名前: ${name}\nメールアドレス: ${email}\n\nメッセージ:\n${message || "(なし)"}`
                );
                const currentState = State.get();
                location.href = `mailto:${currentState.profile.email}?subject=${subject}&body=${body}`;
            }
        }, "送信");

        contactBox.appendChild(h("div", { class: "col col-gap-10" },
            h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "お名前 *" }), nameInput),
            h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "メールアドレス *" }), emailInput),
            h("div", { class: "col col-gap-sm" }, h("div", { class: "mini", text: "メッセージ" }), messageInput),
            submitBtn
        ));

        box.appendChild(contactBox);

        return box;
    }

    return { QuizPage };
}
