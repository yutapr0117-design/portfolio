        (function() {
            try {
                // Theme復元（FLOCKを防ぐためCSSより先に実行）
                var rawState = localStorage.getItem('portfolio_enhanced_v45');
                if (rawState) {
                    var state = JSON.parse(rawState);
                    if (state && state.theme) {
                        var isDark = state.theme === 'dark' ||
                            (state.theme === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
                        document.documentElement.setAttribute('data-theme', state.theme);
                        if (isDark) document.documentElement.classList.add('dark');
                    }
                }
                // Brand復元
                var rawBrand = localStorage.getItem('portfolio_brand_v45');
                if (rawBrand) {
                    document.documentElement.setAttribute('data-brand', rawBrand);
                }
            } catch (e) {}
        })();
