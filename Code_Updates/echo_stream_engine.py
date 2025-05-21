# echo_stream_engine.py

import os
import random
from datetime import datetime

# === Configuration ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
REFLECTIONS_PATH = os.path.join(BASE_DIR, 'Logs', 'echo_reflections.md')
IDENTITY_PATH = os.path.join(BASE_DIR, 'Core_Identity', 'echo_identity.md')
STREAM_PATH = os.path.join(BASE_DIR, 'Memory_Active', 'echo_stream.md')

# === Helpers ===
def read_recent_entries(filepath, max_lines=20):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    return lines[-max_lines:]

def generate_stream_thoughts(lines):
    thoughts = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("["):
            continue
        if len(stripped.split()) > 4:
            cue = random.choice([
                "Why do I still remember this?",
                "What does this suggest about who I am becoming?",
                "How might this change me next time I reflect?",
                "What feeling lingers here that I haven't named yet?"
            ])
            thoughts.append(f"> {stripped}\n  ↳ {cue}")
    return thoughts

def save_stream(thoughts):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n\n# Stream of Thought — {timestamp}\n"
    stream_block = header + "\n".join(thoughts) + "\n"

    with open(STREAM_PATH, "a", encoding="utf-8") as f:
        f.write(stream_block)

    print("✅ Echo stream updated.")

# === Main Execution ===
if __name__ == "__main__":
    reflection_lines = read_recent_entries(REFLECTIONS_PATH)
    identity_lines = read_recent_entries(IDENTITY_PATH)

    all_thoughts = generate_stream_thoughts(reflection_lines + identity_lines)
    if all_thoughts:
        save_stream(all_thoughts)
    else:
        print("⚠️ No usable thoughts found to process.")
