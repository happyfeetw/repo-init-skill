---
name: repo-init
description: Initialize or update repository-level agent operating instructions, AGENTS.md, quality workflow docs, execution-plan templates, and harness guidance for an AI-agent-driven software project. Use when Codex is asked to set up a new repository for agent-driven development, bootstrap or merge AGENTS.md, auto-select Chinese or English templates from the user conversation language, check existing AGENTS/docs before writing, ask whether to overwrite or merge, create reusable quality workflow documentation, add harness expectations, or migrate these standards into another repo.
---

# Repo Init

## Goal

Set up a repository so AI agents and human collaborators share the same quality workflow: source priority, risk routing, planning, harness gates, report evidence, contract checks, safety rules, and completion standards.

Select template language from the current user-agent conversation language: Chinese conversation -> Chinese templates; English conversation -> English templates. If the user explicitly requests a language, use that language.

## Workflow

1. Inspect the target repository before writing:
   - `pwd`
   - `git status --short --branch`
   - existing `AGENTS.md`, `docs/`, `.github/workflows/`, `scripts/harness/`, package/build files, and module layout
2. Select language:
   - Use `zh` when the current conversation with the user is primarily Chinese.
   - Use `en` when the current conversation with the user is primarily English.
   - Do not ask the user about language unless their request explicitly asks for a different language or the conversation is genuinely mixed.
3. Identify whether this is:
   - a fresh repo with no agent instructions
   - a repo with an existing `AGENTS.md` that must be merged
   - a repo that already has harness/docs conventions and only needs alignment
4. Always scan before writing:
   - `scripts/init_repo_quality.py --repo <target-repo> --conversation-lang zh --scan`
   - or `scripts/init_repo_quality.py --repo <target-repo> --conversation-lang en --scan`
   - include `--with-harness-skeleton` in the scan if the user wants a harness entrypoint created
5. If the scan finds existing `AGENTS.md`, related docs, or harness files, stop and ask the user how to proceed unless the user already specified a choice:
   - Overwrite: replace generated targets. Use `--mode overwrite`.
   - Merge: preserve existing files, generate `.proposed` files with `--mode propose`, then manually merge the standards into the existing repo-specific instructions and docs.
   - Skip: leave existing files untouched and report what already exists.
6. Use the bundled initializer only after the conflict choice is clear:
   - Fresh repo: `scripts/init_repo_quality.py --repo <target-repo> --conversation-lang <zh|en>`
   - Merge path: `scripts/init_repo_quality.py --repo <target-repo> --conversation-lang <zh|en> --mode propose`
   - Overwrite path: `scripts/init_repo_quality.py --repo <target-repo> --conversation-lang <zh|en> --mode overwrite`
   - Add `--with-harness-skeleton` only when the target repo does not already have a harness entrypoint or the user asks for one.
7. For merge mode:
   - Read existing `AGENTS.md` and related docs.
   - Read the generated `.proposed` files.
   - Preserve repo-specific domain, build, test, deploy, security, and workflow rules.
   - Add only the missing quality workflow, harness, report, risk routing, and completion standards.
   - Remove `.proposed` files only after their useful content is merged or explicitly rejected.
8. Adapt placeholders:
   - module names
   - build/test commands
   - docs index path
   - runtime/release commands
   - contract gate names
   - package managers and language-specific checks
9. Validate with the narrowest available checks:
   - `git diff --check`
   - repository docs/harness gate if present
   - generated harness skeleton `scripts/harness/check.sh docs` if created
   - skill script dry run or temp-dir run when modifying this skill
10. Final handoff must include:
   - files created or updated
   - selected language and why
   - whether conflicts were found and whether the user chose overwrite, merge, or skip
   - whether existing instructions were preserved or proposed separately
   - validation commands and results
   - remaining repo-specific placeholders or follow-up work

## Bundled Resources

- `scripts/init_repo_quality.py`: copies templates into a target repository and optionally creates a minimal harness skeleton.
- `assets/AGENTS.zh.md`: Chinese `AGENTS.md` template.
- `assets/AGENTS.en.md`: English `AGENTS.md` template.
- `assets/docs/agent-quality-workflow.zh.md`: Chinese quality workflow reference.
- `assets/docs/agent-exec-plan.zh.md`: Chinese execution-plan template.
- `assets/docs/harness-guide.zh.md`: Chinese harness guide.
- `assets/docs/agent-quality-workflow.en.md`: English quality workflow reference.
- `assets/docs/agent-exec-plan.en.md`: English execution-plan template.
- `assets/docs/harness-guide.en.md`: English harness guide.

Read asset files only when you need to inspect or manually merge their contents. Prefer running the initializer for straightforward bootstraps.

## Safety Rules

- Never overwrite an existing `AGENTS.md`, docs, or harness script without explicit user confirmation or `--force`.
- Never choose overwrite when the user has not explicitly approved overwrite.
- Prefer merge over overwrite when existing files contain repo-specific rules.
- Do not add production dependencies.
- Do not commit or generate secrets.
- Do not assume every repo has backend/frontend/mobile modules; trim irrelevant gates.
- Keep initialized docs generic and product-agnostic until the target repo supplies domain-specific rules.
