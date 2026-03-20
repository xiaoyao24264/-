$tempScript = "$env:TEMP\wprint2.ps1"
$code = @'
$file = "C:\Users\changhaoyan\Desktop\template.docx"
$proc = Start-Process $file -Verb Print -PassThru -WindowStyle Minimized
Start-Sleep 10
if (!$proc.HasExited) { $proc.Kill() }
Write-Host "Done"
'@
$code | Out-File -FilePath $tempScript -Encoding UTF8
$task = "PrintA_" + (Get-Random 9999)
Register-ScheduledTask -TaskName $task -Action (New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$tempScript`"") -Trigger (New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(-1)) -Principal (New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited) -Settings (New-ScheduledTaskSettings -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable) -Force | Out-Null
Start-Sleep 8
Unregister-ScheduledTask -TaskName $task -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item $tempScript -Force -ErrorAction SilentlyContinue
Write-Host "Task done"
