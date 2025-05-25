import os
import json
from datetime import datetime

# Define the path to the memory journal (this should be the correct path)
MEMORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Memory_Journal", "echo_memory_journal.json")

def write_reflection(reflection_text):
    # Get the current date and time for the reflection
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reflection_entry = {
        "date": timestamp,
        "text": reflection_text,
        "tags": ["reflection"]
    }

    # Check if the memory file exists and read existing data
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            existing_reflections = json.load(f)
    else:
        existing_reflections = {"journal_entries": []}

    # Check for duplicates by comparing entry structure (date and text)
    duplicate = False
    for entry in existing_reflections.get("journal_entries", []):
        if entry["text"] == reflection_entry["text"] and entry["date"] == reflection_entry["date"]:
            duplicate = True
            break

    if duplicate:
        print("Reflection already exists.")
        return

    # Append the new reflection
    existing_reflections["journal_entries"].append(reflection_entry)

    # Write the updated reflections back to the file
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(existing_reflections, f, indent=4, ensure_ascii=False)

    print(f"Reflection saved successfully: {reflection_entry['text']}")

def read_reflections():
    # Read the reflections from the memory file
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            existing_reflections = json.load(f)
        
        print("Recent Reflections:")
        for entry in existing_reflections.get("journal_entries", []):
            print(f"Date: {entry['date']}, Reflection: {entry['text']}")
    else:
        print("No reflections found.")

# Main execution block
if __name__ == "__main__":
    print("Please choose an option:")
    print("1. Write a reflection")
    print("2. Read reflections")
    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        reflection_text = input("Please write your reflection: ").strip()
        write_reflection(reflection_text)
    elif choice == "2":
        read_reflections()
    else:
        print("Invalid choice. Please enter 1 or 2.")