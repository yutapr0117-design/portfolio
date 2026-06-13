---
file: main.js
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-06-13
canonical-ref: AI2AI.md (canon C1-C7) / CLAUDE.md §3 (kernel 保護) / docs/architecture/main-js-extraction-map.md / docs/architecture/repository-maintainability-map.md
---

# main.js

## What

このリポジトリで配信される SPA (Single Page Application) の **最後の monolithic ファイル**であり、AIDK (AI Development Kernel) Isolated Kernel と View Transition Proxy と Trusted Types Policy と single top-level IIFE を含む **不可侵領域** (DO NOT EDIT) と、24 個の葉モジュール (`js/*.js` / `js/quiz/*.js`) を合成する factory 呼び出し本体。Stage 5 物理分割を経て 7,785 行 → **1,086 行 (−86%)** に縮小済み。

## Why

このファイルの存在理由は **AIDK Kernel の物理的安全領域** を確保するため。

歴史的に main.js は 7,785 行に肥大化していたが、Stage 5 で 16 個の小さな増分 (Stage 5-c〜5-s) を経て葉モジュールを段階的に抽出した。残った 1,086 行は技術的に **「これ以上分割すると Kernel が壊れる」** という工学的限界に達した部分:

- **AIDK Kernel proper**: View Transition API の同期実行・error boundary・graceful degradation
- **startViewTransitionProxy** (L150 周辺): Chrome の View Transition API の競合 / timeout を吸収
- **Trusted Types Policy** (L211 周辺): CSP `require-trusted-types-for` に対応した innerHTML safe wrapper
- **single top-level IIFE** (C2 制約): module-level ESM import は許可するが、main 論理は IIFE 内に閉じる
- **`_installEventListenerRegistry` / `_installInnerHTMLSanitizer`** (L832 / L878): runtime safety net (memory leak / XSS 防止)

これらは「**最終的に温存する**」と意思決定済 (妥協ではなく、機械強制された安全契約に従った honest な記録)。

## How (usage)

`index.html` から `<script type="module" src="./main.js"></script>` で起動される唯一の ESM エントリ。

```
index.html
  └─ main.js  (module-level imports + IIFE)
       ├─ import { createXxx } from './js/<name>.js'  (× 24 葉モジュール)
       ├─ AIDK Isolated Kernel  (DO NOT EDIT)
       ├─ View Transition Proxy + Trusted Types Policy
       ├─ render / executeSafeTransition  (view-transition core)
       ├─ SITE_CONFIG  (Check 2/17 が grep する単一ソース)
       └─ 各 factory の合成呼び出し
            createAIDKRails / createComponents / createPages / ... × 11 factory
```

## Constraints

- **C1 Boring Technology**: フレームワーク禁止 (Vanilla JS only)
- **C2 IIFE**: main 論理は単一 top-level IIFE 内に閉じる
- **C3 ErrorBoundary**: View Transition API の error は graceful に処理
- **C5 Human Writes Zero Code**: 実装コードは AI 生成・人間は設計のみ
- **Check 2 / 17**: SITE_CONFIG.VERSION / SITE_CONFIG.LAST_UPDATED が `index.html` の ai:version / ai:last-modified と一致
- **Check 19**: sw.js CACHE_NAME と ai:version が一致
- **Check 43a-d**: AIDK Kernel header / startViewTransitionProxy / Trusted Types Policy / single IIFE 構造の存在を機械強制
- **Check 47**: js/ leaf module からの import/export bijection を機械強制 (24 modules)
- **Check 52**: 1,086 行 ≤ 6,400 (strong-advisory budget)
- **編集承認**: AIDK Kernel proper (L129-1000+) は **DO NOT EDIT 領域**。触る場合は orchestrator 明示承認必要

## Change impact

main.js 編集時に同時更新が必要なファイル:
- `SITE_CONFIG.VERSION` を変える → `index.html` の `ai:version` + `package.json` version + `sw.js` CACHE_NAME + `aio-manifest.json` 等の sha256 連鎖
- 葉モジュール import を追加 → `js/<name>.js` 新設 + `_modules47` (check_repository_consistency.py 内リスト) 拡張 + `index.html` modulepreload 追加 (Check 57)
- factory 合成呼び出し追加 → e2e/portfolio.spec.js の ALL_ROUTES (Check 58) + main.js renderer switch 追加
- AIDK Kernel 触る → Playwright visual baseline 更新が必要 (まずレビュー → snapshot 更新 PR → merge → 本 PR の二段階)

## Audience-specific notes

### For AI agents
- 役割タグ: `entry-point`, `kernel-host`, `factory-composer`, `aidk-protected`
- Import count: 24 leaf modules from `js/` and `js/quiz/`
- 不可侵領域: L129 以降の AIDK Kernel (Check 43 で structural integrity 機械強制)
- Stage 5 完遂時の最終形であり、これ以上の分割は意図的に行わない

### For human engineers (新卒レベル)
- 「触っていい場所」: factory の合成呼び出し部分 (大体 L1000 以降の init 部分)
- 「触ってはいけない場所」: AIDK Kernel (L129〜1000) — Comment header `DO NOT EDIT` で明示
- 機能追加したいときは、まず葉モジュール `js/<name>.js` を新設して factory pattern で書く → main.js でその factory を呼ぶ
- 「変えると何が壊れるか」を事前に知るには Check 番号で grep (例: SITE_CONFIG を変えるなら Check 2/17/19 がトリガー)

### For third parties (監査 / 採用 / 研究)
- Stage 5 物理分割 (7,785 → 1,086 行) の **proof-of-work**。設計判断は `docs/architecture/main-js-extraction-map.md` に記録
- AIDK Kernel を温存する判断は「妥協」ではなく「工学的限界を honest に認めた」記録 — 設計者 (横井雄太) の判断
- 24 葉モジュール抽出は `factory pattern` で statically analyzable な dependency injection を実現 (Check 47 で bijection 機械強制)
