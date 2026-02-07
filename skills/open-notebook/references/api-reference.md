# Open Notebook API Reference

Complete API endpoint documentation.

## Base Information

- Base URL: `http://localhost:5055`
- API Prefix: `/api`
- Content-Type: `application/json`

## Endpoints by Category

### Notebooks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notebooks` | List all notebooks |
| POST | `/api/notebooks` | Create notebook |
| GET | `/api/notebooks/{id}` | Get notebook details |
| PUT | `/api/notebooks/{id}` | Update notebook |
| DELETE | `/api/notebooks/{id}` | Delete notebook |

**Create Notebook Request:**
```json
{
  "name": "Research Project",
  "description": "My research notes"
}
```

### Sources

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/sources` | List sources |
| POST | `/api/sources` | Create/upload source |
| GET | `/api/sources/{id}` | Get source |
| PUT | `/api/sources/{id}` | Update source |
| DELETE | `/api/sources/{id}` | Delete source |
| POST | `/api/sources/{id}/process` | Reprocess source |
| GET | `/api/sources/{id}/insights` | Get insights |

**Create Source (URL):**
```json
{
  "type": "url",
  "url": "https://example.com",
  "notebook_id": "notebook:abc123",
  "title": "Optional Title"
}
```

**Create Source (Text):**
```json
{
  "type": "text",
  "content": "Content here...",
  "notebook_id": "notebook:abc123"
}
```

**Upload File (multipart/form-data):**
- `file`: Binary file content
- `type`: "file"
- `notebook_id`: Optional notebook ID
- `transformations`: Optional JSON array of transformation IDs

### Notes

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notes` | List notes |
| POST | `/api/notes` | Create note |
| GET | `/api/notes/{id}` | Get note |
| PUT | `/api/notes/{id}` | Update note |
| DELETE | `/api/notes/{id}` | Delete note |

**Create Note:**
```json
{
  "title": "My Note",
  "content": "Note content...",
  "note_type": "human",
  "notebook_id": "notebook:abc123"
}
```

### Search

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/search` | Search knowledge base |
| POST | `/api/search/ask` | AI Q&A (streaming) |
| POST | `/api/search/ask/simple` | AI Q&A (simple) |

**Search Request:**
```json
{
  "query": "search term",
  "type": "text",
  "limit": 100,
  "search_sources": true,
  "search_notes": true,
  "minimum_score": 0.2
}
```

**Ask Request:**
```json
{
  "question": "What is the main topic?",
  "strategy_model": "model:gemini-pro",
  "answer_model": "model:gemini-pro",
  "final_answer_model": "model:gemini-pro"
}
```

### Transformations

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/transformations` | List transformations |
| POST | `/api/transformations` | Create transformation |
| POST | `/api/transformations/execute` | Execute transformation |
| GET | `/api/transformations/{id}` | Get transformation |
| PUT | `/api/transformations/{id}` | Update transformation |
| DELETE | `/api/transformations/{id}` | Delete transformation |

**Create Transformation:**
```json
{
  "name": "summarize",
  "title": "Summarize Content",
  "description": "Generate a summary",
  "prompt": "Summarize the following content in 3 bullet points: {input}",
  "apply_default": false
}
```

### Models

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/models` | List models |
| POST | `/api/models` | Add model |
| GET | `/api/models/{id}` | Get model |
| DELETE | `/api/models/{id}` | Delete model |

### Podcasts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/podcasts` | List podcasts |
| POST | `/api/podcasts` | Create podcast |
| GET | `/api/podcasts/{id}` | Get podcast |
| GET | `/api/podcasts/{id}/audio` | Download audio |

**Create Podcast:**
```json
{
  "name": "Episode 1",
  "content": "Content to convert to podcast...",
  "episode_profile": "default",
  "speaker_profile": "default"
}
```

### Commands

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/commands` | List commands |
| GET | `/api/commands/{id}` | Get command status |
| POST | `/api/commands/{id}/cancel` | Cancel command |

**Command Status Response:**
```json
{
  "job_id": "cmd:abc123",
  "status": "completed",
  "result": {...},
  "error_message": null,
  "progress": 100
}
```

## Python Client Example

```python
import httpx
import os

class OpenNotebookClient:
    def __init__(self, base_url=None, password=None):
        self.base_url = base_url or os.getenv("OPEN_NOTEBOOK_URL", "http://localhost:5055")
        self.password = password or os.getenv("OPEN_NOTEBOOK_PASSWORD")
        self.headers = {}
        if self.password:
            self.headers["Authorization"] = f"Bearer {self.password}"
    
    def search(self, query, search_type="text"):
        with httpx.Client() as client:
            resp = client.post(
                f"{self.base_url}/api/search",
                json={"query": query, "type": search_type},
                headers=self.headers
            )
            return resp.json()
```

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request - Invalid input |
| 404 | Not Found - Resource doesn't exist |
| 500 | Server Error - Internal error |
