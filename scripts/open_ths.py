"""
打开同花顺 - 使用 PyAutoGUI
"""
import pyautogui
import time
import os

# 设置暂停时间
pyautogui.PAUSE = 0.5

# 方法1：直接运行可执行文件（推荐）
try:
    os.startfile(r"C:\同花顺软件\同花顺\hexinlauncher.exe")
    print("✅ 同花顺已启动！")
except Exception as e:
    print(f"方法1失败: {e}")
    
    # 方法2：使用 Win 键搜索
    print("尝试方法2：通过开始菜单搜索...")
    pyautogui.press('win')
    time.sleep(1)
    pyautogui.write('同花顺')
    time.sleep(0.5)
    pyautogui.press('enter')
    print("✅ 已按回车，应该启动了！")
