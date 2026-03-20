"""
激活微信窗口并发送消息
"""
import ctypes
from ctypes import wintypes
import time
import subprocess
import win32com.client

user32 = ctypes.windll.user32

# 1. 获取微信主窗口句柄
result = subprocess.run(
    ["powershell", "-Command", "(Get-Process WeChatAppEx | Select-Object -First 1).MainWindowHandle"],
    capture_output=True, text=True
)
hwnd = int(result.stdout.strip() or 0)

print(f"WeChat window handle: {hwnd}")

if hwnd:
    # 2. 恢复并激活窗口
    user32.ShowWindow(hwnd, 9)  # SW_RESTORE
    time.sleep(0.3)
    user32.SetForegroundWindow(hwnd)
    time.sleep(0.5)
    print("Window activated!")
    
    # 3. 使用 SendKeys 发送按键
    shell = win32com.client.Dispatch("WScript.Shell")
    
    # 打开搜索
    shell.SendKeys("^f")
    print("Sent Ctrl+F")
    time.sleep(1)
    
    # 输入联系人
    shell.SendKeys("茗子")
    print("Sent name")
    time.sleep(1)
    
    # 回车进入聊天
    shell.SendKeys("{ENTER}")
    print("Sent Enter")
    time.sleep(1)
    
    # 再次回车确认
    shell.SendKeys("{ENTER}")
    time.sleep(0.5)
    
    # 发送消息
    shell.SendKeys("你好")
    time.sleep(0.5)
    shell.SendKeys("{ENTER}")
    print("Sent message!")
else:
    print("Cannot find WeChat window")
