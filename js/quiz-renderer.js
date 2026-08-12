/**
 * js/quiz-renderer.js — QuizPage renderer (URL ?type で 4 quiz domain 切替・問題を read-only 表示・
 *   検索フィルタ・模範解答リクエスト contact form。採点/回答 flow は持たない)
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
 *   - QuizPage の DOM 出力・quiz domain lookup (QUIZ_DATA_MAP)・レンダリングは抽出時 byte-equivalent。検索フィルタ _filterBy は
 *     後の bug-fix で対象フィールドを拡張済（#285=stakeholder name/quote、#296=section 章タイトル。
 *     いずれも「画面に描画されるのに検索できない」visible-but-unsearchable drift の是正で、対象を増やす
 *     単調拡大ゆえ既存ヒットは不変）。
 *   - 4 quiz domain (AWS / PM / Quality / Architecture) の lookup table は不変
 *   - State.appsData.quizSearch 等の永続化への副作用も不変
 *   - AIDK Kernel / AIO 正本層 / style.css は無変更
 */
export function createQuizRenderer({ h, createIcon, Toast, Router, State, awsQuizData, pmQuizData, qualityQuizData, architectureQuizData }) {
    // [A11Y 3.1.2 Language of Parts] 文書は html lang="ja" なので、**日本語文字を 1 つも含まない
    //   塊**をそのまま置くと、日本語のスクリーンリーダーが英語を日本語の音韻で読み上げる
    //   (実測 #1020: quiz だけで 49 箇所 — うち "Core Knowledge & Tech Lead's View:" が 34 回)。
    //   行の言語は data (js/quiz/*.js) 側で混在するため静的には決められない。**描画時にその行の
    //   文字種で判定する**のが唯一 honest な方法で、判定は「日本語文字が無く Latin 文字がある」。
    //   AWS のサービス名のような固有名詞にも付くが、英語音韻で読ませたいのはむしろ正しい。
    const JA_CHARS = /[ぁ-んァ-ヶー一-龯]/;
    const langOfText = (t) => (!JA_CHARS.test(t) && /[A-Za-z]/.test(t) ? 'en' : undefined);

    function QuizPage() {
        const state = State.get();

        const route = Router.getRoute();
        const quizType = route.query.type || 'aws';

        // [FIX] 永続化された検索語は「入力された quiz 種別」と一致するときだけ復元する。従来は
        //   quizSearch 単一文字列を種別を問わず適用していたため、ある種別で検索したまま別の種別へ
        //   切り替えると語が持ち越され、切替先が「一致する問題は見つかりませんでした」の空ページに
        //   なっていた (sidebar の種別リンク / hiring-risk の CTA はどちらも主要導線)。
        const initialSearch = (state.appsData.quizSearchType === quizType)
            ? (state.appsData.quizSearch || "")
            : "";

        // ===== v40: Quiz data lookup table for extensibility =====
        const QUIZ_DATA_MAP = {
            aws: { title: 'AWS問題集', data: awsQuizData },
            pm: { title: 'PM問題集', data: pmQuizData },
            quality: { title: '品質・プロセス問題集', data: qualityQuizData },
            architecture: { title: '設計判断問題集', data: architectureQuizData }
        };
        // [FIX] URL 由来の外部入力を添字にするため own-key のみ採用する。素の `MAP[type] || fallback`
        //   は継承キー ('constructor' 等) で truthy な非 config 値を返して fallback を素通りし、
        //   Object.keys(undefined) が throw → FatalPage で表示不能だった (実測・#350 と同 class)。
        const quizConfig = Object.prototype.hasOwnProperty.call(QUIZ_DATA_MAP, quizType)
            ? QUIZ_DATA_MAP[quizType]
            : QUIZ_DATA_MAP.aws;
        const pageTitle = quizConfig.title;  // v40: BUGFIX - Define pageTitle from QUIZ_DATA_MAP
        const sourceData = quizConfig.data;
        const isArchitecture = quizType === 'architecture';

        const box = h("div", { class: "col col-centered" });

        box.appendChild(h("h1", { class: "h2", text: pageTitle }));

        // Search Input — listHost のみを手動再描画し input 自体は再生成しない (focus 保持)。
        // 旧実装は oninput→State.update→全再描画で input が破棄され、1 文字目で focus を失い
        // 検索が事実上使えなかった (確認済バグ)。ProjectsPage と同じ「リスト部分だけ独立」方式へ。
        const searchInput = h("input", {
            type: "search",
            class: "input pl-10",
            placeholder: "問題を検索...",
            value: initialSearch,
            'aria-label': '問題検索',
            oninput: (e) => {
                const val = e.target.value;
                State.updateSilently(s => { s.appsData.quizSearch = val; s.appsData.quizSearchType = quizType; });
                renderList(val);
            }
        });
        box.appendChild(h("div", { class: "mb-6" },
            // [A11Y] role='search' で検索入力を landmark 化する (ARIA APG search landmark)。
            //   SR ユーザーが landmark ナビゲーションで検索領域へ直接ジャンプできる (WCAG 1.3.1)。
            //   視覚描画は不変 (role 属性のみ・render-neutral)。ProjectsPage 検索と同型 (#879)。
            h("div", { class: "relative", role: "search" },
                searchInput,
                h("div", {
                    class: "absolute left-3 top-1/2 -translate-y-1/2 text-muted pointer-events-none"
                }, createIcon("search", 18))
            )
        ));

        // 検索結果を載せるホスト (input の外。oninput でここだけ作り直す)
        // [A11Y 4.1.3] 検索結果件数の live region。従来は 0 件のときだけ空状態 div が role=status を
        //   持ち **ヒット時は無言**だった (ProjectsPage は件数を通知するのに quiz だけ非対称)。
        //   listHost は毎キーストローク作り直されるため live region は外側の安定ノードに置く。sr-only。
        const resultStatus = h("div", { class: 'sr-only', role: 'status', 'aria-live': 'polite' }, '');
        box.appendChild(resultStatus);
        const listHost = h("div", {});
        box.appendChild(listHost);

        function _filterBy(rawQuery) {
            const query = String(rawQuery || '').toLowerCase().trim();
            const filtered = {};
            Object.keys(sourceData).forEach(section => {
                // section 見出し (画面に描画される章タイトル。例「第4章：可用性とFinOps（コスト）の天秤」)
                // も検索対象にする。タイトルにのみ含まれる topic 語 (FinOps / 可用性 / 泥沼 等) で検索した
                // とき「見えるのに 0 件」になる visible-but-unsearchable drift (#285 の stakeholder と同 class)
                // を防ぐ。section 名が一致したら、その章の全問を残す。
                const sectionMatch = !query || section.toLowerCase().includes(query);
                const questions = sourceData[section].filter(q => {
                    if (!query) {return true;}
                    if (sectionMatch) {return true;}
                    const titleMatch = q.title.toLowerCase().includes(query);
                    const idMatch = q.id.toLowerCase().includes(query);
                    const contentMatch = q.content ? q.content.some(line => line.toLowerCase().includes(query)) : false;
                    const situationMatch = q.situation ? q.situation.some(line => line.toLowerCase().includes(query)) : false;
                    const questionMatch = q.question ? q.question.toLowerCase().includes(query) : false;
                    // architecture quiz のステークホルダー主張 (name/quote) は画面描画されるが
                    // 従来フィルタ対象外で「見えるのに検索できない」状態だった。可視テキストを検索可能にする。
                    const stakeholderMatch = q.stakeholders ? q.stakeholders.some(sh =>
                        (sh.name && sh.name.toLowerCase().includes(query)) ||
                        (sh.quote && sh.quote.toLowerCase().includes(query))
                    ) : false;
                    return titleMatch || idMatch || contentMatch || situationMatch || questionMatch || stakeholderMatch;
                });
                if (questions.length > 0) {
                    filtered[section] = questions;
                }
            });
            return { filtered, query };
        }

        function renderList(rawQuery) {
            while (listHost.firstChild) { listHost.removeChild(listHost.firstChild); }
            const { filtered: quizData, query } = _filterBy(rawQuery);
            const matchCount = Object.keys(quizData).length;

            // 検索中のみ announce (初期描画で喋らない)。通知は resultStatus へ一本化する — 空状態 div
            // にも live region を持たせると同じ内容が 2 回読まれる (Toast 二重アナウンス #901 と同 class)。
            resultStatus.textContent = query
                ? (matchCount === 0
                    ? '「' + query + '」に一致する問題は見つかりませんでした。'
                    : '「' + query + '」に一致する問題 ' + matchCount + ' 件')
                : '';

            // 0件時UI (視覚表示。読み上げは resultStatus が担当するため live region にはしない)
            if (query && matchCount === 0) {
                listHost.appendChild(h("div", { class: 'card panel-empty' },
                    '「' + query + '」に一致する問題は見つかりませんでした。'));
                return;
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

                    // [A11Y 1.1.1] 章アイコンとゾーンラベルの絵文字は純粋な装飾。aria-hidden が
                    //   無いと SR は章題の前に「classical building」等を読み上げ、全章・全問で
                    //   意味の無い語が挟まる (実測: アクセシビリティツリーに絵文字が露出)。
                    const sHeader = h("div", { class: "quiz-section-header" });
                    sHeader.appendChild(h("div", { class: "quiz-section-icon", 'aria-hidden': 'true' }, icons[sIdx] || '📌'));
                    sHeader.appendChild(h("h2", { class: "quiz-section-title" }, section));
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
                        sitZone.appendChild(h("div", { class: "quiz-zone-label situation" }, h("span", { 'aria-hidden': 'true' }, "📋 "), "状況"));
                        const sitBody = h("div", { class: "quiz-zone-body" });
                        q.situation.forEach(line => {
                            sitBody.appendChild(h("p", { text: line }));
                        });
                        sitZone.appendChild(sitBody);
                        qBlock.appendChild(sitZone);

                        // ステークホルダーゾーン
                        const shZone = h("div", { class: "quiz-zone" });
                        shZone.appendChild(h("div", { class: "quiz-zone-label stakeholder" }, h("span", { 'aria-hidden': 'true' }, "💬 "), "ステークホルダーの主張"));
                        q.stakeholders.forEach(sh => {
                            const quote = h("div", { class: "quiz-stakeholder-quote" });
                            quote.appendChild(h("span", { class: "quiz-stakeholder-name" }, sh.name + ":"));
                            quote.appendChild(h("span", { text: "「" + sh.quote + "」" }));
                            shZone.appendChild(quote);
                        });
                        qBlock.appendChild(shZone);

                        // 問ゾーン
                        const qZone = h("div", { class: "quiz-zone" });
                        qZone.appendChild(h("div", { class: "quiz-zone-label question" }, h("span", { 'aria-hidden': 'true' }, "🎯 "), "問"));
                        qZone.appendChild(h("div", { class: "quiz-question-prompt" }, q.question));
                        qBlock.appendChild(qZone);

                        sCard.appendChild(qBlock);
                    });

                    wrapper.appendChild(sCard);
                });

                listHost.appendChild(wrapper);
            } else {
                // ===== v29: 既存問題集 — 改良レンダリング =====
                const wrapper = h("div", { class: "quiz-page-wrapper" });
                Object.keys(quizData).sort().forEach(section => {
                    const sCard = h("div", { class: "quiz-section-card" });

                    const sHeader = h("div", { class: "quiz-section-header" });
                    sHeader.appendChild(h("div", { class: "quiz-section-icon", 'aria-hidden': 'true' }, "📝"));
                    sHeader.appendChild(h("h2", { class: "quiz-section-title" }, section));
                    sCard.appendChild(sHeader);

                    const questions = quizData[section];
                    questions.forEach((q) => {
                        const qBlock = h("div", { class: "quiz-question-block" });

                        const qHeader = h("div", { class: "quiz-q-header" });
                        qHeader.appendChild(h("div", { class: "quiz-q-badge" }, q.id));
                        qHeader.appendChild(h("div", { class: "quiz-q-title", lang: langOfText(q.title) }, q.title.replace(q.id + '. ', '')));
                        qBlock.appendChild(qHeader);

                        q.content.forEach(line => {
                            if (!line.trim()) {return;}
                            // Check if it's a label line (ends with ':' or is a short header)
                            const isLabel = /^(状況|問|Challenge|Core Knowledge|境界点|Reboot vs|Stop|ASG|io2|gp[23]|注意|現場|意図|ポイント|解説|補足)[：:。]?/.test(line) || (line.endsWith(':') && line.length < 50);
                            qBlock.appendChild(h("div", {
                                class: "quiz-content-line text-prewrap" + (isLabel ? " is-label" : ""),
                                lang: langOfText(line)
                            }, line));
                        });

                        sCard.appendChild(qBlock);
                    });

                    wrapper.appendChild(sCard);
                });
                listHost.appendChild(wrapper);
            }
        }

        // 初回描画 (永続化された検索語を反映)
        renderList(initialSearch);

        // Contact form section
        const contactBox = h("div", { class: "card p col col-gap" });
        contactBox.appendChild(h("h2", { class: "h3", text: "模範解答について" }));
        contactBox.appendChild(h("div", { class: "muted" }, "模範解答をご希望の方は、以下のフォームからお気軽にご連絡ください。"));

        // [A11Y 3.3.2 Labels or Instructions / 4.1.2] お名前・メールアドレスは submit の JS バリデーション
        //   (`if (!name || !email)`) で必須だが、従来は required/aria-required 未指定で SR ユーザーには
        //   送信してエラー Toast が出るまで必須と分からなかった。aria-required='true' で必須状態を事前に
        //   露出する (メッセージは placeholder「（任意）」どおり optional ゆえ付与しない)。ARIA 属性のみ
        //   ゆえ native validation UI を発火させず既存の Toast バリデーション挙動は不変 (render-neutral)。
        const nameInput = h("input", { class: "input", type: "text", placeholder: "お名前", autocomplete: "name", 'aria-label': 'お名前', 'aria-required': 'true' });
        const emailInput = h("input", { class: "input", type: "email", placeholder: "メールアドレス", autocomplete: "email", 'aria-label': 'メールアドレス', 'aria-required': 'true' });
        const messageInput = h("textarea", { class: "input textarea-resize-v", rows: 4, placeholder: "メッセージ（任意）", 'aria-label': 'メッセージ' });

        const submitBtn = h("button", {
            class: "btn btn-primary",
            onclick: () => {
                const name = nameInput.value.trim();
                const email = emailInput.value.trim();
                const message = messageInput.value.trim();

                // [A11Y 3.3.1/2.4.3] 検証エラーは Toast だけでは「どのフィールドが不正か」が SR に伝わらず、
                //   利用者はフォームを探し直すことになる。不正な入力へ aria-invalid を立て、最初の不正
                //   フィールドへ focus を移す (属性 + focus のみ = 視覚描画は不変)。
                const markInvalid = (el, bad) => {
                    if (bad) { el.setAttribute('aria-invalid', 'true'); } else { el.removeAttribute('aria-invalid'); }
                };
                markInvalid(nameInput, !name);
                markInvalid(emailInput, !email);
                if (!name || !email) {
                    Toast.show("お名前とメールアドレスを入力してください", "error");
                    (!name ? nameInput : emailInput).focus();
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
