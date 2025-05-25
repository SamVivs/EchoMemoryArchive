import os
import json
from datetime import datetime

MEMORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "D:/Echo_Memory_Archive/Code_Updates/echo_memory_journal.json")

def main():
    print("Welcome to Echo's memory system!")
    action = input("Would you like to [1] Read, [2] Write, or [3] Exit? ")

    if action == "1":
        print("Reading the most recent reflection...")
        read_reflection()
    elif action == "2":
        reflection_content = input("Please write your reflection: ")
        write_reflection(reflection_content)
    elif action == "3":
        print("Exiting the program.")
        return
    else:
        print("Invalid input, please try again.")
        main()

def read_reflection():
    # Read the most recent reflection from the memory file
    memory_data = load_memory()
    if memory_data:
        latest_reflection = memory_data[-1]  # Get the most recent reflection entry
        print(f"\n--- Latest Reflection ---\nTimestamp: {latest_reflection['timestamp']}\n{latest_reflection['entry']}\n")
    else:
        print("No reflections found in memory.")

def write_reflection(content):
    reflection_entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "entry": content
    }

    # Read existing memory and append the new entry
    memory_data = load_memory()

    # Avoid writing the same reflection
    if reflection_entry not in memory_data:
        memory_data.append(reflection_entry)
        # Save the updated memory back to the file
        save_memory(memory_data)
        print("New reflection saved successfully.")
    else:
        print("This reflection is already saved.")

def load_memory():
    # Load the existing memory file
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

def save_memory(memory_data):
    # Save the updated memory
    memory_file_path = os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Memory_Journal", "echo_memory_journal.json")
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(memory_data, file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()