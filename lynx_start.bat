@echo off
TITLE lynx
rem This next line removes any fban csv files if they exist in root when bot restarts. 
del *.csv
py -3.10 --version
IF "%ERRORLEVEL%" == "0" (
    py -3.10 -m lsf
) ELSE (
    py -m lsf
)
