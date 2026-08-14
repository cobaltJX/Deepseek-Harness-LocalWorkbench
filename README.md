# DSH Local Workbench

A local Windows desktop workbench for DeepSeek Harness.

It combines two projects:

- DeepSeek Harness: the local agent runtime.
- dsh-launcher: a WebView2 desktop launcher for Windows.

This README is written for first-time users who have not worked with Node.js,
pnpm, or DeepSeek Harness before. Follow the steps in order.

## 1. Requirements

System:

- Windows 10 or Windows 11, 64-bit.
- A DeepSeek API key.

Software:

- Node.js 24 or newer.
- pnpm.
- Microsoft Edge WebView2 Runtime.

## 2. Install Node.js

Open this URL:

```text
https://nodejs.org/
```

Download the Windows 64-bit LTS installer. Use Node.js 24 or newer.

During installation:

1. Double-click the downloaded `.msi` file.
2. Follow the installer steps.
3. If the installer offers `Add to PATH`, make sure it is selected.
4. After installation, close every PowerShell window and open a new one.

Verify:

```powershell
node --version
npm --version
```

If both commands print version numbers, Node.js is installed correctly.

## 3. Install pnpm

Run:

```powershell
npm install -g pnpm@11.7.0
```

If you get a permission error, open PowerShell as Administrator and run the
same command again.

Verify:

```powershell
pnpm --version
```

It should print:

```text
11.7.0
```

## 4. Install WebView2 Runtime

Most Windows 10 and Windows 11 systems already include WebView2 Runtime.

If `DshWeb.exe` reports that WebView2 is missing, download it from:

```text
https://developer.microsoft.com/microsoft-edge/webview2/
```

Install the Evergreen Runtime or Evergreen Bootstrapper.

## 5. Project Layout

The published project normally looks like this:

```text
DSH-Local-Workbench-Publish\
  README.md
  .gitignore
  NOTICE.md
  harness\               # DeepSeek Harness source
  launcher-source\       # dsh-launcher source for rebuilding the shell
  launcher-bin\          # Prebuilt desktop launcher
  docs\                  # Plugin map and feasibility notes
```

Two important placeholders:

- `<HARNESS_DIR>`: the local harness directory, for example
  `C:\DSH-Local-Workbench-Publish\harness`.
- `<LAUNCHER_DIR>`: the desktop launcher directory, for example
  `C:\DSH-Local-Workbench-Publish\launcher-bin`.

The rest of this README uses these placeholders.

## 6. Build The Local Harness

Open PowerShell:

```powershell
cd <HARNESS_DIR>
```

Install dependencies:

```powershell
pnpm install
```

If downloads are slow, use the npm mirror:

```powershell
pnpm config set registry https://registry.npmmirror.com
pnpm install
```

Build:

```powershell
pnpm run build
```

This creates the built Web frontend and runtime files.

## 7. Configure The Launcher Path

The launcher scripts use a placeholder:

```text
<HARNESS_DIR>
```

Replace it with your actual harness directory.

Files to update:

```text
<LAUNCHER_DIR>\start-dsh.vbs
<LAUNCHER_DIR>\start-dsh.cmd
```

You can replace the placeholder with PowerShell.

First enter the project root:

```powershell
cd <PROJECT_ROOT>
```

Assume your actual harness directory is:

```text
C:\DSH-Local-Workbench-Publish\harness
```

Run:

```powershell
$harnessDir = 'C:\DSH-Local-Workbench-Publish\harness'

$cmd = Join-Path (Get-Location) 'launcher-bin\start-dsh.cmd'
$vbs = Join-Path (Get-Location) 'launcher-bin\start-dsh.vbs'

(Get-Content $cmd) -replace '<HARNESS_DIR>', $harnessDir | Set-Content $cmd -Encoding ASCII
(Get-Content $vbs) -replace '<HARNESS_DIR>', $harnessDir | Set-Content $vbs -Encoding ASCII
```

Open both files afterward and verify that the placeholder is replaced with your
actual path.

## 8. Configure The DeepSeek API Key

There are two options.

### Option A: Configure in the Web UI

After starting the app, open:

```text
Settings -> Models
```

Enter your DeepSeek API key and save it.

### Option B: Use an Environment Variable

Run:

```powershell
$env:DEEPSEEK_API_KEY="sk-your-key"
```

This only affects the current PowerShell window.

## 9. Start The Project

### Option A: Start the harness manually

```powershell
cd <HARNESS_DIR>

pnpm dsh --profile web --port 3080
```

When the server is ready, you should see:

```text
dsh web: http://127.0.0.1:3080
```

Open:

```text
http://127.0.0.1:3080
```

### Option B: Start the desktop launcher

Open:

```text
<LAUNCHER_DIR>\DshWeb.exe
```

The launcher starts the local harness in the background and opens the Web UI in
a WebView2 window.

## 10. First-Time Web UI Setup

1. Open the Web UI.
2. Go to `Settings -> Models`.
3. Enter your DeepSeek API key.
4. Select a model, for example `deepseek-v4-flash`.
5. Choose a workspace directory.
6. Start a conversation.

## 11. Stop The Service

If you started the desktop launcher, close the window.

If you started the service from the command line, press `Ctrl+C`.

You can also run:

```powershell
Get-NetTCPConnection -LocalPort 3080 -State Listen |
  Select-Object -ExpandProperty OwningProcess |
  ForEach-Object { Stop-Process -Id $_ -Force }
```

## 12. Troubleshooting

### `node` is not recognized

Possible causes:

1. Node.js is not installed.
2. Node.js was not added to PATH.
3. The current PowerShell window was opened before Node.js was installed.

Fix:

1. Reinstall Node.js and make sure `Add to PATH` is selected.
2. Close all PowerShell windows.
3. Open a new PowerShell window.
4. Run:

```powershell
node --version
```

### `pnpm` is not recognized

Install pnpm:

```powershell
npm install -g pnpm@11.7.0
```

Open a new PowerShell window and verify:

```powershell
pnpm --version
```

If it is still missing, make sure the user PATH contains:

```text
C:\Users\<your-user-name>\AppData\Roaming\npm
```

### Port 3080 is already in use

Stop the process using the port:

```powershell
Get-NetTCPConnection -LocalPort 3080 -State Listen |
  Select-Object -ExpandProperty OwningProcess |
  ForEach-Object { Stop-Process -Id $_ -Force }
```

Or use a different port:

```powershell
pnpm dsh --profile web --port 3081
```

### `pnpm install` times out

Increase the timeout and lower concurrency:

```powershell
pnpm config set fetch-timeout 600000
pnpm config set fetch-retries 5
pnpm config set fetch-retry-maxtimeout 120000
pnpm config set network-concurrency 2
pnpm config set registry https://registry.npmmirror.com
```

Then run:

```powershell
pnpm install
```

### DshWeb.exe cannot find the service

Check both launcher scripts:

```text
launcher-bin\start-dsh.vbs
launcher-bin\start-dsh.cmd
```

Make sure the `<HARNESS_DIR>` placeholder has been replaced with your actual
harness directory.

## 13. Customizations In This Project

This project is not a plain copy of the upstream projects. It includes:

1. A desktop launcher that points to the local harness instead of a global
   `dsh` command or npx.
2. Removable file and folder attachment chips for drag-and-drop from Windows
   Explorer.
3. Folder drops kept as one folder item instead of being expanded into many
   files.
4. Automatic clearing of attachment chips after sending a message.
5. Lower context-compaction and tool-result-pruning thresholds to reduce token
   usage in long sessions.

## 14. Suggested GitHub Topics

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
