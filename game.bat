CHCP 65001

@echo off
set /p command=请输入构建命令:
if "%command%"=="init" (
    python -m venv pyenv
    call pyenv\\Scripts\\activate.bat
    pip install -r requirements.txt
    pnpm -C gui install
) else if "%command%"=="dev front" (
    pnpm -C gui run dev
) else if "%command%"=="dev back" (
    call pyenv\\Scripts\\activate.bat
    python manage.py runserver 8080
) else if "%command%"=="update requirement" (
    pyenv\\Scripts\\python.exe -m pip freeze > requirements.txt
) else if "%command%"=="db migrate" (
    call pyenv\\Scripts\\activate.bat
    python manage.py migrate
    python manage.py makemigrations
) else (
    echo 未知命令
)

