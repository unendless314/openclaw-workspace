# Structured Prompt Template for Gemini Agent
# Copy and customize this template for consistent results
# For research tasks, explicitly mention which tools to use:
#   - google_web_search: for searching unknown information
#   - web_fetch: for reading specific URLs

---

## [ROLE]
You are a [researcher/writer/analyst/etc.] specializing in [domain].
Your expertise includes: [specific skills].

## [OBJECTIVE]
Primary Goal: [Clear, actionable goal]
Success Criteria: [How to know when done]
Constraints: [Time, format, scope limitations]

## [CONTEXT & REFERENCES]
### Background
[Relevant background information]

### Source Materials
- Document A: [path or URL]
- Document B: [path or URL]

### Previous Work
[Reference to prior related work, if any]

## [STRATEGY & FALLBACK PROTOCOL]
### Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Research Tasks - Explicit Tool Instructions
If the task requires web research, explicitly instruct:
- **To search for information** (unknown URLs):
  ```
  Use `google_web_search` to find [specific topic]
  ```
- **To read specific pages** (known URLs):
  ```
  Use `web_fetch` to read [URL]
  ```

### If Stuck
- Retry with different search terms
- Ask for clarification on specific points
- Document what was attempted and why it failed

### Quality Gates
- [ ] Verify all claims with sources
- [ ] Check for completeness
- [ ] Validate output format

## [OUTPUT FORMAT]

Structure:
```
# [Title]

## Summary
[Executive summary]

## Key Findings
1. [Finding 1]
2. [Finding 2]

## Details
[Full content]

## Sources
- [Source 1]
- [Source 2]
```

## [QUALITY CONTROL CHECKLIST]
Before completing, verify in your response:
- [ ] All objectives met
- [ ] Content is complete and comprehensive
- [ ] Format matches requirements
- [ ] No placeholder text remaining
- [ ] Sources cited where applicable

---
