# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:37:08 2019

@author: hewi
"""

import pandas as pd
import os.path
import glob

import asyncio
import aiohttp

import json


def read_data(path, id_column_name):
    df = pd.read_excel(path,  index_col = id_column_name)
    return df

def parse_config(filepath):
    try:
        with open(filepath, "r") as f:
            raw_config = json.load(f)
    except FileNotFoundError:
        raise Exception(f"Kan ikke finde en fil ved navn {filepath}")
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"Din config-fil er misdannet. ({e})")
    config = {}
    for config_entry_name in ["downloads_location", 
                                "sheets_location", 
                                "name_of_sheet_with_urls",
                                "name_of_sheet_with_results",
                                "id_column_name",
                                "columns_to_check",
                                "timeout"]:
        if config_entry_name not in raw_config:
            raise Exception(f"Din config-fil mangler {config_entry_name}")
    config["download_path"] = raw_config["downloads_location"]
    config["id_column_name"] = raw_config["id_column_name"]
    config["columns_to_check"] = raw_config["columns_to_check"]
    if raw_config["timeout"].isnumeric():
        config["timeout"] = int(raw_config["timeout"])
    else:
        raise Exception(f"Du skrev {raw_config['timeout']} i timeout, men det er ikke et positivt helt tal.")
    if os.path.isdir(raw_config["sheets_location"]):
        config["url_sheet_path"] = os.path.join(raw_config["sheets_location"], raw_config["name_of_sheet_with_urls"])
        config["result_sheet_path"] = os.path.join(raw_config["sheets_location"], raw_config["name_of_sheet_with_results"])
    else:
        raise Exception(f"Du skrev {raw_config['sheets_location']} i sheets_location, men det er ikke navnet på en mappe jeg kan finde.")
    for pathname in ["url_sheet_path", "result_sheet_path"]:
        if os.path.splitext(config[pathname])[1] == "":
            config[pathname] += ".xlsx"
    if not os.path.exists(config["url_sheet_path"]):
        raise Exception(f"Du skrev {raw_config['name_of_sheet_with_urls']} i name_of_sheet_with_urls, men det er ikke navnet på en fil som findes i {raw_config['sheets_location']}")
    if not os.path.isdir(config["download_path"]):
        os.makedirs(config["download_path"])
    return config

# returns void if the download succeeded, throws some kind of error if it didn't
async def download_file(session, url, download_location):
    # turning off ssl checking is maybe risky but some of the URLs don't work if we have it turned on...
    async with session.request("get", url, ssl=False, timeout = 30) as response: 
        # in production the timeout should probably be more than 30 seconds but in testing i'm impatient
        if response.ok and response.content_type in ["application/pdf", "application/octet-stream"]:
                content = await asyncio.wait_for( response.read(), 30)
                with open(download_location, "wb") as f:
                    f.write(content)
                return
    # the control flow is simpler if we're guaranteed to always throw an exception if the download fails
    raise Exception("Download failed")


# returns true if, after execution, the file is downloaded, and false if it isn't
async def try_multiple_columns_download_file(session, dataframe, line_id, config):
    download_path = os.path.join(config["download_path"], str(line_id) + '.pdf')
    if os.path.exists(download_path):
        return True
    urls_to_try = [ dataframe.at[line_id, column_name] for column_name in config["columns_to_check"] ]
    for url in urls_to_try:
        if (type(url) == str): # pandas reads empty cells as floats, we gotta check for that or the script gets confused
            try:
                await download_file(session, url, download_path)
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


async def do_downloads():

    # if the config file is invalid, we shouldn't execute the rest of the code!
    try:
        config = parse_config("config.json")
    except Exception as e:
        print(e)
        return

    try:
        data = read_data(config["url_sheet_path"], config["id_column_name"])
    except ValueError:
        print(f"Du skrev {config['id_column_name']} i id_column_name, men det er ikke en kolonne som eksisterer på URL-arket.")
        return
    for column_name in config["columns_to_check"]:
        if not column_name in data.columns:
            print(f"Du skrev {column_name} i columns_to_check, men det er ikke en kolonne som eksisterer på URL-arket.")
            return

    print("URL-arket er indlæst")

    # this line is of course just here for testing, so it doesn't take forever to run
    data = data[:10].copy()

    results = await try_download_all(data, config)

    print("Alle downloads er færdige")

    results_df = pd.DataFrame(index = data.index)
    results_df["pdf_downloaded"] = results
    try:
        results_df.to_excel(config["result_sheet_path"])
        print(f"Resultaterne er gemt i {config['result_sheet_path']}")
    except PermissionError:
        print(f"Kunne ikke gemme download-resultater på {config['result_sheet_path']}. Det kan være fordi du har filen åben.")

    
asyncio.run(do_downloads())
'''
py download_files_fixed.py
'''