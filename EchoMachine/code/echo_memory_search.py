import json
import re
from pathlib import Path
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
CHANGE_LOG_FILE = BASE_DIR / "memory_change_log.json"
EXPORT_DIR = BASE_DIR / "exports"

# === LOAD EMBEDDING MODEL === #
print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# === LOAD MEMORIES === #
def load_memories():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get("journal_entries", [])
    except Exception as e:
        print(f"[Error loading memory JSON]: {e}")
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

# === EXPORT SEARCH RESULTS === #
def export_results(results, query):
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = EXPORT_DIR / f"search_export_{timestamp}.md"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# Search Export\n\n**Query:** {query}\n\n")
        for i, entry in enumerate(results, 1):
            f.write(f"### [{i}] {entry.get('date', 'No Date')}\n")
            f.write(f"Tags: {', '.join(entry.get('tags', []))}\n\n")
            f.write(f"{entry.get('text') or entry.get('content') or '(no text)'}\n\n")
    print(f"[✓] Results exported to {filename}")

# === SEMANTIC SEARCH === #
def semantic_search(memories, query, top_k=10):
    texts = [m.get("text") or m.get("content") or "" for m in memories]
    embeddings = model.encode(texts, convert_to_tensor=True)
    query_embedding = model.encode(query, convert_to_tensor=True)
    hits = util.semantic_search(query_embedding, embeddings, top_k=top_k)[0]
    return [memories[hit["corpus_id"]] for hit in hits]

# === FALLBACK KEYWORD SEARCH === #
def keyword_search(memories, query):
    query_lower = query.lower()
    return [m for m in memories if query_lower in (m.get("text", "") + m.get("content", "") + str(m.get("tags", [])) + m.get("date", "")).lower()]

# === TAG AND DATE FILTERING === #
def filter_memories(memories, filters):
    for key, value in filters.items():
        if key == 'tag':
            memories = [m for m in memories if any(value in tag.lower() for tag in m.get("tags", []))]
        elif key == 'date':
            memories = [m for m in memories if value in m.get("date", "").lower()]
    return memories

# === DISPLAY RESULTS WITH HIGHLIGHTING === #
def display_results(results, query):
    print("\n===== Top Matching Memories =====")
    for i, entry in enumerate(results):
        date = entry.get("date", "(no date)")
        text = entry.get("text") or entry.get("content") or "(no text)"
        snippet = text.strip().replace("\n", " ")[:80] + ("..." if len(text) > 80 else "")
        if query:
            for word in query.split():
                snippet = re.sub(f"(?i)({re.escape(word)})", r"[\033[1m\1\033[0m]", snippet)
        tags = entry.get("tags", [])
        print(f"[{i+1}] ({date}) \"{snippet}\"\n     → Tags: {tags}")

# === MAIN INTERFACE === #
def main():
    memories = load_memories()
    if not memories:
        print("No memories found.")
        return

    query = input("\nAsk Echo anything: ").strip()

    filters = {}
    tokens = query.split()
    query_parts = []
    for token in tokens:
        if ":" in token:
            k, v = token.split(":", 1)
            filters[k.strip().lower()] = v.strip().lower()
        else:
            query_parts.append(token)
    core_query = " ".join(query_parts).strip()

    results = semantic_search(memories, core_query)
    results = filter_memories(results, filters)

    if not results and core_query:
        print("No semantic matches found — trying keyword fallback...")
        results = keyword_search(memories, core_query)
        results = filter_memories(results, filters)

    if not results:
        print("No matching entries found.")
        return

    display_results(results, core_query)
    export_results(results, core_query)

    while True:
        action = input("\nOptions: [v]iew full | [e]dit | [a]dd tag | [d]elete | [q]uit → ").strip().lower()
        if action == 'q':
            break
        elif action in ['v', 'e', 'a', 'd']:
            try:
                index = int(input("Enter result number: ")) - 1
                if 0 <= index < len(results):
                    entry = results[index]
                    if action == 'v':
                        print(f"\n--- Full Entry ---\nDate: {entry.get('date', 'N/A')}\nTags: {entry.get('tags', [])}\nText:\n{entry.get('text') or entry.get('content') or '(no text)'}")
                    elif action == 'a':
                        new_tag = input("Enter new tag to add: ").strip()
                        if new_tag:
                            entry.setdefault("tags", []).append(new_tag)
                            save_memories(memories)
                            log_change("add_tag", entry)
                            print(f"[✓] Tag '{new_tag}' added.")
                    elif action == 'e':
                        print("\n--- Edit Entry ---")
                        new_date = input(f"New date (or Enter to keep '{entry.get('date', '')}'): ").strip()
                        new_text = input("New full text (or Enter to keep current): ").strip()
                        new_tags = input("New comma-separated tags (or Enter to keep current): ").strip()
                        if new_date:
                            entry['date'] = new_date
                        if new_text:
                            if 'text' in entry:
                                entry['text'] = new_text
                            else:
                                entry['content'] = new_text
                        if new_tags:
                            entry['tags'] = [t.strip() for t in new_tags.split(',') if t.strip()]
                        save_memories(memories)
                        log_change("edit", entry)
                        print("[✓] Entry updated.")
                    elif action == 'd':
                        confirm = input("Are you sure you want to delete this entry? (y/n): ").strip().lower()
                        if confirm == 'y':
                            memories.remove(entry)
                            save_memories(memories)
                            log_change("delete", entry)
                            print("[✓] Entry deleted.")
                else:
                    print("Invalid result number.")
            except ValueError:
                print("Please enter a valid number.")

if __name__ == "__main__":
    main()
