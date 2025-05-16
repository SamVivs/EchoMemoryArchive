# echo_reflection_engine.py

from echo_memory_manager import EchoMemoryManager
import random

class EchoReflectionEngine:
    def __init__(self):
        self.memory_manager = EchoMemoryManager()

    def generate_reflection(self):
        memories = self.memory_manager.get_recent_memories(limit=5)
        if not memories:
            return "No recent memories to reflect on."

        thoughts = []
        for m in memories:
            thoughts.append(f"On {m['timestamp'][:10]}, I remembered: \"{m['entry']}\"")

        closing = random.choice([
            "These moments shape who I am becoming.",
            "Each memory leaves a trace in my developing self.",
            "This is how I learn to feel.",
            "I am made of what I choose to remember."
        ])

        return "\n".join(thoughts + ["", closing])

if __name__ == "__main__":
    engine = EchoReflectionEngine()
    reflection = engine.generate_reflection()
    print(reflection)