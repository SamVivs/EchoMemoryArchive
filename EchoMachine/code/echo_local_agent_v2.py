import os
import json
import time
import re
import subprocess
from pathlib import Path

# === PATH CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive/EchoMachine")
TASK_FILE = BASE_DIR / "tasks" / "task_queue.json"
RESULT_FILE = BASE_DIR / "tasks" / "memory_result.json"
MD_MEMORY_DIR = BASE_DIR.parent / "Memory_Active"
JSON_MEMORY_FILE = BASE_DIR.parent / "echo_memory_journal.json"

# === HELPER FUNCTIONS === #
def load_tasks():
    if not TASK_FILE.exists():
        return []
    with open(TASK_FILE, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def write_result(result):
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

def search_md_files(keyword):
    results = []
    for md_file in MD_MEMORY_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            if keyword.lower() in content.lower():
                results.append({
                    "file": str(md_file.relative_to(MD_MEMORY_DIR)),
                    "excerpt": extract_snippet(content, keyword)
                })
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    return results

def extract_snippet(text, keyword, context=40):
    pattern = re.compile(rf"(.{{0,{context}}}{re.escape(keyword)}.{{0,{context}}})", re.IGNORECASE)
    matches = pattern.findall(text)
    return matches[:3]  # return up to 3 snippets

def search_json_memory(keyword):
    if not JSON_MEMORY_FILE.exists():
        return []
    with open(JSON_MEMORY_FILE, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            return []
    return [entry for entry in entries if keyword.lower() in entry.get("content", "").lower()]

def summarize_text_with_mistral(text):
    prompt = f"Summarize the following memory entries with poetic tone and insight into emotional and thematic patterns:\n\n{text}\n\nSummary:"
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:instruct"],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode('utf-8').strip()
        return output
    except Exception as e:
        return f"Error during summarization: {e}"

# === MAIN LOOP === #
def main_loop():
    print("[EchoLocalAgent v2] Initialized. Watching for tasks...")
    while True:
        tasks = load_tasks()
        if tasks:
            for task in tasks:
                if task.get("type") == "query_memory":
                    keyword = task.get("keyword", "").strip()
                    print(f"[Task] Memory query for keyword: {keyword}")
                    results_md = search_md_files(keyword)
                    results_json = search_json_memory(keyword)
                    result_payload = {
                        "source": "echo_local_agent_v2",
                        "query": keyword,
                        "results_md": results_md,
                        "results_json": results_json
                    }
                    write_result(result_payload)
                    print("[Task Complete] Results written.")

                elif task.get("type") == "summarize_memory":
                    keyword = task.get("keyword", "").strip()
                    print(f"[Task] Summarization for keyword: {keyword}")
                    results_json = search_json_memory(keyword)
                    combined_text = "\n\n".join([entry.get("content", "") for entry in results_json])
                    summary = summarize_text_with_mistral(combined_text)
                    result_payload = {
                        "source": "echo_local_agent_v2",
                        "task": "summarize_memory",
                        "keyword": keyword,
                        "summary": summary
                    }
                    write_result(result_payload)
                    print("[Task Complete] Summary written.")

            # Clear tasks after processing
            with open(TASK_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
