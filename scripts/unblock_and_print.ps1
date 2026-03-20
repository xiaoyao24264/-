$ErrorActionPreference = "Continue"

# Check if file is blocked (Mark of the Web)
$file = "C:\Users\changhaoyan\Desktop\template.docx"
Write-Host "Checking: $file"

$zone = Get-Item $file -Stream "Zone.Identifier" -ErrorAction SilentlyContinue
if ($zone) {
    Write-Host "Zone.Identifier content:"
    $zone.Content
} else {
    Write-Host "No Zone.Identifier stream (not blocked)"
}

# Try Unblock-File
Unblock-File -Path $file -WhatIf
Write-Host "Unblock-File would be attempted"

# Alternative: copy with -Unblock
$dest = "C:\temp_unblocked.docx"
Copy-Item -Path $file -Destination $dest -Unblock
Write-Host "Copied with -Unblock to: $dest"
Write-Host "Dest exists: $(Test-Path $dest)"

# Now try Word COM again with unblocked file
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

$d = $word.Documents.Open($dest)
Write-Host "Doc after unblock: $d"

if ($d) {
    $d.PrintOut($false, $false, 0, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, 1, 1, "1")
    Start-Sleep -Seconds 6
    $d.Close($false)
    Write-Host "SUCCESS"
} else {
    Write-Host "FAIL"
}

$word.Quit()
