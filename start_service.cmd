@echo off
echo 正在启动证书生成服务...

REM 使用Python 3.9启动服务
py -3.9 -m uvicorn main:app --reload

REM 如果发生错误，暂停以便用户查看错误信息
if %ERRORLEVEL% NEQ 0 (
    echo 启动服务失败，请检查错误信息
    pause
) 