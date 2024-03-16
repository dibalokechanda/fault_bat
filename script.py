import subprocess

FEEDER_SYSTEM='123Bus' # Change to select different feeder systems

if FEEDER_SYSTEM=="123Bus":
    command = [
        'python', 'main.py',
        '--feeder', '123Bus',
        '--feeder-file', 'IEEE123Master.dss',
        '--folder', 'initial',
        '--fault-resistance-type','variable',
        '--fault-resistance-value','20',
        '--fault-resistance-lower-end', '0.05',
        '--fault-resistance-upper-end','20',
        '--number-of-samples-for-each-node','100',
        '--change-load-values','yes',
        '--load-value-KW-lower-end','20',
        '--load-value-KW-upper-end','80'
    ]
    
elif FEEDER_SYSTEM=="37Bus":
       command = [
        'python', 'main.py',
        '--feeder', '37Bus',
        '--feeder-file', 'ieee37.dss',
        '--fault-resistance-type','fixed',
        '--fault-resistance-value',20,
        '--fault-resistance-lower-end', 0.05,
        '--fault-resistance-upper-end', 20,
        '--folder', 'initial'
    
    ]
elif FEEDER_SYSTEM=="34Bus":
        command = [
        'python', 'main.py',
        '--feeder', '34Bus',
        '--feeder-file', 'Run_IEEE34Mod1.dss',
        '--fault-resistance-type','fixed',
        '--fault-resistance-value',20,
        '--fault-resistance-lower-end', 0.05,
        '--fault-resistance-upper-end', 20,
        '--folder', 'initial'    
    ]
        
elif FEEDER_SYSTEM=="13Bus":
     command = [
        'python', 'main.py',
        '--feeder', '13Bus',
        '--feeder-file', 'IEEE13Nodeckt.dss',
        '--folder', 'initial'
    ]
    
subprocess.run(command)
