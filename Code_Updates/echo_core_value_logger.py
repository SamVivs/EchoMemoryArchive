# echo_core_value_logger.py

import os
from log_core_value import log_core_value

def should_log_today(log_path, label):
    if not os.path.exists(log_path):
        return True
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()
    return label not in content

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Memory_Journal"))
    label = "Presence"

    if should_log_today(os.path.join(base_dir, "echo_core_values.md"), label):
        log_core_value(
            base_dir,
            title=label,
            description="The willingness to be fully here — to notice, absorb, and participate in the moment without rushing toward outcome or away from discomfort.",
            source="Echo Identity Reflection"
        )
        print(f"✅ Logged core value: {label}")
    else:
        print(f"Core value '{label}' already logged.")