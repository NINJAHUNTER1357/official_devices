#!/usr/bin/env python3
import os
import json
import sys

def check_all_json():
    invalid_files = []
    checked_files = []
    api_dir = "API"
    
    if not os.path.exists(api_dir):
        print(f"Error: {api_dir} directory not found.")
        sys.exit(1)
        
    for root, _, files in os.walk(api_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                display_path = file_path.replace("\\", "/")
                print(f"Checking {display_path}")
                checked_files.append(display_path)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        json.load(f)
                except Exception as e:
                    print(f"Error checking {display_path}: {e}")
                    invalid_files.append((display_path, str(e)))
                    
    return checked_files, invalid_files

if __name__ == "__main__":
    _, invalid = check_all_json()
    if invalid:
        sys.exit(1)
    sys.exit(0)
