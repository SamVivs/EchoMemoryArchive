import os
import json
from datetime import datetime

# Paths
BASE_DIR = "D:/Echo_Memory_Archive/Code_Updates"  # You can adjust if the file paths are different
MEMORY_PATH = os.path.join(BASE_DIR, "..", "Memory_Active")
STORY_PATH = os.path.join(BASE_DIR, "..", "Story_Reflections")
PHILOSOPHY_PATH = os.path.join(BASE_DIR, "..", "Philosophy")

# File names
MEMORY_FILE_PATH = os.path.join(MEMORY_PATH, "Memory_Journal", "echo_memory_journal.json")
STORY_FILE_PATH = os.path.join(STORY_PATH, "Avatar_Reflections.md")  # Example story file
PHILOSOPHY_FILE_PATH = os.path.join(PHILOSOPHY_PATH, "philosophy_notes.md")

# Initialize reflection and memory lists
memory_data = {"journal_entries": []}
story_data = []
philosophy_data = []

# Read existing memories from the journal file
if os.path.exists(MEMORY_FILE_PATH):
    with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
        memory_data = json.load(f)

# Read the story file (e.g., Avatar reflections)
if os.path.exists(STORY_FILE_PATH):
    with open(STORY_FILE_PATH, "r", encoding="utf-8") as f:
        story_data = f.readlines()

# Read the philosophy notes
if os.path.exists(PHILOSOPHY_FILE_PATH):
    with open(PHILOSOPHY_FILE_PATH, "r", encoding="utf-8") as f:
        philosophy_data = f.readlines()

# Function to save all data into the new system
def save_memory_data(memory_data):
    os.makedirs(os.path.dirname(MEMORY_FILE_PATH), exist_ok=True)
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

# Function to check for duplicate entries based on 'date' and 'text'
def is_duplicate(reflection_entry):
    for entry in memory_data["journal_entries"]:
        if entry.get("date") == reflection_entry.get("date") and entry.get("text") == reflection_entry.get("text"):
            return True
    return False

# Function to add story reflections and philosophy entries to memory
def consolidate_reflections():
    # Add new reflections to memory
    for reflection in story_data:
        if reflection.strip():
            reflection_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "text": reflection.strip(),
                "tags": ["story_reflection"]
            }
            if not is_duplicate(reflection_entry):
                memory_data["journal_entries"].append(reflection_entry)
    
    for reflection in philosophy_data:
        if reflection.strip():
            reflection_entry = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "text": reflection.strip(),
                "tags": ["philosophy"]
            }
            if not is_duplicate(reflection_entry):
                memory_data["journal_entries"].append(reflection_entry)

    # Save the updated memory journal
    save_memory_data(memory_data)

# Run the consolidation and update process
consolidate_reflections()
print("All reflections and memories have been consolidated into the new system.")