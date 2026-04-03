import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

VAULT_PATH = r"D:\Echo_Memory_Archive"
ECHO_AGENT_SCRIPT = os.path.join(VAULT_PATH, "echo_local_agent.py")
LOG_FILE = os.path.join(VAULT_PATH, "watcher_log.txt")

class EchoVaultHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        # Ignore events triggered by the log file itself or temp files
        if event.is_directory:
            return
        if event.src_path.endswith(".tmp") or event.src_path.endswith(".log"):
            return

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write(f"Change detected: {event.event_type} on {event.src_path}\n")
            log.write("Running echo_local_agent.py...\n")

        try:
            subprocess.run(["python", ECHO_AGENT_SCRIPT], cwd=VAULT_PATH, check=True)
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write("echo_local_agent.py completed successfully.\n")
        except subprocess.CalledProcessError as e:
            with open(LOG_FILE, "a", encoding="utf-8") as log:
                log.write(f"Error running echo_local_agent.py: {e}\n")

if __name__ == "__main__":
    event_handler = EchoVaultHandler()
    observer = Observer()
    observer.schedule(event_handler, path=VAULT_PATH, recursive=True)
    observer.start()

    with open(LOG_FILE, "a", encoding="utf-8") as log:
        log.write("Watcher started.\n")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        with open(LOG_FILE, "a", encoding="utf-8") as log:
            log.write("Watcher stopped by user.\n")
    observer.join()