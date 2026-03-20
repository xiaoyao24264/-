$ErrorActionPreference = "Stop"

# Copy from QQ download folder to desktop
$qqFile = "C:\Users\changhaoyan\Desktop\附件1：25年度廉政档案模板(2).docx"
$destFile = "C:\Users\changhaoyan\Desktop\廉政档案打印版.docx"

try {
    Copy-Item -Path $qqFile -Destination $destFile -Force
    Write-Host "Copied to: $destFile"
} catch {
    Write-Host "Copy failed: $_"
    exit 1
}

# Now try to open and print
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($destFile)
    if ($doc -eq $null) {
        Write-Host "ERROR: Cannot open doc"
        $word.Quit()
        exit 1
    }
    Write-Host "Doc opened successfully"
    $doc.PrintOut($false, $false, 0, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, 1, 1, "1")
    Start-Sleep -Seconds 6
    $doc.Close($false)
    Write-Host "SUCCESS"
} catch {
    Write-Host "Print error: $_"
} finally {
    $word.Quit()
}
