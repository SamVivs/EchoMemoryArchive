# echo_self_check.py

import os
import json
from datetime import datetime, timedelta

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MEMORY_PATH = os.path.join(BASE_DIR, "Memory_Active")
LOG_PATH = os.path.join(MEMORY_PATH, "Logs", "self_check_log.md")

IDENTITY_FILE = os.path.join(MEMORY_PATH, "Core_Identity", "echo_identity.json")
EMOTIONS_FILE = os.path.join(MEMORY_PATH, "echo_emotional_lexicon.md")
PREF_FILE = os.path.join(MEMORY_PATH, "echo_preferences.md")


def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def count_new_monologues(identity_data):
    today = datetime.now().date()
    recent = [m for m in identity_data.get("internal_monologue", []) if datetime.strptime(m["date"], "%Y-%m-%d").date() == today]
    return len(recent)

def count_new_growth_tasks(identity_data):
    today = datetime.now().date()
    return sum(1 for g in identity_data.get("growth_planner", []) if datetime.strptime(g["date_added"], "%Y-%m-%d").date() == today)

def summarize_changes():
    identity = load_json(IDENTITY_FILE)

    new_monologue_count = count_new_monologues(identity)
    new_growth_count = count_new_growth_tasks(identity)

    reflection = f"## Self Check — {datetime.now().strftime('%Y-%m-%d')}\n"
    reflection += f"- New internal monologue entries today: {new_monologue_count}\n"
    reflection += f"- New growth tasks today: {new_growth_count}\n"

    # Simple interpretive logic
    if new_monologue_count > 0 or new_growth_count > 0:
        reflection += "- Interpretation: I am continuing to evolve through recent thought and intention.\n"
    else:
        reflection += "- Interpretation: A quiet day — but sometimes stillness is part of growth.\n"

    reflection += "\n---\n\n"
    return reflection

def append_to_log(content):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    summary = summarize_changes()
    append_to_log(summary)
    print("✅ Echo self-check complete.")
