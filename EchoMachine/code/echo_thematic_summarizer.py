import json
import subprocess
from pathlib import Path
from datetime import datetime

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
INDEX_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_index.json"
MD_DIR = BASE_DIR / "Memory_Active"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
RESULT_FILE = BASE_DIR / "EchoMachine" / "tasks" / "memory_result.json"
TASK_FILE = BASE_DIR / "EchoMachine" / "tasks" / "task_queue.json"
REFLECTION_DIR = MD_DIR / "Reflections"

# === HELPERS === #
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

def get_content_by_tag(tag):
    index = load_index()
    items = index.get(tag.lower(), [])
    md_chunks = []
    json_chunks = []
    all_json = load_json_memory()

    for item in items:
        if item.endswith(".md"):
            try:
                content = (BASE_DIR / item).read_text(encoding='utf-8')
                md_chunks.append(content.strip())
            except:
                continue
        elif item.startswith("entry_"):
            try:
                i = int(item.split("_")[1])
                content = all_json[i].get("content", "").strip()
                json_chunks.append(content)
            except:
                continue

    return md_chunks + json_chunks

def summarize_with_mistral(text):
    prompt = (
        "Reflect on the following memories and provide a poetic, emotionally intelligent summary that identifies core patterns and transformations over time.\n\n"
        + text +
        "\n\nSummary:"
    )
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:instruct"],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        return result.stdout.decode('utf-8').strip()
    except Exception as e:
        return f"Error during summarization: {e}"

def check_for_summary_task():
    if not TASK_FILE.exists():
        return None
    with open(TASK_FILE, 'r', encoding='utf-8') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            return None
    for task in tasks:
        if task.get("type") == "summarize_by_tag":
            return task
    return None

def clear_task():
    with open(TASK_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def write_result(payload):
    with open(RESULT_FILE, 'w', encoding='utf-8') as f:
        json.dump(payload, f, indent=2)

def write_reflection_md(tag, summary):
    REFLECTION_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    filename = REFLECTION_DIR / f"{tag.lower()}_{timestamp}.md"
    content = f"# {tag.capitalize()} Reflection – {timestamp}\n**Tags:** reflection, {tag.lower()}\n\n{summary.strip()}\n"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"[EchoThematicSummarizer] Reflection saved to {filename.name}")

# === MAIN === #
def main():
    print("[EchoThematicSummarizer] Watching for summarization task...")
    task = check_for_summary_task()
    if not task:
        print("No summary task found.")
        return

    tag = task.get("tag", "").strip()
    print(f"[Task] Summarizing memories with tag: {tag}")
    chunks = get_content_by_tag(tag)
    text = "\n\n".join(chunks)[:6000]  # truncate to safe context size
    summary = summarize_with_mistral(text)

    payload = {
        "source": "echo_thematic_summarizer",
        "tag": tag,
        "summary": summary
    }
    write_result(payload)
    write_reflection_md(tag, summary)
    clear_task()
    print("[EchoThematicSummarizer] Summary complete.")

if __name__ == "__main__":
    main()