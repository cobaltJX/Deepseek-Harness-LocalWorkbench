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

## Assumed Project Layout

The paths below use placeholders. Replace them with your own locations.

```text
<PROJECT_ROOT>\
  launcher\                  # Prebuilt dsh-launcher release used as the desktop shell
  harness\                   # Locally built DeepSeek Harness source
  notes\                     # Optional development notes
```

For example:

```text
<PROJECT_ROOT>      -> C:\Projects\dsh-local-workbench
<LAUNCHER_DIR>      -> <PROJECT_ROOT>\launcher
<HARNESS_DIR>       -> <PROJECT_ROOT>\harness
```

## Prerequisites

Install the following on Windows:

- Node.js 24 or newer
- pnpm
- Microsoft Edge WebView2 Runtime
- A DeepSeek API key

Verify the tools:

```powershell
node --version
pnpm --version
```

## Installation

### 1. Prepare the local harness

Open PowerShell and go to the harness directory:

```powershell
cd <HARNESS_DIR>
```

Install dependencies and build:

```powershell
pnpm install
pnpm run build
```

This creates the built Web frontend and runtime files used by the launcher.

### 2. Configure the launcher to use the local harness

Edit these files in the launcher directory:

```text
<LAUNCHER_DIR>\start-dsh.vbs
<LAUNCHER_DIR>\start-dsh.cmd
```

Replace the harness path with your actual `<HARNESS_DIR>`.

For `start-dsh.vbs`, use a command like:

```text
cd /d "<HARNESS_DIR>" && pnpm dsh --profile web --port 3080
```

For `start-dsh.cmd`, use:

```bat
cd /d "<HARNESS_DIR>"
pnpm dsh --profile web --port 3080
```

### 3. Run the harness manually

To test without the desktop shell:

```powershell
cd <HARNESS_DIR>
pnpm dsh --profile web --port 3080
```

Open:

```text
http://127.0.0.1:3080
```

### 4. Run the desktop launcher

Start:

```text
<LAUNCHER_DIR>\DshWeb.exe
```

The launcher starts the local harness in the background and opens the Web UI in
a WebView2 window.

## First-Time Web UI Setup

1. Open the Web UI.
2. Go to `Settings -> Models`.
3. Enter your DeepSeek API key.
4. Select `deepseek-v4-flash` or another available model.
5. Choose a workspace directory.
6. Start a conversation.

## Using File and Folder Attachments

- Drag a file or folder from Windows Explorer into the Web UI.
- The attachment appears as a removable chip above the input box.
- Click the `x` button to remove an attachment before sending.
- After sending, attachment chips are cleared automatically.
- Dropping a folder keeps it as one folder item. It is not expanded into many
  separate file attachments.

## Stopping the Harness

Close the desktop launcher, or run:

```powershell
Get-NetTCPConnection -LocalPort 3080 -State Listen |
  Select-Object -ExpandProperty OwningProcess |
  ForEach-Object { Stop-Process -Id $_ -Force }
```

## Token Usage Optimization

The default `standard` agent preset has lower context thresholds.

Modified file:

```text
<HARNESS_DIR>\apps\cli\config\agent-presets\standard\agent.cordis.yml
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
- Do not commit `node_modules`, `dist`, `lib`, or other build artifacts to Git.
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
