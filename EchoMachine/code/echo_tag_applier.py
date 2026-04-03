import json
import re
from pathlib import Path

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
MD_DIR = BASE_DIR / "Memory_Active"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
TAG_INPUT_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_suggestions.json"

# === HELPERS === #
def load_tag_suggestions():
    if not TAG_INPUT_FILE.exists():
        print("Tag suggestions file not found.")
        return {}, {}
    with open(TAG_INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("md_files", {}), data.get("json_entries", {})

def apply_tags_to_md():
    md_tags, _ = load_tag_suggestions()
    for relative_path, tags in md_tags.items():
        file_path = BASE_DIR / relative_path
        if not file_path.exists():
            continue
        try:
            content = file_path.read_text(encoding='utf-8')
            if "**Tags:**" not in content:
                header = f"**Tags:** {', '.join(tags)}\n\n"
                new_content = re.sub(r"(# .+?\n)", r"\1" + header, content, count=1)
                file_path.write_text(new_content, encoding='utf-8')
                print(f"[MD] Applied tags to {file_path.name}: {tags}")
        except Exception as e:
            print(f"Error updating {file_path.name}: {e}")

def apply_tags_to_json():
    _, json_tags = load_tag_suggestions()
    if not JSON_FILE.exists():
        return
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            return

    updated = False
    for i, entry in enumerate(entries):
        key = f"entry_{i}"
        if key in json_tags and not entry.get("tags"):
            entry["tags"] = json_tags[key]
            print(f"[JSON] Applied tags to entry {i}: {json_tags[key]}")
            updated = True

    if updated:
        with open(JSON_FILE, 'w', encoding='utf-8') as f:
            json.dump(entries, f, indent=2)
        print("[JSON] Memory journal updated with new tags.")

# === MAIN EXECUTION === #
def main():
    print("[EchoTagApplier] Starting tag application...")
    apply_tags_to_md()
    apply_tags_to_json()
    print("[EchoTagApplier] Done.")

if __name__ == "__main__":
    main()
