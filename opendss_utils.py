# OpenDSS Imports
import py_dss_interface 

# Python Libraries Import
import os 
import pathlib
 
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
    """Exclude pre-specified buses defined in a python dictionary
    """
    if feeder_name=="34Bus":
        bus_to_exclude =['sourcebus','888','890']
        updated_bus_list = [bus for bus in bus_list if bus not in bus_to_exclude]
    elif feeder_name=="123Bus":
    
    elif feeder_name=="13Bus":
         updated_bus_list=bus_list
        
    return 
        
    