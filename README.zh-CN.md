# repo-init skill

`repo-init` 是一个兼容 Codex skill 结构的仓库初始化技能，用于为 AI agent 驱动的软件项目初始化仓库级工作约定和质量工作流。

它可以帮助 agent 初始化或更新：

- `AGENTS.md`
- 质量工作流文档
- 执行计划模板
- harness 使用说明
- 可选的最小 `scripts/harness/check.sh` 骨架

这个 skill 的默认策略是保守的：先扫描目标仓库，检查是否已有 `AGENTS.md`、相关工程文档和 harness 文件；发现冲突时，不会静默覆盖，而是要求选择覆盖、融合或跳过。

English documentation: [README.md](README.md).

## 能力

- 根据用户与 agent 的沟通语言自动选择中文或英文模板。
- 写入前扫描目标仓库。
- 检查已有 `AGENTS.md`、`docs/engineering` 下的质量文档和 `scripts/harness`。
- 支持三种冲突处理模式：
  - `fail`：默认模式，发现已有目标文件就停止。
  - `propose`：保留已有文件，生成 `.proposed` 文件供融合。
  - `overwrite`：在明确确认后覆盖已有目标。
- 可为新仓库创建最小 harness 骨架。
- 内置中英文模板。

## 仓库结构

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

## 安装

克隆仓库后，把 `repo-init` skill 目录复制到 Codex skills 目录：

```bash
git clone https://github.com/happyfeetw/repo-init-skill.git
mkdir -p ~/.codex/skills
cp -R repo-init-skill/repo-init ~/.codex/skills/repo-init
```

如果设置了 `CODEX_HOME`，则复制到 `$CODEX_HOME/skills`：

```bash
mkdir -p "$CODEX_HOME/skills"
cp -R repo-init-skill/repo-init "$CODEX_HOME/skills/repo-init"
```

## 使用 skill

向 agent 发起请求：

```text
Use $repo-init to initialize AGENTS.md, quality workflow docs, and harness guidance for this repository.
```

预期流程：

1. agent 先检查目标仓库。
2. agent 根据当前对话语言选择中文或英文模板。
3. agent 扫描已有 `AGENTS.md`、文档和 harness 文件。
4. 如发现冲突，agent 询问是覆盖、融合还是跳过。
5. agent 写入文件、适配占位项、运行验证并报告剩余事项。

## 直接使用脚本

只扫描，不写入：

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang zh \
  --scan
```

用中文模板初始化新仓库：

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang zh \
  --with-harness-skeleton
```

用英文模板初始化新仓库：

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang en \
  --with-harness-skeleton
```

已有文件时生成融合提案：

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang zh \
  --mode propose
```

明确确认后覆盖已有目标：

```bash
python3 repo-init/scripts/init_repo_quality.py \
  --repo /path/to/repo \
  --conversation-lang zh \
  --mode overwrite
```

## 验证

运行：

```bash
scripts/validate.sh
```

验证脚本会检查 Python 语法，并覆盖以下 smoke 场景：

- 中文初始化
- 英文初始化
- 冲突扫描
- 默认冲突失败
- 生成 `.proposed` 融合文件
- 显式覆盖

## 许可证

MIT，见 [LICENSE](LICENSE)。
