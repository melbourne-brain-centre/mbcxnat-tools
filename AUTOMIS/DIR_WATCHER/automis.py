# The Observer watches for any file change and then dispatches the respective events to an event handler.
from typing import final
from watchdog.observers import Observer
# The event handler will be notified when an event occurs.
from watchdog.events import FileSystemEventHandler
import time
import config
import os
from checker import FileChecker
import datetime
from colorama import Fore, Style, init
import subprocess

init()

GREEN = Fore.GREEN
BLUE = Fore.BLUE
RED = Fore.RED
YELLOW = Fore.YELLOW

event2color = {
    "created": GREEN,
    "modified": BLUE,
    "deleted": RED,
    "moved": YELLOW,
}

def check_size(path):
    """Utility function to check file size"""
    return subprocess.check_output(['du','-s', path]).split()[0].decode('utf-8')

def check_upload(now, path):
    """Utility function to check for upload completion """
    initial_size = check_size(path)
    print_with_color(f"{now} -- Receiving {path} size = {int(initial_size)/1024} Mb", color=BLUE)
    time.sleep(5)
    final_size = check_size(path)
    while True:
        if initial_size == final_size:
            print_with_color(f"{now} -- Recieve Complete Directory Size = {int(final_size)/1024} Mb", color=BLUE)
            return
        else:
            initial_size = check_size(path)
            print_with_color(f"{now} -- Receiving {path} size = {int(initial_size)/1024} Mb", color=BLUE)
            time.sleep(2)
            final_size = check_size(path)

def dicom_sort(now,src_path, dest_path):
    """Utility function to sort incomming dicom dirs"""
    if not os.path.exists(f'{dest_path}'):
        print_with_color(f"{now} -- DICOM SORT START", color=BLUE)
        subprocess.run(['python', './dicom-sort.py', '-s', f'{src_path}', '-t', f'{dest_path}', '-o', 'i'])
        print_with_color(f"{now} -- DICOM SORT SUCCESS -- {src_path}", color=GREEN)

def create_table(now, proj_dir):
    """Utility function to create a mapping table for deidentification"""
    path = f"../SCRATCH"
    proj_name = "AUTOMIS"
    test_arr = []
    with open(f"{proj_dir}/TABLE.txt","w") as table:
        pass
    for root, dirs, files in os.walk(path):
        temp_arr = root.split("/")
        if len(temp_arr) == 5:
            table_id = f"{proj_name}_{temp_arr[3]},{temp_arr[4]}\n"
            with open(f"{proj_dir}/TABLE.txt","r") as f:
                read_file = f.readlines()
                if table_id not in read_file:
                    test_arr.append(table_id)

    with open(f"{proj_dir}/TABLE.txt","a") as f:
        for each in test_arr:
            f.write(each)
    
    print_with_color(f"{now} -- TABLE CREATION SUCCESS", color=GREEN)
    return test_arr

def dicom_deident(now,src_path, proj_path):
    """Utility function to deident sorted dirs"""
    # if not os.path.exists(f'{dest_path}'):
    print_with_color(f"{now} -- DICOM DEIDENT START", color=BLUE)
    subprocess.run(['python', './dicom-deident.py', '-t', f'{proj_path}TABLE.txt', '-s', f'{src_path}', '-d', f'{proj_path}DEIDENT', '-m', '2'])
    print_with_color(f"{now} -- DICOM DEIDENT SUCCESS -- {src_path}", color=GREEN)

def zip_upload(now, case_label, proj_dir):
    """Utility function to zip deident dirs"""
    case_id = case_label.split(',')[0]
    to_zip = f"{proj_dir}DEIDENT/{case_id}"
    subprocess.run(['zip','-rT','-9',f'../SCRATCH/{case_id}.zip',f'{to_zip}'])
    print_with_color(f"{now} -- ZIP SUCCESS -- {case_id}", color=GREEN)
    return case_id

def xnat_upload(now, case_id, proj_dir, server, x_user, x_pwd):
    """Utility function to upload zips to XNAT"""
    proj_name = "TP_MXBAT"
    print_with_color(f"{now} -- UPLOAD XNAT START -- {case_id}", color=BLUE)
    subprocess.run(['python', './xnat-upload.py', '-x', f'{server}', '-s', f'{proj_dir}SCRATCH/{case_id}.zip', '-u', f'{x_user}', '-p', f'{x_pwd}'])
    print_with_color(f"{now} -- UPLOAD XNAT SUCCESS -- {case_id}", color=GREEN)
    return case_id
    pass


def print_with_color(s, color=Fore.WHITE, brightness=Style.NORMAL, **kwargs):
    """Utility function wrapping the regular `print()` function 
    but with colors and brightness"""
    print(f"{brightness}{color}{s}{Style.RESET_ALL}", **kwargs)


# Class that inherits from FileSystemEventHandler for handling the events sent by the Observer
class LogHandler(FileSystemEventHandler):

    def __init__(self, watchPattern, exceptionPattern, doWatchDirectories, xnatServer, xnatUser, xnatPwd):
        self.watchPattern = watchPattern
        self.exceptionPattern = exceptionPattern
        self.doWatchDirectories = doWatchDirectories
        self.xnatServer = xnatServer
        self.xnatUser = xnatUser
        self.xnatPwd = xnatPwd
        # Instantiate the checker
        self.fc = FileChecker(self.exceptionPattern)

    def on_any_event(self, event):
        pass

    def on_modified(self, event):
        pass

    def on_deleted(self, event):
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"{now} -- {event.event_type} -- Folder: {event.src_path}"
        print_with_color(msg, color=event2color[event.event_type])

    def on_created(self, event):
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        # To Observe files only not directories
        if not event.is_directory:
            # To cater for the on_move event
            path = event.src_path
            if path.endswith(self.watchPattern):
                msg = f"{now} -- {event.event_type} -- File: {path}"
                print_with_color(msg, color=event2color[event.event_type])
                # Check if upload is complete
                check_upload(now, event.src_path)
                print_with_color(f"{now} -- UNZIP START", color=BLUE)
                subprocess.run(['unzip',f'{path}','-d',f'{path[:-4]}'])
                print_with_color(f"{now} -- UNZIP SUCCESS", color=GREEN)
                
        elif self.doWatchDirectories:
            msg = f"{now} -- {event.event_type} -- Folder: {event.src_path}"
            proj_dir = "/home/biren/XNAT/MBCTOOLS/mbcxnat-tools/AUTOMIS/"
            src_path = event.src_path
            dest_path = f"{proj_dir}SCRATCH/{src_path.split('/')[2]}/{src_path.split('/')[3]}"
            print_with_color(msg, color=event2color[event.event_type])
            
            if not os.path.exists(f'{dest_path}'):
                # Check if upload is complete
                check_upload(now, src_path)
                # Sort DICOM files
                dicom_sort(now, src_path, dest_path)
                # DEIDENT
                pro_table = create_table(now, proj_dir)
                #print(pro_table)
                #print(pro_table[-1])
                dicom_deident(now, dest_path, proj_dir)
                # XNAT 
                # zip first
                case_id = zip_upload(now,pro_table[-1],proj_dir)
                print(self.xnatServer, self.xnatUser, self.xnatPwd)
                xnat_upload(now, case_id, proj_dir, self.xnatServer, self.xnatUser, self.xnatPwd)

    def on_moved(self, event):
        pass


class LogWatcher:
    # Initialize the observer
    observer = None
    # Initialize the stop signal variable
    stop_signal = 0

    # The observer is the class that watches for any file system change and then dispatches the event to the event handler.
    def __init__(self, watchDirectory, watchDelay, watchRecursively, watchPattern, doWatchDirectories, exceptionPattern, xnatServer, xnatUser, xnatPwd):
        # Initialize variables in relation
        self.watchDirectory = watchDirectory
        self.watchDelay = watchDelay
        self.watchRecursively = watchRecursively
        self.watchPattern = watchPattern
        self.doWatchDirectories = doWatchDirectories
        self.exceptionPattern = exceptionPattern
        self.xnatServer = xnatServer
        self.xnatUser = xnatUser
        self.xnatPwd = xnatPwd

        # Create an instance of watchdog.observer
        self.observer = Observer()
        # The event handler is an object that will be notified when something happens to the file system.
        self.event_handler = LogHandler(
            watchPattern, exceptionPattern, self.doWatchDirectories, self.xnatServer, self.xnatUser, self.xnatPwd)

    def schedule(self):
        print("Observer Scheduled:", self.observer.name)
        # Call the schedule function via the Observer instance attaching the event
        self.observer.schedule(
            self.event_handler, self.watchDirectory, recursive=self.watchRecursively)

    def start(self):
        print("Observer Started:", self.observer.name)
        self.schedule()
        # Start the observer thread and wait for it to generate events
        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Started On: {now}"
        print(msg)

        msg = (
            f"Watching {'Recursively' if self.watchRecursively else 'Non-Recursively'}: {self.watchPattern}"
            f" -- Folder: {self.watchDirectory} -- Every: {self.watchDelay}(sec) -- For Patterns: {self.exceptionPattern}\n"
            f"XNAT: {self.xnatServer} -- User: {self.xnatUser}"
        )
        print(msg)
        self.observer.start()

    def run(self):
        print("Observer is running:", self.observer.name)
        self.start()
        try:
            while True:
                time.sleep(self.watchDelay)

                if self.stop_signal == 1:
                    print(
                        f"Observer stopped: {self.observer.name}  stop signal:{self.stop_signal}")
                    self.stop()
                    break
        except:
            self.stop()
        self.observer.join()

    def stop(self):
        print("Observer Stopped:", self.observer.name)

        now = (datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        msg = f"Observer: {self.observer.name} - Stopped On: {now}"
        print(msg)
        self.observer.stop()
        self.observer.join()

    def info(self):
        info = {
            'observerName': self.observer.name,
            'watchDirectory': self.watchDirectory,
            'watchDelay': self.watchDelay,
            'watchRecursively': self.watchRecursively,
            'watchPattern': self.watchPattern,
            'xnatServer': self.xnatServer,
            'xnatUser': self.xnatUser,
            'xnatPwd': self.xnatPwd
        }
        return info


def is_dir_path(path):
    """Utility function to check whether a path is an actual directory"""
    if os.path.isdir(path):
        return path
    else:
        raise NotADirectoryError(path)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        description="Watchdog script for watching for files & directories' changes")
    parser.add_argument("-s","--path",
                        help="Source path",
                        default=config.WATCH_DIRECTORY,
                        type=is_dir_path,
                        )
    parser.add_argument("-d", "--watch-delay",
                        help=f"Watch delay, default is {config.WATCH_DELAY}",
                        default=config.WATCH_DELAY,
                        type=int,
                        )
    parser.add_argument("-r", "--recursive",
                        action="store_true",
                        help=f"Whether to recursively watch for the path's children, default is {config.WATCH_RECURSIVELY}",
                        default=config.WATCH_RECURSIVELY,
                        )
    parser.add_argument("-p", "--pattern",
                        help=f"Pattern of files to watch, default is {config.WATCH_PATTERN}",
                        default=config.WATCH_PATTERN,
                        )
    parser.add_argument("--watch-directories",
                        action="store_true",
                        help=f"Whether to watch directories, default is {config.DO_WATCH_DIRECTORIES}",
                        default=config.DO_WATCH_DIRECTORIES,
                        )
    parser.add_argument("-x","--xnat-server",
                        help="Xnat instance server address",
                        default=config.XNAT_SERVER,
                        )
    parser.add_argument("-u","--xnat-user",
                        help="Xnat User",
                        default=config.XNAT_USER,
                        )
    parser.add_argument("-a","--xnat-pwd",
                        help="Xnat User password",
                        default=config.XNAT_PWD,
                        )

    # parse the arguments
    args = parser.parse_args()
    # define & launch the log watcher
    log_watcher = LogWatcher(
        watchDirectory=args.path,
        watchDelay=args.watch_delay,
        watchRecursively=args.recursive,
        watchPattern=tuple(args.pattern.split(",")),
        doWatchDirectories=args.watch_directories,
        exceptionPattern=config.EXCEPTION_PATTERN,
        xnatServer = args.xnat_server,
        xnatUser = args.xnat_user,
        xnatPwd = args.xnat_pwd
    )
    log_watcher.run()
