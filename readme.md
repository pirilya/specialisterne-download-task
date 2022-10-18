# Summary

This script will download pdf reports from links in a spreadsheet, and report the results back in a different spreadsheet, according to the settings the user has specified in the file `config.json`.

# Install/setup

## 1. Make sure you have Python installed

This is a Python script, so in order to run it you need to have Python installed. Python is automatically installed on Mac computers but not on Windows. [You can download Python here.](https://www.python.org/downloads/)

If you're on Windows and want to know whether you have Python installed, you can go to Settings -> Apps -> Apps & Features to see a list of all programs installed on your computer. If Python is on that list, you have Python installed.

## 2. Download the script files

The simplest way is to [download the zip from here](https://github.com/pirilya/specialisterne-download-task/zipball/main), and then unzip it.

## 3. Run the install script

Inside the folder you've just unzipped, there's a folder called "scripts". Go inside it.

If you're on Windows, double click the file `setup-windows.bat` to run it. If you're on Mac or Linux, do the same with `setup-sh.sh`. 

This will open a terminal / command line window. Don't close the window before it's done.

Once it says 

```

Setup complete! Press any key to close this window
```
you can close the window.

# Running the program

## 1. Edit config.json

The file config.json is where all your settings are, so if you want to change those, you need to edit config.json. The explanation of how to do this is in the section called [The config file](#the-config-file).

## 2. Run the script

Inside the scripts folder, click `run-windows.bat` if you're on Windows and `run-sh.sh` if you're on Mac or Linux. Just like during setup, this will open a terminal / command line window, which you shouldn't close until it's done running.

The text in the terminal is important information about what the script is doing, whether it ran successfully or encountered issues. I suggest you read it.

Once it says
```

The script is done! Press any key to close this window
```
you can close the window.

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

# For developers

If you're reading this section, I assume you're capable of running Python scripts.

If you used the setup script, the venv for this program is named `.venv`.

The python files are all in the `python/` folder. You have to run them from the root folder, since the path to config.json is hardcoded. So e.g.

```
(.venv) PS C:\Users\KOM\Documents\download-task> py python/download_files.py
```

The normal version of the program, that runs when a user clicks one of the run scripts, is `download_files.py`.

There's also a version that prints time elapsed as it runs, called `download_with_timer.py`. It will by default do the same thing as the regular `download_files.py`, just with a timer, but you can also call it with a flag like so:
```
python python/download_with_timer.py --from-empty
```
If you use this flag, it will first empty the download folder, so you can get benchmarks for how long it takes when you start from scratch.

You can test the script by running `test.py`.