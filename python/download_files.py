import asyncio
import pandas as pd
import os.path
import glob

import download_files_core as downloader
import config_functions

def save_download_results(dataframe, results, filename_column, results_filename):
    results_df = pd.DataFrame(index = dataframe.index)
    results_df[filename_column] = dataframe[filename_column]
    results_df["pdf_downloaded"] = results
    try:
        results_df.to_excel(results_filename, index = False)
        return True
    except PermissionError:
        return False

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

async def do_downloads(config_file_name, output_f):

    # if the config file is invalid, we shouldn't execute the rest of the code!
    try:
        config = config_functions.parse_config(config_file_name)
    except Exception as e:
        output_f(e)
        return

    output_f("Reading URL sheet...")

    data = pd.read_excel(config["url_sheet_path"])
    #data = data[:100].copy()

    success, err_msg = config_functions.check_columns(data, config)
    if not success:
        output_f(err_msg)
        return

    output_f("URL sheet has been read. Starting downloads...")

    progress = progress_bar(len(data.index), output_f)
    results = await downloader.try_download_all(data, config, progress.add)
    progress.finish()

    output_f("All downloads are done. Saving results...")

    success = save_download_results(data, results, config["save_as"], config["result_sheet_path"])
    if success:
        output_f(f"Results saved in {config['result_sheet_path']}")
    else:
        output_f(f"Could not save download results in {config['result_sheet_path']}. This might be because you have the file open.")
    return

if __name__ == "__main__":
    asyncio.run(do_downloads("config.json", print))