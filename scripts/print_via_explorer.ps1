$ErrorActionPreference = "Stop"
$file = "C:\Users\changhaoyan\Desktop\template.docx"
Write-Host "File: $file"
Write-Host "Exists: $(Test-Path $file)"

# Try using WScript.Shell to open and print
$shell = New-Object -ComObject WScript.Shell
Write-Host "Shell created"

# Use explorer to open with print
$cmd = "explorer.exe /print," + $file
Write-Host "Command: $cmd"
Start-Process -FilePath "explorer.exe" -ArgumentList "/print,`"$file`"" -WindowStyle Hidden
Start-Sleep 10
Write-Host "Done"
