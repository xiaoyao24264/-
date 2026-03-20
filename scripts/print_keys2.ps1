$ErrorActionPreference = "Continue"

$file = "C:\Users\changhaoyan\Desktop\template.docx"

# Launch Word with the file
Write-Host "Opening: $file"
$p = Start-Process -FilePath "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" -ArgumentList "`"$file`"" -PassThru
Start-Sleep -Seconds 10

Write-Host "Word PID: $($p.Id), HasExited: $($p.HasExited)"

# Create WScript.Shell to send keys
$wsh = New-Object -ComObject WScript.Shell
Start-Sleep -Seconds 2

# Try to activate Word window
$activated = $wsh.AppActivate("Word")
Write-Host "Activated: $activated"

Start-Sleep -Seconds 1
$wsh.SendKeys("^p")
Start-Sleep -Seconds 2

Write-Host "Sending Enter..."
$wsh.SendKeys("{ENTER}")
Start-Sleep -Seconds 5

# Close with Alt+F4
$wsh.SendKeys("%{F4}")
Start-Sleep -Seconds 2

if (!$p.HasExited) {
    $p.Kill()
    Write-Host "Killed process"
}

Write-Host "All done"
