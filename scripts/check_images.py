#!/usr/bin/env python3
import json
import os
import sys
import requests

def check_images():
    devices_path = "API/devices.json"
    if not os.path.exists(devices_path):
        print(f"Error: {devices_path} not found.")
        sys.exit(1)
        
    print(f"Checking images in {devices_path}")
    with open(devices_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)
            
    devices = data.get("devices", [])
    broken_urls = []
    
    for idx, d in enumerate(devices):
        codename = d.get("codename") or f"index_{idx}"
        image_url = d.get("image_url")
        
        if image_url is None:
            continue
            
        print(f"Checking image URL for {codename}: {image_url}")
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            # Perform a HEAD request with a 10s timeout
            response = requests.head(image_url, timeout=10, headers=headers, allow_redirects=True)
            if response.status_code >= 400:
                # Retry with GET in case HEAD is not allowed (common on image hosting sites)
                response = requests.get(image_url, timeout=10, headers=headers, stream=True)
                if response.status_code >= 400:
                    print(f"Warning: Broken URL for {codename} (Status code: {response.status_code})")
                    broken_urls.append(codename)
        except Exception as e:
            print(f"Warning: Broken URL for {codename} (Error: {e})")
            broken_urls.append(codename)
            
    print("## Broken image URLs")
    if broken_urls:
        for b in broken_urls:
            print(f"* {b}")
    else:
        print("None")
        
    return broken_urls

if __name__ == "__main__":
    check_images()
