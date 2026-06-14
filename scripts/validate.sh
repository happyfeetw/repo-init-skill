#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"

run() {
  printf '\n==> %s\n' "$1"
  shift
  "$@"
}

run "Compile initializer" "$PYTHON" -m py_compile "$REPO_ROOT/repo-init/scripts/init_repo_quality.py"

tmp_zh=""
tmp_en=""
tmp_conflict=""
tmp_zh="$(mktemp -d /tmp/repo-init-zh.XXXXXX)"
trap 'rm -rf "${tmp_zh:-}" "${tmp_en:-}" "${tmp_conflict:-}"' EXIT
git -C "$tmp_zh" init >/dev/null
run "Chinese initialization" "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_zh" \
  --conversation-lang zh \
  --with-harness-skeleton
grep -q "仓库工作约定" "$tmp_zh/AGENTS.md"
"$tmp_zh/scripts/harness/check.sh" docs

tmp_en="$(mktemp -d /tmp/repo-init-en.XXXXXX)"
git -C "$tmp_en" init >/dev/null
run "English initialization" "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_en" \
  --conversation-lang en \
  --with-harness-skeleton
grep -q "Repository Working Agreements" "$tmp_en/AGENTS.md"
"$tmp_en/scripts/harness/check.sh" docs

tmp_conflict="$(mktemp -d /tmp/repo-init-conflict.XXXXXX)"
git -C "$tmp_conflict" init >/dev/null
printf '# Existing\n' > "$tmp_conflict/AGENTS.md"
run "Conflict scan" "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_conflict" \
  --conversation-lang zh \
  --scan
if "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_conflict" \
  --conversation-lang zh; then
  printf 'Expected default conflict failure, got success.\n' >&2
  exit 1
fi
run "Conflict proposal" "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_conflict" \
  --conversation-lang zh \
  --mode propose
test -f "$tmp_conflict/AGENTS.md.proposed"
grep -q "# Existing" "$tmp_conflict/AGENTS.md"
run "Explicit overwrite" "$PYTHON" "$REPO_ROOT/repo-init/scripts/init_repo_quality.py" \
  --repo "$tmp_conflict" \
  --conversation-lang en \
  --mode overwrite
grep -q "Repository Working Agreements" "$tmp_conflict/AGENTS.md"

printf '\nValidation passed.\n'
