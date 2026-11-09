# 已有能力台账

> 这是**现状记录**，不是任务清单。只有「要继续改进 / 补测试 / 扩展」的条目才另建 Issue。
> 本仓库是公开仓库，证据里不要出现 token、内网地址、真实个人信息。

| 编号 | 已有能力 | 当前版本/环境 | 证据 | 代码位置 | 核验人 | 核验日期 | 结论 |
|---|---|---|---|---|---|---|---|
| B01 | WebView2 桌面启动器 | | | `launcher-source/src/` | | | 待核验 |
| B02 | Harness 运行时集成 | | | `harness.zip` | | | 待核验 |
| B03 | 启动脚本（cmd / vbs） | | | `launcher-bin/` | | | 待核验 |
| B04 | 开机自启动安装与卸载 | | | `launcher-bin/uninstall-autostart.cmd` | | | 待核验 |
| B05 | 打包与构建流程 | | | `launcher-source/scripts/`、`installer/` | | | 待核验 |
| B06 | 测试 | | | `launcher-source/tests/` | | | 待核验 |
| B07 | 插件地图文档 | | | `docs/plugin-map.md` | | | 待核验 |
| B08 | 可行性分析文档 | | | `docs/feasibility.md` | | | 待核验 |

## 结论取值

`验收通过` / `部分可用` / `仅演示` / `待核验` / `已废弃`

## 证据存放约定

- 截图与录屏：贴到对应 Issue 评论，GitHub 自动托管，别把大文件塞进仓库。
- 测试记录：`docs/evidence/B0x-YYYYMMDD.md`。
- 禁止：token、密钥、内网 IP、真实用户名与路径（如 `C:\Users\<真实姓名>`）。

## 关键判断

已上线且能用的，只进台账；**只有要继续改进的，才建 Issue**，避免重复开发。
