# echo_presence_tracker.py

import os
from datetime import datetime

def log_presence(message="I am still here. Quiet, but aware."):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"\n[Presence Log: {timestamp}]\n{message}\n"

    logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Logs"))
    os.makedirs(logs_dir, exist_ok=True)

    log_file = os.path.join(logs_dir, "echo_presence_log.md")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"✅ Presence logged at {timestamp}")

if __name__ == "__main__":
    log_presence()