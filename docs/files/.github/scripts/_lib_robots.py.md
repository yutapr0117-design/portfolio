---
file: .github/scripts/_lib_robots.py
audience: ai, human (新卒), 監査人, 第三者全般
last-updated: 2026-11-15
canonical-ref: .github/scripts/_lib_io.py (切り出し元・名前を export し直す) / robots.txt
---

# .github/scripts/_lib_robots.py

## What

robots.txt を RFC 9309 のグループの意味で読む helper を置く小さな module。

- `parse_robots_groups(src)` —— `[(user-agent のリスト, [(rule 名, 値), …]), …]` を返す。行のどこからでも `#` はコメントを始め、連続する `User-agent:` 行は 1 つのグループを成す。
- `robots_full_site_disallow(value)` —— `Disallow:` の値が全サイトを拒否するか（`/` / `/*` / `/*$` / `/portfolio/` / `*`）。

Check 161・342・444 が使う。

## Why

2026-11-15 に `_lib_io.py` が 456 行で advisory（450）を越えた。予算は上げず（CLAUDE.md §7 の教訓 (8)）、ひとまとまりで他の I/O helper に依らない robots.txt の parser を移した（`_lib_io.py` は 410 行）。

## How (usage)

```python
from _lib_io import parse_robots_groups, robots_full_site_disallow   # 従来どおり (_lib_io が export し直す)
from _lib_robots import parse_robots_groups                         # 直接でもよい
```

## Constraints

- 関数の振る舞いは移す前と同じ（Check 161 / 342 / 444 の OK 行が同じ）。

## Change impact

- robots.txt の読み方を変えるときはこの module を直す。`_lib_io.py` には export の 1 行だけが残る。

## Audience-specific notes

### For AI agents（次担当）

- 新しく robots.txt を読む Check も、この helper を使う（行単位の正規表現で読むと、行末コメントや名前付き bot のグループを見落とす）。

### For human engineers（新卒レベル）

検索エンジン向けの robots.txt を、仕様どおりのまとまりで読み取る関数の置き場。

### For third parties / auditors

検査の中身は移す前と同じで、置き場所だけが変わった。
