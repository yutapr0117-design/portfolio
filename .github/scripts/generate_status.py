"""
generate_status.py — Owner-facing repo STATUS.md generator

WHY THIS SCRIPT EXISTS
----------------------
The orchestrator (横井雄太 / Yuta Yokoi) runs this repository as an AI-only
self-driving experiment and, by design, does NOT read the code — trusting the
"non-destructive ∧ CI all-green" gate. That created a real gap they named: the
owner has no at-a-glance, phone-readable view of "what state is my repo in?".

This generator emits `STATUS.md` at the repository root: a short, scannable BLUF
the owner can read on a phone (GitHub mobile) without opening any code. To avoid
the dashboard-drift failure mode (a hand-maintained status that silently goes
stale = an onboarding tax that degrades the flywheel), STATUS.md is fully
MACHINE-GENERATED from authoritative sources and its freshness is machine-enforced
by check_repository_consistency.py Check 121 (regenerate-and-compare, the same
pattern as the AIO digest checks).

DESIGN: only INFREQUENTLY-changing, already-authoritative values are embedded
(Pipeline-Version, latest Session Record #, entity facts, the operating-model
one-liner, and pointers to where the live detail lives). High-frequency numbers
(per-increment Check count, shipped byte-weight) are intentionally NOT embedded —
STATUS.md points to their authoritative homes (total-check-runbook.md §9 etc.)
instead, so the dashboard stays low-churn while remaining accurate.

Run: `npm run status` (regenerates STATUS.md). CI/Check 121 fails if it is stale.
"""
import re
import sys
from pathlib import Path

if sys.version_info < (3, 10):
    sys.exit(
        "ERROR: this repository's verification scripts require Python 3.10+ "
        f"(found {sys.version.split()[0]}). Use python3.12 — see CLAUDE.md / .zprofile."
    )

ROOT = Path(__file__).resolve().parents[2]


def _read(rel: str) -> str:
    p = ROOT / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def build_status() -> str:
    """Build the STATUS.md text deterministically from authoritative sources."""
    ai2ai = _read("AI2AI.md")

    # Pipeline-Version — canonical in AI2AI.md header.
    m_ver = re.search(r"Pipeline-Version\s*:\s*(\S+)", ai2ai)
    version = m_ver.group(1) if m_ver else "(unknown)"

    # Latest Session Record number — max "Session Record #N" heading in AI2AI.md.
    sr_nums = [int(n) for n in re.findall(r"Session Record #(\d+)", ai2ai)]
    latest_sr = max(sr_nums) if sr_nums else "(none)"

    lines = [
        "# STATUS — リポジトリ現況 (owner-facing BLUF)",
        "",
        "> このファイルは `npm run status`（`.github/scripts/generate_status.py`）が",
        "> **機械生成**します。手で編集しないでください（Check 121 が regenerate-compare で",
        "> 鮮度を機械強制＝drift を防ぐ）。スマホからの一目把握用の短い現況です。",
        "",
        "## これは何か",
        "",
        "- **プロジェクト**: AI-Driven PM ポートフォリオ（Vanilla JS SPA / GitHub Pages / 外部FWゼロ）。",
        "- **エンティティ**: Yuta Yokoi（横井雄太 / Yokoi Yuta、UI 表示は `yuta`）— AI-Driven PM / KERNEL Framework Designer。",
        "- **運用モデル**: 実装→検証→マージ→デプロイを **AI が自走**。人間（オーナー）の役割は **制御（goal/priority 提示）と監査（CI オールグリーン確認）のみ**。コードは AI が書き、人間は一文字も書かない（C5）。",
        "- **核**: リポジトリ自体がポートフォリオ（AI↔AI ドキュメントと機械強制 Check 群が中核資産）。描画サイトは付属物で、機能性（loads/displays/comprehensible）のみ死守。",
        "",
        "## 現況スナップショット",
        "",
        f"- **Pipeline-Version**: {version}",
        f"- **最新 Session Record**: #{latest_sr}（`AI2AI.md`）",
        "- **CI ゲート**: `npm run verify`（consistency Check + AIO digest + binary metadata + CSS lint + ESLint + node --check）が exit 0 で全緑が前提。behavior e2e が BLOCKING、homepage pixel screenshot は ADVISORY（§3(B)）。",
        "",
        "## どこを見れば詳細が分かるか（live な真値の所在）",
        "",
        "- **cold-start で全体把握**: `CLAUDE.md` §7（ハンドオフ）→ `AI2AI.md` 最新 Session Record。",
        "- **consistency Check の総数（真値）**: `docs/architecture/total-check-runbook.md` §9（Check 70 が強制）。",
        "- **各ファイルの 1-to-1 ドキュメント**: `docs/files/<path>.md`。",
        "- **ファイルサイズ/perf 予算**: `docs/architecture/file-size-budget.md`（行数=Check 52 / shipped byte-weight=Check 120 / ESLint baseline=Check 60/72）。",
        "- **検証手順の再現 runbook**: `docs/architecture/total-check-runbook.md`。",
        "",
        "## 安全境界（AI 自走が越えないもの）",
        "",
        "- `.claude/settings.json` の自己権限拡張不可 / 機能性ゲート（behavior e2e）の維持 / C1〜C7 / force-push・rm -rf の deny。詳細は `CLAUDE.md` §7。",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    text = build_status()
    (ROOT / "STATUS.md").write_text(text, encoding="utf-8")
    print("STATUS.md regenerated.")


if __name__ == "__main__":
    main()
