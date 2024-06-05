import py_dss_interface    

# Python Built-in Modules Import
import itertools
from collections import Counter

# Additional Library Imports
import numpy as np
from tqdm import tqdm
from sklearn.preprocessing import StandardScaler
from print_color import print

 

class FaultSimulation:
    
    """Fault Simulation Class 
      - get_features --> Gets the voltage magnitude and phase values of all the buses in the feeder system 
      - standardize --> Perform standarization to the feature matrix with StandardScaler()
      - fault_simulation_lg --> Perform Line to Ground Fault Simulation 
      - fault_simulation_ll --> Perform Line to Line Fault Simulation 
      - non_fault_simulation --> Perform a simulation for non-fault events
      
    """
    
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
        self.fault_currents_labels=[]
    
                                                                                                                                                    
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
                if node !=4: 
                    data_template[data_index,mapping_dict[node]:mapping_dict[node]+2]=active_bus_feature[count:count+2]          # Insert features in appropriate positions
                    count=count+2                                                                                                # Increase count variable
                    data_template[data_index,1::2]=np.radians(data_template[data_index,1::2])                                    # Convert the angle from degree unit to radian unit
                    
        return  data_template    
    
    
    def standardize(self,final_dataset):
        scalers = {}
        for i in range(final_dataset.shape[1]):
            scalers[i] = StandardScaler()
            final_dataset[:, i, :] = scalers[i].fit_transform(final_dataset[:, i, :])         
            
        return final_dataset                                                                               

        
    def fault_simulation_lg(self):
        """Perform LG Fault Simulation
        """
        # Keep track of number of simulations (for debugging purpose)
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
                    self.fault_currents_labels.append(abs(self.dss.cktelement_currents()[0]))
                    
                    # Execute the fault object deactivation command
                    self.dss.text(fault_obj_deactivate_command)      
                    
                    # Increment count of simulations performed
                    count_lg+=1  
        
         # Convert the list of 2D dataset matrices into 3D matrix and standarize it 
        final_dataset_lg= self.standardize(np.stack(self.dataset_lg))
        
        # Return LG dataset only (Only needed if partial dataset need to be exported)  
        return final_dataset_lg                                         
             
    def fault_simulation_ll(self):
        """Perform LL Fault Simulation
        """
        
        # Create a list of node pairs for LL fault simulation
        ll_nodes=[]
        for fault_node1, fault_node2 in itertools.permutations(self.feeder.nodes, 2):
            if fault_node1.split('.')[0] == fault_node2.split('.')[0] and fault_node1.split('.')[1] != fault_node2.split('.')[1] and int(fault_node1.split('.')[1]) < int(fault_node2.split('.')[1])  :
                ll_nodes.append((fault_node1, fault_node2))
                
        # Keep track of number of simulations (for debugging purpose)
        count_ll=0

        for ll_node in tqdm(ll_nodes,desc="LL Fault Simulation"):
            self.dss.circuit_set_active_bus(ll_node[0].split('.')[0])
            
            fault_name= ll_node[0].split('.')[0]+'_'+ll_node[0].split('.')[1]+ll_node[1].split('.')[1]
            
            if len(self.dss.bus_nodes())==3:
                for idx,fr in enumerate(self.fault_information.fault_resistances):                    
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={ll_node[0]} Bus2={ll_node[1]} Phases=1 r={fr}'                   
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'                                                   
                
                    self.dss.text(fault_command)                                                                                              
                    self.dss.text(f'Solve mode=direct')                                                                                       
                    
                    # Get the features of the buses 
                    self.dataset.append(self.get_features())                                                                                  
                    self.dataset_ll.append(self.get_features())
                    
                    self.fault_detection_labels.append(1)
                    self.fault_class_labels.append(self.fault_class_map['LL'])                                                                                                                        
                    self.fault_location_labels.append(self.feeder.bus_id_map[ll_node[0].split('.')[0]])                                       
                    self.fault_resistance_labels.append(fr)                                                                                    
                    self.dss.circuit_set_active_element(fault_obj)
                    self.fault_currents_labels.append(abs(self.dss.cktelement_currents()[0]))                                                                                 
                    
                    # Execute the fault object deactivation command   
                    self.dss.text(fault_obj_deactivate_command)                                                                                    
                    
                    # Increment count of simulations performed
                    count_ll+=1
                    
        # Convert the list of 2D dataset matrices into 3D matrix and standarize it 
        final_dataset_ll= self.standardize(np.stack(self.dataset_ll))  
        
        # Return LL Dataset only (Only needed if partial dataset need to be exported)  
        return final_dataset_ll 
    
    
    def fault_simulation_llg(self):
        """Perform LLG Fault Simulation
        """
        
        llg_nodes=[]

        for fault_node1, fault_node2 in itertools.permutations(self.feeder.nodes, 2):
            if fault_node1.split('.')[0] == fault_node2.split('.')[0] and fault_node1.split('.')[1] != fault_node2.split('.')[1] and int(fault_node1.split('.')[1]) < int(fault_node2.split('.')[1])  :
                llg_nodes.append((fault_node1+'.'+fault_node1.split('.')[1], fault_node2+'.0'))
                
        # Keep track of number of simulations (for debugging purpose)
        count_llg=0
        
        for llg_node in tqdm(llg_nodes,desc="LLG Fault Simulation"):
            self.dss.circuit_set_active_bus(llg_node[0].split(".")[0])
            fault_name= llg_node[0].split('.')[0]+'_'+llg_node[0].split('.')[1]+llg_node[1].split('.')[1]+'g'
            if len(self.dss.bus_nodes())==3:
                for idx,fr in enumerate(self.fault_information.fault_resistances):
                                        
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={llg_node[0]} Bus2={llg_node[1]} Phases=2 r={fr} '                
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'                                                   
                    self.dss.text(fault_command)                                                                                                    
                    self.dss.text(f'Solve mode=direct')                                                                                            
                    self.dataset.append(self.get_features())                                                                                    
                    self.dataset_llg.append(self.get_features())
                    self.fault_detection_labels.append(1)
                    self.fault_class_labels.append(self.fault_class_map['LLG'])                                                                                                                        
                    self.fault_location_labels.append(self.feeder.bus_id_map[llg_node[0].split('.')[0]])                                       
                    self.fault_resistance_labels.append(fr)                                                                                    
                    self.dss.circuit_set_active_element(fault_obj)
                    self.fault_currents_labels.append(abs(self.dss.cktelement_currents()[0]))                                                                                  
                    # Execute the fault object deactivation command   
                    self.dss.text(fault_obj_deactivate_command)                                                                                            
                    # Increment count of simulations performed
                    count_llg+=1                                                                
    
    def fault_simulation_lll(self):
        """Perform LLL fault simulation
        """
        lll_nodes=[]

        for bus_name in self.feeder.bus_list:
            self.dss.circuit_set_active_bus(bus_name)
            if len(self.dss.bus_nodes())==3:
                lll_nodes.append((bus_name+".1.2.3", bus_name+".4.4.4"))
    
        count_lll=0

        for lll_node in tqdm(lll_nodes,desc="LLL Fault Simulation"):
            self.dss.circuit_set_active_bus(lll_node[0].split(".")[0])
        
            fault_name= lll_node[0].split('.')[0]+'_'+'123'
       
            if len(self.dss.bus_nodes())==3:
                for idx,fr in enumerate(self.fault_information.fault_resistances):
        
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={lll_node[0]} Bus2={lll_node[1]} Phases=3 r={fr} '               
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'                                                   
                    
                    self.dss.text(fault_command)                                                                                                    
                    self.dss.text(f'Solve mode=direct')
                    self.dataset.append(self.get_features())                                                                                    
                    self.dataset_lll.append(self.get_features())
                    self.fault_detection_labels.append(1)
                    self.fault_class_labels.append(self.fault_class_map['LLL'])                                                                                                                        
                    self.fault_location_labels.append(self.feeder.bus_id_map[lll_node[0].split('.')[0]])                                       
                    self.fault_resistance_labels.append(fr)                                                                                    
                    self.dss.circuit_set_active_element(fault_obj)
                    self.fault_currents_labels.append(abs(self.dss.cktelement_currents()[0]))                                                                                  
                    # Execute the fault object deactivation command   
                    self.dss.text(fault_obj_deactivate_command)                                                                                            
                    # Increment count of simulations performed
                    count_lll+=1                                                                                                                                       
               
    
    def fault_simulation_lllg(self):
        """Perfrom LLLG Fault Simulation
        """
        lllg_nodes=[]

        for bus_name in self.feeder.bus_list:
            self.dss.circuit_set_active_bus(bus_name)
            if len(self.dss.bus_nodes())==3:
                lllg_nodes.append(bus_name+".1.2.3")
                
            
        count_lllg=0

        for lllg_node in tqdm(lllg_nodes,desc="LLLG Fault Simulation"):
            self.dss.circuit_set_active_bus(lllg_node.split(".")[0])
            
            fault_name= lllg_node.split('.')[0]+'_'+'123g'
                        
            if len(self.dss.bus_nodes())==3:
                for idx,fr in enumerate(self.fault_information.fault_resistances):
                                        
                    fault_obj=f'Fault.{fault_name}_{str(idx)}'
                    fault_command = f'New Fault.{fault_name}_{str(idx)} Bus1={lllg_node} Phases=3 r={fr} '                                     
                    fault_obj_deactivate_command=f'Fault.{fault_name}_{str(idx)}.enabled=NO'    
                    
                    
                    self.dss.text(fault_command)                                                                                                    
                    self.dss.text(f'Solve mode=direct')
                    self.dataset.append(self.get_features())                                                                                    
                    self.dataset_lllg.append(self.get_features())
                    self.fault_detection_labels.append(1)
                    self.fault_class_labels.append(self.fault_class_map['LLLG'])                                                                                                                        
                    self.fault_location_labels.append(self.feeder.bus_id_map[lllg_node.split('.')[0]])                                       
                    self.fault_resistance_labels.append(fr)                                                                                    
                    self.dss.circuit_set_active_element(fault_obj)
                    self.fault_currents_labels.append(abs(self.dss.cktelement_currents()[0]))                                                                                  
                    # Execute the fault object deactivation command   
                    self.dss.text(fault_obj_deactivate_command)                                                                                            
                    # Increment count of simulations performed
                    count_lllg+=1                                                                                          
                    
    def non_fault_simulation(self):
            
        lds= self.fault_information.load_values 
        loads=self.feeder.connected_loads_name
        
        for ld in tqdm(lds,desc="Non Fault Event Simulation"):
            for load in loads:
                self.dss.text(f'{load}.KW={str(ld)}')  
                                
            self.dss.text(f'Solve mode=direct')                                                                                            
            self.dataset_non_fault.append(self.get_features())
            self.dataset.append(self.get_features())                                                                                   
           
            self.fault_detection_labels.append(0)
            self.fault_class_labels.append(self.fault_class_map['Non_Fault']) 
            self.fault_location_labels.append(-100)                                                                                                                               
            self.fault_resistance_labels.append(0)
            self.fault_currents_labels.append(0)                                                                                               
                                                                                         
    
    def get_dataset(self,print_info=True):
        """Return the dataset
        """
        if print_info:
            print('Dataset Information:')
            print('---------------------')
            
            print(f'Dataset Shape:{self.standardize(np.stack(self.dataset)).shape} \n',color='yellow')
            
            print("Fault Detection Label Information",color='green',format='bold')
            print('---------------------------------',color='green')
            print(f"Count: {len(self.fault_detection_labels)}", tag='Fault Detection', tag_color='green', color='white')
            print(f"Class Count: {len(set(self.fault_detection_labels))}", tag='Fault Detection', tag_color='green', color='white')
            print(f"Per Class Count: {Counter(self.fault_detection_labels)} \n", tag='Fault Detection', tag_color='green', color='white')
            
            print("Fault Location Label Information",color='purple',format='bold')
            print('---------------------------------',color='purple')
            print(f"Count: {len(self.fault_location_labels)}", tag='Fault Location', tag_color='purple', color='white')
            print(f"Class Count: {len(set(self.fault_location_labels))}", tag='Fault Location', tag_color='purple', color='white')
            print(f"Per Class Count: {Counter(self.fault_location_labels)}\n", tag='Fault Location', tag_color='purple', color='white')
            
            
            print("Fault Class Label Information",color='blue',format='bold')
            print('---------------------------------',color='blue')
            print(f"Count: {len(self.fault_class_labels)}", tag='Fault Class', tag_color='blue', color='white')
            print(f"Class Count: {len(set(self.fault_class_labels))}", tag='Fault Class', tag_color='blue', color='white')
            print(f"Per Class Count: {Counter(self.fault_class_labels)}\n", tag='Fault Class', tag_color='blue', color='white')
            
            print("Fault Resistance Label Information",color='cyan',format='bold')
            print('---------------------------------',color='cyan')
            print(f"Count: {len(self.fault_resistance_labels)}", tag='Fault Resistance', tag_color='cyan', color='white')
            print(f"Max Resistance: {max(self.fault_resistance_labels)}", tag='Fault Resistance', tag_color='cyan', color='white')
            print(f"Min Resistance: {min(self.fault_resistance_labels)}\n", tag='Fault Resistance', tag_color='cyan', color='white')
            
            
            print("Fault Current Label Information",color='red',format='bold')
            print('---------------------------------',color='red')
            print(f"Count: {len(self.fault_currents_labels)}", tag='Fault Current', tag_color='red', color='white')
            print(f"Max Current: {max(self.fault_currents_labels)}", tag='Fault Current', tag_color='red', color='white')
            print(f"Min Current: {min(self.fault_currents_labels)}\n", tag='Fault Current', tag_color='red', color='white')
                        
        return self.standardize(np.stack(self.dataset)),self.fault_detection_labels,self.fault_location_labels,self.fault_class_labels,self.fault_resistance_labels,self.fault_currents_labels