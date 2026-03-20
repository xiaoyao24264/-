"""
OpenClaw GUI Agent Skill - 集成的 GUI 智能体

用法:
1. 先截图: ssh_exec("截图命令")
2. 用 image() 分析截图
3. 用 plan_action() 生成动作
4. 用 ground_action() 获取精确坐标
5. 用 execute_action() 执行
"""

import subprocess
import time
import re
import logging
from typing import Dict, List, Tuple, Optional

from .executor import WindowsExecutor, parse_action_string

logger = logging.getLogger("gui_agent")


class OpenClawGUIAgent:
    """
    集成到 OpenClaw 的 GUI Agent
    使用 OpenClaw 的 image 工具作为视觉模型
    """

    def __init__(
        self,
        instruction: str,
        ssh_host: str = "172.20.48.1",
        ssh_user: str = "changhaoyan",
        max_turns: int = 15,
        max_history: int = 6,
    ):
        self.instruction = instruction
        self.ssh_host = ssh_host
        self.ssh_user = ssh_user
        self.max_turns = max_turns
        self.max_history = max_history

        self.executor = WindowsExecutor(ssh_host, ssh_user)
        self.turn_count = 0
        self.history = []

    def run(self) -> Dict:
        """
        运行完整的 GUI Agent 循环

        Returns:
            dict: 包含 done/failed/turn_count/history
        """
        print(f"[GUI Agent] Starting task: {self.instruction}")

        while self.turn_count < self.max_turns:
            try:
                step_result = self.step()

                if step_result.get("done"):
                    print(f"[GUI Agent] Task completed at turn {self.turn_count}")
                    return {"done": True, "turn_count": self.turn_count, "history": self.history}

                if step_result.get("failed"):
                    print(f"[GUI Agent] Task failed at turn {self.turn_count}")
                    return {"done": False, "failed": True, "turn_count": self.turn_count, "history": self.history}

                self.turn_count += 1

            except Exception as e:
                logger.error(f"Step error: {e}")
                self.history.append({"turn": self.turn_count, "error": str(e)})
                self.turn_count += 1

        return {"done": False, "failed": False, "turn_count": self.turn_count, "history": self.history, "reason": "max_turns"}

    def step(self) -> Dict:
        """
        执行单步: 截图 -> 分析 -> 动作 -> 执行
        """
        # Step 1: 截图
        screenshot_bytes = self.executor.screenshot()
        print(f"[Turn {self.turn_count}] Screenshot captured, size={len(screenshot_bytes)} bytes")

        # Step 2: 用视觉模型分析 + 生成动作
        # 这里需要调用 OpenClaw 的 image 工具
        # 在 skill 内部无法直接调用 image 工具，需要通过 agent 框架
        # 所以这个方法返回截图，让调用者用 image 工具分析后再调用 execute
        action_code = self._get_action_from_llm(screenshot_bytes)

        if not action_code:
            return {"done": False, "failed": False}

        print(f"[Turn {self.turn_count}] Action: {action_code}")

        # Step 3: 解析并执行动作
        result = self._execute(action_code)

        # 记录历史
        self.history.append({
            "turn": self.turn_count,
            "screenshot_size": len(screenshot_bytes),
            "action": action_code,
            "result": result,
        })

        # 刷新过长的历史
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history:]

        return result

    def _get_action_from_llm(self, screenshot_bytes: bytes) -> Optional[str]:
        """
        获取 LLM 生成的动作
        需要集成 OpenClaw 的 image 工具
        这个方法设计为可以被 agent 框架调用
        """
        # 这里只是返回 None，真正的视觉理解需要外部调用者用 image 工具
        return None

    def _execute(self, action_code: str) -> Dict:
        """执行动作代码"""
        func_name, args = parse_action_string(action_code)

        if func_name == "click":
            x, y = args[0], args[1]
            button = args[2] if len(args) > 2 else "left"
            success = self.executor.click(x, y, button)
            return {"done": False, "failed": not success}

        elif func_name == "type":
            text = args[0]
            success = self.executor.type_text(text)
            return {"done": False, "failed": not success}

        elif func_name == "hotkey":
            success = self.executor.hotkey(*args)
            return {"done": False, "failed": not success}

        elif func_name == "scroll":
            amount = args[0] if args else 0
            success = self.executor.scroll(amount)
            return {"done": False, "failed": not success}

        elif func_name == "wait":
            seconds = args[0] if args else 1
            self.executor.wait(seconds)
            return {"done": False, "failed": False}

        elif func_name == "done":
            return {"done": True, "failed": False}

        elif func_name == "fail":
            return {"done": False, "failed": True}

        return {"done": False, "failed": False}


def get_vision_analysis(screenshot_path: str, instruction: str, history: str = "") -> str:
    """
    辅助函数: 用 image 工具分析截图
    返回视觉模型的分析结果
    """
    # 这个函数需要外部调用 image() 工具
    # 使用时需要通过 agent 框架
    from .prompts import WORKER_USER_PROMPT

    prompt = f"""You are a GUI agent. Analyze this screenshot.

Task: {instruction}

Previous actions:
{history if history else "None"}

Describe what you see and what the next action should be.
Be specific about what to click and where.
"""
    return prompt  # 返回提示词，实际分析由 image 工具完成
