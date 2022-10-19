import os.path
import json

def _create_if_doesnt_exist(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    return path

def _sheet_path(folderpath, filename, must_exist = False):
    if not os.path.isdir(folderpath):
        raise Exception("sheets_location_not_found")
    path = os.path.join(folderpath, filename)
    if os.path.splitext(path)[1] == "":
        path += ".xlsx"
    if must_exist and not os.path.exists(path):
        raise Exception("url_sheet_not_found")
    return path

def read_config(filepath):
    try:
        with open(filepath, "r") as f:
            json_str = f.read()
            # the user might input a filepath with backslashes, which the json parser chokes on
            json_str = json_str.replace("\\", "/")
    except FileNotFoundError:
        raise Exception("config_not_found")
    except json.decoder.JSONDecodeError:
        raise Exception("config_invalid")
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
            raise Exception("config_incomplete")

def _ensure_is_list(columns_var):
    if type(columns_var) != list:
        raise Exception("not_list")
    return columns_var

def _ensure_is_positive_int(timeout_str):
    try:
        timeout = int(timeout_str)
        if timeout <= 0:
            raise ValueError
    except ValueError as e:
        raise Exception("not_positive_int")
    return timeout

def parse_config(raw_config):
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
            _ensure_is_list(raw_config["columns_to_check"]),
        "timeout" :
            _ensure_is_positive_int(raw_config["timeout"])
    }
    return config


def check_columns(df, config):
    if not config["save_as"] in df.columns:
        return False, "id_column_not_found"
    for column_name in config["columns_to_check"]:
        if not column_name in df.columns:
            return False, "check_column_not_found"
    return True, None