# DeepSeek Harness 本地 App 部署可行性评估

仓库位置：[deepseek-harness-master](C:/Users/jx/Desktop/deepseek-harness-master/)

## 结论

可行，而且不建议从零重写 agent。源码本身已经是完整的 agent 运行时，本地 App 的主要工作是：

1. 启动并托管 `dsh` 运行时；
2. 给现有 Web UI 做桌面壳，或通过 SDK 自己实现原生 UI；
3. 管理 DeepSeek 凭据、模型、workspace、会话和进程生命周期；
4. 用 Cordis 插件扩展业务能力，而不是改 agent loop。

当前源码版本是 `0.1.0-rc.5`，README 明确标注 developer preview 和未来会有破坏兼容性的变更。因此建议按“先做桌面壳，再做定制插件，暂不做深度 fork”的路线推进。

## 源码实际结构

这个仓库不是单纯网页版。根目录已经包含：

| 路径 | 作用 |
|---|---|
| `apps/cli` | `dsh` CLI，启动 profile，支持 web、headless、plugin、dump-config |
| `apps/web` | Vite 构建的 Web 前端，产出 `dist/` |
| `packages/core/*` | agent、agent-loop、session、tools、system-prompt |
| `packages/llm/*` | LLM 抽象、DeepSeek 官方适配器、多 provider 适配器 |
| `packages/bundle/*` | `dsh-base`、`dsh-web-app`、`dsh-headless` 组合层 |
| `packages/api/*` | Web Host 的 Typert RPC gateway 和 remote API |
| `packages/sdk/*` | TypeScript JSON-RPC SDK |
| `packages/subagent` 等 | subagent、workflow、goal、plan、todo、skill、MCP、web、filesystem、shell、compaction |
| `python/` | Python SDK 和打包的 runtime |
| `native/landlock-run` | Linux landlock 原生沙箱 |

根 README 给出了两个入口：

- `npx @deepseek-ai/dsh web`：启动本地 Web UI，默认 `http://127.0.0.1:3080`。
- `dsh --profile headless "task"`：无 UI 的一次性 agent 任务。

同时 CLI 还有 `--dump-config`、`plugin` 等模式。说明官方已经提供本地部署能力，不只是网页版。

## 关键机制

### 1. Cordis 插件树

`dsh` 通过 profile、bundle、patch 层组装插件树。`dsh-base` 是第一层，负责模型适配器、工具、持久化、沙箱、权限、settings、credentials、telemetry 和 subagent provider。`dsh-web-app` 在 `dsh-base` 之上加入 Web server、API gateway、前端静态资源和浏览器插件。

这意味着本地 App 可以：

- 使用默认 `web` profile，直接得到完整 UI 和 agent；
- 用 `$DSH_HOME/cordis.patch.yml` 或 `--patch` 覆盖模型、工具、权限、持久化；
- 新增自定义插件注册工具、模型适配器或事件监听器。

### 2. Agent 架构是现成的

`dsh-agent-loop` 是唯一包含具体 loop 逻辑的包，负责 session/turn/step 生命周期、模型请求、工具调用、取消和恢复。其他功能都挂在事件或服务扩展点上。

核心链路是：

```text
turn/start
  -> agent/pre-step
  -> step/start
  -> agent/request
  -> llm/stream
  -> assistant/message
  -> tool/call
  -> tools/pre-execute -> tools/execute -> tools/post-execute -> tool/result
  -> step/end
  -> agent/turn-stopping
turn/end
```

Session 是 append-only 的 durable event log，模型上下文、回放、持久化、UI、telemetry 都从 session log 投影出来。

### 3. DeepSeek 接入已经内置

`@deepseek-ai/dsh-llm-deepseek` 是 DeepSeek 官方 chat-completions 适配器，provider route 为 `deepseek-official`。配置支持：

- `DEEPSEEK_API_KEY`
- `DEEPSEEK_BASE_URL`
- `thinking`
- `reasoningEffort`
- `maxTokens`
- `models`
- `retryPolicy`

默认模型是 `deepseek-v4-flash` 和 `deepseek-v4-pro`，但 model id 是 pass-through，可接入公司网关或私有 endpoint。

另外 `@deepseek-ai/dsh-llm-pi-ai` 支持 OpenAI-compatible custom provider、自建服务、企业 gateway。Web UI 的 Settings 页面也支持填写自定义 provider 的 base URL、API protocol 和模型列表。

所以“接入 DeepSeek”不需要改源码，只需要：

1. 设置 API key；
2. 选择或配置 provider/model；
3. 选择 workspace；
4. 可选配置沙箱、权限和持久化。

### 4. 本地进程接口

源码提供三层调用方式：

| 接口 | 适用场景 |
|---|---|
| `dsh web` 本地 HTTP/WebSocket | 桌面壳内嵌现有 Web UI |
| TypeScript/Python JSON-RPC SDK | 自研 UI 或后台 agent 服务 |
| ACP、headless | 编辑器、自动化、一次性任务 |

Python SDK 的 bundled runtime 当前只发布 Linux x64/arm64 和 macOS arm64 wheel。Windows 上需要系统 Node.js 运行源码或自行打包 runtime，这是原生 Python SDK 路线的主要限制。

## 本地 App 方案

### 方案 A：Electron/Tauri 壳 + 现有 Web UI

推荐作为第一版。

```text
Desktop App
  -> spawn dsh web --host 127.0.0.1 --port <random>
  -> wait for URL
  -> load http://127.0.0.1:<port>
  -> manage start/stop/logs/upgrade
```

优点：

- 工作量最小；
- Web UI、agent loop、工具、会话、权限、模型配置全部继承；
- 适合快速做出可用的本地桌面产品。

注意：

- Web server 明确没有 TLS、auth 和 origin policy，因此 App 必须只绑定 loopback，不要把 `0.0.0.0` 暴露到局域网；
- API key 由 harness 写入 `$DSH_HOME/.credentials.yaml`，桌面壳可以在外层再用系统 keychain 做一道保护；
- 需要管理 `dsh` 子进程的启动失败、端口占用、退出和自动重启。

### 方案 B：自定义原生 UI + JSON-RPC SDK

适合想要更深度产品控制、不想直接暴露 Web UI 的场景。

```text
Native App
  -> DeepSeekHarness / HarnessClient
  -> initialize
  -> session/prompt
  -> consume session.event / session.status / subagent events
```

优点：

- UI 完全自研；
- 可以封装成后台服务、CLI 或内部平台；
- SDK 已提供 `initialize`、`session/prompt`、`shutdown` 以及 session/subagent 事件流。

缺点：

- 需要自己实现会话流、工具卡、审批、取消、错误处理和交互体验；
- JSON-RPC 协议目前没有 per-session close 或 prompt-cancel，取消能力要通过关闭 runtime 或更上层 API；
- Windows 下 Python runtime 没有生产 wheel，需要依赖 Node runtime 或自行打包 executable。

### 方案 C：混合架构

推荐最终形态：

```text
Desktop App
  - 内嵌 dsh web 作为主 UI
  - 同时启动受控 JSON-RPC/ACP/MCP 端点
  - 提供 App 级 settings、workspace、任务历史、凭据和插件管理
```

这样既有成熟 UI，又能对 agent 做程序化调度和扩展。

## 完整 Agent 架构映射

以下能力已经在源码中存在，本地 App 只需要按需挂载：

| 能力 | 对应包/入口 |
|---|---|
| Agent loop | `packages/core/agent-loop` |
| Session 持久化 | `packages/session/session-persistence-jsonl`、`session-persistence-sqlite` |
| 工具执行管道 | `packages/core/tools` |
| 文件系统 | `packages/fs/*` |
| Shell | `packages/shell/*` |
| 子 Agent | `packages/subagent/*` |
| 工作流 | `packages/workflow/*` |
| Goal/Plan/Todo | `packages/goal`、`packages/plan`、`packages/todo` |
| Skill | `packages/skill/*` |
| Web search/fetch | `packages/web/*` |
| MCP | `packages/mcp-client` |
| 上下文压缩 | `packages/compaction/*` |
| DeepSeek 模型 | `packages/llm/llm-deepseek` |
| 通用 OpenAI-compatible provider | `packages/llm/llm-pi-ai` |
| Web API/UI | `packages/api/*`、`packages/host/*`、`apps/web` |

## 建议的落地顺序

### Phase 0：先验证 runtime

- 安装或核对 Node 22.19+/24；
- 运行 `pnpm install && pnpm run build`；
- 运行 `pnpm dsh web`；
- 在 Web UI 配置 DeepSeek API key、模型和 workspace；
- 跑一个真实任务，确认工具、权限、会话持久化都正常。

### Phase 1：做桌面壳 PoC

- 用 Electron 或 Tauri 启动 `dsh web`；
- 自动选择空闲端口；
- 监听 stdout 中的 URL，加载到 WebView；
- 处理退出、日志、崩溃重启、首次 onboarding。

### Phase 2：做 App 级管理

- 将 API key 放入系统 keychain；
- 创建自定义 `cordis.patch.yml` 或 profile；
- 管理 workspace、模型默认值、权限策略；
- 选择 JSONL 或 SQLite 持久化。

### Phase 3：扩展业务能力

- 增加自定义 tool；
- 增加企业 provider；
- 通过 MCP/ACP/JSON-RPC 接入现有系统；
- 做任务队列、历史检索和审计。

### Phase 4：打包和升级

- 打包内置 Node runtime 或 `dsh` executable；
- 跟随上游版本升级；
- 为 session 格式和 credentials 做迁移/备份策略。

## 主要风险

1. **developer preview 风险**：`0.1.0-rc.5`，明确声明会有破坏兼容性变更，不建议深度 fork 后长期脱离上游。
2. **Web 服务无鉴权**：只能本地 loopback 使用；做远程访问需要自建认证和 TLS 层。
3. **Windows 差异**：Web/CLI 走 PowerShell 和 Windows ACL sandbox；Python bundled runtime 没有 Windows wheel；POSIX 的 bash/PTY 组合不能直接照搬。
4. **当前环境未构建**：目录没有 `node_modules`，本次没有执行 `pnpm install/build`。本机 Node 是 `24.16.0`，满足运行要求；pnpm 是 `11.16.0`，仓库指定 `11.7.0`，构建前最好核对 lockfile 和 packageManager。
5. **Session 格式无兼容承诺**：AGENTS.md 说明 SQLite 使用单调 `SCHEMA_VERSION`，session format 当前为 `0` 且不承诺兼容。

## 总体判断

| 指标 | 判断 |
|---|---|
| 技术可行性 | 高 |
| DeepSeek 接入成本 | 低 |
| 首版本地桌面 App 成本 | 中低，优先用 Web UI 壳 |
| 自研原生 UI 成本 | 中高 |
| 完整 agent 架构复用 | 高 |
| 生产稳定性风险 | 中，因为 developer preview |

推荐：先做 **方案 A + 方案 C 的混合形态**，以 `dsh web` 为内核，桌面壳负责宿主生命周期和凭据管理，后续再按需加 JSON-RPC、MCP/ACP 或自定义插件。
