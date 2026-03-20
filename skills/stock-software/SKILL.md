---
name: stock-software
description: 打开股票软件（同花顺、通达信等）。当用户要求打开股票行情软件、股票交易软件时使用此技能。
---

# 股票软件 Skill

## 已配置的软件路径

- **同花顺**: `C:\同花顺软件\同花顺\hexinlauncher.exe`
- **工作软件文件夹**: `C:\Users\changhaoyan\Desktop\工作软件`

## 打开方法

1. 首先确认 exec.host 配置为 "node"
2. 使用 PowerShell 在 Windows 节点上启动程序：

```powershell
powershell.exe -Command "Start-Process 'C:\同花顺软件\同花顺\hexinlauncher.exe'"
```

## 配置检查

如果 exec 失败，检查：
1. 节点是否已配对：`openclaw devices list`
2. exec.host 是否为 "node"：`openclaw config get tools.exec.host`
3. 如需要，改用 gateway host 并通过 WSL 执行

## 常见问题

- 如果报错 "command not found"，尝试完整路径
- 如果报错 "exec host not allowed"，修改配置并重启 gateway
