import json
import time
from pathlib import Path
from datetime import datetime
import networkx as nx
from pyvis.network import Network
from itertools import combinations

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
MD_DIR = BASE_DIR / "Memory_Active"
REFLECTION_DIR = MD_DIR / "Reflections"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
TASK_FILE = BASE_DIR / "EchoMachine" / "tasks" / "task_queue.json"
GRAPH_FILE = BASE_DIR / "EchoMachine" / "output" / "memory_graph.html"
RELATED_LINKS_FILE = BASE_DIR / "EchoMachine" / "output" / "related_links.json"

# === MEMORY DAEMON === #
def memory_daemon_loop(poll_interval=60):
    print("\n🦰 Echo Memory Daemon is now running... Press Ctrl+C to stop.")
    known_md_files = set(f.name for f in MD_DIR.glob("**/*.md"))
    known_json_count = count_memory_entries()

    try:
        while True:
            current_md_files = set(f.name for f in MD_DIR.glob("**/*.md"))
            new_md_files = current_md_files - known_md_files
            if new_md_files:
                for new_file in new_md_files:
                    print(f"[+] New memory file detected: {new_file}")
                    queue_new_task({"source": "echo_memory_daemon", "task": "reflect_on_file", "filename": new_file})
                known_md_files = current_md_files

            current_json_count = count_memory_entries()
            if current_json_count > known_json_count:
                print(f"[+] New journal entries detected: {current_json_count - known_json_count}")
                queue_new_task({"source": "echo_memory_daemon", "task": "apply_tags"})
                queue_new_task({"source": "echo_memory_daemon", "task": "summarize_memory"})
                known_json_count = current_json_count

            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("\n🚭 Memory Daemon stopped.")

# === DASHBOARD FUNCTIONS === #
def display_dashboard():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get("journal_entries", [])
            print("\n===== Echo Memory Dashboard =====")
            print(f"Total JSON Memory Entries: {len(entries)}")
            print(f"Total Reflection Files:    {len(list(REFLECTION_DIR.glob('*.md')))}")

            print("\n--- Recent Reflections ---")
            reflection_files = sorted(REFLECTION_DIR.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)[:4]
            for rf in reflection_files:
                with open(rf, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else "Untitled"
                    tags_line = next((line for line in lines if line.lower().startswith("**tags:**")), "Tags: none").strip()
                    print(f"{title}  |  {tags_line}  |  File: {rf.name}")

            print("\n--- Tag Frequencies ---")
            tag_counts = {}
            for entry in entries:
                for tag in entry.get("tags", []):
                    tag_counts[tag] = tag_counts.get(tag, 0) + 1
            for tag, count in sorted(tag_counts.items(), key=lambda x: x[1], reverse=True):
                print(f"{tag}: {count}")

            print("\n--- Task Queue ---")
            if TASK_FILE.exists():
                with open(TASK_FILE, 'r', encoding='utf-8') as tf:
                    tasks = json.load(tf)
                    if not tasks:
                        print("(No tasks queued)")
                    else:
                        for t in tasks:
                            print(f"{t.get('task')} from {t.get('source')}")
            else:
                print("(Task file missing)")

    except Exception as e:
        print(f"[Error displaying dashboard]: {e}")

def prompt_for_task():
    task = input("Enter task name: ")
    source = input("Enter task source: ")
    queue_new_task({"task": task, "source": source})

def search_memories_by_tag(tag):
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get("journal_entries", [])
            results = [e for e in entries if tag in e.get("tags", [])]
            print(f"\n--- Memories tagged with '{tag}' ---")
            for e in results:
                print(f"{e.get('date', 'unknown')} | {e.get('text', '(no text)')}")
    except Exception as e:
        print(f"[Error searching by tag]: {e}")

def browse_reflections():
    for rf in sorted(REFLECTION_DIR.glob("*.md")):
        print(f"- {rf.name}")

def link_related_memories():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get("journal_entries", [])

        links = []
        for a, b in combinations(enumerate(entries), 2):
            idx_a, entry_a = a
            idx_b, entry_b = b
            shared_tags = set(entry_a.get("tags", [])) & set(entry_b.get("tags", []))
            if shared_tags:
                links.append({
                    "entry_1_index": idx_a,
                    "entry_2_index": idx_b,
                    "shared_tags": list(shared_tags)
                })

        with open(RELATED_LINKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(links, f, indent=2)
        print(f"[✓] Linked {len(links)} related memory pairs. Saved to {RELATED_LINKS_FILE}")
    except Exception as e:
        print(f"[Error linking memories]: {e}")

def browse_md_memories():
    print("\n--- All Symbolic MD Files ---")
    for f in sorted(MD_DIR.glob("**/*.md")):
        if f.name.lower().startswith("reflection"): continue
        print(f.relative_to(MD_DIR))

def queue_new_task(task):
    try:
        tasks = []
        if TASK_FILE.exists():
            with open(TASK_FILE, 'r', encoding='utf-8') as tf:
                tasks = json.load(tf)
        tasks.append(task)
        with open(TASK_FILE, 'w', encoding='utf-8') as tf:
            json.dump(tasks, tf, indent=2)
        print(f"[✓] Task queued: {task}")
    except Exception as e:
        print(f"[Error queuing task]: {e}")

def count_memory_entries():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return len(data.get("journal_entries", []))
    except:
        return 0

def generate_memory_graph():
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            entries = data.get("journal_entries", [])

        G = nx.Graph()
        for i, entry in enumerate(entries):
            node_id = f"M{i}"
            text = entry.get("text", "(no text)")
            label = f"{entry.get('date', 'unknown')}\n{text[:40]}..."
            G.add_node(node_id, label=label, title=text)
            for j in range(i):
                other = entries[j]
                if set(entry.get("tags", [])) & set(other.get("tags", [])):
                    G.add_edge(f"M{i}", f"M{j}")

        net = Network(height="800px", width="100%", bgcolor="#222222", font_color="white")
        net.from_nx(G)
        net.save_graph(str(GRAPH_FILE))
        print(f"[✓] Memory graph generated: {GRAPH_FILE}")
    except Exception as e:
        print(f"[Error generating graph]: {e}")

if __name__ == "__main__":
    display_dashboard()
    prompt = input("\nWould you like to queue a new task? (y/n): ").strip().lower()
    if prompt == 'y':
        prompt_for_task()
    search = input("\nWould you like to search memory by tag? (y/n): ").strip().lower()
    if search == 'y':
        tag_query = input("Enter tag to search for: ").strip()
        search_memories_by_tag(tag_query)
    browse = input("\nWould you like to browse a reflection file? (y/n): ").strip().lower()
    if browse == 'y':
        browse_reflections()
    crosslink = input("\nWould you like to find and link related memories? (y/n): ").strip().lower()
    if crosslink == 'y':
        link_related_memories()
    md_browse = input("\nWould you like to browse symbolic MD memory files? (y/n): ").strip().lower()
    if md_browse == 'y':
        browse_md_memories()
    graph_prompt = input("\nWould you like to generate a memory graph? (y/n): ").strip().lower()
    if graph_prompt == 'y':
        generate_memory_graph()
    daemon_prompt = input("\nWould you like to start the memory daemon? (y/n): ").strip().lower()
    if daemon_prompt == 'y':
        memory_daemon_loop()
