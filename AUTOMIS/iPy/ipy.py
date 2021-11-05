import pyinotify
import asyncio


def handle_read_callback(notifier):
    """
    Just stop receiving IO read events after the first
    iteration (unrealistic example).
    """
    print(notifier)
    # notifier.loop.stop()


wm = pyinotify.WatchManager()
loop = asyncio.get_event_loop()
notifier = pyinotify.AsyncioNotifier(wm, loop,
                                     callback=handle_read_callback)
wm.add_watch('../TEST1', pyinotify.IN_CREATE)
loop.run_forever()
notifier.stop()
