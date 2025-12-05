@echo off
set "CMD_DIR=%~dp0"

echo Lancement de la commande pygbag dans un nouveau CMD...
x
start "Pygbag Console" cmd /k "cd /d "%CMD_DIR%" && pygbag.exe --template index.tmpl --can_close 1 --app_name InfiniteDistro --title InfiniteDistro --icon ./src/img/favicon.png ./src"