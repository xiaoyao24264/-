"""
微信自动发消息脚本
"""
import pyautogui
import time

# 等待微信启动
time.sleep(3)

# 点击搜索框（需要手动调整坐标）
# 先获取屏幕大小
print(f"屏幕尺寸: {pyautogui.size()}")

# 点击微信顶部搜索框（大概位置）
pyautogui.click(100, 50)
time.sleep(1)

# 输入联系人名字
pyautogui.write('韩超')
time.sleep(1)

# 按回车搜索
pyautogui.press('enter')
time.sleep(2)

# 点击联系人
pyautogui.click(200, 150)
time.sleep(1)

# 输入消息
pyautogui.write('你好')
time.sleep(0.5)

# 发送
pyautogui.press('enter')

print("消息已发送！")
