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

def _read_config(filepath):
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

class config:
    def __init__(self, path):
        self.error = None
        self.raw = {}
        try:
            self.raw = _read_config(path)
            _error_if_incomplete(self.raw)
            self.save_as = self.raw["filename_column"]
            self.download_path = _create_if_doesnt_exist(self.raw["downloads_location"])
            self.url_sheet_path = _sheet_path(self.raw["sheets_location"], self.raw["name_of_sheet_with_urls"], must_exist = True)
            self.result_sheet_path = _sheet_path(self.raw["sheets_location"], self.raw["name_of_sheet_with_results"])
            self.columns_to_check = _ensure_is_list(self.raw["columns_to_check"])
            self.timeout = _ensure_is_positive_int(self.raw["timeout"])
        except Exception as e:
            self.error = str(e)
    def all_attrs(self):
        result = self.raw.copy()
        result.update(self.__dict__)
        return result
    def check_columns(self, df):
        if not self.save_as in df.columns:
            self.error = "id_column_not_found"
        for column_name in self.columns_to_check:
            if not column_name in df.columns:
                self.error = "check_column_not_found"