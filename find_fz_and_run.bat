@echo off
setlocal

REM �����ļ���·����ͨ���ģʽ
set "folder=C:\Users\19508\Desktop\���"
set "pattern=�����II*.exe"

REM ���������Ϣ
echo Searching in folder: "%folder%"
echo Using pattern: "%pattern%"

REM ����ƥ����ļ�
for %%f in ("%folder%\%pattern%") do (
    REM ȷ���ҵ������ļ�������Ŀ¼
    if exist "%%f" (
        echo Running %%f
        REM ִ��ƥ����ļ�
        start "" "%%f"
        REM �˳�ѭ�������ֻ�����е�һ��ƥ����ļ���
        goto :eof
    )
)

echo No matching files found.
endlocal