$ErrorActionPreference = "Stop"

$scriptContent = @'
$file = "C:\Users\changhaoyan\Desktop\template.docx"
$wordPath = "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE"

Write-Host "Starting Word..."
$p = Start-Process -FilePath $wordPath -ArgumentList "/q `"$file`"" -PassThru
Start-Sleep -Seconds 8

if ($p.HasExited) {
    Write-Host "Word exited early: $($p.ExitCode)"
    exit 1
}

Write-Host "Word is running, PID: $($p.Id)"

$wsh = New-Object -ComObject WScript.Shell
Start-Sleep -Seconds 3

$activated = $wsh.AppActivate($p.Id)
Write-Host "AppActivate by PID: $activated"

if (-not $activated) {
    $activated = $wsh.AppActivate("Word")
    Write-Host "AppActivate by name: $activated"
}

Start-Sleep -Seconds 2

if ($activated) {
    Write-Host "Sending Ctrl+P..."
    $wsh.SendKeys("^p")
    Start-Sleep -Seconds 2
    $wsh.SendKeys("{ENTER}")
    Write-Host "Print command sent"
    Start-Sleep -Seconds 5
} else {
    Write-Host "Could not activate Word window"
}

$wsh.SendKeys("%{F4}")
Start-Sleep -Seconds 2

if (!$p.HasExited) {
    $p.Kill()
}

Write-Host "Done"
'@

$scriptPath = "C:\Users\changhaoyan\Desktop\scripts\pt.ps1"
$scriptContent | Out-File -FilePath $scriptPath -Encoding ASCII
Write-Host "Script saved to: $scriptPath"

# Use schtasks to run the script in user's interactive session
$taskName = "PrintDoc_$(Get-Random)"

# Create task that runs as the current user in interactive session
$create = schtasks /create /tn $taskName /tr "powershell.exe -ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$scriptPath`"" /sc once /st (Get-Date).ToString("HH:mm") /ru $env:USERNAME /rp /f 2>&1
Write-Host "Create result: $create"

# Run immediately
$run = schtasks /run /tn $taskName 2>&1
Write-Host "Run result: $run"

# Wait for execution
Start-Sleep -Seconds 15

# Check task
$query = schtasks /query /tn $taskName /fo CSV /v 2>&1 | ConvertFrom-Csv | Select-Object "Last Result", "Last Run Time"
Write-Host "Task result: $($query.'Last Result')"

# Cleanup
schtasks /delete /tn $taskName /f 2>&1 | Out-Null
Remove-Item $scriptPath -Force -ErrorAction SilentlyContinue
Write-Host "Done"
