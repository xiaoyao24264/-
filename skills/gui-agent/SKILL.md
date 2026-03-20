# GUI Agent Skill - 视觉 GUI 控制智能体

让 AI 像人类一样通过屏幕截图理解界面并执行操作。

## 核心流程

```
用户指令 → 截图 → 视觉模型理解 → Grounding(生成坐标) → PyAutoGUI执行 → 循环
```

## 文件结构

- `SKILL.md` - 本文件，说明
- `agent.py` - GUI Agent 主循环
- `grounder.py` - 视觉→坐标 grounding 模块
- `executor.py` - PyAutoGUI 执行器
- `prompts.py` - 提示词模板

## 依赖

- `pyautogui` - Windows 上需要安装
- 视觉模型 API（MiniMax / GPT-4V / Claude 等）

## 使用方式

```python
from agent import GUIAgent

agent = GUIAgent(
    instruction="打开记事本并输入 hello",
    ssh_host="172.20.48.1",
    ssh_user="changhaoyan",
)
agent.run()
```

## 参考

Agent-S (simular-ai/Agent-S) 架构借鉴：
- Worker Agent: 负责任务规划和动作生成
- Grounding Agent: 将动作翻译成精确坐标
- Reflection: 事后验证动作效果
