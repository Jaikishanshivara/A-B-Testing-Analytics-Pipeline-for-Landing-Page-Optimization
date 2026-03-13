@echo off
cd /d "D:\Projects\AB Testing"

echo Starting AB Testing Pipeline...
"C:\Users\Jaikishan\AppData\Local\Programs\Python\Python310\python.exe" pipeline\elt_pipeline.py

echo Pipeline Finished