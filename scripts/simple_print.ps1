# Simple print script
$file = "C:\Users\changhaoyan\Desktop\廉政档案打印版.docx"
Write-Host "Starting print for: $file"
$p = Start-Process -FilePath $file -Verb Print -WindowStyle Hidden -PassThru
Start-Sleep 10
if ($p.HasExited) {
    Write-Host "Process exited with code: $($p.ExitCode)"
} else {
    Write-Host "Process still running, killing..."
    $p.Kill()
}
Write-Host "Done"
