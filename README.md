# Graph Dataset Generation for Multi-task Fault Diagnosis
This repository holds the code to generate the dataset for fault diagnosis in a power distribution system. For the moment, the following feeder systems are included.

- 13 BUS 
- 34 BUS
- 37 BUS
- 123 BUS
- 8500 NODE

Learn more about these feeder systems from these resources [[1](https://ieeexplore.ieee.org/abstract/document/119237)], [[2](https://ieeexplore.ieee.org/abstract/document/8063903)], [[3](https://cmte.ieee.org/pes-testfeeders/resources/)]. 

# Generated Files Description

As an example see the 37Bus system [folder](https://github.com/dibalokechanda/fault_bat/tree/main/37Bus_Dataset).

 - `dataset.npy`: This contains the feature tensor with dimensions *Number of Samples X Number of Nodes in the feeder system X 6*

 - `edge_list.npy`: This contains the edge list matrix which is the graph connectivity information. This can processed with libraries like `NetworkX` to generate the graph representing the distribution system.

 - `fault_detection_labels.npy`: This contains the binary fault detection labels. For a fault event, the label is $1$ and for a non-fault event, the label is $0$.

 - `fault_location_labels.npy`: This contains the fault location label for three-phase nodes in the distribution system. The location labels is encoded to an integer value. Use `bus_id_map` to see which bus name corresponds to which integer value.

 - `fault_class_labels.npy`: This contains the fault classification label for a fault event. The fault classes are encoded as follows
    
    - Line-to-Ground (LG) : 0
    - Line-to-Line (LL) : 1
    - Line-to-Line-to-Ground (LLG) : 2
    - Line-to-Line-to-Line (LLL) : 3
    - Line-to-Line-to-Line-to-Ground (LLLG) : 4
    - Non-Fault Event : 5 
- `fault_resistance_labels.npy`: This contains the numerical value for fault resistance for the fault event. We recommend normalizing the value before using it in a regression task. 

- `fault_currents_labels.npy`: This contains the numerical value for the fault current for the fault event. We strongly recommend normalizing the value before using it as the range and variance are large.

- `1_hop_by_bus_name.npy` : This holds the one-hop neighborhood node name for all the nodes in the feeder system.

- `2_hop_by_bus_name.npy` : This holds the two-hop neighborhood node name for all the nodes in the feeder system.

- `bus_id_map.npy` : This holds the mapping between bus names and the corresponding unique integer id. 

The other files contain the metadata for simulation settings and the feeder system.

- `feeder_infos`: A json file that contains the feeder information. 
- `X_Dataset`: Contains the simulation parameters

## Generated  Dataset Folder Structure

As an example, the folder structure for the 37Bus is shown below.


```text
37Bus_Dataset
├── dataset
│   ├── dataset.npy
│   ├── edge_list.npy
|   ├── fault_detection_labels.npy
|   ├── fault_location_labels.npy
|   ├── fault_class_labels.npy
|   ├── fault_resistance_labels.npy
|   ├── fault_currents_labels.npy
|   ├── 1_hop_by_bus_name.npy
|   ├── 2_hop_by_bus_name.npy
│   └── bus_id_map.npy
|  
├── 37Bus_Dataset
└── feeder_infos
```

# Steps to Generate the Dataset
### Clone the repo and install packages

Clone the repository with the following command 


```bash
git clone https://github.com/dibalokechanda/fault_bat.git
```

Then `cd` into the root of the directory. Install the packages from the requirements.txt file with the following command. We highly recommend using a virtual environment to avoid package conflicts.

```bash
pip install -r requirements.txt
```

**Important Note**: This code is implemented using `py_dss_interface==1.0.2` which is the older version.

### Specify necessary parameters in `script.py`

To change between feeder systems update the `FEEDER_SYSTEM` variable. For more granular control modify the `command` list in the `script.py` file. As an example consider IEEE-37 Bus system:

```python
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
```

These are the command line arguments for running the code. Following is an explanation for  each argument:

- `python`: This means executing a Python script.
- `main_dataset_generation.py`: The path to the main file.
- `--feeder`: Name of the folder that contains the feeder files. Make sure it matches the folder name under `./feeders`
- `--feeder-file`: The main file to execute for simulating the feeder system.

- `--fault-resistance-type`:  If the fault resistance is variable or fixed. We just exploring the research works in graph-based fault diagnosis in distribution systems to decide on this parameter.

- `--fault-resistance-value`: If the fault resistance value is fixed, the value of the fault resistance.

- `--fault-resistance-lower-end`: If the fault resistance is variable, it will be sampled from a uniform distribution. This parameter defines the lower end of that uniform distribution.

- `--fault-resistance-upper-end`: If the fault resistance is variable, it will be sampled from a uniform distribution. This parameter defines the upper end of that uniform distribution.

- `--folder`: Name of the folder to save the generated dataset.

- `--number-of-samples-for-each-node`: For each node in the feeder system, how many data points are to be generated.

- `--change-load-values`: If the load value needs to be changed or not. We recommend setting it to 'yes' if you plan to use the dataset for fault detection. Changing the load value simulates a non-fault event.

- `--load-value-KW-lower-end`: The load value is sampled from a uniform distribution. This parameter defines the lower end of the uniform distribution.

- `--load-value-KW-upper-end`: The load value is sampled from a uniform distribution. This parameter defines the upper end of the uniform distribution.

### Execute the code

To execute the code run the following command 

```bash
python .\script.py
```

# References

[1] [Kersting, William H. "Radial distribution test feeders." IEEE Transactions on Power Systems 6, no. 3 (1991): 975-985.](https://ieeexplore.ieee.org/abstract/document/119237)

[2] [Schneider, Kevin P., B. A. Mather, Bikash Chandra Pal, C-W. Ten, Greg J. Shirek, Hao Zhu, Jason C. Fuller et al. "Analytic considerations and design basis for the IEEE distribution test feeders." IEEE Transactions on power systems 33, no. 3 (2017): 3181-3188.](https://ieeexplore.ieee.org/abstract/document/8063903)

[3] [https://cmte.ieee.org/pes-testfeeders/resources/](https://cmte.ieee.org/pes-testfeeders/resources/)

