@echo off
chcp 65001 >nul
title OpenClash 配置生成器

echo.
echo ========================================
echo    OpenClash 配置生成器
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未检测到Python，请先安装Python
    echo.
    echo 📥 下载地址: https://www.python.org/downloads/
    echo 💡 安装时请勾选 "Add Python to PATH"
    echo.
    pause
    exit /b 1
)

echo ✅ Python 环境检测通过
echo.

REM 检查依赖是否安装
python -c "import requests, yaml, flask" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 正在安装依赖包...
    python -m pip install --upgrade pip
    python -m pip install requests pyyaml flask click colorama tqdm
    if %errorlevel% neq 0 (
        echo ❌ 依赖安装失败，尝试使用国内镜像...
        python -m pip install requests pyyaml flask click colorama tqdm -i https://pypi.tuna.tsinghua.edu.cn/simple/
    )
)

echo ✅ 依赖检查完成
echo.

:menu
echo 请选择运行模式:
echo 1. Web界面 (推荐)
echo 2. 交互式命令行
echo 3. 运行测试
echo 4. 退出
echo.
set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" goto web
if "%choice%"=="2" goto interactive
if "%choice%"=="3" goto test
if "%choice%"=="4" goto exit
echo 无效选择，请重新输入
goto menu

:web
echo.
echo 🌐 启动Web界面...
echo 📱 请在浏览器中访问: http://localhost:5000
echo ⏹️  按 Ctrl+C 停止服务
echo.
python web_interface.py
goto menu

:interactive
echo.
echo 💻 启动交互式命令行...
echo.
python openclash_generator.py --interactive
goto menu

:test
echo.
echo 🧪 运行测试...
echo.
python test_generator.py
echo.
pause
goto menu

:exit
echo.
echo 👋 再见!
pause
exit /b 0