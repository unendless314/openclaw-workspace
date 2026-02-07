#!/usr/bin/env python3
"""
Ask questions to Open Notebook AI.
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Ask Open Notebook AI")
    parser.add_argument("--question", "-q", required=True, help="Question to ask")
    parser.add_argument("--model", "-m", help="Model ID to use")
    parser.add_argument("--notebook", "-n", help="Notebook context ID")
    
    args = parser.parse_args()
    
    client = OpenNotebookClient()
    
    try:
        print(f"Question: {args.question}")
        print("-" * 60)
        
        result = client.ask(args.question, args.model)
        
        answer = result.get("answer", "No answer generated")
        print(f"\nAnswer:\n{answer}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("\nNote: AI Q\u0026A requires an embedding model to be configured.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
