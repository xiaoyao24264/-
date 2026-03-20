$ErrorActionPreference = "Stop"
$filePath = "C:\Users\changhaoyan\Desktop\template.docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($filePath)
if ($doc -eq $null) {
    Write-Host "ERROR: cannot open doc"
    exit 1
}
$doc.PrintOut($false, $false, 0, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, [System.Reflection.Missing]::Value, 1, 1, "1")
Start-Sleep -Seconds 6
$doc.Close($false)
$word.Quit()
Write-Host "SUCCESS"
