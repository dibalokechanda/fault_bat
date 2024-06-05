# Graph Dataset Generation for Multi-task Fault Diagnosis
This repository holds the code to generate the dataset for fault diagnosis in a power distribution system. For the moment, the following feeder systems are included.

- 13 BUS 
- 34 BUS
- 37 BUS
- 123 BUS
- 123 BUS
- 8500 BUS

Learn more about these feeder systems from these resources [[1](https://ieeexplore.ieee.org/abstract/document/119237)], [[2](https://ieeexplore.ieee.org/abstract/document/8063903)], [[3](https://cmte.ieee.org/pes-testfeeders/resources/)]. 

# Generate Files Description

 - `dataset.npy`: This contains the feature tensor with dimensions *Number of Samples X Number of Nodes in the feeder system X 6*

 - `edge_list.npy`: This contains the edge list matrix which contains the graph connectivity information. This can processed with libraries like `NetworkX` to generate the graph representing the distribution system.

 - `fault_detection_labels.npy`: This contains the binary fault detection labels. For a fault event, the label is $1$ and for a non-fault event, the label is $0$.

 - `fault_location_labels.npy`: This contains the fault location label for three-phase nodes in the distribution system. 

 - `fault_class_labels.npy`: This contains the fault classification label for a fault event. The fault classes are encoded as follows
    
    - Line-to-Ground (LG) : 0
    - Line-to-Line (LL) : 1
    - Line-to-Line-to-Ground (LLG) : 2
    - Line-to-Line-to-Line (LLL) : 3,
    - Line-to-Line-to-Line-to-Ground (LLLG) : 4
    - Non_Fault:5 
- `fault_resistance_labels.npy`: This contains the numerical value for fault resistance for the fault event. We recommend normalizing the value before using it in a regression task. 

- `fault_currents_labels.npy`: This contains the numerical value for the fault current for the fault event. We strongly recommend normalizing the value before using it as the range and variance are large.


## Generated  Dataset Folder Structure

```text
37Bus_Dataset
├── dataset
│   ├── dataset.npy
│   ├── edge_list.npy
|   ├── fault_detection_labels.npy
|   ├── fault_location_labels.npy
|   ├── fault_class_labels.npy
|   ├── fault_resistance_labels.npy
│   └── fault_currents_labels.npy
|  
├── 37Bus_Dataset
└── feeder_infos
```

### Clone the repo and install packages

Clone the repository with the following command 


```bash
git clone https://github.com/dibalokechanda/fault_bat.git
```

Then `cd` into the root of the directory .

Install the packages from the requirements.txt file with the following command. We highly recommend using a virtual environment to avoid package conflicts.


```bash
pip install -r requirements.txt
```

**Import Note**: This code is implemented using `py_dss_interface==1.0.2` which is the older version.

### Specify necessary parameters in `script.py`

To change between feeder systems update the `FEEDER_SYSTEM` variable. For more granular control modify the `command` list in the `script.py` file. As an example consider IEEE-37 Bus system:

```python



```

### Execute the code

To execute the code run the following command 

```bash
python .\script.py
```

# References

[1] [Kersting, William H. "Radial distribution test feeders." IEEE Transactions on Power Systems 6, no. 3 (1991): 975-985.](https://ieeexplore.ieee.org/abstract/document/119237)

[2] [Schneider, Kevin P., B. A. Mather, Bikash Chandra Pal, C-W. Ten, Greg J. Shirek, Hao Zhu, Jason C. Fuller et al. "Analytic considerations and design basis for the IEEE distribution test feeders." IEEE Transactions on power systems 33, no. 3 (2017): 3181-3188.](https://ieeexplore.ieee.org/abstract/document/8063903)

[3] [https://cmte.ieee.org/pes-testfeeders/resources/](https://cmte.ieee.org/pes-testfeeders/resources/)

