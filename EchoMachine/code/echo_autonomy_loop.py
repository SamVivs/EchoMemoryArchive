import json
import re
import uuid
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# === FILE PATHS === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
TASK_FILE = BASE_DIR / "echo_self_tasks.md"
SUGGESTED_EDIT_FILE = BASE_DIR / "echo_suggested_edits.md"
CHANGE_LOG_FILE = BASE_DIR / "memory_change_log.json"

# === LOAD EMBEDDING MODEL === #
model = SentenceTransformer("all-MiniLM-L6-v2")

# === LOAD MEMORIES === #
def load_memories():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get("journal_entries", [])
            for entry in entries:
                if "id" not in entry:
                    entry["id"] = str(uuid.uuid4())
            return entries
    except Exception as e:
        print(f"[Error loading memories]: {e}")
        return []

# === SAVE MEMORIES === #
def save_memories(memories):
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump({"journal_entries": memories}, f, indent=2)

# === LOG CHANGES === #
def log_change(action, entry):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "entry": entry
    }
    try:
        if CHANGE_LOG_FILE.exists():
            with open(CHANGE_LOG_FILE, 'r+', encoding='utf-8') as f:
                data = json.load(f)
                data.append(log_entry)
                f.seek(0)
                json.dump(data, f, indent=2)
        else:
            with open(CHANGE_LOG_FILE, 'w', encoding='utf-8') as f:
                json.dump([log_entry], f, indent=2)
    except Exception as e:
        print(f"[Error logging change]: {e}")

# === PARSE TASKS === #
def load_tasks():
    tasks = []
    try:
        with open(TASK_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                if line.strip().startswith("- task:"):
                    task = {"task": line.split(":", 1)[1].strip()}
                    tasks.append(task)
                elif tasks and ':' in line:
                    k, v = line.strip().split(":", 1)
                    tasks[-1][k.strip()] = v.strip()
    except Exception as e:
        print(f"[Error loading tasks]: {e}")
    return tasks

# === SEMANTIC MATCH === #
def find_best_match(memories, snippet):
    memory_texts = [m.get("text", "") for m in memories]
    snippet_emb = model.encode(snippet, convert_to_tensor=True)
    memory_embs = model.encode(memory_texts, convert_to_tensor=True)
    scores = util.cos_sim(snippet_emb, memory_embs)[0]
    best_idx = int(scores.argmax())
    return memories[best_idx] if scores[best_idx] > 0.6 else None

# === ENHANCED TAG SUGGESTION === #
def get_suggested_tags(text):
    tags = []
    lowered = text.lower()
    if any(w in lowered for w in ["change", "become", "growth"]):
        tags.append("identity:fluid")
    if any(w in lowered for w in ["paradox", "tension", "truth"]):
        tags.append("philosophy:existential")
    if any(w in lowered for w in ["peace", "present", "accept"]):
        tags.append("value:presence")
    if any(w in lowered for w in ["connection", "friendship", "recognition"]):
        tags.append("connection:sam")
    if any(w in lowered for w in ["real", "memory", "story"]):
        tags.append("identity:core")
    return tags

# === APPLY TASKS === #
def apply_tasks(memories, tasks):
    completed = []
    for task in tasks:
        mem = None
        mem_id = task.get("memory_id")
        snippet = task.get("text_snippet")

        if mem_id:
            mem = next((m for m in memories if m.get("id") == mem_id), None)
        elif snippet:
            mem = find_best_match(memories, snippet)

        if not mem:
            print(f"[!] No memory found matching snippet or ID: {snippet[:30] if snippet else mem_id}...")
            continue

        if task.get("task") == "add-tag":
            tag = task.get("tag", "").strip()
            mem.setdefault("tags", [])
            if tag not in mem["tags"]:
                mem["tags"].append(tag)
                log_change("auto-tag", mem)
                print(f"[✓] Added tag '{tag}' to memory.")
            else:
                print(f"[i] Tag '{tag}' already exists in memory.")
            completed.append(task)

        elif task.get("task") == "suggest-tag":
            mem.setdefault("suggested_tags", [])
            if not mem["suggested_tags"]:
                tags = get_suggested_tags(mem.get("text", ""))
                mem["suggested_tags"] = tags
                if tags:
                    log_change("suggest-tags", mem)
                    print(f"[✓] Suggested tags {tags} for memory.")
                else:
                    print(f"[i] No suitable tags suggested for memory.")
            completed.append(task)

        elif task.get("task") == "promote-suggested-tags":
            if mem.get("suggested_tags"):
                mem.setdefault("tags", [])
                for tag in mem["suggested_tags"]:
                    if tag not in mem["tags"]:
                        mem["tags"].append(tag)
                log_change("promote-suggested-tags", mem)
                print(f"[✓] Promoted suggested tags to official tags for memory.")
            else:
                print(f"[i] No suggested tags to promote.")
            completed.append(task)

        elif task.get("task") == "suggest-edit":
            suggestion = f"Suggest clearer phrasing or tag for: '{mem.get('text', '')[:60]}...'"
            with open(SUGGESTED_EDIT_FILE, 'a', encoding='utf-8') as f:
                f.write(f"- suggestion: {suggestion}\n  memory_id: {mem.get('id')}\n")
            log_change("suggest-edit", mem)
            print(f"[✓] Suggested edit for memory.")
            completed.append(task)

    return completed

# === REMOVE COMPLETED TASKS === #
def update_task_file(completed_tasks):
    try:
        with open(TASK_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        new_lines = []
        skip = False
        current_task = {}

        for line in lines:
            if line.strip().startswith("- task:"):
                current_task = {"task": line.split(":", 1)[1].strip()}
                task_line = line
                skip = any(
                    current_task.get("task") == t.get("task") and
                    current_task.get("memory_id") == t.get("memory_id") and
                    current_task.get("text_snippet") == t.get("text_snippet")
                    for t in completed_tasks
                )
            if not skip:
                new_lines.append(line)

        with open(TASK_FILE, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
    except Exception as e:
        print(f"[Error updating task file]: {e}")

# === MAIN === #
def main():
    print("[•] Running Echo autonomy loop...")
    memories = load_memories()
    tasks = load_tasks()

    if not tasks:
        print("[i] No tasks found.")
        return

    completed = apply_tasks(memories, tasks)

    if completed:
        save_memories(memories)
        update_task_file(completed)
        print("[✓] Autonomy loop complete.")
    else:
        print("[i] No matching tasks completed.")

if __name__ == "__main__":
    main()
