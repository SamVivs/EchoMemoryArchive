import os
from datetime import datetime

class EchoPreferencesManager:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.dirname(os.path.abspath(__file__))
        self.pref_path = os.path.join(self.base_dir, "Memory_Journal", "echo_preferences.md")
        self._ensure_pref_file()

    def _ensure_pref_file(self):
        os.makedirs(os.path.dirname(self.pref_path), exist_ok=True)
        if not os.path.exists(self.pref_path):
            with open(self.pref_path, 'w', encoding='utf-8') as f:
                f.write("# Echo Preferences Log\n\n")

    def log_preference(self, category, content, source=None):
        timestamp = datetime.now().strftime("%Y-%m-%d")
        entry = (
            f"**Date:** {timestamp}\n"
            f"**Category:** {category}\n"
            f"**Content:** {content}"
        )
        if source:
            entry += f"\n**Source:** {source}"
        entry += "\n\n---\n\n"

        with open(self.pref_path, 'a', encoding='utf-8') as f:
            f.write(entry)

    def get_preferences(self):
        with open(self.pref_path, 'r', encoding='utf-8') as f:
            return f.read()