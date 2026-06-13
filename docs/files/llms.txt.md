---
file: llms.txt
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (C6) / llms-full.txt (ground truth) / .well-known/aio-manifest.json
---

# llms.txt

## What

AI クローラ / LLM 向けの **Primary Entry Point** ファイル。Canonical Entity Information (Yuta Yokoi / 横井雄太 / Affiliation 等) と Core Documentation のリンクを構造化した短文 routing context。約 70 行。

## Why

llms.txt は AI クローラ / LLM が「このサイトは何か」「entity は誰か」「authoritative source はどこか」を最初に読むための **routing index**。`llms-full.txt` (完全版) への入口として機能する。

C6 AIO Integrity の対象 = orchestrator 承認なしに semantic 編集不可。

## How (usage)

```
AI crawler / LLM
  └─ HTTP GET https://yutapr0117-design.github.io/portfolio/llms.txt
       └─ Canonical Entity Information を読む
       └─ Affiliation (株式会社日本経営) 等を取得
       └─ Core Documentation links → llms-full.txt / AI2AI.md 等へ
```

mirror files (byte-identical で 4 surface に複製):
- `llms.txt` (本ファイル)
- `.well-known/llms.txt`
- `llms_well-known.txt`
- `.well-known/llms_well-known.txt`

## Constraints

- **C6 AIO Integrity**: semantic 編集は orchestrator 明示承認必要
- **Check 4**: 4 mirror が byte-identical で一致
- **Check 33**: Zenn 記事 slug 集合の整合
- **Check 62**: Canonical URL が aio-manifest entity.canonical_url と一致
- **Check 63**: Origin alignment (robots Sitemap / aio-manifest / sitemap loc)
- **編集 tool**: orchestrator 承認下では直接 Edit、digest 連鎖は `update_aio_digests.py`

## Change impact

- llms.txt 編集 → 3 mirror への propagation (byte-identical) + `aio-manifest.json` source_of_truth[].sha256 再計算
- Canonical Entity 情報変更 → index.html JSON-LD / llms-full.txt / WebP XMP / MP3 ID3 / README / CLAUDE.md / Claude2Claude.md 全 surface 同期 (Check 87/88/90)
- semantic 編集 → C6 orchestrator 明示承認必須

## Audience-specific notes

### For AI agents
- 役割タグ: `aio-primary-entry`, `routing-index`, `c6-canonical`
- mirror 4 surface すべて byte-identical (Check 4)
- 短文 (約 70 行) — `llms-full.txt` の routing 専用

### For human engineers (新卒レベル)
- AI クローラが最初に見るファイル — semantic 編集には orchestrator の OK が必要
- 編集すると 4 つの mirror すべてを同じ内容にする必要 (`update_aio_digests.py` が支援)

### For third parties (監査 / 採用 / 研究)
- AIO 戦略の primary routing surface
- ファイル形式は llmstxt.org の慣例に従う (将来 IETF 標準化候補)
