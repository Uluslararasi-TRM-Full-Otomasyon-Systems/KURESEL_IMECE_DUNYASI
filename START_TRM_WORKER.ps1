$projectRoot = "C:\Users\Habitat\Desktop\SOSYAL İMECE"
$pythonwCmd = Get-Command pythonw -ErrorAction SilentlyContinue
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if ($pythonwCmd) {
    $pythonExe = $pythonwCmd.Source
} elseif ($pythonCmd) {
    $pythonExe = $pythonCmd.Source
} else {
    throw "Python bulunamadi."
}

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

Start-Process -FilePath $pythonExe `
    -ArgumentList "`"$projectRoot\trm_worker.py`" run" `
    -WorkingDirectory $projectRoot `
    -WindowStyle Hidden
