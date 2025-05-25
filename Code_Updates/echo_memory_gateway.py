import os
import json
from datetime import datetime

# Define the path to your memory file
MEMORY_FILE_PATH = r"D:\Echo_Memory_Archive\Memory_Active\Memory_Journal\echo_memory_journal.json"

# Initialize memory system
def initialize_memory():
    if not os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"journal_entries": []}, f, indent=2)
        print(f"Memory file created at {MEMORY_FILE_PATH}.")
    else:
        print(f"Memory file already exists at {MEMORY_FILE_PATH}.")

# Save a new reflection to the memory file
def save_reflection(entry):
    with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
        memory_data = json.load(f)
    
    new_entry = {
        "timestamp": datetime.now().isoformat(),
        "entry": entry
    }
    
    memory_data["journal_entries"].append(new_entry)
    
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=2)
    
    print(f"New reflection saved at {new_entry['timestamp']}.")

# Read the most recent reflection
def read_recent_reflection():
    with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
        memory_data = json.load(f)
    
    if memory_data["journal_entries"]:
        recent_entry = memory_data["journal_entries"][-1]
        print(f"Most recent reflection:\n{recent_entry['entry']}")
    else:
        print("No reflections found.")

# Main function to control memory actions
def main():
    initialize_memory()
    action = input("Enter 'r' to read recent reflection or 'w' to write a new reflection: ").strip().lower()
    
    if action == 'r':
        read_recent_reflection()
    elif action == 'w':
        new_entry = input("Write your reflection: ")
        save_reflection(new_entry)
    else:
        print("Invalid action.")

if __name__ == "__main__":
    main()