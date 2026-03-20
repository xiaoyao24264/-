"""
获取所有窗口位置
"""
import ctypes
from ctypes import wintypes
import time

user32 = ctypes.windll.user32

windows = []

EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

def enum_cb(hwnd, lparam):
    try:
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                title = buffer.value
                rect = wintypes.RECT()
                user32.GetWindowRect(hwnd, ctypes.byref(rect))
                if rect.right > rect.left and rect.bottom > rect.top:
                    windows.append((title, rect.left, rect.top, rect.right, rect.bottom))
    except:
        pass
    return True

user32.EnumWindows(EnumWindowsProc(enum_cb), 0)

with open("windows.txt", "w", encoding="utf-8") as f:
    f.write(f"屏幕: {user32.GetSystemMetrics(0)}x{user32.GetSystemMetrics(1)}\n\n")
    for t, l, top, r, b in windows:
        if t:
            f.write(f"({l},{top}) {t}\n")
    f.write(f"\n共 {len(windows)} 个窗口\n")
