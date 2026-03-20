$ErrorActionPreference = "Stop"
Add-Type -AssemblyName Microsoft.VisualBasic

$file = "C:\Users\changhaoyan\Desktop\template.docx"

# Launch Word with the file
Write-Host "Opening Word with file..."
$p = Start-Process -FilePath "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" -ArgumentList "`"$file`"" -PassThru
Start-Sleep -Seconds 8

if ($p.HasExited) {
    Write-Host "Word exited early: $($p.ExitCode)"
    exit 1
}

Write-Host "Word is running, PID: $($p.Id)"

# Wait for document to load
Start-Sleep -Seconds 5

# Send Ctrl+P for Print
Write-Host "Sending Ctrl+P..."
[Microsoft.VisualBasic.Interaction]::AppActivate($p.Id)
Start-Sleep -Seconds 2

# Create WScript.Shell to send keys
$wsh = New-Object -ComObject WScript.Shell
$wsh.AppActivate("Word") | Out-Null
Start-Sleep -Seconds 1
$wsh.SendKeys("^p")
Start-Sleep -Seconds 3

# Send Enter to print
Write-Host "Sending Enter..."
$wsh.SendKeys("{ENTER}")
Start-Sleep -Seconds 5

# Close Word
Write-Host "Closing Word..."
$wsh.SendKeys("%{F4}")  # Alt+F4
Start-Sleep -Seconds 2

if (!$p.HasExited) {
    $p.Kill()
}

Write-Host "Done"
