@echo off
echo.
echo ========================================
echo    GitHub Push Helper - Crafted by Yukthesh
echo ========================================
echo.

set /p username="Enter your GitHub username: "
set /p repo_name="Enter repository name (e.g., StreetScan-AI): "

if "%username%"=="" (
    echo Error: Username is required!
    pause
    exit /b 1
)

if "%repo_name%"=="" (
    echo Error: Repository name is required!
    pause
    exit /b 1
)

echo.
echo Repository Details:
echo   Username: %username%
echo   Repository: %repo_name%
echo   Remote URL: https://github.com/%username%/%repo_name%.git
echo.

set /p confirm="Proceed with pushing to GitHub? (y/N): "
if /i not "%confirm%"=="y" (
    echo Push cancelled by user
    pause
    exit /b 0
)

echo.
echo Adding remote repository...
git remote add origin https://github.com/%username%/%repo_name%.git
if errorlevel 1 (
    echo Remote might already exist, updating URL...
    git remote set-url origin https://github.com/%username%/%repo_name%.git
)

echo.
echo Pushing to GitHub...
git push -u origin master

if errorlevel 1 (
    echo.
    echo Failed to push to GitHub. Please check:
    echo 1. Repository exists on GitHub
    echo 2. You have write permissions
    echo 3. Your GitHub credentials are correct
) else (
    echo.
    echo ========================================
    echo    Successfully pushed to GitHub!
    echo ========================================
    echo.
    echo View your repository at: https://github.com/%username%/%repo_name%
    echo.
    echo Your RTSP Vehicle Detection System is now live with Yukthesh branding!
)

pause 