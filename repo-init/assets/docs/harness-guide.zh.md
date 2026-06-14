# Harness 使用说明

文档性质: 常驻工程规范。本文说明仓库级 harness 的入口、分层、报告和扩展规则。

## 修订记录

| 日期 | 修订内容 |
| --- | --- |
| YYYY-MM-DD | 建立 harness 使用说明。 |

## 统一入口

仓库应提供统一入口:

```bash
scripts/harness/check.sh <gate> [args]
```

建议 gate:

| Gate | 目的 |
| --- | --- |
| `quick` | 默认本地 PR 门禁，串联低环境依赖检查 |
| `changed` | 根据变更文件选择检查 |
| `docs` | 文档索引、链接、命名、修订记录、仓库卫生、空白检查 |
| `backend` | 后端编译、测试或质量门 |
| `frontend` | 前端类型检查、构建或测试 |
| `mobile` | 移动端静态审计、构建或 smoke |
| `contract` | API、schema、客户端路径、公开枚举等契约检查 |
| `runtime` | 运行中服务 health、metrics、脱敏日志和可选 smoke |
| `e2e` | 端到端业务闭环 |
| `release` | 发布前完整证据包 |
| `harness-tests` | harness 脚本和报告契约自测 |

## 分层规则

- `quick` 不依赖真实 secret、生产服务、不可控外部账号或手工工具。
- runtime/E2E/release 这类重型检查保持显式运行。
- 每个 gate 必须能单独运行。
- CI 和本地使用同一个 harness 入口。
- 修改 harness 选择逻辑或报告格式时，必须运行 `harness-tests`。

## 报告契约

重要 gate 应支持:

```bash
HARNESS_REPORT_DIR=release-artifacts/harness/<gate> scripts/harness/check.sh <gate>
```

报告目录至少包含:

- `summary.json`
- `summary.md`
- `steps.jsonl`
- `logs/`

步骤状态:

- `PASS`
- `FAIL`
- `SKIPPED`
- `PLANNED`

跳过步骤必须写原因和开启条件。报告和日志必须脱敏。

## 最小骨架

如果仓库还没有 harness，可以先实现:

1. `docs`: 文档与仓库卫生检查。
2. `quick`: 串联 docs 和核心模块静态检查。
3. `changed`: 按变更文件选择 gate。
4. `harness-tests`: 自测选择逻辑和报告格式。
5. `runtime` / `release`: 在有运行环境后补齐。
