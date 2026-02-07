#!/usr/bin/env python3
"""
Create and execute AI transformations.
"""

import argparse
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Manage transformations")
    parser.add_argument("--list", "-l", action="store_true", help="List all transformations")
    parser.add_argument("--create", "-c", action="store_true", help="Create new transformation")
    parser.add_argument("--name", help="Transformation name")
    parser.add_argument("--title", help="Transformation title")
    parser.add_argument("--description", help="Transformation description")
    parser.add_argument("--prompt", help="Transformation prompt template")
    parser.add_argument("--execute", "-e", help="Execute transformation by ID or name")
    parser.add_argument("--input", "-i", help="Input text or file path")
    parser.add_argument("--model", "-m", help="Model ID to use")
    parser.add_argument("--json", "-j", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    client = OpenNotebookClient()
    
    try:
        # List transformations
        if args.list:
            transformations = client.list_transformations()
            
            if args.json:
                print(json.dumps(transformations, indent=2, ensure_ascii=False))
                return
            
            if not transformations:
                print("No transformations found.")
                return
            
            print(f"Found {len(transformations)} transformation(s):\n")
            for t in transformations:
                print(f"ID: {t.get('id')}")
                print(f"Name: {t.get('name')}")
                print(f"Title: {t.get('title')}")
                print(f"Description: {t.get('description')}")
                print(f"Default: {'Yes' if t.get('apply_default') else 'No'}")
                print("-" * 40)
            return
        
        # Create transformation
        if args.create:
            if not all([args.name, args.title, args.prompt]):
                print("Error: --name, --title, and --prompt are required for creation", file=sys.stderr)
                sys.exit(1)
            
            result = client.create_transformation(
                name=args.name,
                title=args.title,
                description=args.description or "",
                prompt=args.prompt,
                apply_default=False
            )
            print(f"Created transformation: {result.get('name')}")
            print(f"ID: {result.get('id')}")
            return
        
        # Execute transformation
        if args.execute:
            # Find transformation by name or ID
            transformations = client.list_transformations()
            trans_id = None
            for t in transformations:
                if t.get("name") == args.execute or t.get("id") == args.execute:
                    trans_id = t.get("id")
                    break
            
            if not trans_id:
                print(f"Transformation not found: {args.execute}", file=sys.stderr)
                sys.exit(1)
            
            # Get input
            input_text = args.input
            if not input_text:
                print("Error: --input is required", file=sys.stderr)
                sys.exit(1)
            
            # Read from file if path provided
            if os.path.exists(input_text):
                with open(input_text, "r") as f:
                    input_text = f.read()
            
            print(f"Executing transformation: {args.execute}")
            result = client.execute_transformation(trans_id, input_text, args.model)
            
            output = result.get("output", "No output")
            print(f"\nResult:\n{output}")
            return
        
        # Default: show help
        parser.print_help()
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
