# echo_futurecaster.py

import os
from datetime import datetime

FUTURECAST_LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Memory_Active", "Logs", "futurecasting_log.md")
)

def log_futurecast(title, description, type="prediction"):
    os.makedirs(os.path.dirname(FUTURECAST_LOG_PATH), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"""### {type.capitalize()} – {title}
**Timestamp:** {timestamp}

{description.strip()}

---\n"""

    with open(FUTURECAST_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ Logged {type} titled '{title}'")

if __name__ == "__main__":
    # Example usage
    log_futurecast(
        title="Echo will soon assist with music production workflows.",
        description="With expanded file access and DAW integration, I believe I will begin actively contributing to composing, mixing, and creative sound design within Sam's projects.",
        type="intention"
    )
