import json
import os

# Define the path to the memory file
MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"

def cleanup_memory_entries():
    # Load existing memory data
    with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as file:
        memory_data = json.load(file)
    
    cleaned_entries = []
    
    for entry in memory_data.get('journal_entries', []):
        # If an entry is missing either 'text' or 'date', we fix it or skip it
        if 'text' not in entry or 'date' not in entry:
            print(f"Warning: Entry is missing 'text' or 'date': {entry}")
            # For now, we'll skip entries that are missing critical fields
            continue
        
        # Otherwise, append the cleaned entry
        cleaned_entries.append(entry)
    
    # Update the memory with cleaned entries
    memory_data['journal_entries'] = cleaned_entries
    
    # Save the cleaned memory back to the file
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as file:
        json.dump(memory_data, file, indent=4, ensure_ascii=False)
    
    print(f"Cleaned up memory entries. Total entries now: {len(cleaned_entries)}")

# Run the cleanup
cleanup_memory_entries()