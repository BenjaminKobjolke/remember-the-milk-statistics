@echo off
echo ========================================
echo  RTM Statistics - Update Libraries
echo ========================================
echo.

:: Check if uv is installed
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv is not installed or not in PATH
    echo Please install uv first: https://docs.astral.sh/uv/getting-started/installation/
    exit /b 1
)

echo [1/4] Updating all dependencies to latest versions...
uv lock --upgrade
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to update lock file
    exit /b 1
)

echo.
echo [2/4] Syncing updated dependencies...
uv sync --all-extras
if %ERRORLEVEL% neq 0 (
    echo ERROR: Failed to sync dependencies
    exit /b 1
)

echo.
echo [3/4] Running linting checks...
uv run ruff check src/ tests/
set QUALITYRESULT=%ERRORLEVEL%
if %QUALITYRESULT% neq 0 (
    echo WARNING: Linting issues found
)

uv run mypy src/
set MYRESULT=%ERRORLEVEL%
if %MYRESULT% neq 0 set QUALITYRESULT=1
if %MYRESULT% neq 0 (
    echo WARNING: Type checking issues found
)

echo.
echo [4/4] Running tests...
if defined TICKETS_WATCHER_COMMAND_RUN (
    uv run pytest tests/ -v
) else (
    uv run pytest tests/ -q
)
set TESTRESULT=%ERRORLEVEL%
if %TESTRESULT% neq 0 (
    echo WARNING: Some tests failed after update
    echo You may need to fix compatibility issues
)

echo.
echo ========================================
echo  Update complete!
echo ========================================
echo.
echo Updated packages are now in uv.lock
echo Remember to commit uv.lock if everything works correctly
echo.
if %TESTRESULT% neq 0 exit /b %TESTRESULT%
if %QUALITYRESULT% neq 0 exit /b %QUALITYRESULT%
exit /b 0
