# LEARNINGS.md

Log corrections, knowledge gaps, and best practices here.

## Format

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details
Full context

### Suggested Action
Specific fix

### Metadata
- Source: conversation | error | user_feedback
- Related Files: 
- Tags: 
- See Also: 
```

## [LRN-20260317-001] config

**Logged**: 2026-03-17T14:30:00+08:00
**Priority**: high
**Status**: pending
**Area**: config

### Summary
WSL Gateway 无法直接执行 Windows 程序，节点 system.run 未启用

### Details
Gateway 运行在 WSL (Linux) 环境，无法直接执行 Windows .exe 文件。通过节点执行需要节点支持 system.run 功能，但当前节点未启用此功能。

### Suggested Action
1. 在 Windows 上安装 OpenClaw 节点应用并启用 system.run
2. 或使用其他方式（如 SSH）从 WSL 调用 Windows 程序

### Metadata
- Source: error
- Related Files: ~/.openclaw/openclaw.json
- See Also: node-connect skill
