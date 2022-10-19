import asyncio
import pandas as pd
import os.path
import glob
import sys

import download_files_core as downloader
import config_functions
import interface

def save_download_results(dataframe, results, filename_column, results_filename):
    results_df = pd.DataFrame(index = dataframe.index)
    results_df[filename_column] = dataframe[filename_column]
    results_df["pdf_downloaded"] = results
    try:
        results_df.to_excel(results_filename, index = False)
        return True
    except PermissionError:
        return False

def already_downloaded(download_path):
    files = glob.glob(os.path.join(download_path, "*.pdf")) 
    return set(os.path.basename(f)[:-4] for f in files)

def empty_folder (folderpath):
    for f in os.listdir(folderpath):
        os.remove(os.path.join(folderpath, f))

async def do_downloads(config_file_name, ui, options):
    # if the config file is invalid, we shouldn't execute the rest of the code!
    try:
        raw_config = config_functions.read_config(config_file_name)
        ui.raw_config = raw_config
        config = config_functions.parse_config(raw_config)
    except Exception as e:
        ui.communicate_error(str(e))
        return
    ui.raw_config = {}
    ui.config = config
    
    if options.from_empty:
        empty_folder(config["download_path"])

    ui.communicate_progress("start_read")

    data = pd.read_excel(config["url_sheet_path"])
    if options.only_first_hundred:
        data = data[:20].copy()
    ui.data = data

    success, err_msg = config_functions.check_columns(data, config)
    if not success:
        ui.communicate_error(err_msg)
        return

    ui.communicate_progress("end_read")

    if not options.skip_downloads:
        ui.communicate_progress("start_download")
        results = await downloader.try_download_all(data, config, ui.progress_bar.add)
        ui.communicate_progress("end_download")
    else:
        files = already_downloaded(config["download_path"])
        results = [(filename in files) for filename in data[config["save_as"]]]

    ui.communicate_progress("start_save")

    success = save_download_results(data, results, config["save_as"], config["result_sheet_path"])
    if success:
        ui.communicate_progress("end_save")
    else:
        ui.communicate_error("save_failed")
    ui.finish()

class flags:
    def __init__(self):
        self.skip_downloads = "--no-download" in sys.argv
        self.has_timer = "--timer" in sys.argv
        self.from_empty = "--from-empty" in sys.argv
        self.only_first_hundred = "--first-hundred" in sys.argv

if __name__ == "__main__":
    flags = flags()
    ui = interface.messages(has_timer = flags.has_timer)
    asyncio.run(do_downloads("config.json", ui, flags))
