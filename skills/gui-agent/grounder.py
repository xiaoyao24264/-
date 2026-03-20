"""
GUI Agent Grounder - 视觉 grounding 模块
参考 Agent-S 的 Grounding Agent 思路

将高层动作指令（来自 LLM）翻译成精确的坐标动作
"""

import re
import logging
from typing import Tuple, Optional

logger = logging.getLogger("gui_agent.grounder")

# Agent-S 的 Worker Agent 提示词模板 - 指导 LLM 生成正确格式的动作
WORKER_SYSTEM_PROMPT = """You are an expert GUI agent controlling a Windows computer.

You are given a task and must choose the correct action to complete it.

AVAILABLE ACTIONS:
- click(description, x, y, button) - Click at coordinates (x,y)
- type(text) - Type text using keyboard
- hotkey(key1, key2, ...) - Press keyboard shortcut
- scroll(amount) - Scroll mouse (positive=up, negative=down)
- wait(seconds) - Wait for something to load
- done() - Task completed successfully
- fail() - Task cannot be completed

IMPORTANT RULES:
1. Always click on the ELEMENT ITSELF, not nearby areas
2. Click on TEXT LABELS directly when possible
3. For buttons, click on the CENTER of the button
4. For text fields, click on the text field first, then type
5. Use hotkeys instead of clicking when possible (e.g., Ctrl+C for copy)
6. After clicking something, WAIT at least 1-2 seconds for the UI to respond
7. Always verify your action worked before proceeding

ACTION FORMAT:
Action: <describe what you're doing>
Code: agent.click("Close button", 150, 30, "left")
"""

WORKER_USER_PROMPT = """Task: {instruction}

Previous actions:
{history}

Current screen: (see screenshot)

{analysis_instruction}

Respond with:
Action: <what you're going to do and why>
Code: <exact code to execute>
"""

GROUNDING_PROMPT = """Look at this screenshot. I need to execute this action:
{action_plan}

1. Describe what element should be clicked/interacted with
2. Give exact x,y coordinates for clicking

Respond in this format:
Element: <what you're clicking>
x: <exact x coordinate>
y: <exact y coordinate>
Reason: <why these coordinates>
"""


class GUIGrounder:
    """
    Grounding 模块 - 将 LLM 生成的动作翻译成精确坐标
    参考 Agent-S 的 Grounding Agent (OSWorldACI)
    """

    def __init__(self, vision_model=None, platform: str = "windows"):
        """
        Args:
            vision_model: callable, 接受 (image_bytes, prompt) 返回文本
            platform: windows / macos / linux
        """
        self.vision_model = vision_model
        self.platform = platform
        self.notes = []  # 文本缓存，类似 Agent-S 的 notes buffer

    def ground_action(self, action_plan: str, screenshot: bytes) -> str:
        """
        将高层动作计划 grounded 到具体坐标

        Args:
            action_plan: 来自 Worker Agent 的高层动作代码
            screenshot: 当前截图 bytes

        Returns:
            执行代码，已填入精确坐标
        """
        # 如果没有视觉模型，直接返回原计划
        if self.vision_model is None:
            return action_plan

        # 解析动作类型
        if "click" in action_plan:
            return self._ground_click(action_plan, screenshot)
        elif "type" in action_plan:
            return action_plan  # type 不需要 grounding
        elif "hotkey" in action_plan:
            return action_plan  # hotkey 不需要 grounding
        elif "scroll" in action_plan:
            return self._ground_scroll(action_plan, screenshot)
        else:
            return action_plan

    def _ground_click(self, action_plan: str, screenshot: bytes) -> str:
        """Grounding click 动作"""
        # 提取 x, y 占位符或描述
        match = re.search(r'click\([^,]+,\s*(\{[^}]+\}|\d+)\s*,\s*(\{[^}]+\}|\d+)', action_plan)
        
        if match:
            x_str, y_str = match.group(1), match.group(2)
            # 如果已经有具体数字，不需要 grounding
            try:
                int(x_str)
                int(y_str)
                return action_plan
            except ValueError:
                pass  # 需要 grounding

        # 调用视觉模型找坐标
        grounding_response = self.vision_model(
            screenshot,
            GROUNDING_PROMPT.format(action_plan=action_plan)
        )

        logger.info(f"Grounding response: {grounding_response}")

        # 解析坐标
        x_match = re.search(r"x:\s*(\d+)", grounding_response)
        y_match = re.search(r"y:\s*(\d+)", grounding_response)

        if x_match and y_match:
            x, y = int(x_match.group(1)), int(y_match.group(1))

            # 替换占位符或添加坐标
            if "{x}" in action_plan and "{y}" in action_plan:
                action_plan = action_plan.replace("{x}", str(x)).replace("{y}", str(y))
            else:
                # 替换已有坐标
                def replace_coord(m):
                    try:
                        int(m.group(1))
                        return m.group(0)  # 已有具体数字，不改
                    except:
                        return str(x) if "x" in m.group(0) else str(y)
                
                action_plan = re.sub(r'click\(([^,]+),\s*[^,\s]+\s*,\s*[^,\s]+', 
                                     lambda m: f'click({m.group(1)}, {x}, {y}', 
                                     action_plan, count=1)

        return action_plan

    def _ground_scroll(self, action_plan: str, screenshot: bytes) -> str:
        """Grounding scroll 动作 - 视具体 UI 而定，简化处理"""
        return action_plan

    def analyze_screenshot(self, screenshot: bytes, task: str) -> str:
        """
        用视觉模型分析截图
        参考 Agent-S 的 reflection 思路
        """
        if self.vision_model is None:
            return "No vision model available"

        prompt = f"""Analyze this screenshot for the task: {task}

Describe:
1. What applications/windows are visible
2. What is the current state
3. What would be a good next action
"""
        return self.vision_model(screenshot, prompt)
