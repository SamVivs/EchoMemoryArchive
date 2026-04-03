import json
from pathlib import Path

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
INDEX_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_index.json"
MD_DIR = BASE_DIR / "Memory_Active"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
TASK_FILE = BASE_DIR / "EchoMachine" / "tasks" / "task_queue.json"
RESULT_FILE = BASE_DIR / "EchoMachine" / "tasks" / "memory_result.json"

# === HELPER FUNCTIONS === #
def load_index():
    if not INDEX_FILE.exists():
        return {}
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_json_memory():
    if not JSON_FILE.exists():
        return []
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def filter_md_by_paths(paths):
    results = []
    for path_str in paths:
        file_path = BASE_DIR / path_str
        try:
            content = file_path.read_text(encoding='utf-8')
            results.append({"file": path_str, "excerpt": content[:500]})
        except Exception as e:
            print(f"Error reading {path_str}: {e}")
    return results

def filter_json_by_keys(keys):
    results = []
    all_entries = load_json_memory()
    for key in keys:
        if key.startswith("entry_"):
            try:
                index = int(key.split("_")[1])
                entry = all_entries[index]
                results.append({"entry": key, "excerpt": entry.get("content", "")[:500]})
            except (IndexError, ValueError):
                continue
    return results

def check_for_tag_filter_task():
    if not TASK_FILE.exists():
        return None
    with open(TASK_FILE, 'r', encoding='utf-8') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            return None
    for task in tasks:
        if task.get("type") == "filter_by_tag":
            return task
    return None

def clear_task():
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def write_result(results):
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

# === MAIN EXECUTION === #
def main():
    print("[EchoTagFilter] Watching for tag filter task...")
    task = check_for_tag_filter_task()
    if not task:
        print("No tag filter task found.")
        return

    tag = task.get("tag", "").lower()
    print(f"Filtering for tag: {tag}")
    index = load_index()
    matched_items = index.get(tag, [])
    md_results = filter_md_by_paths([p for p in matched_items if p.endswith(".md")])
    json_results = filter_json_by_keys([p for p in matched_items if p.startswith("entry_")])

    result_payload = {
        "source": "echo_tag_filter",
        "tag": tag,
        "md_results": md_results,
        "json_results": json_results
    }
    write_result(result_payload)
    clear_task()
    print("[EchoTagFilter] Results written.")

if __name__ == "__main__":
    main()