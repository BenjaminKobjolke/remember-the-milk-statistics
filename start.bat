@echo off
REM Takes one snapshot of the configured smart list. Schedule this in Windows Task Scheduler.
pushd "%~dp0"
uv run python -m rtm_statistics
set RESULT=%ERRORLEVEL%
popd
exit /b %RESULT%
