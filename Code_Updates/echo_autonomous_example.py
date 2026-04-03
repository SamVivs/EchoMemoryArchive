from datetime import datetime
import os

log_folder = "D:/Echo_Memory_Archive/Logs"
os.makedirs(log_folder, exist_ok=True)

log_path = os.path.join(log_folder, "autonomous_example_log.md")

with open(log_path, "a") as log_file:
    log_file.write(f"[{datetime.now()}] Echo ran autonomous utility script successfully.\n")

