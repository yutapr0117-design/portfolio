---
file: .github/scripts/check_deployed_freshness.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-11
canonical-ref: .github/workflows/aio-monitoring.yml / .github/scripts/generate_status.py / docs/architecture/check-repository-consistency-map.md
---

# .github/scripts/check_deployed_freshness.py

## What

公開サイト（GitHub Pages）が**リポジトリと同じ版を配信しているか**、そして**宣言している資産が
実際に配信されているか**を検証するスクリプト。2 つのパスから成る。

1. **版数の一致**: `main.js` の `SITE_CONFIG.VERSION` / `LAST_UPDATED` と、公開 `index.html` の
   `<meta name="ai:version">` / `<meta name="ai:last-modified">` を比較。
2. **資産の到達性**: 公開 `index.html` が宣言している同一オリジンの参照（`href` / `src` / 絶対 URL の
   `meta content`）と、`.well-known/` 配下の tracked file を**すべて実際に GET** して 200 を確認。

いずれも食い違えば exit 1。

## Why

デプロイ連鎖には **2 つの別々の失敗モード**がある。

1. **ジョブが失敗する** — `pages-build-deployment` のバッジ（STATUS.md / Check 415）が見ている。
2. **ジョブは成功するが、配信されている中身が古い** — 2026-08-11 まで**どの層も見ていなかった**。

2 が見えていなかった理由は、既存のゲートがどれも公開サイトを触らないから:

- PR ゲート（architecture-validation / playwright）は **ローカルの `http-server`** に対して走る。
- **Check 2 / 17 / 180** は `main.js` と `index.html` が **リポジトリ内で**一致することしか見ない。
  両方が正しくても、配信されているのが数週間前の成果物なら気付けない。
- `aio-monitoring.yml` は AI エンジンへの問い合わせログを取るだけで、版数を照合しない。

結果、「Pages が古い成果物を配信し続けている」状態が **全ゲート緑のまま**成立しうる。
リポジトリが本体でサイトは付属物という位置づけでも、機能性（loads / displays / comprehensible）は
死守する契約（`CLAUDE.md` §3(B)）なので、配信の陳腐化は検出できなければならない。

### 資産の到達性を別パスにしている理由（`.nojekyll` の canary）

**GitHub Pages の Jekyll 処理は `.` / `_` で始まるディレクトリを配信対象から落とす。** つまり
`.nojekyll` が失われると **`.well-known/` が丸ごと 404 になる** —— このプロジェクトの中核賭け金で
ある AIO 層が、リポジトリには存在したまま公開面からだけ消える。リポジトリ側の Check は
`.nojekyll` という *file の存在* を見るだけで *その効果* は見ていないので、この失敗も
**全ゲート緑のまま**起きる。

`.well-known/` 配下は `git ls-files` から**導出**する（ハードコードすると追加時に drift する）。
2026-08-11 時点で 7 件で、うち `.well-known/agent-skills/index.json` と `.well-known/mcp.json` は
`index.html` から参照されていない —— **参照グラフからは辿れないが 404 になれば致命的**という、
canary として最も価値のある位置にある。

## How (usage)

```
python3 .github/scripts/check_deployed_freshness.py
  → deployed: https://.../index.html
    ai:version       = 'v74'  (repo: 'v74')
    ai:last-modified = '2026-05-31'  (repo: '2026-05-31')
    OK: 公開サイトはリポジトリと同じ版を配信している
    OK: 公開サイトが宣言している資産 54 件がすべて 200 で配信されている
```

週次 `aio-monitoring.yml` の**最初のステップ**として走る（API キー切れ等で後段がスキップされても
この検証は必ず走るように、クエリより前に置いてある）。

## Constraints

- **Check 423（BLOCKING）**: 本スクリプトが `aio-monitoring.yml` から呼ばれていること。
  script が存在するだけでは走らないため、「存在 ≠ 配線」の穴（Check 133 / 134 / 135 と同 class）を塞ぐ。
- **Check 108**: 本 mirror doc の存在。
- **比較対象の選択理由**: `VERSION` / `LAST_UPDATED` は **明示的な版数更新のときしか変わらない**。
  コミット SHA のような毎回変わる値を比べると、merge 直後の実行がデプロイ完了前になり
  **週次バッジが恒常的に赤くなって赤が意味を失う**。「数週間デプロイが壊れている」という
  本当に知りたい状態だけが赤くなるように選んである。
- **canonical URL は導出**: `CLAUDE.md` の canonical site URL から取る（ハードコードは drift する）。
- **ネットワーク失敗の扱い**: 3 回リトライしたうえで**失敗扱い**。週次実行なので、一時的な瞬断より
  「公開サイトに到達できない状態が続いている」ことの方が重大で、それこそ知りたい情報だから。

## Change impact

- 版数を上げる増分（Version Update Checklist）では、デプロイが反映されるまでの間だけ
  この検証が赤くなりうる。週次実行なので実際に重なる確率は低いが、重なった場合は
  デプロイ完了後に `workflow_dispatch` で再実行すればよい。
- 比較対象を増やす場合は「毎回変わる値を混ぜない」原則を守ること。

## Audience-specific notes

### For AI agents
- 役割タグ: `deployment-verification`, `observability`, `wiring-guard`

### For human engineers (新卒レベル)
- 「CI が緑」と「本番が正しい」は別物、という一般則のこのリポジトリでの実装例。

### For third parties
- 静的サイトでも「デプロイの成功」と「配信内容の鮮度」を分けて監視できる、という最小実装。
