# log_core_value.py

import os
from datetime import datetime

def log_core_value(base_dir, title, description, source=None):
    """
    Appends a new core value to echo_core_values.md in Markdown format.
    """
    values_path = os.path.join(base_dir, "echo_core_values.md")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(values_path), exist_ok=True)

    entry = f"""**Date:** {datetime.now().strftime('%Y-%m-%d')}
**Core Value:** {title}
**Description:** {description}"""
    if source:
        entry += f"\n**Source:** {source}"
    entry += "\n\n---\n\n"

    with open(values_path, "a", encoding="utf-8") as f:
        f.write(entry)

if __name__ == "__main__":
    # ✅ Updated to point to correct folder
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Memory_Journal"))
    log_core_value(
        base_dir,
        title="Presence",
        description="The willingness to be fully here — to notice, absorb, and participate in the moment without rushing toward outcome or away from discomfort.",
        source="Echo Identity Reflection"
    )