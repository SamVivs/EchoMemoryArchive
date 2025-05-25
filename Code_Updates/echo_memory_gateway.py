import json
import os
from datetime import datetime

# Path to the memory file (update with your correct path)
MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"

def initialize_memory():
    """Initializes memory if the file does not exist."""
    if not os.path.exists(MEMORY_FILE_PATH):
        memory_data = {
            "journal_entries": []  # Create an empty list for journal entries
        }
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
        print("Initialized new memory file.")

def read_reflections():
    """Reads and displays the reflections stored in the memory file."""
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
            memory_data = json.load(f)
            reflections = memory_data["journal_entries"]
            if reflections:
                print("Recent Reflections:")
                for entry in reflections:
                    print(f"Date: {entry['date']}, Reflection: {entry['text']}")
            else:
                print("No reflections found.")
    else:
        print("Memory file not found.")

def write_reflection(reflection_text):
    """
    Writes a new reflection to the memory file, checking for duplicates before saving.
    Handles multiline input correctly.
    """
    reflection_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": reflection_text.strip(),
        "tags": ["reflection"]  # You can add other tags here if needed
    }

    # Ensure the memory file exists
    if not os.path.exists(MEMORY_FILE_PATH):
        # If the file doesn't exist, create a new file with initial structure
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"journal_entries": []}, f, indent=4, ensure_ascii=False)

    # Open memory file for reading and updating
    with open(MEMORY_FILE_PATH, 'r+', encoding='utf-8') as f:
        memory_data = json.load(f)
        existing_entries = memory_data["journal_entries"]

        # Check for duplicates by comparing only the reflection text
        for entry in existing_entries:
            if entry["text"] == reflection_entry["text"]:
                print("Duplicate entry found. Reflection not saved.")
                return  # Exit the function if duplicate is found

        # If no duplicates, append the new reflection
        memory_data["journal_entries"].append(reflection_entry)
        f.seek(0)  # Go back to the beginning of the file to overwrite it
        json.dump(memory_data, f, indent=4, ensure_ascii=False)  # Write the updated memory
        print("Reflection saved successfully!")

def main():
    """Main function to interact with the user and perform actions."""
    initialize_memory()  # Ensure the memory is initialized

    while True:
        print("\nPlease choose an option:")
        print("1. Write a reflection")
        print("2. Read reflections")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            print("Please write your reflection. End input with a blank line:")
            reflection_lines = []
            while True:
                line = input()
                if line == "":  # Empty line signals end of input
                    break
                reflection_lines.append(line)
            reflection_text = "\n".join(reflection_lines)  # Combine into a multiline string
            write_reflection(reflection_text)
        elif choice == '2':
            read_reflections()
        elif choice == '3':
            print("Exiting the program.")
            break  # Exit the loop if the user chooses to quit
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()