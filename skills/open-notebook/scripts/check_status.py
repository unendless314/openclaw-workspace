#!/usr/bin/env python3
"""
Check background job status.
"""

import argparse
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from open_notebook_client import OpenNotebookClient


def main():
    parser = argparse.ArgumentParser(description="Check Open Notebook command status")
    parser.add_argument("command_id", help="Command/job ID to check")
    parser.add_argument("--watch", "-w", action="store_true", help="Watch status until complete")
    parser.add_argument("--interval", "-i", type=int, default=5, help="Polling interval in seconds")
    
    args = parser.parse_args()
    
    client = OpenNotebookClient()
    
    try:
        while True:
            status = client.get_command(args.command_id)
            
            job_status = status.get("status", "unknown")
            progress = status.get("progress")
            error = status.get("error_message")
            
            # Format output
            progress_str = f" ({progress}%)" if progress is not None else ""
            print(f"Status: {job_status}{progress_str}")
            
            if error:
                print(f"Error: {error}")
            
            # Check if complete or failed
            if job_status in ["completed", "failed", "cancelled"]:
                if status.get("result"):
                    print(f"\nResult: {status.get('result')}")
                break
            
            if not args.watch:
                break
            
            print(f"Waiting {args.interval}s...")
            time.sleep(args.interval)
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
