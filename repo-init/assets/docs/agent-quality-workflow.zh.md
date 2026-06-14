# Agent 驱动项目质量工作流

文档性质: 常驻工程规范。本文定义本仓库中 AI agent、自动化脚本和人工协作者共同遵守的质量工作流。

## 修订记录

| 日期 | 修订内容 |
| --- | --- |
| YYYY-MM-DD | 建立质量工作流规范。 |

## 原则

- 当前代码、配置、脚本和命令输出优先于旧文档和记忆。
- 质量要求应尽量进入测试、lint、脚本、契约快照、运行时 smoke 或 release gate。
- 普通 PR 使用低环境依赖、稳定、快速、可重复的默认 gate。
- 依赖真实服务、数据库、外部账号、对象存储、移动端工具或线上环境的验证保持显式运行，并输出结构化报告。
- 高风险变更先计划、后实现，并在交付前有独立 review 或等价证据。

## 风险分级

| 等级 | 典型任务 | 最低要求 |
| --- | --- | --- |
| 低风险 | 文档、文案、小样式、fixture、无行为变更 | 最小检查 |
| 中风险 | 单模块实现、需求清晰 | 简短计划 + 模块验证 |
| 高风险 | 跨模块、公共 API、权限、安全、审计、事务、迁移、数据一致性 | 持久化计划 + 专项 gate + review |
| 发布/事故风险 | 发布、回滚、生产配置、生产数据、故障修复 | 只读评估 + 回滚方案 + runtime/release 证据 |

## 验证矩阵

| 变更面 | 必跑 | 条件触发 |
| --- | --- | --- |
| 文档 | `scripts/harness/check.sh docs` | `git diff --check` |
| 后端 | `scripts/harness/check.sh backend` | contract/API smoke |
| 前端 | `scripts/harness/check.sh frontend` | UI smoke |
| 移动端 | `scripts/harness/check.sh mobile` | 设备/模拟器 smoke |
| API/契约 | `scripts/harness/check.sh contract` | runtime schema/client report |
| 数据库/迁移 | backend gate + schema/migration check | runtime DB/E2E |
| Harness/CI | `scripts/harness/check.sh harness-tests` | `quick` |
| 发布 | `scripts/harness/check.sh release` | runtime context/E2E |

如果验证不能运行，必须记录命令、原因、替代证据和后续补跑位置。

## 完成标准

- 实现目标行为，且没有混入非目标。
- 文档、索引、运行手册、issue、PR 说明或项目记忆已同步，或确认无需同步。
- 运行了与变更面匹配的最小 gate。
- 高风险变更有专项验证、runtime/release 证据或独立 review。
- 失败或跳过验证有说明。
- 没有覆盖未授权的用户或协作者改动。
