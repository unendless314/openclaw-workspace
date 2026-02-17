--- 
name: gemini-agent
version: "1.0"
description: Delegate standalone cognitive tasks to the Google Gemini agent while you handle orchestration. Saves outputs directly to your workspace for iterative processing and track status with unified execution wrapper.
metadata: {"openclaw":{"emoji":"♊️","requires":{"bins":["gemini"]}}}
---

# Workflow Strategy

Delegate planning, research, drafting, and analysis to the Google Gemini agent. Best suited for background tasks where high latency is acceptable.

Begin with a concise checklist (3-7 bullets) of planned sub-tasks before delegating any multi-step task to Gemini; keep checklist items conceptual rather than implementation-level.

Always validate outputs after each major workflow step; if critical results are missing, self-correct or flag for review before presenting to the user.

**Important Note**: Gemini agent cannot write files due to environment limitations. Always use the wrapper script to capture Gemini's output to the specified file path.

```
User Request
    ↓
[You] Analyze & Plan
    ↓
[You] Delegate to Gemini (if appropriate)
    ↓
[Gemini] Execute & Report
    ↓
[Script] Save Results (via wrapper)
    ↓
[You] Synthesize & Add Value
    ↓
[You] Present to User
```

## Execution Script

This skill includes `scripts/gemini-run.sh` which provides:
- **Guaranteed file output** - Never lose results due to execution method inconsistencies
- **Status tracking** - `.status` files show progress (pending/running/completed/failed)
- **Timing metrics** - Duration tracking for each task
- **Background support** - Proper PID management and monitoring
- **File protection** - Output files are locked as read-only (`chmod 444`) after generation to prevent accidental overwrites. ⚠️ **Never edit the original output file directly** - extract content to a different file instead.

## Usage

```bash
# Foreground execution
bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Your prompt' 'workspace/gemini/out/topic/output.md'"

# Background execution
bash background:true command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Your prompt' 'workspace/gemini/out/topic/output.md'"

# Retry with exponential backoff for important task（capped at 5）
bash workspace/skills/gemini-agent/scripts/gemini-run.sh --max-retries 5 "Your prompt" "output.md"
```

## Critical Constraints

1. **HIGH LATENCY**: Expect 30s for simple queries, 4-8min for research/writing tasks
   - Simple Q&A: 30-60s
   - Analysis/Structuring: 60-180s
   - Web Research: 3-5min (includes search + reading)
   - Research + Drafting: 4-8min
2. **RATE LIMITING**: Free tier 1000 calls/day—avoid mass concurrent jobs.
3. **ALWAYS USE WRAPPER**: Never call `gemini` directly without wrapper

### Timeout Guidelines

Set appropriate timeouts based on task complexity:

```bash
# Quick queries
bash command:"..." timeout:60

# Analysis tasks
bash command:"..." timeout:180

# Research tasks
bash command:"..." timeout:300

# Complex multi-step tasks
bash command:"..." timeout:600
```

**Be patient**—complex tasks legitimately take 3-5 minutes. Premature termination wastes work and quota.

## Directory Structure

```
workspace/
└── gemini/
    ├── ingest/          # Original input/initial output
    │   └── {topic-slug}/
    │       └── raw.md
    ├── draft/           # Intermediate/iterative drafts
    │   └── {topic-slug}/
    │       ├── step01-structure.md
    │       └── step02-refined.md
    └── out/             # Final deliverables
        └── {topic-slug}/
            ├── final-report.md
            └── implementation-plan.md
```

**Naming conventions:**
- `slug`: kebab-case (e.g., `quantum-entanglement`, `react-router-migration`)
- iteration files: `step{N}.md` (e.g., `step01.md`, `step02.md`)

### Simple Task (One-shot)

```bash
bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Research 2025 AI trends' 'workspace/gemini/out/ai-2025-trends/output.md'"
```

### Background Task

```bash
bash background:true command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Complex analysis' 'workspace/gemini/out/analysis/result.md'"

# Monitor with process tool
process action:list
process action:log sessionId:XXX
```

### Multi-step Workflow

```bash
# Step 1: Ingest
bash background:true command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Research [topic]' 'workspace/gemini/ingest/[topic]/raw.md'"

# Step 2: Structure (after step 1 completes)
bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Read workspace/gemini/ingest/[topic]/raw.md, structure content' 'workspace/gemini/draft/[topic]/step01.md'"

# Step 3: Finalize
bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Read workspace/gemini/draft/[topic]/step01.md, generate final report' 'workspace/gemini/out/[topic]/final.md'"
```

## Structured Prompting (Recommended)

For best results with Gemini, use a **structured prompt format** to maximize compliance:

```
[ROLE]
Define who Gemini should be (researcher, coder, analyst, etc.)

[OBJECTIVE]
Clear, actionable goal with success criteria

[CONTEXT & REFERENCES]
Background info and source materials

[STRATEGY & FALLBACK PROTOCOL]
Step-by-step approach and what to do if stuck
- For research: explicitly mention `google_web_search` or `web_fetch`

[OUTPUT FORMAT]
Explicit file path and expected structure

[QUALITY CONTROL CHECKLIST]
Verification steps before completing
```

### Available Tools

Gemini Agent has access to these tools when explicitly instructed:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `google_web_search` | Search Google for information | When you need to find unknown information |
| `web_fetch` | Read specific webpage content | When you have a known URL to read |

See [references/structured-prompt-template.md](references/structured-prompt-template.md) for a reusable template.

## Output Format

All outputs are saved as Markdown files with clear **Prompt-Response** structure:

```markdown
# Gemini Agent 對話記錄

---

## Prompt

Your original prompt text here...

---

## Response

Gemini's response here...

---

*生成時間: 2026-02-01T19:51:17+08:00*  
*耗時: 51秒*
*成功嘗試: 第 2 次*
```

This format ensures:
- **Full context preservation** - Both question and answer are recorded
- **Chain of thought support** - Future iterations can reference the original prompt
- **Debugging clarity** - Easy to trace what was asked vs what was returned

## Status Checking

After any execution, check status:

```bash
# Check status file
cat workspace/gemini/out/topic/output.md.status

# Example output:
# started_at: 2026-02-01T19:00:00+08:00
# status: completed
# output_file: /home/openclaw/.openclaw/workspace/gemini/out/topic/output.md
# completed_at: 2026-02-01T19:01:30+08:00
# duration_seconds: 90
# exit_code: 0

# Read actual output (includes both prompt and response)
cat workspace/gemini/out/topic/output.md
```

## Error Handling

If status shows `failed`:
1. Check `exit_code` in .status file
2. Read output file - it contains stderr messages
3. Common issues:
   - Exit code 1: Rate limit exceeded (wait and retry)
   - No output: Network issues or API unavailable

## Anti-patterns to Avoid

| Inefficient | Efficient |
|-----------------|----------------------------|
| `gemini "Analyze report"` (no output file) | Use wrapper script with explicit output path |
| Wrapper script saves to `/tmp/` | Wrapper script saves to `workspace/gemini/...` |
| Sequential jobs without background | Use `background:true` for parallel execution |
| "Research python-pptx" (may not use tools) | "Use `google_web_search` to find python-pptx documentation and tutorials" |
| Editing the original output file directly | Extract content to a different file |

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for common issues and solutions.

## Suitable Scenarios

**Best suited for:**
- Multi-step research or analysis (supports iteration)
- Complex tasks with intermediate result storage
- Large-scale parallel document handling
- Workflows requiring repeated access to historical results

**Not recommended for:**
- Real-time interaction (latency is too high)
- Single, trivial queries (cost/complexity not justified)

---

