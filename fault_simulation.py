import py_dss_interface    
import numpy as np

class FaultSimulation:
    
    def __init__(self,dss,feeder,fault_information):
        
        self.dss=dss
        self.feeder=feeder
        self.fault_information=fault_information
        
        # Dictionary that maps fault types to a integer number
        self.fault_class_map={'LG':0,'LL':1,'LLG':2,'LLL':3,'LLLG':4,'Non_Fault':5}  
        
        # Separate lists to contain the feature matrics by fault type                
        self.dataset_lg=[]                                                                                                                  
        self.dataset_ll=[]                                                                                                                 
        self.dataset_llg=[]                                                                                                                      
        self.dataset_lll=[] 
        self.dataset_lllg=[] 
        self.dataset_non_fault=[] 
        
        # List to contain the entire fault dataset
        self.dataset=[]
        
        # Separate lists to hold the labels for the fault 
        self.fault_detection=[]
        self.labels_by_fault_node_name=[]                                                                                                        
        self.labels=[]    
        self.fault_class=[]                                                                                                                     
        self.fault_resistance=[]                                                                                                               
        self.fault_currrents=[]
    
                                                                                                                                                    
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
                                                                                                                                                
            for node in dss.bus_nodes():                                                                                     # Loop over the nodes of the bus 
                data_template[data_index,mapping_dict[node]:mapping_dict[node]+2]=active_bus_feature[count:count+2]          # Insert features in appropriate positions
                count=count+2                                                                                                # Increase count variable
                data_template[data_index,1::2]=np.radians(data_template[data_index,1::2])                                    # Convert the angle from degree unit to radian unit
                    
        return  data_template    

        
    def fault_simulation_lg():
        pass
    
    def fault_simulation_ll():
        pass
    
    def fault_simulation_llg():
        pass
    
    def fault_simulation_lll():
        pass
    
    def fault_simulation_llg():
        pass
    
    def non_fault_simulation():
        pass