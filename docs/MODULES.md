# 模块划分（占位，待确认）

> 当前是按仓库目录推断的占位划分，跑通流程后按实际代码重命名即可。
> 改名时同步更新：本文件、Project 的 `Module` 字段、`module:*` 标签、CODEOWNERS。

| 模块 | 名称 | 范围 | 主要目录 |
|---|---|---|---|
| M0 | 项目治理 | 文档、Issue/PR 模板、看板、流程 | `docs/`、`.github/` |
| M1 | 启动器 | WebView2 窗口、启动流程、自启动 | `launcher-source/src/`、`launcher-bin/` |
| M2 | Harness 运行时 | 运行时集成、插件、配置 | `harness.zip`、`docs/plugin-map.md` |
| M3 | 构建与打包 | 构建脚本、安装包、发布产物 | `launcher-source/scripts/`、`installer/` |
| M4 | 文档与发布 | README、变更日志、发布说明 | `README.md`、`launcher-source/CHANGELOG.md` |

## 模块负责人

见 [OWNERSHIP.md](OWNERSHIP.md)。一个模块一个负责人，负责人默认是该模块 Issue 的验收人。
