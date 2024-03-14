# Imports
# Local Imports
from opendss_utils import OpenDSS, exclude_buses
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
    
    # Get all name of the bus
    bus_list = dss.circuit_all_bus_names() 
    
    
    # Set an active bus 
    dss.circuit_set_active_bus('149_1') 
    
    # Set the solve mode to dynamics  
    dss.text(f"Solve mode=dynamics number=10 stepsize=0.0002")
     
    dss.text(f"New Fault.149_1 Bus1=149.1 phases=1  r=0.1")
    dss.text(f"Solve number=500") 
    dss.text(f"Fault.149_1.enabled=NO")

    

if __name__ == "__main__":
    main()
    





