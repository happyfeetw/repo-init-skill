# Agent Execution Plan Template

Document nature: Persistent template. Use for complex tasks, cross-module work, high-risk changes, release changes, harness/CI changes, or multi-participant collaboration.

## Revision History

| Date | Change |
| --- | --- |
| YYYY-MM-DD | Established execution plan template. |

## 1. Background

- Issue:
- PR:
- Trigger:
- Business goal:
- Current facts:
  - Code:
  - Config:
  - Docs:
  - Runtime output:

## 2. Non-Goals

- Not doing:
- Deferred to:
- Adjacent work to exclude:

## 3. Risk Tier

- Tier: Low / Medium / High / Release or Incident
- Rationale:
- Escalation conditions:
- Independent review needed:

## 4. Editable Scope

- Allowed:
- Forbidden:
- Existing changes to protect:

## 5. Implementation Steps

| Step | Scope | Files/modules | Validation |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

At the end of each step, answer:

- What changed:
- Why it is safe to continue:
- How to roll back if it fails:

## 6. Acceptance Criteria

- [ ] Behavior matches the goal.
- [ ] Non-goals were not mixed in.
- [ ] Related docs were updated or no update is needed.
- [ ] Minimal validation passed.
- [ ] Skipped or failed validation is explained.
- [ ] High-risk items were reviewed or have equivalent evidence.

## 7. Validation Matrix

| Surface | Required | Conditional | Result |
| --- | --- | --- | --- |
| docs | `scripts/harness/check.sh docs` | | |
| backend | `scripts/harness/check.sh backend` | | |
| frontend | `scripts/harness/check.sh frontend` | | |
| mobile | `scripts/harness/check.sh mobile` | | |
| contract | `scripts/harness/check.sh contract` | | |
| runtime | `scripts/harness/check.sh runtime` | | |
| release | `scripts/harness/check.sh release` | | |

## 8. Rollback

- Code:
- Data/migration:
- Config:
- Release:
- Docs/issue state:

## 9. Handoff Draft

```text
## Summary

-

## Validation

- [ ]

## Risks

-
```
