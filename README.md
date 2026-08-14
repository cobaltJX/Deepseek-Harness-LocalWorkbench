# DSH Local Workbench

A local Windows desktop workbench for DeepSeek Harness.

It combines a WebView2 desktop launcher with a locally built DeepSeek Harness,
and includes small UX and token-saving changes for everyday local coding-agent
workflows.

## Features

- Local WebView2 desktop shell
- Drag-and-drop files and folders from Windows Explorer
- Removable file and folder attachment chips
- Attachments clear automatically after sending
- Folder drops stay as one folder item instead of expanding into individual files
- Lower context-compaction thresholds for long sessions
- Direct access to a locally built harness for custom plugin development

## Project Layout

```text
D:\tools\ds-harness\
  app-v0.1.10\                 # Prebuilt dsh-launcher release used as the desktop shell
  deepseek-harness-master\     # Locally built DeepSeek Harness source
  dsHarness-secondary development\ # Development notes and earlier launcher experiments
```

## Quick Start

Build and run the local harness from source:

```powershell
cd D:\tools\ds-harness\deepseek-harness-master

pnpm install
pnpm run build
pnpm dsh --profile web --port 3080
```

Or run the prebuilt desktop launcher:

```text
D:\tools\ds-harness\app-v0.1.10\DshWeb.exe
```

The default Web UI is available at:

```text
http://127.0.0.1:3080
```

## Local Harness Integration

The prebuilt launcher normally starts DeepSeek Harness through a global `dsh`
command or `npx`. This project changes the launcher scripts to run the local
source checkout instead.

Modified files:

```text
app-v0.1.10\start-dsh.vbs
app-v0.1.10\start-dsh.cmd
```

The launch command is now:

```text
cd /d "D:\tools\ds-harness\deepseek-harness-master" && pnpm dsh --profile web --port 3080
```

## Drag-and-Drop Improvements

Modified file:

```text
packages/client/ui-conversation/src/client/skeleton/InputBar.tsx
```

Changes:

- Native launcher drop events now create visible, removable attachment chips.
- Browser folder drops no longer recursively expand all files into the dialog.
- Folder drops add a single folder summary instead of many separate file attachments.
- Attachment chips are cleared automatically when a message is sent.

## Token Usage Optimization

Modified file:

```text
apps/cli/config/agent-presets/standard/agent.cordis.yml
```

Current defaults:

```yaml
compaction-basic:
  thresholdRatio: 0.7
  retainRatio: 0.12
  maxTokens: 4096

tool-result-pruner:
  thresholdChars: 4096
  headChars: 2048
  tailChars: 768
```

These values trigger compaction earlier, keep less raw history, and trim large
tool results sooner.

## Development Notes

- DeepSeek Harness is currently in developer preview and may introduce
  compatibility-breaking changes.
- The local working directory contains `node_modules` and build artifacts.
  Do not commit those to Git.
- Keep attribution and license notices for the upstream projects.

## Suggested Topics

```text
deepseek
deepseek-harness
agent
coding-agent
webview2
windows
desktop-app
llm
ai-agent
```
