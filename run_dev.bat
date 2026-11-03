@echo off
title SAARTHI Runner
echo Starting SAARTHI Platform...
powershell -ExecutionPolicy Bypass -File "%~dp0scripts\run_dev.ps1"
pause
