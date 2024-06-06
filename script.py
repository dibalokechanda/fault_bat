import subprocess

FEEDER_SYSTEM='8500-Node' # Change to select different feeder systems

if FEEDER_SYSTEM=="8500-Node":
    command = [
        'python', 'main_dataset_generation.py',
        '--feeder', '8500-Node',
        '--feeder-file', 'RUN_8500Node.dss',
        '--folder', 'initial',
        '--fault-resistance-type','variable',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end','20',
        '--number-of-samples-for-each-node','1',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'
    ] 

elif FEEDER_SYSTEM=="123Bus":
    command = [
        'python', 'main_dataset_generation.py',
        '--feeder', '123Bus',
        '--feeder-file', 'IEEE123Master.dss',
        '--folder', '123Bus_Dataset',
        '--fault-resistance-type','variable',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end','20',
        '--number-of-samples-for-each-node','10',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'
    ]
    
elif FEEDER_SYSTEM=="37Bus":
       command = [
        'python', 'main_dataset_generation.py',
        '--feeder', '37Bus',
        '--feeder-file', 'ieee37.dss',
        '--fault-resistance-type','fixed',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end', '20',
        '--folder', '37Bus_Dataset',
        '--number-of-samples-for-each-node','10',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'
    ]
elif FEEDER_SYSTEM=="34Bus":
        command = [
        'python', 'main_dataset_generation.py',
        '--feeder', '34Bus',
        '--feeder-file', 'Run_IEEE34Mod1.dss',
        '--fault-resistance-type','fixed',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end', '20',
        '--folder', '34Bus_Dataset' ,
        '--number-of-samples-for-each-node','10',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'   
    ]
        
elif FEEDER_SYSTEM=="13Bus":
     command = [
        'python','main_dataset_generation.py',
        '--feeder', '13Bus',
        '--feeder-file', 'IEEE13Nodeckt.dss',
        '--fault-resistance-type','fixed',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end', '20',
        '--folder', '13Bus_Dataset' ,
        '--number-of-samples-for-each-node','10',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'  
    ]
    
subprocess.run(command)
