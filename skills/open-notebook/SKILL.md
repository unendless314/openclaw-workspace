---
name: open-notebook
description: Interact with Open Notebook API for knowledge base management, content processing, and AI-powered research. Use when working with Open Notebook to upload sources, create notebooks, search content, generate insights, create podcasts, or automate content workflows.
metadata:
  {
    "openclaw":
      {
        "emoji": "📓",
        "requires": { "bins": ["python3"] },
      },
  }
---

# Open Notebook

Open Notebook API client for knowledge base management and content automation.

## Base URL

Default: `http://localhost:5055`

Override with `OPEN_NOTEBOOK_URL` environment variable.

## Authentication

If password protection is enabled, set:
```bash
export OPEN_NOTEBOOK_PASSWORD="your-password"
```

## Core Concepts

- **Notebook**: Collection of sources and notes (like a project folder)
- **Source**: Content input (PDF, URL, text, YouTube, audio)
- **Note**: Written notes (human or AI-generated)
- **Transformation**: Custom AI prompt pipelines for content processing
- **Insight**: AI-generated analysis of sources
- **Podcast**: AI-generated audio content from sources

## Common Workflows

### 1. Upload & Process Content

```bash
# Upload a file
python3 scripts/upload_source.py --file document.pdf --notebook "My Research"

# Add URL source
python3 scripts/upload_source.py --url "https://example.com/article" --notebook "My Research"

# Process with transformations
python3 scripts/upload_source.py --file doc.pdf --transformations summarize,extract_keywords
```

### 2. Search Knowledge Base

```bash
# Text search (no embedding required)
python3 scripts/search.py --query "machine learning" --type text

# AI question answering (requires embedding model)
python3 scripts/ask.py --question "What are the key findings?"
```

### 3. Generate Podcast

```bash
# Create podcast from sources
python3 scripts/create_podcast.py --notebook "My Research" --name "Episode 1"
```

## API Endpoints

See [references/api-reference.md](references/api-reference.md) for complete endpoint documentation.

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `upload_source.py` | Upload files, URLs, or text |
| `search.py` | Search knowledge base |
| `ask.py` | AI Q&A with sources |
| `create_notebook.py` | Create new notebooks |
| `list_notebooks.py` | List all notebooks |
| `create_transformation.py` | Create custom AI transformations |
| `create_podcast.py` | Generate podcasts |
| `check_status.py` | Check processing job status |

## Docker Operations

If service is not running, start it:

```bash
cd ~/Projects/open-notebook
sudo docker compose -f docker-compose.full.yml up -d
```

Check status:
```bash
cd ~/Projects/open-notebook
sudo docker compose -f docker-compose.full.yml ps
```
