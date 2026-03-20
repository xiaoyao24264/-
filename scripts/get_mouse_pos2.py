"""
获取鼠标位置 - 持续打印
"""
import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32

class POINT(wintypes.Structure):
    _fields_ = [("x", wintypes.LONG),
                ("y", wintypes.LONG)]

print("移动鼠标，然后查看位置...")
print("按 Ctrl+C 退出")
print("-" * 40)

try:
    while True:
        pt = POINT()
        if user32.GetCursorPos(ctypes.byref(pt)):
            print(f"\r鼠标位置: ({pt.x}, {pt.y})", end="")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("\n退出")
