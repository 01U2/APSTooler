"""
## Disclaimer

The APSTooler ("the toolkit") is provided without any warranties. Its use is at your own risk, and the creator accepts no liability for any damages arising from its use. The toolkit is for informational purposes only and should not be considered professional advice. By using the toolkit, you agree to indemnify the creator against any claims or damages. If you do not agree, please refrain from using the toolkit.

## Documentation

The code is  interface for interacting with the Autodesk AutoCAD API:


"""
import os
import time
import datetime
import time
import json


class DWG:
    def __init__(self, dir):
        self.dir = r"C:\temp\accCache.json"
        pass
    
    def cache_files(self, acc_dir):
        cache_file_path = r"C:\temp\accCache.json"
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
                    count+=1
                    print(f"{file_name} added")
        with open(cache_file_path, 'w') as C:
            json.dump(cache_file, C, indent = 4)
            print(f"{count} files were found")
            return "json file create at C:\temp"
        