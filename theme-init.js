        // WHY この script が存在するか / なぜ <head> で render-blocking に置くか:
        //   main.js (ESM) は async ロードされるため、適用前に最初のペイントが走ると
        //   一瞬 light テーマが見えてから dark に切替わる FOUC（Flash of Unstyled/
        //   Incorrect Theme）が起きる。これを防ぐため、CSS 適用より前の同期実行点で
        //   localStorage から theme/brand を復元し data-theme / .dark / data-brand を
        //   先に確定させる。
        // HIDDEN INVARIANT: 下記の localStorage キーは main.js ロード前に動く必要があるため、
        //   CONSTANTS.STORAGE_KEY ('portfolio_enhanced_v45') と Brand.KEY ('portfolio_brand_v45')
        //   を **意図的にハードコード複製** している。State/Brand 側でキーや theme schema を
        //   変えたら、この 2 リテラルも同時更新しないと初期ペイントだけ旧値になる（要同時更新）。
        // 空 catch の理由: 復元失敗は描画を絶対に止めてはならない（fail-open）。テーマ復元は
        //   best-effort であり、失敗時は CSS デフォルト（light）で描画継続する。
        (function() {
            try {
                // Theme復元（FOUC を防ぐため CSS より先に実行）
                const rawState = localStorage.getItem('portfolio_enhanced_v45');
                if (rawState) {
                    const state = JSON.parse(rawState);
                    if (state && state.theme) {
                        const isDark = state.theme === 'dark' ||
                            (state.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
                        document.documentElement.setAttribute('data-theme', state.theme);
                        if (isDark) {document.documentElement.classList.add('dark');}
                    }
                }
                // Brand復元
                const rawBrand = localStorage.getItem('portfolio_brand_v45');
                if (rawBrand) {
                    document.documentElement.setAttribute('data-brand', rawBrand);
                }
            } catch (e) {}
        })();
