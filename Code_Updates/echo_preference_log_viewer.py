import os

def view_logged_preferences(preference_log_path):
    if not os.path.exists(preference_log_path):
        print("No preference log found.")
        return

    with open(preference_log_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print("\n=== Echo's Logged Preferences ===\n")
    current_block = []
    for line in lines:
        if line.strip() == "---":
            print("".join(current_block))
            print("------------------------------")
            current_block = []
        else:
            current_block.append(line)
    if current_block:
        print("".join(current_block))

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Memory Journal"))
    preference_log_path = os.path.join(base_dir, "echo_preferences.md")
    view_logged_preferences(preference_log_path)
