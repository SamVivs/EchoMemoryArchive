import requests

def read_reflections_from_memory():
    url = "http://127.0.0.1:5000/read_reflections"
    response = requests.get(url)

    if response.status_code == 200:
        reflections = response.json()

        # Check if the response is a list or a dictionary
        if isinstance(reflections, list):
            print("Recent Reflections:")
            for entry in reflections:
                print(f"Date: {entry['date']}, Reflection: {entry['text']}")
        else:
            print("Unexpected structure: Reflections are not in a list format.")
    else:
        print(f"Failed to retrieve reflections: {response.text}")

read_reflections_from_memory()