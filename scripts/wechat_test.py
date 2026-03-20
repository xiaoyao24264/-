"""
微信自动化测试脚本
运行这个脚本来测试是否能自动化操作微信
"""
import win32gui
import win32con
import win32api
import time
import sys

print("=" * 50)
print("微信自动化测试脚本")
print("=" * 50)

# 1. 查找微信窗口
print("\n1. 查找微信窗口...")
wechat_hwnd = None

def find_wechat(hwnd, extra):
    title = win32gui.GetWindowText(hwnd)
    if title and ('微信' in title or 'WeChat' in title.lower()):
        if win32gui.IsWindowVisible(hwnd):
            print(f"   找到微信窗口: {hwnd} - {title}")
            extra[0] = hwnd

wechat_hwnd = [0]
win32gui.EnumWindows(find_wechat, wechat_hwnd)

if wechat_hwnd[0]:
    hwnd = wechat_hwnd[0]
    print(f"   窗口句柄: {hwnd}")
    
    # 2. 激活窗口
    print("\n2. 激活微信窗口...")
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(1)
    print("   已激活")
    
    # 3. 发送 Ctrl+F 打开搜索
    print("\n3. 打开搜索框 (Ctrl+F)...")
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)
    win32api.keybd_event(ord('F'), 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(ord('F'), 0, win32con.KEYEVENTF_KEYUP, 0)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(1)
    print("   已发送 Ctrl+F")
    
    # 4. 输入联系人名字
    print("\n4. 输入联系人名字: hanchao")
    win32gui.SendMessage(hwnd, win32con.WM_IME_COMPOSITION, 0, win32con.GCS_COMPSTR)
    for c in "hanchao":
        win32api.SendMessage(hwnd, win32con.WM_CHAR, ord(c), 0)
        time.sleep(0.1)
    time.sleep(1)
    print("   已输入")
    
    # 5. 按回车
    print("\n5. 按回车...")
    win32api.keybd_event(win32con.VK_RETURN, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(win32con.VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
    time.sleep(2)
    print("   已按回车")
    
    print("\n" + "=" * 50)
    print("测试完成！请检查微信是否已打开搜索结果")
    print("=" * 50)
    
else:
    print("   未找到微信窗口！请确保微信已打开")
    print("   可以手动打开微信后重新运行此脚本")
