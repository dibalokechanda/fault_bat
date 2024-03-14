import subprocess

FEEDER_SYSTEM='123Bus' # Change to select different feeder systems

if FEEDER_SYSTEM=="123Bus":
    command = [
        'python', 'main.py',
        '--feeder', '123Bus',
        '--feeder-file', 'IEEE123Master.dss',
        '--folder', 'initial'
    ]
elif FEEDER_SYSTEM=="34Bus":
        command = [
        'python', 'main.py',
        '--feeder', '34Bus',
        '--feeder-file', 'Run_IEEE34Mod1.dss',
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
