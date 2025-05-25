import requests

def read_reflections_from_memory():
    url = "http://127.0.0.1:5000/read_reflections"
    response = requests.get(url)

    if response.status_code == 200:
        reflections = response.json()
        print("Recent Reflections:")
        for entry in reflections["journal_entries"]:
            print(f"Date: {entry['date']}, Reflection: {entry['text']}")
    else:
        print(f"Failed to retrieve reflections: {response.text}")

read_reflections_from_memory()