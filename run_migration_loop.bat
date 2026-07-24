@echo off
:loop
echo Starting migration...
venv\Scripts\python.exe ml\data_processing\migrate_to_db.py
if %errorlevel% neq 0 (
    echo Migration encountered an error (likely a network disconnect). Retrying in 5 seconds...
    timeout /t 5 /nobreak
    goto loop
)
echo Migration finished successfully! Starting model training...
venv\Scripts\python.exe ml\models\train_model.py
if %errorlevel% neq 0 (
    echo Model training failed.
    exit /b %errorlevel%
)
echo Entire pipeline completed successfully!
