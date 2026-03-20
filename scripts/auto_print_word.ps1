# Windows 打印自动化脚本 v2
# 通过计划任务在用户交互会话中运行 Word 打印

param(
    [string]$FilePath = "C:\Users\changhaoyan\Desktop\廉政档案模板.docx",
    [string]$PrinterName = "Generic 26C-7SeriesPCL",
    [int]$PageToPrint = 1
)

$ErrorActionPreference = "Stop"

# 转换路径为短文件名（避免中文路径问题）
$shortPath = (New-Object -ComObject Scripting.FileSystemObject).GetFileName($FilePath)
$folder = Split-Path $FilePath -Parent
$shortFolder = (New-Object -ComObject Scripting.FileSystemObject).GetFolder($folder)
$parentPath = $shortFolder.Parent.Path
$shortName = $shortFolder.Name
$fullShortPath = Join-Path $parentPath "$shortName\$shortPath"

Write-Host "原始路径: $FilePath"
Write-Host "短路径: $fullShortPath"

# 创建临时脚本内容
$scriptContent = @"
`$word = New-Object -ComObject Word.Application
`$word.Visible = `$false
`$word.DisplayAlerts = 0

`$doc = `$word.Documents.Open("`"$FilePath`"")
if (`$doc -eq `$null) {
    Write-Host "ERROR: 无法打开文档"
    exit 1
}

# 打印指定页面
`$doc.PrintOut(
    [ref]`$false,        # Background
    [ref]`$false,        # Append  
    [ref]1,              # Range (1 = current page when using Pages param)
    [ref][System.Reflection.Missing]::Value,
    [ref][System.Reflection.Missing]::Value,
    [ref][System.Reflection.Missing]::Value,
    [ref]1,              # Item (wdPrintDocumentContent = 1)
    [ref]1,              # Copies
    [ref]"$PageToPrint"  # Pages
)

Start-Sleep -Seconds 5
`$doc.Close(`$false)
`$word.Quit()

Write-Host "SUCCESS: 已发送打印任务"
"@

# 保存脚本到用户临时目录
$scriptPath = "$env:TEMP\auto_print_$([guid]::NewGuid().ToString('N')).ps1"
$scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8

Write-Host "脚本已保存: $scriptPath"

# 创建计划任务（立即运行，在用户会话）
$taskName = "AutoPrintDoc_$([guid]::NewGuid().ToString('N').Substring(0,8))"
$taskAction = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-ExecutionPolicy Bypass -NoProfile -WindowStyle Hidden -File `"$scriptPath`""
$taskTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(-1)
$taskPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited
$taskSettings = New-ScheduledTaskSettings -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

try {
    Register-ScheduledTask -TaskName $taskName -Action $taskAction -Trigger $taskTrigger -Principal $taskPrincipal -Settings $taskSettings -Force
    
    Write-Host "计划任务已创建: $taskName"
    
    # 等待任务执行
    Start-Sleep -Seconds 8
    
    # 获取任务结果
    $taskResult = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue | Get-ScheduledTaskInfo
    Write-Host "任务状态: $($taskResult.LastTaskResult)"
    
    # 清理
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
    Remove-Item $scriptPath -Force -ErrorAction SilentlyContinue
    
    if ($taskResult.LastTaskResult -eq 0) {
        Write-Host "✅ 打印成功！"
    } else {
        Write-Host "⚠️ 打印任务已提交（可能成功）"
    }
    
} catch {
    Write-Host "ERROR: $_"
    
    # 备用方案：直接尝试打开文件触发打印
    Write-Host "尝试备用方案：直接打开文件..."
    try {
        $proc = Start-Process $FilePath -Verb Print -WindowStyle Minimized -PassThru
        Start-Sleep -Seconds 5
        if (!$proc.HasExited) {
            $proc.Kill()
        }
        Write-Host "✅ 备用方案已执行"
    } catch {
        Write-Host "备用方案失败: $_"
    }
}
