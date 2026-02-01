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

## Custom Skills

### gemini-agent

位於 `workspace/skills/gemini-agent/`，提供統一的 Gemini Agent 執行 wrapper。

需要委派任務給 Gemini 時，優先使用此 skill 而非官方 gemini skill。

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

> ⚠️ **注意**: 這是這台 Linux 機器的特定配置。如果換到 Mac/Windows，小林可能會回到 GitHub Desktop 操作，屆時需要重新確認他的偏好。

---

Add whatever helps you do your job. This is your cheat sheet.
