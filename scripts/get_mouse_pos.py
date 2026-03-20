"""
获取鼠标位置的脚本
运行后会每秒打印当前鼠标位置，方便确定微信界面坐标
"""
import pyautogui
import time

print("获取鼠标位置")
print("移动鼠标到目标位置，程序会自动记录坐标")
print("按 Ctrl+C 退出")
print("-" * 40)

try:
    while True:
        x, y = pyautogui.position()
        print(f"\r位置: ({x}, {y})", end="")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n\n退出")
