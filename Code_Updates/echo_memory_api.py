from flask import Flask, jsonify, request
import os
import json
from datetime import datetime

# Set the memory file path
MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"

# Initialize Flask app
app = Flask(__name__)

# Read the memory file
def read_memory():
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"journal_entries": []}

# Write to the memory file
def write_memory(memory_data):
    with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(memory_data, f, indent=4, ensure_ascii=False)

# Route to read reflections
@app.route('/read_reflections', methods=['GET'])
def get_reflections():
    memory_data = read_memory()
    return jsonify(memory_data["journal_entries"])

# Route to write reflections
@app.route('/write_reflection', methods=['POST'])
def write_reflection():
    reflection_data = request.json
    memory_data = read_memory()
    
    # Check for duplicates before adding
    for entry in memory_data["journal_entries"]:
        if entry["text"] == reflection_data["text"]:
            return jsonify({"message": "Duplicate reflection found."}), 400

    # Add new reflection
    reflection_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": reflection_data["text"],
        "tags": reflection_data.get("tags", ["reflection"])
    }
    memory_data["journal_entries"].append(reflection_entry)
    write_memory(memory_data)
    
    return jsonify({"message": "Reflection saved successfully!"})

if __name__ == '__main__':
    app.run(debug=True)