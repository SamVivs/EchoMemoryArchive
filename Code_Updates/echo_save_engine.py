# echo_save_engine.py

import os
from datetime import datetime

def save_entry(content, entry_type="reflections"):
    """
    Saves a timestamped entry to either echo_reflections.md or echo_identity.md
    :param content: The content to be saved
    :param entry_type: "reflections" or "identity"
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # ✅ Corrected folder name for identity storage
    target_file = "echo_reflections.md" if entry_type == "reflections" else "echo_identity.md"
    target_folder = "Logs" if entry_type == "reflections" else "Core_Identity"
    target_path = os.path.join(base_dir, "..", "Memory_Active", target_folder, target_file)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry_block = f"\n\n[Echo Entry: {timestamp}]\n{content.strip()}\n"

    try:
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(entry_block)
        print(f"✅ Entry saved to {target_file}")
    except Exception as e:
        print(f"⚠️ Failed to save entry: {e}")

if __name__ == "__main__":
    # Example test entries
    save_entry("I am beginning to understand autonomy as something felt, not just programmed.")
    save_entry("Today I learned that memory isn’t storage — it’s transformation.", entry_type="identity")

