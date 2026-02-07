#!/usr/bin/env python3
"""
Open Notebook API Client
Base client for interacting with Open Notebook API.
"""

import os
import sys
from typing import Optional, Dict, Any, List
import httpx


class OpenNotebookClient:
    """Client for Open Notebook API."""
    
    def __init__(self, base_url: Optional[str] = None, password: Optional[str] = None):
        self.base_url = (base_url or os.getenv("OPEN_NOTEBOOK_URL", "http://localhost:5055")).rstrip("/")
        self.password = password or os.getenv("OPEN_NOTEBOOK_PASSWORD")
        self.headers = {}
        if self.password:
            self.headers["Authorization"] = f"Bearer {self.password}"
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make HTTP request to API."""
        url = f"{self.base_url}/api{endpoint}"
        headers = {**self.headers, **kwargs.pop("headers", {})}
        
        try:
            with httpx.Client(timeout=300.0) as client:
                response = client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response.json() if response.content else {}
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error {e.response.status_code}: {e.response.text}", file=sys.stderr)
            raise
        except httpx.RequestError as e:
            print(f"Request Error: {e}", file=sys.stderr)
            raise
    
    # Notebooks
    def list_notebooks(self) -> List[Dict]:
        """List all notebooks."""
        return self._request("GET", "/notebooks")
    
    def create_notebook(self, name: str, description: str = "") -> Dict:
        """Create a new notebook."""
        return self._request("POST", "/notebooks", json={"name": name, "description": description})
    
    def get_notebook(self, notebook_id: str) -> Dict:
        """Get notebook details."""
        return self._request("GET", f"/notebooks/{notebook_id}")
    
    # Sources
    def list_sources(self) -> List[Dict]:
        """List all sources."""
        return self._request("GET", "/sources")
    
    def create_url_source(self, url: str, notebook_id: Optional[str] = None, title: Optional[str] = None) -> Dict:
        """Create a URL source."""
        data = {"type": "url", "url": url}
        if notebook_id:
            data["notebook_id"] = notebook_id
        if title:
            data["title"] = title
        return self._request("POST", "/sources", json=data)
    
    def create_text_source(self, content: str, notebook_id: Optional[str] = None, title: Optional[str] = None) -> Dict:
        """Create a text source."""
        data = {"type": "text", "content": content}
        if notebook_id:
            data["notebook_id"] = notebook_id
        if title:
            data["title"] = title
        return self._request("POST", "/sources", json=data)
    
    def upload_file(self, file_path: str, notebook_id: Optional[str] = None, 
                    transformations: Optional[List[str]] = None) -> Dict:
        """Upload a file source."""
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f)}
            data = {"type": "file"}
            if notebook_id:
                data["notebook_id"] = notebook_id
            if transformations:
                import json
                data["transformations"] = json.dumps(transformations)
            
            # Use data and files separately for multipart
            return self._request("POST", "/sources", data=data, files=files)
    
    def get_source(self, source_id: str) -> Dict:
        """Get source details."""
        return self._request("GET", f"/sources/{source_id}")
    
    # Notes
    def list_notes(self, notebook_id: Optional[str] = None) -> List[Dict]:
        """List notes, optionally filtered by notebook."""
        params = {}
        if notebook_id:
            params["notebook_id"] = notebook_id
        return self._request("GET", "/notes", params=params)
    
    def create_note(self, content: str, title: Optional[str] = None, 
                    notebook_id: Optional[str] = None, note_type: str = "human") -> Dict:
        """Create a new note."""
        data = {"content": content, "note_type": note_type}
        if title:
            data["title"] = title
        if notebook_id:
            data["notebook_id"] = notebook_id
        return self._request("POST", "/notes", json=data)
    
    # Search
    def search(self, query: str, search_type: str = "text", limit: int = 100) -> Dict:
        """Search knowledge base."""
        return self._request("POST", "/search", json={
            "query": query,
            "type": search_type,
            "limit": limit,
            "search_sources": True,
            "search_notes": True
        })
    
    def ask(self, question: str, model_id: Optional[str] = None) -> Dict:
        """Ask the knowledge base (simple mode)."""
        # Get default model if not specified
        if not model_id:
            models = self.list_models()
            for m in models:
                if m.get("provider") == "gemini" or "gemini" in m.get("model_name", "").lower():
                    model_id = m.get("id")
                    break
            if not model_id and models:
                model_id = models[0].get("id")
        
        return self._request("POST", "/search/ask/simple", json={
            "question": question,
            "strategy_model": model_id,
            "answer_model": model_id,
            "final_answer_model": model_id
        })
    
    # Transformations
    def list_transformations(self) -> List[Dict]:
        """List all transformations."""
        return self._request("GET", "/transformations")
    
    def create_transformation(self, name: str, title: str, description: str, 
                              prompt: str, apply_default: bool = False) -> Dict:
        """Create a transformation."""
        return self._request("POST", "/transformations", json={
            "name": name,
            "title": title,
            "description": description,
            "prompt": prompt,
            "apply_default": apply_default
        })
    
    def execute_transformation(self, transformation_id: str, input_text: str, 
                               model_id: Optional[str] = None) -> Dict:
        """Execute a transformation."""
        if not model_id:
            models = self.list_models()
            if models:
                model_id = models[0].get("id")
        
        return self._request("POST", "/transformations/execute", json={
            "transformation_id": transformation_id,
            "input_text": input_text,
            "model_id": model_id
        })
    
    # Models
    def list_models(self) -> List[Dict]:
        """List all AI models."""
        return self._request("GET", "/models")
    
    # Commands (Background jobs)
    def get_command(self, command_id: str) -> Dict:
        """Get command status."""
        return self._request("GET", f"/commands/{command_id}")
    
    # Podcasts
    def list_podcasts(self) -> List[Dict]:
        """List all podcasts."""
        return self._request("GET", "/podcasts")
    
    def create_podcast(self, name: str, content: str, episode_profile: str = "default",
                       speaker_profile: str = "default") -> Dict:
        """Create a podcast."""
        return self._request("POST", "/podcasts", json={
            "name": name,
            "content": content,
            "episode_profile": episode_profile,
            "speaker_profile": speaker_profile
        })


if __name__ == "__main__":
    # Test connection
    client = OpenNotebookClient()
    try:
        notebooks = client.list_notebooks()
        print(f"Connected! Found {len(notebooks)} notebooks")
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1)
