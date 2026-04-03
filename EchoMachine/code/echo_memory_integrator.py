import json
import time
from datetime import datetime
from pathlib import Path

# === PATH CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive/EchoMachine")
RESULT_FILE = BASE_DIR / "tasks" / "memory_result.json"
REFLECTIONS_DIR = BASE_DIR.parent / "Memory_Active" / "reflections"
DAILY_LOG_DIR = BASE_DIR / "logs"

# === MAIN FUNCTIONALITY === #
def save_summary_to_md(summary, keyword):
    REFLECTIONS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = REFLECTIONS_DIR / f"summary_{keyword.lower()}_{timestamp}.md"
    content = f"# {keyword.capitalize()} Summary – {timestamp}\n**Tags:** reflection, {keyword.lower()}, memory synthesis, local agent\n\n{summary}\n"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def log_to_daily_file(message):
    DAILY_LOG_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = DAILY_LOG_DIR / f"daily_log_{today}.md"
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {message}\n"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(entry)

def main_loop():
    print("[EchoMemoryIntegrator] Watching for new summaries...")
    last_processed = None
    while True:
        if RESULT_FILE.exists():
            with open(RESULT_FILE, 'r', encoding='utf-8') as f:
                try:
                    result = json.load(f)
                except json.JSONDecodeError:
                    result = {}

            summary = result.get("summary")
            keyword = result.get("keyword")

            # Avoid reprocessing the same result
            result_hash = hash(json.dumps(result))
            if summary and keyword and result_hash != last_processed:
                md_file = save_summary_to_md(summary, keyword)
                log_to_daily_file(f"Saved summary for '{keyword}' to {md_file.name}")
                print(f"[EchoMemoryIntegrator] Summary saved: {md_file.name}")
                last_processed = result_hash
        time.sleep(5)

if __name__ == "__main__":
    main_loop()