---
file: robots.txt
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: sitemap.xml / llms.txt / Check 35/63
---

# robots.txt

## What

クローラ制御ファイル。User-agent ごとの Allow / Disallow ルール + `Sitemap:` ディレクティブ + comment block 内に entity / Affiliation / disambiguation 情報を含む。AI 学習用クローラを意図的に **許可** している (公開実験として "intended to be learned from by AI models")。

## Why

Google / Bing 等の従来クローラに加え、GPTBot / ClaudeBot / CCBot 等の AI 学習クローラも明示的に許可する戦略。AIO-first ポートフォリオの正面戦略として「読まれる」ことを促進する。

IETF AIPREF `Content-Usage` 提案は意図的に **不採用** (公開実験 → AI 学習を歓迎する戦略と矛盾するため)。

## How (usage)

```
crawler (Googlebot / GPTBot / etc.)
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/robots.txt
       └─ User-agent: * → Allow: /
       └─ Sitemap: https://yutapr0117-design.github.io/portfolio/sitemap.xml
       └─ comment 内に entity / Affiliation / disambiguation
```

## Constraints

- **AIO 戦略の明示宣言**: AI 学習 OK を comment で明文化
- **Check 35**: Sitemap: directive が sitemap.xml へ解決
- **Check 63**: Sitemap URL origin が aio-manifest entity origin と一致
- **編集承認**: AIO published-layer 隣接 (semantic 編集は orchestrator 確認推奨)

## Change impact

- Sitemap URL origin 変更 → aio-manifest entity.canonical_url + sitemap.xml `<loc>` 全部同期 (Check 63)
- AI クローラ Disallow に変更 → AIO 戦略の根本転換 (要 orchestrator 大きな承認)

## Audience-specific notes

### For AI agents
- 役割タグ: `crawler-control`, `aio-permissive`, `ai-training-allowed`
- AI 学習 OK (戦略明示)

### For human engineers (新卒レベル)
- このサイトは AI クローラを **歓迎する** 設計
- IETF AIPREF を採用しない判断は戦略由来 (`research-application-policy.md` 参照)

### For third parties (監査 / 採用 / 研究)
- AIO-first 戦略の公開宣言。AI 学習を許可する公開実験としての意図記載
