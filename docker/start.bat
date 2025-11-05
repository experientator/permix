@echo off
echo ================================
echo  DOCKER BUILD STARTED
echo ================================

:: Build the image
docker build -t tkinter-app .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Docker build failed!
    pause
    exit /b 1
)

echo.
echo ================================
echo  BUILD SUCCESSFUL
echo  Starting application...
echo ================================
echo.

:: Run the container
docker run -it --rm ^
    -e DISPLAY=host.docker.internal:0 ^
    -v "%cd%":/app ^
    tkinter-app

echo.
echo Application closed.
pause