$ErrorActionPreference = "Continue"

# Get the actual docx file in downloads (QQ sends files here)
$downloads = [Environment]::GetFolderPath("Desktop")
Write-Host "Desktop: $downloads"

# List all docx files on desktop
Get-ChildItem -Path $downloads -Filter "*.docx" | ForEach-Object {
    Write-Host "Found: $($_.FullName) - $($_.Length) bytes"
}

# Try to print using shell execute (more reliable than verb)
Add-Type -AssemblyName System.Windows.Forms

$fileToPrint = "C:\Users\changhaoyan\Desktop\template.docx"
Write-Host "Trying to print: $fileToPrint"

# Method: use Invoke-Item which uses the default handler
$proc = Start-Process -FilePath $fileToPrint -PassThru -WindowStyle Minimized
Start-Sleep -Seconds 3

if ($proc -eq $null) {
    Write-Host "Start-Process returned null"
} else {
    Write-Host "Process started, ID: $($proc.ID), HasExited: $($proc.HasExited)"
    
    # Send Ctrl+P to print (if process is Word)
    Start-Sleep -Seconds 5
    
    # Try to close
    if (!$proc.HasExited) {
        Write-Host "Process still running"
    } else {
        Write-Host "Process exited with code: $($proc.ExitCode)"
    }
}

Write-Host "Done"
