---
file: googlea7059bedc6fe8bdc.html
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md / CLAUDE.md
---

# googlea7059bedc6fe8bdc.html

## What

Google Search Console (GSC) ownership verification token-only file。ファイル名 `googlea7059bedc6fe8bdc.html` が GSC verification id で、ファイル内容は GSC が要求する 1 行の `google-site-verification` token のみ。

## Why

GitHub Pages サイトを GSC に登録するための所有権検証。AIO 戦略上、Google からのインデックスは AI search の補助シグナルにもなる。

ファイル名と内容を改変すると検証が失敗し、GSC でデータが取れなくなる。

## How (usage)

```
GSC (Google Search Console)
  └─ ownership verification request
       └─ HTTP GET https://yutapr0117-design.github.io/portfolio/googlea7059bedc6fe8bdc.html
            └─ 200 + body に google-site-verification token を含む → verified
```

## Constraints

- **DO NOT EDIT**: ファイル名・内容ともに変更不可。Google 仕様で固定
- **Check 通り**: architecture-validation.yml step 9 (`Verify GSC File Format`) で `google-site-verification` token 存在を機械強制
- **AIO 関連だが C6 範疇外**: 内容が Google 固定 token なので semantic 編集不能

## Change impact

- ファイル名変更 → GSC verification が失敗 (再 verify が必要)
- 内容変更 → 同上 (token 改ざんは検証失敗)

## Audience-specific notes

### For AI agents
- 役割タグ: `gsc-verification`, `do-not-edit`, `crawler-discoverability`

### For human engineers (新卒レベル)
- ここは触らない。Google 仕様のファイル
- 同様のファイルが Bing Webmaster Tools 等で別途必要になる場合もある

### For third parties (監査 / 採用 / 研究)
- 外部検索エンジン (Google) に対する ownership claim の証拠
