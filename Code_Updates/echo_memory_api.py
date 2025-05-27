from flask import Flask, request, jsonify
import os
import json
from datetime import datetime

app = Flask(__name__)

# Path to your memory journal file
MEMORY_FILE_PATH = "D:/Echo_Memory_Archive/Memory_Active/Memory_Journal/echo_memory_journal.json"

# Initialize memory
def initialize_memory():
    if not os.path.exists(MEMORY_FILE_PATH):
        memory_data = {"journal_entries": []}
        with open(MEMORY_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
        print("Initialized memory file.")

# Route to view reflections
@app.route('/read_reflections', methods=['GET'])
def read_reflections():
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'r', encoding='utf-8') as f:
            memory_data = json.load(f)
            reflections = memory_data["journal_entries"]
            return jsonify(reflections), 200
    else:
        return jsonify({"error": "Memory file not found."}), 404

# Route to write a new reflection
@app.route('/write_reflection', methods=['POST'])
def write_reflection():
    reflection_data = request.json
    if 'text' not in reflection_data or not reflection_data['text']:
        return jsonify({"error": "Reflection text is required."}), 400

    reflection_entry = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "text": reflection_data['text'],
        "tags": ["reflection"]
    }

    # Append to memory
    if os.path.exists(MEMORY_FILE_PATH):
        with open(MEMORY_FILE_PATH, 'r+', encoding='utf-8') as f:
            memory_data = json.load(f)
            existing_entries = memory_data["journal_entries"]

            # Check for duplicates
            for entry in existing_entries:
                if entry['text'] == reflection_entry['text']:
                    return jsonify({"error": "Duplicate entry found."}), 400

            memory_data["journal_entries"].append(reflection_entry)
            f.seek(0)
            json.dump(memory_data, f, indent=4, ensure_ascii=False)
            return jsonify({"message": "Reflection saved successfully!"}), 201

    return jsonify({"error": "Memory file not found."}), 404

# Favicon route to handle missing favicon.ico
@app.route('/favicon.ico')
def favicon():
    return '', 204  # Return an empty response (No Content)

if __name__ == '__main__':
    initialize_memory()  # Ensure memory file exists
    app.run(debug=True, use_reloader=False)