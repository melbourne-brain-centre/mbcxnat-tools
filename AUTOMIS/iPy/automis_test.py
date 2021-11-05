import sys
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler


def on_created(event):
    # subprocess.run(['python3', 'sort.py', f'-s {src}', f'-t {new_dest}', '-o i'])
    print("created")
        
def on_deleted(event):
    print("deleted")
        
def on_modified(event):
    return

def on_moved(event):
    print("moved")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileSystemEventHandler()

    event_handler.on_created = on_created
    event_handler.on_deleted = on_deleted
    event_handler.on_modified = on_modified
    event_handler.on_moved = on_moved

    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
