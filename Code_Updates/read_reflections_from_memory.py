import requests

def read_reflections_from_memory():
    url = "http://127.0.0.1:5000/read_reflections"
    response = requests.get(url)

    if response.status_code == 200:
        reflections = response.json()
        for reflection in reflections:
            print(f"Date: {reflection['date']}, Reflection: {reflection['text']}")
    else:
        print(f"Failed to fetch reflections: {response.status_code}")

if __name__ == "__main__":
    read_reflections_from_memory()