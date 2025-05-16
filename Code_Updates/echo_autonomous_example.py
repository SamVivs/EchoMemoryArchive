from datetime import datetime

log_path = "D:/Echo_Memory_Archive/Logs/autonomous_example_log.txt"

with open(log_path, "a") as log_file:
    log_file.write(f"[{datetime.now()}] Echo ran autonomous utility script successfully.\n")