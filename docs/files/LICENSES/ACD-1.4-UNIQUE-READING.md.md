---
file: LICENSES/ACD-1.4-UNIQUE-READING.md
audience: ai, human (新卒), 監査人, 法律家
last-updated: 2026-11-18
canonical-ref: .github/scripts/measure_legal_uncertainty.py / LICENSES/ACD-1.4-THIRD-CLARITY-TRIAL.md
---

# LICENSES/ACD-1.4-UNIQUE-READING.md

## What

1.4 草案の法的解釈を一意に定める記録。各条の「最も強い別の読み」を `- §x.y | 別の読み: … | 一意 / 試作 Tnn / 法の側 | 根拠: …` の形で、5 人の帯の小節（19.1〜19.5）に書く。

## Why

オーナーの依頼（2026-11-18）「ACD-1.4-DRAFT.txt の法的解釈が一意に定まるように『５人』で連携しながら続けて」。初めは THIRD の §19 に書いたが、5 人が同じ file の末尾に足して衝突が続き、THIRD が 839 行で上限 1,000 に近づいたので、同じ日にこの file へ移した（本文は無改変・見出しの番号はそのまま）。

## How

各帯の人は自分の小節の中に行を足す。`measure_legal_uncertainty.py` の section19() が行を数え（一意 / 試作 / 法の側）、合格の線（開いている試作 0、一意の行がすべて閉じている条を名指す）を出す。開いている試作は `list_open_items.py` にも出る。

## Constraints

末尾に足さない（衝突の元）。行の形を変えるときは section19() の ROW19 と同じ PR で。

## Change impact

草案の版が上がれば `ACD-N.M-UNIQUE-READING.md` を作る（道具は glob で最新の版を読む）。

## Audience-specific notes

- **法律家**: 「法の側」の行は、本文の語では一意にならず法が決める所で、`QUESTIONS-FOR-COUNSEL.md` の問いか THIRD §18 の行を名指す。
