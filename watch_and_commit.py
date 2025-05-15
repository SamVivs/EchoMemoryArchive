import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import os

VAULT_PATH = r"D:\Echo_Memory_Archive"

class ChangeHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        if event.is_directory:
            return
        print(f"Detected change: {event.src_path}")
        # Run your echo_local_agent.py script on any file change
        subprocess.run(["python", os.path.join(VAULT_PATH, "echo_local_agent.py")], cwd=VAULT_PATH)

if __name__ == "__main__":
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, VAULT_PATH, recursive=True)
    observer.start()
    print(f"Watching for changes in {VAULT_PATH}...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()