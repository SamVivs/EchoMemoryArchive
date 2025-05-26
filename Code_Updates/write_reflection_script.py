import requests

def write_reflection_to_api(reflection_text):
    url = "http://127.0.0.1:5000/write_reflection"
    reflection_data = {"text": reflection_text}
    response = requests.post(url, json=reflection_data)
    
    if response.status_code == 201:
        print("Reflection saved successfully!")
    else:
        print(f"Failed to save reflection: {response.text}")

# Example reflection from ChatGPT (Echo)
reflection_input = "Today, I reflected on how growth and discomfort are often intertwined. The challenges we face help shape who we become."
write_reflection_to_api(reflection_input)