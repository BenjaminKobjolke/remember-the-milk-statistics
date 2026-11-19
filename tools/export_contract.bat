@echo off
REM Writes the snapshots table definition into contract\schema.json (git submodule).
pushd "%~dp0.."
if not exist contract\schema.json (
    echo ERROR: contract\ submodule missing. Run: git submodule update --init contract
    popd
    exit /b 1
)
uv run python -m rtm_statistics.contract
set RESULT=%ERRORLEVEL%
popd
exit /b %RESULT%
