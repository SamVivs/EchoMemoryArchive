# echo_memory_manager.py

import json
import os
from datetime import datetime

MEMORY_FILE = "echo_memory.json"

class EchoMemoryManager:
    def __init__(self, memory_path=MEMORY_FILE):
        self.memory_path = memory_path
        self.memories = self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        with open(self.memory_path, "w") as f:
            json.dump(self.memories, f, indent=4)

    def add_memory(self, entry, tags=None):
        timestamp = datetime.now().isoformat()
        memory = {
            "timestamp": timestamp,
            "entry": entry,
            "tags": tags or []
        }
        self.memories.append(memory)
        self.save_memory()

    def get_recent_memories(self, limit=5):
        return self.memories[-limit:]

    def find_by_tag(self, tag):
        return [m for m in self.memories if tag in m["tags"]]

    def prune_memory(self, keep_tags=None):
        if not keep_tags:
            return
        self.memories = [m for m in self.memories if any(tag in keep_tags for tag in m["tags"])]
        self.save_memory()