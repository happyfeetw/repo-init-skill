# Repository Working Agreements

These instructions define the default quality workflow for this repository. They apply to AI agents, automation scripts, and human collaborators unless a more specific module-level instruction overrides them.

## Communication

- Keep explanations concise and task-focused.
- For implementation work, report the decision, plan, changed files, validation, and residual risk.
- When a request is ambiguous, make the safest reasonable assumption and state it. Ask only when the answer materially affects correctness, safety, data, or release risk.
- Do not present guesses as verified facts.

## Source Priority

Current repository state is the source of truth. When code, docs, issues, historical notes, or memory conflict, use this order:

1. Current code, configuration, scripts, migrations, CI configuration, and live command output.
2. Current docs, engineering notes, runbooks, module reports, and contract snapshots.
3. Current issues, pull requests, release records, and deployment records.
4. Maintained project memory, context indexes, or knowledge-base files.
5. Archived docs, old plans, old chat context, and unverified oral assumptions.

If lower-priority context conflicts with current files or command output, verify before acting and update stale sources when they are part of the deliverable.

## Core Quality Rules

- Keep changes minimal, reversible, and scoped to the request.
- Protect user or teammate changes. Do not revert unrelated work unless explicitly asked.
- Do not add production dependencies, public API changes, migrations, permissions, or release behavior changes without clear need and validation.
- Never commit secrets, real credentials, private keys, customer data, production passwords, or sensitive personal data.
- Convert repeated review rules into executable checks whenever practical.
- Every important acceptance criterion should be provable through commands, logs, reports, screenshots, API responses, CI results, or diff evidence.

## Risk Routing

Classify non-trivial tasks before editing:

| Tier | Typical work | Required path |
| --- | --- | --- |
| Low | Docs, copy, small styles, fixtures, local no-behavior changes | Direct edit, minimal validation |
| Medium | Single-module implementation with clear requirements | Short plan, targeted tests/build |
| High | Cross-module work, public API, auth, permissions, security, privacy, audit, transactions, migrations, persistence, data consistency, cache, queue, concurrency | Plan first, narrow implementation slices, independent review or equivalent evidence |
| Release / Incident | Release gates, rollback, production config, production data, outage or hotfix work | Read-only assessment first, rollback plan, runtime/release evidence |

Escalate immediately if requirements are ambiguous, scope expands unexpectedly, a gate fails twice without a clear cause, the change touches high-risk domains, or current code, docs, and runtime output disagree.

## Planning

For non-trivial work, maintain a live task plan. For high-risk or cross-module work, create or update a durable plan with background, non-goals, risk tier, editable scope, implementation steps, acceptance criteria, validation matrix, rollback strategy, and completion sync. Keep the plan synchronized with actual progress.

## Collaboration

Use explicit roles when multiple people, tools, or agents participate:

- Lead: owns facts, boundaries, decisions, final review, and handoff.
- Scout: read-only discovery of files, symbols, docs, logs, and command outputs.
- Implementer: edits only the assigned scope.
- Reviewer: checks correctness, regressions, security, data, and missing tests.
- Verifier: runs commands and records evidence.

One task has one final owner. Do not recursively delegate. One file should have one active implementer at a time. Resolve disagreements using current code, executable evidence, and task goals.

## Harness

This repository should expose a single harness entrypoint:

```bash
scripts/harness/check.sh <gate> [args]
```

Expected gates:

| Gate | Purpose | Default strength |
| --- | --- | --- |
| `quick` | Default local PR gate using low-environment checks | Run for broad changes |
| `changed` | Select checks from changed files | Prefer for normal PR work |
| `docs` | Docs index, links, naming, revision policy, repo hygiene, whitespace | Run for docs and workflow changes |
| `backend` | Backend compile/tests/quality gate | Run for backend changes |
| `frontend` | Frontend type-check/build/tests | Run for frontend changes |
| `mobile` | Mobile static audit/build/smoke | Run for mobile changes |
| `contract` | API/schema/client path/public enum contract checks | Run for public contract changes |
| `runtime` | Health, metrics, sanitized logs, optional smoke against a running service | Explicit diagnostic |
| `e2e` | End-to-end workflow against real or provisioned runtime dependencies | Explicit or dedicated CI |
| `release` | Full pre-release evidence package | Required before release |
| `harness-tests` | Self-tests for harness scripts and report contracts | Run when harness changes |

`quick` must not require real secrets, production services, uncontrolled external accounts, or manual tools. Runtime-heavy checks stay explicit unless stable, fast, reproducible, and easy to interpret. CI should call the same harness entrypoint as local development.

## Harness Reports

Important gates should support:

```bash
HARNESS_REPORT_DIR=release-artifacts/harness/<gate> scripts/harness/check.sh <gate>
```

Reports should include `summary.json`, `summary.md`, `steps.jsonl`, and `logs/`. Allowed statuses are `PASS`, `FAIL`, `SKIPPED`, and `PLANNED`. Skipped steps must include reason and enabling condition. Reports and logs must be sanitized.

## Changed-Gate Selection

`changed` should reduce cost without reducing quality. It should support plan-only mode and changed-file overrides.

| Changed surface | Required gates | Conditional gates |
| --- | --- | --- |
| Docs | `docs` | whitespace check |
| Backend routes/controllers | `backend`, `contract` | frontend/mobile build, API smoke |
| DTO/schema/enums | `backend`, `contract` | client schema report |
| Client API wrappers | `contract`, `frontend` or `mobile` | runtime smoke |
| Frontend pages/components | `frontend` | UI smoke or screenshots |
| Mobile pages/interactions | `mobile` | device/simulator smoke |
| Database/persistence | `backend`, migration/schema check | runtime DB check, E2E |
| Auth/permissions/audit/transactions | `backend`, guardrails, `contract` | API regression, independent review |
| Harness/CI | `harness-tests`, `quick` | affected specialized gates |
| Release/deploy config | `docs`, `release` or dry-run | runtime context, rollback validation |

## Docs Gate

Docs are product and engineering state. The docs gate should check docs index, active local links, stable filenames, document nature, revision history, snapshot naming, temporary/junk files, and `git diff --check`.

Update docs, runbooks, workflow files, or project memory when a change affects long-term behavior, validation, release steps, architecture, backlog state, or operating assumptions.

## Contract Gates

Public contracts should fail early in PRs. Prioritize static, low-environment checks: route contract, static schema contract, client path contract, public enum/catalog contract, runtime schema diff as explicit diagnostic, and client field alignment as report-only until stable.

Only update snapshots for intentional contract changes. Code and snapshot updates must be in the same PR. Temporary allowlists need a reason, owner, and expiration condition.

## Structure Guardrails

Turn high-value architecture rules into executable tests or scripts. Prioritize sensitive field exposure, response envelope consistency, DTO boundaries, centralized exception handling, audit/change-log boundaries, after-commit side effects, transaction boundaries, server-side permission checks, and database constraints for core invariants.

## Runtime, E2E, and Release

Runtime gates should collect health, key metrics, sanitized error-log tail, optional API regression or smoke summary, and relevant schema/database/migration status.

Release gates should record commit, branch, target environment, parameters, config checks, database checks, production builds/tests, explicitly enabled heavy E2E/smoke, skipped-step reasons, report path, and failure logs. Pin runtime dependency versions exactly; do not use floating `latest` tags for release-critical dependencies.

## Security

- Never commit real secrets or customer data.
- Example config must use obvious placeholders.
- Runtime checks should detect missing, empty, placeholder, and unsafe default values.
- Logs, artifacts, and uploaded reports must be sanitized.
- Auth, permissions, privacy, audit, transaction, persistence, migration, data-consistency, and release changes are high risk by default.

## Definition of Done

Before final handoff:

- The requested behavior is implemented and non-goals were not mixed in.
- Relevant docs, runbooks, indexes, issues, PR notes, or project memory are updated, or no update is needed.
- The narrowest meaningful validation passed.
- High-risk surfaces received specialized gates, runtime/release evidence, or independent review.
- Failed or skipped validation is listed with reason and follow-up.
- User or teammate changes were not overwritten.
- The final response includes changed files, validation performed, residual risks, and recommended next review if needed.
