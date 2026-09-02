' Sosyal İmece Orchestrator API - Windows Background Service
' Bu script, komut penceresi açmadan API'yi arka planda çalıştırır

Option Explicit

Dim objShell, objFSO, scriptPath, projectPath, pythonPath, venvPath, command
Dim logFile, logPath

' Proje dizini (otomatik tespit)
Set objFSO = CreateObject("Scripting.FileSystemObject")
scriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)
projectPath = objFSO.GetParentFolderName(scriptPath)

' Log dosyası yolu
logPath = projectPath & "\orchestrator_service.log"

' Python sanal ortam yolu (varsa)
venvPath = projectPath & "\venv\Scripts\python.exe"

' Sistem Python yolu (fallback)
pythonPath = "python.exe"

' Kullanılacak Python yolunu belirle
If objFSO.FileExists(venvPath) Then
    pythonPath = venvPath
End If

' Çalıştırılacak komut
command = """" & pythonPath & """ """ & projectPath & "\orchestrator_api.py"""

' Shell nesnesi oluştur
Set objShell = CreateObject("WScript.Shell")

' Log dosyasına başlangıç zamanı yaz
Set logFile = objFSO.OpenTextFile(logPath, 8, True)
logFile.WriteLine "=========================================="
logFile.WriteLine "Sosyal İmece Service Başlatıldı: " & Now()
logFile.WriteLine "Python Yolu: " & pythonPath
logFile.WriteLine "Komut: " & command
logFile.Close

' Komutu arka planda çalıştır (WindowStyle = 0)
objShell.Run command, 0, False

' Temizlik
Set objShell = Nothing
Set objFSO = Nothing

WScript.Echo "Sosyal İmece API arka planda başlatıldı."
