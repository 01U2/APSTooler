'''        
## Disclaimer
The APSTooler ("the toolkit") is provided without any warranties. Its use is at your own risk, and the creator accepts no liability for any damages arising from its use. The toolkit is for informational purposes only and should not be considered professional advice. By using the toolkit, you agree to indemnify the creator against any claims or damages. If you do not agree, please refrain from using the toolkit.

## Documentation
The code is  interface for interacting with the Autodesk AutoCAD API:


The DWG class s used to manage and update custom attributes in AutoCAD DWG files.
Attributes
----------    
`dir` : Directory path where the cache JSON file is stored.

Methods
-------
cache_files(acc_dir):
Extracts information from DWG files in the specified directory and stores it in a JSON cache file.

load_cache(): 
Reads and returns the content of the cache JSON file.

update_att(attributes):
Updates custom attributes in the DWG files based on the provided attributes.

_update_custom_atts(file_path, item_atts):
Internal method to update custom attributes in a specific DWG file.
'''

import os
from datetime import datetime
import json
import comtypes.client
import time

class DWG:
    
    def __init__(self, dir):
        self.dir = dir
    
    def cache_files(self, acc_dir):
        cache_file_path = os.path.join(self.dir, "acc_cache.json")
        cache_file = {}
        count = 0
        for root, _, files in os.walk(acc_dir):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                if file_name.lower().endswith('.dwg'):
                    file_modified_date = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                    cache_file[file_name] = {
                        "path": file_path,
                        "modified_time": file_modified_date
                    }
                    count += 1
                    print(f"{file_name} added")
        with open(cache_file_path, 'w') as C:
            json.dump(cache_file, C, indent=4)
            print(f"{count} files were found")
            return "json file created at C:\\temp"
    
    def load_cache(self):
        cache_file = os.path.join(self.dir, "acc_cache.json")
        if os.path.isfile(cache_file):
            with open(cache_file, 'r') as c:
                return json.load(c)
        else:
            return "Cache file not found"
    
    def update_att(self, attributes):
        cache_file = self.load_cache()
        for item in attributes:
            for file_name, item_att in item.items():
                if file_name in cache_file:
                    file_path = cache_file[file_name]["path"]
                    try:
                        self._update_custom_atts(file_path, item_att)
                        print(f"{file_name} was updated successfully")
                    except Exception as e:
                        print(f"{file_name} error: {e}")
                else:
                    raise FileNotFoundError(f"{file_name} was not found")
    
    def _update_custom_atts(self, file_path, item_atts):
        acad = None
        new_cad = False
        try:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"{file_path} was not found")
            try:
                acad = comtypes.client.GetActiveObject("AutoCAD.Application")
            except (OSError, comtypes.COMError):
                acad = comtypes.client.CreateObject("AutoCAD.Application")
                acad.Visible = False
                new_cad = True

            cad = acad.Documents.Open(file_path)
            custom_info = cad.SummaryInfo

            for key, value in item_atts.items():
                retry_count = 0
                while retry_count < 3:
                    try:
                        custom_info.AddCustomInfo(key, str(value))
                        print(f"{key} : {value} added")
                        break  # Exit the while loop if successful
                    except Exception as e:
                        if e.args[0] == -2145386475:  # duplicate key error
                            custom_info.SetCustomKey(key, str(value))
                            print(f"{key} : {value} updated")
                            break  # Exit the while loop if successful
                        elif 'Call was rejected by callee' in str(e):
                            inner_retry_count = 0
                            while inner_retry_count < 3:
                                try:
                                    time.sleep(2)
                                    custom_info.AddCustomInfo(key, str(value))
                                    print(f"{key} : {value} added")
                                    break  # Exit the inner while loop if successful
                                except Exception as inner_e:
                                    if 'Call was rejected by callee' in str(inner_e):
                                        inner_retry_count += 1
                                        if inner_retry_count == 3:
                                            raise inner_e  # Re-raise the exception if it fails 3 times
                                    else:
                                        raise inner_e  # Re-raise other exceptions
                            else:
                                retry_count += 1
                        else:
                            raise e  # Re-raise other exceptions

            time.sleep(1)
            cad.Save()
        except FileNotFoundError as e:
            print(e)
        except comtypes.COMError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            time.sleep(3)
            cad.Close()
            if new_cad:
                acad.Quit()
