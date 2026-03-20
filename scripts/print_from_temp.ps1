$ErrorActionPreference = "Stop"
$qqFile = "C:\Users\changhaoyan\Desktop\附件1：25年度廉政档案模板(2).docx"
$tempFile = "C:\temp_print.docx"

Write-Host "QQ file: $qqFile"
Write-Host "QQ file exists: $(Test-Path $qqFile)"

# Create temp dir
New-Item -Path "C:\temp" -ItemType Directory -Force | Out-Null

# Copy to temp with ASCII name
Copy-Item -Path $qqFile -Destination $tempFile -Force
Write-Host "Copied to: $tempFile"
Write-Host "Temp file exists: $(Test-Path $tempFile)"

# Now try to open and print
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

Write-Host "Word opened"

$d = $word.Documents.Open($tempFile)
Write-Host "Doc result: $d"

if ($d) {
    Write-Host "Printing..."
    $d.PrintOut($false, $false, 0, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, 1, 1, "1")
    Start-Sleep -Seconds 6
    $d.Close($false)
    Write-Host "SUCCESS"
} else {
    Write-Host "FAIL: doc is null"
}

$word.Quit()
