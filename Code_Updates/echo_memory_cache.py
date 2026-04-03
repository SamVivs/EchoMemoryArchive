# echo_memory_cache.py

import os
import json
from datetime import datetime

CACHE_FILE = os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "echo_cache.json")

def update_memory_cache(target_dir):
    index = {}
    for root, _, files in os.walk(target_dir):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                try:
                    mod_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M:%S")
                    index[path] = {
                        "last_processed": mod_time,
                        "status": "cached"
                    }
                except Exception as e:
                    print(f"⚠️ Failed to index {path}: {e}")

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print("✅ Memory cache updated.")

if __name__ == "__main__":
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Logs"))
    update_memory_cache(target_dir)