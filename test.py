import asyncio
import os
import time

import download_files
import test_dummies
import aiohttp.test_utils

def test_parse_config ():
    # I cannot be bothered to test all the myriad ways a config file can be broken
    # So I'm just picking one of the ways, and that'll have to do.
    error = None
    try:
        download_files.parse_config("test/broken-config.json")
    except Exception as e:
        error = e
    assert error != None

    config = download_files.parse_config("test/working-config.json")
    expected = {
        "download_path" : "test/downloads",
        "url_sheet_path" : "test/sheets/urls.xlsx",
        "result_sheet_path" : "test/sheets/output.xlsx",
        "save_as" : "filename",
        "columns_to_check" : ["url1", "url2"],
        "timeout" : 30
    }
    path_keys = [key for key in expected if key[-5:] == "_path"]
    other_keys = [key for key in expected if key not in path_keys]
    # we don't care whether the paths are the same character-for-character, 
    # only whether they resolve to the same path
    for key in path_keys:
        assert os.path.samefile(config[key], expected[key])

    for key in other_keys:
        assert config[key] == expected[key]

def test_check_columns():
    data = download_files.pd.DataFrame(data={'col1' : [1,2], 'col2' : [3,4]})

    failing_config = {"save_as" : "col1", "columns_to_check" : ["nonexistant column name"]}
    success, _ = download_files.check_columns(data, failing_config)
    assert not success

    passing_config = {"save_as" : "col1", "columns_to_check" : ["col2"]}
    success, _ = download_files.check_columns(data, passing_config)
    assert success


async def test_download_file():
    server = await test_dummies.make_server()
    async with aiohttp.test_utils.TestClient(server) as session:
        expected = {"/works" : True, "/doesnt-exist" : False, "/not-pdf" : False}
        for key in expected:
            try:
                download_location = "test/downloads/something.pdf"
                await download_files.download_file(session, key, download_location, 5)
                success = os.path.exists(download_location)
            except Exception as e:
                success = False
            assert success == expected[key]

async def test_try_multiple_download():
    data = download_files.pd.DataFrame(data={
        'col1' : ["/works","/doesnt-exist", "/not-pdf"], 
        'col2' : ["","/works", ""],
        'name' : ["test1", "test2", "test3"]
        })
    expected = [True, True, False]
    config = {"save_as" : "name", "download_path" : "test/downloads", "columns_to_check" : ["col1", "col2"]}
    server = await test_dummies.make_server()
    def aggregator (thing):
        pass
    async with aiohttp.test_utils.TestClient(server) as session:
        for i in data.index:
            success = await download_files.try_multiple_columns_download_file(session, data, i, config, aggregator)
            print(i, success)

def empty_folder (folderpath):
    for f in os.listdir(folderpath):
        os.remove(os.path.join(folderpath, f))

async def test_full ():

    # empty downloads folder
    download_folder = os.path.join("test", "downloads")
    empty_folder(download_folder)

    await download_files.do_downloads("test/working-config.json", test_dummies.dont_print)

    assert os.listdir(download_folder) == ["working-pdf-1.pdf", "working-pdf-2.pdf"]

    # next let's try to run it on a non-empty downloads folder
    await download_files.do_downloads("test/working-config.json", test_dummies.dont_print)

    assert os.listdir(download_folder) == ["working-pdf-1.pdf", "working-pdf-2.pdf"]

async def run_all_tests ():
    test_parse_config()
    test_check_columns()
    await test_download_file()
    await test_try_multiple_download()
    await test_full()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
