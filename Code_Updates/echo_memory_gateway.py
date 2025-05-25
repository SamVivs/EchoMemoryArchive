import json
import os
from datetime import datetime

# Define the memory file path
MEMORY_FILE_PATH = 'D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json'

def initialize_memory():
    # Initialize memory file if it doesn't exist or is empty
    if not os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)
    else:
        # If the file exists, but it's empty, ensure it's a list
        with open(MEMORY_FILE_PATH, 'r+', encoding='utf-8') as f:
            content = f.read().strip()
            if not content:
                f.seek(0)
                json.dump([], f, indent=4, ensure_ascii=False)

def write_reflection(reflection_content):
    # Read the existing memory journal
    with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
        memory_data = json.load(f)

    # Add the new reflection entry to the memory
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reflection_entry = {
        "timestamp": timestamp,
        "reflection": reflection_content
    }

    memory_data.append(reflection_entry)  # Append the new reflection to the list

    # Write the updated memory back to the file
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

# Main logic
def main():
    initialize_memory()  # Ensure the memory file exists and is a list
    write_reflection("Echo processed a test reflection entry. This serves as a simple validation for the memory gateway script.")

if __name__ == "__main__":
    main()