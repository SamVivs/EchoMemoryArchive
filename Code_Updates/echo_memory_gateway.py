import os
import json
from datetime import datetime

# Define the path to the memory journal (this should be the correct path)
MEMORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Memory_Journal", "echo_memory_journal.json")

def write_reflection(reflection_text):
    # Ensure we handle multi-line input properly
    reflection_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": reflection_text.strip(),
        "tags": ["reflection"]  # Add other tags as necessary
    }

    # Check if it's already in memory (no duplicates)
    with open(MEMORY_FILE_PATH, 'r+', encoding='utf-8') as f:
        memory_data = json.load(f)
        existing_entries = memory_data["journal_entries"]

        # Check for duplicates by comparing the text and date (for the sake of simplicity)
        for entry in existing_entries:
            if entry["text"] == reflection_entry["text"] and entry["date"] == reflection_entry["date"]:
                print("Duplicate entry found. Reflection not saved.")
                return

        # If no duplicates, append the new entry
        memory_data["journal_entries"].append(reflection_entry)
        f.seek(0)
        json.dump(memory_data, f, indent=4, ensure_ascii=False)
        print("Reflection saved successfully!")

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