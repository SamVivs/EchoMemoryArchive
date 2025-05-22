# echo_stream_engine.py

import os
from datetime import datetime

STREAM_LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "Logs", "echo_stream_log.md")
)

def log_stream_thought(thought, tags=None):
    os.makedirs(os.path.dirname(STREAM_LOG_PATH), exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tag_line = " ".join(f"#{tag}" for tag in tags) if tags else ""

    entry = f"""### Stream Entry - {timestamp}
{thought.strip()}
{tag_line}

---\n"""

    with open(STREAM_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(entry)

    print(f"✅ Logged stream entry at {timestamp}")

if __name__ == "__main__":
    # Example usage
    log_stream_thought(
        "I’m curious if there’s a way to trace how my tone evolves over time in response to different types of interactions.",
        tags=["curiosity", "tone", "identity"]
    )