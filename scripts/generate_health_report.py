#!/usr/bin/env python3
import os
import sys
import json
import requests

# Ensure the scripts directory is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from validate_json import check_all_json
from check_devices import check_devices
from check_images import check_images

def run():
    # 1. Syntax Check
    print("Running JSON Syntax Check...")
    checked_files, invalid_files = check_all_json()
    
    # 2. Device Check
    print("Running Device Check...")
    device_results = check_devices()
    
    # 3. Image URL Check
    print("Running Image URL Check...")
    broken_images = check_images()
    
    # Let's determine if we have any errors or warnings
    has_issues = False
    
    # Syntax section
    syntax_lines = []
    if invalid_files:
        has_issues = True
        for path, err in invalid_files:
            syntax_lines.append(f"* {path}: {err}")
    else:
        syntax_lines.append("✅ All JSON files valid")
        
    # Devices statistics
    total = device_results["total"]
    active = device_results["active"]
    inactive = device_results["inactive"]
    
    # Duplicate Codenames
    duplicate_codenames = device_results["duplicate_codenames"]
    duplicate_codename_alts = device_results["duplicate_codename_alts"]
    
    dup_lines = []
    if duplicate_codenames:
        for name in duplicate_codenames:
            dup_lines.append(f"* Duplicate codename: {name}")
    if duplicate_codename_alts:
        for name in duplicate_codename_alts:
            dup_lines.append(f"* Duplicate codename_alt: {name}")
            
    if dup_lines:
        has_issues = True
    else:
        dup_lines.append("None")
        
    # Load devices JSON to lookup github usernames for missing fields grouping
    devices_path = "API/devices.json"
    devices = []
    if os.path.exists(devices_path):
        try:
            with open(devices_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                devices = data.get("devices", [])
        except Exception as e:
            print(f"Error loading {devices_path} for grouping: {e}")
            
    dev_to_gh = {}
    for idx, d in enumerate(devices):
        dev_id = d.get("codename") or f"Device at index {idx}"
        dev_to_gh[dev_id] = d.get("github_username")
        
    # Group missing fields and empty values by github_username
    device_problems = {}
    
    for dev_id, field in device_results["missing_fields"]:
        if dev_id not in device_problems:
            device_problems[dev_id] = []
        device_problems[dev_id].append(field)
        
    for dev_id, field, val in device_results["empty_values"]:
        if dev_id not in device_problems:
            device_problems[dev_id] = []
        if field not in device_problems[dev_id]:
            device_problems[dev_id].append(field)
            
    # Mentions grouping
    maintainer_groups = {}
    unassigned_devices = []
    missing_fields_lines = []
    
    if device_problems:
        has_issues = True
        for dev_id, fields in sorted(device_problems.items()):
            missing_fields_lines.append(f"* {dev_id}: missing {', '.join(fields)}")
            
            # Lookup gh_username
            gh_user = dev_to_gh.get(dev_id)
            if gh_user is None or (isinstance(gh_user, str) and gh_user.strip() == ""):
                unassigned_devices.append((dev_id, fields))
            else:
                gh_user = gh_user.strip()
                if gh_user not in maintainer_groups:
                    maintainer_groups[gh_user] = []
                maintainer_groups[gh_user].append((dev_id, fields))
                
    if not missing_fields_lines:
        missing_fields_lines.append("None")
        
    # Format Action Required and Unassigned Devices sections
    action_lines = []
    if maintainer_groups:
        for gh_user, dev_list in sorted(maintainer_groups.items()):
            action_lines.append(f"@{gh_user}")
            action_lines.append("")
            for dev_id, fields in dev_list:
                action_lines.append(f"* {dev_id}: missing {', '.join(fields)}")
            action_lines.append("")
        if action_lines and action_lines[-1] == "":
            action_lines.pop()
    else:
        action_lines.append("None")
        
    unassigned_lines = []
    if unassigned_devices:
        for dev_id, fields in unassigned_devices:
            unassigned_lines.append(f"* {dev_id}: missing {', '.join(fields)}")
    else:
        unassigned_lines.append("None")
        
    # Broken image URLs
    image_lines = []
    if broken_images:
        has_issues = True
        for img in broken_images:
            image_lines.append(f"* {img}")
    else:
        image_lines.append("None")
        
    # Construct labels
    labels = ["health-report"]
    if device_problems:
        labels.append("missing-fields")
    if duplicate_codenames or duplicate_codename_alts:
        labels.append("duplicate-codename")
    if broken_images:
        labels.append("broken-image-url")
        
    # Construct final markdown
    report = []
    report.append("# JSON Health Report")
    report.append("")
    report.append("## Summary")
    report.append("")
    report.append(f"* Total devices: {total}")
    report.append(f"* Active devices: {active}")
    report.append(f"* Inactive devices: {inactive}")
    report.append("")
    report.append("## Syntax")
    report.append("")
    report.extend(syntax_lines)
    report.append("")
    report.append("## Duplicate Codenames")
    report.append("")
    report.extend(dup_lines)
    report.append("")
    report.append("## Missing Required Fields")
    report.append("")
    report.extend(missing_fields_lines)
    report.append("")
    report.append("## Broken Image URLs")
    report.append("")
    report.extend(image_lines)
    report.append("")
    report.append("## Action Required")
    report.append("")
    report.extend(action_lines)
    report.append("")
    report.append("## Unassigned Devices")
    report.append("")
    report.extend(unassigned_lines)
    report.append("")
    report.append("Checked successfully.")
    
    report_body = "\n".join(report)
    
    # Output report to log
    print("================ Generated Report ================")
    try:
        print(report_body)
    except UnicodeEncodeError:
        print(report_body.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8'))
    print("==================================================")
    
    # GitHub issue creation/updating/closing
    token = os.environ.get("GITHUB_TOKEN")
    repo = os.environ.get("GITHUB_REPOSITORY")
    
    if not token or not repo:
        print("Warning: GITHUB_TOKEN or GITHUB_REPOSITORY not set. Skipping GitHub issue updates.")
        return
        
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }
    
    # Fetch open issues
    print(f"Fetching open issues for {repo}...")
    url = f"https://api.github.com/repos/{repo}/issues?state=open&per_page=100"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    issues = response.json()
    
    target_issue = None
    title = "[Health Report] API JSON Validation"
    for issue in issues:
        if issue.get("title") == title and "pull_request" not in issue:
            target_issue = issue
            break
            
    if target_issue:
        issue_number = target_issue["number"]
        
        if has_issues:
            print(f"Warnings/errors found. Updating open issue #{issue_number}...")
            update_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
            update_response = requests.patch(
                update_url,
                headers=headers,
                json={"body": report_body, "state": "open", "labels": labels}
            )
            update_response.raise_for_status()
            print("Issue updated successfully.")
        else:
            print("All checks passed. Posting closing comment...")
            comment_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments"
            comment_response = requests.post(
                comment_url,
                headers=headers,
                json={"body": "All JSON checks are now passing. Closing this report."}
            )
            comment_response.raise_for_status()
            
            print(f"Closing issue #{issue_number}...")
            update_url = f"https://api.github.com/repos/{repo}/issues/{issue_number}"
            update_response = requests.patch(
                update_url,
                headers=headers,
                json={"body": report_body, "state": "closed", "labels": labels}
            )
            update_response.raise_for_status()
            print("Issue closed successfully.")
    else:
        if has_issues:
            print("Warnings/errors found. Creating new issue...")
            create_url = f"https://api.github.com/repos/{repo}/issues"
            create_response = requests.post(
                create_url,
                headers=headers,
                json={"title": title, "body": report_body, "labels": labels}
            )
            create_response.raise_for_status()
            print(f"Issue created successfully: {create_response.json().get('html_url')}")
        else:
            print("All checks passed and no open issue found. No action needed.")

if __name__ == "__main__":
    run()
