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
    files = glob.glob(os.path.join(config["download_path"], "*.pdf")) 
    return set(os.path.basename(f)[:-4] for f in files)

async def do_downloads(config_file_name, output_f):
    # read flags
    skip_downloads = "--no-download" in sys.argv
    has_timer = "--timer" in sys.argv
    from_empty = "--from-empty" in sys.argv
    only_first_hundred = "--first-hundred" in sys.argv

    ui = interface.messages(output_f, has_timer = has_timer)
    # if the config file is invalid, we shouldn't execute the rest of the code!
    try:
        config = config_functions.parse_config(config_file_name)
    except Exception as e:
        output_f(e)
        return
    ui.config = config

    if from_empty:
        empty_folder(config["download_path"])

    ui.communicate_progress("start_read")

    data = pd.read_excel(config["url_sheet_path"])
    if only_first_hundred:
        data = data[:100].copy()
    ui.data = data

    success, err_msg = config_functions.check_columns(data, config)
    if not success:
        output_f(err_msg)
        return

    ui.communicate_progress("end_read")

    if not skip_downloads:
        ui.communicate_progress("start_download")
        results = await downloader.try_download_all(data, config, ui.progress_bar.add)
        ui.communicate_progress("end_download")
    else:
        files = already_downlaoded(config["download_path"])
        results = [(filename in files) for filename in data[config["save_as"]]]

    ui.communicate_progress("start_save")

    success = save_download_results(data, results, config["save_as"], config["result_sheet_path"])
    if success:
        ui.communicate_progress("end_save")
    else:
        output_f(f"Could not save download results in {config['result_sheet_path']}. This might be because you have the file open.")
    ui.finish()

if __name__ == "__main__":
    asyncio.run(do_downloads("config.json", print))
