"""
update_aio_digests.py — AIO digest / manifest 自動更新スクリプト

GitHub Actions から呼び出され、以下のファイルを現在のSHA-256で同期する:
  - .well-known/index.json          (digest フィールド)
  - .well-known/agent-skills/index.json  (index.json と byte-identical に保つ)
  - .well-known/aio-manifest.json   (sha256 フィールド + generated_at)
                                    対象: source_of_truth と supporting_evidence の両セクション

対象ファイルのSHAが変わっていなければファイルを書き換えない。
変更があった場合のみ上書きし、変更ファイル名を stdout に出力する。

Idempotency guarantee:
  generated_at is updated ONLY when at least one sha256 digest changes
  (across source_of_truth, supporting_evidence, and observational_evidence sections).
  If all digests are already current, aio-manifest.json is
  left untouched (write_if_changed ensures byte-level idempotency).

Exit codes:
  0 — 処理完了 (変更なしを含む)
  1 — エラー
"""

from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]

# digest 対象: URL → ローカルファイル
URL_TO_LOCAL: dict[str, Path] = {
    "https://yutapr0117-design.github.io/portfolio/llms-full.txt": ROOT / "llms-full.txt",
    "https://yutapr0117-design.github.io/portfolio/AI2AI.md":       ROOT / "AI2AI.md",
}

# aio-manifest 対象: path → ローカルファイル (source_of_truth + supporting_evidence)
MANIFEST_PATH_TO_LOCAL: dict[str, Path] = {
    "llms.txt":       ROOT / "llms.txt",
    "llms-full.txt":  ROOT / "llms-full.txt",
    "AI2AI.md":       ROOT / "AI2AI.md",
    "yuta-yokoi-ai-pm-orchestration-system.webp":          ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp",
    "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3": ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",
    # supporting_evidence
    "Claude2Claude.md":                          ROOT / "Claude2Claude.md",
    "ChatGPT2ChatGPT.md":                        ROOT / "ChatGPT2ChatGPT.md",
    "docs/evidence/ai-pioneer-identity-review.md": ROOT / "docs" / "evidence" / "ai-pioneer-identity-review.md",
    "docs/session-records/AI2AI-archive.md": ROOT / "docs" / "session-records" / "AI2AI-archive.md",
    # observational_evidence
    "docs/evidence/aio-monitoring-log.json":     ROOT / "docs" / "evidence" / "aio-monitoring-log.json",
}

INDEX_FILES = [
    ROOT / ".well-known" / "index.json",
    ROOT / ".well-known" / "agent-skills" / "index.json",
]
MANIFEST_FILE = ROOT / ".well-known" / "aio-manifest.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_if_changed(path: Path, new_bytes: bytes) -> bool:
    """ファイルが変化していれば書き込み、変化を bool で返す。"""
    if path.exists() and path.read_bytes() == new_bytes:
        return False
    path.write_bytes(new_bytes)
    return True


def update_index_files() -> list[str]:
    """index.json のdigestを更新し、変更ファイルのパスリストを返す。"""
    changed: list[str] = []
    src = INDEX_FILES[0]
    if not src.exists():
        print(f"ERROR: {src} not found")
        sys.exit(1)

    data = json.loads(src.read_text(encoding="utf-8"))
    for skill in data.get("skills", []):
        url = skill.get("url", "")
        local = URL_TO_LOCAL.get(url)
        if not local or not local.exists():
            print(f"WARNING: no local file for {url} — skipping")
            continue
        skill["digest"] = "sha-256:" + sha256_file(local)

    new_bytes = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    for f in INDEX_FILES:
        if write_if_changed(f, new_bytes):
            changed.append(str(f.relative_to(ROOT)))

    return changed


def update_manifest_section(data: dict, section_key: str) -> bool:
    """Update sha256 fields in a manifest section. Returns True if any digest changed."""
    changed_any = False
    for entry in data.get(section_key, []):
        path_key = entry.get("path", "")
        local = MANIFEST_PATH_TO_LOCAL.get(path_key)
        if not local or not local.exists():
            print(f"WARNING: no local file for manifest [{section_key}] path '{path_key}' — skipping")
            continue
        expected = sha256_file(local)
        if entry.get("sha256") != expected:
            entry["sha256"] = expected
            changed_any = True
    return changed_any


def update_manifest() -> list[str]:
    """aio-manifest.json の sha256 を更新する (source_of_truth + supporting_evidence)。

    Idempotency: generated_at は、少なくとも1つの sha256 が変わった場合のみ更新する。
    全 sha256 が既に現物と一致している場合、aio-manifest.json を書き換えない。
    """
    if not MANIFEST_FILE.exists():
        print(f"ERROR: {MANIFEST_FILE} not found")
        sys.exit(1)

    data = json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))

    changed_any_digest = False
    for section in ("source_of_truth", "supporting_evidence", "observational_evidence"):
        if update_manifest_section(data, section):
            changed_any_digest = True

    if changed_any_digest:
        # Only update generated_at when digests actually change
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        data["generated_at"] = now_iso
        # 8 案: top-level last_metadata_update を真値として記録
        # (C6 derived-value 例外条項 A 案 に基づく自動更新フィールド)
        data["last_metadata_update"] = now_iso
        # B1 案: binary が変わったら xmp:ModifyDate / xmp:MetadataDate / MP3 TXXX
        # AIO:MetadataLastModified も同期更新する (binary 編集の sha256 が変わったら
        # その binary 内日付メタも同期させる)
        binary_paths = {"yuta-yokoi-ai-pm-orchestration-system.webp", "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"}
        binary_changed = False
        for section in ("source_of_truth",):
            for entry in data.get(section, []):
                if entry.get("path") in binary_paths:
                    # この entry は今回 digest 更新で sha が書き換わった可能性がある
                    binary_changed = True
                    break
        if binary_changed:
            try:
                from _lib_io import update_webp_xmp_dates, update_mp3_metadata_date
                webp = ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp"
                mp3 = ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3"
                if webp.exists():
                    if update_webp_xmp_dates(webp, now_iso):
                        print(f"  WebP XMP dates synced to {now_iso}")
                        # digest を再計算 (binary が変わったので)
                        for entry in data["source_of_truth"]:
                            if entry.get("path") == "yuta-yokoi-ai-pm-orchestration-system.webp":
                                entry["sha256"] = sha256_file(webp)
                if mp3.exists():
                    if update_mp3_metadata_date(mp3, now_iso):
                        print(f"  MP3 ID3 metadata date synced to {now_iso}")
                        for entry in data["source_of_truth"]:
                            if entry.get("path") == "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3":
                                entry["sha256"] = sha256_file(mp3)
            except ImportError:
                print("WARNING: _lib_io not importable — binary date sync skipped")
    # else: do not rewrite aio-manifest.json only to refresh generated_at

    data.setdefault("manifest_version", "1.0")

    new_bytes = (json.dumps(data, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    if write_if_changed(MANIFEST_FILE, new_bytes):
        return [str(MANIFEST_FILE.relative_to(ROOT))]
    return []


def main() -> int:
    errors: list[str] = []

    # 入力ファイル存在確認 (optional supporting_evidence files skipped if missing)
    required = list(URL_TO_LOCAL.values()) + [
        ROOT / "llms.txt", ROOT / "llms-full.txt", ROOT / "AI2AI.md",
        ROOT / "yuta-yokoi-ai-pm-orchestration-system.webp",
        ROOT / "yuta-yokoi-sakura-swing-ai-generated-portfolio-bgm.mp3",
    ]
    for local in required:
        if not local.exists():
            errors.append(f"Missing source file: {local.relative_to(ROOT)}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    changed: list[str] = []
    changed.extend(update_index_files())
    changed.extend(update_manifest())

    if changed:
        print("Updated files:")
        for f in changed:
            print(f"  {f}")
    else:
        print("All digests are already up to date — no changes made.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
