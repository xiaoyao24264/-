"""
微信发消息测试 - 使用主屏幕分辨率 2560x1440
"""
import pyautogui
import pyperclip
import time
import ctypes

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.5

# 获取屏幕分辨率
user32 = ctypes.windll.user32
w = user32.GetSystemMetrics(0)
h = user32.GetSystemMetrics(1)
print(f"分辨率: {w}x{h}")

# 如果分辨率太小，使用估算值
if w < 2000:
    w, h = 2560, 1440
    print(f"使用估算: {w}x{h}")

# 搜索框 - 左侧约10%，顶部约5%
search_x = int(w * 0.1)
search_y = int(h * 0.05)
print(f"点击搜索框: ({search_x}, {search_y})")
pyautogui.click(search_x, search_y)
time.sleep(1)

# 输入联系人
pyautogui.write("hanchao")
time.sleep(1)
pyautogui.press("enter")
time.sleep(1)

# 点击联系人 - 搜索结果
contact_x = int(w * 0.1)
contact_y = int(h * 0.12)
print(f"点击联系人: ({contact_x}, {contact_y})")
pyautogui.click(contact_x, contact_y)
time.sleep(1)

# 发送消息
print("发送消息: 你好")
pyperclip.copy("你好")
pyautogui.hotkey("ctrl", "v")
time.sleep(0.5)
pyautogui.press("enter")

print("完成!")
