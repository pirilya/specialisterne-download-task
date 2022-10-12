# Summary

This script will download pdf reports from links in a spreadsheet, and report the results back in a different spreadsheet, according to the settings the user has specified in the file `config.json`.

# Running the script

## 0. Make sure you have Python installed

This is a Python script, so in order to run it you need to have Python installed. Python is automatically installed on Mac computers but not on Windows. [You can download Python here.](https://www.python.org/downloads/)

If you're on Windows and want to know whether you have Python installed, you can go to Settings -> Apps -> Apps & Features to see a list of all programs installed on your computer. If Python is on that list, you have Python installed.

## 1. Download `download_files.py` and `config.json`

You can find them right here on this page on github.com by scrolling up a bit, or you can download them from these links: [`download_files.py`](https://raw.githubusercontent.com/pirilya/specialisterne-download-task/main/download_files.py") [`config.json`](https://raw.githubusercontent.com/pirilya/specialisterne-download-task/main/config.json") (follow the link, right click, Save page as...)

Make sure to put them in the same folder!

## 2. Edit config.json

The file config.json is where all your settings are, so if you want to change those, you need to edit config.json. The explanation of how to do this is in the section called [The config file](#the-config-file).

## 3. Open a terminal / command line. 

On Windows:

1. Press Windows Key + X
2. Choose "Windows PowerShell" (may instead be called "Command Prompt" on some systems)

[maybe insert screenshot of this]

On Apple (note: I don't have an Apple computer myself so I just copied these instructions from someone else):

1. Click the launchpad icon in the dock
2. Type "terminal" in the search field
3. Double-click Terminal

## 4. Tell the terminal what folder to run in.

1. Copy the address of the folder that you put `download_files.py` and `config.json` in, back in step 1.
2. In the terminal, type "cd" and then paste the address of the folder

[insert screenshot of this]

## 5. Install libraries

In the terminal, type `pip install -r requirements.txt` and press Enter.

(If you know what a venv is, you might want to do this inside of one. But if you don't, don't worry about it.)

## 6. Run the script

In the terminal, type `python download_files.py` and press Enter.

## 6.5. Error messages

If you get an error that says something like `The term "python" is not recognized`, that means you don't have python installed. Go back to step 0 and install python.

If you get an error that says `ModuleNotFoundError: No module named '{module name}'`, that means you're missing a library. Did you skip step 5?

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
    "filename_column" : "BRnum",
    "columns_to_check" : ["Pdf_URL", "Report Html Address"],
    "timeout" : "30"
}
```
The part to the left of the : is what the setting is called. Do not change this!

The part to the right of the : is what that setting is currently set to. You can change these to whatever you want.

I will now explain what each setting does.

## downloads_location

```
"downloads_location" : "downloads/",
```

This setting tells the program what folder to put the downloaded PDFs in. It can be an absolute path, such as `"C:\Users\KOM\Documents\download-task\downloads"` (Windows) or `"/Users/KOM/Documents/download-task/downloads"` (Mac), or a relative path, such as `"downloads"`.

## sheets_location

```
"sheets_location" : "sheets/",
```

This setting tells the program what folder to look for the spreadsheets in. It can be an absolute path, such as `"C:\Users\KOM\Documents\download-task\sheets"` (Windows) or `"/Users/KOM/Documents/download-task/sheets"` (Mac), or a relative path, such as `"sheets"`.

## name_of_sheet_with_urls

```
"name_of_sheet_with_urls" : "GRI_2017_2020 (1).xlsx",
```

The name of the spreadsheet that has the URLs you want to download. 

You can write it with or without the `.xlsx`, up to you, either works.

## name_of_sheet_with_results

```
"name_of_sheet_with_results" : "Results_2017_2020.xlsx",
```

The name of the spreadsheet you want to put the results in.  

IF YOU PUT THE NAME OF AN EXISTING SPREADSHEET, THAT SPREADSHEET WILL GET OVERWRITTEN!

You can write it with or without the `.xlsx`, up to you, either works.

## filename_column

```
"filename_column" : "BRnum",
```

The title of the column in the URLs spreadsheet that has the name you want to give the downloaded files.

## columns_to_check

```
"columns_to_check" : ["Pdf_URL", "Report Html Address"],
```

The titles of the columns in the URLs spreadsheet that has the links you want to try downloading from.
For each line in the spreadsheet, the program will try these columns in the order you put them.

Note that the column names are wrapped in square brackets []. This is important! Do not remove the square brackets! The square brackets are how we tell the program that we're giving it a list of values, instead of just one value.

## timeout

```
"timeout" : "30"
```

Sometimes a file takes a long time to download. This setting tells the program how many seconds it should wait for a download before giving up on it.

If you set this to a high number, the program will probably take a longer time to run.

# Error messages

I've tried to make sure that if something goes wrong, the program writes you a reasonably understandable error message that tells you what the something is.

If you get an error message that is many lines long, and has bits of code in it, that's not one of mine, and it means things went wrong in a way I didn't predict was possible. I suggest you try running the program again, and if the issue keeps happening, download a fresh copy of config.json and start over on editing it to have the settings you want.