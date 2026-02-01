from dotenv import load_dotenv
load_dotenv()

import os
import sys
import json
import hashlib
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from requests.auth import HTTPBasicAuth
from datetime import datetime, timezone

BASELINE_FILE = "baseline.json"

# =========================
# Email Configuration
# =========================
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
ALERT_TO = os.getenv("ALERT_TO")


def send_email_alert(subject, body):
    if not all([SMTP_SERVER, EMAIL_USER, EMAIL_PASS, ALERT_TO]):
        print("[!] Email not configured. Skipping email alert.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = ALERT_TO
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        print("[+] Email alert sent")

    except Exception as e:
        print(f"[!] Email alert failed: {e}")


# =========================
# Load Jira Configuration
# =========================
def load_jira_config():
    config = {
        "url": os.getenv("JIRA_URL"),
        "email": os.getenv("JIRA_EMAIL"),
        "token": os.getenv("JIRA_API_TOKEN"),
        "project": os.getenv("JIRA_PROJECT_KEY")
    }

    missing = [k for k, v in config.items() if not v]
    if missing:
        print(f"[!] Jira not configured. Missing: {', '.join(missing)}")
        return None

    return config


# =========================
# Hashing & Scanning
# =========================
def sha256_hash(path):
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def scan_directory(directory):
    results = {}

    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            try:
                results[path] = {
                    "hash": sha256_hash(path),
                    "size": os.path.getsize(path),
                    "mtime": os.path.getmtime(path)
                }
            except Exception as e:
                print(f"[ERROR] Failed to scan {path}: {e}")

    return results


# =========================
# Baseline Handling
# =========================
def create_baseline(directory):
    print("[*] Creating baseline...")
    baseline = scan_directory(directory)

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=4)

    print(f"[+] Baseline saved to {BASELINE_FILE}")


def load_baseline():
    if not os.path.exists(BASELINE_FILE):
        print("[!] Baseline not found. Run baseline creation first.")
        sys.exit(1)

    with open(BASELINE_FILE, "r") as f:
        return json.load(f)


# =========================
# Jira Integration
# =========================
def create_jira_issue(config, title, description, priority="High"):
    url = f"{config['url']}/rest/api/3/issue"

    payload = {
        "fields": {
            "project": {"key": config["project"]},
            "summary": title,
            "issuetype": {"name": "Task"},
            "priority": {"name": priority},
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}]
                    }
                ]
            }
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers={"Content-Type": "application/json"},
        auth=HTTPBasicAuth(config["email"], config["token"])
    )

    if response.status_code == 201:
        print("[+] Jira issue created successfully")
    else:
        print(f"[!] Jira error {response.status_code}: {response.text}")


# =========================
# Integrity Checking
# =========================
def check_integrity(directory):
    print("[*] Running integrity check...")
    baseline = load_baseline()
    current = scan_directory(directory)

    baseline_files = set(baseline.keys())
    current_files = set(current.keys())

    alerts = []

    for path in baseline_files & current_files:
        if baseline[path]["hash"] != current[path]["hash"]:
            alerts.append(f"MODIFIED: {path}")

    for path in current_files - baseline_files:
        alerts.append(f"NEW FILE: {path}")

    for path in baseline_files - current_files:
        alerts.append(f"DELETED: {path}")

    if not alerts:
        print("[+] No integrity violations detected")
        return

    timestamp = datetime.now(timezone.utc).isoformat()
    report = "\n".join(alerts)

    print("[!] Integrity violations detected")

    # ---- EMAIL ALERT (ADDED) ----
    send_email_alert(
        subject="🚨 FIM ALERT: File Integrity Violation",
        body=f"Time (UTC): {timestamp}\n\n{report}"
    )

    jira = load_jira_config()
    if not jira:
        print("[!] Alerts detected but Jira not configured")
        print(report)
        return

    create_jira_issue(
        jira,
        title="FIM Alert: File Integrity Violation",
        description=f"Time (UTC): {timestamp}\n\n{report}",
        priority="High"
    )


# =========================
# Main Program
# =========================
def main():
    print("\n==== FILE INTEGRITY MONITORING ====")
    print("1. Create baseline")
    print("2. Check integrity")

    choice = input("Select option (1/2): ").strip()
    directory = input("Directory to monitor: ").strip()

    if not os.path.isdir(directory):
        print("[!] Invalid directory path")
        sys.exit(1)

    if choice == "1":
        create_baseline(directory)
    elif choice == "2":
        check_integrity(directory)
    else:
        print("[!] Invalid option")


if __name__ == "__main__":
    main()