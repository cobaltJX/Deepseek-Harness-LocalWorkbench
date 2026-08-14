@echo off
rem Manual foreground start of dsh service (debug use; normally use dsh-web.cmd)
title DeepSeek Harness Server
cd /d "<HARNESS_DIR>"
pnpm dsh --profile web --port 3080
if errorlevel 1 (
  echo.
  echo [ERROR] dsh failed to start. Install globally with: npm install -g @deepseek-ai/dsh
  echo Log: %USERPROFILE%\.dsh-web.log
  pause
)
