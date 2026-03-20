$ErrorActionPreference = "Continue"

$file = "C:\Users\changhaoyan\Desktop\template.docx"

# Use Word's /p switch to open print dialog directly
Write-Host "Starting Word with /p switch..."
$p = Start-Process -FilePath "C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE" -ArgumentList "/p `"$file`"" -PassThru -WindowStyle Maximized

Start-Sleep -Seconds 8

Write-Host "Word PID: $($p.Id), HasExited: $($p.HasExited)"

if ($p.HasExited) {
    Write-Host "Word exited with: $($p.ExitCode)"
} else {
    Write-Host "Word is running"
}

# Now use WScript.Shell to send Enter after activating
$wsh = New-Object -ComObject WScript.Shell
Start-Sleep -Seconds 3

# Try to activate by window title part
$title = "Word"
$activated = $wsh.AppActivate($title)
Write-Host "AppActivate('$title'): $activated"

if (-not $activated) {
    # Try alternative title
    $activated = $wsh.AppActivate("Microsoft Word")
    Write-Host "AppActivate('Microsoft Word'): $activated"
}

if (-not $activated) {
    # Try with document name
    $activated = $wsh.AppActivate("template")
    Write-Host "AppActivate('template'): $activated"
}

Start-Sleep -Seconds 2

# Send Enter to confirm print
Write-Host "Sending Enter..."
$wsh.SendKeys("{ENTER}")
Start-Sleep -Seconds 5

# Try Escape to close any dialogs
$wsh.SendKeys("{ESC}")
Start-Sleep -Seconds 2

# Close Word
if (!$p.HasExited) {
    Write-Host "Killing Word..."
    $p.Kill()
}

Write-Host "Done"
