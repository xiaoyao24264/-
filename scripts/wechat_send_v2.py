"""
微信自动发消息脚本 v2
功能：激活微信窗口，搜索联系人，发送消息
"""
import pyautogui
import time
import sys

# 禁用 failsafe
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

def activate_wechat():
    """激活微信窗口"""
    import subprocess
    # 使用 PowerShell 激活微信窗口
    subprocess.run([
        'powershell', '-Command',
        'Add-Type -TypeDefinition @"using System;using System.Runtime.InteropServices;public class Win32 {[DllImport(\"user32.dll\")]public static extern bool SetForegroundWindow(IntPtr hWnd);} "@'
    ], capture_output=True)
    
    # 枚举窗口找到微信
    result = subprocess.run([
        'powershell', '-Command',
        'Get-Process WeChat -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty Id'
    ], capture_output=True, text=True)
    
    if result.stdout.strip():
        pid = result.stdout.strip()
        # 使用 PowerShell 激活窗口
        subprocess.run([
            'powershell', '-Command',
            f'Start-Process powershell -ArgumentList "-Command \\"Add-Type -TypeDefinition @\\'using System;using System.Runtime.InteropServices;public class Win32 {{[DllImport(\\"user32.dll\\")]public static extern bool SetForegroundWindow(IntPtr hWnd);}};$hwnd = (Get-Process -Id {pid}).MainWindowHandle;if($hwnd){{[Win32]::SetForegroundWindow($hwnd)}}\\'\\""'
        ], capture_output=True)
        print(f"已激活微信窗口 (PID: {pid})")
        return True
    return False

def find_and_click_contact(contact_name):
    """查找并点击联系人"""
    # 先获取屏幕截图
    screenshot = pyautogui.screenshot()
    
    # 点击微信顶部搜索区域（一般在上方）
    # 尝试点击搜索框位置 (需要根据实际调整)
    search_box_x, search_box_y = 150, 30  # 微信顶部搜索框位置
    pyautogui.click(search_box_x, search_box_y)
    time.sleep(1)
    
    # 输入联系人名字（用拼音或英文名）
    pyautogui.write(contact_name)
    time.sleep(1)
    
    # 按回车搜索
    pyautogui.press('enter')
    time.sleep(1)
    
    # 点击搜索结果中的第一个联系人
    # 一般搜索结果在搜索框下方
    result_x, result_y = 150, 80
    pyautogui.click(result_x, result_y)
    time.sleep(1)

def send_message(message):
    """发送消息"""
    # 输入消息
    pyautogui.write(message)
    time.sleep(0.5)
    
    # 发送
    pyautogui.press('enter')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("用法: python wechat_send.py <联系人> <消息>")
        print("示例: python wechat_send.py hanchao 你好")
        sys.exit(1)
    
    contact = sys.argv[1]
    message = sys.argv[2]
    
    print(f"开始给 [{contact}] 发送消息: [{message}]")
    
    # 等待微信启动
    print("等待微信启动...")
    time.sleep(5)
    
    # 激活微信
    print("激活微信窗口...")
    activate_wechat()
    time.sleep(2)
    
    # 查找联系人
    print(f"搜索联系人: {contact}")
    find_and_click_contact(contact)
    time.sleep(2)
    
    # 发送消息
    print(f"发送消息: {message}")
    send_message(message)
    
    print("完成！")
