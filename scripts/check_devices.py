#!/usr/bin/env python3
import json
import os
import sys

def check_devices():
    devices_path = "API/devices.json"
    if not os.path.exists(devices_path):
        print(f"Error: {devices_path} not found.")
        sys.exit(1)
        
    print(f"Checking {devices_path}")
    with open(devices_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except Exception as e:
            print(f"Error decoding JSON: {e}")
            sys.exit(1)
            
    devices = data.get("devices", [])
    
    # Statistics
    total_devices = len(devices)
    active_devices = sum(1 for d in devices if d.get("active") is True)
    inactive_devices = total_devices - active_devices
    
    # Duplicates
    codename_counts = {}
    codename_alt_counts = {}
    
    for d in devices:
        c = d.get("codename")
        c_alt = d.get("codename_alt")
        if c:
            codename_counts[c] = codename_counts.get(c, 0) + 1
        if c_alt:
            codename_alt_counts[c_alt] = codename_alt_counts.get(c_alt, 0) + 1
            
    duplicate_codenames = [name for name, count in codename_counts.items() if count > 1]
    duplicate_codename_alts = [name for name, count in codename_alt_counts.items() if count > 1]
    
    # Required fields and empty values
    missing_fields_report = []
    empty_values_report = []
    
    required_fields = [
        "codename",
        "codename_alt",
        "vendor",
        "model",
        "maintainer_name",
        "telegram_username",
        "github_username",
        "active"
    ]
    
    allowed_null_fields = {"frame", "image_url", "donate_link"}
    
    for idx, d in enumerate(devices):
        dev_id = d.get("codename") or f"Device at index {idx}"
        
        # Required fields check
        for rf in required_fields:
            if rf not in d:
                missing_fields_report.append((dev_id, rf))
            else:
                v = d[rf]
                if v is None or (isinstance(v, str) and v.strip() == ""):
                    empty_values_report.append((dev_id, rf, v))
                
    # Format markdown report
    report_lines = []
    report_lines.append("## Devices")
    report_lines.append(f"Total devices: {total_devices}")
    report_lines.append(f"Active devices: {active_devices}")
    report_lines.append(f"Inactive devices: {inactive_devices}")
    
    report_lines.append("## Duplicate codenames")
    duplicates = []
    if duplicate_codenames:
        duplicates.extend([f"Duplicate codename: {name}" for name in duplicate_codenames])
    if duplicate_codename_alts:
        duplicates.extend([f"Duplicate codename_alt: {name}" for name in duplicate_codename_alts])
        
    if duplicates:
        for dup in duplicates:
            report_lines.append(f"* {dup}")
    else:
        report_lines.append("None")
        
    report_lines.append("## Missing required fields")
    if missing_fields_report:
        for dev_id, field in missing_fields_report:
            report_lines.append(f"* {dev_id}: missing `{field}`")
    else:
        report_lines.append("None")
        
    report_lines.append("## Empty values")
    if empty_values_report:
        for dev_id, field, val in empty_values_report:
            report_lines.append(f"* {dev_id}: `{field}` is empty/null (`{val}`)")
    else:
        report_lines.append("None")
        
    report = "\n\n".join(report_lines)
    print(report)
    
    return {
        "total": total_devices,
        "active": active_devices,
        "inactive": inactive_devices,
        "duplicate_codenames": duplicate_codenames,
        "duplicate_codename_alts": duplicate_codename_alts,
        "missing_fields": missing_fields_report,
        "empty_values": empty_values_report,
        "markdown": report
    }

if __name__ == "__main__":
    check_devices()
