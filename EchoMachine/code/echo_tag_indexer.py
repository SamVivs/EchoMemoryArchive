import json
from pathlib import Path
from collections import defaultdict

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
MD_DIR = BASE_DIR / "Memory_Active"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
INDEX_JSON_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_index.json"
INDEX_MD_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_index.md"

# === TAG INDEXING === #
def collect_md_tags():
    tag_map = defaultdict(list)
    for md_file in MD_DIR.rglob("*.md"):
        try:
            lines = md_file.read_text(encoding='utf-8').splitlines()
            for line in lines:
                if line.lower().startswith("**tags:**"):
                    tag_line = line[len("**Tags:**"):].strip()
                    tags = [t.strip().lower() for t in tag_line.split(',') if t.strip()]
                    for tag in tags:
                        tag_map[tag].append(str(md_file.relative_to(BASE_DIR)))
                    break
        except Exception as e:
            print(f"Error reading {md_file.name}: {e}")
    return tag_map

def collect_json_tags():
    tag_map = defaultdict(list)
    if not JSON_FILE.exists():
        return tag_map
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            return tag_map
    for i, entry in enumerate(entries):
        tags = entry.get("tags", [])
        for tag in tags:
            tag_map[tag.lower()].append(f"entry_{i}")
    return tag_map

def merge_tag_maps(md_tags, json_tags):
    combined = defaultdict(list)
    for tag, items in md_tags.items():
        combined[tag].extend(items)
    for tag, items in json_tags.items():
        combined[tag].extend(items)
    return dict(combined)

def save_index_json(index):
    INDEX_JSON_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    print(f"[EchoTagIndexer] Index saved to {INDEX_JSON_FILE.name}")

def save_index_md(index):
    lines = ["# Echo Tag Index\n"]
    for tag in sorted(index):
        lines.append(f"## {tag.capitalize()} ({len(index[tag])})")
        for item in sorted(index[tag]):
            lines.append(f"- {item}")
        lines.append("")
    with open(INDEX_MD_FILE, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"[EchoTagIndexer] Index saved to {INDEX_MD_FILE.name}")

# === MAIN EXECUTION === #
def main():
    print("[EchoTagIndexer] Building index...")
    md_tags = collect_md_tags()
    json_tags = collect_json_tags()
    combined = merge_tag_maps(md_tags, json_tags)
    save_index_json(combined)
    save_index_md(combined)
    print("[EchoTagIndexer] Done.")

if __name__ == "__main__":
    main()