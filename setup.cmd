@echo off
echo 证书生成服务 - 环境设置

REM 检查 Python 3.9 是否可用
py -3.9 --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python 3.9 未找到，请确保已安装Python 3.9
    echo 可访问 https://www.python.org/downloads/release/python-3913/ 下载安装
    pause
    exit /b 1
)

echo 找到 Python 3.9，开始安装依赖...

REM 安装所有依赖
py -3.9 -m pip install -r requirements.txt

REM 生成证书模板
py -3.9 templates/certificate_template.py

echo 环境设置完成！
echo 可以通过运行 start_service.cmd 启动服务
pause 