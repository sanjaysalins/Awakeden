' start_watcher.vbs -- starts watcher_service.py with ZERO visible window, not
' even a flash (WScript.Shell.Run's third arg (0) = hidden window style). A
' .bat launcher can't do this: double-clicked, cmd.exe itself shows a console
' for as long as the script runs, even if the program it launches (pythonw.exe)
' has no window of its own. Double-clicking a .vbs runs it under wscript.exe,
' which has no console host at all.
'
' Double-click this to start the watcher. Nothing will visibly happen -- give
' it ~10s then check the Claude Code status line to confirm it's running.
' Safe to double-click more than once: watcher_service.py's own pidfile check
' quietly exits a second instance.
Dim shell, fso, scriptDir
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
shell.Run """" & scriptDir & "\.venv\Scripts\pythonw.exe"" """ & scriptDir & "\watcher_service.py""", 0, False
