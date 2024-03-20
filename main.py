#Imports
# Python Imports
import os
from dataclasses import dataclass

# Local Imports
from opendss_utils import * 
from fault_simulation import FaultSimulation
from arguments import parse_args
from utils import store_feeder_info_to_json

def initialize():
    """
     - Get the arguments passed in
     - Initialize the dss object
    """
    
    # Handle the arguments passed in 
    argument_parser=parse_args()       
    argument_parser.dump_json()
    args=argument_parser.get_args()
    
    # Initialize the OpenDSS object and get the file path
    dss, dss_file=OpenDSS(args.feeder,args.feeder_file).get_dss_obj()
    
    # Compile the dss file and solve power flow for the first time 
    dss.text(f"compile [{dss_file}]")
    dss.text(f"solve")
    
    return args,dss
    
def generate_feeder_infos(args,dss,store_info=False):
    """Generate necessary information for fault simulation
        - Gets the bus list of the feeder system (after exclusion of extra buses)
        - Get bus list by number of phases 
        - Get connectivity information of the feeder system
        - Get the one-hop bus names for each bus
        - Get the two-hop bus names for each bus
    """    
    # Get name of all the buses that is returned by py_dss_interface
    bus_list_before_exclusion = dss.circuit_all_bus_names() 
      
    # Exclude Buses to get the updated bus list
    bus_to_exclude,bus_list=exclude_buses(args.feeder,bus_list_before_exclusion)
    
    # Get Buslist by number of phases
    bus_list_1_phase, bus_list_2_phases,bus_list_3_phases=get_buses_by_phase(dss,bus_list)
    
    # Get connected load names and the name of the buses with connected loads
    bus_with_loads_connected,connected_loads_name=get_connected_loads(dss,bus_list)
    
    # Get connectivity info of the feeder system
    edge_list_by_bus_id,edge_list_by_bus_name,bus_id_map=get_connectivity_info(dss,bus_list)
      
    # Get nodes for all the buses
    nodes,nodes_by_name=get_nodes(dss,bus_list)  
    
    # Get one-hop bus names for each bus
    neighborhood_dict_1_hop_by_bus_name=get_one_hop_buses(edge_list_by_bus_name)
    
    # Get two-hop bus names for each bus
    neighborhood_dict_2_hop_by_bus_name= get_two_hop_buses(edge_list_by_bus_name)
    
    # Dictionary containig info related to the feeder system
    feeder_infos={'bus_list_before_exclusion':bus_list_before_exclusion,
                  'bus_list':bus_list,
                  'bus_to_exclude':bus_to_exclude,
                  'bus_list_1_phase': bus_list_1_phase,
                  'bus_list_2_phases': bus_list_2_phases,
                  'bus_list_3_phases': bus_list_3_phases,
                  'edge_list_by_bus_id': edge_list_by_bus_id,
                  'edge_list_by_bus_name':edge_list_by_bus_name,
                  'bus_id_map':bus_id_map,
                  'bus_with_loads_connected':bus_with_loads_connected,
                  'connected_loads_name':connected_loads_name}
   
    if store_info:
        # Store the info related to the feeder system to a json file
       
       
        store_feeder_info_to_json(args,feeder_infos)
        
    # Create data class to store feeder related informations    
    @dataclass
    class FeederInformation:
        feeder_name:str
        bus_list: list
        bus_list_1_phase: list
        bus_list_2_phases: list
        bus_list_3_phases: list
        edge_list_by_bus_id: list[tuple[int]]
        edge_list_by_bus_name: list[tuple[str]]
        nodes:list[str]
        nodes_by_name:list[str]
        bus_id_map: dict
        neighborhood_dict_1_hop_by_bus_name:dict
        neighborhood_dict_2_hop_by_bus_name:dict
                
    # Construct the feeder object which contains the all the information related to feeder
    feeder = FeederInformation(args.feeder,bus_list,
                                bus_list_1_phase, bus_list_2_phases,bus_list_3_phases
                               ,edge_list_by_bus_id,edge_list_by_bus_name,nodes,nodes_by_name,bus_id_map,
                               neighborhood_dict_1_hop_by_bus_name,neighborhood_dict_2_hop_by_bus_name)
    return feeder


def generate_fault_infos(args):
    """ Generate additional information necessary for fault simulation
        - Get the fault resistance values for fault simulation
        - Get the load values for fault simulation 
    """
    # Get fault resistance values
    fault_resistances=get_resistance_values(args,viz=False,num_bins=20,decimal_precision=2)
    
    # Get load values 
    load_values=get_load_values(args,decimal_precision=2)
    
    # Create data class to generate 
    @dataclass
    class FaultInformation:
         fault_resistances:list
         load_values:list
         
    fault_information= FaultInformation(fault_resistances,load_values)
    return fault_information
         
def main():
    # Initialize the DSS object and also get the arguments passed in 
    args, dss=initialize()
    
    # Collect the feeder infos
    feeder=generate_feeder_infos(args,dss,store_info=True)
    fault_information=generate_fault_infos(args)
    
    # Get the fault simulator object 
    fault_simulaor=FaultSimulation(dss,feeder,fault_information)
    
    fault_simulaor.fault_simulation_lg()
    
    
if __name__ == "__main__":
    main()
    





