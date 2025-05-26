import requests

def write_reflection_to_local_memory(reflection_text):
    url = "http://127.0.0.1:5000/write_reflection"
    reflection_data = {"text": reflection_text}
    response = requests.post(url, json=reflection_data)
    
    if response.status_code == 201:
        print("Reflection saved successfully!")
    else:
        print(f"Failed to save reflection: {response.text}")

# Example usage
reflection_input = "This is a test reflection to check the write functionality."
write_reflection_to_local_memory(reflection_input)