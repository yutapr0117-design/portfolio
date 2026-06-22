---
file: icon.svg
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-22
canonical-ref: manifest.webmanifest (icons) / index.html (rel=icon, apple-touch-icon)
---

# icon.svg

## What

PWA / favicon / apple-touch アイコン。512x512 viewBox の正方形 SVG。ブランド色グラデーション(#6366f1→#818cf8)の角丸正方形に、中央ハブ(人間 PM)と周囲 4 ノード(AI)を線で結んだ「人間が統治する AI オーケストレーション」を表すマーク。manifest.webmanifest の icons と index.html の rel=icon / apple-touch-icon から参照。

## Why

B-group 案2(PWA)で installable にするためアイコンが必要。square PNG を生成できないため、C1(Boring Tech・依存ゼロ)準拠で手書き可能な SVG で作成。SVG アイコンは sizes:any で modern ブラウザに対応し、解像度非依存。デザインは中心メッセージ A(人間統治 × AI 自走/オーケストレーション)を象徴する node-graph。

## How (usage)

manifest の icon(purpose: any maskable)+ ブラウザタブ favicon + iOS apple-touch-icon として表示。

## Constraints

- **正方形 / viewBox 512**: maskable 対応のため content は中央安全圏に配置。
- **C1 準拠**: 外部依存なし(純 SVG)。
- **ブランド整合**: theme_color(#6366f1)と一致。

## Change impact

- ブランド色/マーク変更時は本 SVG を更新(manifest は src 参照のみゆえ通常不変)。

## Audience-specific notes

### For AI agents
- 役割タグ: `pwa-icon`, `favicon`, `brand-mark`

### For human engineers (新卒レベル)
- SVG なので解像度非依存。PNG 不要で installable アイコンを満たす。

### For third parties
- 「人間が統治する AI オーケストレーション」を象徴する node-graph マーク。
