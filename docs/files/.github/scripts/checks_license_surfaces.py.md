---
file: .github/scripts/checks_license_surfaces.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-10-26
canonical-ref: .github/scripts/check_repository_consistency.py (CHECK_SOURCE_FILES と run 呼び出し) / LICENSE (適用宣言の単一ソース) / LICENSES/FROZEN.md
---

# .github/scripts/checks_license_surfaces.py

## What

ライセンスの機械可読面と凍結を守る Check 群: **444**（ライセンス宣言の cross-surface coherence）/ **445**（SPDX 提出用 XML の同期）/ **451**（機械可読記述子と条文）/ **452**（提出準備マーカー）/ **453**（凍結中の提出物の sha256）。

## Why

2026-10-26 に `checks_aio_config.py` から切り出した。980 行で advisory (950) を超え、1,000 行の BLOCKING (Check 365) まで 20 行だった。OSI の作業で最も触る検査なので、止まる前に分けた。

## How

`run(ctx)` が共有の `check()` / `ROOT` などを参照で受け取る（check.py 分割の型・exec 不使用）。各 Check は自前で対象 file を読み、`checks_aio_config.py` の 62-69 と変数を共有しない。

## Constraints

- 適用する版は `LICENSE` の 2 行（SPDX 識別子と `Full text:`）から導出する。版の決め打ちを足さない。
- 445 の XML は凍結された 1.0 の提出物なので、識別子は出典の本文から導出する。

## Change impact

`CHECK_SOURCE_FILES` に登録済みで、Check 45 / 70 / 105 が番号を横断して集約する。

## Audience-specific notes

- **AI（次のセッション）**: 新しい版を確定・適用するとき、ここの Check が版の決め打ちで赤くならないかを最初に見る。
