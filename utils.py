#Imports
import os 
import json
from collections import OrderedDict


def store_feeder_info_to_json(args,infos):
    
    feeder_info = OrderedDict()
    feeder_info['name_of_the_feeder']=args.feeder
    feeder_info['num_of_original_buses']=len(infos['bus_list_before_exclusion'])
    feeder_info['num_of_buses']=len(infos['bus_list'])
    feeder_info['num_of_excluded_buses']=len(infos['bus_list_before_exclusion'])-len(infos['bus_list'])
    feeder_info['num_single_phase_buses'],feeder_info['num_two_phase_buses'],feeder_info['num_three_phase_buses']= len(infos['bus_list_1_phase']),len(infos['bus_list_2_phases']),len(infos['bus_list_3_phases'])
    feeder_info['num_edges']=int(len(infos['edge_list_by_bus_name'])/2)
    
    folder_name = os.path.splitext(args.folder)[0]
    json_file='feeder_infos' # json file name with the same name as the folder
    os.makedirs(folder_name, exist_ok=True)  # Create folder if it doesn't exist
    json_path = os.path.join('../..',folder_name, json_file)
    
  
    with open(json_path, 'w') as json_file:
        json.dump(feeder_info, json_file, indent=4)