import os.path
import json

def _create_if_doesnt_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def _sheet_path(folderpath, filename, must_exist = False):
    if not os.path.isdir(folderpath):
        raise Exception(f"You wrote {folderpath} in sheets_location, but that doesn't seem to be a folder that exists.")
    path = os.path.join(folderpath, filename)
    if os.path.splitext(path)[1] == "":
        path += ".xlsx"
    if must_exist and not os.path.exists(path):
        raise Exception(f"You wrote {filename} in name_of_sheet_with_urls, but that's not the name of a file that exists in {folderpath}")
    return path

def _read_config(filepath):
    try:
        with open(filepath, "r") as f:
            json_str = f.read()
            # the user might input a filepath with backslashes, which the json parser chokes on
            json_str = json_str.replace("\\", "/")
    except FileNotFoundError:
        raise Exception(f"Cannot find a file named {filepath}")
    except json.decoder.JSONDecodeError as e:
        raise Exception(f"Your config file is not a valid json file. (This is what the computer thinks is the issue: {e})")
    return json.loads(json_str)

def _error_if_incomplete(raw_config):
    for config_entry_name in ["downloads_location", 
                                "sheets_location", 
                                "name_of_sheet_with_urls",
                                "name_of_sheet_with_results",
                                "filename_column",
                                "columns_to_check",
                                "timeout"]:
        if config_entry_name not in raw_config:
            raise Exception(f"Your config file is missing {config_entry_name}")

def _ensure_is_list(variable, key):
    if type(variable) != list:
        raise Exception(f"You wrote {variable} in {key}, but {key} needs to be a list (wrapped in square brackets [])")
    return variable

def _ensure_is_positive_int(variable, key):
    try:
        number = int(variable)
        if number <= 0:
            raise ValueError
    except ValueError as e:
        raise Exception(f"You wrote {variable} in {key}, but that's not a positive whole number.")
    return number

def parse_config(filepath):
    raw_config = _read_config(filepath)
    _error_if_incomplete(raw_config)
    config = {
        "save_as" : raw_config["filename_column"],
        "download_path" : 
            _create_if_doesnt_exist(raw_config["downloads_location"]),
        "url_sheet_path" : 
            _sheet_path(raw_config["sheets_location"], raw_config["name_of_sheet_with_urls"], must_exist = True),
        "result_sheet_path" : 
            _sheet_path(raw_config["sheets_location"], raw_config["name_of_sheet_with_results"]),
        "columns_to_check" :
            _ensure_is_list(raw_config["columns_to_check"], "columns_to_check"),
        "timeout" :
            _ensure_is_positive_int(raw_config["timeout"], "timeout")
    }
    return config


def check_columns(df, config):
    if not config["save_as"] in df.columns:
        return False, f"You wrote {config['save_as']} in id_column_name, but that's not the title of a column that exists in the URL sheet."
    for column_name in config["columns_to_check"]:
        if not column_name in df.columns:
            return False, f"You wrote {column_name} in columns_to_check, but that's not the title of a column that exists in the URL sheet."
    return True, None