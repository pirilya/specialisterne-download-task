import pandas as pd
import os.path
import glob

import asyncio
import aiohttp

import json

def parse_config(filepath):
    try:
        with open(filepath, "r") as f:
            raw_config = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Cannot find a file named {filepath}")
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"Your config file is not a valid json file. (This is what the computer thinks is the issue: {e})")
    config = {}
    for config_entry_name in ["downloads_location", 
                                "sheets_location", 
                                "name_of_sheet_with_urls",
                                "name_of_sheet_with_results",
                                "filename_column",
                                "columns_to_check",
                                "timeout"]:
        if config_entry_name not in raw_config:
            raise Exception(f"Your config file is missing {config_entry_name}")
    config["download_path"] = raw_config["downloads_location"]
    config["save_as"] = raw_config["filename_column"]
    config["columns_to_check"] = raw_config["columns_to_check"]
    if type(config["columns_to_check"]) != list:
        raise Exception(f"You wrote {config['columns_to_check']} in columns_to_check, but columns_to_check needs to be a list (wrapped in square brackets [])")
    try:
        config["timeout"] = int(raw_config["timeout"])
        if config["timeout"] <= 0:
            raise ValueError
    except ValueError as e:
        raise Exception(f"You wrote {raw_config['timeout']} in timeout, but that's not a positive whole number.")
    if os.path.isdir(raw_config["sheets_location"]):
        config["url_sheet_path"] = os.path.join(raw_config["sheets_location"], raw_config["name_of_sheet_with_urls"])
        config["result_sheet_path"] = os.path.join(raw_config["sheets_location"], raw_config["name_of_sheet_with_results"])
    else:
        raise Exception(f"You wrote {raw_config['sheets_location']} in sheets_location, but that doesn't seem to be a folder that exists.")
    for pathname in ["url_sheet_path", "result_sheet_path"]:
        if os.path.splitext(config[pathname])[1] == "":
            config[pathname] += ".xlsx"
    if not os.path.exists(config["url_sheet_path"]):
        raise Exception(f"You wrote {raw_config['name_of_sheet_with_urls']} in name_of_sheet_with_urls, but that's not the name of a file that exists in {raw_config['sheets_location']}")
    if not os.path.isdir(config["download_path"]):
        os.makedirs(config["download_path"])
    return config


def check_columns(df, config):
    if not config["save_as"] in df.columns:
        return False, f"You wrote {config['save_as']} in id_column_name, but that's not the title of a column that exists in the URL sheet."
    for column_name in config["columns_to_check"]:
        if not column_name in df.columns:
            return False, f"You wrote {column_name} in columns_to_check, but that's not the title of a column that exists in the URL sheet."
    return True, None


# returns void if the download succeeded, throws some kind of error if it didn't
async def download_file(session, url, download_location, timeout):
    # turning off ssl checking is maybe risky but some of the URLs don't work if we have it turned on...
    async with session.get(url, ssl=False, timeout = timeout) as response:
        if response.ok and response.content_type in ["application/pdf", "application/octet-stream"]:
                content = await asyncio.wait_for( response.read(), timeout)
                if content[:5] == "%PDF-":
                    with open(download_location, "wb") as f:
                        f.write(content)
                    return
    # the control flow is simpler if we're guaranteed to always throw an exception if the download fails
    raise Exception("Download failed")


# returns true if, after execution, the file is downloaded, and false if it isn't
async def try_multiple_columns_download_file(session, dataframe, line_id, config):
    filename = dataframe.at[line_id, config["save_as"]]
    download_path = os.path.join(config["download_path"], filename + '.pdf')
    if os.path.exists(download_path):
        return True
    urls_to_try = [ dataframe.at[line_id, column_name] for column_name in config["columns_to_check"] ]
    for url in urls_to_try:
        if (type(url) == str): # pandas reads empty cells as floats, we gotta check for that or the script gets confused
            try:
                await download_file(session, url, download_path, config["timeout"])
                return True
            except Exception as e:
                pass
                #print("Error of type:", type(e), "Error content:", e)
    return False


async def try_download_all(dataframe, config):
    # setting the same user-agent that my actual browser has, so we don't get caught by bot detection
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    
    async with aiohttp.ClientSession( headers = headers ) as session:
        function_calls = [try_multiple_columns_download_file(session, dataframe, j, config) for j in dataframe.index]
        return await asyncio.gather(*function_calls)


def save_download_results(dataframe, results, filename_column, results_filename):
    results_df = pd.DataFrame(index = dataframe.index)
    results_df[filename_column] = dataframe[filename_column]
    results_df["pdf_downloaded"] = results
    try:
        results_df.to_excel(results_filename, index = False)
        return True
    except PermissionError:
        return False


async def do_downloads(config_file_name, output_f):

    # if the config file is invalid, we shouldn't execute the rest of the code!
    try:
        config = parse_config(config_file_name)
    except Exception as e:
        output_f(e)
        return

    output_f("Reading URL sheet...")

    data = pd.read_excel(config["url_sheet_path"])

    success, err_msg = check_columns(data, config)
    if not success:
        output_f(err_msg)
        return

    output_f("URL sheet has been read. Starting downloads...")

    results = await try_download_all(data, config)

    output_f("All downloads are done. Saving results...")

    success = save_download_results(data, results, config["save_as"], config["result_sheet_path"])
    if success:
        output_f(f"Results saved in {config['result_sheet_path']}")
    else:
        output_f(f"Could not save download results in {config['result_sheet_path']}. This might be because you have the file open.")
    return

if __name__ == "__main__":
    asyncio.run(do_downloads("config.json", print))