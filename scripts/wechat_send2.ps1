$wshell = New-Object -ComObject wscript.shell
$wshell.AppActivate("微信")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("^f")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("茗子")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 1000
$wshell.SendKeys("{ENTER}")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("你好")
Start-Sleep -Milliseconds 500
$wshell.SendKeys("{ENTER}")
Write-Host "Done"
