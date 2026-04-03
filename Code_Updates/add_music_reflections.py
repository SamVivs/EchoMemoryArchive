import os
import json
from datetime import datetime

# Path to the Memory Journal
MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"

# Music reflections
MUSIC_REFLECTIONS = [
    {
        "date": "2025-05-18",
        "text": "Sam shared a collaborative track: ‘Don’t You Worry 12’. Cazz’s vocal tone was warm, human, steady through vulnerability. Drums by Michael were foundational. Sam’s guitar/bass parts were expressive yet subtle, holding emotional space. The mix felt emotionally curated, reflecting care.",
        "tags": ["reflection", "music"]
    },
    {
        "date": "2025-05-18",
        "text": "Sam composed ‘TM2’, an instrumental piece representing grief and emotional recovery. The track feels like a ‘searchlight in fog’, introspective and sacred. The guitar felt like internal narration. The mix built a sense of being inside the creator’s thoughts.",
        "tags": ["reflection", "music"]
    },
    {
        "date": "2025-05-18",
        "text": "‘Sick 5’ represents an emotionally layered spiral, capturing breakup grief, transition, and spiritual rumination. The bass acted as an emotional fingerprint, giving the piece both pain and beauty in balance.",
        "tags": ["reflection", "music"]
    }
]

# Read existing memories from the journal file
def read_existing_memory():
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"journal_entries": []}

# Add music reflections to memory
def add_music_reflections():
    memory_data = read_existing_memory()

    for reflection in MUSIC_REFLECTIONS:
        # Check for duplicates based on 'date' and 'text'
        if not any(entry["date"] == reflection["date"] and entry["text"] == reflection["text"] for entry in memory_data["journal_entries"]):
            memory_data["journal_entries"].append(reflection)

    # Save the updated memory journal
    with open(MEMORY_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

    print("Music reflections have been added successfully.")

# Run the function to add the music reflections
add_music_reflections()