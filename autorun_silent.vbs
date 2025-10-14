' ========================================
' Airline Application - Silent Launcher
' ========================================
' This script runs servers completely silently
' No windows, no popups - just starts the servers

Set objShell = CreateObject("WScript.Shell")

' Get the directory where this script is located
strScriptPath = WScript.ScriptFullName
strScriptDir = Left(strScriptPath, InStrRev(strScriptPath, "\"))

' Backend directory and command
strBackendDir = strScriptDir & "backend"
strBackendCmd = "cmd /c cd /d """ & strBackendDir & """ && .venv\Scripts\activate && fastapi dev main.py"

' Frontend directory and command
strFrontendDir = strScriptDir & "frontend"
strFrontendCmd = "cmd /c cd /d """ & strFrontendDir & """ && npm run dev"

' Run backend hidden (0 = hidden window, False = don't wait)
objShell.Run strBackendCmd, 0, False

' Run frontend hidden
objShell.Run strFrontendCmd, 0, False

' Wait 200 milliseconds for frontend to start
WScript.Sleep 200

' Open frontend in default browser
objShell.Run "http://localhost:5173", 1, False

' Clean up
Set objShell = Nothing
