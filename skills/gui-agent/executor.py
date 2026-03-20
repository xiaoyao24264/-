"""
GUI Agent Executor - PyAutoGUI 执行器
通过 SSH 在 Windows 上执行 GUI 操作

依赖: Windows 上已安装 Python + pyautogui
测试命令: ssh user@host "pip show pyautogui"
"""

import subprocess
import time
import re
from typing import Tuple, Optional

# PyAutoGUI 快捷键映射
HOTKEY_MAP = {
    "ctrl": "^",
    "control": "^",
    "alt": "%",
    "shift": "+",
    "cmd": "^{ESC}",
    "win": "^{ESC}",
    "escape": "{ESC}",
    "esc": "{ESC}",
    "enter": "{ENTER}",
    "return": "{ENTER}",
    "tab": "{TAB}",
    "backspace": "{BACKSPACE}",
    "bs": "{BACKSPACE}",
    "delete": "{DELETE}",
    "del": "{DELETE}",
    "home": "{HOME}",
    "end": "{END}",
    "pageup": "{PGUP}",
    "pagedown": "{PGDN}",
    "up": "{UP}",
    "down": "{DOWN}",
    "left": "{LEFT}",
    "right": "{RIGHT}",
    "f1": "{F1}",
    "f2": "{F2}",
    "f3": "{F3}",
    "f4": "{F4}",
    "f5": "{F5}",
    "f6": "{F6}",
    "f7": "{F7}",
    "f8": "{F8}",
    "f9": "{F9}",
    "f10": "{F10}",
    "f11": "{F11}",
    "f12": "{F12}",
    "space": " ",
    " ": " ",
}


class WindowsExecutor:
    """
    在 Windows 上执行 GUI 操作
    支持: click, type, hotkey, scroll, screenshot, wait, done, fail
    """

    def __init__(self, ssh_host: str, ssh_user: str):
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user

    def ssh_run(self, command: str, timeout: int = 30) -> Tuple[str, str]:
        """通过 SSH 执行命令"""
        result = subprocess.run(
            ["ssh", f"{self.ssh_user}@{self.ssh_host}", command],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.stdout, result.stderr

    def _run_python(self, code: str, timeout: int = 30) -> Tuple[str, str]:
        """在 Windows 上运行 Python 代码"""
        # Escape double quotes in the code
        escaped_code = code.replace('"', '\\"')
        cmd = f'python -c "import pyautogui; pyautogui.FAILSAFE=False; {escaped_code}"'
        return self.ssh_run(cmd, timeout=timeout)

    def click(self, x: int, y: int, button: str = "left") -> bool:
        """点击指定坐标
        
        Args:
            x: x 坐标
            y: y 坐标
            button: left / right / middle
        """
        btn = {"left": "left", "right": "right", "middle": "middle"}.get(button, "left")
        code = f'pyautogui.click({x}, {y}, button=\'{btn}\')'
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def move_to(self, x: int, y: int) -> bool:
        """移动鼠标到指定坐标"""
        code = f"pyautogui.moveTo({x}, {y})"
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def double_click(self, x: int, y: int, button: str = "left") -> bool:
        """双击指定坐标"""
        btn = {"left": "left", "right": "right", "middle": "middle"}.get(button, "left")
        code = f"pyautogui.doubleClick({x}, {y}, button=\'{btn}\')"
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """输入文字
        
        Args:
            text: 要输入的文字
            interval: 每个字符间隔（秒）
        """
        # Escape special characters for Python string
        escaped = text.replace("\\", "\\\\").replace('"', '\\"')
        code = f'pyautogui.typewrite("{escaped}", {interval})'
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def press(self, key: str) -> bool:
        """按一个键
        
        Args:
            key: 键名（如 enter, esc, tab, a, 1 等）
        """
        key_lower = key.lower()
        if key_lower in HOTKEY_MAP:
            key_str = HOTKEY_MAP[key_lower]
        else:
            key_str = key.lower()

        # 处理普通字符键
        if len(key_str) == 1 and key_str.isalnum():
            key_str = key_str.lower()

        code = f'pyautogui.press(\'{key_str}\')'
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def hotkey(self, *keys) -> bool:
        """发送快捷键组合
        
        Args:
            *keys: 键序列，如 hotkey("ctrl", "c") 表示 Ctrl+C
        """
        key_strs = []
        for key in keys:
            key_lower = key.lower()
            if key_lower in HOTKEY_MAP:
                key_strs.append(HOTKEY_MAP[key_lower])
            else:
                key_strs.append(key.lower())

        combined = "".join(key_strs)
        code = f'pyautogui.hotkey(\'{combined[0]}\' if len(\'{combined}\')==1 else *[\'{c}\' for c in \'{combined}\']\')'
        
        # 简化处理
        code = f"pyautogui.hotkey({', '.join(repr(k) for k in key_strs)})"
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def scroll(self, clicks: int) -> bool:
        """滚动鼠标
        
        Args:
            clicks: 正数=向上滚，负数=向下滚
        """
        code = f"pyautogui.scroll({clicks})"
        out, err = self._run_python(code)
        return "error" not in err.lower()

    def wait(self, seconds: float) -> bool:
        """等待"""
        time.sleep(seconds)
        return True

    def screenshot(self, save_path: str = "C:\\temp_gui_screenshot.png") -> bytes:
        """截取屏幕并返回图片数据"""
        # 先截屏保存
        script = f"""
import pyautogui
pyautogui.FAILSAFE=False
img = pyautogui.screenshot()
img.save(r"{save_path}")
print("screenshot saved")
"""
        escaped = script.replace('"', '\\"')
        self.ssh_run(f'python -c "{escaped}"', timeout=15)

        # 下载截图
        local_path = f"/tmp/screenshot_{int(time.time()*1000)}.png"
        result = subprocess.run(
            ["scp", f"{self.ssh_user}@{self.ssh_host}:{save_path}", local_path],
            capture_output=True,
            timeout=15,
        )
        
        if result.returncode != 0:
            return b""

        with open(local_path, "rb") as f:
            return f.read()

    def done(self) -> bool:
        """标记任务完成"""
        return True

    def fail(self) -> bool:
        """标记任务失败"""
        return False


def parse_action_string(action_str: str) -> Tuple[str, list]:
    """
    解析动作字符串
    例如: agent.click("submit button", 100, 200, "left")
    返回: ("click", [100, 200, "left"])
    """
    action_str = action_str.strip()
    if action_str.startswith("agent."):
        action_str = action_str[6:]

    match = re.match(r"(\w+)\((.*)\)\s*$", action_str, re.DOTALL)
    if not match:
        return action_str, []

    func_name = match.group(1)
    args_str = match.group(2)

    # 解析参数
    args = _parse_args(args_str)
    return func_name, args


def _parse_args(args_str: str) -> list:
    """解析参数字符串"""
    args = []
    current = ""
    in_single_quote = False
    in_double_quote = False
    paren_depth = 0

    for char in args_str:
        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current += char
        elif char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current += char
        elif char in "([{" and not in_single_quote and not in_double_quote:
            paren_depth += 1
            current += char
        elif char in ")]}" and not in_single_quote and not in_double_quote:
            paren_depth -= 1
            current += char
        elif char == "," and not in_single_quote and not in_double_quote and paren_depth == 0:
            val = current.strip()
            if val:
                args.append(_parse_value(val))
            current = ""
        else:
            current += char

    if current.strip():
        args.append(_parse_value(current.strip()))

    return args


def _parse_value(val: str) -> any:
    """解析单个参数值"""
    val = val.strip()
    
    # 去掉引号
    if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
        return val[1:-1]
    
    # 布尔值
    if val.lower() == "true":
        return True
    if val.lower() == "false":
        return False
    if val.lower() == "none" or val.lower() == "null":
        return None
    
    # 数字
    try:
        if "." in val:
            return float(val)
        return int(val)
    except:
        pass
    
    return val
