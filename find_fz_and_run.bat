@echo off
setlocal

REM 设置文件夹路径和通配符模式
set "folder=C:\Users\19508\Desktop\封包"
set "pattern=悟空神辅II*.exe"

REM 输出调试信息
echo Searching in folder: "%folder%"
echo Using pattern: "%pattern%"

REM 遍历匹配的文件
for %%f in ("%folder%\%pattern%") do (
    REM 确保找到的是文件而不是目录
    if exist "%%f" (
        echo Running %%f
        REM 执行匹配的文件
        start "" "%%f"
        REM 退出循环（如果只想运行第一个匹配的文件）
        goto :eof
    )
)

echo No matching files found.
endlocal