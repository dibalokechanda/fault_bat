# OpenDSS Imports
import py_dss_interface 

# Python Libraries Import
import os 
import pathlib

# Additional Import
import numpy as np
 
class OpenDSS():
    """Interfacing to OpenDSS with py_dss_interface

    Attributes:
        feeder_name:str: Name of feeder e.g. 34Bus, 123Bus, 13Bus.
        feeder_init_dss_file:str: Initial OpenDSS file that need to get excuted to load the DSS object e.g. 
                                  IEEE13Nodeckt.dss, Run_IEEE34Mod1.dss, IEEE123Master.dss

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
    elif feeder_name=="34Bus":
        bus_to_exclude =['sourcebus','888','890']
    elif feeder_name=="123Bus":
        bus_to_exclude =['610','300_open','94_open','150']
        
    updated_bus_list = [bus for bus in bus_list if bus not in bus_to_exclude]
    return updated_bus_list
        
        
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
    

def get_features(dss,bus_list):    
    """
    Get features of all the buses in the feeder system
    """                                                                                
    feature_vec_dim=6                                                                                                    # Dimension of the feature vectors
    mapping_dict={1:0,2:2,3:4}                                                                                      
    data_template= np.zeros((len(bus_list),feature_vec_dim),dtype=np.float64)                                            # Initialize the feature matrix each time
    
    for data_index,active_bus in enumerate(bus_list):                                                                    # Enumerate over all the buses 
        dss.circuit_set_active_bus(active_bus)                                                                           # Set a active bus 
        active_bus_feature=dss.bus_pu_vmag_angle()                                                                       # Get the voltage amplitude (in per unit) and angle (in degrees) of the active bus
        count=0                                                                                                          # Set count variable to 0
        if len(dss.bus_load_list())!=0:                                                                                  # Checking if the bus has loaded connected to it, only insert features vectors in the matrix if the bus has loaded connected to it                                    
            for node in dss.bus_nodes():                                                                                 # Loop over the nodes of the bus 
                data_template[data_index,mapping_dict[node]:mapping_dict[node]+2]=active_bus_feature[count:count+2]      # Insert features in appropriate positions
                count=count+2                                                                                            # Increase count variable
            data_template[data_index,1::2]=np.radians(data_template[data_index,1::2])                                    # Convert the angle from degree unit to radian unit
                
    return  data_template     