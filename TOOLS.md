# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

### 股票软件

- 同花顺 → C:\同花顺软件\同花顺\hexinlauncher.exe
- 工作软件文件夹 → C:\Users\changhaoyan\Desktop\工作软件

### WeGame
- 路径：`C:\Program Files (x86)\WeGame\wegame.exe`

### 云服务器
- IP: 134.175.217.108
- 用户名: root
- 密码: （问少爷）
- SSH Windows 跳板机: `172.20.48.1` / `changhaoyan`

### SSH Windows 连接

- Windows IP: `172.20.48.1`
- 用户名: `changhaoyan`

#### 打开同花顺（正确方式）
```bash
ssh changhaoyan@172.20.48.1 "schtasks /create /tn \"OpenTHS\" /tr \"C:\同花顺软件\同花顺\hexin.exe\" /sc once /st 23:59 /f && schtasks /run /tn \"OpenTHS\""
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
