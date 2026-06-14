# Agent 执行计划模板

文档性质: 常驻模板。复杂任务、跨模块任务、高风险变更、发布变更、harness/CI 变更或多执行者协作时使用。

## 修订记录

| 日期 | 修订内容 |
| --- | --- |
| YYYY-MM-DD | 建立执行计划模板。 |

## 1. 背景

- 关联 issue:
- 关联 PR:
- 触发原因:
- 业务目标:
- 当前事实来源:
  - 代码:
  - 配置:
  - 文档:
  - 运行输出:

## 2. 非目标

- 本次不做:
- 延后到:
- 不应混入的相邻事项:

## 3. 风险等级

- 风险等级: 低风险 / 中风险 / 高风险 / 发布或事故风险
- 分级理由:
- 升级条件:
- 是否需要独立 review:

## 4. 可编辑范围

- 允许修改:
- 禁止触碰:
- 需要保护的已有改动:

## 5. 实施步骤

| 步骤 | 范围 | 文件/模块 | 验证 |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

每步结束时回答:

- 改了什么:
- 为什么可以继续:
- 失败如何回退:

## 6. 验收标准

- [ ] 行为符合任务目标。
- [ ] 没有混入非目标。
- [ ] 相关文档已更新或确认无需更新。
- [ ] 最小验证通过。
- [ ] 跳过或失败的验证已说明。
- [ ] 高风险项已 review 或有等价证据。

## 7. 验证矩阵

| 改动面 | 必跑 | 条件触发 | 结果 |
| --- | --- | --- | --- |
| docs | `scripts/harness/check.sh docs` | | |
| backend | `scripts/harness/check.sh backend` | | |
| frontend | `scripts/harness/check.sh frontend` | | |
| mobile | `scripts/harness/check.sh mobile` | | |
| contract | `scripts/harness/check.sh contract` | | |
| runtime | `scripts/harness/check.sh runtime` | | |
| release | `scripts/harness/check.sh release` | | |

## 8. 回滚策略

- 代码回滚:
- 数据/迁移回滚:
- 配置回滚:
- 发布回滚:
- 文档/issue 状态回滚:

## 9. 交付说明草稿

```text
## Summary

-

## Validation

- [ ]

## Risks

-
```
