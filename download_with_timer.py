import asyncio
import time
import download_files
import test
import sys

class stopwatch:
    def __init__(self):
        self.last = self.start = time.time()
    def step(self, msg):
        now = time.time()
        print(f"{msg:50} Time on this step: {now - self.last} seconds")
        self.last = now
    def finish(self):
        print(f"{'':50} Total time: {time.time() - self.start} seconds.")

async def do_downloads_with_timer ():
    if "--from-empty" in sys.argv:
        test.empty_folder(download_files.parse_config("config.json")["download_path"])
    timer = stopwatch()
    await download_files.do_downloads("config.json", timer.step)
    timer.finish()

asyncio.run(do_downloads_with_timer())