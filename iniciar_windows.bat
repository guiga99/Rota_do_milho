@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  py -3.12 -m venv .venv
  if errorlevel 1 goto erro
)
.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
if errorlevel 1 goto erro
.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --browser.gatherUsageStats false
exit /b %errorlevel%
:erro
echo Falha na preparacao. Verifique Python 3.12 e acesso ao registro de pacotes.
pause
exit /b 1
