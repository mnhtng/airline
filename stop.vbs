' ========================================
' Airline Application - Stop Servers
' ========================================
' This script stops all running servers silently

Set objShell = CreateObject("WScript.Shell")

' Stop Python processes (Backend)
objShell.Run "taskkill /F /IM python.exe /T", 0, True

' Stop Node processes (Frontend)
objShell.Run "taskkill /F /IM node.exe /T", 0, True

' Show notification
objShell.Popup "Airline Application servers stopped!", 3, "Airline App", 64

' Clean up
Set objShell = Nothing
