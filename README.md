# repo-init skill

`repo-init` is a Codex-compatible skill for bootstrapping repository-level agent instructions and quality workflow assets.

It helps an agent initialize or update:

- `AGENTS.md`
- quality workflow documentation
- execution-plan templates
- harness guidance
- an optional minimal `scripts/harness/check.sh` skeleton

The skill is intentionally conservative: it scans first, detects existing `AGENTS.md` and related documents, and requires an explicit overwrite or merge path before changing existing targets.

中文说明见 [README.zh-CN.md](README.zh-CN.md).

## What It Does

- Selects Chinese or English templates from the user-agent conversation language.
- Scans the target repository before writing.
- Detects existing `AGENTS.md`, `docs/engineering` quality docs, and `scripts/harness`.
- Supports three conflict modes:
  - `fail`: stop when target files already exist.
  - `propose`: preserve existing files and create `.proposed` files for manual merge.
  - `overwrite`: replace existing generated targets after explicit approval.
- Can create a minimal harness skeleton for new repositories.
- Ships reusable Chinese and English templates.

## Repository Layout

```text
repo-init-skill/
├── repo-init/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   ├── assets/
│   │   ├── AGENTS.en.md
│   │   ├── AGENTS.zh.md
│   │   └── docs/
│   └── scripts/init_repo_quality.py
├── scripts/validate.sh
├── README.md
├── README.zh-CN.md
└── LICENSE
```

## Install

Clone this repository, then copy the `repo-init` skill directory into your Codex skills directory:

```bash
git clone https://github.com/happyfeetw/repo-init-skill.git
mkdir -p ~/.codex/skills
cp -R repo-init-skill/repo-init ~/.codex/skills/repo-init
```

If `CODEX_HOME` is set, install under `$CODEX_HOME/skills` instead:

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R repo-init-skill/repo-init "$CODEX_HOME/skills/repo-init"
```

## Use the Skill

Ask your agent:

```text
Use $repo-init to initialize AGENTS.md, quality workflow docs, and harness guidance for this repository.
```

Expected behavior:

1. The agent inspects the target repository.
2. The agent chooses Chinese or English templates based on the conversation language.
3. The agent scans for existing `AGENTS.md`, docs, and harness files.
4. If conflicts exist, the agent asks whether to overwrite, merge, or skip.
5. The agent writes files, adapts placeholders, validates, and reports remaining follow-up.

## Use the Script Directly

Scan only:

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang en \
  --scan
```

Initialize a fresh repository with English templates:

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang en \
  --with-harness-skeleton
```

Initialize with Chinese templates:

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang zh \
  --with-harness-skeleton
```

Generate merge proposals when targets already exist:

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang en \
  --mode propose
```

Overwrite existing targets only after explicit approval:

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang en \
  --mode overwrite
```

## Validation

Run:

```bash
scripts/validate.sh
```

The validation script checks Python syntax and runs smoke tests for:

- Chinese initialization
- English initialization
- conflict scan
- default conflict failure
- proposal generation
- explicit overwrite

## License

MIT. See [LICENSE](LICENSE).
