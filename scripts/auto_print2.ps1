param(
    [string]$FilePath = "C:\Users\changhaoyan\Desktop\template.docx",
    [string]$PrinterName = "Generic 26C-7SeriesPCL"
)

$tempScript = "$env:TEMP\print_doc.ps1"
$scriptCode = @'
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open("FILE_PATH")
$doc.PrintOut($false, $false, 1)
Start-Sleep -Seconds 5
$doc.Close($false)
$word.Quit()
Write-Host "Done"
'@

$scriptCode = $scriptCode.Replace("FILE_PATH", $FilePath)
$scriptCode | Out-File -FilePath $tempScript -Encoding UTF8

$taskName = "PrintDoc_" + [guid]::NewGuid().ToString("N").Substring(0,8)
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$tempScript`""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(-2)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings (New-ScheduledTaskSettings -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries) -Force
Start-Sleep -Seconds 10
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
Remove-Item $tempScript -Force -ErrorAction SilentlyContinue
Write-Host "Print task completed"
