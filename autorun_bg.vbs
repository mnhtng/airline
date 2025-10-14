' ========================================
' Airline Application - Background Launcher
' ========================================
' This script runs servers silently in the background
' Double-click this file to start both servers without showing terminal windows

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

' Show a notification that servers are starting
objShell.Popup "Airline Application Started!" & vbCrLf & vbCrLf & _
               "Backend: http://localhost:8000" & vbCrLf & _
               "Frontend: http://localhost:5173" & vbCrLf & _
               "API Docs: http://localhost:8000/docs" & vbCrLf & vbCrLf & _
               "Browser opened automatically!", _
               5, "Airline App", 64

' Clean up
Set objShell = Nothing
