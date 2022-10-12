# PDF downloader

This script will download pdf reports from links in a spreadsheet, and report the results back in a different spreadsheet, according to the settings the user has specified in the file `config.json`.

# Running the script

This is a Python script, so in order to run it you need to have Python installed. Python is automatically installed on Mac computers but not on Windows. [You can download Python here.](https://www.python.org/downloads/)

## 1. Download `download_files.py` and `config.json`

You can find them right here on this page on github.com by scrolling up a bit, or you can download them from these links: <a href="https://raw.githubusercontent.com/pirilya/specialisterne-download-task/main/download_files.py" download>`download_files.py`</a> <a href="https://raw.githubusercontent.com/pirilya/specialisterne-download-task/main/config.json" download>`config.json`</a>

## 2. Open a terminal / command line. 

On Windows:

1. Press Windows Key + X
2. Choose "Windows PowerShell" (may instead be called "Command Prompt" on some systems)

[maybe insert screenshot of this]

On Apple (note: I don't have an Apple computer myself so I just copied these instructions from someone else):

1. Click the launchpad icon in the dock
2. Type "terminal" in the search field
3. Double-click Terminal

## 3. Tell the terminal what folder to run in.

1. Copy the address of the folder that you put `download_files.py` and `config.json` in, back in step 1.
2. In the terminal, type "cd" and then paste the address of the folder

[insert screenshot of this]

## 4. Run the script

In the terminal, type `python download_files.py` and press Enter.

[note to self: either explain `pip install`, or set up a venv and explain that]

## 5. Error messages

If you get an error that says something like `The term "python" is not recognized`, that means you don't have python installed. Go back to step 0 and install python.

If you get an error that says `ModuleNotFoundError: No module named '{module name}'`, like for example `ModuleNotFoundError: No module named 'aiohttp'`, then you need to type `pip install aiohttp` into the terminal and press Enter. Then try to run the script again.

All other error messages will be explained in a later section.

# The config file

In the same folder as `download_files.py`, you have a file named `config.json`. This file contains all your options and configuration. To change things about how the script runs, you change the config file. (If you don't know how to open a .json file, Notepad works fine.)

The file should look something like this:
```json
{
    "downloads_location" : "downloads/",
    "sheets_location" : "sheets/",
    "name_of_sheet_with_urls" : "GRI_2017_2020 (1).xlsx",
    "name_of_sheet_with_results" : "Results_2017_2020.xlsx",
    "id_column_name" : "BRnum",
    "columns_to_check" : ["Pdf_URL", "Report Html Address"],
    "timeout" : "30"
}
```
The part to the left of the : is what the setting is called. Do not change this!

The part to the right of the : is what that setting is currently set to. You can change these to whatever you want.

I will now explain what each setting does.

## downloads_location

This setting tells the program what folder to put the downloaded PDFs in. It can be an absolute path, such as "C:\Users\KOM\Documents\download-task\downloads" (Windows) or "/Users/KOM/Documents/download-task/downloads" (Mac), or a relative path, such as "downloads".

## sheets_location

This setting tells the program what folder to look for the spreadsheets in. It can be an absolute path, such as "C:\Users\KOM\Documents\download-task\sheets" (Windows) or "/Users/KOM/Documents/download-task/sheets" (Mac), or a relative path, such as "sheets".

## name_of_sheet_with_urls

The name of the spreadsheet that has the URLs you want to download. 

You can write it with or without the `.xlsx`, up to you, either works.

## name_of_sheet_with_results

The name of the spreadsheet you want to put the results in.  

IF YOU PUT THE NAME OF AN EXISTING SPREADSHEET, THAT SPREADSHEET WILL GET OVERWRITTEN!

You can write it with or without the `.xlsx`, up to you, either works.

## id_column_name

The title of the column in the URLs spreadsheet that has the ID of the file.

## columns_to_check

The titles of the columns in the URLs spreadsheet that has the links you want to try downloading from.
For each line in the spreadsheet, the program will try these columns in the order you put them.

## timeout

Sometimes a file takes a long time to download. This setting tells the program how many seconds it should wait for a download before giving up on it.

If you set this to a high number, the program will probably take a longer time to run.

# Error messages

I've tried to make sure that if something goes wrong, the program writes you a reasonably understandable error message that tells you what the something is.

If you get an error message that is many lines long, and has bits of code in it, that's not one of mine, and it means things went wrong in a way I didn't predict was possible. I suggest you try running the program again, and if the issue keeps happening, download a fresh copy of config.json and start over on editing it to have the settings you want.