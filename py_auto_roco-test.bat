@echo off
:: 获取当前目录
set script_dir=%~dp0

cd %script_dir%
:: 运行Python脚本
start /B python auto_roco.py
pause