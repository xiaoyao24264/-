# 微信发送消息脚本
$wshell = New-Object -ComObject wscript.shell

# 尝试激活微信窗口 - 用不同的标题
$wechatTitles = @("微信", "WeChat", "WeChatApp")
$activated = $false

foreach ($title in $wechatTitles) {
    $result = $wshell.AppActivate($title)
    if ($result) {
        Write-Host "激活成功: $title"
        $activated = $true
        Start-Sleep -Milliseconds 500
        break
    }
}

if (-not $activated) {
    Write-Host "激活失败，尝试发送Ctrl+F"
}

# 发送 Ctrl+F 打开搜索
$wshell.SendKeys('^f')
Start-Sleep -Milliseconds 1000

# 输入联系人名字
$wshell.SendKeys('茗子')
Start-Sleep -Milliseconds 1000

# 按回车
$wshell.SendKeys('{ENTER}')
Start-Sleep -Milliseconds 1000

# 再次按回车进入聊天
$wshell.SendKeys('{ENTER}')
Start-Sleep -Milliseconds 500

# 输入消息
$wshell.SendKeys('你好')
Start-Sleep -Milliseconds 500

# 发送
$wshell.SendKeys('{ENTER}')

Write-Host "消息已发送"
