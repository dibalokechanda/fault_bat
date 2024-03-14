# Imports
# Local Imports
from opendss_utils import OpenDSS, exclude_buses, get_buses_by_phase, get_connectivity_info, get_resistance_values
from arguments import parse_args

# Main Function
def main():
    # Handle the arguments passed in 
    argument_parser=parse_args()       
    argument_parser.dump_json()
    args=argument_parser.get_args()
    
    # Initialize the OpenDSS object and get the file path
    dss, dss_file=OpenDSS(args.feeder,args.feeder_file).get_dss_obj()
    
    # Compile the dss file and solve power flow 
    dss.text(f"compile [{dss_file}]")
    dss.text(f"solve")
    
    # Get name of all the buses
    bus_list = dss.circuit_all_bus_names() 
      
    # Exclude Buses to get the updated bus list
    updated_bus_list=exclude_buses(args.feeder,bus_list)
    
    # Get Buslist by number of phases
    bus_list_1_phase, bus_list_2_phases,bus_list_3_phases=get_buses_by_phase(dss,updated_bus_list)
    
    # Get connectivity info of the feeder system
    edge_list_by_bus_id,edge_list_by_bus_name,bus_id_map=get_connectivity_info(dss,updated_bus_list)
    
    get_resistance_values(dss,args)
    

    

if __name__ == "__main__":
    main()
    





