@echo off
title Push Project to GitHub (janhavibodakhe2811-del)
echo ====================================================
echo Pushing AI Software Engineer Assistant to GitHub...
echo Repository: https://github.com/janhavibodakhe2811-del/AI--Software-Assistant
echo ====================================================
echo.
echo If prompted by Git, sign in with your GitHub account: janhavibodakhe2811-del
echo.
cd /d "%~dp0ai-software-assistant"
git push -u origin main --force
echo.
if %ERRORLEVEL% equ 0 (
    echo ====================================================
    echo SUCCESS! Your project is now live on GitHub:
    echo https://github.com/janhavibodakhe2811-del/AI--Software-Assistant
    echo ====================================================
) else (
    echo ====================================================
    echo If authentication failed, you can also push using a Personal Access Token (PAT):
    echo git remote set-url origin https://<YOUR_TOKEN>@github.com/janhavibodakhe2811-del/AI--Software-Assistant.git
    echo git push -u origin main --force
    echo ====================================================
)
pause
