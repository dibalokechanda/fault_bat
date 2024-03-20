import py_dss_interface    
import numpy as np

class FaultSimulation:
    
    def __init__(self,dss,feeder,fault_information):
        self.dss=dss
        self.feeder=feeder
        self.fault_information=fault_information
        
        
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

        
    