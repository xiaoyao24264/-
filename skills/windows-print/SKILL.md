# Windows Print Automation Script
# 用途：打开Word文档并打印第一页
# 放到 Windows 桌面上双击运行即可

$ErrorActionPreference = "SilentlyContinue"

# 打开 Word 文档（用默认程序）
$filePath = "C:\Users\changhaoyan\Desktop\廉政档案模板.docx"
$shell = New-Object -ComObject WScript.Shell

# 使用 explorer 打开（会在用户当前会话打开）
Start-Process "explorer.exe" "$filePath"

# 等待 Word 启动
Start-Sleep -Seconds 5

# 发送 Ctrl+P 打印快捷键
$WshShell = New-Object -ComObject WScript.Shell
$WshShell.AppActivate("Word")  # 激活 Word 窗口
Start-Sleep -Seconds 1
$WshShell.SendKeys("^p")  # Ctrl+P
Start-Sleep -Seconds 2
$WshShell.SendKeys("{ENTER}")  # 确认打印
Start-Sleep -Seconds 2
$WshShell.SendKeys("{ESC}")  # 取消

Write-Host "打印指令已发送！"
