# GitHub 配置基线

记录本仓库的实际配置，便于交接与排障。

| 项 | 值 | 位置 |
|---|---|---|
| 仓库 | `cobaltJX/Deepseek-Harness-LocalWorkbench` | — |
| 可见性 | Public | Settings → General |
| 归属 | 个人账号（非组织） | — |
| 默认分支 | `main` | Settings → General |
| Issues | 已开启 | Settings → Features |
| Projects | 已开启 | Settings → Features |
| 分支保护 | `protect-main`：必须走 PR、禁强推、禁删 | Settings → Rules → Rulesets |
| Issue 模板 | `feature.yml` / `bug.yml` | `.github/ISSUE_TEMPLATE/` |
| PR 模板 | `PULL_REQUEST_TEMPLATE.md` | `.github/` |
| 审核人分配 | `CODEOWNERS` → @cobaltJX | `.github/CODEOWNERS` |
| 迭代周期 | 2 周（Project 建好后配置） | Project Iteration 字段 |

## 计划与限制

- 公开仓库：分支保护、Actions、Insights 均可用，无需付费计划。
- 个人账号：**没有 Teams**，权限只能逐个加 Collaborator。
- 公开仓库意味着 **Issue/PR 对外可见**，敏感信息一律不进仓库和 Issue。

## 待办配置（需在网页完成）

- [ ] 创建 Project「DSH Workbench｜研发计划」并配置字段
- [ ] 建四个视图（全部任务 / 本轮迭代 / 路线图 / 受阻待验收）
- [ ] 开启 Auto-add、Item closed、Auto-archive 三个 workflow
- [ ] 给协作者单独授予 Project 访问权限
