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

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Skill 使用偏好

遇到對應任務時，依此優先順序選用：

1. **gemini-agent** - 研究、寫作、分析類任務首選
2. **doc-coediting** - 文件協作、PRD、RFC 起草
3. **kimi-agent** - 程式碼實作、除錯、審查
4. **ai-project-architecture** - 專案架構設計、模組拆分

### 使用習慣
- 偏好委派給子 agent，而非 main session 直接執行
- 務必使用 SKILL.md 文檔中指定的 cli 腳本呼叫專用 agent

---

## Custom Skills 位置

- **gemini-agent**: `workspace/skills/gemini-agent/` - 統一的 Gemini Agent 執行 wrapper

---

## Git / GitHub Setup (本機專用)

### 這台機器的 Git 配置

- **GitHub CLI (`gh`)** 已安裝並登入為 `unendless314`
- **認證方式**: 透過 `gh auth login` 設定，儲存在系統金鑰庫
- **倉庫位置**: `~/.openclaw/workspace/`
- **遠端**: `https://github.com/unendless314/openclaw-workspace.git`

### 常用指令

```bash
cd ~/.openclaw/workspace
git add .
git commit -m "更新說明"
git push
```

---

Add whatever helps you do your job. This is your cheat sheet.
