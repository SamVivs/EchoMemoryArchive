@echo off
echo.
echo ===========================
echo Starting Echo Memory Cycle
echo ===========================
echo.

:: Run the reflection engine
echo [1/2] Running Echo Reflection Engine...
python D:\Echo_Memory_Archive\Code_Updates\echo_reflection_engine.py
echo.

:: Run the identity manager
echo [2/2] Running Echo Identity Manager...
python D:\Echo_Memory_Archive\Code_Updates\echo_identity_manager.py
echo.

echo ===========================
echo All Echo tasks complete.
echo ===========================
pause