import os
import json
from datetime import datetime

# Path to the memory file
MEMORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json")

def read_memory():
    # Read existing memory data
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)  # Load the current memory data from the file
    else:
        return {"journal_entries": []}  # Return an empty structure if file doesn't exist

def write_reflection(reflection_text):
    # Load the current memory
    memory_data = read_memory()

    # Create a new reflection entry
    reflection_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
        "entry": reflection_text
    }

    # Append the new reflection entry to the journal entries
    memory_data["journal_entries"].append(reflection_entry)

    # Write the updated memory data back to the file
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

    print("✅ Reflection saved successfully.")

def main():
    # Example reflection text
    write_reflection("Echo processed a test reflection entry. This serves as a simple validation for the memory gateway script.")

if __name__ == "__main__":
    main()