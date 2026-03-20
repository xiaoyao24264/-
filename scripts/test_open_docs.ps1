$ErrorActionPreference = "Stop"

# Test 1: Try opening a different file first
$testFile = "C:\Users\changhaoyan\Desktop\credit_notice.docx"
Write-Host "Test file: $testFile"
Write-Host "Exists: $(Test-Path $testFile)"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

Write-Host "Opening credit_notice.docx..."
$d = $word.Documents.Open($testFile)
Write-Host "Result: $d"

if ($d) {
    Write-Host "Opened successfully! Closing..."
    $d.Close($false)
    Write-Host "SUCCESS"
} else {
    Write-Host "FAILED - trying second file"
}

# Test 2: Try template.docx
$testFile2 = "C:\Users\changhaoyan\Desktop\template.docx"
Write-Host "`nTest file2: $testFile2"
Write-Host "Exists: $(Test-Path $testFile2)"

$d2 = $word.Documents.Open($testFile2)
Write-Host "Result: $d2"

if ($d2) {
    Write-Host "Opened successfully! Closing..."
    $d2.Close($false)
    Write-Host "SUCCESS"
} else {
    Write-Host "FAILED"
}

$word.Quit()
