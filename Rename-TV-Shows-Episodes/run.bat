@echo off
for %%x in (%cd%) do title %%~nx
call conda activate
python run.py
pause