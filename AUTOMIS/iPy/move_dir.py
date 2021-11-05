import sys
import os
import time
import logging
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        folder_to_track = sys.argv[1]
        folder_destination = sys.argv[2]
        for filename in os.listdir(folder_to_track):
            src = folder_to_track+'/'+filename
            new_dest = folder_destination+'/'+filename
            os.rename(src,new_dest)
            # subprocess.run(['python3', 'sort.py', f'-s {src}', f'-t {new_dest}', '-o i'])


def main():
    folder_to_track = sys.argv[1]
    # folder_destination = sys.argv[2]
    observer = Observer()
    event_handler = Handler()
    observer.schedule(event_handler, folder_to_track, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(60)
    except:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()