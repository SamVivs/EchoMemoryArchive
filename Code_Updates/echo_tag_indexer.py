# echo_tag_indexer.py

import os
import re
from collections import defaultdict

STREAM_LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Logs", "echo_stream_log.md")
)
INDEX_OUTPUT_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Logs", "stream_tag_index.md")
)

def build_tag_index():
    if not os.path.exists(STREAM_LOG_PATH):
        print("⚠️ No stream log found.")
        return

    with open(STREAM_LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    entries = content.strip().split("---\n")
    tag_map = defaultdict(list)

    for entry in entries:
        timestamp_match = re.search(r"### Stream Entry - ([^\n]+)", entry)
        timestamp = timestamp_match.group(1) if timestamp_match else "Unknown time"

        tags = re.findall(r"#(\w+)", entry)
        entry_text = re.sub(r"### Stream Entry - .+\n", "", entry).strip()

        for tag in tags:
            tag_map[tag].append((timestamp, entry_text))

    with open(INDEX_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("# Stream Tag Index\n\n")
        for tag in sorted(tag_map.keys()):
            f.write(f"## #{tag}\n")
            for timestamp, text in tag_map[tag]:
                f.write(f"- **{timestamp}**: {text}\n")
            f.write("\n")

    print(f"✅ Tag index built with {len(tag_map)} tags.")

if __name__ == "__main__":
    build_tag_index()