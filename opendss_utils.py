# OpenDSS Imports
import py_dss_interface 

# Python Libraries Import
import os 
import pathlib
import random
from collections import defaultdict


# Additional Imports
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import networkx as nx
 
class OpenDSS():
    """Interfacing to OpenDSS with py_dss_interface

    Attributes:
        feeder_name:str: Name of feeder e.g.  13Bus, 34Bus, 37Bus, 123Bus,
        feeder_init_dss_file:str: Initial OpenDSS file that need to get excuted to load the DSS object e.g. 
                                  IEEE13Nodeckt.dss, ieee37.dss, Run_IEEE34Mod1.dss, IEEE123Master.dss

    Methods:
        get_dss_obj(): Returns the initialized OpenDSS object

    """
    def __init__(self,feeder_name,feeder_init_dss_file):
        self.script_path = os.path.dirname(os.path.abspath('__file__'))                      
        self.dss_file = pathlib.Path(self.script_path).joinpath("feeders",feeder_name, feeder_init_dss_file )
        self.dss=py_dss_interface.DSSDLL()
        
    def get_dss_obj(self):
        return self.dss, self.dss_file
    
def exclude_buses(feeder_name,bus_list):
    """Exclude pre-specified buses
       By default OpenDSS returns additional buses which are disconnected from the original feeder system
    """
    if feeder_name=="13Bus":
        bus_to_exclude =['sourcebus','634']
    elif feeder_name=="34Bus":          # Total Numbr of bus: 36 --> Includes 
        bus_to_exclude =['sourcebus']
    elif feeder_name=="37Bus":          # Total Number of bus : 38 --> 37 normal buses + 1 regulator bus (799r)
        bus_to_exclude =['sourcebus']  
    elif feeder_name=="123Bus":
        bus_to_exclude =['610','300_open','94_open','150']
        
    updated_bus_list = [bus for bus in bus_list if bus not in bus_to_exclude]
    return bus_to_exclude,updated_bus_list
        
        
def get_buses_by_phase(dss,updated_bus_list):
    """Filter out buses by number of phases
    """

    bus_list_3_phases = []
    bus_list_2_phases =[]
    bus_list_1_phase =[]

    for bus in updated_bus_list:                                                                                                          
        dss.circuit_set_active_bus(bus)                                                                                            
        if len(dss.bus_nodes())==3:                                                                                                
            bus_list_3_phases.append(bus)
        if len(dss.bus_nodes())==2:                                                                                                
            bus_list_2_phases.append(bus)
        if len(dss.bus_nodes())==1:                                                                                                 
            bus_list_1_phase.append(bus)   
            
    return bus_list_1_phase, bus_list_2_phases,bus_list_3_phases
    
def get_nodes(dss,bus_list):
    nodes_by_name=[]                                                                                                    
    nodes=[]                                                                                                            

    for active_bus in bus_list:                                                                                               
        dss.circuit_set_active_bus(active_bus)                                                                            # Set a particular bus to be active
        for node in dss.bus_nodes():                                                                                      # Loop over all the nodes of the active bus
            nodes_by_name.append(active_bus+'_'+str(node))                                                               
            nodes.append(active_bus+'.'+str(node))                                                                      

    return nodes_by_name,nodes

def get_connectivity_info(dss,bus_list):
    
    edge_list_by_bus_name=[]                                                                                                       
    edge_list_by_bus_id=[]  
    
    bus_ids =list(range(len(bus_list)))    
    bus_id_map = dict(zip(bus_list, bus_ids))                                                                        
    
    for active_bus1 in bus_list:                                                                                        # Enumerate over all the buses 
        dss.circuit_set_active_bus(active_bus1)                                                                         # Set a particular bus to be active
        pde_bus1= dss.bus_all_pde_active_bus()                                                                          # For a particular bus get the power delivery element to it as a list 
        for active_bus2 in bus_list:                                                                                    # Enumerate over all the buses again
            dss.circuit_set_active_bus(active_bus2)                                                                     # Set a particular bus to be active
            pde_bus2 = dss.bus_all_pde_active_bus()                                                                     # For a particular bus get the the power delivery element to it as a list 
            if any(element in  pde_bus1 for element in  pde_bus2) and active_bus1!=active_bus2:                         # If there is a common power delivery element and two buses are not the same
                edge_list_by_bus_name.append((active_bus1,active_bus2))                                                            
                edge_list_by_bus_id.append((bus_id_map[active_bus1],bus_id_map[active_bus2]))                                      
                
    return edge_list_by_bus_id,edge_list_by_bus_name,bus_id_map


def get_resistance_values(args,viz=False,**kwargs):
    """Generate resistance value for fault simulation
       Two ways are specified for generating the resistance values: fixed and variable
       - fixed: returns the same value repeated for number of sampels 
       - variable: Assuming data is generated for three-phase (node) bus, for each phase (node) a random seed is set and resistance value is sampled from a uniform distribution
       
    If viz is set to True it will create a histogram of sampled values and save the image to --folder
    """
    if args.fault_resistance_type=="fixed":
        number_of_samples=args.number_of_samples_for_each_node
        fault_resistance_val=args.fault_resistance_value
        fault_resistances=[fault_resistance_val]*number_of_samples
        
    if args.fault_resistance_type=="variable":
        
        # Check if decimal precision was passed in as kwargs
        decimal_precision = kwargs.get('decimal_precision', 2)  # Using .get() method to get the value or a default value if not found

        # Extract lower and upper bound of the uniform distribution from the passed arguments
        lower_bound=args.fault_resistance_lower_end
        upper_bound=args.fault_resistance_upper_end
        
        # Extract number of samples 
        number_of_samples=args.number_of_samples_for_each_node
        
        fault_resistances=[]
        for _ in range(3):
        # Set a random seed 
            seed=random.randint(1,1000)
            np.random.seed(seed)
        # Generate fault resistance value by sampling from a uniform distribution
            fault_resistance_samples_per_node= list(np.round(np.random.uniform(lower_bound,upper_bound,number_of_samples), decimals=decimal_precision))
            fault_resistances.extend(fault_resistance_samples_per_node)  
                
    if viz==True:
        num_bins = kwargs.get('num_bins', 10)  # Using .get() method to get the value or a default value if not found
        sns.histplot(fault_resistances, bins=num_bins, kde=False)  
        plt.xlabel('Fault Resistance Values')
        plt.ylabel('Frequency')
        
        file_path = os.path.join('../../',args.folder,f'fault_resistance_histogram.png')

        plt.savefig(file_path)

              
    return fault_resistances


def get_load_values(args,**kwargs):
    if args.change_load_values=='no':
        pass
    
    elif args.change_load_values=='yes':
        # Check if decimal precision was passed in as kwargs
        decimal_precision = kwargs.get('decimal_precision', 2)  # Using .get() method to get the value or a default value if not found
        
        upper_bound_KW=args.load_value_KW_lower_end
        lower_bound_KW=args.load_value_KW_upper_end
        
        # Extract number of samples 
        number_of_samples=args.number_of_samples_for_each_node
        
        # Generate load values by sampling from a uniform distribution
        lds= list(np.round(np.random.uniform(upper_bound_KW,lower_bound_KW,number_of_samples),decimals=decimal_precision))                                                       
        
        return lds

def get_one_hop_buses(edge_list_by_bus_name):
    """Generate bus list within one-hop for each bus in the feeder system
    """
    neighborhood_dict_1_hop_by_bus_name= defaultdict(set)
    # Iterate over each edge and add the neighboring nodes
    for node1, node2 in edge_list_by_bus_name:
        neighborhood_dict_1_hop_by_bus_name[node1].add(node2)
        neighborhood_dict_1_hop_by_bus_name[node2].add(node1)

    # Convert the sets to lists 
    neighborhood_dict_1_hop_by_bus_name = {node: list(neighborhood.union({node})) for node, neighborhood in neighborhood_dict_1_hop_by_bus_name.items()}
    
    return neighborhood_dict_1_hop_by_bus_name


def get_two_hop_buses(edge_list_by_bus_name):
    """Generate bus list within two-hop for each bus in the feeder system
    """
    # Create an empty graph
    graph = nx.Graph()

    # Add edges from the edge_list_by_bus_name
    graph.add_edges_from(edge_list_by_bus_name)

    # Get the 1-hop and 2-hop neighbors for every node
    neighborhood_dict_2_hop_by_bus_name = {}
    for node in graph.nodes():
        neighbors = set(graph.neighbors(node))
        neighborhood_dict_2_hop_by_bus_name[node] = neighbors.copy()
        for neighbor in neighbors:
            neighborhood_dict_2_hop_by_bus_name[node].update(set(graph.neighbors(neighbor)))

    neighborhood_dict_2_hop_by_bus_name = {node: list(neighborhood.union({node})) for node, neighborhood in neighborhood_dict_2_hop_by_bus_name.items()}

    return neighborhood_dict_2_hop_by_bus_name


def get_nodes(dss,bus_list):
    """Get all the possible nodes for all the buses
    """  
    nodes=[]                                                                                                            # A list to contain the possible nodes
    for active_bus in bus_list:                                                                                         # Enumerate over all buses
        dss.circuit_set_active_bus(active_bus)                                                                          # Set a particular bus to be active
        for node in dss.bus_nodes():                                                                                    # Loop over all the nodes of the active bus
            nodes.append(active_bus+'.'+str(node))                                                                      # Get the node by concatenating the bus name and the node name
   
    return nodes