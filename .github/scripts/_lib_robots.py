"""_lib_robots.py — robots.txt を RFC 9309 のグループの意味で読む helper (Check 161 / 342 / 444 が使う)。

2026-11-15 に _lib_io.py (advisory 450) から移した (456 行で越えたため・予算は上げない)。robots.txt の parser は
ひとまとまりで、他の I/O helper に依らない。読み手は `from _lib_io import parse_robots_groups` のまま動く
(_lib_io が名前を export し直す)。
"""
from __future__ import annotations

import re

# [2026-11-08] サイトは /portfolio/ の下に在るので、その接頭辞の拒否も全サイトの拒否である (Allow: / より
#   長い一致が勝つ)。`*` の 1 文字も全てに一致する。旧版は / と /* と /*$ だけを見ていた (監査で実測)。
_ROBOTS_FULL_SITE = re.compile(r"^(\*|/(portfolio/?)?(\*\$?)?)$")


def parse_robots_groups(src: str) -> list[tuple[list[str], list[tuple[str, str]]]]:
    """robots.txt を RFC 9309 のグループの意味で読む。

    返り値は ``[(user-agent のリスト (小文字), [(rule 名 (小文字), 値), ...]), ...]``。

    - ``#`` は**行のどこからでも**コメントを始める (``Disallow: / # tmp`` の値は ``/``)。
    - 連続する ``User-agent:`` 行は 1 つのグループを成す。rule の後に来た
      ``User-agent:`` が次のグループを始める。空行とコメント行はグループを終えない。
    - 最初の ``User-agent:`` より前の rule は agent 空のグループに入れて返す
      (RFC は無視せよと言うが、検査側が見落とさないように残す)。

    2026-11-02 まで Check 161 / 342 は行単位の正規表現で読んでおり、行末コメント付きの
    ``Disallow: /`` と ``Disallow: /*`` と、名前付き bot のグループの全サイト拒否を
    3 つとも素通りしていた。
    """
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    agents: list[str] = []
    rules: list[tuple[str, str]] = []
    seen_rule = False
    for raw in src.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key, value = key.strip().lower(), value.strip()
        if key == "user-agent":
            if seen_rule:
                groups.append((agents, rules))
                agents, rules, seen_rule = [], [], False
            agents.append(value.lower())
        elif key in ("allow", "disallow"):
            rules.append((key, value))
            seen_rule = True
        else:
            seen_rule = seen_rule or bool(agents)
    if agents or rules:
        groups.append((agents, rules))
    return groups


def robots_full_site_disallow(value: str) -> bool:
    """``Disallow:`` の値が全サイトを拒否するか (``/`` / ``/*`` / ``/*$``)。"""
    return bool(_ROBOTS_FULL_SITE.match(value.strip()))
