---
file: .github/scripts/update_binary_aio_rights.py
audience: ai, human (新卒), 監査人, 採用担当, 学術研究者, 第三者全般
last-updated: 2026-08-23
canonical-ref: .github/scripts/update_binary_aio_organization.py / .github/scripts/_lib_io.py / LICENSES/ACD-1.0.txt / AI2AI.md
---

# .github/scripts/update_binary_aio_rights.py

## What

one-shot tool。binary AIO 層（WebP XMP / MP3 ID3v2.4）に対して 3 つの編集を行う:

1. **WebP `dc:rights`** の権利表示を ACD-1.0 へ（RIFF chunk を再計算して置換）
2. **MP3 `TCOP`** の権利表示を ACD-1.0 へ（**同一バイト長 52 bytes の in-place 置換**）
3. **🔴 MP3 の malformed frame の修復**（size 欄 4 bytes の in-place 是正）

実行後は `update_aio_digests.py` で digest を再生成する（tool の出力が案内する）。

## Why

**(1)(2) 権利表示の面ごとの食い違い**: 2026-08-23 に LICENSE を ACD-1.0（権利留保ゼロ）へ
移行したが、binary 内の権利表示は `All rights reserved` のままだった。XMP / ID3 を読む機械は
**公開層から矛盾した権利情報を受け取る**。C6 が守るのは「面ごとに食い違わせない」ことなので
是正対象。

**(3) が本 tool の最も重い部分**: `COMM` frame（offset 6540）の size 欄が実データより
**3 バイト大きく**（宣言 2396 / 実体 2393）、ID3v2.4 の frame は連結されているため
**以降の walk が破綻していた**。実測: 厳密な reader は offset 8946 で不正な frame id
`b'X\x00\x00\x00'` を読んで停止し、**それ以降の 5 frame が一切読めなかった**:

    TXXX:AIO:Organization
    TXXX:AIO:OrganizationURL
    TXXX:AIO:OrganizationRole
    TXXX:AIO:OrganizationStartDate
    TXXX:AIO:MetadataLastModified   ← Check 91 が存在と同期を BLOCKING 強制している当の field

つまり **PR #49 の「Organization 情報を cross-surface に反映」は MP3 面では一度も標準リーダーに
届いていなかった**。さらに Check 91 は「必ず存在せよ」と機械強制しているのに、その field は
誰にも読めない位置にあった —— #929（WebMCP の幻セレクタ）/ #930（route 追従 JSON-LD）と同じ
**「宣言はあるが実態が伴わない」class の binary 面**。修復で **読める frame が 33 → 38** になった。

## How (usage)

```
python3 .github/scripts/update_binary_aio_rights.py
python3 .github/scripts/update_aio_digests.py
```

冪等。既に適用済みなら各ステップが skip する。

## Constraints

- **frame を parse して tag を組み直してはならない。** この file には malformed frame があり、
  組み直すとデータを落とすか、さらに破損させる。本 tool の MP3 側 2 編集はいずれも
  **byte 長を変えない in-place 編集**で、file size もすべての frame の offset も変わらない。
- **TCOP の新文言は必ず 52 bytes**。長さが変わる場合、tool は書き込まずに中断する。
- 日付フィールドは C6 の A1 派生値例外に従い `_lib_io` の helper で同期する（Check 91）。

## Change impact

- **malformed frame を「種別」で探してはならない。** この file には `COMM` が 5 個あり、
  malformed なのは最後の 1 つだけ。初版は `data.find(b"COMM")` で先頭の COMM を掴み、
  **修復を行わずに「既に一致」と報告した**（成功したふりをした）。現行版は **walk が実際に
  破綻する位置**から犯人を特定し、修復後に「読める frame が増えたこと」を検証してから書き込む。
- 権利表示の文言を変えるときは、WebP 側は自由に長さを変えられるが、**MP3 側は 52 bytes 固定**。

## Audience-specific notes

### For AI agents
- 役割タグ: `one-shot-tool`, `binary-metadata`, `id3v2.4`, `webp-xmp`, `c6-derived-values`
- 教訓: **「書き込んだ」と「読める」は別**。binary metadata は書き込みが成功しても、
  前方の frame が壊れていれば読み手には存在しないのと同じ。

### For human engineers (新卒レベル)
- ID3v2.4 の frame size は **synchsafe（7 bit/byte）**。普通の 32bit 整数と読み違えると
  全く違う値になる。そして frame は連結されているので、**1 つでもサイズが狂うと以降が全滅する**。

### For third parties
- 公開バイナリのメタデータが「宣言と実態」で乖離していた実例と、その検出・修復の記録。
