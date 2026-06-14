/* eslint-disable -- KARTE official vendor analytics snippet (minified). Do not restyle: it is third-party integration code, not maintained in this repo. */
/* WHY この stub が存在するか: 実体の KARTE script は CDN から async ロードされる。先にこの
   queue-stub (`krt` グローバル) を同期定義しておくことで、ロード完了前の `krt(...)` 呼び出しを
   o.q に buffer し、ロード後に o.x へ flush する。これを「未使用」と見て消すと初期計測が落ちる。
   関連制約: C7 — KARTE CDN には SRI を付けない（外部更新で prod ロードが壊れるため）。接続は
   index.html の CSP connect-src/script-src で制限する方針。 */
!function(n){if(!window[n]){var o=window[n]=function(){var n=[].slice.call(arguments);return o.x?o.x.apply(0,n):o.q.push(n)};o.q=[],o.i=Date.now(),o.allow=function(){o.o="allow"},o.deny=function(){o.o="deny"}}}("krt")
