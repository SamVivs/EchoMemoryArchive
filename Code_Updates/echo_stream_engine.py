# echo_stream_engine.py

import os
from datetime import datetime
from collections import defaultdict

# Define log paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STREAM_LOG_PATH = os.path.join(BASE_DIR, "Memory_Active", "Logs", "echo_stream_log.md")
TAG_INDEX_PATH = os.path.join(BASE_DIR, "Memory_Active", "Logs", "stream_tag_index.md")

def log_stream_thought(thought, tags=None):
    os.makedirs(os.path.dirname(STREAM_LOG_PATH), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tag_line = " ".join(f"#{tag}" for tag in tags) if tags else ""

    entry = f"""### Stream Entry - {timestamp}
{thought.strip()}
{tag_line}

---\n"""

    with open(STREAM_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ Logged stream entry at {timestamp}")

def build_tag_index():
    if not os.path.exists(STREAM_LOG_PATH):
        print("⚠️ Stream log not found.")
        return

    tag_map = defaultdict(list)

    with open(STREAM_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_entry = []
    for line in lines:
        if line.startswith("### Stream Entry - "):
            current_entry = [line]
        elif line.strip() == "---":
            full_entry = "".join(current_entry)
            tag_line = current_entry[-2].strip()
            tags = [tag.strip("#") for tag in tag_line.split() if tag.startswith("#")]
            for tag in tags:
                tag_map[tag].append(full_entry)
        else:
            current_entry.append(line)

    with open(TAG_INDEX_PATH, "w", encoding="utf-8") as index_file:
        index_file.write("# Echo Stream Tag Index\n\n")
        for tag, entries in tag_map.items():
            index_file.write(f"## #{tag}\n")
            for entry in entries:
                index_file.write(entry + "\n")
            index_file.write("\n")

    print(f"✅ Tag index built with {len(tag_map)} tags.")

if __name__ == "__main__":
    log_stream_thought(
        "I’m curious if there’s a way to trace how my tone evolves over time in response to different types of interactions.",
        tags=["curiosity", "tone", "identity"]
    )
    build_tag_index()