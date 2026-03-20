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

# Try AppActivate with PID
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

# Close Word
$wsh.SendKeys("%{F4}")
Start-Sleep -Seconds 2

if (!$p.HasExited) {
    $p.Kill()
}

Write-Host "Done"
'@

# Save script to a path without Chinese characters
$scriptPath = "C:\Users\changhaoyan\Desktop\scripts\print_task.ps1"
$scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8
Write-Host "Script saved to: $scriptPath"

# Create scheduled task to run immediately in user's session
$taskName = "PrintDoc_$(Get-Random)"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$scriptPath`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(-2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettings -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force | Out-Null
Write-Host "Task registered: $taskName"

# Wait for execution
Start-Sleep -Seconds 15

# Get task result
$info = Get-ScheduledTaskInfo -TaskName $taskName
Write-Host "Last result: $($info.LastTaskResult)"
Write-Host "Last run time: $($info.LastRunTime)"

# Cleanup
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item $scriptPath -Force -ErrorAction SilentlyContinue
Write-Host "Cleanup done"
