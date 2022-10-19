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
    error_msg = {
        "config_not_found" : "Cannot find a file named config.json",
        "config_invalid" : "Your config file is not a valid json file. Did you delete a comma?",
        "config_incomplete" : "Your config file is missing one of the required settings. Did you delete a line? Or change a setting name?",
        "sheets_location_not_found" : "You wrote {sheets_location} in sheets_location, but that doesn't seem to be a folder that exists.",
        "url_sheet_not_found" : "You wrote {name_of_sheet_with_urls} in name_of_sheet_with_urls, but that's not the name of a file that exists in {sheets_location}.",
        "not_list" : "You wrote {columns_to_check} in columns_to_check, but columns_to_check needs to be a list (wrapped in square brackets [])",
        "not_positive_int" : "You wrote {timeout} in timeout, but that's not a positive whole number.",
        "id_column_not_found" : "You wrote {save_as} in id_column_name, but that's not the title of a column that exists in the URL sheet.",
        "check_column_not_found" : "You wrote {columns_to_check} in columns_to_check, but one of those is not the title of a column that exists in the URL sheet.",
        "save_failed" : "Could not save download results in {result_sheet_path}. This might be because you have the file open."
    }
    def __init__(self, has_timer = False):
        self.timer = stopwatch() if has_timer else None
        self.data_length = 0
        self._config = None
    def output(self, msg, **kwargs):
        formatted = msg.format(**kwargs)
        print(formatted)
    def communicate_error(self, msg):
        if self._config == None:
            # the way the code is currently set up, this case will never happen, but better be prepared for future code changes
            self.output(self.error_msg[msg])
        else:
            self.output(self.error_msg[msg], **self._config.all_attrs())
    def communicate_progress (self, msg):
        if msg == "end_download":
            self.progress_bar.finish()

        self.output(self.progress_msg[msg], **self._config.all_attrs())

        if msg == "start_download":
            self.progress_bar = progress_bar(self.data_length, print)
        if msg[:4] == "end_" and self.timer != None:
            self.timer.step()
    def finish(self):
        if self.timer != None:
            self.timer.finish()
    def attach_config(self, config):
        self._config = config


