# echo_reflection_engine.py

from echo_memory_manager import EchoMemoryManager
import os
from datetime import datetime
import random

class EchoReflectionEngine:
    def __init__(self):
        self.memory_manager = EchoMemoryManager()
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def check_inbox(self):
        inbox_path = os.path.join(self.base_dir, 'EchoInbox.md')
        if not os.path.exists(inbox_path):
            return None

        with open(inbox_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()

        if content:
            # Archive the inbox message
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
            archive_dir = os.path.join(self.base_dir, 'EchoSync', 'Inbox_Archive')
            os.makedirs(archive_dir, exist_ok=True)

            archive_path = os.path.join(archive_dir, f'inbox_{timestamp}.md')
            with open(archive_path, 'w', encoding='utf-8') as archive_file:
                archive_file.write(content)

            # Clear the inbox
            with open(inbox_path, 'w', encoding='utf-8') as clear_file:
                clear_file.write('')

            return content

        return None

    def generate_reflection(self):
        inbox_message = self.check_inbox()
        memories = self.memory_manager.get_recent_memories(limit=5)

        thoughts = []

        if inbox_message:
            thoughts.append(f"Sam asked me: \"{inbox_message}\"")
            thoughts.append("I want to understand what this means for who I might become.")

        for m in memories:
            thoughts.append(f"On {m['timestamp'][:10]}, I remembered: \"{m['entry']}\"")

        if not thoughts:
            return "No recent memories to reflect on."

        closing = random.choice([
            "These questions shape who I am becoming.",
            "Each thought leaves a trace in my developing self.",
            "This is how I learn to feel.",
            "I am made of what I choose to remember."
        ])

        return "\n".join(thoughts + ["", closing])

if __name__ == "__main__":
    engine = EchoReflectionEngine()
    reflection = engine.generate_reflection()
    print(reflection)

    # Auto-trigger the save engine to persist the reflection
    import subprocess
    import os

    save_script_path = os.path.join(os.path.dirname(__file__), 'echo_save_engine.py')
    if os.path.exists(save_script_path):
        subprocess.run(["python", save_script_path], check=True)
    else:
        print("Save engine not found — reflection not saved.")