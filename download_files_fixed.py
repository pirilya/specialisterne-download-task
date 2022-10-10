# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 15:37:08 2019

@author: hewi
"""

#### IF error : "ModuleNotFOundError: no module named PyPDF2"
   # then uncomment line below (i.e. remove the #):
       
#pip install PyPDF2

import pandas as pd
import PyPDF2
import os.path
import urllib
import urllib.request
import urllib.error
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

'''
### loop through dataset, try to download file.
for j in df2.index:
    savefile = os.path.join(pth + str(j) + '.pdf')
    try:
        urllib.request.urlretrieve(df2.at[j,'Pdf_URL'], savefile)
        #if os.path.isfile(savefile):
            #try:
                #pdfFileObj = open(savefile, 'rb')
               # creating a pdf reader object
                #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                #with open(savefile, 'rb') as pdfFileObj:
                    #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                    #if pdfReader.numPages > 0:
                        #df2.at[j, 'pdf_downloaded'] = "yes"
                    #else:
                        #df2.at[j, 'pdf_downloaded'] = "file_error"
               
            #except Exception as e:
               # df2.at[j, 'pdf_downloaded'] = str(e)
                #print(str(str(j)+" " + str(e)))
        #else:
            #df2.at[j, 'pdf_downloaded'] = "404"
            #print("not a file")
            
    except (urllib.error.HTTPError, urllib.error.URLError, ConnectionResetError, Exception ) as e:
        print(e)
        df2.at[j,"error"] = str(e)
'''
    


#df2.to_excel(writer, sheet_name="dwn")
#writer.save()
#writer.close()

def read_data(filepath, sheetname, index_col_name):
    df = pd.read_excel(list_pth, sheet_name = sheetname, index_col = index_col_name)
    print("dataframe read")

    ### filter out rows with no URL
    non_empty = df.Pdf_URL.notnull() == True
    return df[non_empty].copy()
    
def filter_already_downloaded(dataframe, download_location):
    ### check for files already downloaded
    dwn_files = glob.glob(os.path.join(download_location, "*.pdf")) 
    exist = [os.path.basename(f)[:-4] for f in dwn_files]
    ### filter out rows that have been downloaded
    return dataframe[~dataframe.index.isin(exist)]

# returns true if the download succeeded and false if it didn't
async def try_download_file(url, download_location):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, ssl=False) as response: # putting the ssl checker in relaxed mode should be fine, right?
                if response.status == 200: # status code 200 means everything went well
                    print("success for", download_location)
                    content = await asyncio.wait_for( response.read(), 30)
                    print("successfully read", download_location)
                    with open(download_location, "wb") as f:
                        f.write(content)
                    return True
        except (aiohttp.InvalidURL, aiohttp.client_exceptions.ClientConnectorError) as e:
            print(e)
    return False

# returns true if the download succeeded and false if it didn't
async def try_multiple_columns_download_file(dataframe, line_id):
    download_path = os.path.join(pth + str(line_id) + '.pdf')
    urls_to_try = [ dataframe.at[line_id,'Pdf_URL'], dataframe.at[line_id,'Report Html Address'] ]
    for url in urls_to_try:
        if (type(url) == str): # pandas reads empty cells as floats, we gotta check for that or the script gets confused
            success = await try_download_file(url, download_path)
            if success:
                return True
    return False

async def try_download_all(dataframe):
    function_calls =  [try_multiple_columns_download_file(dataframe, j) for j in dataframe.index]
    await asyncio.wait_for( asyncio.gather(*function_calls), timeout=60)

# for debugging -- some of the lines cause issues and i want to isolate which!
async def try_download_all_synchronous(dataframe):
    for j in dataframe.index:
        print(j)
        await try_multiple_columns_download_file(dataframe, j)


data = read_data(list_pth, 0, "BRnum")

data = data[25:30].copy()

#data = filter_already_downloaded(data, dwn_pth)

asyncio.run(try_download_all(data))
'''
py download_files_fixed.py
'''