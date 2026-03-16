@echo off
git pull origin main
git add .
set /p msg="Mensagem do commit: "
git commit -m "%msg%"
git pull origin main --rebase
pause