import time

class stopwatch:
    def __init__(self):
        self.last = self.start = time.time()
    def step(self):
        now = time.time()
        print(f"{'':50} Time on this step: {now - self.last} seconds")
        self.last = now
    def finish(self):
        print(f"{'':50} Total time: {time.time() - self.start} seconds.")

class progress_bar:
    def __init__(self, total, output_f):
        self.total = total
        self.finished = self.successes = self.fails = 0
        self.output_f = output_f
    def __print_self(self, delete):
        endchar = "\r" if delete else "\n"
        self.output_f(f"{self.finished:>10} / {self.total} ({self.successes} successes, {self.fails} failures)", end=endchar)
    def add(self, is_success):
        if is_success:
            self.successes += 1
        else:
            self.fails += 1
        self.finished += 1
        self.__print_self(True)
    def finish(self):
        self.__print_self(False)

class messages:
    progress_msg = {
        "start_read" : "Reading URL sheet...",
        "end_read" : "URL sheet has been read.",
        "start_download" : "Starting downloads...",
        "end_download" : "All downloads are done.",
        "start_save" : "Saving results...",
        "end_save" : "Results saved in {result_sheet_path}"
    }
    def __init__(self, output_f, has_timer = False):
        self.output_f = output_f
        self.timer = stopwatch() if has_timer else None
    def output(self, msg, **kwargs):
        formatted = msg.format(**kwargs)
        self.output_f(formatted)
    def communicate_progress (self, msg):
        if msg == "end_download":
            self.progress_bar.finish()

        if msg == "end_save":
            self.output(self.progress_msg[msg], result_sheet_path = self.config["result_sheet_path"])
        else:
            self.output(self.progress_msg[msg])

        if msg == "start_download":
            self.progress_bar = progress_bar(len(self.data.index), self.output_f)
        if msg[:4] == "end_" and self.timer != None:
            self.timer.step()
    def finish(self):
        if self.timer != None:
            self.timer.finish()


