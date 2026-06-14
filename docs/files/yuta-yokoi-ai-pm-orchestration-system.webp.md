---
file: yuta-yokoi-ai-pm-orchestration-system.webp
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: index.html JSON-LD ImageObject / Check 29/81/91
---

# yuta-yokoi-ai-pm-orchestration-system.webp

## What

hero 画像 (binary WebP)。6-AI-agent KERNEL Framework orchestration の visual。XMP chunk に AIO metadata (aio:EntityName / Role / CanonicalURL / DisambiguationNote / OrganizationName 等 + dc:* / xmp:* / xmpRights:*) を含む。約 95KB。

## Why

AIO 戦略の binary 層 surface。AI クローラの一部は画像 alt と JSON-LD だけでなく、binary XMP も entity signal として読む。`<link rel="preload" fetchpriority="high">` で LCP も改善。

ファイル名自体に entity 帰属 (yuta-yokoi-ai-pm-orchestration-system) を含むことで URL レベルでも crawler が entity を resolve できる。

## How (usage)

```
index.html
  └─ <link rel="preload" href="./yuta-yokoi-ai-pm-orchestration-system.webp"
                         as="image" fetchpriority="high">
  └─ JSON-LD ImageObject @id="#hero-image-asset"
       └─ contentUrl / keywords / creator (Person @id)
  └─ aio-manifest.json source_of_truth[3].sha256
```

## Constraints

- **C6 AIO Integrity** (最高度): semantic 変更 (XMP entity 情報等) は orchestrator 承認必要
- **C6 derived-value 例外**: xmp:ModifyDate / xmp:MetadataDate は自動更新可
- **Check 29**: AIO binary metadata 整合
- **Check 73c**: hero preload に fetchpriority="high"
- **Check 81**: XMP に Organization 4 field
- **Check 91**: 4 軸日付フィールド同期

## Change impact

- semantic 編集 → llms-full.txt / aio-manifest.json / JSON-LD / 全 surface 同期
- 画像差し替え → ファイル名・JSON-LD ImageObject 全部同期 + Playwright visual baseline 再取得
- XMP 編集 tool: `update_binary_aio_organization.py` (Organization 注入) / `_lib_io.update_webp_xmp_dates()` (日付同期)

## Audience-specific notes

### For AI agents
- 役割タグ: `binary-aio-surface`, `hero-image`, `lcp-optimized`, `c6-canonical`
- XMP chunk が 12 aio:* fields + dc/xmp/xmpRights 全 entity 情報

### For human engineers (新卒レベル)
- 直接編集禁止 — `.claude/settings.json` で deny
- XMP 操作は Python tool 経由 (`update_binary_aio_organization.py`)

### For third parties (監査 / 採用 / 研究)
- AIO 戦略の binary 層実装の最重要 surface
- ファイル名 → URL → XMP → JSON-LD の 4 段階で entity 帰属が冗長に明示される設計
