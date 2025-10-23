$exe = "C:\Users\mainm\Desktop\SecureCast\dist\SecureCast.exe"
$ico = "C:\Users\mainm\Desktop\SecureCast\assets\icon.ico"
$desktop = Join-Path $env:USERPROFILE "Desktop"
$lnk = Join-Path $desktop "SecureCast.lnk"

if (-not (Test-Path $exe)) {
  Write-Host "EXE not found at: $exe"
  exit 1
}

$ws = New-Object -ComObject WScript.Shell
$sc = $ws.CreateShortcut($lnk)
$sc.TargetPath = $exe
$sc.WorkingDirectory = Split-Path $exe
$sc.IconLocation = $ico
$sc.Save()
Write-Host "Shortcut created: $lnk"
