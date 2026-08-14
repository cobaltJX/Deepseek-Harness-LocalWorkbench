# DeepSeek Harness 插件地图与修改指南

仓库根目录：

```text
C:\Users\jx\Desktop\deepseek-harness-master
```

## 1. 结论

DeepSeek Harness 确实是“一切皆插件”的架构，运行时的 agent loop、工具、模型适配器、文件系统、Shell、子 Agent、持久化、Web UI 都是由 Cordis 插件树组装出来的。

但源码里不是所有文件都是插件。需要区分四类：

| 类型 | 位置 | 作用 |
|---|---|---|
| Cordis 插件 | `packages/*/*` | 提供 service、event、tool、effect |
| 纯库/协议包 | `packages/*/*` 的一部分 | 只提供类型、工具函数，不直接注册插件 |
| Bundle 组合层 | `packages/bundle/*` | 决定哪些插件按什么顺序挂载 |
| App/运行时入口 | `apps/*`、`python/*`、`examples/*` | 启动 CLI、Web、SDK 或示例组合 |

## 2. 怎么找插件

每个插件通常有这些文件：

```text
packages/<group>/<pkg>/
  package.json          # npm 包名、exports、依赖
  README.md             # 职责、配置、注意事项
  src/index.ts          # 插件入口，通常 export const name = '...'
  src/*.ts              # 具体实现
  lib/                  # 构建后的 JS
```

Bundle 组合层有：

```text
packages/bundle/base/cordis.patch.yml
packages/bundle/web-app/cordis.patch.yml
packages/bundle/headless/cordis.patch.yml
```

其中每一条就是一次插件挂载，例如：

```yaml
- id: llm-deepseek
  name: '@deepseek-ai/dsh-llm-deepseek'
```

想看实际生效的插件树：

```powershell
cd C:\Users\jx\Desktop\deepseek-harness-master

pnpm dsh --profile web --dump-default-config
pnpm dsh --profile web --dump-config
```

生成的可视化组合图在：

```text
apps/cli/composition.md
```

## 3. 核心 Agent 插件

| 文件夹 | 插件/包 | 主要职责 | 主要入口 |
|---|---|---|---|
| `packages/core/session` | `@deepseek-ai/dsh-session` | append-only session log、SessionEvent、会话内存 store | `src/index.ts` |
| `packages/core/agent` | `@deepseek-ai/dsh-agent` | Agent 接口、registry、`agent/*` 事件 | `src/index.ts` |
| `packages/core/agent-loop` | `@deepseek-ai/dsh-agent-loop` | 唯一的具体 loop 驱动，turn/step/tool 生命周期 | `src/index.ts` |
| `packages/core/system-prompt` | `@deepseek-ai/dsh-system-prompt` | system prompt section 和 tool schema 组装 | `src/index.ts` |
| `packages/core/tools` | `@deepseek-ai/dsh-tools` | tool registry、参数校验、执行管道 | `src/index.ts` |
| `packages/core/scope` | `@deepseek-ai/dsh-scope` | per-agent scoped registration | `src/index.ts` |
| `packages/core/agent-default-model` | `@deepseek-ai/dsh-agent-default-model` | 默认 provider/model | `src/index.ts` |
| `packages/core/agent-tool-presentation` | `@deepseek-ai/dsh-agent-tool-presentation` | native/code/both 工具呈现模式 | `src/index.ts` |

## 4. 模型与 LLM

| 文件夹 | 插件/包 | 主要职责 | 关键点 |
|---|---|---|---|
| `packages/llm/llm` | `@deepseek-ai/dsh-llm` | LLM 抽象、Message/StreamChunk、adapter seam、prepareCall | `src/index.ts` |
| `packages/llm/llm-deepseek` | `@deepseek-ai/dsh-llm-deepseek` | DeepSeek 官方 chat-completions 适配器，`deepseek-official` 路由 | `src/index.ts`、`src/adapter.ts`、`src/serialize.ts`、`src/translate.ts` |
| `packages/llm/llm-pi-ai` | `@deepseek-ai/dsh-llm-pi-ai` | 通用多 provider/OpenAI-compatible/gateway 适配器 | `src/index.ts` |
| `packages/llm/llm-retry` | `@deepseek-ai/dsh-llm-retry` | `agent/request-error` 后的重试策略 | `src/index.ts` |
| `packages/llm/token-meter` | `@deepseek-ai/dsh-token-meter` | token 计量、context 压力相关投影 | `src/index.ts` |

DeepSeek 官方模型的配置不是硬编码，可通过 `$DSH_HOME/settings.yaml` 的 `llm-deepseek:` 或 Web 的 Models 页面改。

## 5. 工具与执行能力

### 5.1 文件系统

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/fs/fs` | `@deepseek-ai/dsh-fs` | 文件系统 service seam |
| `packages/fs/fs-local` | `@deepseek-ai/dsh-fs-local` | 本地文件系统 provider |
| `packages/fs/fs-sandbox` | `@deepseek-ai/dsh-fs-sandbox` | 沙箱文件系统 provider |
| `packages/fs/fs-observation-policy` | `@deepseek-ai/dsh-fs-observation-policy` | 文件观察策略 |
| `packages/fs/tool-fs` | `@deepseek-ai/dsh-tool-fs` | 模型可见的 read/write 文件工具 |
| `packages/fs/tool-fs-search` | `@deepseek-ai/dsh-tool-fs-search` | grep/glob 搜索工具 |
| `packages/fs/tool-str-replace-editor` | `@deepseek-ai/dsh-tool-str-replace-editor` | 结构化编辑工具 |

### 5.2 Shell 与终端

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/shell/shell` | `@deepseek-ai/dsh-shell` | shell service seam |
| `packages/shell/bash-local` | `@deepseek-ai/dsh-bash-local` | 本地 Bash executor |
| `packages/shell/bash-sandbox` | `@deepseek-ai/dsh-bash-sandbox` | 沙箱 Bash executor |
| `packages/shell/pwsh-local` | `@deepseek-ai/dsh-pwsh-local` | 本地 PowerShell executor |
| `packages/shell/pwsh-sandbox` | `@deepseek-ai/dsh-pwsh-sandbox` | Windows PowerShell 沙箱 executor |
| `packages/shell/shell-env` | `@deepseek-ai/dsh-shell-env` | 注入 shell 环境变量 |
| `packages/shell/tool-bash` | `@deepseek-ai/dsh-tool-bash` | 模型可见 Bash 工具 |
| `packages/shell/tool-pwsh` | `@deepseek-ai/dsh-tool-pwsh` | 模型可见 PowerShell 工具 |
| `packages/shell/tool-bash-persistent` | `@deepseek-ai/dsh-tool-bash-persistent` | 持久 Bash 会话工具 |
| `packages/terminal/terminal` | `@deepseek-ai/dsh-terminal` | terminal service seam |
| `packages/terminal/terminal-bash` | `@deepseek-ai/dsh-terminal-bash` | Bash 持久终端 provider |
| `packages/terminal/tool-terminal` | `@deepseek-ai/dsh-tool-terminal` | 模型可见终端工具 |

### 5.3 子进程与沙箱

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/subprocess/subprocess` | `@deepseek-ai/dsh-subprocess` | subprocess service seam |
| `packages/subprocess/subprocess-local` | `@deepseek-ai/dsh-subprocess-local` | 本地子进程/PTY 实现，依赖 `node-pty` |
| `packages/sandbox/sandbox` | `@deepseek-ai/dsh-sandbox` | sandbox service seam |
| `packages/sandbox/sandbox-local` | `@deepseek-ai/dsh-sandbox-local` | 本地 sandbox provider |
| `packages/sandbox/sandbox-windows-acl` | `@deepseek-ai/dsh-sandbox-windows-acl` | Windows ACL 受限 token runner |
| `packages/sandbox/sandbox-policy` | `@deepseek-ai/dsh-sandbox-policy` | 文件写权限策略 |

### 5.4 Web、Skill、MCP、LSP

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/web/web` | `@deepseek-ai/dsh-web` | web capability seam |
| `packages/web/web-fetch-http` | `@deepseek-ai/dsh-web-fetch-http` | HTTP fetch provider |
| `packages/web/web-search-deepseek` | `@deepseek-ai/dsh-web-search-deepseek` | DeepSeek web search provider |
| `packages/web/web-search-exa` | `@deepseek-ai/dsh-web-search-exa` | Exa search provider |
| `packages/web/web-search-perplexity` | `@deepseek-ai/dsh-web-search-perplexity` | Perplexity search provider |
| `packages/web/tool-web` | `@deepseek-ai/dsh-tool-web` | 模型可见 web search/fetch 工具 |
| `packages/skill/skill` | `@deepseek-ai/dsh-skill` | skill registry 和发现 |
| `packages/skill/skill-filesystem` | `@deepseek-ai/dsh-skill-filesystem` | 从文件系统加载 skill |
| `packages/skill/skill-badge` | `@deepseek-ai/dsh-skill-badge` | skill 徽标 |
| `packages/skill/tool-skill` | `@deepseek-ai/dsh-tool-skill` | 模型可见 skill 工具 |
| `packages/mcp/mcp-client` | `@deepseek-ai/dsh-mcp-client` | MCP server 客户端，把 MCP tools 注册成 dsh tools |
| `packages/lsp/lsp` | `@deepseek-ai/dsh-lsp` | LSP seam |
| `packages/lsp/lsp-stdio` | `@deepseek-ai/dsh-lsp-stdio` | stdio LSP provider |
| `packages/lsp/tool-lsp` | `@deepseek-ai/dsh-tool-lsp` | 模型可见 LSP 工具 |

## 6. Agent 高阶能力

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/subagent/subagent` | `@deepseek-ai/dsh-subagent` | subagent service seam |
| `packages/subagent/subagent-spawn-in-process` | `@deepseek-ai/dsh-subagent-spawn-in-process` | 进程内 spawn 子 agent |
| `packages/subagent/subagent-fork-in-process` | `@deepseek-ai/dsh-subagent-fork-in-process` | fork 子 agent |
| `packages/subagent/subagent-acp` | `@deepseek-ai/dsh-subagent-acp` | ACP 子 agent |
| `packages/subagent/subagent-codex` | `@deepseek-ai/dsh-subagent-codex` | Codex 子 agent |
| `packages/subagent/subagent-claude-code` | `@deepseek-ai/dsh-subagent-claude-code` | Claude Code 子 agent |
| `packages/subagent/subagent-dsh-sdk` | `@deepseek-ai/dsh-subagent-dsh-sdk` | SDK 子 agent |
| `packages/subagent/tool-subagent` | `@deepseek-ai/dsh-tool-subagent` | 模型可见 subagent 委托工具 |
| `packages/subagent/tool-subagent-control` | `@deepseek-ai/dsh-tool-subagent-control` | 子 agent 控制/列表工具 |
| `packages/subagent/tool-subagent-report` | `@deepseek-ai/dsh-tool-subagent-report` | 子 agent 返回通道 |
| `packages/workflow/workflow` | `@deepseek-ai/dsh-workflow` | workflow seam |
| `packages/workflow/workflow-worker-thread` | `@deepseek-ai/dsh-workflow-worker-thread` | worker-thread workflow provider |
| `packages/workflow/tool-workflow` | `@deepseek-ai/dsh-tool-workflow` | 模型可见 workflow 工具 |
| `packages/workflow/tool-ralph` | `@deepseek-ai/dsh-tool-ralph` | Ralph 迭代 agent |
| `packages/goal/goal` | `@deepseek-ai/dsh-goal` | goal service |
| `packages/goal/goal-round-driver` | `@deepseek-ai/dsh-goal-round-driver` | goal round driver |
| `packages/goal/command-goal` | `@deepseek-ai/dsh-command-goal` | `/goal` command |
| `packages/goal/tool-goal` | `@deepseek-ai/dsh-tool-goal` | 模型可见 goal 工具 |
| `packages/plan/plan-mode` | `@deepseek-ai/dsh-plan-mode` | plan mode 状态与 prompt |
| `packages/todo/tool-todo` | `@deepseek-ai/dsh-tool-todo` | todo_write 工具 |
| `packages/jobs/jobs` | `@deepseek-ai/dsh-jobs` | 后台 job seam |
| `packages/jobs/jobs-local` | `@deepseek-ai/dsh-jobs-local` | 本地 job registry |
| `packages/jobs/tool-jobs` | `@deepseek-ai/dsh-tool-jobs` | job 控制工具 |

## 7. Session、持久化与上下文

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/session/session-persistence` | `@deepseek-ai/dsh-session-persistence` | session persistence seam |
| `packages/session/session-persistence-jsonl` | `@deepseek-ai/dsh-session-persistence-jsonl` | JSONL 持久化 |
| `packages/session/session-persistence-sqlite` | `@deepseek-ai/dsh-session-persistence-sqlite` | SQLite 持久化 |
| `packages/session/session-checkpoint-policy` | `@deepseek-ai/dsh-session-checkpoint-policy` | 请求/工具/步骤 checkpoint |
| `packages/session/session-projection` | `@deepseek-ai/dsh-session-projection` | 会话投影注册 |
| `packages/session/session-projection-cache` | `@deepseek-ai/dsh-session-projection-cache` | 投影缓存 |
| `packages/session/session-stats` | `@deepseek-ai/dsh-session-stats` | 会话统计 |
| `packages/session/session-title` | `@deepseek-ai/dsh-session-title` | 会话标题 seam |
| `packages/session/session-title-llm` | `@deepseek-ai/dsh-session-title-llm` | LLM 标题 provider |
| `packages/session/session-title-first-prompt-llm` | `@deepseek-ai/dsh-session-title-first-prompt-llm` | 首条 prompt 标题 provider |
| `packages/session/session-title-all-prompts-llm` | `@deepseek-ai/dsh-session-title-all-prompts-llm` | 全 prompt 标题 provider |
| `packages/session/session-telemetry` | `@deepseek-ai/dsh-session-telemetry` | telemetry seam |
| `packages/session/session-telemetry-otel` | `@deepseek-ai/dsh-session-telemetry-otel` | OTLP telemetry provider |
| `packages/session-query/session-query` | `@deepseek-ai/dsh-session-query` | 会话查询 seam |
| `packages/session-query/session-query-sqlite` | `@deepseek-ai/dsh-session-query-sqlite` | SQLite 全文查询 |
| `packages/session-query/session-log-export` | `@deepseek-ai/dsh-session-log-export` | 会话日志导出 |
| `packages/session-query/tool-session-query` | `@deepseek-ai/dsh-tool-session-query` | 模型可见会话查询工具 |
| `packages/context/agent-instructions` | `@deepseek-ai/dsh-agent-instructions` | agent instructions context |
| `packages/context/session-reference` | `@deepseek-ai/dsh-session-reference` | 会话引用 context |
| `packages/context/time-context` | `@deepseek-ai/dsh-time-context` | 时间上下文 |
| `packages/context/tmux-context` | `@deepseek-ai/dsh-tmux-context` | tmux 上下文 |
| `packages/compaction/compaction` | `@deepseek-ai/dsh-compaction` | compaction seam |
| `packages/compaction/compaction-basic` | `@deepseek-ai/dsh-compaction-basic` | 基础上下文压缩 |
| `packages/compaction/compaction-tool-result-pruner` | `@deepseek-ai/dsh-compaction-tool-result-pruner` | 大工具结果裁剪 |
| `packages/compaction/command-compact` | `@deepseek-ai/dsh-command-compact` | `/compact` command |

## 8. Web Host、API 与前端

### 8.1 Host 端

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/host/webserver` | `@deepseek-ai/dsh-host-webserver` | `node:http` server、HTTP/upgrade route |
| `packages/host/frontend-static` | `@deepseek-ai/dsh-host-frontend-static` | 前端 SPA dist 静态服务 |
| `packages/host/apiproxy` | `@deepseek-ai/dsh-host-apiproxy` | `/api` API proxy |
| `packages/host/directory-picker` | `@deepseek-ai/dsh-host-directory-picker` | 目录选择 seam |
| `packages/host/directory-picker-auto` | `@deepseek-ai/dsh-host-directory-picker-auto` | 自动选择 native/browse picker |
| `packages/host/directory-picker-browse` | `@deepseek-ai/dsh-host-directory-picker-browse` | Web browse picker |
| `packages/host/directory-picker-native` | `@deepseek-ai/dsh-host-directory-picker-native` | 原生目录选择器 |
| `packages/host/plugin-inventory` | `@deepseek-ai/dsh-host-plugin-inventory` | 当前插件清单投影 |

### 8.2 API

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/api/gateway` | `@deepseek-ai/dsh-api-gateway` | Typert RPC gateway |
| `packages/api/remotes` | `@deepseek-ai/dsh-api-remotes` | Web BFF remote 方法 |
| `packages/typert/generator` | `@deepseek-ai/dsh-typert-generator` | 生成 RPC descriptor |
| `packages/typert/loader` | `@deepseek-ai/dsh-typert-loader` | 加载 RPC descriptor |
| `packages/typert/protocol` | `@deepseek-ai/dsh-typert-protocol` | RPC 协议 |
| `packages/typert/registry` | `@deepseek-ai/dsh-typert-registry` | RPC registry |

### 8.3 Client/UI

主要浏览器插件在：

```text
packages/client/*/src
```

常用的前端插件：

| 文件夹 | 插件/包 | 职责 |
|---|---|---|
| `packages/client/web` | `@deepseek-ai/dsh-client-web` | Web shell |
| `packages/client/web-react` | `@deepseek-ai/dsh-client-web-react` | React shell |
| `packages/client/runtime` | `@deepseek-ai/dsh-client-runtime` | 浏览器运行时 |
| `packages/client/connection` | `@deepseek-ai/dsh-client-connection` | `/api` 和 WebSocket transport |
| `packages/client/modules` | `@deepseek-ai/dsh-client-modules` | 浏览器模块表 |
| `packages/client/hmr` | `@deepseek-ai/dsh-client-hmr` | 前端 HMR |
| `packages/client/locale` | `@deepseek-ai/dsh-client-locale` | 多语言 |
| `packages/client/ui-layout` | `@deepseek-ai/dsh-client-ui-layout` | 页面布局 |
| `packages/client/ui-sidebar` | `@deepseek-ai/dsh-client-ui-sidebar` | 侧边栏 |
| `packages/client/ui-conversation` | `@deepseek-ai/dsh-client-ui-conversation` | 会话区 |
| `packages/client/ui-tool` | `@deepseek-ai/dsh-client-ui-tool` | tool 调用渲染 |
| `packages/client/ui-settings-models` | `@deepseek-ai/dsh-client-ui-settings-models` | Models 设置页 |
| `packages/client/ui-settings-plugins` | `@deepseek-ai/dsh-client-ui-settings-plugins` | 插件设置页 |
| `packages/client/ui-trajectory` | `@deepseek-ai/dsh-client-ui-trajectory` | trajectory 展示 |
| `packages/client/ui-workspace` | `@deepseek-ai/dsh-client-ui-workspace` | workspace 选择 |

## 9. Bundle、App 和启动入口

### 9.1 Bundle 组合层

| 文件 | 作用 |
|---|---|
| `packages/bundle/base/cordis.patch.yml` | 每个 profile 的第一层，挂载核心 agent、LLM、工具、权限、持久化、telemetry 等 |
| `packages/bundle/web-app/cordis.patch.yml` | 在 base 上挂载 Web host、API、前端插件 |
| `packages/bundle/headless/cordis.patch.yml` | 在 base 上挂载 one-shot headless runner |

### 9.2 App 入口

| 文件 | 作用 |
|---|---|
| `apps/cli/src/bin.ts` | `dsh` CLI 入口 |
| `apps/cli/src/args.ts` | CLI 参数解析 |
| `apps/cli/src/profile-boot.ts` | profile 加载、bundle patch 叠加、HMR |
| `apps/cli/src/plugin.ts` | `dsh plugin` 管理插件 |
| `apps/cli/src/dump-config.ts` | dump 配置 |
| `apps/web/src/main.ts` | Web 前端入口 |
| `apps/web/vite.config.ts` | Vite 构建配置 |

### 9.3 SDK、ACP、Python Runtime

| 文件/文件夹 | 作用 |
|---|---|
| `packages/sdk/protocol` | JSON-RPC wire protocol |
| `packages/sdk/client` | TypeScript SDK client |
| `packages/sdk/server` | stdio JSON-RPC server |
| `packages/acp/acp` | ACP server |
| `python/sdk` | Python SDK |
| `python/sdk-runtime` | 打包的 runtime |
| `examples/jsonrpc-agent/cordis.yml` | JSON-RPC agent 示例组合 |
| `examples/acp-agent/cordis.yml` | ACP agent 示例组合 |

## 10. 怎么改内容

### 10.1 换模型

如果只是切换 DeepSeek 模型：

```text
Settings -> Models
```

或者改：

```text
$DSH_HOME/settings.yaml
```

例如：

```yaml
llm-deepseek:
  baseURL: https://api.deepseek.com
  models:
    - id: deepseek-v4-flash
    - id: deepseek-v4-pro
```

如果接入新的 OpenAI-compatible provider，使用：

```text
packages/llm/llm-pi-ai
```

或在 Web 的 Models 页面添加 custom provider。

### 10.2 加一个模型适配器

新写一个插件，调用：

```ts
ctx.llm.registerAdapter(['provider-name'], adapter)
```

参考：

```text
packages/llm/llm-deepseek/src/index.ts
docs/cookbook/adding-an-llm-adapter.md
```

### 10.3 加一个工具

新写一个插件，调用：

```ts
ctx.tools.register(defineTool({...}))
```

参考：

```text
packages/core/tools/README.md
packages/fs/tool-fs/src
docs/cookbook/adding-a-tool.md
```

### 10.4 改 Web UI

找到对应 client 包：

```text
packages/client/<feature>/src
```

修改后重新构建：

```powershell
cd C:\Users\jx\Desktop\deepseek-harness-master
pnpm run build
pnpm dsh --profile web --port 3080
```

### 10.5 改权限

主要在这几处：

```text
packages/sandbox/sandbox-policy
packages/interaction/permission-presets
packages/interaction/user-approval
```

默认组合在：

```text
packages/bundle/base/cordis.patch.yml
```

### 10.6 改会话持久化

JSONL：

```text
packages/session/session-persistence-jsonl
```

SQLite：

```text
packages/session/session-persistence-sqlite
packages/session-query/session-query-sqlite
```

### 10.7 临时覆盖某个插件

在：

```text
$DSH_HOME/cordis.patch.yml
```

按 plugin id 覆盖，例如：

```yaml
- id: llm-deepseek
  name: '@deepseek-ai/dsh-llm-deepseek'
  config:
    reasoningEffort: max
```

## 11. 快速搜索命令

找某个 plugin id 在哪：

```powershell
cd C:\Users\jx\Desktop\deepseek-harness-master

rg -n "id: llm-deepseek|tool-bash|subagent|session-persistence" packages apps examples
```

找某个包名：

```powershell
rg -n "@deepseek-ai/dsh-llm-deepseek" packages apps examples
```

看某个插件的完整说明：

```powershell
Get-Content packages\llm\llm-deepseek\README.md
```

## 12. 重要提醒

当前版本是 `0.1.0-rc.5` developer preview，官方明确说明会有破坏兼容性变更。做本地 App 时，优先通过 `cordis.patch.yml`、`settings.yaml` 和新增插件来扩展，不要直接大改 `packages/core/agent-loop`。
