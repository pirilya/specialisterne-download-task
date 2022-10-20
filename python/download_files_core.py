import asyncio
import aiohttp
import os.path

# If we don't have these two lines, the command line 
# prints an error message when a site sends malformed cookies
import logging
logging.getLogger("aiohttp").setLevel("ERROR")

# returns void if the download succeeded, throws some kind of error if it didn't
async def download_file(session, url, download_location, timeout):
    # turning off ssl checking is maybe risky but some of the URLs don't work if we have it turned on...
    async with session.get(url, ssl=False) as response:
        if response.ok and response.content_type in ["application/pdf", "application/octet-stream"]:
            content = await asyncio.wait_for( response.read(), timeout )
            if content[:5] == b"%PDF-":
                with open(download_location, "wb") as f:
                    f.write(content)
                return
    # the control flow is simpler if we're guaranteed to always throw an exception if the download fails
    raise Exception("Download failed")


# returns true if, after execution, the file is downloaded, and false if it isn't
async def try_multiple_columns_download_file(session, dataframe, line_id, config, aggregator):
    filename = dataframe.at[line_id, config.save_as]
    download_path = os.path.join(config.download_path, filename + '.pdf')
    if os.path.exists(download_path):
        aggregator(True)
        return True
    urls_to_try = [ dataframe.at[line_id, column_name] for column_name in config.columns_to_check ]
    for url in urls_to_try:
        if (type(url) == str): # pandas reads empty cells as floats, we gotta check for that or the script gets confused
            try:
                await download_file(session, url, download_path, config.timeout)
                aggregator(True)
                return True
            except Exception as e:
                pass
                #print("Error of type:", type(e), "Error content:", e)
    aggregator(False)
    return False


def try_download_all(dataframe, config, output_f):
    # setting the same user-agent that my actual browser has, so we don't get caught by bot detection
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0"}
    
    timeout = aiohttp.ClientTimeout(total=None, sock_connect=config.timeout, sock_read=config.timeout)
    async def inner():
        # this is kind of a clunky way to do things 
        # but having to unpack the "async with" to synchronous calls would also be clunky!
        async with aiohttp.ClientSession( headers = headers, timeout = timeout ) as session:
            function_calls = [try_multiple_columns_download_file(session, dataframe, j, config, output_f) for j in dataframe.index]
            return await asyncio.gather(*function_calls)
    return asyncio.run(inner())