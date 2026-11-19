@echo off
echo ========================================
echo  RTM Statistics - Initial Setup
echo ========================================
echo.

:: Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    echo Please install uv first: https://docs.astral.sh/uv/getting-started/installation/
    exit /b 1
)

echo [1/2] Creating virtual environment and installing dependencies...
uv sync --all-extras
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to sync dependencies
    exit /b 1
)

echo.
echo [2/2] Running tests...
if defined TICKETS_WATCHER_COMMAND_RUN (
    uv run pytest tests/ -v
) else (
    uv run pytest tests/ -q
)
set TESTRESULT=%ERRORLEVEL%
if %TESTRESULT% neq 0 (
    echo WARNING: Some tests failed
)

echo.
echo ========================================
echo  Setup complete!
echo ========================================
echo.
exit /b %TESTRESULT%
