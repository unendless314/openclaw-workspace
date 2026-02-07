#!/usr/bin/env python3
"""
Upload source to Open Notebook.
Supports files, URLs, and text content.
"""

import argparse
import sys
import os

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Upload content to Open Notebook")
    parser.add_argument("--file", "-f", help="Path to file to upload")
    parser.add_argument("--url", "-u", help="URL to add as source")
    parser.add_argument("--text", "-t", help="Text content to add")
    parser.add_argument("--notebook", "-n", help="Notebook name or ID")
    parser.add_argument("--title", help="Source title")
    parser.add_argument("--transformations", help="Comma-separated transformation IDs to apply")
    parser.add_argument("--wait", "-w", action="store_true", help="Wait for processing to complete")
    
    args = parser.parse_args()
    
    if not any([args.file, args.url, args.text]):
        parser.error("Must provide --file, --url, or --text")
    
    client = OpenNotebookClient()
    
    # Resolve notebook ID from name if provided
    notebook_id = None
    if args.notebook:
        notebooks = client.list_notebooks()
        for nb in notebooks:
            if nb.get("name") == args.notebook or nb.get("id") == args.notebook:
                notebook_id = nb.get("id")
                break
        if not notebook_id:
            print(f"Notebook '{args.notebook}' not found. Creating new notebook...")
            nb = client.create_notebook(args.notebook)
            notebook_id = nb.get("id")
            print(f"Created notebook: {notebook_id}")
    
    # Parse transformations
    transformation_ids = None
    if args.transformations:
        transformation_ids = [t.strip() for t in args.transformations.split(",")]
    
    # Upload content
    try:
        if args.file:
            if not os.path.exists(args.file):
                print(f"Error: File not found: {args.file}", file=sys.stderr)
                sys.exit(1)
            
            print(f"Uploading file: {args.file}")
            result = client.upload_file(args.file, notebook_id, transformation_ids)
            print(f"File uploaded successfully!")
            print(f"Source ID: {result.get('id')}")
            
        elif args.url:
            print(f"Adding URL: {args.url}")
            result = client.create_url_source(args.url, notebook_id, args.title)
            print(f"URL source created!")
            print(f"Source ID: {result.get('id')}")
            
        elif args.text:
            print(f"Adding text content...")
            result = client.create_text_source(args.text, notebook_id, args.title)
            print(f"Text source created!")
            print(f"Source ID: {result.get('id')}")
        
        # Show processing status if available
        if isinstance(result, dict):
            if "source_id" in result:
                print(f"Processing: {result.get('source_id')}")
            if "job_id" in result and args.wait:
                print(f"Waiting for job: {result.get('job_id')}")
                # TODO: Implement polling
                
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
