#!/usr/bin/env python3
"""Extract all automations from an Airtable base via internal v0.3 API.

Usage:
    python3 extract_automations.py <base_id> <output_dir> <cookie>

Arguments:
    base_id     Airtable base ID (e.g. appXXXXXXXXXXXXXX)
    output_dir  Directory for JSON output (e.g. apps/time/automations)
    cookie      Full cookie header value from an authenticated Airtable browser session

The cookie must contain __Host-airtable-session. Get it from:
  Browser → DevTools → Network tab → any Airtable request → copy Cookie header value.
"""

import os
import json
import re
import sys
import time

try:
    import requests
except ImportError:
    print("ERROR: 'requests' not installed. Run: pip3 install requests")
    sys.exit(1)


def slugify(text):
    text = text.replace("/", "_").replace(" ", "_")
    return re.sub(r"(?u)[^-\w.]", "", text)


def extract(base_id, output_dir, cookie):
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "cookie": cookie,
        "x-airtable-application-id": base_id,
        "x-airtable-inter-service-client": "webClient",
        "x-requested-with": "XMLHttpRequest",
        "x-time-zone": "Asia/Bangkok",
        "x-user-locale": "en",
    }

    os.makedirs(output_dir, exist_ok=True)

    # 1. Fetch base schema to discover automation IDs
    print(f"[*] Fetching base schema for {base_id}...")
    r = requests.get(
        f"https://airtable.com/v0.3/application/{base_id}/read",
        headers=headers,
        params={"includeAllData": "true"},
    )

    if r.status_code == 401:
        print("[!] 401 Unauthorized — cookie expired. Get a fresh one from DevTools.")
        sys.exit(1)
    if r.status_code != 200:
        print(f"[!] Failed ({r.status_code}): {r.text[:200]}")
        sys.exit(1)

    app_data = r.json().get("data", {})
    sections = app_data.get("workflowSectionsById", {})

    workflow_ids = []
    for section in sections.values():
        workflow_ids.extend(section.get("workflowOrder", []))

    if not workflow_ids:
        print("[*] No automations found in this base.")
        return

    print(f"[*] Found {len(workflow_ids)} automations. Extracting...")

    # 2. Fetch each automation
    for w_id in workflow_ids:
        print(f"    - {w_id}...", end="", flush=True)

        wr = requests.get(
            f"https://airtable.com/v0.3/workflow/{w_id}/read", headers=headers
        )
        if wr.status_code != 200:
            print(f" ERROR ({wr.status_code})")
            continue

        w_data = wr.json().get("data", {}).get("workflow", {})
        name = w_data.get("name", w_id)
        deployment_id = w_data.get("targetWorkflowDeploymentId")

        filename = f"{slugify(name)}.json"
        filepath = os.path.join(output_dir, filename)

        if deployment_id:
            dr = requests.get(
                f"https://airtable.com/v0.3/workflowDeployment/{deployment_id}/read",
                headers=headers,
                params={"stringifiedObjectParams": "{}"},
            )
            if dr.status_code == 200:
                with open(filepath, "w") as f:
                    json.dump(dr.json(), f, indent=2)
                print(f" OK ({name})")
            else:
                with open(filepath, "w") as f:
                    json.dump(wr.json(), f, indent=2)
                print(f" PARTIAL — deployment failed ({name})")
        else:
            with open(filepath, "w") as f:
                json.dump(wr.json(), f, indent=2)
            print(f" OK — draft ({name})")

        time.sleep(0.2)  # rate limit

    print(f"\n[*] Done. Output: {output_dir}/")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2], sys.argv[3])
