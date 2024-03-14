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
        argParser.add_argument('--feeder', default='123Bus', type=str, help='name of the feeder system')
        argParser.add_argument('--feeder-file', default='IEEE123Master.dss', type=str, help='name of the feeder system')
        argParser.add_argument('--folder', default='initial_folder', type=str, help='the name of folder to store the generated dataset and also the JSON file which will store the parameters')
        argParser.add_argument('--fault-resistance-type',choices=["fixed", "variable"], default='fixed', type=str, help='if the resistance is fixed to a single value or is it variable within a specified range')
        argParser.add_argument('--fault-resistance-value', default=20.00, type=float, help='if the resistance is specified as fixed, the value of the resistance')
        argParser.add_argument('--fault-resistance-lower-end', default=0.05, type=float, help='if the resistance is specified as variable, the lower limit of the uniform distribution from which fault resistance will be sampled')
        argParser.add_argument('--fault-resistance-upper-end', default=20.00, type=float, help='if the resistance is specified as variable, the upper limit of the uniform distribution from which fault resistance will be sampled')
        argParser.add_argument('--change-load-values', default=False, type=bool, help='whether to change the original load value')
        argParser.add_argument('--load-value-KW-lower-end', default=20.00, type=float, help='if the load value is to be changed, the lower end of the uniform distribution from which load value will be sampled')
        argParser.add_argument('--load-value-KW-upper-end', default=80.00, type=float, help='if the load value is to be changed, the upper end of the uniform distribution from which load value will be sampled')
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