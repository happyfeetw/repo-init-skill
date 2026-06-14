#!/usr/bin/env python3
"""Initialize repository AGENTS.md and quality workflow docs from repo-init assets."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
ASSETS_DIR = SKILL_DIR / "assets"

TEMPLATE_MAP = {
    "en": [
        ("AGENTS.en.md", "AGENTS.md"),
        ("docs/agent-quality-workflow.en.md", "docs/engineering/agent-quality-workflow.md"),
        ("docs/agent-exec-plan.en.md", "docs/engineering/agent-exec-plan.md"),
        ("docs/harness-guide.en.md", "docs/engineering/harness-guide.md"),
    ],
    "zh": [
        ("AGENTS.zh.md", "AGENTS.md"),
        ("docs/agent-quality-workflow.zh.md", "docs/engineering/agent-quality-workflow.md"),
        ("docs/agent-exec-plan.zh.md", "docs/engineering/agent-exec-plan.md"),
        ("docs/harness-guide.zh.md", "docs/engineering/harness-guide.md"),
    ],
}

RELATED_KEYWORDS = (
    "agent",
    "agents",
    "harness",
    "quality",
    "workflow",
    "exec-plan",
    "执行计划",
    "质量",
    "工作流",
)

HARNESS_SKELETON = """#!/usr/bin/env bash
set -euo pipefail

COMMAND="${1:-quick}"
if [ "$#" -gt 0 ]; then
  shift
fi

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

log() {
  printf '%s\\n' "$*"
}

run_step() {
  local name="$1"
  shift
  log ""
  log "==> ${name}"
  "$@"
  log "PASS: ${name}"
}

run_docs() {
  run_step "Git whitespace checks" bash -c "cd '${REPO_ROOT}' && git diff --check && git diff --cached --check"
  if [ -f "${REPO_ROOT}/docs/engineering/agent-quality-workflow.md" ]; then
    run_step "Required quality docs exist" bash -c "
      test -f '${REPO_ROOT}/AGENTS.md'
      test -f '${REPO_ROOT}/docs/engineering/agent-quality-workflow.md'
      test -f '${REPO_ROOT}/docs/engineering/agent-exec-plan.md'
      test -f '${REPO_ROOT}/docs/engineering/harness-guide.md'
    "
  fi
}

run_quick() {
  run_docs
  log ""
  log "Customize: add project-specific backend/frontend/mobile/contract checks here."
}

run_changed() {
  run_docs
  log ""
  log "Customize: add changed-file-based gate selection here."
}

case "${COMMAND}" in
  docs) run_docs ;;
  quick) run_quick ;;
  changed) run_changed ;;
  harness-tests) run_docs ;;
  help|-h|--help)
    cat <<'USAGE'
Usage: scripts/harness/check.sh [quick|changed|docs|harness-tests]

This is a minimal skeleton. Customize it for this repository's modules.
USAGE
    ;;
  *)
    log "Unknown harness command: ${COMMAND}" >&2
    exit 2
    ;;
esac
"""


def proposed_path(path: Path) -> Path:
    candidate = path.with_name(path.name + ".proposed")
    index = 2
    while candidate.exists():
        candidate = path.with_name(f"{path.name}.proposed.{index}")
        index += 1
    return candidate


def detect_cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    letters = sum(1 for char in text if char.isalpha() or "\u4e00" <= char <= "\u9fff")
    return cjk / max(letters, 1)


def detect_language(repo: Path, *, lang: str, conversation_lang: str) -> str:
    if lang != "auto":
        return lang
    if conversation_lang != "auto":
        return conversation_lang

    agents = repo / "AGENTS.md"
    if agents.exists():
        try:
            text = agents.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            text = ""
        if detect_cjk_ratio(text) >= 0.2:
            return "zh"
        if text.strip():
            return "en"

    locale = " ".join(filter(None, [os.environ.get("LC_ALL"), os.environ.get("LANG")])).lower()
    if locale.startswith("zh") or ".zh" in locale or "chinese" in locale:
        return "zh"
    return "en"


def target_paths(lang: str, *, with_harness_skeleton: bool) -> list[Path]:
    paths = [Path(dst_rel) for _, dst_rel in TEMPLATE_MAP[lang]]
    if with_harness_skeleton:
        paths.append(Path("scripts/harness/check.sh"))
    return paths


def scan_existing(repo: Path, lang: str, *, with_harness_skeleton: bool) -> tuple[list[Path], list[Path]]:
    exact = [path for path in target_paths(lang, with_harness_skeleton=with_harness_skeleton) if (repo / path).exists()]
    related: set[Path] = set()

    root_agents = repo / "AGENTS.md"
    if root_agents.exists():
        related.add(Path("AGENTS.md"))

    engineering = repo / "docs/engineering"
    if engineering.exists():
        for path in engineering.iterdir():
            if not path.is_file():
                continue
            lowered = path.name.lower()
            if any(keyword.lower() in lowered for keyword in RELATED_KEYWORDS):
                related.add(path.relative_to(repo))

    harness = repo / "scripts/harness"
    if harness.exists():
        related.add(Path("scripts/harness"))

    return sorted(exact), sorted(related)


def print_scan(repo: Path, lang: str, exact: list[Path], related: list[Path]) -> None:
    print(f"Target repo: {repo}")
    print(f"Selected language: {lang}")
    if exact:
        print("Existing target files:")
        for path in exact:
            print(f"- {path}")
    else:
        print("Existing target files: none")
    if related:
        print("Related existing files/directories:")
        for path in related:
            print(f"- {path}")
    else:
        print("Related existing files/directories: none")


def copy_template(src_rel: str, dst_rel: str, repo: Path, *, mode: str) -> tuple[Path, str]:
    src = ASSETS_DIR / src_rel
    dst = repo / dst_rel
    status = "created"
    if dst.exists() and mode == "fail":
        raise FileExistsError(dst)
    if dst.exists() and mode == "propose":
        dst = proposed_path(dst)
        status = "proposed"
    elif dst.exists() and mode == "overwrite":
        status = "overwritten"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dst)
    return dst, status


def write_harness(repo: Path, *, mode: str) -> tuple[Path, str]:
    dst = repo / "scripts/harness/check.sh"
    status = "created"
    if dst.exists() and mode == "fail":
        raise FileExistsError(dst)
    if dst.exists() and mode == "propose":
        dst = proposed_path(dst)
        status = "proposed"
    elif dst.exists() and mode == "overwrite":
        status = "overwritten"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(HARNESS_SKELETON, encoding="utf-8")
    mode = dst.stat().st_mode
    dst.chmod(mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return dst, status


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize AGENTS.md and quality workflow docs.")
    parser.add_argument("--repo", default=".", type=Path, help="Target repository root. Defaults to cwd.")
    parser.add_argument("--lang", choices=["auto", *sorted(TEMPLATE_MAP)], default="auto", help="Template language.")
    parser.add_argument(
        "--conversation-lang",
        choices=["auto", *sorted(TEMPLATE_MAP)],
        default="auto",
        help="Language inferred by the agent from the user conversation. Used when --lang=auto.",
    )
    parser.add_argument(
        "--mode",
        choices=["fail", "propose", "overwrite"],
        default="fail",
        help="Conflict handling. fail stops on existing targets; propose writes *.proposed; overwrite replaces files.",
    )
    parser.add_argument("--force", action="store_true", help="Alias for --mode overwrite.")
    parser.add_argument("--scan", action="store_true", help="Only scan existing target and related files.")
    parser.add_argument(
        "--with-harness-skeleton",
        action="store_true",
        help="Create a minimal scripts/harness/check.sh skeleton if desired.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    if not repo.exists() or not repo.is_dir():
        raise SystemExit(f"Target repo does not exist or is not a directory: {repo}")

    lang = detect_language(repo, lang=args.lang, conversation_lang=args.conversation_lang)
    mode = "overwrite" if args.force else args.mode
    exact, related = scan_existing(repo, lang, with_harness_skeleton=args.with_harness_skeleton)

    if args.scan:
        print_scan(repo, lang, exact, related)
        return 0

    if exact and mode == "fail":
        print_scan(repo, lang, exact, related)
        raise SystemExit(
            "Existing target files found. Ask the user whether to overwrite or merge. "
            "Use --mode overwrite only after explicit overwrite approval, or --mode propose for merge review."
        )

    results: list[tuple[Path, str]] = []
    for src_rel, dst_rel in TEMPLATE_MAP[lang]:
        results.append(copy_template(src_rel, dst_rel, repo, mode=mode))

    if args.with_harness_skeleton:
        results.append(write_harness(repo, mode=mode))

    print(f"Initialized quality workflow files in: {repo}")
    print(f"Selected language: {lang}")
    print(f"Conflict mode: {mode}")
    for path, status in results:
        print(f"- {status}: {path.relative_to(repo)}")
    if any(status == "proposed" for _, status in results):
        print("Existing files were preserved. Review *.proposed files and merge manually.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
