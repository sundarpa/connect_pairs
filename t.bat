@echo off

REM Check if arguments are provided
if "%~1"=="" (
    echo No arguments provided. Exiting...
    exit /b
)

REM Call the VBScript file with the provided arguments
cscript "C:\SearchTool\t.vbs" %*
