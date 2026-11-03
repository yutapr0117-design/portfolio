"""probe_scope.py — mutation-probe が consistency gate を「名指した Check の module だけ」で走らせるための import hook。

**なぜ在るか (2026-11-04)**: probe は mutation 1 件ごとに gate 全体 (約 60 module) を走らせていた。
実 CI で 1 件 10.3 秒・shard あたり 25.7 分となり、timeout 30 分に対する余裕が 1.17 倍まで縮んだ。
mutation-probe.yml のコメントは 2026-09-29 に「余裕が 1.5 倍を切ったら、分割ではなく gate 全体を
走らせる構造を見直す」と記録していた (1 件あたりの所要は Check が増えるたびに伸び、分割では止まらない)。
2026-09-29 からの帰属は「名指した Check が発火したか」で決まるので、まず名指した Check の module
だけで走らせ、発火しなかったときだけ gate 全体で走らせ直す (mutation_probe.py)。判定は従来と同じになる。

**働き**: 環境変数 `CHECK_ONLY_MODULE` があるときだけ、それ以外の `checks_*` module の `run` を
何もしない関数へ差し替える。module 自体は import されるので、他 module が使う helper は残る。
値が `__monolith__` なら、すべての module の `run` を空にする (名指した Check が monolith 内にある場合)。
**環境変数が無ければ何もしない** —— 通常の verify / CI の挙動は不変。
"""
import importlib.abc
import importlib.machinery
import os
import sys

_ONLY = os.environ.get("CHECK_ONLY_MODULE")


class _ScopedFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path, target=None):
        if not name.startswith("checks_") or name == _ONLY:
            return None
        spec = importlib.machinery.PathFinder.find_spec(name, path)
        if spec is None or spec.loader is None:
            return spec
        _orig = spec.loader

        class _Loader(importlib.abc.Loader):
            def create_module(self, s):
                return _orig.create_module(s)

            def exec_module(self, module):
                _orig.exec_module(module)
                module.run = lambda ctx: None

        spec.loader = _Loader()
        return spec


if _ONLY:
    sys.meta_path.insert(0, _ScopedFinder())
