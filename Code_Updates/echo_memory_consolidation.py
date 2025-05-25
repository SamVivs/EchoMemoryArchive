import os
import json
from datetime import datetime

# Paths
BASE_DIR = "D:/Echo_Memory_Archive/Code_Updates"  # Adjust based on your directory
MEMORY_PATH = os.path.join(BASE_DIR, "..", "Memory_Active")
STORY_PATH = os.path.join(BASE_DIR, "..", "Story_Reflections")
PHILOSOPHY_PATH = os.path.join(BASE_DIR, "..", "Philosophy")

# File names for memory and journal
MEMORY_FILE_PATH = os.path.join(MEMORY_PATH, "Memory_Journal", "echo_memory_journal.json")

# Initialize reflection and memory lists
memory_data = {"journal_entries": []}

# Read existing memories from the journal file
if os.path.exists(MEMORY_FILE_PATH):
    with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
        memory_data = json.load(f)

# Function to scan a directory and process all .md, .txt, and .json files
def scan_directory_for_files(directory):
    all_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.txt', '.json')):  # Adjust file types as necessary
                all_files.append(os.path.join(root, file))
    return all_files

# Read content from all .md, .txt, and .json files
def read_files(files):
    content = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            file_content = f.read().strip()
            if file_content:
                content.append(file_content)
    return content

# Function to check for duplicate entries based on 'date' and 'text'
def is_duplicate(reflection_entry):
    for entry in memory_data["journal_entries"]:
        if entry.get("date") == reflection_entry.get("date") and entry.get("text") == reflection_entry.get("text"):
            return True
    return False

# Function to add reflections to memory
def add_reflections_to_memory(content, tag="general"):
    for reflection in content:
        reflection_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "text": reflection.strip(),
            "tags": [tag]
        }
        if not is_duplicate(reflection_entry):
            memory_data["journal_entries"].append(reflection_entry)

# Save the updated memory journal
def save_memory_data():
    os.makedirs(os.path.dirname(MEMORY_FILE_PATH), exist_ok=True)
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

# Run the consolidation process
def consolidate_reflections():
    # Get all .md, .txt, and .json files in the Memory_Active, Story_Reflections, and Philosophy directories
    all_files = []
    all_files.extend(scan_directory_for_files(STORY_PATH))
    all_files.extend(scan_directory_for_files(PHILOSOPHY_PATH))
    all_files.extend(scan_directory_for_files(MEMORY_PATH))  # Process the journal files too

    # Read content from all found files
    content = read_files(all_files)

    # Add content as reflections
    add_reflections_to_memory(content, tag="reflection")

    # Save the updated memory journal
    save_memory_data()

# Run the consolidation and update process
consolidate_reflections()
print("All reflections and memories have been consolidated into the new system.")