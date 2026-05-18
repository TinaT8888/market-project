@echo off
cd /d C:\Users\tinat\OneDrive\Desktop\market-project

python src\ingest.py
python src\transform.py

echo Pipeline completed.
pause

