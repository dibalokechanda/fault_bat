import py_dss_interface    
import numpy as np
from tqdm import tqdm
import itertools

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
        self.fault_detection_labels=[]
        self.fault_location_labels=[]    
        self.fault_class_labels=[]  
        self.labels_by_fault_node_name=[]                                                                                                                                                                                                                    
        self.fault_resistance_labels=[]                                                                                                               
        self.fault_currrents_labels=[]
    
                                                                                                                                                    
    def get_features(self):    
        """
        Get features of all the buses in the feeder system
        """                                                                                
        feature_vec_dim=6                                                                                                    # Dimension of the feature vectors
        mapping_dict={1:0,2:2,3:4}                                                                                      
        data_template= np.zeros((len(self.feeder.bus_list),feature_vec_dim),dtype=np.float64)                                # Initialize the feature matrix each time
        
        for data_index,active_bus in enumerate(self.feeder.bus_list):                                                        # Enumerate over all the buses 
            self.dss.circuit_set_active_bus(active_bus)                                                                      # Set a active bus 
            active_bus_feature=self.dss.bus_pu_vmag_angle()                                                                  # Get the voltage amplitude (in per unit) and angle (in degrees) of the active bus
            count=0                                                                                                          # Set count variable to 0
                                                                                                                                                
            for node in self.dss.bus_nodes():                                                                                # Loop over the nodes of the bus 
                data_template[data_index,mapping_dict[node]:mapping_dict[node]+2]=active_bus_feature[count:count+2]          # Insert features in appropriate positions
                count=count+2                                                                                                # Increase count variable
                data_template[data_index,1::2]=np.radians(data_template[data_index,1::2])                                    # Convert the angle from degree unit to radian unit
                    
        return  data_template    

        
    def fault_simulation_lg(self):
        """Perform LG Fault Simulation
        """
        # Keep track of number of simulations
        count_lg=0

        # Enumerate over the fault name and fault nodes
        for fault_name,fault_node in tqdm(zip(self.feeder.nodes_by_name,self.feeder.nodes),desc="LG Fault Simulation",total=len(self.feeder.nodes)): 
            self.dss.circuit_set_active_bus(fault_name.split('_')[0])                                                       # Set a particular bus to be active
            if len(self.dss.bus_nodes())==3:                                                                                # Check if the bus has 3 nodes | If the bus has 3 nodes only then we create the fault   
                for idx,fr in enumerate(self.fault_information.fault_resistances):                                          # Enumerate over the fault resistnace                              
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={fault_node} Phases=1 r={fr}'                  # Command for the LG Fault
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'                                # Command for the Fault Object Deactivation
                     
                    self.dss.text(fault_command)                                                                            # Execute the LG Fault command
                    self.dss.text(f'Solve mode=direct')                                                                     # Run Power Flow in Direct mode
                    
                    # Get the features of the buses 
                    self.dataset.append(self.get_features())                                                        
                    self.dataset_lg.append(self.get_features())
                                                    
                    # Get the labels 
                    self.fault_detection_labels.append(1)                                                                                      
                    self.fault_class_labels.append(self.fault_class_map['LG'])                                             
                    self.fault_location_labels.append(self.feeder.bus_id_map[fault_name.split('_')[0]])                                 
                    self.fault_resistance_labels.append(fr)                                                                 
                    self.dss.circuit_set_active_element(fault_obj)                                                         # Set the fault object as active element to get the current 
                    self.fault_currrents_labels.append(abs(self.dss.cktelement_currents()[0]))
                    
                    # Execute the fault object deactivation command
                    self.dss.text(fault_obj_deactivate_command)      
                    
                    # Increment count of simulations performed
                    count_lg+=1  
                                             
    
                              
    def fault_simulation_ll(self):
        """Perform LL Fault Simulation
        """
        
        # Create a list of node pairs for LL fault simulation
        ll_nodes=[]
        for fault_node1, fault_node2 in itertools.permutations(self.feeder.nodes, 2):
            if fault_node1.split('.')[0] == fault_node2.split('.')[0] and fault_node1.split('.')[1] != fault_node2.split('.')[1] and int(fault_node1.split('.')[1]) < int(fault_node2.split('.')[1])  :
                ll_nodes.append((fault_node1, fault_node2))
                
        # Keep track of number of simulations
        count_ll=0

        for ll_node in tqdm(ll_nodes,desc="LL Fault Simulation"):
            self.dss.circuit_set_active_bus(ll_node[0].split('.')[0])
            
            fault_name= ll_node[0].split('.')[0]+'_'+ll_node[0].split('.')[1]+ll_node[1].split('.')[1]
            
            if len(self.dss.bus_nodes())==3:
                for idx,fr in enumerate(self.fault_information.fault_resistances):                    
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={ll_node[0]} Bus2={ll_node[1]} Phases=1 r={fr}'                   # Command for the LL Fault
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'                                                   # Command for the Fault Object Deactivation
                
                    self.dss.text(fault_command)                                                                                               # Execute the LL Fault command
                    self.dss.text(f'Solve mode=direct')                                                                                        # Run Power Flow in Direct mode
                    
                    # Get the features of the buses 
                    self.dataset.append(self.get_features())                                                                                  
                    self.dataset_ll.append(self.get_features())
                    
                    self.fault_detection_labels.append(1)
                    self.fault_class_labels.append(self.fault_class_map['LL'])                                                                                                                        
                    self.fault_location_labels.append(self.feeder.bus_id_map[ll_node[0].split('.')[0]])                                       
                    self.fault_resistance_labels.append(fr)                                                                                    
                    self.dss.circuit_set_active_element(fault_obj)
                    self.fault_currrents_labels.append(abs(self.dss.cktelement_currents()[0]))                                                # Set the fault object as active element to get the current                                  
                    
                    # Execute the fault object deactivation command   
                    self.dss.text(fault_obj_deactivate_command)                                                                                    
                    
                    # Increment count of simulations performed
                    count_ll=count_ll+1

    
    def fault_simulation_llg():
        pass
    
    def fault_simulation_lll():
        pass
    
    def fault_simulation_llg():
        pass
    
    def non_fault_simulation():
        pass