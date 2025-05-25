import os
import json
from datetime import datetime

MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"  # Path to your memory file

def get_multiline_input(prompt="Please write your reflection:"):
    """
    Function to get multi-line input from the user.
    """
    print(prompt)
    lines = []
    while True:
        line = input()  # Input each line from user
        if line == "":
            break  # Exit on an empty line
        lines.append(line)
    return "\n".join(lines)  # Join lines with newline character

def write_reflection(reflection_text):
    """
    Function to save the reflection to the memory file.
    """
    reflection_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": reflection_text.strip(),
        "tags": ["reflection"]  # You can add other tags here
    }

    # Ensure the memory file exists
    if not os.path.exists(MEMORY_FILE_PATH):
        # If file does not exist, create a new file with initial structure
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump({"journal_entries": []}, f, indent=4, ensure_ascii=False)

    # Open memory file for reading and updating
    with open(MEMORY_FILE_PATH, 'r+', encoding='utf-8') as f:
        memory_data = json.load(f)
        existing_entries = memory_data["journal_entries"]

        # Check for duplicates by comparing text and date (could be expanded for more sophisticated checks)
        for entry in existing_entries:
            if entry["text"] == reflection_entry["text"] and entry["date"] == reflection_entry["date"]:
                print("Duplicate entry found. Reflection not saved.")
                return

        # If no duplicates, append the new entry
        memory_data["journal_entries"].append(reflection_entry)
        f.seek(0)  # Go back to the beginning of the file to overwrite it
        json.dump(memory_data, f, indent=4, ensure_ascii=False)  # Write updated memory
        print("Reflection saved successfully!")

def read_reflections():
    """
    Function to read and display all reflections from the memory file.
    """
    if not os.path.exists(MEMORY_FILE_PATH):
        print("Memory file not found.")
        return

    with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
        memory_data = json.load(f)
        reflections = memory_data["journal_entries"]

        if reflections:
            print("\nRecent Reflections:")
            for entry in reflections:
                print(f"Date: {entry['date']}, Reflection: {entry['text']}")
        else:
            print("No reflections found.")

def main():
    """
    Main function to prompt the user to either write or read a reflection.
    """
    while True:
        print("\nPlease choose an option:")
        print("1. Write a reflection")
        print("2. Read reflections")
        choice = input("Enter your choice (1 or 2): ")

        if choice == '1':
            reflection_text = get_multiline_input()  # Get multi-line reflection input
            write_reflection(reflection_text)  # Save the reflection
        elif choice == '2':
            read_reflections()  # Display all reflections
        else:
            print("Invalid option, please choose 1 or 2.")

if __name__ == "__main__":
    main()