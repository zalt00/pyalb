call %~dp0\venv\Scripts\activate.bat
set "PYTHONPATH=%~dp0;%PYTHONPATH"
C:\Users\Timelam\git\pyalb\pyalb\src\Platformer\venv\Scripts\python.exe %~dp0\Scripts\level_reader.py %~dp0 %1
call %~dp0\venv\Scripts\deactivate.bat
