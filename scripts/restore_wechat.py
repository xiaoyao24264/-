"""
恢复微信窗口脚本
"""
import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32

print("开始查找微信窗口...")

EnumWindows = user32.EnumWindows
EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)
GetWindowText = user32.GetWindowTextW
GetWindowTextLength = user32.GetWindowTextLengthW
IsWindowVisible = user32.IsWindowVisible
GetClassName = user32.GetClassNameW

windows = []

def enum_cb(hwnd, lparam):
    if IsWindowVisible(hwnd):
        length = GetWindowTextLength(hwnd)
        title = ""
        if length > 0:
            buffer = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buffer, length + 1)
            title = buffer.value
        
        # 获取类名
        class_buffer = ctypes.create_unicode_buffer(256)
        GetClassName(hwnd, class_buffer, 256)
        class_name = class_buffer.value
        
        windows.append((hwnd, title, class_name))
    return True

EnumWindows(EnumWindowsProc(enum_cb), 0)

# 打印前30个窗口
print(f"共找到 {len(windows)} 个窗口")
print("\n前30个窗口:")
for h, t, c in windows[:30]:
    if t:
        print(f"  {h}: '{t}' (class: {c})")

# 查找微信
print("\n搜索微信:")
found = False
for h, t, c in windows:
    if "wechat" in t.lower() or "wechat" in c.lower() or "微信" in t:
        print(f"找到微信窗口: hwnd={h}, title='{t}'")
        # 尝试恢复窗口
        # SW_RESTORE = 9
        user32.ShowWindow(h, 9)
        time.sleep(0.2)
        user32.SetForegroundWindow(h)
        print("已尝试恢复窗口")
        found = True
        break

if not found:
    print("未找到微信窗口")

# 尝试通过进程ID找窗口
print("\n尝试通过进程...")
import subprocess
result = subprocess.run(['powershell', '-Command', 
    'Get-Process WeChatAppEx | Select-Object -First 1 | ForEach-Object { $_.Id }'],
    capture_output=True, text=True)
print(f"Process ID: {result.stdout.strip()}")
