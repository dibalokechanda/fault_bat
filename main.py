#Imports
# Python Imports
import os

# Local Imports
from opendss_utils import OpenDSS, exclude_buses, get_buses_by_phase, get_connectivity_info, get_resistance_values,get_load_values,get_one_hop_buses, get_two_hop_buses
from arguments import parse_args
from utils import store_feeder_info_to_json

def initialize():
    """
     - Get the arguments passed 
     - Initialize the dss object
    """
    
    # Handle the arguments passed in 
    argument_parser=parse_args()       
    argument_parser.dump_json()
    args=argument_parser.get_args()
    
    # Initialize the OpenDSS object and get the file path
    dss, dss_file=OpenDSS(args.feeder,args.feeder_file).get_dss_obj()
    
    # Compile the dss file and solve power flow 
    dss.text(f"compile [{dss_file}]")
    dss.text(f"solve")
    
    return args,dss
    
def generate_feeder_infos(store_info=False):
    """Generate necessary information for fault simulation
        - Gets the bus list of the feeder system (after exclusion of extra buses)
        - Get bus list by number of phases 
        - Get connectivity information of the feeder system
        - Get the fault resistance values for fault simulation
        - Get the load values for fault simulation 
        - Get the one-hop bus names for each bus
        - Get the two-hop bus names for each bus
    """
   
    args, dss=initialize()
    
    # Get name of all the buses
    bus_list = dss.circuit_all_bus_names() 
      
    # Exclude Buses to get the updated bus list
    bus_to_exclude,updated_bus_list=exclude_buses(args.feeder,bus_list)
    
    # Get Buslist by number of phases
    bus_list_1_phase, bus_list_2_phases,bus_list_3_phases=get_buses_by_phase(dss,updated_bus_list)
    
    # Get connectivity info of the feeder system
    edge_list_by_bus_id,edge_list_by_bus_name,bus_id_map=get_connectivity_info(dss,updated_bus_list)
    
    # Get fault resistance values
    fault_resistances=get_resistance_values(args,viz=False,num_bins=20,decimal_precision=2)
    
    # Get load values 
    load_values=get_load_values(args,decimal_precision=2)
    
    # Get one-hop bus names for each bus
    neighborhood_dict_1_hop_by_bus_name=get_one_hop_buses(edge_list_by_bus_name)
    
    # Get two-hop bus names for each bus
    neighborhood_dict_2_hop_by_bus_name= get_two_hop_buses(edge_list_by_bus_name)
    
    # Dictionary containig info related to the feeder system
    feeder_infos={'bus_list':bus_list,
                  'updated_bus_list':updated_bus_list,
                  'bus_to_exclude':bus_to_exclude,
                  'bus_list_1_phase': bus_list_1_phase,
                  'bus_list_2_phases': bus_list_2_phases,
                  'bus_list_3_phases': bus_list_3_phases,
                  'edge_list_by_bus_id': edge_list_by_bus_id,
                  'edge_list_by_bus_name':edge_list_by_bus_name,
                  'bus_id_map':bus_id_map}
    
    if store_info:
         # Store the info related to the feeder system to a json file
        store_feeder_info_to_json(args,feeder_infos)
        
    return feeder_infos
         
def main():
    feeder_infos=generate_feeder_infos(store_info=False)
    

if __name__ == "__main__":
    main()
    





