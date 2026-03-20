"""
获取屏幕信息
"""
import mss

s = mss.mss()
print(f"显示器数量: {len(s.monitors)}")
for i, m in enumerate(s.monitors):
    print(f"显示器 {i}: {m}")
s.close()
