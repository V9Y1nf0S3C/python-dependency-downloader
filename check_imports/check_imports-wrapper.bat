@echo off
REM pip install --no-index --find-links .\a\wheels_offline\requests\ requests
REM pip install --no-index --find-links .\a\wheels_offline\lxml\ lxml
REM pip install --no-index --find-links .\a\wheels_offline\selenium selenium
REM pip install --no-index --find-links .\a\wheels_offline\jsbeautifier jsbeautifier

python check_imports.py check_imports-input.txt
echo =============================================================================
echo                    Task completed. Going to exit
echo =============================================================================
pause >nul
pause >nul
pause >nul
exit /b
