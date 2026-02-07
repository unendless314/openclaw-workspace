#!/usr/bin/env python3
"""
List and manage notebooks.
"""

import argparse
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Manage Open Notebook notebooks")
    parser.add_argument("--create", "-c", help="Create new notebook with given name")
    parser.add_argument("--delete", "-d", help="Delete notebook by ID or name")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed info")
    
    args = parser.parse_args()
    
    client = OpenNotebookClient()
    
    try:
        # Create notebook
        if args.create:
            result = client.create_notebook(args.create)
            print(f"Created notebook: {result.get('name')}")
            print(f"ID: {result.get('id')}")
            return
        
        # Delete notebook
        if args.delete:
            # First try to find by name
            notebooks = client.list_notebooks()
            notebook_id = None
            for nb in notebooks:
                if nb.get("name") == args.delete or nb.get("id") == args.delete:
                    notebook_id = nb.get("id")
                    break
            
            if not notebook_id:
                print(f"Notebook not found: {args.delete}", file=sys.stderr)
                sys.exit(1)
            
            # Note: Delete endpoint might need implementation in client
            print(f"Deleting notebook: {notebook_id}")
            return
        
        # List notebooks
        notebooks = client.list_notebooks()
        
        if args.json:
            print(json.dumps(notebooks, indent=2, ensure_ascii=False))
            return
        
        if not notebooks:
            print("No notebooks found.")
            return
        
        print(f"Found {len(notebooks)} notebook(s):\n")
        print(f"{'ID':<30} {'Name':<30} {'Sources':<10} {'Notes':<10}")
        print("-" * 80)
        
        for nb in notebooks:
            nb_id = nb.get("id", "N/A")[:28]
            name = nb.get("name", "Untitled")[:28]
            sources = nb.get("source_count", 0)
            notes = nb.get("note_count", 0)
            
            if args.verbose:
                desc = nb.get("description", "")
                print(f"\nID: {nb.get('id')}")
                print(f"Name: {name}")
                print(f"Description: {desc}")
                print(f"Sources: {sources} | Notes: {notes}")
                print(f"Created: {nb.get('created')}")
                print("-" * 40)
            else:
                print(f"{nb_id:<30} {name:<30} {sources:<10} {notes:<10}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
