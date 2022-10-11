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

###!!NB!! column with URL's should be called: "Pdf_URL" and the year should be in column named: "Pub_Year"

### File names will be the ID from the ID column (e.g. BR2005.pdf)

########## EDIT HERE:
    
### specify path to file containing the URLs
list_pth = 'sheets/GRI_2017_2020 (1).xlsx'

###specify Output folder (in this case it moves one folder up and saves in the script output folder)
pth = 'downloads/'

###Specify path for existing downloads
dwn_pth = 'downloads/'

###specify the ID column name
ID = "BRnum"


#writer = pd.ExcelWriter(pth+'check_3.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})

#df2.to_excel(writer, sheet_name="dwn")
#writer.save()
#writer.close()

def already_downloaded_ids(download_location):
    files = glob.glob(os.path.join(download_location, "*.pdf")) 
    return [os.path.basename(f)[:-4] for f in files]

def read_data(filepath, sheetname, index_col_name):
    df = pd.read_excel(list_pth, sheet_name = sheetname, index_col = index_col_name)
    return df
    
def filter_already_downloaded(dataframe, download_location):
    exist = already_downloaded_ids(download_location)
    return dataframe[~dataframe.index.isin(exist)]

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

# returns true if the download succeeded and false if it didn't
async def try_multiple_columns_download_file(session, dataframe, line_id):
    download_path = os.path.join(pth + str(line_id) + '.pdf')
    urls_to_try = [ dataframe.at[line_id,'Pdf_URL'], dataframe.at[line_id,'Report Html Address'] ]
    for url in urls_to_try:
        if (type(url) == str): # pandas reads empty cells as floats, we gotta check for that or the script gets confused
            try:
                await download_file(session, url, download_path)
                return True
            except Exception as e:
                pass
                #print("Error of type:", type(e), "Error content:", e)
    return False

async def try_download_all(dataframe, headers):
    async with aiohttp.ClientSession( headers = headers ) as session:
        function_calls = [try_multiple_columns_download_file(session, dataframe, j) for j in dataframe.index]
        await asyncio.gather(*function_calls)

data = read_data(list_pth, 0, "BRnum")
print("dataframe loaded")

# data = data[:50].copy()

data = filter_already_downloaded(data, dwn_pth)

# setting the same user-agent that my actual browser has, so we don't get caught by bot detection
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}

asyncio.run(try_download_all(data, headers))
'''
py download_files_fixed.py
'''