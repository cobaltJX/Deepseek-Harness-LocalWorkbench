# 开发与验收流程

## 状态定义

| 状态 | 含义 | 进入条件 |
|---|---|---|
| Backlog | 需求池 | 已记录，未安排 |
| Todo | 待开发 | 范围、负责人、日期已定 |
| In Progress | 开发中 | 已开分支开始写 |
| In Review | 待审核/验收 | 已提 PR 或交付物 |
| Blocked | 受阻 | 外部依赖/资源受阻，已在 Issue 说明 |
| Done | 已完成 | 验收通过且有证据 |

## 标准流程

1. 建 Issue，写清范围与验收标准。
2. 加进 Project，填 Module / Priority / Iteration / 日期 / Assignee。
3. 从 Issue 建分支（`Create a branch`）。
4. 提交并开 PR，描述写 `Closes #编号`。
5. 审核：看代码、测试结果、安全影响。
6. 需改则 `Request changes`，改完重审。
7. 合并 PR。
8. 验收：功能跑一遍，证据贴到 Issue 评论。
9. 验收通过关闭 Issue，状态自动变 `Done`。

## 公开仓库的额外要求

- 外部贡献者通过 **fork + PR** 提交，不给写权限。
- PR 里出现 token、密钥、内网地址、真实个人信息，一律拒绝并要求清理历史。
- 涉及下载与安装的逻辑，必须校验来源与哈希。

## 禁止

- 直接 push 到 `main`
- 未验收就拖 `Done`
- 把密钥、口令、token 提交进仓库
