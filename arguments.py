import argparse
import json
import os

class parse_args():
    """
    - Creates Arguments Parser object
    - Creates a dictory with the folder name specified by --folder argument
    - Creates a json file with the same name as the folder and stores the arguments as
    """
    
    def __init__(self):
        argParser = argparse.ArgumentParser(description='arguments')
        argParser.add_argument('--feeder', default='34Bus', type=str, help='name of the feeder system')
        argParser.add_argument('--feeder-file', default='Run_IEEE34Mod1.dss', type=str, help='name of the feeder system')
        argParser.add_argument('--folder', default='initial_folder', type=str, help='the name of folder to store the generated dataset and also the JSON file which will store the parameters')
        self.args = argParser.parse_args()
    
    def get_args(self):
        return self.args
    
    def dump_json(self):
        folder_name = os.path.splitext(self.args.folder)[0]
        json_file=folder_name # json file name with the same name as the folder
        os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
        
        json_path = os.path.join(folder_name, self.args.folder)
        
        with open(json_path, 'w') as json_file:
            json.dump(vars(self.args), json_file, indent=4)