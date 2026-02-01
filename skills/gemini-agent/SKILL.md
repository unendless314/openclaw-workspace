--- 
name: gemini-agent
version: "1.0"
description: Delegate standalone cognitive tasks to the Google Gemini agent while you handle orchestration. Saves outputs directly to your workspace for iterative processing and track status with unified execution wrapper.
metadata: {"openclaw":{"emoji":"♊️","requires":{"bins":["gemini"]}}}
---

# Workflow Strategy

Delegate planning, research, drafting, and analysis to the Google Gemini agent. Best suited for background tasks where high latency is acceptable.

Begin with a concise checklist (3-7 bullets) of planned sub-tasks before delegating any multi-step task to Gemini; keep checklist items conceptual rather than implementation-level.

```
User Request
    ↓
[You] Analyze & Plan
    ↓
[You] Delegate to Gemini (if appropriate)
    ↓
[Gemini] Execute & Save Results
    ↓
[You] Synthesize & Add Value
    ↓
[You] Present to User
```

---

## Unified Execution

This skill includes `scripts/gemini-run.sh` which provides:
- **Guaranteed file output** - Never lose results due to execution method inconsistencies
- **Status tracking** - `.status` files show progress (pending/running/completed/failed)
- **Timing metrics** - Duration tracking for each task
- **Background support** - Proper PID management and monitoring

## Usage

```bash
# Foreground execution
bash command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Your prompt' 'workspace/gemini/out/topic/output.md'"

# Background execution
bash background:true command:"workspace/skills/gemini-agent/scripts/gemini-run.sh 'Your prompt' 'workspace/gemini/out/topic/output.md'"
```

## Critical Constraints

1. **HIGH LATENCY**: 30-120s per call
2. **RATE LIMITING**: Free tier 1000 calls/day—avoid mass concurrent jobs.
3. **ALWAYS USE WRAPPER**: Never call `gemini` directly without wrapper

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

## Execution Patterns

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
| `gemini "..." > file.md` (direct redirect) | Use wrapper script (guaranteed output) |
| Save to `/tmp/` | Save to `workspace/gemini/...` |
| Sequential jobs without background | Use `background:true` for parallel execution |

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

**Core Principle:**
1. Delegate appropriate user requests to Gemini for background execution, saving outputs to the workspace for later retrieval and synthesis.
2. Always validate outputs after each major workflow step; if critical results are missing, self-correct or flag for review before presenting to the user.
3. Always use the wrapper script for reliable execution. The wrapper ensures output consistency and provides debugging capabilities through status tracking.
