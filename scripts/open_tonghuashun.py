"""
打开同花顺脚本
用法：双击运行或 python open_tonghuashun.py
"""

import os
import subprocess
import sys

# 同花顺常见安装路径
TONGHUASHUN_PATHS = [
    r"C:\同花顺10\xiada.exe",
    r"C:\同花顺10\ths.exe",
    r"C:\Program Files\同花顺\xiada.exe",
    r"C:\Program Files\同花顺\ths.exe",
    r"C:\同花顺\xiada.exe",
    r"C:\同花顺\ths.exe",
]

def find_tonghuashun():
    """查找同花顺路径"""
    for path in TONGHUASHUN_PATHS:
        if os.path.exists(path):
            return path
    return None

def main():
    print("🔍 正在查找同花顺...")
    
    exe_path = find_tonghuashun()
    
    if exe_path:
        print(f"✅ 找到同花顺: {exe_path}")
        print("🚀 正在启动...")
        subprocess.Popen(exe_path)
        print("✅ 已启动成功！")
        input("\n按回车键退出...")
    else:
        print("❌ 未找到同花顺软件")
        print("\n请手动告诉我你的同花顺安装路径")
        print("例如: C:\\同花顺10\\xiada.exe")
        input("\n按回车键退出...")

if __name__ == "__main__":
    main()
