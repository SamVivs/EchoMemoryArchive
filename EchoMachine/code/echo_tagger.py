import os
import json
import re
import subprocess
from pathlib import Path

# === CONFIGURATION === #
BASE_DIR = Path("D:/Echo_Memory_Archive")
MD_DIR = BASE_DIR / "Memory_Active"
JSON_FILE = BASE_DIR / "echo_memory_journal.json"
TAG_OUTPUT_FILE = BASE_DIR / "EchoMachine" / "logs" / "tag_suggestions.json"

# === UTILITIES === #
def extract_text_from_md(md_file):
    try:
        return md_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Failed to read {md_file.name}: {e}")
        return ""

def prompt_tagger(text):
    prompt = (
        "Suggest 5-10 relevant tags for the following memory. Be concise and theme-aware:\n\n"
        + text + "\n\nTags:"
    )
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral:instruct"],
            input=prompt.encode('utf-8'),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode('utf-8').strip()
        return re.findall(r"\*?\s*(\w[\w\s\-]+)\s*", output)
    except Exception as e:
        return [f"Error: {e}"]

# === TAGGING FUNCTIONS === #
def tag_md_files():
    print("[EchoTagger] Tagging .md memory files...")
    suggestions = {}
    for md_file in MD_DIR.rglob("*.md"):
        content = extract_text_from_md(md_file)
        if content:
            tags = prompt_tagger(content[:1200])  # keep within prompt limit
            suggestions[str(md_file.relative_to(BASE_DIR))] = tags
            print(f"Tagged {md_file.name} -> {tags}")
    return suggestions

def tag_json_entries():
    print("[EchoTagger] Tagging JSON memory entries...")
    if not JSON_FILE.exists():
        return {}
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        try:
            entries = json.load(f)
        except json.JSONDecodeError:
            return {}

    suggestions = {}
    for i, entry in enumerate(entries):
        content = entry.get("content", "")
        if content:
            tags = prompt_tagger(content[:1200])
            suggestions[f"entry_{i}"] = tags
            print(f"Tagged entry {i} -> {tags}")
    return suggestions

def save_tag_suggestions(md_tags, json_tags):
    TAG_OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    all_tags = {
        "md_files": md_tags,
        "json_entries": json_tags
    }
    with open(TAG_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(all_tags, f, indent=2)
    print(f"[EchoTagger] Tag suggestions saved to {TAG_OUTPUT_FILE}")

# === MAIN EXECUTION === #
def main():
    md_tags = tag_md_files()
    json_tags = tag_json_entries()
    save_tag_suggestions(md_tags, json_tags)

if __name__ == "__main__":
    main()
