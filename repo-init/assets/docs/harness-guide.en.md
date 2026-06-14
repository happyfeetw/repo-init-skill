# Harness Guide

Document nature: Persistent engineering standard. This document describes the repository harness entrypoint, layers, reports, and extension rules.

## Revision History

| Date | Change |
| --- | --- |
| YYYY-MM-DD | Established harness guide. |

## Entrypoint

The repository should expose one entrypoint:

```bash
scripts/harness/check.sh <gate> [args]
```

Suggested gates:

| Gate | Purpose |
| --- | --- |
| `quick` | Default local PR gate using low-environment checks |
| `changed` | Select checks from changed files |
| `docs` | Docs index, links, naming, revision history, repo hygiene, whitespace |
| `backend` | Backend compile, tests, or quality gate |
| `frontend` | Frontend type-check, build, or tests |
| `mobile` | Mobile static audit, build, or smoke |
| `contract` | API, schema, client path, public enum contract checks |
| `runtime` | Running-service health, metrics, sanitized logs, optional smoke |
| `e2e` | End-to-end business workflow |
| `release` | Full pre-release evidence package |
| `harness-tests` | Self-tests for harness scripts and report contracts |

## Layering Rules

- `quick` does not depend on real secrets, production services, uncontrolled external accounts, or manual tools.
- Runtime/E2E/release checks stay explicit.
- Every gate must be independently runnable.
- CI and local development call the same harness entrypoint.
- Changes to harness selection or report format must run `harness-tests`.

## Report Contract

Important gates should support:

```bash
HARNESS_REPORT_DIR=release-artifacts/harness/<gate> scripts/harness/check.sh <gate>
```

Reports should include:

- `summary.json`
- `summary.md`
- `steps.jsonl`
- `logs/`

Step statuses:

- `PASS`
- `FAIL`
- `SKIPPED`
- `PLANNED`

Skipped steps must include reason and enabling condition. Reports and logs must be sanitized.

## Minimal Skeleton

If the repository has no harness yet, implement:

1. `docs`: docs and repo hygiene checks.
2. `quick`: docs plus core module static checks.
3. `changed`: changed-file-based gate selection.
4. `harness-tests`: self-test selection logic and report shape.
5. `runtime` / `release`: add after a runtime environment exists.
