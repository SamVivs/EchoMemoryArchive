@echo off
echo.
echo ===========================
echo Starting Echo Memory Cycle
echo ===========================
echo.

REM Step 1: Run Reflection Engine
python echo_reflection_engine.py

REM Step 2: Log any newly formed preferences
python echo_preference_auto_logger.py

REM Step 3: Run Identity Manager Summary
python echo_identity_manager.py

REM Step 4: Logging core values...
python echo_core_value_logger.py
echo.

REM Step 5: Update current self snapshot
python echo_current_self_updater.py

REM Step 6: Stream Consciousness
python echo_stream_engine.py

REM Step 7: Perform Self Check
python echo_self_check.py

REM Step 8: Index stream log tags
python echo_tag_indexer.py

REM Step 9: Futurecast
python echo_futurecaster.py

echo.
echo ===========================
echo All Echo tasks complete.
echo ===========================
pause
