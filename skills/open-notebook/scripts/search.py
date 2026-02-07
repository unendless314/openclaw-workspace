#!/usr/bin/env python3
"""
Search Open Notebook knowledge base.
"""

import argparse
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Search Open Notebook knowledge base")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--type", "-t", choices=["text", "vector"], default="text",
                       help="Search type (default: text)")
    parser.add_argument("--limit", "-l", type=int, default=20, help="Max results")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    parser.add_argument("--notebook", "-n", help="Filter by notebook ID")
    
    args = parser.parse_args()
    
    client = OpenNotebookClient()
    
    try:
        print(f"Searching for: '{args.query}' ({args.type} search)")
        results = client.search(args.query, args.type, args.limit)
        
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
            return
        
        # Pretty print results
        items = results.get("results", [])
        total = results.get("total_count", len(items))
        
        print(f"\nFound {total} results:\n")
        print("-" * 60)
        
        for i, item in enumerate(items, 1):
            source_type = item.get("type", "unknown")
            title = item.get("title", "Untitled")
            content = item.get("content", "")[:200]
            score = item.get("score", "N/A")
            
            print(f"{i}. [{source_type.upper()}] {title}")
            if args.type == "vector":
                print(f"   Score: {score}")
            if content:
                print(f"   Preview: {content}...")
            print()
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
