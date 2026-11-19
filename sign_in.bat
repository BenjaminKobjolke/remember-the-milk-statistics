@echo off
REM Opens the RTM authorization page and stores the token in settings.ini.
pushd "%~dp0"
uv run python -m rtm_statistics --auth-only
set RESULT=%ERRORLEVEL%
popd
exit /b %RESULT%
