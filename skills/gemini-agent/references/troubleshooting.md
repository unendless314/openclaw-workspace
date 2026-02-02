# Gemini Agent Troubleshooting

## Common Issues and Solutions

### Issue: "You have exhausted your capacity on this model"

**Symptom:**
```
Attempt 1 failed: You have exhausted your capacity on this model. 
Your quota will reset after 0s.. Retrying after 715.990087ms...
```

**Cause:** Gemini free tier daily quota (1000 calls/day) exceeded.

**Solution:**
1. Wait for quota reset (usually within 24 hours)
2. Check status file for `failed` status
3. Retry the task after some time

### Issue: No output in file but status shows "completed"

**Symptom:**
- Status file shows `status: completed`
- Output file exists but is empty

**Cause:** Gemini returned empty response (rare but possible).

**Solution:**
1. Check if prompt was too vague or empty
2. Retry with more specific prompt
3. Check Gemini service status

### Issue: Background task not starting

**Symptom:**
```
❌ 背景任務啟動失敗
```

**Cause:** Script failed validation or gemini binary not found.

**Solution:**
1. Verify gemini is installed: `which gemini`
2. Check if output directory is writable
3. Review prompt syntax (no unescaped quotes)

### Issue: Process killed before completion

**Symptom:**
- Status file shows `status: failed`
- No `completed_at` or `failed_at` timestamp

**Cause:** Task was manually terminated or timed out.

**Solution:**
1. Check if user requested termination
2. For long tasks, increase timeout or break into smaller chunks
3. Use `process action:log` to see last output before termination

### Issue: Permission denied when running wrapper

**Symptom:**
```
bash: workspace/skills/gemini-agent/scripts/gemini-run.sh: Permission denied
```

**Solution:**
```bash
chmod +x workspace/skills/gemini-agent/scripts/gemini-run.sh
```

## Status File Reference

### Status Values

| Status | Meaning | Action |
|--------|---------|--------|
| `pending` | Task initialized, not started | Wait for update |
| `running` | Gemini is processing | Monitor with `process action:log` |
| `completed` | Task finished successfully | Read output file |
| `failed` | Task failed | Check `exit_code` and output file |

### Status File Fields

```yaml
started_at: 2026-02-01T19:00:00+08:00    # ISO timestamp
status: completed                          # pending/running/completed/failed
output_file: /path/to/output.md           # Absolute path
duration_seconds: 90                      # Wall clock time
completed_at: 2026-02-01T19:01:30+08:00  # ISO timestamp (if completed)
exit_code: 0                              # 0=success, non-zero=failure
pid: 12345                                # Background process ID (if applicable)
```

## Best Practices

1. **Always check status** before reading output
2. **Use absolute paths** for output files when possible
3. **Monitor background tasks** with `process action:list`
4. **Use descriptive slugs** for topic directories

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (often rate limit) |
| 2 | Misuse of command (syntax error) |
| 126 | Command not executable |
| 127 | Command not found |
| 130 | Interrupted (Ctrl+C) |
| 137 | Killed (OOM or manual) |
