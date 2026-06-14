# Agent-Driven Project Quality Workflow

Document nature: Persistent engineering standard. This document defines the quality workflow shared by AI agents, automation scripts, and human collaborators in this repository.

## Revision History

| Date | Change |
| --- | --- |
| YYYY-MM-DD | Established quality workflow standard. |

## Principles

- Current code, configuration, scripts, and command output outrank old docs and memory.
- Quality rules should move into tests, lint, scripts, contract snapshots, runtime smoke, or release gates whenever practical.
- Ordinary PRs use low-environment, stable, fast, repeatable default gates.
- Checks that depend on real services, databases, external accounts, object storage, mobile tooling, or online environments stay explicit and produce structured reports.
- High-risk changes require planning before implementation and independent review or equivalent evidence before handoff.

## Risk Tiers

| Tier | Typical work | Minimum requirement |
| --- | --- | --- |
| Low | Docs, copy, small styles, fixtures, no behavior change | Minimal check |
| Medium | Clear single-module implementation | Short plan plus module validation |
| High | Cross-module, public API, permissions, security, audit, transactions, migrations, data consistency | Durable plan plus specialized gates and review |
| Release / Incident | Release, rollback, production config, production data, hotfix | Read-only assessment plus rollback plan and runtime/release evidence |

## Validation Matrix

| Surface | Required | Conditional |
| --- | --- | --- |
| Docs | `scripts/harness/check.sh docs` | `git diff --check` |
| Backend | `scripts/harness/check.sh backend` | contract/API smoke |
| Frontend | `scripts/harness/check.sh frontend` | UI smoke |
| Mobile | `scripts/harness/check.sh mobile` | device/simulator smoke |
| API/contract | `scripts/harness/check.sh contract` | runtime schema/client report |
| Database/migration | backend gate + schema/migration check | runtime DB/E2E |
| Harness/CI | `scripts/harness/check.sh harness-tests` | `quick` |
| Release | `scripts/harness/check.sh release` | runtime context/E2E |

If validation cannot run, record the command, reason, replacement evidence, and follow-up.

## Definition of Done

- Target behavior is implemented without mixing non-goals.
- Docs, indexes, runbooks, issues, PR notes, or project memory are updated, or no update is needed.
- The matching minimal gate ran.
- High-risk changes have specialized validation, runtime/release evidence, or independent review.
- Failed or skipped validation is explained.
- User or teammate changes were not overwritten.
